"""skill/quarantine.py — quarantine tier for community skills (§18).

Anything outside the trusted allowlist (§5) lands here. Surfaced in
/quarantine for per-skill user approval. Runs sandboxed (Docker, no network)
if manually activated. Requires explicit per-skill approval.
"""
from __future__ import annotations

import json
import time
from typing import Any

from core.agent.base_agent import new_id
from core.memory import get_memory
from core.memory.layers.l4_procedural import Skill
from storage.local import get_storage


def submit_community_skill(*, name: str, source_url: str, normalized: dict[str, Any],
                           signature: str) -> str:
    """Submit a community skill to the quarantine queue. Returns the quarantine id."""
    qid = new_id("quarantine-")
    st = get_storage()
    with st.transaction() as conn:
        conn.execute(
            "INSERT INTO skill_quarantine(id,name,source_url,normalized,signature,"
            "submitted_at,approved,reviewed_at) VALUES(?,?,?,?,?,?,0,NULL);",
            (qid, name, source_url, json.dumps(normalized), signature, time.time()),
        )
    return qid


def list_quarantine() -> list[dict[str, Any]]:
    st = get_storage()
    rows = st.query_all("SELECT * FROM skill_quarantine ORDER BY submitted_at DESC;")
    out = []
    for r in rows:
        d = dict(r)
        try:
            d["normalized"] = json.loads(r["normalized"] or "{}")
        except Exception:
            d["normalized"] = {}
        out.append(d)
    return out


def approve(quarantine_id: str, *, confidence: float = 0.70) -> Skill | None:
    """Approve a quarantined skill -> promote to L4 as an active (non-trusted)
    skill at the given confidence (default 0.70 — lower than the trusted 0.90)."""
    st = get_storage()
    row = st.query_one("SELECT * FROM skill_quarantine WHERE id=?;", (quarantine_id,))
    if not row:
        return None
    norm = json.loads(row["normalized"] or "{}")
    skill = Skill(
        id=new_id("skill-"), name=row["name"], source=row.get("source_url") or "community",
        version=norm.get("version", "1.0.0"), description=norm.get("description", ""),
        body=norm.get("body", ""), tags=norm.get("tags", []), triggers=norm.get("triggers", []),
        license=norm.get("license", "unknown"), confidence=confidence,
        status="active", signature=row.get("signature") or "",
        category=norm.get("category", "general"),
        target_agent=norm.get("target_agent", ""),
        last_used=0.0, last_verified=time.time(), use_count=0, needs_review=False,
        created_at=time.time(),
    )
    mem = get_memory()
    mem.l4.upsert(skill)
    with st.transaction() as conn:
        conn.execute(
            "UPDATE skill_quarantine SET approved=1, reviewed_at=? WHERE id=?;",
            (time.time(), quarantine_id),
        )
    return skill


def reject(quarantine_id: str) -> bool:
    st = get_storage()
    with st.transaction() as conn:
        cur = conn.execute("DELETE FROM skill_quarantine WHERE id=?;", (quarantine_id,))
        return cur.rowcount > 0


def pending_count() -> int:
    st = get_storage()
    row = st.query_one("SELECT COUNT(*) AS c FROM skill_quarantine WHERE approved=0;")
    return int(row["c"]) if row else 0
