"""observability/timeline.py — agent timeline + /trace (§11).

Every agent run produces a timeline, visible live via [S] and replayable via
/trace <goal_id>. Timeline entries are written to ~/.galaxy/timelines/<goal_id>.jsonl.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from config import get_config


def record(goal_id: str, *, agent: str, event: str, detail: str = "") -> None:
    """Append a timeline entry for a goal."""
    cfg = get_config()
    cfg.timeline_dir.mkdir(parents=True, exist_ok=True)
    entry = {"t": round(time.time(), 3), "agent": agent, "event": event, "detail": detail}
    with open(cfg.timeline_dir / f"{goal_id}.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def replay_goal(goal_id: str, io) -> str:
    """/trace <goal_id>: replay the agent timeline."""
    cfg = get_config()
    path = cfg.timeline_dir / f"{goal_id}.jsonl"
    if not path.exists():
        return f"No timeline for {goal_id}."
    lines = path.read_text("utf-8").splitlines()
    if not lines:
        return f"Empty timeline for {goal_id}."
    start_t = json.loads(lines[0])["t"]
    io.print(f"Timeline for {goal_id}:")
    for line in lines:
        try:
            e = json.loads(line)
            elapsed = e["t"] - start_t
            io.print(f"  T+{elapsed:6.1f}s  {e['agent']:14s}  {e['event']}"
                     + (f"  {e['detail']}" if e.get('detail') else ''))
        except Exception:
            continue
    return f"{len(lines)} events."
