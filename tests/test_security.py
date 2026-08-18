"""tests/test_security.py — capability gate, secret filter, audit, sandbox."""
import pytest


@pytest.mark.asyncio
async def test_capability_gate_intercepts_every_call(fresh_home):
    """§STEP 4: the capability gate is a real enforced chokepoint — every
    tool call passes through it."""
    from connectors.builtin import get_registry
    from security.audit import tail_audit
    reg = get_registry()
    # every call should produce an audit entry
    await reg.call("shell.exec", agent="code", goal_id="g1", args={"cmd": "echo a"})
    await reg.call("file.write", agent="code", goal_id="g1",
                   args={"path": "test_file.txt", "content": "x"})
    await reg.call("memory_query", agent="code", goal_id="g1", args={"query": "x"})
    class IO:
        def __init__(self): self.out = []
        def print(self,*a,**k): self.out.append(a)
    io = IO()
    tail_audit(io, 10)
    actions = [a[0] for a in io.out]
    assert any("shell.exec" in str(a) for a in actions)
    assert any("file" in str(a) for a in actions)


@pytest.mark.asyncio
async def test_blackhole_blocks_tool(fresh_home):
    """§10: black hole rules block matching actions."""
    from connectors.builtin import get_registry
    from core.memory import get_memory
    mem = get_memory()
    mem.add_rule(kind="blackhole", rule="rm -rf")
    reg = get_registry()
    r = await reg.call("shell.exec", agent="code", goal_id="g1", args={"cmd": "rm -rf /"})
    assert r["ok"] is False
    assert r["blocked_by"] == "blackhole"


def test_secret_filter_redacts_all_patterns():
    """§10: the SECRET_PATTERNS list redacts sk-, ghp_, JWT, Bearer, etc."""
    from security.secret_filter import redact
    cases = [
        ("key sk-abc123def456ghi789jkl012mno345pqr678", "[REDACTED]"),
        ("pat ghp_abcdefABCDEF0123456789abcdefghij0123456789", "[REDACTED]"),
        ("jwt eyJhbGciOiJIUzI1.eyJzdWIiOiIxMjM0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c", "[REDACTED]"),
        ("auth Bearer abc123def456ghi789jkl012mno345pqr678", "[REDACTED]"),
        ("password=supersecret123", "[REDACTED]"),
    ]
    for raw, _ in cases:
        redacted = redact(raw)
        assert "[REDACTED]" in redacted
        # the original secret must not survive
        for secret in ["sk-abc123", "ghp_abcdef", "eyJhbGci", "Bearer abc", "supersecret123"]:
            if secret in raw:
                assert secret not in redacted, f"{secret} survived redaction"


def test_audit_log_is_append_only_jsonl(fresh_home):
    """§10: the audit log is append-only JSONL on disk."""
    from security.audit import log
    from config import get_config
    import json
    log(actor="test", action="tool:x", args={"a": 1}, result="ok")
    log(actor="test", action="tool:y", args={"b": 2}, result="ok")
    cfg = get_config()
    lines = cfg.audit_log.read_text("utf-8").strip().splitlines()
    assert len(lines) == 2
    for line in lines:
        e = json.loads(line)
        assert "ts" in e and "actor" in e and "action" in e and "nonce" in e


def test_secrets_fallback_roundtrip_without_keyring(fresh_home):
    """§10: on environments without an OS keychain, the passphrase-encrypted
    file fallback actually works (exercised, not unreachable)."""
    from security.secrets_fallback import encrypt_secret, decrypt_secret, keyring_available
    # this sandbox has no keychain — that's the point of the test
    assert keyring_available() is False
    enc = encrypt_secret("my-super-secret-api-key")
    assert enc != "my-super-secret-api-key"
    dec = decrypt_secret(enc)
    assert dec == "my-super-secret-api-key"


def test_sandbox_verify_no_network():
    """§STEP 5: a test that the sandbox genuinely has no network. Skipped if
    Docker isn't available (the faithful equivalent still ships)."""
    from security.sandbox import is_docker_available, verify_no_network
    if not is_docker_available():
        pytest.skip("docker not available in this environment")
    assert verify_no_network() is True


@pytest.mark.asyncio
async def test_moon_probation_denies_shell_scopes_network(fresh_home):
    """§4: a new Moon's shell.exec is denied for 3 goals; network.req is
    restricted to declared endpoints (NOT blocked outright)."""
    from security.capability import get_gate
    gate = get_gate()
    gate.register_moon("test-moon", declared_endpoints=["api.example.com"])
    from connectors.builtin import get_registry
    reg = get_registry()
    # shell.exec denied during probation
    r = await reg.call("shell.exec", agent="test-moon", goal_id="g1", args={"cmd": "ls"})
    assert r["ok"] is False
    assert "probation" in r["error"]
    # network.req to declared endpoint allowed
    r2 = await reg.call("web_fetch", agent="test-moon", goal_id="g1",
                        args={"url": "https://api.example.com/x"})
    # web_fetch may fail at runtime (no network) but must NOT be blocked by egress
    assert r2.get("blocked_by") != "moon_egress"
    # network.req to undeclared endpoint blocked
    r3 = await reg.call("web_fetch", agent="test-moon", goal_id="g1",
                        args={"url": "https://evil.com/x"})
    assert r3["ok"] is False
    assert "egress" in r3["error"]


@pytest.mark.asyncio
async def test_tool_level_consent_overrides_capability_default(fresh_home):
    """§4/§10: a tool's own declared `consent` must be respected even when it
    diverges from its capability's coarse default. `ssh` declares "explicit"
    even though its capability (network.req) defaults to "auto" — it must
    still require explicit consent, not silently inherit the lighter default.
    """
    from security.capability import get_gate
    from connectors.builtin import get_registry
    get_gate().set_auto_grant(False)  # exercise the real (non-bypassed) path
    reg = get_registry()
    r = await reg.call("ssh", agent="devops", goal_id="g-ssh",
                        args={"host": "example.com", "command": "id"})
    assert r["ok"] is False
    assert r["needs_consent"] is True


@pytest.mark.asyncio
async def test_lenient_tool_grant_does_not_leak_to_stricter_sibling(fresh_home):
    """§4/§10: tools are granted individually, not by capability. Using a
    lenient network.req tool (web_search, consent=auto) for a goal must not
    silently pre-authorize a stricter network.req tool (ssh, consent=explicit)
    for that same goal."""
    from security.capability import get_gate
    from connectors.builtin import get_registry
    get_gate().set_auto_grant(False)
    reg = get_registry()
    await reg.call("web_search", agent="research", goal_id="g-shared", args={"query": "x"})
    r = await reg.call("ssh", agent="devops", goal_id="g-shared",
                        args={"host": "example.com", "command": "id"})
    assert r["ok"] is False
    assert r["needs_consent"] is True


@pytest.mark.asyncio
async def test_explicit_grant_unblocks_the_specific_tool(fresh_home):
    """§4: gate.grant(goal_id, tool_name) unblocks exactly that tool for that
    goal, after which the call proceeds past the consent gate."""
    from security.capability import get_gate
    from connectors.builtin import get_registry
    gate = get_gate()
    gate.set_auto_grant(False)
    reg = get_registry()
    blocked = await reg.call("ssh", agent="devops", goal_id="g-grant",
                              args={"host": "example.com", "command": "id"})
    assert blocked["needs_consent"] is True
    gate.grant("g-grant", "ssh")
    after = await reg.call("ssh", agent="devops", goal_id="g-grant",
                            args={"host": "example.com", "command": "id"})
    assert after.get("needs_consent") is None
