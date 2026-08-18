"""Skill loading, verification, taxonomy rebuild, and persistent bootstrap."""
from __future__ import annotations

import time
from pathlib import Path

from config import get_config
from skill.ingestion import ingest_all_bundled
from skill.signing import sign_skill
from skill.taxonomy import TAXONOMY_VERSION, rebuild_taxonomy
from storage.local import get_storage
from core.memory import get_memory


def _bundled_skill_count() -> int:
    root = Path(__file__).resolve().parent.parent / "skills_data"
    return sum(1 for path in root.rglob("*.md")) if root.exists() else 0


def load_all_skills() -> dict[str, int]:
    """Ingest every bundled trusted source and rebuild its durable taxonomy."""
    counts = ingest_all_bundled()
    taxonomy = rebuild_taxonomy()
    counts.update({"taxonomy_skills": taxonomy["skills"],
                   "taxonomy_review": taxonomy["review"],
                   "taxonomy_systems": taxonomy["systems"],
                   "taxonomy_orbits": taxonomy["orbits"]})
    return counts


def ensure_skills_bootstrapped() -> dict[str, int | bool]:
    """Ensure a fresh or isolated GALAXY_HOME reconstructs persistent L4 skills.

    The bundled corpus is the durable source of truth. A home-specific SQLite
    database is a materialized index, so a new home must rebuild it rather than
    silently starting with an empty L4. Existing custom rows are preserved.
    """
    cfg = get_config()
    cfg.ensure_dirs()
    from schema.migrations import ensure_latest
    ensure_latest()
    st = get_storage()
    expected = _bundled_skill_count()
    actual = int(st.query_one("SELECT COUNT(*) AS c FROM skills WHERE status='trusted';")["c"])
    current_taxonomy = int(st.query_one("SELECT COUNT(*) AS c FROM skills WHERE status='trusted' AND taxonomy_version=?;", (TAXONOMY_VERSION,))["c"])
    systems = int(st.query_one("SELECT COUNT(*) AS c FROM skill_solar_systems;")["c"])
    needs_load = actual < expected or current_taxonomy < actual or systems == 0
    if needs_load:
        counts = load_all_skills()
        counts.update({"bootstrapped": True, "expected_bundled": expected, "existing_trusted_before": actual})
        return counts
    return {"bootstrapped": False, "expected_bundled": expected, "existing_trusted": actual,
            "taxonomy_version": TAXONOMY_VERSION}


def verify_all_signatures() -> dict[str, int]:
    """Re-verify every trusted skill's signature against its stored body."""
    mem = get_memory()
    st = get_storage()
    stats = {"verified": 0, "mismatch": 0, "missing": 0}
    skills = mem.l4.list(status="trusted")
    for s in skills:
        if not s.signature:
            stats["missing"] += 1
            continue
        expected = sign_skill(s.name, s.source, s.version, s.body, {
            "name": s.name, "source": s.source, "version": s.version,
            "description": s.description, "tags": s.tags, "triggers": s.triggers,
            "license": s.license, "target_agent": s.target_agent, "category": s.category,
        })
        if expected == s.signature:
            stats["verified"] += 1
            with st.transaction() as conn:
                conn.execute("UPDATE skills SET last_verified=? WHERE id=?;", (time.time(), s.id))
        else:
            stats["mismatch"] += 1
            with st.transaction() as conn:
                conn.execute("UPDATE skills SET needs_review=1, status='quarantine' WHERE id=?;", (s.id,))
    return stats


def skill_counts_by_source() -> dict[str, int]:
    """Summary for /skills."""
    st = get_storage()
    rows = st.query_all("SELECT source, COUNT(*) AS c FROM skills GROUP BY source;")
    return {r["source"]: int(r["c"]) for r in rows}
