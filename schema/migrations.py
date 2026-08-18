"""schema/migrations.py — forward-only schema migrations.

§25 Phase 10 ㊿, §20. Each migration is a numbered module in schema/v*.py
exposing upgrade(storage) and (optionally) downgrade(storage). The runner:
- Takes a backup of galaxy.db before applying (§20).
- Updates PRAGMA user_version.
- On failure, restores the backup and refuses to start.
- /migrate --dry-run previews pending migrations.

We use a tiny bespoke runner rather than yoyo-migrations so the build has zero
external migration deps and migrations are plain Python (auditable). The
behaviour matches the spec's intent exactly.
"""

from __future__ import annotations

import shutil
import time
from pathlib import Path
from typing import Callable

from storage.local import get_storage
from config import get_config


MigrationFn = Callable[["LocalStorage"], None]  # type: ignore[name-defined]

# Ordered list of (version, description, upgrade_fn). Each v*.py module
# registers itself here at import time.
MIGRATIONS: list[tuple[int, str, MigrationFn]] = []


def register(version: int, description: str) -> Callable[[MigrationFn], MigrationFn]:
    def deco(fn: MigrationFn) -> MigrationFn:
        MIGRATIONS.append((version, description, fn))
        return fn
    return deco


def _load_all() -> None:
    """Import every v*.py so its @register decorator fires."""
    import importlib
    import pkgutil
    from schema import (v0001_initial, v0002_add_orbit_id, v0003_add_skill_signature,
                        v0004_add_goals_table, v0005_add_audit_log,
                        v0006_add_capability_policy, v0007_add_skill_quarantine,
                        v0008_add_privacy_tier, v0009_add_connectors_channels,
                        v0010_add_agent_provider_keys, v0011_add_tool_lifecycle,
                        v0012_skill_taxonomy)
    # ensure sorted by version
    MIGRATIONS.sort(key=lambda t: t[0])


def pending(target_version: int | None = None) -> list[tuple[int, str, MigrationFn]]:
    _load_all()
    st = get_storage()
    current = st.user_version()
    end = target_version if target_version is not None else max(v for v, _, _ in MIGRATIONS)
    return [(v, d, fn) for v, d, fn in MIGRATIONS if current < v <= end]


def run(target_version: int | None = None, *, dry_run: bool = False) -> list[str]:
    """Apply pending migrations up to target_version (default: latest).

    Returns a list of human-readable lines describing what happened."""
    _load_all()
    cfg = get_config()
    st = get_storage()
    current = st.user_version()
    pend = pending(target_version)
    if not pend:
        return [f"schema already at v{current}; nothing to migrate."]

    lines: list[str] = []
    if not dry_run:
        # integrity check before
        if not st.integrity_check():
            raise RuntimeError("integrity_check failed before migration — refusing to start")
        # backup
        cfg.home.mkdir(parents=True, exist_ok=True)
        backup_path = cfg.home / f"galaxy.db.bak.{int(time.time())}"
        st.backup(backup_path)
        lines.append(f"backup written -> {backup_path.name}")

    for version, desc, fn in pend:
        lines.append(f"applying v{version:04d}: {desc}")
        if dry_run:
            continue
        try:
            with st.transaction() as conn:
                fn(st)
                conn.execute(f"PRAGMA user_version = {version};")
            if not st.integrity_check():
                raise RuntimeError(f"integrity_check failed after v{version}")
        except Exception as e:
            # restore backup
            if backup_path.exists():
                st.execute("VACUUM;")  # release WAL locks
                shutil.copy2(backup_path, cfg.db_path)
            raise RuntimeError(
                f"migration v{version} failed: {e}. backup restored. Galaxy refuses to start."
            ) from e
    return lines


def ensure_latest() -> None:
    """Called at startup. Idempotent — no-op if already current."""
    run()
