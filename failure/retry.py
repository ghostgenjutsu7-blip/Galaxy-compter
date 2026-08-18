"""failure/retry.py — exponential backoff + fallback chains (§15).

Implements the recovery-strategy table from §15:
  LLM rate limit -> next key, same provider (3 keys)
  LLM provider down -> fallback provider (2)
  LLM timeout -> retry once, then smaller model (2)
  LLM content filter -> re-prompt safe reformulation (3)
  LLM context overflow -> compact, retry (3)
  LLM malformed -> re-prompt schema reminder (2)
  Tool transient -> exponential backoff (3)
  Tool logic -> reflect, alternative (2)
  Tool permission -> escalate (1)
  DB locked -> wait + retry 5s (5)
"""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Callable, Awaitable


@dataclass
class RetryPolicy:
    max_retries: int
    base_delay: float = 0.5
    max_delay: float = 30.0
    backoff_factor: float = 2.0


POLICIES: dict[str, RetryPolicy] = {
    "rate_limit":     RetryPolicy(3, base_delay=1.0),
    "provider_down":  RetryPolicy(2, base_delay=2.0),
    "timeout":        RetryPolicy(2, base_delay=1.0),
    "content_filter": RetryPolicy(3, base_delay=0.5),
    "overflow":       RetryPolicy(3, base_delay=0.0),
    "malformed":      RetryPolicy(2, base_delay=0.0),
    "tool_transient": RetryPolicy(3, base_delay=0.5, max_delay=10.0),
    "tool_logic":     RetryPolicy(2, base_delay=0.0),
    "db_locked":      RetryPolicy(5, base_delay=5.0, max_delay=5.0),
}


def delay_for(policy: RetryPolicy, attempt: int) -> float:
    return min(policy.max_delay, policy.base_delay * (policy.backoff_factor ** attempt))


async def retry_with_backoff(coro_fn: Callable[..., Awaitable[Any]],
                             *, kind: str = "tool_transient",
                             on_retry: Callable[[int, Exception], None] | None = None,
                             **kwargs) -> Any:
    """Retry an async call with exponential backoff per the §15 policy."""
    policy = POLICIES.get(kind, RetryPolicy(3))
    last_err: Exception | None = None
    for attempt in range(policy.max_retries + 1):
        try:
            return await coro_fn(**kwargs)
        except Exception as e:
            last_err = e
            if attempt >= policy.max_retries:
                raise
            if on_retry:
                on_retry(attempt + 1, e)
            await asyncio.sleep(delay_for(policy, attempt))
    raise last_err  # unreachable


def cascading_failure_check(recent_errors: list[str]) -> bool:
    """If 3 consecutive steps failed with similar errors, pause (§15)."""
    if len(recent_errors) < 3:
        return False
    last3 = recent_errors[-3:]
    # "similar" = same error class substring
    return any(e in last3[0] and e in last3[1] and e in last3[2]
               for e in ["rate_limit", "timeout", "db_locked", "provider_down"])
