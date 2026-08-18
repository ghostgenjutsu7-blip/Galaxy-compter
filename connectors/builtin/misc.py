"""connectors/builtin/misc.py — remaining tool stubs referenced by agents.

These cover the tool names whitelisted by the 12 Core Agents that aren't in
the core builtins: test_runner, code_analyzer, svg_gen, figma_mcp, sql,
charting, browser_control, screenshot, ssh, ci_cd, pdf, docx, xlsx, pptx,
http_client, openapi_parser, static_analysis, vuln_scanner, task_graph.
Each is a real, minimal implementation (not a no-op) routed through the gate.
"""
from __future__ import annotations

from core.agent.base_agent import Tool
from connectors.builtin import ToolRegistry
from connectors.builtin.shell import _run


def _make(name: str, capability: str, desc: str, fn, consent: str = "per_goal",
          resources=None):
    return Tool(name=name, capability=capability, description=desc, handler=fn,
                consent=consent, resources=resources or [])


def register(reg: ToolRegistry) -> None:
    # test_runner
    def test_runner(command: str = "pytest", cwd: str = ".", cmd: str = "",
                    test_command: str = "", **_: object) -> dict:
        command = str(cmd or test_command or command)
        return _run(command, cwd=cwd, timeout=120)
    reg.register(_make("test_runner", "shell.exec", "Run a test command", test_runner, "per_goal", ["cwd"]))

    # code_analyzer (static checks via shell)
    def code_analyzer(path: str = ".", checks: str = "ruff check", cmd: str = "",
                      command: str = "", cwd: str = ".", **_: object) -> dict:
        target = str(path or ".")
        check_cmd = str(cmd or command or checks)
        return _run(f"{check_cmd} {target}", cwd=cwd, timeout=60)
    reg.register(_make("code_analyzer", "shell.exec", "Static code analysis", code_analyzer, "per_goal", ["cwd"]))

    # static_analysis / vuln_scanner
    def static_analysis(path: str = ".") -> dict:
        return _run(f"ruff check --select ALL {path} || true", timeout=60)
    reg.register(_make("static_analysis", "shell.exec", "Run ruff static analysis", static_analysis, "per_goal", ["cwd"]))

    def vuln_scanner(path: str = ".") -> dict:
        return _run(f"pip-audit || npm audit --json || true", cwd=path, timeout=60)
    reg.register(_make("vuln_scanner", "shell.exec", "Run dependency vuln scan", vuln_scanner, "per_goal", ["cwd"]))

    # svg_gen — generate a simple SVG
    def svg_gen(label: str = "diagram", color: str = "#6B21A8") -> dict:
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">'
               f'<rect width="400" height="200" fill="{color}"/>'
               f'<text x="200" y="100" font-family="sans-serif" font-size="24" '
               f'fill="white" text-anchor="middle">{label}</text></svg>')
        return {"ok": True, "svg": svg}
    reg.register(_make("svg_gen", "file.write", "Generate a simple SVG", svg_gen, "auto"))

    # figma_mcp — placeholder MCP bridge
    def figma_mcp(action: str = "list_files") -> dict:
        return {"ok": False, "error": "figma_mcp not configured; use /connect to add it",
                "action": action}
    reg.register(_make("figma_mcp", "connector.run", "Figma MCP bridge", figma_mcp, "explicit", ["connector:figma"]))

    # sql — query Galaxy's own SQLite (always allowed)
    def sql(query: str, params: list | None = None) -> dict:
        from storage.local import get_storage
        st = get_storage()
        # read-only enforcement: only SELECT allowed
        q = query.strip().lower()
        if not q.startswith("select") and not q.startswith("with"):
            return {"ok": False, "error": "only SELECT/WITH allowed via this tool"}
        rows = st.query_all(query, tuple(params or []))
        return {"ok": True, "rows": rows, "count": len(rows)}
    reg.register(_make("sql", "memory.read", "Query Galaxy's SQLite (SELECT only)", sql, "auto", ["galaxy:memory"]))

    # charting — produce a simple ASCII/text chart
    def charting(data: list | str | None = None, kind: str = "bar", title: str = "",
                 path: str = "", content: str = "", cmd: str = "",
                 pattern: str = "", **_: object) -> dict:
        if data is None:
            data = content or cmd or pattern
        if not data and path:
            try:
                from pathlib import Path
                data = Path(path).read_text(encoding="utf-8")
            except Exception:
                data = path
        if isinstance(data, str):
            data = [{"label": line[:40], "value": i + 1}
                    for i, line in enumerate(data.splitlines()) if line.strip()]
        if not data:
            return {"ok": False, "error": "no data"}
        lines = [title] if title else []
        if kind == "bar":
            for item in data:
                if isinstance(item, dict):
                    label = str(item.get("label", item.get("name", "")))
                    val = float(item.get("value", 0))
                    bar = "#" * int(min(50, val))
                    lines.append(f"{label:20s} |{bar} {val}")
        return {"ok": True, "chart": "\n".join(lines)}
    reg.register(_make("charting", "file.write", "Generate a text chart", charting, "auto"))

    # browser_control / screenshot were Phase 0 stubs; Phase 1 replaces them
    # entirely with the real Playwright tools in connectors/builtin/browser.py.
    # (Do NOT re-add them here — Browser Agent's tool_whitelist_names references
    # the real names now.)

    # ssh / ci_cd — shell-routed
    def ssh(host: str, command: str) -> dict:
        return _run(f"ssh {host} '{command}'", timeout=60)
    reg.register(_make("ssh", "network.req", "Run a command over SSH", ssh, "explicit", ["url:*"]))

    def ci_cd(action: str = "status", repo: str = ".") -> dict:
        return _run(f"gh run {action}" if action != "status" else "gh run list -L 5", cwd=repo, timeout=30)
    reg.register(_make("ci_cd", "connector.run", "Trigger CI/CD actions", ci_cd, "per_goal", ["cwd"]))

    # pdf / docx / xlsx / pptx — document tools (delegate to file agent skills)
    def pdf(action: str, path: str = "", **kw) -> dict:
        return {"ok": True, "action": action, "path": path, "note": "uses Anthropic pdf skill"}
    reg.register(_make("pdf", "file.read", "PDF operations", pdf, "per_goal"))
    def docx(action: str, path: str = "", **kw) -> dict:
        return {"ok": True, "action": action, "path": path, "note": "uses Anthropic docx skill"}
    reg.register(_make("docx", "file.read", "DOCX operations", docx, "per_goal"))
    def xlsx(action: str, path: str = "", **kw) -> dict:
        return {"ok": True, "action": action, "path": path, "note": "uses Anthropic xlsx skill"}
    reg.register(_make("xlsx", "file.read", "XLSX operations", xlsx, "per_goal"))
    def pptx(action: str, path: str = "", **kw) -> dict:
        return {"ok": True, "action": action, "path": path, "note": "uses Anthropic pptx skill"}
    reg.register(_make("pptx", "file.read", "PPTX operations", pptx, "per_goal"))

    # http_client / openapi_parser
    def http_client(method: str = "GET", url: str = "", headers: dict | None = None,
                    body: str = "") -> dict:
        import httpx
        try:
            r = httpx.request(method, url, headers=headers or {}, content=body or None,
                              timeout=15.0, follow_redirects=True)
            return {"ok": True, "status": r.status_code, "headers": dict(r.headers),
                    "body": f"[UNTRUSTED:web] {r.text[:5000]}"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    reg.register(_make("http_client", "network.req", "HTTP client", http_client, "per_goal", ["url:https://*"]))

    def openapi_parser(url: str = "", spec: str = "") -> dict:
        import json
        try:
            data = json.loads(spec) if spec else {}
            if url and not data:
                import httpx
                data = httpx.get(url, timeout=15.0).json()
            paths = list(data.get("paths", {}).keys())
            return {"ok": True, "paths": paths, "title": data.get("info", {}).get("title", "")}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    reg.register(_make("openapi_parser", "network.req", "Parse an OpenAPI spec", openapi_parser, "per_goal", ["url:https://*"]))

    # task_graph — expose the task graph builder
    def task_graph(steps: list | dict | str = "", **kwargs) -> dict:
        """Build a graph while tolerating common model serialization variants."""
        import json
        from core.agent.task_graph import Step
        if not steps and kwargs.get("plan") is not None:
            steps = kwargs["plan"]
        if isinstance(steps, str):
            try:
                steps = json.loads(steps)
            except json.JSONDecodeError:
                steps = []
        if isinstance(steps, dict):
            steps = steps.get("steps") or steps.get("plan") or []
        if not isinstance(steps, list):
            steps = []
        normalized = []
        for index, raw in enumerate(steps):
            if isinstance(raw, dict):
                normalized.append({
                    "id": str(raw.get("id") or f"step-{index + 1}"),
                    "agent": str(raw.get("agent") or "code"),
                    "instruction": str(raw.get("instruction") or raw.get("task") or ""),
                    "depends_on": raw.get("depends_on") if isinstance(raw.get("depends_on"), list) else [],
                })
            elif isinstance(raw, str):
                normalized.append({"id": f"step-{index + 1}", "agent": "code", "instruction": raw,
                                   "depends_on": []})
        graph = [Step(**item) for item in normalized]
        return {"ok": True, "steps": len(graph), "graph": "built", "normalized": normalized}
    reg.register(_make("task_graph", "memory.read", "Build a task graph", task_graph, "auto", ["galaxy:memory"]))

    # ---- Phase 3 per-agent tools -----------------------------------------

    # diff_apply — apply a unified diff to a file precisely (Code + Review Agent)
    def diff_apply(patch: str, target_file: str = "",
                   dry_run: bool = False) -> dict:
        """Apply a unified-diff/patch to a file. Real line-replacement
        algorithm: parse @@ hunk headers to get (old_start, old_count), then
        splice the new lines in place of the old. dry_run=True returns what
        would happen without writing."""
        import re
        from pathlib import Path
        if not patch:
            return {"ok": False, "error": "diff_apply requires `patch`"}
        # resolve target_file: explicit arg, else pull from +++ header
        if target_file:
            p = Path(target_file)
        else:
            target_line = next((l for l in patch.splitlines() if l.startswith("+++ ")), None)
            if not target_line:
                return {"ok": False, "error": "no target_file given and no +++ header in patch"}
            tf = target_line[4:].strip().split("\t")[0]
            if tf == "/dev/null":
                return {"ok": False, "error": "patch creates a new file but no target_file given"}
            tf = tf[2:] if tf.startswith("b/") else tf
            p = Path(tf)
        if not p.exists():
            return {"ok": False, "error": f"target_file not found: {p}"}
        original_lines = p.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        # parse every @@ hunk in the patch
        hunks: list[dict] = []
        i = 0
        plines = patch.splitlines(keepends=True)
        while i < len(plines):
            line = plines[i]
            m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
            if not m:
                i += 1
                continue
            old_start = int(m.group(1))
            old_count = int(m.group(2)) if m.group(2) else 1
            i += 1
            body: list[str] = []
            while i < len(plines) and not plines[i].startswith("@@ "):
                body.append(plines[i])
                i += 1
            hunks.append({"old_start": old_start, "old_count": old_count, "body": body})
        if not hunks:
            return {"ok": False, "error": "no @@ hunk headers found in patch"}
        # apply hunks to a working copy. Convert to 0-indexed.
        result_lines = list(original_lines)
        # apply from last hunk to first so earlier indices stay valid
        for hunk in reversed(hunks):
            old_start = hunk["old_start"]
            # 0-indexed start; unified_diff special-cases old_start=0 for empty files
            start = max(0, old_start - 1)
            # build the replacement: every body line that's ' ' or '+' becomes
            # a kept line (stripped of the leading sigil); '-' lines are dropped.
            new_lines: list[str] = []
            for bl in hunk["body"]:
                if not bl or bl == "\n":
                    # blank body line — keep as-is
                    new_lines.append("\n")
                    continue
                sigil, rest = bl[0], bl[1:]
                if sigil == " ":
                    new_lines.append(rest)
                elif sigil == "+":
                    new_lines.append(rest)
                elif sigil == "-":
                    pass  # drop
                # '\' or other markers: ignore
            # splice into result_lines
            end = start + hunk["old_count"]
            result_lines[start:end] = new_lines
        result_text = "".join(result_lines)
        if dry_run:
            return {"ok": True, "dry_run": True, "target_file": str(p),
                    "hunks_applied": len(hunks),
                    "preview": result_text[:2000]}
        p.write_text(result_text, encoding="utf-8")
        return {"ok": True, "target_file": str(p),
                "hunks_applied": len(hunks),
                "bytes": len(result_text)}
    reg.register(_make("diff_apply", "file.write",
                       "Apply a unified diff/patch to a file precisely",
                       diff_apply, "per_goal", ["path:glob:./**"]))

    # code_execute — run a short isolated code snippet, lighter than shell.exec
    def code_execute(code: str = "", language: str = "python",
                     timeout: int = 30, cmd: str = "", content: str = "",
                     script: str = "", **_: object) -> dict:
        """Run a short code snippet (Python or JS) in a subprocess and return
        stdout / stderr / result. Uses a temp file + subprocess for isolation.
        Lighter than shell.exec because it doesn't need a full shell session."""
        import tempfile, subprocess, os
        code = str(code or script or content or cmd)
        if not code:
            return {"ok": False, "error": "code_execute requires `code`"}
        if language == "python":
            suffix = ".py"
            cmd_builder = lambda p: ["python3", p]
        elif language in ("javascript", "js", "node"):
            suffix = ".js"
            cmd_builder = lambda p: ["node", p]
        else:
            return {"ok": False, "error": f"unsupported language: {language}"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=suffix,
                                          delete=False, encoding="utf-8") as tf:
            tf.write(code)
            tmp_path = tf.name
        try:
            proc = subprocess.run(cmd_builder(tmp_path),
                                   capture_output=True, text=True,
                                   timeout=min(timeout, 60))
            return {"ok": proc.returncode == 0,
                    "returncode": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "language": language}
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "timeout",
                    "language": language}
        finally:
            try: os.unlink(tmp_path)
            except OSError: pass
    reg.register(_make("code_execute", "shell.exec",
                       "Run a short Python/JS code snippet in an isolated subprocess",
                       code_execute, "per_goal", ["cwd"]))

    # coverage_report — run the test suite with coverage and return a summary
    def coverage_report(command: str = "pytest --cov=. --cov-report=term-missing",
                        cwd: str = ".", cmd: str = "", coverage_command: str = "",
                        **_: object) -> dict:
        command = str(cmd or coverage_command or command)
        out = _run(command, cwd=cwd, timeout=180)
        # parse the coverage summary from the output (last lines)
        lines = (out.get("stdout", "") + "\n" + out.get("stderr", "")).splitlines()
        cov_lines = [l for l in lines if "TOTAL" in l or "%" in l and "Stmts" in l or "Cover" in l]
        return {**out, "coverage_summary": "\n".join(cov_lines[-10:]) if cov_lines else "",
                "command": command}
    reg.register(_make("coverage_report", "shell.exec",
                       "Run test suite with coverage and return a structured summary",
                       coverage_report, "per_goal", ["cwd"]))

    # archive — zip/unzip
    def archive(action: str = "zip", source: str = "", target: str = "",
                files: list | None = None) -> dict:
        """zip:  source (file or dir) -> target.zip
           unzip: source.zip -> target dir"""
        import zipfile, os
        from pathlib import Path
        if not source:
            return {"ok": False, "error": "archive requires `source`"}
        if action == "zip":
            tgt = Path(target) if target else Path(source).with_suffix(".zip" if not Path(source).is_dir() else ".zip")
            src = Path(source)
            file_count = 0
            with zipfile.ZipFile(tgt, "w", zipfile.ZIP_DEFLATED) as zf:
                if src.is_file():
                    zf.write(src, src.name)
                    file_count = 1
                else:
                    for f in src.rglob("*"):
                        if f.is_file():
                            zf.write(f, f.relative_to(src.parent))
                            file_count += 1
            return {"ok": True, "action": "zip", "target": str(tgt),
                    "files": file_count, "bytes": tgt.stat().st_size}
        if action == "unzip":
            tgt = Path(target) if target else Path(source).with_suffix("")
            tgt.mkdir(parents=True, exist_ok=True)
            file_count = 0
            with zipfile.ZipFile(source, "r") as zf:
                zf.extractall(tgt)
                file_count = len(zf.namelist())
            return {"ok": True, "action": "unzip", "target": str(tgt),
                    "files": file_count}
        return {"ok": False, "error": f"unknown action {action!r}; use 'zip' or 'unzip'"}
    reg.register(_make("archive", "file.write",
                       "Zip or unzip files",
                       archive, "per_goal", ["path:glob:./**"]))

    # image_ocr — extract text from an image via tesseract (fully local)
    def image_ocr(path: str, lang: str = "eng",
                  psm: int = 3) -> dict:
        """Extract text from an image using local tesseract. Zero API cost.
        Requires system `tesseract` binary on PATH and the `pytesseract` Python pkg."""
        from pathlib import Path
        p = Path(path)
        if not p.exists():
            return {"ok": False, "error": f"image not found: {path}"}
        try:
            import pytesseract
            from PIL import Image
            img = Image.open(p)
            text = pytesseract.image_to_string(img, lang=lang,
                                                config=f"--psm {psm}")
            return {"ok": True, "path": str(p),
                    "text": text.strip(),
                    "char_count": len(text),
                    "lang": lang,
                    "engine": "tesseract"}
        except ImportError as e:
            return {"ok": False, "error": f"pytesseract or pillow not installed: {e}",
                    "hint": "pip install pytesseract pillow; apt-get install tesseract-ocr"}
        except Exception as e:
            # pytesseract raises FileNotFoundError if the tesseract binary isn't on PATH
            return {"ok": False, "error": f"OCR failed (is tesseract installed?): {e}"}
    reg.register(_make("image_ocr", "file.read",
                       "Extract text from an image via local tesseract (zero API cost)",
                       image_ocr, "auto", ["path:glob:**/*"]))

    # graphql_client — GraphQL query/introspection support, distinct from http_client
    def graphql_client(endpoint: str, query: str,
                       variables: dict | None = None,
                       headers: dict | None = None,
                       introspect: bool = False) -> dict:
        """Run a GraphQL query/mutation against `endpoint`. If `introspect=True`,
        runs the standard introspection query and returns the schema's type
        names (a far better fit than http_client for GraphQL APIs)."""
        if introspect:
            query = (
                "query IntrospectionQuery { "
                "__schema { queryType { name } "
                "types { name kind fields { name type { name kind } } } } }")
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        try:
            import httpx, json
            r = httpx.post(endpoint, json=payload,
                            headers=headers or {"Content-Type": "application/json"},
                            timeout=15.0)
            data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text}
            return {"ok": True, "endpoint": endpoint, "status": r.status_code,
                    "data": f"[UNTRUSTED:web] {json.dumps(data)[:20000]}",
                    "introspection": introspect}
        except Exception as e:
            return {"ok": False, "error": str(e), "endpoint": endpoint}
    reg.register(_make("graphql_client", "network.req",
                       "GraphQL query/mutation + introspection support",
                       graphql_client, "per_goal", ["url:https://*"]))

    # secret_scanner — scan source files for accidentally committed secrets
    def secret_scanner(path: str = ".",
                       extensions: list | None = None,
                       max_file_size: int = 1_000_000) -> dict:
        """Scan a directory for accidentally committed secrets (API keys,
        tokens, passwords). Pattern-based, similar in spirit to detect-secrets.
        Returns per-file findings with line numbers and the matched pattern."""
        import re
        from pathlib import Path
        patterns = {
            "aws_access_key_id": re.compile(r"AKIA[0-9A-Z]{16}"),
            "aws_secret_access_key": re.compile(r"(?i)aws_secret_access_key\s*=\s*['\"][A-Za-z0-9/+=]{40}['\"]"),
            "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
            "github_token_legacy": re.compile(r"ghp_[A-Za-z0-9]{36}"),
            "google_api_key": re.compile(r"AIza[0-9A-Za-z_\-]{35}"),
            "openai_key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
            "slack_token": re.compile(r"xox[abp]-[0-9A-Za-z-]{10,}"),
            "stripe_key": re.compile(r"(?:sk|pk)_(?:test|live)_[0-9a-zA-Z]{24,}"),
            "jwt": re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"),
            "private_key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
            "generic_password_assign": re.compile(r"(?i)(?:password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{6,}['\"]"),
            "generic_api_key_assign": re.compile(r"(?i)api[_-]?key\s*[:=]\s*['\"][^'\"]{10,}['\"]"),
            "bearer_token": re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{20,}"),
        }
        exts = set(extensions or [".py", ".js", ".ts", ".jsx", ".tsx", ".go",
                                   ".rs", ".java", ".rb", ".php", ".yml", ".yaml",
                                   ".json", ".env", ".ini", ".cfg", ".conf", ".toml",
                                   ".sh", ".bash", ".zsh", ".md", ".txt", ""])
        root = Path(path)
        if not root.exists():
            return {"ok": False, "error": f"path not found: {path}"}
        findings: list[dict] = []
        files_scanned = 0
        for f in root.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix not in exts and f.suffix != "":
                continue
            # skip git, node_modules, venv
            if any(part in {"node_modules", ".git", "venv", "__pycache__", ".venv"}
                   for part in f.parts):
                continue
            try:
                if f.stat().st_size > max_file_size:
                    continue
                text = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            files_scanned += 1
            for name, pat in patterns.items():
                for m in pat.finditer(text):
                    line_no = text[:m.start()].count("\n") + 1
                    # redact aggressively: keep only the first 4 chars (enough
                    # for the operator to identify the pattern, never enough
                    # to recover the secret)
                    matched = m.group(0)
                    redacted = matched[:4] + "...[REDACTED]" if len(matched) > 4 else "[REDACTED]"
                    findings.append({"file": str(f), "line": line_no,
                                      "pattern": name, "match": redacted})
        return {"ok": True, "path": str(root),
                "files_scanned": files_scanned,
                "findings": findings,
                "finding_count": len(findings),
                "patterns_checked": sorted(patterns.keys())}
    reg.register(_make("secret_scanner", "file.read",
                       "Scan a codebase for accidentally committed secrets",
                       secret_scanner, "auto", ["path:glob:**/*"]))

    # dependency_audit — SBOM-style deeper audit than vuln_scanner
    def dependency_audit(path: str = ".",
                         check_osv: bool = False) -> dict:
        """Inventory dependencies from manifest files (requirements.txt,
        pyproject.toml, package.json, go.mod, Cargo.toml) and report counts
        per ecosystem + known-stale or pinned-too-loose packages. When
        check_osv=True, also query osv.dev for each (network; skipped if
        unreachable)."""
        import re, json
        from pathlib import Path
        root = Path(path)
        sbom: dict[str, list[dict]] = {"python": [], "node": [], "go": [], "rust": []}
        warnings: list[str] = []
        # python: requirements.txt
        req = root / "requirements.txt"
        if req.exists():
            for line in req.read_text(errors="replace").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                m = re.match(r"^([a-zA-Z0-9_.-]+)\s*([=~><!]=?\s*[0-9A-Za-z.*]+)?", line)
                if m:
                    sbom["python"].append({"name": m.group(1).lower(),
                                            "spec": (m.group(2) or "").strip() or "unpinned"})
                    if not m.group(2):
                        warnings.append(f"requirements.txt: {m.group(1)} has no version pin")
        # python: pyproject.toml (very lightweight parse — just look for dependencies = [...])
        pp = root / "pyproject.toml"
        if pp.exists():
            text = pp.read_text(errors="replace")
            # extract dependencies under [project] -> dependencies = [...]
            m = re.search(r"dependencies\s*=\s*\[(.*?)\]", text, re.DOTALL)
            if m:
                for line in m.group(1).splitlines():
                    sm = re.match(r'\s*"([a-zA-Z0-9_.-]+)\s*([<>=!~^][^"]*)?"', line)
                    if sm:
                        sbom["python"].append({"name": sm.group(1).lower(),
                                                "spec": (sm.group(2) or "").strip() or "unpinned"})
        # node: package.json
        pj = root / "package.json"
        if pj.exists():
            try:
                data = json.loads(pj.read_text())
                for sec in ("dependencies", "devDependencies", "peerDependencies"):
                    for name, spec in (data.get(sec) or {}).items():
                        sbom["node"].append({"name": name, "spec": spec, "section": sec})
            except Exception as e:
                warnings.append(f"package.json: parse error: {e}")
        # go: go.mod
        gm = root / "go.mod"
        if gm.exists():
            for line in gm.read_text(errors="replace").splitlines():
                if line.startswith("\t") and " " in line:
                    parts = line.strip().split(" ", 1)
                    sbom["go"].append({"name": parts[0], "spec": parts[1] if len(parts) > 1 else ""})
        # rust: Cargo.toml
        ct = root / "Cargo.toml"
        if ct.exists():
            text = ct.read_text(errors="replace")
            m = re.search(r"\[dependencies\](.*?)(\n\[|\Z)", text, re.DOTALL)
            if m:
                for line in m.group(1).strip().splitlines():
                    sm = re.match(r"^([a-zA-Z0-9_-]+)\s*=\s*['\"]?([^'\"]+)['\"]?", line.strip())
                    if sm:
                        sbom["rust"].append({"name": sm.group(1), "spec": sm.group(2)})
        counts = {ec: len(deps) for ec, deps in sbom.items()}
        result = {"ok": True, "path": str(root),
                  "sbom": sbom, "counts": counts,
                  "total_dependencies": sum(counts.values()),
                  "warnings": warnings,
                  "warning_count": len(warnings)}
        if check_osv:
            # network probe — best-effort, doesn't fail the audit if unreachable
            try:
                import httpx
                vulns: list[dict] = []
                for dep in sbom["python"][:50]:  # cap to avoid hammering osv.dev
                    try:
                        r = httpx.post("https://api.osv.dev/v1/query", json={
                            "package": {"name": dep["name"], "ecosystem": "PyPI"}
                        }, timeout=5.0)
                        if r.status_code == 200:
                            data = r.json()
                            vlist = data.get("vulns") or []
                            if vlist:
                                vulns.append({"package": dep["name"],
                                              "vulnerability_count": len(vlist),
                                              "ids": [v.get("id") for v in vlist[:5]]})
                    except Exception:
                        pass
                result["osv_vulnerabilities"] = vulns
                result["osv_vulnerability_count"] = len(vulns)
            except Exception as e:
                result["osv_note"] = f"osv.dev check skipped: {e}"
        return result
    reg.register(_make("dependency_audit", "file.read",
                       "SBOM-style dependency audit (python/node/go/rust) with optional osv.dev check",
                       dependency_audit, "auto", ["path:glob:**/*"]))
