"""connectors/builtin/__init__.py — built-in connectors + tool registry.

§6, §25 Phase 5 ⑳. The built-in tools every agent can use: file system,
shell, web, git, docker, memory query. Each tool declares its capability
(verb on a resource) so the Capability Gate (security/capability.py) can
enforce policy at a single chokepoint.

The ToolRegistry is the single place tools are registered; agents reference
tools by name, and the Orchestrator resolves names -> implementations here.
Every call goes through the capability gate (set via set_gate()).
"""
from __future__ import annotations

from typing import Any

from core.agent.base_agent import Tool


class ToolRegistry:
    """Global registry of tool implementations. Every agent's tool whitelist
    resolves through here, and every call routes through the capability gate."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}
        self._gate: Any = None  # security.capability.CapabilityGate, set in Phase 8

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool
        try:
            from observability.tool_lifecycle import register_catalog_entry
            register_catalog_entry(name=tool.name, kind="builtin", description=tool.description,
                                  source="builtin_registry", status="registered",
                                  details={"capability": tool.capability, "consent": tool.consent})
        except Exception:
            pass

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return sorted(self._tools.keys())

    def set_gate(self, gate: Any) -> None:
        self._gate = gate

    async def call(self, name: str, *, agent: str, goal_id: str,
                   args: dict[str, Any]) -> dict[str, Any]:
        """Invoke a tool through the mandatory Capability Gate."""
        tool = self._tools.get(name)
        from observability.tool_lifecycle import record_tool_lifecycle
        record_tool_lifecycle(goal_id=goal_id, agent=agent, name=name, phase="invoked",
                              status="requested", source="registry", details={"args": args})
        if tool is None:
            record_tool_lifecycle(goal_id=goal_id, agent=agent, name=name, phase="failed",
                                  status="unknown_tool", source="registry")
            return {"ok": False, "error": f"unknown tool {name!r}"}
        if self._gate is None:
            from security.capability import get_gate
            self._gate = get_gate()
        call_args = dict(args)
        if name == "skill.activate":
            call_args.setdefault("agent", agent)
            call_args.setdefault("goal_id", goal_id)
        result = await self._gate.enforce(tool, agent=agent, goal_id=goal_id, args=call_args)
        if result.get("ok"):
            record_tool_lifecycle(goal_id=goal_id, agent=agent, name=name, phase="verified",
                                  status="success", source="registry", details={"result_type": type(result.get("result")).__name__})
        else:
            record_tool_lifecycle(goal_id=goal_id, agent=agent, name=name, phase="failed",
                                  status="error", source="registry", details={"error": result.get("error", "")})
        return result


_registry: ToolRegistry | None = None


def get_registry() -> ToolRegistry:
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
        _register_builtins(_registry)
    return _registry


def reset_registry_for_tests() -> ToolRegistry:
    global _registry
    _registry = ToolRegistry()
    _register_builtins(_registry)
    return _registry


def _register_builtins(reg: ToolRegistry) -> None:
    """Register every built-in tool. Called once at registry creation."""
    from connectors.builtin.browser import register as reg_browser
    from connectors.builtin.capabilities import register as reg_capabilities
    from connectors.builtin.skills import register as reg_skills
    from connectors.builtin.data import register as reg_data
    from connectors.builtin.devops import register as reg_devops
    from connectors.builtin.docker import register as reg_docker
    from connectors.builtin.files import register as reg_files
    from connectors.builtin.git import register as reg_git
    from connectors.builtin.mcp_tools import register as reg_mcp
    from connectors.builtin.memory import register as reg_memory
    from connectors.builtin.misc import register as reg_misc
    from connectors.builtin.shell import register as reg_shell
    from connectors.builtin.thirdparty import register as reg_thirdparty
    from connectors.builtin.vision import register as reg_vision
    from connectors.builtin.web import register as reg_web
    reg_files(reg)
    reg_shell(reg)
    reg_web(reg)
    reg_git(reg)
    reg_docker(reg)
    reg_memory(reg)
    reg_misc(reg)
    reg_browser(reg)
    reg_capabilities(reg)
    reg_skills(reg)
    reg_data(reg)
    reg_vision(reg)
    reg_devops(reg)
    reg_thirdparty(reg)
    reg_mcp(reg)
