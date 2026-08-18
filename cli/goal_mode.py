"""cli/goal_mode.py — Goal mode display (Rich trees, expandable).

§9, §25 Phase 6 ㉴. Renders the live goal header + agent tree + final summary.
The orchestrator calls on_step/on_handoff callbacks that this module renders.
"""
from __future__ import annotations

import time
from typing import Any

from rich.console import Group
from rich.panel import Panel
from rich.tree import Tree
from rich.table import Table
from rich.text import Text


class GoalDisplay:
    """Accumulates goal state and renders the §9-style header + tree."""

    def __init__(self, console) -> None:
        self.console = console
        self.start_time = 0.0
        self.goal_text = ""
        self.context_tokens = 0
        self.max_context = 200_000
        self.steps: list[dict[str, Any]] = []

    def start(self, goal_text: str) -> None:
        self.start_time = time.time()
        self.goal_text = goal_text
        self.steps = []

    def add_step(self, agent: str, instruction: str, status: str = "running") -> None:
        self.steps.append({"agent": agent, "instruction": instruction,
                           "status": status, "start": time.time()})

    def complete_step(self, agent: str, success: bool, what: str) -> None:
        for s in reversed(self.steps):
            if s["agent"] == agent and s["status"] == "running":
                s["status"] = "done" if success else "failed"
                s["what"] = what
                s["end"] = time.time()
                break

    def render_header(self) -> str:
        elapsed = time.time() - self.start_time if self.start_time else 0
        mins, secs = int(elapsed // 60), int(elapsed % 60)
        return (f"Galaxy Computer — Mission: \"{self.goal_text[:40]}\" — "
                f"{mins}:{secs:02d} — "
                f"{self.context_tokens//1000}K/{self.max_context//1000}K")

    def render_tree(self) -> Tree:
        tree = Tree("Mission", guide_style="purple")
        for s in self.steps:
            mark = {"running": "...", "done": "[green]OK[/green]",
                    "failed": "[red]X[/red]"}.get(s["status"], "?")
            label = f"{s['agent']:14s} {s.get('instruction','')[:40]}  {mark}"
            node = tree.add(label)
            if s.get("what"):
                node.add(f"[dim]{s['what'][:60]}[/dim]")
        return tree

    def render_final(self, summary: dict) -> Panel:
        title = f"Mission Complete — {summary['elapsed_ms']/1000:.1f}s elapsed"
        lines = [f"success: {summary['success']}",
                 f"classification: {summary['classification']}",
                 f"gravity: {summary['gravity_score']} ({summary['gravity_bucket']})",
                 f"promoted to L3: {summary['promoted_to_l3']}",
                 "steps:"]
        for s in summary["steps"]:
            mark = "+" if s["success"] else "x"
            lines.append(f"  [{mark}] {s['agent']}: {s['what']}")
        lines.append(f"tokens: {summary['input_tokens']} in / {summary['output_tokens']} out")
        lines.append(f"llm_calls: {summary['llm_calls']}")
        return Panel("\n".join(lines), title=title, border_style="purple")
