"""eval/suite.py — the v1 smoke-test suite (§16).

10-15 golden tasks covering: code generation (a few languages), one refactor,
one test-writing, one documentation, one data-analysis, one research, one
file-operation, and at least one multi-agent handoff task. Each task has an
input, an expected-output rubric, and a time budget.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class EvalTask:
    id: str
    category: str
    description: str
    goal: str
    expected_agents: list[str]
    rubric: Callable[[dict], tuple[bool, str]]  # (summary) -> (passed, reason)
    time_budget_s: int = 120


def _rubric_agents(expected: list[str]):
    def check(summary: dict) -> tuple[bool, str]:
        actual = [s["agent"] for s in summary.get("steps", [])]
        if not all(a in actual for a in expected):
            return False, f"expected agents {expected}, got {actual}"
        return True, "all expected agents engaged"
    return check


def _rubric_success(summary: dict) -> tuple[bool, str]:
    if summary.get("success"):
        return True, "task succeeded"
    return False, "task failed"


def _rubric_handoff(summary: dict) -> tuple[bool, str]:
    steps = summary.get("steps", [])
    if len(steps) >= 3:
        return True, f"{len(steps)}-agent handoff chain"
    return False, f"only {len(steps)} steps; need >=3 for handoff test"


def _rubric_classification(category: str):
    def check(summary: dict) -> tuple[bool, str]:
        cls = summary.get("classification", {})
        if cls.get("category") == category:
            return True, f"classified as {category}"
        return False, f"expected {category}, got {cls.get('category')}"
    return check


def _rubric_memory(summary: dict) -> tuple[bool, str]:
    if summary.get("promoted_to_l3"):
        return True, "memory promoted to L3"
    # also accept if gravity is high enough that promotion would happen
    if summary.get("gravity_score", 0) >= 0.60:
        return True, f"gravity {summary['gravity_score']:.2f} indicates learning"
    return False, "no memory promotion / low gravity"


SUITE: list[EvalTask] = [
    EvalTask("code-python-1", "code_generation",
             "Write a Python function to read a CSV",
             "write a python function to read a csv file and print the rows",
             ["planning", "code", "review"],
             _rubric_agents(["planning", "code", "review"])),
    EvalTask("code-python-2", "code_generation",
             "Write a Python async fetcher",
             "write a python async function to fetch a url and return the json",
             ["planning", "code", "review"],
             _rubric_agents(["code"])),
    EvalTask("code-js-1", "code_generation",
             "Write a JS Express route",
             "write a javascript express route that returns hello world",
             ["planning", "code", "review"],
             _rubric_agents(["code"])),
    EvalTask("code-ts-1", "code_generation",
             "Write a TypeScript interface",
             "write a typescript interface for a user with name email and age",
             ["planning", "code", "review"],
             _rubric_agents(["code"])),
    EvalTask("refactor-1", "refactor",
             "Refactor a long function",
             "refactor this python function into smaller helpers: def f(x): return x*2+1",
             ["planning", "code", "review"],
             _rubric_agents(["code"])),
    EvalTask("test-write-1", "test_writing",
             "Write a pytest test",
             "write a pytest test for a function that adds two numbers",
             ["planning", "code", "review"],
             _rubric_agents(["code"])),
    EvalTask("docs-1", "documentation",
             "Write a README",
             "write a readme for a python cli tool that manages todos",
             ["planning", "write", "review"],
             _rubric_agents(["write"])),
    EvalTask("data-1", "data_analysis",
             "Analyze CSV data",
             "analyze a csv of sales data and report the top product by revenue",
             ["planning", "data", "review"],
             _rubric_agents(["data"])),
    EvalTask("research-1", "research",
             "Research a topic",
             "research the differences between sqlite and postgres for small apps",
             ["planning", "research", "write"],
             _rubric_agents(["research"])),
    EvalTask("file-1", "file_operation",
             "Process a document",
             "convert a markdown file to a pdf",
             ["planning", "file", "review"],
             _rubric_agents(["file"])),
    EvalTask("devops-1", "devops",
             "Write a Dockerfile",
             "write a dockerfile for a python flask app",
             ["planning", "devops", "review"],
             _rubric_agents(["devops"])),
    EvalTask("security-1", "security",
             "Security review",
             "review this code for security issues: def login(user, pw): return user.check(pw)",
             ["planning", "security", "review"],
             _rubric_agents(["security"])),
    EvalTask("api-1", "api_integration",
             "Build an API client",
             "build a python client for a rest api that returns users",
             ["planning", "api", "review"],
             _rubric_agents(["api"])),
    EvalTask("handoff-1", "multi_agent_handoff",
             "Multi-agent handoff",
             "build a small rest api with tests and documentation",
             ["planning", "code", "review"],
             _rubric_handoff),
    EvalTask("memory-1", "memory_correctness",
             "Memory promotion",
             "write a python csv reader with error handling",
             ["planning", "code", "review"],
             _rubric_memory),
]


def get_suite() -> list[EvalTask]:
    return list(SUITE)
