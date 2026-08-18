"""resources/router.py — per-task-type model routing (§19).

Cheap models for classification/short planning/formatting. Mid-tier for
default execution. Expensive for complex reasoning and security review.
Long-context specialist for >200K contexts.
"""
from __future__ import annotations

from typing import Any


# §19 per-task routing table
TASK_ROUTING: dict[str, tuple[str, str | None]] = {
    "classification": ("cheap", None),
    "planning":       ("mid", "cheap"),
    "code_generation": ("mid", "cheap"),
    "code_review":    ("mid", None),
    "hard_reasoning": ("expensive", "mid"),
    "web_research":   ("mid", "cheap"),
    "long_context":   ("long_context", "mid"),
    "fast_chat":      ("cheap", None),
    "multilingual":   ("mid", None),
}

# tier -> default model name per provider (when user hasn't pinned)
TIER_DEFAULTS: dict[str, dict[str, str]] = {
    "cheap": {"OpenAI": "gpt-4o-mini", "Anthropic": "claude-haiku", "Galaxy Echo": "galaxy-echo"},
    "mid":   {"OpenAI": "gpt-4o", "Anthropic": "claude-sonnet", "Galaxy Echo": "galaxy-echo"},
    "expensive": {"OpenAI": "o1", "Anthropic": "claude-opus", "Galaxy Echo": "galaxy-echo"},
    "long_context": {"Google AI Studio": "gemini-1.5-pro", "Galaxy Echo": "galaxy-echo"},
}


def route(task_type: str, *, agent: str = "",
          context_tokens: int = 0) -> tuple[str, str]:
    """Return (tier, fallback_tier) for a task, considering context size."""
    if context_tokens > 200_000:
        tier, _ = TASK_ROUTING["long_context"]
        return tier, "mid"
    entry = TASK_ROUTING.get(task_type, ("mid", "cheap"))
    return entry[0], entry[1]


def model_for_tier(tier: str, provider: str) -> str:
    return TIER_DEFAULTS.get(tier, {}).get(provider, "galaxy-echo")
