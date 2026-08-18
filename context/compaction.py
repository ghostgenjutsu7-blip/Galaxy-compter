"""context/compaction.py — sliding window + summarization (§12, §13).

When approaching the model's context limit (80%): summarize old messages (keep
decisions and tool results, drop small talk), move large file contents to L3
Star references instead of inline text, and compress repeated tool outputs.
"""
from __future__ import annotations

from typing import Any


COMPACTION_TRIGGER_PCT = 0.80


def should_compact(current_tokens: int, max_tokens: int) -> bool:
    return current_tokens >= max_tokens * COMPACTION_TRIGGER_PCT


def compact_messages(messages: list[dict[str, str]], *,
                     keep_recent: int = 6,
                     keep_system: bool = True) -> list[dict[str, str]]:
    """Compact a message list. Keep system + recent N; summarize the middle
    into a single 'summary' message. Drops pure-smalltalk."""
    if len(messages) <= keep_recent + 1:
        return messages
    sys_msgs = [m for m in messages if m["role"] == "system"] if keep_system else []
    rest = [m for m in messages if m["role"] != "system"]
    if len(rest) <= keep_recent:
        return sys_msgs + rest
    middle = rest[:-keep_recent]
    recent = rest[-keep_recent:]
    # summarize middle: keep decisions + tool results, drop filler
    summary_parts: list[str] = []
    for m in middle:
        content = m.get("content", "")
        if any(k in content.lower() for k in ("decision", "agreed", "plan", "result", "created", "wrote", "fixed")):
            summary_parts.append(f"[{m['role']}] {content[:150]}")
    summary = "Compacted prior context:\n" + "\n".join(summary_parts) if summary_parts else "[prior context compacted]"
    return sys_msgs + [{"role": "system", "content": summary}] + recent


def compact_tool_output(output: str, max_chars: int = 2000) -> str:
    """Compress repeated tool outputs (e.g. five npm install logs -> summary)."""
    if len(output) <= max_chars:
        return output
    # keep head + tail + a count of repeated lines
    lines = output.splitlines()
    if len(lines) > 20:
        head = lines[:5]
        tail = lines[-5:]
        return "\n".join(head + [f"... [{len(lines)-10} lines compacted] ..."] + tail)
    return output[:max_chars] + "\n...[truncated]"


def sliding_budget(total_tokens: int) -> dict[str, int]:
    """Return the §13 sliding context-budget allocation in tokens."""
    from config import CONTEXT_BUDGET
    return {k: int(total_tokens * pct) for k, pct in CONTEXT_BUDGET.items()}
