"""core/agent/task_graph.py — parallel execution + dependency tracking.

§4, §25 Phase 3 ⑯. A Planet's plan becomes a DAG of steps. Steps with no
unmet dependencies run in parallel (up to the 4-Moons-per-Planet backpressure
limit, §14). Steps with dependencies wait. The Orchestrator owns the event
loop and feeds the graph.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable


@dataclass
class Step:
    id: str
    agent: str
    instruction: str = ""
    depends_on: list[str] = field(default_factory=list)
    status: str = "pending"  # pending | running | done | failed | skipped
    result: Any = None
    error: str = ""


class TaskGraph:
    """A DAG of Steps. run() executes ready steps in parallel under a
    concurrency semaphore."""

    def __init__(self, steps: list[Step], max_concurrency: int = 4) -> None:
        self.steps: dict[str, Step] = {s.id: s for s in steps}
        self.max_concurrency = max_concurrency

    def ready_steps(self) -> list[Step]:
        return [s for s in self.steps.values()
                if s.status == "pending"
                and all(self.steps[d].status == "done" for d in s.depends_on if d in self.steps)]

    def is_complete(self) -> bool:
        return all(s.status in ("done", "failed", "skipped") for s in self.steps.values())

    async def run(self, executor: Callable[[Step], Awaitable[Any]],
                  on_step_done: Callable[[Step], Awaitable[None]] | None = None) -> dict[str, Any]:
        """Execute the graph. executor(step) -> result. Returns step results."""
        sem = asyncio.Semaphore(self.max_concurrency)
        pending: set[asyncio.Task] = set()

        async def run_one(step: Step) -> None:
            async with sem:
                step.status = "running"
                try:
                    step.result = await executor(step)
                    step.status = "done"
                except Exception as e:
                    step.error = str(e)
                    step.status = "failed"
                if on_step_done:
                    await on_step_done(step)

        while not self.is_complete():
            ready = self.ready_steps()
            if not ready:
                # nothing ready but not complete -> blocked by a failure
                if not pending:
                    break
                # wait for in-flight to potentially unblock
                done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
                continue
            for step in ready:
                pending.add(asyncio.create_task(run_one(step)))
            if pending:
                done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        # drain
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        return {sid: {"status": s.status, "result": s.result, "error": s.error}
                for sid, s in self.steps.items()}
