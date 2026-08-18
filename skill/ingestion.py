"""skill/ingestion.py — the 8-step ingestion pipeline (§18).

discover → parse → normalize → dedup → sign → quarantine-check → index → audit

This pipeline runs identically whether a skill is one of the four trusted
sources (§5) or a community contribution. The only difference is the
quarantine-check step: trusted sources land in L4 at 0.90–0.95; anything else
lands in the Quarantine tier for per-skill user approval.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from config import TRUSTED_SKILL_SOURCES, SKILL_CONFIDENCE, get_config
from core.memory.layers.l4_procedural import Skill
from core.memory import get_memory
from skill.signing import sign_skill
from skill.conflict import dedup_skills, resolve_conflicts
from storage.local import get_storage


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML-ish frontmatter (key: value lines between --- fences)."""
    fm: dict[str, Any] = {}
    body = text
    if text.startswith("---"):
        parts = text[3:].split("---", 1)
        if len(parts) == 2:
            for line in parts[0].strip().splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    v = v.strip().strip('"').strip("'")
                    # parse lists like ["a", "b"]
                    if v.startswith("[") and v.endswith("]"):
                        try:
                            fm[k.strip()] = json.loads(v)
                        except Exception:
                            fm[k.strip()] = [x.strip().strip('"').strip("'")
                                             for x in v[1:-1].split(",") if x.strip()]
                    else:
                        fm[k.strip()] = v
            body = parts[1].strip()
    return fm, body


def discover(source_dir: Path) -> list[Path]:
    """Collect every .md skill file under source_dir."""
    if not source_dir.exists():
        return []
    return sorted(source_dir.rglob("*.md"))


def parse(path: Path) -> dict[str, Any]:
    """Parse a skill file into a raw record."""
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    return {
        "name": fm.get("name", path.stem),
        "source": fm.get("source", _source_from_path(path)),
        "version": fm.get("version", "1.0.0"),
        "description": fm.get("description", ""),
        "body": body,
        "tags": fm.get("tags", []),
        "triggers": fm.get("triggers", []),
        "license": fm.get("license", "MIT"),
        "target_agent": fm.get("target_agent", ""),
        "category": fm.get("category", "general"),
        "frontmatter": fm,
        "path": str(path),
    }


def _source_from_path(path: Path) -> str:
    """skills_data/ECC/python/foo.md -> ECC."""
    try:
        return path.relative_to(get_config().home.parent).parts[0]
    except Exception:
        return path.parts[-3] if len(path.parts) >= 3 else "unknown"


def normalize_skill(raw: dict[str, Any]) -> Skill:
    """Convert a raw parsed record into Galaxy's Skill schema."""
    return Skill(
        name=raw["name"], source=raw["source"], version=raw.get("version", "1.0.0"),
        description=raw.get("description", ""), body=raw.get("body", ""),
        tags=list(raw.get("tags", [])), triggers=list(raw.get("triggers", [])),
        license=raw.get("license", "MIT"),
        confidence=SKILL_CONFIDENCE["trusted_load"],
        status="trusted" if raw["source"] in TRUSTED_SKILL_SOURCES else "quarantine",
        signature=sign_skill(raw["name"], raw["source"], raw.get("version", "1.0.0"),
                             raw.get("body", ""), raw.get("frontmatter")),
        category=raw.get("category", "general"),
        target_agent=raw.get("target_agent", ""),
        last_used=0.0, last_verified=time.time(), use_count=0, needs_review=False,
        created_at=time.time(),
    )


def quarantine_check(skill: Skill) -> Skill:
    """Trusted source -> L4 at 0.90–0.95. Anything else -> quarantine tier."""
    if skill.source in TRUSTED_SKILL_SOURCES:
        # ECC + UIUXProMax -> 0.95; OpenDesign + AnthropicSkills -> 0.90 (§5)
        if skill.source in ("ECC", "UIUXProMax"):
            skill.confidence = SKILL_CONFIDENCE["trusted_load"]  # 0.95
        else:
            skill.confidence = SKILL_CONFIDENCE["trusted_load_lower"]  # 0.90
        skill.status = "trusted"
    else:
        skill.confidence = 0.40
        skill.status = "quarantine"
        skill.needs_review = True
    return skill


def index_audit(skills: list[Skill]) -> dict[str, int]:
    """Persist to L4 + write the audit log. Returns counts."""
    from core.memory import get_memory
    mem = get_memory()
    st = get_storage()
    counts = {"ingested": 0, "trusted": 0, "quarantine": 0, "deduped": 0}
    # dedup by (name, source); keep highest version + highest confidence
    deduped = dedup_skills(skills)
    counts["deduped"] = len(skills) - len(deduped)
    for skill in deduped:
        # resolve conflicts (same trigger, different skills)
        mem.l4.upsert(skill)
        counts["ingested"] += 1
        if skill.status == "trusted":
            counts["trusted"] += 1
        else:
            counts["quarantine"] += 1
        # audit log entry (metadata only)
        with st.transaction() as conn:
            conn.execute(
                "INSERT INTO skill_activations(ts,skill_id,agent,goal_id,outcome) "
                "VALUES(?,?,?,?,?);",
                (time.time(), skill.id, "ingestion", "", "loaded"),
            )
    return counts


def ingest_source(source_dir: Path) -> dict[str, int]:
    """Run the full pipeline on one source directory. Returns counts."""
    paths = discover(source_dir)
    raws = [parse(p) for p in paths]
    skills = [normalize_skill(r) for r in raws]
    for s in skills:
        quarantine_check(s)
    # resolve trigger conflicts within this batch
    skills = resolve_conflicts(skills)
    return index_audit(skills)


def ingest_all_bundled() -> dict[str, int]:
    """Ingest every bundled trusted source under skills_data/. This is what
    runs at first launch (and via /migrate or /skills --reload)."""
    cfg = get_config()
    # skills_data lives alongside the package
    project_root = Path(__file__).resolve().parent.parent
    skills_data = project_root / "skills_data"
    total = {"ingested": 0, "trusted": 0, "quarantine": 0, "deduped": 0}
    for source_name in TRUSTED_SKILL_SOURCES:
        src_dir = skills_data / source_name
        if not src_dir.exists():
            continue
        counts = ingest_source(src_dir)
        for k in total:
            total[k] += counts.get(k, 0)
    return total
