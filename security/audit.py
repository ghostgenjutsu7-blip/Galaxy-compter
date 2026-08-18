"""security/audit.py — append-only JSONL audit log (§10).

Immutable, append-only at ~/.galaxy/audit.log. Rotated at 100MB, kept 90 days.
Never includes prompts/completions — only metadata. /audit inspects it.
"""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from config import get_config
from security.secret_filter import redact_dict


MAX_LOG_SIZE = 100 * 1024 * 1024  # 100MB
RETENTION_DAYS = 90


def log(*, actor: str, action: str, args: dict[str, Any] | None = None,
        result: str = "ok", duration_ms: int = 0,
        goal_id: str = "") -> None:
    """Append one audit entry. Metadata only; args are redacted."""
    cfg = get_config()
    cfg.home.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "actor": actor,
        "action": action,
        "args": redact_dict(args or {}),
        "result": result,
        "duration_ms": duration_ms,
        "goal_id": goal_id,
        "nonce": str(uuid.uuid4()),
    }
    with open(cfg.audit_log, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    _maybe_rotate()


def _maybe_rotate() -> None:
    cfg = get_config()
    try:
        if cfg.audit_log.exists() and cfg.audit_log.stat().st_size > MAX_LOG_SIZE:
            # rotate: rename to .1, start fresh
            rotated = cfg.audit_log.with_suffix(".log.1")
            if rotated.exists():
                rotated.unlink()
            cfg.audit_log.rename(rotated)
    except Exception:
        pass


def tail_audit(io, limit: int = 20) -> str:
    """/audit: show the last N entries."""
    cfg = get_config()
    if not cfg.audit_log.exists():
        return "No audit log yet."
    lines = cfg.audit_log.read_text(encoding="utf-8").splitlines()[-limit:]
    for line in lines:
        try:
            e = json.loads(line)
            io.print(f"  {e['ts']}  {e['actor']:14s}  {e['action']:24s}  {e['result']}")
        except Exception:
            io.print(f"  {line[:120]}")
    return f"{len(lines)} entries."


def prune_old() -> int:
    """Drop entries older than RETENTION_DAYS. Returns count removed."""
    cfg = get_config()
    if not cfg.audit_log.exists():
        return 0
    cutoff = time.time() - RETENTION_DAYS * 86400
    kept = 0
    removed = 0
    tmp = cfg.audit_log.with_suffix(".log.tmp")
    with open(cfg.audit_log, "r", encoding="utf-8") as src, \
         open(tmp, "w", encoding="utf-8") as dst:
        for line in src:
            try:
                e = json.loads(line)
                ts = time.mktime(time.strptime(e["ts"], "%Y-%m-%dT%H:%M:%SZ"))
                if ts >= cutoff:
                    dst.write(line)
                    kept += 1
                else:
                    removed += 1
            except Exception:
                dst.write(line)
                kept += 1
    tmp.replace(cfg.audit_log)
    return removed
