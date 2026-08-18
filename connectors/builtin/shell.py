"""connectors/builtin/shell.py — shell.exec tool (capability-gated, scoped to cwd).

§6, §10. Prompts on first use per goal. Long-running sessions killed at 5 min.
Quarantine-tier skills run this in a Docker sandbox (security/sandbox.py).

Windows without WSL2 (2026-07): shell.exec routes through
security/windows_sandbox.py's elevated -> unelevated chain automatically —
mirroring upstream's own fallback (see that module's docstring). It NEVER
falls through to unsandboxed execution on its own. Fully unsandboxed
execution is a SEPARATE tool below (shell_exec_unsandboxed, consent=explicit)
so bypassing the sandbox is always a deliberate, gated choice — not
something that happens silently because setup failed.
"""
from __future__ import annotations

import asyncio
import subprocess
import time

from core.agent.base_agent import Tool
from connectors.builtin import ToolRegistry


SHELL_TIMEOUT = 5 * 60  # §10: kill at 5 minutes


def _run(cmd: str, cwd: str = ".", timeout: int = SHELL_TIMEOUT,
         env: dict | None = None) -> dict:
    start = time.time()
    try:
        proc = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True,
            timeout=timeout, env={**__import__("os").environ, **(env or {})},
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "elapsed_ms": int((time.time() - start) * 1000),
            "cmd": cmd,
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout", "cmd": cmd,
                "elapsed_ms": int((time.time() - start) * 1000)}


def shell_exec(cmd: str = "", cwd: str = ".", timeout: int = 120,
               env: dict | None = None, command: str = "", script: str = "",
               **_: object) -> dict:
    cmd = str(cmd or command or script)
    if not cmd:
        return {"ok": False, "error": "missing shell command"}
    if cwd in ("", "."):
        try:
            from config import get_config
            configured_root = str(get_config().get("project_root", "") or "")
            if configured_root:
                cwd = configured_root
        except Exception:
            pass
    from security.windows_sandbox import detect_platform
    plat = detect_platform()
    if plat == "windows_native":
        from security.windows_sandbox import run_sandboxed as run_windows_sandboxed
        result = run_windows_sandboxed(cmd, cwd=cwd, env=env, timeout=min(timeout, SHELL_TIMEOUT))
        if result["ok"] or result.get("returncode") is not None:
            # real execution happened (even a failing command's non-zero
            # exit code counts) — don't fall through to unsandboxed.
            return result
        # both elevated and unelevated setup genuinely failed (not just the
        # command) — surface this clearly rather than silently degrading.
        # The agent/user must explicitly choose shell_exec_unsandboxed below.
        return {"ok": False, "error": result.get("error", "Windows sandbox setup failed"),
                "needs_consent": True, "hint": "use shell_exec_unsandboxed if you need to "
                                               "proceed without a sandbox"}
    return _run(cmd, cwd=cwd, timeout=min(timeout, SHELL_TIMEOUT), env=env)


def shell_exec_unsandboxed(cmd: str = "", cwd: str = ".", timeout: int = 120,
                           env: dict | None = None, command: str = "", script: str = "",
                           **_: object) -> dict:
    """Runs `cmd` with NO sandbox at all — full access to the real
    filesystem and network, on any platform. Only reachable via
    consent=explicit: this is Galaxy's equivalent of upstream's
    "danger-full-access", which is deliberately never an automatic
    fallback (see security/windows_sandbox.py's module docstring)."""
    cmd = str(cmd or command or script)
    if not cmd:
        return {"ok": False, "error": "missing shell command"}
    result = _run(cmd, cwd=cwd, timeout=min(timeout, SHELL_TIMEOUT), env=env)
    result["sandboxed"] = False
    return result


def register(reg: ToolRegistry) -> None:
    reg.register(Tool(
        name="shell.exec", capability="shell.exec",
        description="Execute a shell command (scoped to cwd, 5-min max). On "
                    "Windows without WSL2, runs inside the native Windows "
                    "sandbox (elevated, falling back to unelevated).",
        handler=shell_exec, consent="per_goal",
        resources=["cwd"],
    ))
    reg.register(Tool(
        name="shell_exec_unsandboxed", capability="shell.exec",
        description="Execute a shell command with NO sandbox — full system "
                    "access. Only use when shell.exec reports the sandbox "
                    "could not be set up and the task truly cannot proceed "
                    "otherwise. Always asks for explicit, one-time consent.",
        handler=shell_exec_unsandboxed, consent="explicit",
        resources=["cwd"],
    ))
