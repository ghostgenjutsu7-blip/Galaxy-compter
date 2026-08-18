"""providers/manager.py — provider + key registry, rotation, persistence.

Implements §8's multi-key-per-provider design and §19's free-provider tiers.
Keys are stored AES-encrypted (security/secrets_fallback.py handles the actual
encryption); here we store the encrypted blob and the non-secret metadata.
"""

from __future__ import annotations

import threading
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from storage.local import get_storage

# Known free-tier-friendly providers (§19). Used by /setup Free Mode.
KNOWN_PROVIDERS = {
    "NVIDIA NIM": "https://integrate.api.nvidia.com/v1",
    "Kilo Gateway": "https://api.kilo.ai/api/gateway",
    "OpenRouter": "https://openrouter.ai/api/v1",
    "Groq": "https://api.groq.com/openai/v1",
    "Together.ai": "https://api.together.xyz/v1",
    "Fireworks": "https://api.fireworks.ai/inference/v1",
    "Google AI Studio": "https://generativelanguage.googleapis.com/v1beta/openai/",
    "Anthropic": "https://api.anthropic.com/v1",
    "OpenAI": "https://api.openai.com/v1",
    "Ollama (Local)": "http://localhost:11434/v1",
    # The deterministic in-process test provider — never makes a network call.
    "Galaxy Echo": "galaxy-echo://local",
}

FREE_PROVIDERS = {
    "NVIDIA NIM", "Kilo Gateway", "OpenRouter", "Groq", "Together.ai", "Ollama (Local)",
}


@dataclass
class ProviderKey:
    id: int
    alias: str
    status: str  # high | medium | low
    encrypted_secret: str = ""  # ciphertext blob (base64) from secrets_fallback
    tier: str = "paid"  # paid | free — informational label only; Galaxy does not
                        # track spend or rate-limit headroom internally (see §12)
    last_error_ts: float = 0.0
    error_count_5min: list[float] = field(default_factory=list)
    request_count_5min: list[float] = field(default_factory=list)
    latencies_5min: list[tuple[float, int]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("error_count_5min", None)
        d.pop("request_count_5min", None)
        d.pop("latencies_5min", None)
        return d


@dataclass
class Provider:
    name: str
    base_url: str
    keys: list[ProviderKey] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "base_url": self.base_url,
            "keys": [k.to_dict() for k in self.keys],
        }


class ProviderManager:
    """Owns the provider registry. Single instance shared app-wide."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._providers: dict[str, Provider] = {}
        # default agent -> (provider, model) assignments (§19)
        self._agent_models: dict[str, tuple[str, str]] = {}
        # optional explicit agent -> (provider, key_id) assignment
        self._agent_keys: dict[str, tuple[str, int]] = {}
        # fallback chain per agent: list of (provider, model)
        self._fallbacks: dict[str, list[tuple[str, str]]] = {}
        self._load()

    # ---- persistence -------------------------------------------------------
    def _load(self) -> None:
        st = get_storage()
        rows = st.query_all("SELECT * FROM providers ORDER BY name;")
        for r in rows:
            p = Provider(name=r["name"], base_url=r["base_url"])
            krows = st.query_all(
                "SELECT * FROM provider_keys WHERE provider=? ORDER BY id;",
                (r["name"],),
            )
            for kr in krows:
                p.keys.append(ProviderKey(
                    id=kr["id"], alias=kr["alias"], status=kr["status"],
                    encrypted_secret=kr["encrypted_secret"] or "",
                    tier=kr["tier"] or "paid",
                ))
            self._providers[p.name] = p
        am = st.query_all("SELECT * FROM agent_models;")
        for r in am:
            self._agent_models[r["agent"]] = (r["provider"], r["model"])
        try:
            ak = st.query_all("SELECT agent, provider, key_id FROM agent_provider_keys;")
        except Exception:
            ak = []
        for r in ak:
            self._agent_keys[r["agent"]] = (r["provider"], int(r["key_id"]))
        fb = st.query_all("SELECT * FROM agent_fallbacks ORDER BY agent, position;")
        for r in fb:
            self._fallbacks.setdefault(r["agent"], []).append((r["provider"], r["model"]))
        # Always ensure the echo provider exists in-memory even if not persisted
        if "Galaxy Echo" not in self._providers:
            self._providers["Galaxy Echo"] = Provider(name="Galaxy Echo", base_url="galaxy-echo://local")
            self._providers["Galaxy Echo"].keys.append(ProviderKey(
                id=1, alias="echo-local", status="high", tier="free", encrypted_secret="",
            ))

    # ---- registry ----------------------------------------------------------
    def list_providers(self) -> list[Provider]:
        with self._lock:
            return list(self._providers.values())

    def get_provider(self, name: str) -> Provider | None:
        with self._lock:
            return self._providers.get(name)

    def add_provider(self, name: str, base_url: str) -> Provider:
        with self._lock:
            p = Provider(name=name, base_url=base_url)
            self._providers[name] = p
            st = get_storage()
            with st.transaction() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO providers(name, base_url) VALUES(?,?);",
                    (name, base_url),
                )
            return p

    def remove_provider(self, name: str) -> bool:
        if name == "Galaxy Echo":
            return False  # never remove the test provider
        with self._lock:
            if name not in self._providers:
                return False
            del self._providers[name]
            st = get_storage()
            with st.transaction() as conn:
                conn.execute("DELETE FROM providers WHERE name=?;", (name,))
                conn.execute("DELETE FROM provider_keys WHERE provider=?;", (name,))
                conn.execute("DELETE FROM agent_models WHERE provider=?;", (name,))
                conn.execute("DELETE FROM agent_fallbacks WHERE provider=?;", (name,))
            return True

    # ---- keys --------------------------------------------------------------
    def add_key(self, provider: str, alias: str, encrypted_secret: str,
                tier: str = "paid", status: str = "high") -> ProviderKey:
        with self._lock:
            p = self._providers.get(provider)
            if p is None:
                raise KeyError(f"unknown provider {provider!r}")
            st = get_storage()
            with st.transaction() as conn:
                row = conn.execute(
                    "SELECT COALESCE(MAX(id),0)+1 AS next_id FROM provider_keys WHERE provider=?;",
                    (provider,),
                ).fetchone()
                next_id = int(row["next_id"])
                conn.execute(
                    "INSERT INTO provider_keys(provider,id,alias,status,encrypted_secret,tier) "
                    "VALUES(?,?,?,?,?,?);",
                    (provider, next_id, alias, status, encrypted_secret, tier),
                )
            key = ProviderKey(id=next_id, alias=alias, status=status,
                              encrypted_secret=encrypted_secret, tier=tier)
            p.keys.append(key)
            return key

    def remove_key(self, provider: str, key_id: int) -> bool:
        with self._lock:
            p = self._providers.get(provider)
            if p is None:
                return False
            p.keys = [k for k in p.keys if k.id != key_id]
            st = get_storage()
            with st.transaction() as conn:
                conn.execute(
                    "DELETE FROM provider_keys WHERE provider=? AND id=?;",
                    (provider, key_id),
                )
            return True

    # ---- agent -> model assignment ----------------------------------------
    def set_agent_model(self, agent: str, provider: str, model: str) -> None:
        with self._lock:
            self._agent_models[agent] = (provider, model)
            st = get_storage()
            with st.transaction() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO agent_models(agent,provider,model) VALUES(?,?,?);",
                    (agent, provider, model),
                )

    def get_agent_model(self, agent: str) -> tuple[str, str] | None:
        with self._lock:
            return self._agent_models.get(agent)

    def set_agent_key(self, agent: str, provider: str, key_id: int) -> None:
        """Pin one agent to one provider key while preserving model assignment."""
        with self._lock:
            if self._providers.get(provider) is None:
                raise KeyError(f"unknown provider {provider!r}")
            if self._key(provider, int(key_id)) is None:
                raise KeyError(f"unknown key {provider!r}:{key_id}")
            key = (provider, int(key_id))
            self._agent_keys[agent] = key
            st = get_storage()
            with st.transaction() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO agent_provider_keys(agent,provider,key_id) VALUES(?,?,?);",
                    (agent, provider, int(key_id)),
                )

    def clear_agent_key(self, agent: str) -> None:
        with self._lock:
            self._agent_keys.pop(agent, None)
            st = get_storage()
            with st.transaction() as conn:
                conn.execute("DELETE FROM agent_provider_keys WHERE agent=?;", (agent,))

    def get_agent_key(self, agent: str) -> tuple[str, int] | None:
        with self._lock:
            return self._agent_keys.get(agent)

    def set_fallback_chain(self, agent: str, chain: list[tuple[str, str]]) -> None:
        with self._lock:
            self._fallbacks[agent] = list(chain)
            st = get_storage()
            with st.transaction() as conn:
                conn.execute("DELETE FROM agent_fallbacks WHERE agent=?;", (agent,))
                for pos, (prov, model) in enumerate(chain):
                    conn.execute(
                        "INSERT INTO agent_fallbacks(agent,position,provider,model) VALUES(?,?,?,?);",
                        (agent, pos, prov, model),
                    )

    def get_fallback_chain(self, agent: str) -> list[tuple[str, str]]:
        with self._lock:
            return list(self._fallbacks.get(agent, []))

    # ---- rotation ----------------------------------------------------------
    def pick_key(self, provider: str, headroom_fn=None, agent: str | None = None) -> ProviderKey | None:
        """Pick the best key for a provider. Highest-status key with the most
        headroom wins; headroom_fn(key) -> 0..1 if supplied. Returns None if
        the provider has no keys (caller should fall back to another provider
        or use the echo provider)."""
        with self._lock:
            p = self._providers.get(provider)
            if not p or not p.keys:
                return None
            if agent:
                assigned = self._agent_keys.get(agent)
                if assigned and assigned[0] == provider:
                    assigned_key = next((k for k in p.keys if k.id == assigned[1]), None)
                    if assigned_key is None:
                        return None
                    self._trim_health(assigned_key, time.time())
                    total = len(assigned_key.request_count_5min)
                    failures = len(assigned_key.error_count_5min)
                    if total >= 4 and failures / total >= 0.25:
                        return None
                    return assigned_key
            status_rank = {"high": 3, "medium": 2, "low": 1}
            now = time.time()
            scored = []
            for k in p.keys:
                self._trim_health(k, now)
                total = len(k.request_count_5min)
                failures = len(k.error_count_5min)
                if total >= 4 and failures / total >= 0.25:
                    continue
                hr = headroom_fn(k) if headroom_fn else 1.0
                scored.append((status_rank.get(k.status, 0) + hr, k))
            scored.sort(key=lambda t: t[0], reverse=True)
            return scored[0][1] if scored else None

    def best_available(self, agent: str) -> tuple[str, str, ProviderKey | None]:
        """Resolve (provider, model, key) for an agent, walking the fallback
        chain if the primary has no key."""
        with self._lock:
            primary = self._agent_models.get(agent)
            chain = []
            if primary:
                chain.append(primary)
            chain.extend(self._fallbacks.get(agent, []))
            # Always end on the echo provider so the system never hard-fails
            chain.append(("Galaxy Echo", "galaxy-echo"))
            for prov, model in chain:
                p = self._providers.get(prov)
                if p is None:
                    continue
                if prov == "Galaxy Echo":
                    return (prov, model, p.keys[0] if p.keys else None)
                key = self.pick_key(prov, agent=agent)
                if key is not None:
                    return (prov, model, key)
            # unreachable — chain always ends on echo
            return ("Galaxy Echo", "galaxy-echo", None)

    def _trim_health(self, key: ProviderKey, now: float) -> None:
        key.error_count_5min = [t for t in key.error_count_5min if now - t < 300]
        key.request_count_5min = [t for t in key.request_count_5min if now - t < 300]
        key.latencies_5min = [(t, ms) for t, ms in key.latencies_5min if now - t < 300]

    def _key(self, provider: str, key_id: int) -> ProviderKey | None:
        p = self._providers.get(provider)
        if not p:
            return None
        return next((key for key in p.keys if key.id == key_id), None)

    def record_key_error(self, provider: str, key_id: int) -> None:
        with self._lock:
            key = self._key(provider, key_id)
            if key is None:
                return
            now = time.time()
            self._trim_health(key, now)
            key.last_error_ts = now
            key.error_count_5min.append(now)
            key.request_count_5min.append(now)

    def record_key_success(self, provider: str, key_id: int, latency_ms: int) -> None:
        with self._lock:
            key = self._key(provider, key_id)
            if key is None:
                return
            now = time.time()
            self._trim_health(key, now)
            key.request_count_5min.append(now)
            key.latencies_5min.append((now, int(latency_ms)))

    def key_error_rate(self, provider: str, key_id: int) -> float:
        with self._lock:
            key = self._key(provider, key_id)
            if key is None:
                return 0.0
            self._trim_health(key, time.time())
            total = len(key.request_count_5min)
            return len(key.error_count_5min) / total if total else 0.0

    def health_snapshot(self) -> list[dict[str, Any]]:
        with self._lock:
            now = time.time()
            rows: list[dict[str, Any]] = []
            for provider in self._providers.values():
                for key in provider.keys:
                    self._trim_health(key, now)
                    total = len(key.request_count_5min)
                    errors = len(key.error_count_5min)
                    latencies = sorted(ms for _, ms in key.latencies_5min)
                    rows.append({"provider": provider.name, "key": key.alias,
                                 "requests_5m": total, "errors_5m": errors,
                                 "error_rate": errors / total if total else 0.0,
                                 "p50_latency_ms": latencies[len(latencies) // 2] if latencies else 0,
                                 "disabled": total >= 4 and errors / total >= 0.25})
            return rows

    def to_dict(self) -> dict[str, Any]:
        with self._lock:
            return {
                "providers": {n: p.to_dict() for n, p in self._providers.items()},
                "agent_models": {a: list(m) for a, m in self._agent_models.items()},
                "fallbacks": {a: [list(x) for x in c] for a, c in self._fallbacks.items()},
                "agent_keys": {a: [p, k] for a, (p, k) in self._agent_keys.items()},
            }


_pm: ProviderManager | None = None
_pm_lock = threading.Lock()


def get_provider_manager() -> ProviderManager:
    global _pm
    if _pm is None:
        with _pm_lock:
            if _pm is None:
                _pm = ProviderManager()
    return _pm


def reset_provider_manager_for_tests() -> ProviderManager:
    global _pm
    with _pm_lock:
        _pm = ProviderManager()
    return _pm
