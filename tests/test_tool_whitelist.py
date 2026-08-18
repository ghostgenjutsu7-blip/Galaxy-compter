"""tests/test_tool_whitelist.py — Phase 0.1 enforcement regression.

The codebase previously declared `tool_whitelist_names` on every Core Agent but
never checked it; any agent could call any tool. This file proves the check is
now real: an agent genuinely CANNOT call a tool outside its whitelist.
"""
import pytest


@pytest.mark.asyncio
async def test_agent_cannot_call_tool_outside_its_whitelist(fresh_home):
    """Phase 0.1: the Research Agent's whitelist is web-only. It must NOT be
    able to call file.write — the gate has to reject it, not just decorate
    the agent object."""
    from connectors.builtin import get_registry
    reg = get_registry()
    r = await reg.call("file.write", agent="research", goal_id="g1",
                       args={"path": "test_file.txt", "content": "x"})
    assert r["ok"] is False
    assert r["blocked_by"] == "whitelist"
    assert "research" in r["error"]
    assert "file.write" in r["error"]
    assert "file.write" not in r.get("whitelist", [])


@pytest.mark.asyncio
async def test_agent_can_call_tool_inside_its_whitelist(fresh_home):
    """Phase 0.1 sanity: the Code Agent CAN still call file.write — the
    enforcement doesn't accidentally block legitimate calls."""
    from connectors.builtin import get_registry
    reg = get_registry()
    r = await reg.call("file.write", agent="code", goal_id="g1",
                       args={"path": "test_file.txt", "content": "ok"})
    assert r["ok"] is True


@pytest.mark.asyncio
async def test_whitelist_check_uses_exact_tool_names_not_prefix(fresh_home):
    """Phase 0.1: agents historically declared 'git' / 'docker' as whitelist
    entries, but the real tools are named git.status, git.diff, docker.build,
    etc. The whitelists now declare the exact tool names. Verify a DevOps agent
    CAN call git.status (real name) and that the moon-probation test path still
    works for non-core agents."""
    from connectors.builtin import get_registry
    from core.core_agents.agents import get_agent
    reg = get_registry()
    a = get_agent("devops")
    # whitelists now contain exact tool names, not the old 'git' / 'docker' prefixes
    assert "git.status" in a.tool_whitelist_names
    assert "git" not in a.tool_whitelist_names
    assert "docker.build" in a.tool_whitelist_names
    assert "docker" not in a.tool_whitelist_names
    # the gate will reach the real git.status handler (it may fail at runtime
    # because we're not in a git repo, but it must NOT be blocked:whitelist)
    r = await reg.call("git.status", agent="devops", goal_id="g1", args={"repo": "."})
    assert r.get("blocked_by") != "whitelist"


@pytest.mark.asyncio
async def test_whitelist_does_not_apply_to_moon_agents(fresh_home):
    """Phase 0.1: Moons are registered separately via register_moon() and have
    no static tool_whitelist_names. The whitelist check must NOT block them —
    the moon-probation check is their restriction model."""
    from security.capability import get_gate
    from connectors.builtin import get_registry
    gate = get_gate()
    gate.register_moon("test-moon-2", declared_endpoints=["api.example.com"])
    reg = get_registry()
    # moon calls web_fetch on its declared endpoint — must not be blocked:whitelist
    r = await reg.call("web_fetch", agent="test-moon-2", goal_id="g1",
                       args={"url": "https://api.example.com/x"})
    assert r.get("blocked_by") != "whitelist"


@pytest.mark.asyncio
async def test_whitelist_block_is_audited(fresh_home):
    """Phase 0.1: a blocked-by-whitelist call must produce an audit entry so
    the operator can see someone tried to escape their whitelist."""
    from connectors.builtin import get_registry
    from security.audit import tail_audit
    reg = get_registry()
    await reg.call("shell.exec", agent="write", goal_id="g1",
                   args={"cmd": "echo should-be-blocked"})
    # write agent's whitelist is ["file.read", "file.write", "memory_query"]
    # — shell.exec is not in it
    class IO:
        def __init__(self): self.out = []
        def print(self, *a, **k): self.out.append(a)
    io = IO()
    tail_audit(io, 20)
    lines = " ".join(str(a) for a in io.out)
    assert "blocked:whitelist" in lines
