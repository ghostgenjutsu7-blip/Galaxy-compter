"""core/memory/fingerprint.py — task fingerprinting.

§3, §4, §25 Phase 2 ⑦. The v0 SHA-256-as-similarity bug is fixed: conceptual
similarity is judged ONLY by LLM classification via the GALAXY_META protocol,
never by a hash. A narrow, separate deterministic hash of (intent keywords +
sorted tool set) is used ONLY to detect exact-repeat requests within a short
recency window — so an accidental double-submit links to the same asteroid
instead of creating a duplicate. This hash is never used to compare two
different tasks.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any

from storage.local import get_storage


@dataclass
class Fingerprint:
    classification: dict[str, str]   # from GALAXY_META (category/domain/intent/complexity)
    repeat_hash: str                 # narrow hash for exact-repeat detection only
    tool_set: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification,
            "repeat_hash": self.repeat_hash,
            "tool_set": self.tool_set,
        }


def _balanced_json_candidates(text: str) -> list[str]:
    """Yield balanced JSON object candidates without truncating nested objects."""
    candidates: list[str] = []
    for start, char in enumerate(text):
        if char != "{":
            continue
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            current = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif current == "\\":
                    escaped = True
                elif current == '"':
                    in_string = False
                continue
            if current == '"':
                in_string = True
            elif current == "{":
                depth += 1
            elif current == "}":
                depth -= 1
                if depth == 0:
                    candidates.append(text[start:index + 1])
                    break
    return candidates


def extract_meta_block(text: str) -> dict[str, Any] | None:
    """Parse a complete GALAXY_META object, including nested classification JSON."""
    if not text:
        return None
    fenced = re.search(r"```galaxy_meta\s*(.*?)\s*```", text, re.DOTALL)
    source = fenced.group(1) if fenced else text
    for raw in _balanced_json_candidates(source):
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and ("mode" in payload or "classification" in payload):
            return payload
    return None


def compute_repeat_hash(classification: dict[str, str], tool_set: list[str]) -> str:
    """Deterministic hash of (intent keywords + sorted tool set). Used ONLY to
    detect exact-repeat requests within a recency window (§3)."""
    intent = classification.get("intent", "")
    category = classification.get("category", "")
    tools_sorted = sorted(tool_set)
    payload = f"{category}|{intent}|" + ",".join(tools_sorted)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]


def build_fingerprint(classification: dict[str, str], tool_set: list[str]) -> Fingerprint:
    return Fingerprint(
        classification=classification,
        repeat_hash=compute_repeat_hash(classification, tool_set),
        tool_set=sorted(set(tool_set)),
    )


def find_repeat_asteroid(repeat_hash: str, recency_seconds: int = 300) -> str | None:
    """Return the asteroid id of an exact-repeat request within the recency
    window, or None. This is the ONLY use of the repeat hash."""
    if not repeat_hash:
        return None
    import time
    cutoff = time.time() - recency_seconds
    st = get_storage()
    row = st.query_one(
        "SELECT id FROM asteroids WHERE fingerprint_hash=? AND created_at>=? "
        "ORDER BY created_at DESC LIMIT 1;",
        (repeat_hash, cutoff),
    )
    return row["id"] if row else None
