"""tests/conftest.py — shared fixtures for the Galaxy test suite."""
import os
import sys
import shutil
import tempfile
from pathlib import Path

import pytest

# ensure the galaxy-computer package root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture
def fresh_home(monkeypatch):
    """A fresh ~/.galaxy pointing at a temp dir, with migrations applied."""
    tmp = Path(tempfile.mkdtemp(prefix="gax-test-"))
    from config import get_config
    cfg = get_config()
    cfg.reset_for_tests(tmp)
    cfg.ensure_dirs()
    monkeypatch.setenv("GALAXY_HOME", str(tmp))
    from storage.local import reset_storage_for_tests
    reset_storage_for_tests(cfg.db_path)
    from schema.migrations import ensure_latest
    ensure_latest()
    # reset all singletons (order matters: storage first, then everything that
    # caches a storage reference at construction time)
    from core.memory.orbits import get_orbits
    import core.memory.orbits as _orbits_mod
    _orbits_mod._orbits = None  # force re-creation against the new storage
    get_orbits()  # warm cache
    from providers.manager import reset_provider_manager_for_tests
    reset_provider_manager_for_tests()
    from providers.client import reset_llm_client_for_tests
    reset_llm_client_for_tests()
    from core.memory import reset_memory_for_tests
    reset_memory_for_tests()
    from core.core_agents.agents import reset_agents_for_tests
    reset_agents_for_tests()
    from core.agent.orchestrator import reset_orchestrator_for_tests
    reset_orchestrator_for_tests()
    from connectors.builtin import reset_registry_for_tests
    reset_registry_for_tests()
    from security.capability import reset_gate_for_tests
    gate = reset_gate_for_tests()
    gate.set_auto_grant(True)
    import core.memory.subconscious.loop as _loop_mod
    _loop_mod._loop = None
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def fresh_home_with_skills(fresh_home):
    """Fresh home with the real bundled skills (ECC, UI UX Pro Max, Open
    Design, Anthropic Skills — see SOURCES.md) ingested."""
    from skills.loader import load_all_skills
    load_all_skills()
    return fresh_home
