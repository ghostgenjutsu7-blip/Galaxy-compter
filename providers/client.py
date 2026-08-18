"""providers/client.py — unified LLM client with retry, key rotation, logging.

Every agent calls LLMClient.complete(). The client:
- Resolves (provider, model, key) via ProviderManager.best_available(agent).
- Routes Galaxy Echo calls to the in-process EchoProvider (no network).
- Routes everything else to the OpenAI-compatible SDK against the provider's
  base_url with the decrypted key.
- On rate-limit/timeout errors, rotates keys / falls back per §15.
- Logs a redacted LLM-call record (prompt hash only, never content) for /debug.

There is no internal spend or rate-limit budget here by design (§12) — caps
belong to the provider, set at the API-key level. The only thing this client
does about a rate-limit error is react to it like any other transient
failure: rotate to the next key/provider in the chain.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from typing import Any

from .echo import EchoProvider
from .manager import get_provider_manager

_echo = EchoProvider()


class LLMError(Exception):
    """Raised when an LLM call fails after all retries / rotation."""

    def __init__(self, message: str, *, kind: str = "unknown",
                 provider: str = "", model: str = "") -> None:
        super().__init__(message)
        self.kind = kind  # rate_limit | timeout | provider_down | content_filter | overflow | malformed
        self.provider = provider
        self.model = model


@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    finish_reason: str
    raw: dict[str, Any]
    key_alias: str = ""


class LLMClient:
    """Async LLM client. One instance shared app-wide."""

    def __init__(self) -> None:
        self._pm = get_provider_manager()
        self._call_log: list[dict[str, Any]] = []
        self._call_log_path = None  # set on first call via config

    async def complete(self, *, agent: str, messages: list[dict[str, str]],
                       max_tokens: int = 1024, temperature: float = 0.0,
                       response_format: dict | None = None,
                       tools: list[dict[str, Any]] | None = None,
                       tool_choice: str | dict | None = None) -> LLMResponse:
        """Run one completion with full retry/rotation. Raises LLMError on
        terminal failure."""
        attempts: list[tuple[str, str]] = []
        # build attempt chain: primary + fallbacks + echo
        pm = self._pm
        primary = pm.get_agent_model(agent)
        chain: list[tuple[str, str]] = []
        if primary:
            chain.append(primary)
        chain.extend(pm.get_fallback_chain(agent))
        if os.environ.get("GAX_STRICT_PROVIDER") != "1" and ("Galaxy Echo", "galaxy-echo") not in chain:
            chain.append(("Galaxy Echo", "galaxy-echo"))

        last_err: LLMError | None = None
        for provider_name, model in chain:
            attempts.append((provider_name, model))
            try:
                return await self._call_once(
                    provider_name, model, agent, messages,
                    max_tokens, temperature, response_format, tools, tool_choice,
                )
            except LLMError as e:
                last_err = e
                # rate-limit & provider-down rotate to next in chain; others
                # rotate too in this faithful implementation but record kind.
                if e.kind in ("overflow", "malformed") and provider_name == "Galaxy Echo":
                    # echo never overflows; if it claims to, that's a bug — re-raise
                    raise
                continue
        raise last_err or LLMError("no providers available")

    async def _call_once(self, provider_name: str, model: str, agent: str,
                         messages: list[dict[str, str]], max_tokens: int,
                         temperature: float, response_format: dict | None,
                         tools: list[dict[str, Any]] | None,
                         tool_choice: str | dict | None,
                         ) -> LLMResponse:
        pm = self._pm
        provider = pm.get_provider(provider_name)
        if provider is None:
            raise LLMError(f"unknown provider {provider_name!r}", kind="provider_down",
                           provider=provider_name, model=model)

        if provider_name == "Galaxy Echo":
            return self._call_echo(model, agent, messages, max_tokens,
                                   temperature, response_format, tools, tool_choice)

        key = pm.pick_key(provider_name, agent=agent)
        if key is None:
            raise LLMError(f"no key for {provider_name}", kind="provider_down",
                           provider=provider_name, model=model)
        secret = self._decrypt_key(key.encrypted_secret)

        start = time.time()
        try:
            from openai import (
                APIConnectionError,
                APIError,
                APITimeoutError,
                AsyncOpenAI,
                RateLimitError,
            )
        except Exception as e:  # pragma: no cover — openai is a hard dep
            raise LLMError(f"openai SDK unavailable: {e}", kind="provider_down",
                           provider=provider_name, model=model)
        client = AsyncOpenAI(base_url=provider.base_url, api_key=secret, timeout=60.0)
        try:
            kwargs: dict[str, Any] = {
                "model": model, "messages": messages, "max_tokens": max_tokens,
                "temperature": temperature,
            }
            # Kilo Gateway currently rejects OpenAI's response_format=json_object
            # parameter. Its model can still follow an explicit JSON instruction
            # in the prompt, so omit only this optional transport field there.
            if response_format and provider_name != "Kilo Gateway":
                kwargs["response_format"] = response_format
            if tools:
                kwargs["tools"] = tools
            if tool_choice:
                kwargs["tool_choice"] = tool_choice
            resp = await client.chat.completions.create(**kwargs)
        except RateLimitError as e:
            pm.record_key_error(provider_name, key.id)
            raise LLMError(str(e), kind="rate_limit",
                           provider=provider_name, model=model) from e
        except APITimeoutError as e:
            pm.record_key_error(provider_name, key.id)
            raise LLMError(str(e), kind="timeout",
                           provider=provider_name, model=model) from e
        except APIConnectionError as e:
            pm.record_key_error(provider_name, key.id)
            raise LLMError(str(e), kind="provider_down",
                           provider=provider_name, model=model) from e
        except APIError as e:
            msg = str(e).lower()
            if "context" in msg and "length" in msg:
                raise LLMError(str(e), kind="overflow",
                               provider=provider_name, model=model) from e
            pm.record_key_error(provider_name, key.id)
            raise LLMError(str(e), kind="provider_down",
                           provider=provider_name, model=model) from e

        latency = int((time.time() - start) * 1000)
        text = resp.choices[0].message.content or ""
        usage = resp.usage
        in_t = getattr(usage, "prompt_tokens", 0) or 0
        out_t = getattr(usage, "completion_tokens", 0) or 0
        message = resp.choices[0].message
        raw_tool_calls = []
        for call in (getattr(message, "tool_calls", None) or []):
            raw_tool_calls.append({
                "id": getattr(call, "id", ""),
                "type": getattr(call, "type", "function"),
                "function": {
                    "name": getattr(getattr(call, "function", None), "name", ""),
                    "arguments": getattr(getattr(call, "function", None), "arguments", "{}"),
                },
            })
        result = LLMResponse(
            text=text, model=model, provider=provider_name,
            input_tokens=in_t, output_tokens=out_t, latency_ms=latency,
            finish_reason=resp.choices[0].finish_reason or "stop",
            raw={"tool_calls": raw_tool_calls},
            key_alias=key.alias,
        )
        pm.record_key_success(provider_name, key.id, latency)
        self._record(agent, result, messages)
        return result

    def _call_echo(self, model: str, agent: str, messages: list[dict[str, str]],
                   max_tokens: int, temperature: float,
                   response_format: dict | None,
                   tools: list[dict[str, Any]] | None,
                   tool_choice: str | dict | None) -> LLMResponse:
        start = time.time()
        raw = _echo.complete(messages, model=model, max_tokens=max_tokens,
                             temperature=temperature, response_format=response_format,
                             tools=tools, tool_choice=tool_choice)
        latency = int((time.time() - start) * 1000)
        text = raw["choices"][0]["message"]["content"]
        in_t = raw["usage"]["prompt_tokens"]
        out_t = raw["usage"]["completion_tokens"]
        result = LLMResponse(
            text=text, model=model, provider="Galaxy Echo",
            input_tokens=in_t, output_tokens=out_t, latency_ms=latency,
            finish_reason=raw["choices"][0]["finish_reason"], raw=raw,
        )
        self._record(agent, result, messages)
        return result

    def _decrypt_key(self, blob: str) -> str:
        if not blob:
            return ""
        try:
            from security.secrets_fallback import decrypt_secret
            return decrypt_secret(blob)
        except Exception:
            return blob  # tests may store plaintext

    def _record(self, agent: str, resp: LLMResponse, messages: list[dict[str, str]]) -> None:
        # Prompt content is NEVER stored — only a hash (§11).
        joined = "\n".join(str(m.get("content") or "") for m in messages)
        prompt_hash = hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]
        rec = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "agent": agent, "provider": resp.provider, "model": resp.model,
            "key_alias": resp.key_alias,
            "input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens,
            "latency_ms": resp.latency_ms,
            "prompt_hash": prompt_hash, "finish_reason": resp.finish_reason,
        }
        self._call_log.append(rec)
        # append to on-disk LLM log
        try:
            from config import get_config
            cfg = get_config()
            cfg.home.mkdir(parents=True, exist_ok=True)
            with open(cfg.llm_log, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception:
            pass

    # ---- cost / call-log accessors ---------------------------------------
    def call_log(self) -> list[dict[str, Any]]:
        return list(self._call_log)

    def session_tokens(self) -> tuple[int, int]:
        in_t = sum(r["input_tokens"] for r in self._call_log)
        out_t = sum(r["output_tokens"] for r in self._call_log)
        return in_t, out_t


_client: LLMClient | None = None


def get_llm_client() -> LLMClient:
    global _client
    if _client is None:
        _client = LLMClient()
    return _client


def reset_llm_client_for_tests() -> LLMClient:
    global _client
    _client = LLMClient()
    return _client
