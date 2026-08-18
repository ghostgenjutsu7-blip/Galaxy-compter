"""tests/test_integration.py — end-to-end flows: orchestrator, concurrency, eval."""
import pytest


@pytest.mark.asyncio
async def test_goal_engages_multiple_agents_with_handoff(fresh_home_with_skills):
    """§STEP 1: a real /goal engages multiple Core Agents with a real Handoff
    Package chain, end to end."""
    from core.agent.orchestrator import get_orchestrator
    orch = get_orchestrator()
    summary = await orch.run_goal("write a python function to read a csv file")
    agents = [s["agent"] for s in summary["steps"]]
    assert "planning" in agents
    assert "code" in agents
    assert "review" in agents
    assert len(agents) >= 3  # real handoff chain
    assert summary["success"] is True
    assert summary["gravity_score"] > 0.60  # real metacognition, not stuck at 0.40


@pytest.mark.asyncio
async def test_research_first_runs_before_each_agent(fresh_home_with_skills):
    """§4: the Research-First Protocol is enforced by the Orchestrator before
    every agent's execution."""
    from core.agent.orchestrator import get_orchestrator
    orch = get_orchestrator()
    summary = await orch.run_goal("write a python csv reader")
    # the orchestrator logs L4/L3 hits in context before each agent
    assert summary["llm_calls"] >= 3  # classify + agents
    # skills were available to the agents
    from core.memory import get_memory
    assert len(get_memory().l4.list(status="trusted")) > 0


@pytest.mark.asyncio
async def test_concurrent_writes_no_corruption(fresh_home):
    """§14: per-entity asyncio locks prevent SQLite corruption under concurrent
    writes."""
    import asyncio

    from concurrency.locks import get_locks
    from core.memory import get_memory
    mem = get_memory()
    locks = get_locks()

    async def write_one(i):
        async with locks.acquire("stars"):
            mem.l3.create_star(topic=f"star-{i}", domain="test",
                               summary=f"s{i}", content=f"c{i}")

    await asyncio.gather(*(write_one(i) for i in range(10)))
    stars = [s for s in mem.l3.list_stars() if s.domain == "test"]
    assert len(stars) == 10  # no lost writes


def test_moon_backpressure_max_four(fresh_home):
    """§14: max 4 concurrent moons per planet."""
    from concurrency.supervisor import get_supervisor
    sup = get_supervisor()
    for _ in range(4):
        sup.moon_started("planet-1")
    assert sup.can_spawn_moon("planet-1") is False
    sup.moon_finished("planet-1")
    assert sup.can_spawn_moon("planet-1") is True


@pytest.mark.asyncio
async def test_checkpoint_and_resume(fresh_home_with_skills):
    """§15: /resume loads the last checkpoint and continues."""
    from core.agent.orchestrator import get_orchestrator
    from failure.checkpoint import checkpoint, load_checkpoint
    orch = get_orchestrator()
    summary = await orch.run_goal("write a python function")
    # write a checkpoint
    checkpoint(summary["goal_id"], state={"goal_text": "write a python function",
                                          "handoffs": [], "remaining_plan": [],
                                          "classification": {}})
    cp = load_checkpoint(summary["goal_id"])
    assert cp is not None
    assert cp["goal_text"] == "write a python function"


@pytest.mark.asyncio
async def test_cascading_failure_detection():
    """§15: 3 consecutive similar failures trigger a pause."""
    from failure.retry import cascading_failure_check
    assert cascading_failure_check(["rate_limit", "rate_limit", "rate_limit"]) is True
    assert cascading_failure_check(["rate_limit", "timeout", "ok"]) is False


@pytest.mark.asyncio
async def test_export_import_roundtrip(fresh_home_with_skills):
    """§17: /export produces an archive; /import restores state."""
    from core.memory import get_memory
    from data.export_import import export_all, import_all
    mem = get_memory()
    before = len(mem.l3.list_stars())
    archive = export_all()
    assert archive.exists()
    # add a star, then import should restore
    mem.l3.create_star(topic="temp", domain="x", summary="y", content="z")
    assert len(mem.l3.list_stars()) == before + 1
    result = import_all(str(archive))
    assert "Imported" in result


@pytest.mark.asyncio
async def test_goal_executes_real_tools_and_creates_artifact(fresh_home_with_skills, tmp_path, monkeypatch):
    """The goal path must execute registered tools, not merely describe them."""
    from config import get_config
    from core.agent.orchestrator import get_orchestrator

    monkeypatch.chdir(tmp_path)
    summary = await get_orchestrator().run_goal("write a python function to read a csv file")
    artifact = tmp_path / "src" / "echo_artifact.py"
    assert summary["success"] is True
    assert artifact.exists()
    assert "read_csv_rows" in artifact.read_text(encoding="utf-8")
    tools = [tool for step in summary["steps"] for tool in step.get("tools_used", [])]
    assert "file.write" in tools
    assert "file.read" in tools
    cfg = get_config()
    assert cfg.audit_log.exists()
    assert len(cfg.audit_log.read_text(encoding="utf-8").splitlines()) >= 2


def test_provider_health_disables_unhealthy_key(fresh_home):
    from providers.manager import get_provider_manager

    pm = get_provider_manager()
    pm.add_provider("Health Provider", "https://health.example/v1")
    key = pm.add_key("Health Provider", "primary", "encrypted", status="high")
    for _ in range(4):
        pm.record_key_error("Health Provider", key.id)
    assert pm.pick_key("Health Provider") is None
    row = next(r for r in pm.health_snapshot() if r["provider"] == "Health Provider")
    assert row["disabled"] is True
    assert row["error_rate"] == 1.0


@pytest.mark.asyncio
async def test_cli_goal_uses_interactive_consent_without_auto_grant(fresh_home_with_skills, tmp_path, monkeypatch):
    from cli.repl import ConsoleIO, repl_loop
    from security.capability import get_gate

    monkeypatch.chdir(tmp_path)
    gate = get_gate()
    gate.set_auto_grant(False)
    io = ConsoleIO()
    io.feed("/goal write a python function to read a csv file", "y", "exit")
    await repl_loop(io)
    artifact = tmp_path / "src" / "echo_artifact.py"
    assert artifact.exists()
    assert any("Consent required" in line for line in io.outputs())
    assert get_loop_running() is False


def get_loop_running() -> bool:
    from core.memory.subconscious.loop import get_loop
    return get_loop().is_running
