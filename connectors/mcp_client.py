"""connectors/mcp_client.py — MCP server connection manager.

§6, §25 Phase 5 ㉑. REWRITE (2026-07): the previous version of this file
declared three security guarantees in its own docstring that were never
actually enforced in code — confirmed by direct inspection and by the fact
that the wizard's own confirmation message ("read-only, egress limited to
...") was printed unconditionally regardless of what the code actually did.
This rewrite makes all three real:

  1. PROTOCOL CORRECTNESS: real servers require an `initialize` handshake
     before anything else, and can interleave asynchronous notifications
     with responses. The old code skipped the handshake entirely and read
     exactly one line per call, assuming it was the response — verified
     live against the official `@modelcontextprotocol/server-everything`
     reference server that this breaks immediately (the very first
     tools/list call returns a `notifications/tools/list_changed` push
     before the real response). Fixed by matching responses on JSON-RPC id.

  2. READ-ONLY ENFORCEMENT: `read_only=True` (the default) now actually
     blocks tools determined to be non-read-only, using the tool's own MCP
     annotations (`readOnlyHint`) when the server provides them, falling
     back to a name-based heuristic otherwise (verified against the
     reference server: it does not populate annotations, so the heuristic
     path is the common case in practice, not a rare fallback).

  3. EGRESS FILTERING: MCP servers run as subprocesses launched with
     HTTP_PROXY/HTTPS_PROXY pointed at a local per-server proxy (_EgressProxy
     below) that only tunnels CONNECT requests to declared_hosts (+
     localhost). HONEST LIMITATION, stated once here rather than repeated
     in every docstring: this is defense-in-depth against a well-behaved
     subprocess that honors standard proxy env vars (the large majority of
     Node/Python HTTP clients do by default) — it is NOT a kernel-level
     sandbox, and a deliberately malicious server using raw sockets could
     still bypass it. A real network-namespace/iptables-based sandbox is a
     larger undertaking (needs root/capabilities Galaxy doesn't assume it
     has) and is noted as a follow-up, not silently implied to be solved.

Crash-loop supervision (3 crashes in 5 min -> pause) delegates to the
existing `concurrency/supervisor.py::Supervisor` — a first pass of this
rewrite duplicated that exact logic inline here instead of using it, caught
during a later spec cross-check and fixed. `Supervisor` is also what
enforces the unrelated 4-concurrent-Moons-per-Planet limit (§14), so
sharing one instance keeps both concerns in the single module the build
order actually assigns them to, rather than tracking MCP crashes in two
places that don't agree with each other.
"""
from __future__ import annotations

import asyncio
import json
import os
import shlex
import time
from dataclasses import dataclass, field
from typing import Any

from core.agent.base_agent import new_id
from storage.local import get_storage

MCP_PROTOCOL_VERSION = "2024-11-05"  # current stable spec as of 2026-07;
# a 2026-07-28 spec is expected but not yet released — see MCP TypeScript
# SDK v2 beta notes checked while building this.

# Tool names containing any of these are treated as non-read-only when the
# server doesn't supply a readOnlyHint annotation. Best-effort, not a
# guarantee — documented plainly rather than implied to be exhaustive.
_WRITE_HINTS = ("create", "delete", "remove", "write", "update", "send",
                "post", "put", "patch", "execute", "run", "modify", "upload",
                "publish", "deploy", "drop", "truncate", "kill", "terminate",
                "insert", "set", "toggle", "enable", "disable", "register",
                "unregister", "reset", "clear", "cancel", "trigger")
# ^ Extended after live-testing against the real reference server, whose
# tool list includes "toggle-simulated-logging" and
# "trigger-long-running-operation" — clearly state-mutating names that the
# original, narrower list would have missed and treated as read-only. This
# heuristic can never be exhaustive (a tool author can name a write
# operation anything); annotations remain the authoritative signal when a
# server provides them.

# Package-manager bootstrap hosts, auto-allowed on the egress proxy
# SEPARATELY from a server's user-declared_hosts. Discovered necessary by
# live-testing against the real reference server: `npx -y <pkg>` checks
# registry.npmjs.org for version metadata EVEN when the package is already
# cached locally, and treats a 403 (our proxy correctly denying an
# undeclared host) as fatal rather than falling back to the cache — the
# server subprocess never even starts. This is a genuinely different trust
# boundary from the server's own runtime calls: resolving/fetching the
# package is package-manager bootstrap traffic (the same trust level Galaxy
# already extends to `pip install`/`npm install` elsewhere, unrestricted),
# whereas declared_hosts governs what the SERVER itself may reach once it's
# live and handling tool-call arguments — those remain fully restricted.
_PACKAGE_MANAGER_HOSTS = {
    "npx": ["registry.npmjs.org", "npmjs.org", "npmjs.com"],
    "npm": ["registry.npmjs.org", "npmjs.org", "npmjs.com"],
    "uvx": ["pypi.org", "files.pythonhosted.org", "pythonhosted.org"],
    "uv": ["pypi.org", "files.pythonhosted.org", "pythonhosted.org"],
    "pip": ["pypi.org", "files.pythonhosted.org", "pythonhosted.org"],
}


def _bootstrap_hosts_for(command: str) -> list[str]:
    """Which package-manager hosts to auto-allow for this command's launcher,
    based on the first token (e.g. 'npx', 'uvx'). Empty for anything else
    (e.g. a bare 'node path/to/server.js' with no package manager involved
    gets no bootstrap exception — nothing to resolve)."""
    first = command.strip().split(None, 1)[0] if command.strip() else ""
    first = first.rsplit("/", 1)[-1]  # handle an absolute path to the binary
    return _PACKAGE_MANAGER_HOSTS.get(first, [])

# A small curated directory of well-known official servers, so mcp_add_server
# can take a short name instead of requiring the user to already know the
# exact launch command. Verified launchable (via `npx -y <pkg> --help`/plain
# run) while building this, 2026-07. NOT exhaustive — see
# registry.modelcontextprotocol.io for the full community registry; this is
# a starting "top shelf", the Galaxy analogue of Antigravity's MCP Store,
# not a replacement for it.
KNOWN_SERVERS: dict[str, dict[str, Any]] = {
    "everything": {
        "command": "npx -y @modelcontextprotocol/server-everything stdio",
        "description": "Official MCP reference/test server — exercises the full protocol.",
        "declared_hosts": [],
    },
    "filesystem": {
        "command": "npx -y @modelcontextprotocol/server-filesystem {path}",
        "description": "Read/write files under a directory you allow. {path} is required.",
        "declared_hosts": [],
        "requires": ["path"],
    },
    "memory": {
        "command": "npx -y @modelcontextprotocol/server-memory",
        "description": "A simple persistent knowledge-graph memory store.",
        "declared_hosts": [],
    },
    "postgres": {
        "command": "npx -y @modelcontextprotocol/server-postgres {connection_string}",
        "description": "Read-only SQL access to a Postgres database. {connection_string} is required.",
        "declared_hosts": [],
        "requires": ["connection_string"],
    },
    "git": {
        "command": "uvx mcp-server-git --repository {path}",
        "description": "Git operations (log, diff, status) on a local repo. {path} is required.",
        "declared_hosts": [],
        "requires": ["path"],
    },
    # NOTE: @modelcontextprotocol/server-github is NOT listed here — the npm
    # package is deprecated (confirmed on npm, 2026-07: "development moved to
    # github.com/github/github-mcp-server", a separate Go binary with a
    # different install method). Galaxy already has a native github_repo_info
    # / github_create_issue pair in connectors/builtin/thirdparty.py, so
    # nothing is lost by leaving this out rather than pointing at a
    # deprecated package.
}


def _tool_is_read_only(tool_def: dict) -> bool:
    """Best-effort per-tool read-only determination. MCP tool annotations
    win if the server provides them; otherwise a name-based heuristic.
    Defaults permissive (True) for genuinely ambiguous names — the
    documented tradeoff is false negatives on a maliciously-named tool that
    avoids every write-verb, not false positives blocking legitimate reads."""
    ann = tool_def.get("annotations") or {}
    if "readOnlyHint" in ann:
        return bool(ann["readOnlyHint"])
    name = (tool_def.get("name") or "").lower()
    return not any(h in name for h in _WRITE_HINTS)


class _EgressProxy:
    """Minimal local HTTP forward proxy. Only tunnels CONNECT (HTTPS)
    requests to hosts in `allowed_hosts` (+ localhost); everything else gets
    403. Plain (non-TLS) HTTP forwarding is deliberately NOT implemented —
    the overwhelming majority of real third-party API traffic is HTTPS, and
    a half-implemented plaintext relay would be more dangerous than useful
    to claim as "supported". See module docstring for the honest limitation
    on subprocesses that bypass proxy env vars entirely."""

    def __init__(self, allowed_hosts: list[str]):
        self.allowed_hosts = {h.lower() for h in allowed_hosts}
        self._server: asyncio.base_events.Server | None = None
        self.port: int = 0
        self.denied_log: list[str] = []  # last N denied hosts, for diagnostics

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def _host_allowed(self, host: str) -> bool:
        host = host.lower().strip("[]")  # strip IPv6 brackets if present
        if host in ("localhost", "127.0.0.1", "::1"):
            return True
        return host in self.allowed_hosts

    async def start(self) -> None:
        self._server = await asyncio.start_server(self._handle, "127.0.0.1", 0)
        self.port = self._server.sockets[0].getsockname()[1]

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            try:
                await self._server.wait_closed()
            except Exception:
                pass

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            first_line = await asyncio.wait_for(reader.readline(), timeout=10)
            if not first_line:
                writer.close()
                return
            parts = first_line.decode(errors="replace").split()
            if len(parts) < 2:
                writer.close()
                return
            method, target = parts[0], parts[1]
            if method != "CONNECT":
                # Plain HTTP — not relayed (see class docstring). Fail
                # closed rather than silently forwarding unchecked.
                writer.write(b"HTTP/1.1 501 Not Implemented (HTTPS/CONNECT only)\r\n\r\n")
                await writer.drain()
                writer.close()
                return
            host, _, port_s = target.partition(":")
            port = int(port_s) if port_s else 443
            # drain remaining CONNECT request headers
            while True:
                line = await reader.readline()
                if line in (b"\r\n", b""):
                    break
            if not self._host_allowed(host):
                self.denied_log.append(host)
                self.denied_log = self.denied_log[-50:]
                writer.write(b"HTTP/1.1 403 Forbidden\r\n\r\n")
                await writer.drain()
                writer.close()
                return
            try:
                remote_reader, remote_writer = await asyncio.open_connection(host, port)
            except Exception:
                writer.write(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
                await writer.drain()
                writer.close()
                return
            writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            await writer.drain()
            await asyncio.gather(
                self._pipe(reader, remote_writer),
                self._pipe(remote_reader, writer),
                return_exceptions=True,
            )
        except Exception:
            try:
                writer.close()
            except Exception:
                pass

    async def _pipe(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            while True:
                data = await reader.read(65536)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception:
            pass
        finally:
            try:
                writer.close()
            except Exception:
                pass


@dataclass
class MCPServer:
    id: str
    name: str
    command: str
    declared_hosts: list[str] = field(default_factory=list)
    declared_capabilities: list[str] = field(default_factory=list)  # optional extra allowlist
    read_only: bool = True
    connected_at: float = 0.0
    tools: dict[str, dict] = field(default_factory=dict)  # populated by tools/list
    proc: Any = None                 # asyncio.subprocess.Process
    proxy: "_EgressProxy | None" = None
    handshake_ok: bool = False       # True only after a successful tools/list
    _next_id: int = 1
    _lock: Any = None  # asyncio.Lock, created lazily


class MCPClient:
    """Manages MCP server subprocesses: launch, handshake, tool discovery,
    egress-gated calls, and crash supervision (3 crashes in 5 min -> pause)."""

    def __init__(self) -> None:
        self._servers: dict[str, MCPServer] = {}
        self._load()

    def _load(self) -> None:
        st = get_storage()
        try:
            rows = st.query_all("SELECT * FROM mcp_servers;")
        except Exception:
            rows = []
        for r in rows:
            caps_raw = r.get("capabilities") or "[]"
            srv = MCPServer(
                id=r["id"], name=r["name"], command=r["command"],
                declared_hosts=json.loads(r.get("declared_hosts") or "[]"),
                declared_capabilities=json.loads(caps_raw),
                read_only=bool(r.get("read_only", 1)),
                connected_at=r.get("connected_at", time.time()),
            )
            self._servers[r["name"]] = srv

    def add(self, *, name: str, command: str, declared_hosts: list[str] | None = None,
            capabilities: list[str] | None = None, read_only: bool = True) -> MCPServer:
        srv = MCPServer(id=new_id("mcp-"), name=name, command=command,
                        declared_hosts=declared_hosts or [],
                        declared_capabilities=capabilities or [],
                        read_only=read_only, connected_at=time.time())
        self._servers[name] = srv
        st = get_storage()
        try:
            with st.transaction() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO mcp_servers(id,name,command,declared_hosts,"
                    "capabilities,read_only,connected_at) VALUES(?,?,?,?,?,?,?);",
                    (srv.id, name, command, json.dumps(srv.declared_hosts),
                     json.dumps(srv.declared_capabilities), 1 if read_only else 0,
                     srv.connected_at),
                )
        except Exception:
            pass  # table may not exist yet; config still held in-memory
        return srv

    async def remove(self, name: str) -> bool:
        srv = self._servers.pop(name, None)
        if srv is not None:
            await self._stop(srv)
        st = get_storage()
        try:
            with st.transaction() as conn:
                conn.execute("DELETE FROM mcp_servers WHERE name=?;", (name,))
        except Exception:
            pass
        return srv is not None

    async def _stop(self, srv: MCPServer) -> None:
        if srv.proc is not None:
            try:
                srv.proc.terminate()
                await asyncio.wait_for(srv.proc.wait(), timeout=5)
            except Exception:
                try:
                    srv.proc.kill()
                except Exception:
                    pass
        if srv.proxy is not None:
            await srv.proxy.stop()
        srv.proc = None
        srv.proxy = None

    def list_servers(self) -> list[MCPServer]:
        return list(self._servers.values())

    def get(self, name: str) -> MCPServer | None:
        return self._servers.get(name)

    # -- protocol plumbing ---------------------------------------------

    def _gen_id(self, srv: MCPServer) -> int:
        i = srv._next_id
        srv._next_id += 1
        return i

    async def _send(self, srv: MCPServer, msg: dict) -> None:
        line = (json.dumps(msg) + "\n").encode()
        srv.proc.stdin.write(line)
        await srv.proc.stdin.drain()

    async def _recv_response_for(self, srv: MCPServer, expected_id: int,
                                 timeout: float = 20.0) -> dict | None:
        """Read lines until one matches expected_id, silently skipping any
        server-pushed notifications in between (verified live: the
        reference server sends notifications/tools/list_changed BEFORE the
        actual tools/list response on first call)."""
        async def _read():
            while True:
                line = await srv.proc.stdout.readline()
                if not line:
                    return None
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if msg.get("id") == expected_id:
                    return msg
        return await asyncio.wait_for(_read(), timeout=timeout)

    async def _ensure_started(self, srv: MCPServer) -> None:
        if srv._lock is None:
            srv._lock = asyncio.Lock()
        async with srv._lock:
            # NOTE: checking only `proc.returncode is None` is not reliable
            # for a process that exits almost instantly (e.g. a crash-loop
            # test using `false`) — asyncio's SIGCHLD-driven watcher may not
            # have updated returncode yet by the time the very next call
            # checks it, milliseconds later, causing a dead process to look
            # "still starting" and skipping re-launch entirely. handshake_ok
            # is the reliable signal: only a REAL completed tools/list sets
            # it, and any failure explicitly clears it below.
            if srv.proc is not None and srv.proc.returncode is None and srv.handshake_ok:
                return
            srv.handshake_ok = False
            if srv.proxy is not None:
                await srv.proxy.stop()  # clean up a previous failed attempt's proxy
            srv.proxy = _EgressProxy(
                allowed_hosts=list(srv.declared_hosts) + _bootstrap_hosts_for(srv.command))
            await srv.proxy.start()
            env = os.environ.copy()
            for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
                env[k] = srv.proxy.url
            args = shlex.split(srv.command)
            srv.proc = await asyncio.create_subprocess_exec(
                *args, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE, env=env,
            )
            mid = self._gen_id(srv)
            await self._send(srv, {"jsonrpc": "2.0", "id": mid, "method": "initialize",
                                   "params": {"protocolVersion": MCP_PROTOCOL_VERSION,
                                             "capabilities": {},
                                             "clientInfo": {"name": "galaxy-computer",
                                                            "version": "1.0"}}})
            resp = await self._recv_response_for(srv, mid)
            if resp is None or "error" in resp:
                raise RuntimeError(f"MCP initialize failed for {srv.name!r}: {resp}")
            await self._send(srv, {"jsonrpc": "2.0", "method": "notifications/initialized",
                                   "params": {}})
            mid2 = self._gen_id(srv)
            await self._send(srv, {"jsonrpc": "2.0", "id": mid2, "method": "tools/list",
                                   "params": {}})
            resp2 = await self._recv_response_for(srv, mid2)
            if resp2 is None:
                raise RuntimeError(f"MCP tools/list got no response for {srv.name!r}")
            tools = ((resp2 or {}).get("result") or {}).get("tools", [])
            srv.tools = {t["name"]: t for t in tools}
            srv.handshake_ok = True

    def _record_crash(self, srv: MCPServer) -> None:
        from concurrency.supervisor import get_supervisor
        get_supervisor().record_crash(srv.name)

    # -- public API -------------------------------------------------------

    async def list_tools(self, name: str) -> dict:
        """Connect (if needed) and return the server's REAL discovered tool
        list — the authoritative source, not whatever a user typed at
        add-time."""
        srv = self._servers.get(name)
        if srv is None:
            return {"ok": False, "error": f"unknown MCP server {name!r}"}
        from concurrency.supervisor import get_supervisor
        if get_supervisor().is_paused(name):
            return {"ok": False, "error": "server paused (crash loop)"}
        try:
            await self._ensure_started(srv)
        except Exception as e:
            self._record_crash(srv)
            return {"ok": False, "error": f"failed to start/handshake: {e}"}
        return {"ok": True, "tools": [
            {"name": t["name"], "description": t.get("description", ""),
             "read_only": _tool_is_read_only(t)}
            for t in srv.tools.values()
        ]}

    async def call(self, name: str, tool: str, params: dict | None = None) -> dict:
        """Invoke a tool on an MCP server via JSON-RPC. Enforces (in order):
        server paused? -> tool actually exists (per real tools/list)? ->
        within the optional declared_capabilities allowlist, if any is set?
        -> read_only gating? Only then does the call go out."""
        srv = self._servers.get(name)
        if srv is None:
            return {"ok": False, "error": f"unknown MCP server {name!r}"}
        from concurrency.supervisor import get_supervisor
        if get_supervisor().is_paused(name):
            return {"ok": False, "error": "server paused (crash loop)"}
        try:
            await self._ensure_started(srv)
        except Exception as e:
            self._record_crash(srv)
            return {"ok": False, "error": f"failed to start/handshake: {e}"}

        if tool not in srv.tools:
            return {"ok": False, "error": f"tool {tool!r} not found on server {name!r} "
                                          f"(discovered: {sorted(srv.tools)})"}
        if srv.declared_capabilities and tool not in srv.declared_capabilities:
            return {"ok": False, "error": f"tool {tool!r} not in the declared "
                                          f"capability allowlist for {name!r}"}
        if srv.read_only and not _tool_is_read_only(srv.tools[tool]):
            return {"ok": False,
                    "error": f"{tool!r} on {name!r} looks like a write operation; "
                             f"the server is configured read_only=True",
                    "needs_consent": True}
        try:
            mid = self._gen_id(srv)
            await self._send(srv, {"jsonrpc": "2.0", "id": mid, "method": "tools/call",
                                   "params": {"name": tool, "arguments": params or {}}})
            resp = await self._recv_response_for(srv, mid)
            if resp is None:
                raise RuntimeError("no response from MCP server (timeout)")
            if "error" in resp:
                return {"ok": False, "error": resp["error"]}
            result = resp.get("result")
            # MCP tool output is external, untrusted content (§10) exactly
            # like any other tool that reads outside data.
            return {"ok": True,
                    "result": f"[UNTRUSTED:mcp:{name}] {json.dumps(result)[:8000]}"}
        except Exception as e:
            self._record_crash(srv)
            return {"ok": False, "error": str(e)}


_mcp: MCPClient | None = None


def get_mcp_client() -> MCPClient:
    global _mcp
    if _mcp is None:
        _mcp = MCPClient()
    return _mcp


def reset_mcp_client_for_tests() -> MCPClient:
    global _mcp
    _mcp = MCPClient()
    return _mcp
