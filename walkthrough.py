"""walkthrough.py — produces the §STEP 6 '5-minute first goal' transcript.

Simulates a fresh user: clean ~/.galaxy → /setup (3 steps) → /goal that
engages 3+ Core Agents with a real handoff chain → final summary. Prints a
real transcript to stdout.
"""
import sys, os, shutil, asyncio, time
sys.path.insert(0, os.path.dirname(__file__))

HOME = "/tmp/gax_walkthrough"
shutil.rmtree(HOME, ignore_errors=True)
os.makedirs(HOME)
os.environ["GALAXY_HOME"] = HOME

from pathlib import Path
from config import get_config
cfg = get_config()
cfg.reset_for_tests(Path(HOME))
cfg.ensure_dirs()
from storage.local import reset_storage_for_tests
reset_storage_for_tests(cfg.db_path)
from schema.migrations import ensure_latest
ensure_latest()
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
reset_gate_for_tests().set_auto_grant(True)


class TranscriptIO:
    def __init__(self):
        self.inputs = []
        self._idx = 0
    def print(self, *a, **k):
        print(*a, **k)
    def input(self, prompt=""):
        if self._idx < len(self.inputs):
            val = self.inputs[self._idx]
            self._idx += 1
            print(f"{prompt}{val}")
            return val
        return ""
    def confirm(self, prompt):
        return self.input(f"{prompt} [y/N] ").lower() in ("y", "yes")
    def pause(self, prompt=""):
        pass
    def feed(self, *lines):
        self.inputs.extend(lines)


async def main():
    io = TranscriptIO()
    # --- /setup inputs ---
    io.feed(
        "en",        # language
        "n",         # add a provider? no — use Galaxy Echo
        "Ada",       # name
        "Developer", # profession
        "n",         # Free Mode?
        "n",         # Subconscious Loop?
    )
    from cli.setup import run_setup
    print("\n" + "=" * 70)
    print("TRANSCRIPT: Fresh install → /setup → /goal (5-minute first goal)")
    print("=" * 70)
    print("\n$ python -m cli")
    print("galaxy> /setup\n")
    await run_setup(io)

    # --- /goal ---
    print("\n" + "=" * 70)
    print("galaxy> /goal write a python function to read a csv file and print the rows")
    print("=" * 70 + "\n")
    from cli.slash_commands import register_all, get_command
    register_all()
    cmd = get_command("goal")
    start = time.time()
    await cmd.handler(["write a python function to read a csv file and print the rows"], io)
    elapsed = time.time() - start
    print(f"\n[walkthrough complete in {elapsed:.1f}s]")

    # --- /memory to show what was learned ---
    print("\n" + "=" * 70)
    print("galaxy> /memory")
    print("=" * 70 + "\n")
    cmd = get_command("memory")
    await cmd.handler([], io)

    # --- /version ---
    print("\n" + "=" * 70)
    print("galaxy> /version")
    print("=" * 70 + "\n")
    cmd = get_command("version")
    await cmd.handler([], io)

asyncio.run(main())
