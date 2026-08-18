"""cli/repl.py — main REPL loop (Chat mode + slash commands).

§9, §25 Phase 6 ㉓. Chat mode is pure conversation; /goal switches to Goal
mode (cli/goal_mode.py). Every slash command from §8 is registered via
cli/slash_commands.py.

Entry point: `python -m cli` or the `galaxy` console script.
"""
from __future__ import annotations

import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from config import ASCII_HEADER, get_config
from schema.migrations import ensure_latest


class ConsoleIO:
    """IO adapter so wizards can be driven interactively or programmatically."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()
        self._scripted_inputs: list[str] = []
        self._outputs: list[str] = []

    def print(self, *args, **kwargs) -> None:
        line = " ".join(str(a) for a in args)
        self._outputs.append(line)
        self.console.print(line, **kwargs)

    def input(self, prompt: str = "") -> str:
        if self._scripted_inputs:
            val = self._scripted_inputs.pop(0)
            self.console.print(f"{prompt}{val}")
            return val
        return Prompt.ask(prompt) if prompt else input()

    def confirm(self, prompt: str) -> bool:
        if self._scripted_inputs:
            return self._scripted_inputs.pop(0).lower() in ("y", "yes")
        return Prompt.ask(f"{prompt} [y/N]", choices=["y", "n"], default="n") == "y"

    def pause(self, prompt: str = "Press Enter to continue...") -> None:
        if not self._scripted_inputs:
            input(prompt)

    def feed(self, *lines: str) -> None:
        """Programmatic input for tests/eval."""
        self._scripted_inputs.extend(lines)

    def outputs(self) -> list[str]:
        return list(self._outputs)


async def repl_loop(io: ConsoleIO | None = None) -> None:
    """The main REPL. Reads input, dispatches to chat or slash commands."""
    from cli.slash_commands import register_all
    from core.agent.orchestrator import get_orchestrator
    register_all()
    io = io or ConsoleIO()
    from core.memory.subconscious.loop import get_loop
    from security.capability import get_gate
    subconscious = get_loop()
    subconscious.start()

    async def consent_handler(tool, agent: str, goal_id: str, args: dict) -> bool:
        target = args.get("path") or args.get("url") or args.get("cmd") or ""
        io.print(f"Consent required: {tool.name} ({agent}) {target}")
        return io.confirm("Approve this tool for the current goal?")

    get_gate().set_consent_handler(consent_handler)
    io.console.print(ASCII_HEADER)
    # ensure first-launch setup
    cfg = get_config()
    if not cfg.get("setup_complete", False):
        io.console.print("[dim]First launch detected. Run /setup to configure, or just start typing.[/dim]")
    while True:
        try:
            line = io.input("\ngalaxy> ")
        except (EOFError, KeyboardInterrupt):
            io.print("\nGoodbye. The mind that remembers everything.")
            subconscious.stop()
            break
        line = line.strip()
        if not line:
            continue
        if line in ("exit", "quit"):
            io.print("Goodbye. The mind that remembers everything.")
            subconscious.stop()
            break
        if line.startswith("/"):
            await _handle_slash(line, io)
        else:
            # chat mode
            try:
                orch = get_orchestrator()
                reply = await orch.chat(line)
                io.print(Panel(reply, title="Galaxy", border_style="purple"))
            except Exception as e:
                io.print(f"[red]Error:[/red] {e}")


async def _handle_slash(line: str, io: ConsoleIO) -> None:
    from cli.slash_commands import get_command
    parts = line[1:].split()
    if not parts:
        return
    name = parts[0]
    args = parts[1:]
    # handle /agent create, /provider add, /skill <name> --pin, etc.
    if name in ("agent", "provider", "skill", "channel", "mcp", "model", "fallback"):
        if args and args[0] in ("create", "add", "keys", "--pin"):
            cmd_name = name
            args = args  # keep subcommand in args
        else:
            cmd_name = name
    else:
        cmd_name = name
    cmd = get_command(cmd_name)
    if cmd is None:
        # try matching /agent <name>, /channel <name> as the base command
        cmd = get_command(name)
    if cmd is None:
        io.print(f"Unknown command: /{name}. Type /help for the list.")
        return
    try:
        result = cmd.handler(args, io)
        if asyncio.iscoroutine(result):
            result = await result
        if result and isinstance(result, str):
            io.print(result)
    except Exception as e:
        io.print(f"[red]Command failed:[/red] {e}")
        if get_config().debug:
            import traceback
            traceback.print_exc()


def main() -> None:
    """Entry point."""
    cfg = get_config()
    cfg.ensure_dirs()
    ensure_latest()
    # load skills on first launch
    from skills.loader import load_all_skills, skill_counts_by_source
    if not skill_counts_by_source():
        load_all_skills()
    asyncio.run(repl_loop())


if __name__ == "__main__":
    main()
