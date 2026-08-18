"""connectors/builtin/docker.py — docker tool (requires explicit connector.run consent)."""
from __future__ import annotations

from core.agent.base_agent import Tool
from connectors.builtin import ToolRegistry
from connectors.builtin.shell import _run


def docker_build(dockerfile: str = ".", tag: str = "galaxy-build") -> dict:
    return _run(f"docker build -t {tag} {dockerfile}")


def docker_run(image: str, command: str = "", network: str = "none",
               readonly: bool = True, scratch: str = "") -> dict:
    """Run a container. Default: --network=none + read-only FS (quarantine mode)."""
    flags = ["--network=" + network, "--rm"]
    if readonly:
        flags.append("--read-only")
    if scratch:
        flags.append(f"--tmpfs {scratch}:rw,size=64m")
    cmd = f"docker run {' '.join(flags)} {image}"
    if command:
        cmd += f' {command}'
    return _run(cmd)


def docker_ps() -> dict:
    return _run("docker ps -a")


def register(reg: ToolRegistry) -> None:
    reg.register(Tool(name="docker.build", capability="connector.run",
                      description="Build a docker image", handler=docker_build,
                      consent="explicit", resources=["connector:docker"]))
    reg.register(Tool(name="docker.run", capability="connector.run",
                      description="Run a docker container (default: no network, read-only)",
                      handler=docker_run, consent="explicit",
                      resources=["connector:docker"]))
    reg.register(Tool(name="docker.ps", capability="connector.run",
                      description="List docker containers", handler=docker_ps,
                      consent="per_goal", resources=["connector:docker"]))
