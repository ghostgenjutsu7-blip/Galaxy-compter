"""Bounded idle-time memory consolidation loop."""
from __future__ import annotations

import asyncio
import time
from typing import Any

from config import SUBCONSCIOUS_INTERVAL_SECONDS, SUBCONSCIOUS_MAX_CYCLE_SECONDS
from core.memory import get_memory
from skills.loader import verify_all_signatures


class SubconsciousLoop:
    def __init__(self) -> None:
        self._task: asyncio.Task | None = None
        self._running = False
        self._last_cycle_at = 0.0
        self._last_signature_check = 0.0
        self._cycle_count = 0
        self._last_error = ""

    @property
    def is_running(self) -> bool:
        return self._running and self._task is not None and not self._task.done()

    @property
    def last_cycle_at(self) -> float:
        return self._last_cycle_at

    @property
    def cycle_count(self) -> int:
        return self._cycle_count

    @property
    def last_error(self) -> str:
        return self._last_error

    def start(self) -> None:
        if self._task is not None and not self._task.done():
            return
        self._running = True
        loop = asyncio.get_running_loop()
        self._task = loop.create_task(self._run(), name="galaxy-subconscious-loop")

    def stop(self) -> None:
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()

    async def _run(self) -> None:
        while self._running:
            try:
                await asyncio.sleep(SUBCONSCIOUS_INTERVAL_SECONDS)
                from core.agent.orchestrator import get_orchestrator
                if get_orchestrator().is_goal_active():
                    continue
                await self.cycle_once()
            except asyncio.CancelledError:
                break
            except Exception as exc:
                self._last_error = str(exc)

    async def cycle_once(self) -> dict[str, Any]:
        """Run one cancellable cycle and never exceed the configured bound."""
        started = time.monotonic()
        stats: dict[str, Any] = {"promoted": 0, "edges": 0, "compressed": 0,
                                  "signatures_verified": 0, "elapsed_ms": 0,
                                  "timed_out": False, "error": ""}
        try:
            result = await asyncio.wait_for(self._cycle_body(),
                                            timeout=SUBCONSCIOUS_MAX_CYCLE_SECONDS)
            stats.update(result)
        except asyncio.TimeoutError:
            stats["timed_out"] = True
            stats["error"] = "cycle timeout"
            self._last_error = stats["error"]
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            stats["error"] = str(exc)
            self._last_error = str(exc)
        finally:
            stats["elapsed_ms"] = int((time.monotonic() - started) * 1000)
            self._last_cycle_at = time.time()
            self._cycle_count += 1
        return stats

    async def _cycle_body(self) -> dict[str, int]:
        mem = get_memory()
        promoted = mem.promote_idle(threshold=0.45)
        edges = self._connect_stars(mem)
        compressed = mem.l2.forgetting_pass().get("compressed", 0)
        mem.l5.refresh_mirror(mem)
        verified = 0
        if time.time() - self._last_signature_check > 7 * 86400:
            verified = verify_all_signatures().get("verified", 0)
            self._last_signature_check = time.time()
        return {"promoted": len(promoted), "edges": edges,
                "compressed": compressed, "signatures_verified": verified}

    def _connect_stars(self, mem) -> int:
        edges_added = 0
        by_domain: dict[str, list] = {}
        for star in mem.l3.list_stars():
            by_domain.setdefault(star.domain, []).append(star)
        for stars in by_domain.values():
            if len(stars) < 2:
                continue
            stars.sort(key=lambda star: star.interaction_count, reverse=True)
            for left, right in zip(stars, stars[1:]):
                existing = {(edge["src"], edge["dst"]) for edge in mem.l3.edges_of(left.id)}
                existing |= {(edge["src"], edge["dst"]) for edge in mem.l3.edges_of(right.id)}
                if ((left.id, right.id) not in existing and
                        (right.id, left.id) not in existing):
                    mem.l3.add_edge(left.id, right.id, weight=0.5, kind="same_domain")
                    edges_added += 1
        return edges_added


_loop: SubconsciousLoop | None = None


def get_loop() -> SubconsciousLoop:
    global _loop
    if _loop is None:
        _loop = SubconsciousLoop()
    return _loop
