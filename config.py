"""config.py — Galaxy configuration singleton (thread-safe).

§25 Phase 1 ①. Centralizes all paths, defaults, and runtime flags. Thread-safe
singleton so the CLI, the Subconscious Loop, and any background tasks all read
the same configuration. Reads from environment variables and ~/.galaxy/config.json
(with env vars winning, so tests can override deterministically).
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any


def _default_galaxy_home() -> Path:
    """Where ~/.galaxy lives. Overridable via GALAXY_HOME for tests."""
    return Path(os.environ.get("GALAXY_HOME", str(Path.home() / ".galaxy")))


# Brand identity (§23)
GALAXY_VERSION = "1.0.0"
SCHEMA_VERSION = 9  # current SQLite PRAGMA user_version (see schema/migrations.py)
TAGLINE = "the mind that remembers everything"

ASCII_HEADER = """
    ·  ✦  ·     ·  ✦  ·     ·  ✦  ·
         GALAXY COMPUTER
    ✦ ─────────── v{ver} ─────────── ✦
      {tagline}
""".format(ver=GALAXY_VERSION, tagline=TAGLINE)

# Color palette (§23) — exposed for any TTY rendering that wants raw hex.
PALETTE = {
    "deep_space": "#0A0A14",
    "void": "#1A0A2E",
    "nebula": "#6B21A8",
    "pulsar": "#A855F7",
    "quasar": "#E879F9",
    "starlight": "#F0E6FF",
    "stardust": "#C084FC",
    "dark_matter": "#4C1D95",
    "signal": "#22D3EE",
    "active": "#4ADE80",
    "warning": "#F59E0B",
}

# Sliding context-budget percentages (§13).
CONTEXT_BUDGET = {
    "system_prompt": 0.05,
    "l4_skills": 0.15,
    "l3_stars": 0.10,
    "conversation": 0.50,
    "file_contents": 0.10,
    "buffer": 0.10,
}

# Gravity Score thresholds (§3).
GRAVITY_THRESHOLDS = {
    "nebula": 0.30,        # 0–0.30 stays asteroid (low value)
    "asteroid": 0.60,      # 0.30–0.60 asteroid (kept)
    "planet_to_l3": 0.85,  # 0.60–0.85 promoted to L3
    "star_permanent": 0.85,  # 0.85+ permanent L3 Star
}
SUBCONSCIOUS_PROMOTE_AT = 0.45  # idle-time promotion threshold (§3)

# Skill confidence lifecycle (§18).
SKILL_CONFIDENCE = {
    "trusted_load": 0.95,
    "trusted_load_lower": 0.90,
    "idle_decay_to": 0.70,
    "idle_decay_days": 90,
    "success_bump_to": 0.95,
    "failure_drop_to": 0.50,
    "needs_review_below": 0.55,
}

# Moon probation (§4).
MOON_PROBATION_GOALS = 3
MAX_MOONS_PER_PLANET = 4  # backpressure (§14)

# Retention (§3 foundational hardening).
ASTEROID_MIN_RETENTION_DAYS = 7

# Subconscious Loop bounds (§3).
SUBCONSCIOUS_INTERVAL_SECONDS = 30 * 60  # 30 min
SUBCONSCIOUS_MAX_CYCLE_SECONDS = 5 * 60  # 5 min per cycle

# The trusted skill sources (§5) — the complete allowlist. Extended
# 2026-07 to cover agents the original four left at zero (browser, file,
# data) or near-zero (write): each verified directly against its own
# official upstream repo's LICENSE, not inferred from any aggregator/index
# (see docs/SKILLS_EXPANSION.md for the full per-source verification and
# the sources deliberately excluded on licensing grounds — trailofbits/skills
# is CC-BY-SA-4.0, incompatible with the MIT/Apache-2.0-only policy below,
# same reasoning as the existing OpenHuman/GPL-3.0 exclusion).
TRUSTED_SKILL_SOURCES = (
    "ECC",           # Everything Claude Code — MIT
    "UIUXProMax",    # UI UX Pro Max Skill
    "OpenDesign",    # Open Design — Apache-2.0
    "AnthropicSkills",  # Anthropic official skills — Apache 2.0
    "BrowserbaseSkills",    # browserbase/skills — MIT — browser agent
    "DuckDBSkills",         # duckdb/duckdb-skills — MIT — data agent
    "ClickHouseSkills",     # ClickHouse/agent-skills — Apache-2.0 — data agent
    "CoreyHainesMarketing", # coreyhaines31/marketingskills — MIT — write agent
    "GoogleWorkspaceCLI",   # googleworkspace/cli — Apache-2.0 — file agent
    "ApolloGraphQL",           # apollographql/skills — MIT — api agent
    "Auth0Skills",             # auth0/agent-skills — Apache-2.0 — api agent
    "SentrySkills",            # getsentry/sentry-skills — Apache-2.0 — devops agent
    "BraveSearchSkills",       # brave/brave-search-skills — MIT — research agent
    "UnitOneSecuritySkills",   # UnitOneAI/SecuritySkills — MIT — security agent
    "BagelHoleDevOpsSecurity", # BagelHole/DevOps-Security-Agent-Skills — MIT — devops + security
    "AlirezaProjectManagement",# alirezarezvani/claude-skills (project-management/) — MIT — planning agent
    "AlirezaResearch",         # alirezarezvani/claude-skills (research/) — MIT — research agent
    "AlirezaResearchOps",      # alirezarezvani/claude-skills (research-ops/) — MIT — research agent
)


class GalaxyConfig:
    """Thread-safe configuration singleton.

    All paths are resolved lazily from GALAXY_HOME so tests can point at a
    temp directory. The singleton is intentionally simple — no hot-reload of
    config.json beyond construction — because configuration changes that
    matter (provider keys, models) go through the live slash-command wizards, not
    by editing config.json at runtime.
    """

    _instance: "GalaxyConfig | None" = None
    _lock = threading.Lock()

    def __new__(cls) -> "GalaxyConfig":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self) -> None:
        self.home: Path = _default_galaxy_home()
        self.db_path: Path = self.home / "galaxy.db"
        self.vault_dir: Path = self.home / "memory_vault"
        self.skills_dir: Path = self.home / "skills"
        self.orbits_dir: Path = self.home / "orbits"
        self.connectors_dir: Path = self.home / "connectors"
        self.checkpoints_dir: Path = self.home / "checkpoints"
        self.maps_dir: Path = self.home / "maps"
        self.audit_log: Path = self.home / "audit.log"
        self.llm_log: Path = self.home / "llm_calls.jsonl"
        self.config_file: Path = self.home / "config.json"
        self.timeline_dir: Path = self.home / "timelines"
        self.eval_history: Path = self.home / "eval-history.json"
        # Runtime flags (env-driven, never persisted — these are session concerns)
        self.debug: bool = os.environ.get("GAX_DEBUG", "") == "1"
        self.offline: bool = os.environ.get("GAX_OFFLINE", "") == "1"
        self.otel_endpoint: str | None = os.environ.get("GAX_OTEL_ENDPOINT")
        # User-editable overrides loaded from config.json (empty until /setup writes it)
        self._overrides: dict[str, Any] = {}
        self._load_overrides()

    def _load_overrides(self) -> None:
        if self.config_file.exists():
            try:
                self._overrides = json.loads(self.config_file.read_text("utf-8"))
            except Exception:
                self._overrides = {}

    def get(self, key: str, default: Any = None) -> Any:
        # env wins, then override, then default
        env_val = os.environ.get("GAX_" + key.upper())
        if env_val is not None:
            return env_val
        return self._overrides.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._overrides[key] = value
        self._persist()

    def _persist(self) -> None:
        self.home.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(self._overrides, indent=2), "utf-8")

    def ensure_dirs(self) -> None:
        """Create every directory Galaxy expects to exist. Idempotent."""
        for d in (
            self.home, self.vault_dir, self.skills_dir, self.orbits_dir,
            self.connectors_dir, self.checkpoints_dir, self.maps_dir,
            self.timeline_dir,
        ):
            d.mkdir(parents=True, exist_ok=True)

    def reset_for_tests(self, home: Path) -> None:
        """Repoint the singleton at a fresh temp home (tests only)."""
        self.home = home
        self.db_path = home / "galaxy.db"
        self.vault_dir = home / "memory_vault"
        self.skills_dir = home / "skills"
        self.orbits_dir = home / "orbits"
        self.connectors_dir = home / "connectors"
        self.checkpoints_dir = home / "checkpoints"
        self.maps_dir = home / "maps"
        self.audit_log = home / "audit.log"
        self.llm_log = home / "llm_calls.jsonl"
        self.config_file = home / "config.json"
        self.timeline_dir = home / "timelines"
        self.eval_history = home / "eval-history.json"
        self._overrides = {}
        self.ensure_dirs()


def get_config() -> GalaxyConfig:
    """Module-level accessor used everywhere in the codebase."""
    return GalaxyConfig()
