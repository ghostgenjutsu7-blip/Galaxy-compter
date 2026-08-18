"""Mandatory capability, consent, resource-scope, and audit gate."""
from __future__ import annotations

import fnmatch
import inspect
import time
from pathlib import Path
from typing import Any, Awaitable, Callable
from urllib.parse import urlparse

from core.agent.base_agent import Tool
from core.memory import get_memory
from security.audit import log as audit_log
from storage.local import get_storage

DEFAULT_POLICY: dict[str, dict[str, Any]] = {
    "file.read": {"consent": "auto"},
    "file.write": {"consent": "per_goal"},
    "shell.exec": {"consent": "per_goal"},
    "network.req": {"consent": "auto"},
    "memory.read": {"consent": "auto"},
    "git.read": {"consent": "auto"},
    "git.write": {"consent": "per_goal"},
    "connector.run": {"consent": "per_goal"},
    "secret.read": {"consent": "explicit"},
}

ConsentHandler = Callable[[Tool, str, str, dict[str, Any]], bool | Awaitable[bool]]


class CapabilityGate:
    """The single chokepoint. A missing handler never bypasses the policy."""

    def __init__(self) -> None:
        self._memory = get_memory()
        self._st = get_storage()
        self._granted: set[tuple[str, str]] = set()
        self._once_granted: set[str] = set()
        self._moon_goals: dict[str, int] = {}
        self._moon_endpoints: dict[str, list[str]] = {}
        self._auto_grant_all = False
        self._consent_handler: ConsentHandler | None = None

    def set_auto_grant(self, on: bool) -> None:
        """Only test/eval harnesses should enable this explicit bypass."""
        self._auto_grant_all = on

    def set_consent_handler(self, handler: ConsentHandler | None) -> None:
        """Install the interactive consent callback used by CLI/channel frontends."""
        self._consent_handler = handler

    def register_moon(self, moon_name: str, declared_endpoints: list[str]) -> None:
        self._moon_endpoints[moon_name] = declared_endpoints
        self._moon_goals.setdefault(moon_name, 0)

    def moon_completed_goal(self, moon_name: str) -> None:
        self._moon_goals[moon_name] = self._moon_goals.get(moon_name, 0) + 1

    def moon_in_probation(self, moon_name: str) -> bool:
        return self._moon_goals.get(moon_name, 0) < 3

    def _policy_for(self, capability: str, tool_consent: str | None = None) -> dict[str, Any]:
        row = self._st.query_one(
            "SELECT * FROM capability_policy WHERE capability=?;", (capability,))
        if row:
            return {"consent": row["consent"]}
        if tool_consent is not None:
            return {"consent": tool_consent}
        return DEFAULT_POLICY.get(capability, {"consent": "per_goal"})

    def _project_root(self) -> Path:
        from config import get_config
        configured = get_config().get("project_root", "")
        return Path(configured).expanduser().resolve() if configured else Path.cwd().resolve()

    def _resource_allowed(self, tool: Tool, args: dict[str, Any]) -> bool:
        """Evaluate declared path/url/cwd resources against the active project."""
        if not tool.resources:
            return True
        root = self._project_root()
        path_arg = args.get("path") or args.get("cwd")
        if path_arg:
            candidate = Path(str(path_arg)).expanduser()
            if not candidate.is_absolute():
                candidate = root / candidate
            candidate = candidate.resolve()
        else:
            candidate = root
        try:
            relative = candidate.relative_to(root).as_posix()
        except ValueError:
            relative = "../" + candidate.as_posix().lstrip("/")
        relative_with_dot = "./" + relative if relative else "."
        raw_url = args.get("url") or args.get("cdp_url")
        if not raw_url and args.get("host"):
            raw_url = f"http://{args['host']}:{args.get('port', '')}"
        url = str(raw_url or "")
        for resource in tool.resources:
            if resource == "cwd":
                if candidate == root or relative != "../" and not relative.startswith("../"):
                    return True
            elif resource.startswith("path:glob:"):
                pattern = resource.removeprefix("path:glob:")
                if (fnmatch.fnmatch(relative, pattern) or
                        fnmatch.fnmatch(relative_with_dot, pattern) or
                        fnmatch.fnmatch(candidate.as_posix(), pattern)):
                    return True
            elif resource.startswith("url:"):
                # Many built-ins construct their fixed endpoint internally; the
                # handler's declared resource is authoritative when no URL arg
                # is supplied. Explicit URLs still require an allowlist match.
                if not url:
                    return True
                pattern = resource.removeprefix("url:")
                if (fnmatch.fnmatch(url, pattern) or
                        fnmatch.fnmatch(f"https://{url}", pattern) or
                        fnmatch.fnmatch(f"ssh://{url}", pattern)):
                    return True
            elif resource == "network":
                if not url or urlparse(url).scheme in {"http", "https"}:
                    return True
            elif resource.startswith("galaxy:"):
                # Internal Galaxy resources are not filesystem or URL paths;
                # their capability and agent whitelist remain authoritative.
                return True
        return False

    async def _ask_consent(self, tool: Tool, *, agent: str, goal_id: str,
                           args: dict[str, Any]) -> bool:
        if self._consent_handler is None:
            return False
        decision = self._consent_handler(tool, agent, goal_id, args)
        if inspect.isawaitable(decision):
            decision = await decision
        return bool(decision)

    async def _grant_or_block(self, *, tool: Tool, consent: str, agent: str,
                              goal_id: str, args: dict[str, Any], start: float) -> dict[str, Any] | None:
        key = (goal_id, tool.name)
        already = key in self._granted or (consent == "once" and tool.name in self._once_granted)
        if self._auto_grant_all or already or consent == "auto":
            return None
        if consent not in {"once", "per_goal", "explicit"}:
            return None
        approved = await self._ask_consent(tool, agent=agent, goal_id=goal_id, args=args)
        if approved:
            if consent == "once":
                self._once_granted.add(tool.name)
            else:
                self._granted.add(key)
            return None
        audit_log(actor=agent, action=f"tool:{tool.capability}", args=args,
                  result="blocked:consent", goal_id=goal_id,
                  duration_ms=int((time.time() - start) * 1000))
        return {"ok": False, "error": f"{tool.name} requires user consent",
                "needs_consent": True, "capability": tool.capability,
                "tool": tool.name}

    async def enforce(self, tool: Tool, *, agent: str, goal_id: str,
                      args: dict[str, Any]) -> dict[str, Any]:
        start = time.time()
        cap = tool.capability
        action_desc = f"{cap} {args.get('cmd', '') or args.get('path', '') or args.get('url', '')}"
        if self._memory.is_blackhooled(action_desc):
            audit_log(actor=agent, action=f"tool:{cap}", args=args,
                      result="blocked:blackhole", goal_id=goal_id,
                      duration_ms=int((time.time() - start) * 1000))
            return {"ok": False, "error": "blocked by black hole rule", "blocked_by": "blackhole"}
        if not self._resource_allowed(tool, args):
            audit_log(actor=agent, action=f"tool:{cap}", args=args,
                      result="blocked:resource", goal_id=goal_id,
                      duration_ms=int((time.time() - start) * 1000))
            return {"ok": False, "error": "resource outside the active project or allowlist",
                    "blocked_by": "resource"}
        if agent not in self._moon_endpoints:
            from core.core_agents.agents import ALL_AGENTS, get_agent
            if agent in ALL_AGENTS:
                whitelist = getattr(get_agent(agent), "tool_whitelist_names", None)
                core_skill_tools = {"skill.search", "skill.read", "skill.activate"}
                if whitelist is not None and tool.name not in whitelist and tool.name not in core_skill_tools:
                    audit_log(actor=agent, action=f"tool:{cap}", args=args,
                              result="blocked:whitelist", goal_id=goal_id,
                              duration_ms=int((time.time() - start) * 1000))
                    return {"ok": False, "error": f"tool {tool.name!r} not in {agent!r} whitelist",
                            "blocked_by": "whitelist", "whitelist": list(whitelist)}
        if agent in self._moon_endpoints:
            if cap == "shell.exec" and self.moon_in_probation(agent):
                audit_log(actor=agent, action=f"tool:{cap}", args=args,
                          result="blocked:moon_probation", goal_id=goal_id,
                          duration_ms=int((time.time() - start) * 1000))
                return {"ok": False, "error": "shell.exec denied during Moon probation"}
            if cap == "network.req":
                raw_url = args.get("url") or args.get("cdp_url")
                if not raw_url and args.get("host"):
                    raw_url = f"http://{args['host']}:{args.get('port', '')}"
                url = str(raw_url or "")
                allowed = self._moon_endpoints[agent]
                if allowed and not any(fnmatch.fnmatch(url, pattern) for pattern in allowed):
                    audit_log(actor=agent, action=f"tool:{cap}", args=args,
                              result="blocked:moon_egress", goal_id=goal_id,
                              duration_ms=int((time.time() - start) * 1000))
                    return {"ok": False, "error": f"Moon egress restricted to {allowed}"}
        policy = self._policy_for(cap, tool.consent)
        blocked = await self._grant_or_block(tool=tool, consent=policy["consent"],
                                             agent=agent, goal_id=goal_id, args=args,
                                             start=start)
        if blocked:
            return blocked
        try:
            result = await tool.handler(**args) if inspect.iscoroutinefunction(tool.handler) else tool.handler(**args)
            audit_log(actor=agent, action=f"tool:{cap}", args=args, result="ok",
                      goal_id=goal_id, duration_ms=int((time.time() - start) * 1000))
            return {"ok": True, "result": result}
        except Exception as exc:
            audit_log(actor=agent, action=f"tool:{cap}", args=args,
                      result=f"error:{exc.__class__.__name__}", goal_id=goal_id,
                      duration_ms=int((time.time() - start) * 1000))
            return {"ok": False, "error": str(exc)}

    def grant(self, goal_id: str, tool_name: str) -> None:
        self._granted.add((goal_id, tool_name))


_gate: CapabilityGate | None = None


def get_gate() -> CapabilityGate:
    global _gate
    if _gate is None:
        _gate = CapabilityGate()
        from connectors.builtin import get_registry
        get_registry().set_gate(_gate)
    return _gate


def reset_gate_for_tests() -> CapabilityGate:
    global _gate
    _gate = CapabilityGate()
    from connectors.builtin import get_registry
    get_registry().set_gate(_gate)
    return _gate
