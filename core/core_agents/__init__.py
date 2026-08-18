"""core/core_agents/__init__.py — the 12 Core Agents (§4).

Each agent is a BaseAgent subclass with a specialty-specific system prompt and
tool whitelist. The Orchestrator routes a goal to the right agent(s); agents
never talk to each other directly (§4 isolation). All tool calls go through
the Capability Gate (security/capability.py) regardless of which agent issued
them.

Suggested default model tiers (§4 table):
  Code/Research/Planning/Review/Design/Data/DevOps/Security -> Sonnet-class (mid)
  Write/Browser/File/API -> Haiku-class (cheap)
  Security -> Opus-class (expensive)
"""
from .agents import (
    CodeAgent, ResearchAgent, WriteAgent, PlanningAgent, ReviewAgent,
    DesignAgent, DataAgent, BrowserAgent, DevOpsAgent, FileAgent,
    APIAgent, SecurityAgent, ALL_AGENTS, get_agent, get_all_agents,
)

__all__ = [
    "CodeAgent", "ResearchAgent", "WriteAgent", "PlanningAgent", "ReviewAgent",
    "DesignAgent", "DataAgent", "BrowserAgent", "DevOpsAgent", "FileAgent",
    "APIAgent", "SecurityAgent", "ALL_AGENTS", "get_agent", "get_all_agents",
]
