# Security Guide

Galaxy Computer v1 ships with a real security model from day one, not as a
later patch. This document explains what Galaxy protects you against, how those
protections are implemented, and how to configure them for your own threat
model. It is a user-facing companion to the architecture document; for the
authoritative engineering reference, see section 10 of the Galaxy Computer v1
Final specification.

Galaxy is MIT-licensed open source. Everything described here runs on your own
machine; there is no Galaxy-hosted backend involved in the Desktop edition.

---

## 1. Threat Model

Galaxy treats twelve specific threats as first-class concerns. The table below
lists each one, its severity, and the defense that ships in v1.

| Threat | Severity | Defense |
|---|---|---|
| Prompt injection via web/file content | High | All retrieved content is treated as data, never as instructions. It is tagged in context as `[UNTRUSTED: from web_search]`, and the system prompt explicitly forbids following any instruction found inside tagged content. |
| Secret leakage in logs | High | An output filter scrubs `sk-*`, `sk-ant-*`, `ghp_*`, `xox[baprs]-*`, `AIza...`, JWT-shaped strings, `Bearer ...` tokens, and `password=...` patterns before anything is logged or displayed. Entropy-based detection catches unknown secret shapes. |
| Exfiltration via tool call | High | Network egress allowlist. Default allow covers only declared API hosts; everything else is denied by default. The user can extend the list. |
| Runaway tool loops | High | Cascading-failure protection pauses and asks the user after repeated similar failures, rather than retrying indefinitely. |
| Malicious skill execution | High | Skill signing (SHA-256 at ingest). Community/unsigned skills are quarantined. Every tool call is capability-scoped through the Capability Gate. |
| Malicious MCP server | Medium | Capability manifest required. Egress filtering. Read-only filesystem by default for untrusted servers. |
| Local file exfiltration | Medium | File operations are scoped to the active project plus an explicit path allowlist. |
| Privilege escalation via shell | High | `shell.exec` prompts on first use per goal. Long-running shell sessions are killed at 5 minutes. |
| Supply chain (compromised skill source) | Medium | Pinned versions. The Subconscious Loop re-verifies signatures weekly. |
| LLM provider exposure of user data | Medium | Clear documentation on what data goes to which provider. Local Mode (Ollama) is available for sensitive goals. |
| Local privilege escalation | Medium | Galaxy runs as the user and never requests `sudo`. If a task would need elevated privileges, Galaxy stops and explains why instead. |

---

## 2. Trust Boundaries

Every arrow in the diagram below is a trust boundary. The Capability Gate is
the single chokepoint through which every tool call must pass. The Audit Log is
append-only; the Subconscious Loop operates alongside the active goal but never
bypasses the gate.

```
[User]  <-->  [Orchestrator]  <-->  [Agent]  <-->  [Capability Gate]  <-->  [Tool]  <-->  [Resource]
                  |                              |
                  v                              v
              [Audit Log]               [Subconscious Loop]
```

- The **User** issues goals and approves first-use prompts.
- The **Orchestrator** classifies, routes, and supervises agents. It owns the
  event loop.
- The **Agent** (Code, Research, Write, Review, etc.) executes work and
  requests tool calls.
- The **Capability Gate** checks each requested tool call against the active
  policy table, the user's overrides, and the trust tier of the requesting
  skill. A denied call never reaches the Tool layer.
- The **Tool** performs the actual side effect (file read, shell exec, HTTP
  request, etc.).
- The **Resource** is the file, process, network endpoint, or external API
  that the tool ultimately touches.
- The **Audit Log** records every gate decision and tool result as metadata
  only.
- The **Subconscious Loop** runs in the background (yielding entirely to any
  active user goal) and is responsible for periodic tasks such as re-verifying
  skill signatures and decaying idle-skill confidence.

---

## 3. Secret Management

### Storage

User API keys and connector tokens are encrypted with **AES-256-GCM**. The
encryption key itself is stored using the highest-available mechanism on the
host:

1. **OS keychain** (preferred). Galaxy uses the `keyring` Python library. When
   a usable keychain backend is present (macOS Keychain, Windows Credential
   Manager, GNOME Keyring, KWallet, etc.), the AES key lives there and is
   decrypted only at call time.
2. **Passphrase-encrypted file fallback**. When `keyring` cannot find a usable
   backend, Galaxy automatically falls back to a passphrase-encrypted local
   file rather than refusing to start.

The fallback exists on purpose. Most headless Linux servers and containers do
not run a keychain daemon. The planned Server/subscription edition (section 22
of the spec) will run on exactly this kind of headless infrastructure, and a
security design that only works on a desktop with a GUI keychain would quietly
break the moment it was deployed there. Building the fallback into v1 means the
same code path is exercised on day one, instead of being bolted on later under
deadline pressure.

### Rules

- A key is never pasted into chat. `/provider add` is the only path in.
- LLM API keys in request headers are never logged. They are stripped at the
  log boundary by the secret filter described below.
- `/provider keys` can rotate keys without restarting Galaxy.
- Exported archives (`/export`) never contain secrets. Re-importing on a new
  machine requires re-adding API keys.

---

## 4. Output Secret Filter

Pattern-matched redaction is applied at every log boundary and at the display
boundary. The filtered output is what gets logged AND what gets shown to the
user. The default pattern set is:

```python
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",                                          # OpenAI / most providers
    r"sk-ant-[A-Za-z0-9-]{20,}",                                     # Anthropic
    r"ghp_[A-Za-z0-9]{30,}",                                         # GitHub PAT
    r"xox[baprs]-[A-Za-z0-9-]{10,}",                                 # Slack
    r"AIza[A-Za-z0-9_-]{35}",                                        # Google API key
    r"eyJ[A-Za-z0-9_=-]+\.eyJ[A-Za-z0-9_=-]+\.?[A-Za-z0-9_.+/=-]*",  # JWT
    r"Bearer\s+[A-Za-z0-9_.-]{20,}",                                 # Bearer tokens
    r"password\s*[:=]\s*\S+",                                        # password= in config
]
```

In addition, an entropy-based detector flags high-entropy strings of unknown
shape that look like credentials. Anything flagged is replaced with
`[REDACTED:secret]` before it reaches the log file or the terminal.

---

## 5. Audit Log

Every tool call, capability decision, and significant state transition is
written to an immutable, append-only JSONL file at `~/.galaxy/audit.log`:

```json
{"ts": "2026-06-16T22:38:39Z", "actor": "code_agent", "action": "tool:shell.exec",
 "args": {"cmd": "npm test"}, "result": "ok",
 "duration_ms": 4200, "nonce": "0192b7c1-..."}
```

- **Rotation:** at 100 MB.
- **Retention:** 90 days by default.
- **Content:** metadata only. Prompts and completions are never written to the
  audit log, so it cannot become a long-lived file full of sensitive content.
- **Inspection:** `/audit` lets the user query their own log.
- **Non-repudiation:** each entry carries a UUIDv7 nonce so duplicates and
  retries are distinguishable from genuine duplicate actions.

---

## 6. Sandboxing

The execution environment for `shell.exec` depends on the trust tier of the
requesting skill.

| Skill tier | Execution environment |
|---|---|
| Quarantine (community, unsigned) | Docker container with `--network=none` and a read-only filesystem, plus optional scratch space for output. |
| Trusted, signed L4 | Native execution, always through the Capability Gate and Audit Log. |
| Future work (post-v1) | Full gVisor or Firecracker isolation for untrusted skills. Not in v1. |

The user can also force Docker sandboxing for all `shell.exec` calls
regardless of trust tier, via `/profile` -> Security.

---

## 7. Skill Signing

At ingest time, Galaxy computes a SHA-256 hash of each skill's normalized
content. The hash is stored alongside the skill record.

- For the four trusted sources, the hash is stored at load time and
  **re-verified weekly by the Subconscious Loop**. This protects against the
  upstream repo silently changing after Galaxy has already vetted it, which is
  a different and narrower concern than trusting the content in the first
  place.
- For community skills, both the hash and the source URL are stored. A hash
  mismatch on re-fetch quarantines the skill and notifies the user, rather
  than silently accepting changed code.

A quarantined skill appears in `/quarantine` and is not auto-activated. If the
user manually approves it, it still runs sandboxed (Docker, no network).

---

## 8. Network Egress Policy

Galaxy's network policy is explicit and conservative.

**Default allow** (outbound):

- LLM provider base URLs, as configured by the user via `/provider add`.
- The Composio API (for connectors).
- Standard package registries: npm, PyPI, crates.io, the Go module proxy.

**Default deny** (outbound):

- Anything not on the allow list above.
- Localhost access from MCP servers, unless the user has explicitly declared
  the loopback endpoint.
- Cloud metadata endpoints, specifically `169.254.169.254` and equivalents on
  other clouds. This closes off a well-known SSRF-style path that matters if
  Galaxy is ever run inside a cloud VM.

The user can extend the allow list from `/profile` -> Security.

---

## 9. User Overrides

`/profile` -> Security exposes the full set of user-tunable security knobs:

| Override | Effect |
|---|---|
| Tighten `file.write` | Require per-action confirmation before any write to disk. |
| Whitelist shell commands | Restrict `shell.exec` to a fixed allowlist of commands. |
| Extend egress | Add specific hosts to the default-allow list. |
| Force Docker | Run all `shell.exec` calls (including trusted-tier) inside a Docker sandbox. |
| Local Mode | Set a fully offline mode for specific solar systems; all LLM calls route to a local model (Ollama, LM Studio, vLLM). |

These overrides are per-profile, so a user running Galaxy on both a work
machine and a personal one can carry different policies on each.

---

## 10. The Capability-Scoped Tool Model

Every tool exposed to an agent is annotated with a `@capability` decorator
that declares the capability it requires (for example, `file.write`,
`shell.exec`, `http.egress`, `mcp.invoke`). The Capability Gate consults a
default policy table to decide whether a given agent invoking a given
capability is allowed, denied, or requires an interactive first-use prompt.

The default policy is conservative: high-impact capabilities (`file.write`,
`shell.exec`, `http.egress`) require a first-use prompt per goal. The
first-use prompt, once approved by the user, is saved as a **White Hole** in
the agent's session memory: a permanent, auditable record of what the user
consented to and when. Subsequent calls within the same goal do not re-prompt;
calls in a new goal start the flow over again.

Capabilities never invoked by an agent are simply absent from its policy
context, so an agent cannot escalate by requesting a capability it has never
been granted.

---

## 11. Reporting a Security Issue

Security issues should be reported responsibly. Please do not open a public
GitHub issue for a vulnerability. Instead, open a private vulnerability report
through the repository's security tab, or contact the maintainers directly with
details and reproduction steps.

Galaxy is MIT-licensed and accepts responsible disclosure in good faith.
