"""connectors/builtin/git.py — git operations (read auto-allowed, write prompts)."""
from __future__ import annotations

import subprocess

from core.agent.base_agent import Tool
from connectors.builtin import ToolRegistry
from connectors.builtin.shell import _run


def _repo_arg(repo: str = ".", cwd: str = "", path: str = "") -> str:
    return str(cwd or path or repo or ".")


def git_status(repo: str = ".", cwd: str = "", path: str = "", **_: object) -> dict:
    return _run("git status --porcelain", cwd=_repo_arg(repo, cwd, path))


def git_diff(repo: str = ".", staged: bool = True, cwd: str = "", path: str = "", **_: object) -> dict:
    cmd = "git diff --cached" if staged else "git diff"
    return _run(cmd, cwd=_repo_arg(repo, cwd, path))


def git_log(repo: str = ".", limit: int = 20, cwd: str = "", path: str = "", **_: object) -> dict:
    return _run(f"git log --oneline -{limit}", cwd=_repo_arg(repo, cwd, path))


def git_commit(repo: str = ".", message: str = "", cwd: str = "", path: str = "",
               msg: str = "", **_: object) -> dict:
    repo = _repo_arg(repo, cwd, path)
    message = str(msg or message)
    _run("git add -A", cwd=repo)
    return _run(f'git commit -m "{message}"', cwd=repo)


def git_push(repo: str = ".", remote: str = "origin", branch: str = "",
             cwd: str = "", path: str = "", **_: object) -> dict:
    branch_arg = f" {branch}" if branch else ""
    return _run(f"git push {remote}{branch_arg}", cwd=_repo_arg(repo, cwd, path))


def register(reg: ToolRegistry) -> None:
    reg.register(Tool(name="git.status", capability="git.read",
                      description="Show git status", handler=git_status, consent="auto",
                      resources=["cwd"]))
    reg.register(Tool(name="git.diff", capability="git.read",
                      description="Show git diff", handler=git_diff, consent="auto",
                      resources=["cwd"]))
    reg.register(Tool(name="git.log", capability="git.read",
                      description="Show git log", handler=git_log, consent="auto",
                      resources=["cwd"]))
    reg.register(Tool(name="git.commit", capability="git.write",
                      description="Stage all + commit", handler=git_commit, consent="per_goal",
                      resources=["cwd"]))
    reg.register(Tool(name="git.push", capability="git.write",
                      description="Push to remote (prompts first time per goal)",
                      handler=git_push, consent="per_goal", resources=["cwd"]))
