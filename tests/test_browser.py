"""tests/test_browser.py — Phase 1 real-Playwright browser tests.

CI is the one legitimate headless exception (per Phase 1 spec): we force
GALAXY_BROWSER_HEADLESS=1 here because this sandbox has no display server.
The default everywhere else (including `python3 walkthrough.py` and any
interactive `/goal` invocation) is headed, falling back to headless only
when no display is detected — see connectors/builtin/browser.py.

These tests launch a real Chromium and exercise real page state: a real
navigation, a real click that mutates the DOM, a real form fill, a real
extraction, a real screenshot file. No mocks of Playwright.
"""
import os
import sys
import pytest

# Force headless BEFORE the registry is constructed (env var read on first call).
os.environ["GALAXY_BROWSER_HEADLESS"] = "1"

# A local HTML fixture is the most reproducible way to test browser tools
# without depending on the live network. We write it to a temp file and
# navigate via file://.
_FIXTURE_HTML = """<!doctype html>
<html><head><title>Galaxy Test Page</title></head>
<body>
  <h1 id="h1">Hello Galaxy</h1>
  <button id="btn" onclick="document.getElementById('out').textContent='CLICKED'">Click me</button>
  <div id="out">not clicked</div>
  <form id="f">
    <input id="name" type="text" placeholder="name">
    <input id="email" type="email" placeholder="email">
  </form>
  <table id="t">
    <tr><th>k</th><th>v</th></tr>
    <tr><td>a</td><td>1</td></tr>
    <tr><td>b</td><td>2</td></tr>
  </table>
  <ul id="l"><li>alpha</li><li>beta</li><li>gamma</li></ul>
</body></html>"""


@pytest.fixture
def local_html_path(tmp_path):
    p = tmp_path / "fixture.html"
    p.write_text(_FIXTURE_HTML, encoding="utf-8")
    return f"file://{p}"


@pytest.fixture(autouse=True)
async def _reset_browser_between_tests():
    """Each pytest-asyncio test gets a fresh event loop, but the browser module
    holds a process-global Playwright instance bound to whatever loop created
    it. Reset between tests so every test starts a fresh browser on its own
    loop — otherwise the second test hangs waiting on a dead browser."""
    from connectors.builtin.browser import reset_browser_for_tests
    try:
        await reset_browser_for_tests()
    except Exception:
        pass
    yield
    try:
        await reset_browser_for_tests()
    except Exception:
        pass


@pytest.mark.asyncio
async def test_browser_navigate_loads_real_page(fresh_home, local_html_path):
    """Real navigation: title and URL come back from a real Chromium."""
    from connectors.builtin import get_registry
    reg = get_registry()
    r = await reg.call("browser_navigate", agent="browser", goal_id="g1",
                       args={"url": local_html_path})
    assert r["ok"] is True
    assert r["result"]["title"] == "Galaxy Test Page"
    assert r["result"]["url"].startswith("file://")
    assert r["result"]["status"] == 200


@pytest.mark.asyncio
async def test_browser_click_mutates_real_dom(fresh_home, local_html_path):
    """Real click: the click handler fires and #out's text changes from
    'not clicked' to 'CLICKED'. This is the real resulting state, not a mock."""
    from connectors.builtin import get_registry
    reg = get_registry()
    await reg.call("browser_navigate", agent="browser", goal_id="g1",
                   args={"url": local_html_path})
    r = await reg.call("browser_click", agent="browser", goal_id="g1",
                       args={"selector": "#btn"})
    assert r["ok"] is True
    # verify the resulting DOM state by reading the changed element via JS
    r2 = await reg.call("browser_console", agent="browser", goal_id="g1",
                        args={"action": "eval",
                              "js": "() => document.getElementById('out').textContent"})
    assert "CLICKED" in r2["result"]["value"]


@pytest.mark.asyncio
async def test_browser_fill_writes_real_input_values(fresh_home, local_html_path):
    """Real fill: the form fields now contain the values we typed."""
    from connectors.builtin import get_registry
    reg = get_registry()
    await reg.call("browser_navigate", agent="browser", goal_id="g1",
                   args={"url": local_html_path})
    r = await reg.call("browser_fill", agent="browser", goal_id="g1",
                       args={"fields": {"#name": "Ada", "#email": "ada@example.com"}})
    assert r["ok"] is True
    assert "#name" in r["result"]["filled"]
    r2 = await reg.call("browser_console", agent="browser", goal_id="g1",
                        args={"action": "eval",
                              "js": "() => ({name: document.getElementById('name').value, "
                                   "  email: document.getElementById('email').value})"})
    assert 'Ada' in r2["result"]["value"]
    assert 'ada@example.com' in r2["result"]["value"]


@pytest.mark.asyncio
async def test_browser_extract_pulls_real_table_and_list(fresh_home, local_html_path):
    """Real extract: the table comes back as a 2D array, the list as a list of
    strings — both match the fixture exactly."""
    from connectors.builtin import get_registry
    import json as _json
    reg = get_registry()
    await reg.call("browser_navigate", agent="browser", goal_id="g1",
                   args={"url": local_html_path})
    r = await reg.call("browser_extract", agent="browser", goal_id="g1", args={})
    assert r["ok"] is True
    # data is tagged [UNTRUSTED:web] + JSON
    raw = r["result"]["data"].replace("[UNTRUSTED:web] ", "", 1)
    data = _json.loads(raw)
    assert data["tables"][0][0] == ["k", "v"]
    assert data["tables"][0][1] == ["a", "1"]
    assert data["tables"][0][2] == ["b", "2"]
    assert data["lists"][0] == ["alpha", "beta", "gamma"]


@pytest.mark.asyncio
async def test_browser_screenshot_writes_real_png_file(fresh_home, local_html_path, tmp_path):
    """Real screenshot: a non-empty PNG file lands on disk."""
    from connectors.builtin import get_registry
    reg = get_registry()
    await reg.call("browser_navigate", agent="browser", goal_id="g1",
                   args={"url": local_html_path})
    out = tmp_path / "shot.png"
    r = await reg.call("browser_screenshot", agent="browser", goal_id="g1",
                       args={"path": str(out), "full_page": True})
    assert r["ok"] is True
    assert out.exists()
    # real PNG signature: 89 50 4E 47
    with open(out, "rb") as fh:
        sig = fh.read(4)
    assert sig == b"\x89PNG"
    assert out.stat().st_size > 1000  # not a stub


@pytest.mark.asyncio
async def test_browser_tabs_open_switch_close(fresh_home, local_html_path):
    """Real tab lifecycle: open a second tab, switch to it, then close it.
    The 'list' action reflects real state at every step."""
    from connectors.builtin import get_registry
    reg = get_registry()
    # default tab exists after navigation
    await reg.call("browser_navigate", agent="browser", goal_id="g1",
                   args={"url": local_html_path, "tab": "default"})
    # open a second tab
    r = await reg.call("browser_tabs", agent="browser", goal_id="g1",
                       args={"action": "open", "tab": "extra", "url": local_html_path})
    assert r["ok"] is True
    assert r["result"]["tab"] == "extra"
    # list shows both
    r = await reg.call("browser_tabs", agent="browser", goal_id="g1",
                       args={"action": "list"})
    assert "default" in r["result"]["tabs"]
    assert "extra" in r["result"]["tabs"]
    # close extra
    r = await reg.call("browser_tabs", agent="browser", goal_id="g1",
                       args={"action": "close", "tab": "extra"})
    assert r["ok"] is True
    r = await reg.call("browser_tabs", agent="browser", goal_id="g1",
                       args={"action": "list"})
    assert "extra" not in r["result"]["tabs"]


@pytest.mark.asyncio
async def test_browser_snapshot_returns_untrusted_tag(fresh_home, local_html_path):
    """Real snapshot: the accessibility tree is tagged [UNTRUSTED:web] so an
    agent can never treat it as an instruction."""
    from connectors.builtin import get_registry
    reg = get_registry()
    await reg.call("browser_navigate", agent="browser", goal_id="g1",
                   args={"url": local_html_path})
    r = await reg.call("browser_snapshot", agent="browser", goal_id="g1", args={})
    assert r["ok"] is True
    assert r["result"]["snapshot"].startswith("[UNTRUSTED:web]")
    # the page heading appears in the a11y tree somewhere
    assert "Hello Galaxy" in r["result"]["snapshot"] or "Galaxy Test Page" in r["result"]["snapshot"]


@pytest.mark.asyncio
async def test_browser_navigate_blocked_for_non_browser_agent(fresh_home, local_html_path):
    """Phase 1 + Phase 0.1: only Browser/Research/Design agents can call
    browser_navigate. Code Agent must NOT be able to (whitelist enforcement)."""
    from connectors.builtin import get_registry
    reg = get_registry()
    r = await reg.call("browser_navigate", agent="code", goal_id="g1",
                       args={"url": local_html_path})
    assert r["ok"] is False
    assert r["blocked_by"] == "whitelist"


@pytest.fixture
def upload_html_path(tmp_path):
    """Local HTML page with a real <input type=file> for browser_upload tests."""
    html = """<!doctype html>
<html><head><title>Upload Test</title></head>
<body>
  <input id="file-input" type="file">
  <div id="result">no file</div>
  <script>
    document.getElementById('file-input').addEventListener('change', function() {
      document.getElementById('result').textContent = this.files[0].name;
    });
  </script>
</body></html>"""
    p = tmp_path / "upload.html"
    p.write_text(html, encoding="utf-8")
    return f"file://{p}"


@pytest.mark.asyncio
async def test_browser_upload_sets_file_input(fresh_home, upload_html_path, tmp_path):
    """Real upload: browser_upload() sets a local file into an <input type=file>
    and the change handler fires — the result div shows the filename."""
    from connectors.builtin import get_registry
    reg = get_registry()
    target = tmp_path / "payload.txt"
    target.write_text("galaxy upload test payload", encoding="utf-8")
    await reg.call("browser_navigate", agent="browser", goal_id="g1",
                   args={"url": upload_html_path})
    r = await reg.call("browser_upload", agent="browser", goal_id="g1",
                       args={"selector": "#file-input", "file_path": str(target)})
    assert r["ok"] is True, f"gate blocked: {r}"
    assert r["result"]["ok"] is True, f"handler failed: {r['result']}"
    r2 = await reg.call("browser_console", agent="browser", goal_id="g1",
                        args={"action": "eval",
                              "js": "() => document.getElementById('result').textContent"})
    assert "payload.txt" in r2["result"]["value"]


@pytest.mark.asyncio
async def test_browser_upload_missing_file_returns_error(fresh_home):
    """browser_upload with a non-existent file must return ok=False from the
    handler before touching the browser at all — the file check is the first
    thing the handler does, so no Chromium is needed for this test."""
    from connectors.builtin import get_registry
    reg = get_registry()
    r = await reg.call("browser_upload", agent="browser", goal_id="g1",
                       args={"selector": "#file-input",
                             "file_path": "/tmp/does_not_exist_galaxy.xyz"})
    # gate passes (auto_grant=True in fresh_home); handler catches file-not-found
    assert r["ok"] is True          # gate-level: call was dispatched
    assert r["result"]["ok"] is False          # handler-level: file not found
    assert "not found" in r["result"]["error"]


@pytest.mark.asyncio
async def test_browser_connect_requires_explicit_consent(fresh_home):
    """browser_connect is declared consent=explicit. Without a grant the gate
    must block it — verifying capability.py's per-tool consent fix applies."""
    from security.capability import get_gate
    from connectors.builtin import get_registry
    get_gate().set_auto_grant(False)
    reg = get_registry()
    r = await reg.call("browser_connect", agent="browser", goal_id="g-cdp",
                       args={"host": "127.0.0.1", "port": 9222})
    assert r["ok"] is False
    assert r.get("needs_consent") is True


@pytest.mark.asyncio
async def test_browser_connect_does_not_launch_own_browser_on_failure(fresh_home):
    """Old browser_connect called _ensure_browser() before the CDP connect,
    launching Galaxy's own Chromium even when the CDP target didn't exist.
    Fixed: uses _ensure_playwright() instead. After a failed connect,
    _browser must remain None — no wasteful Galaxy-browser side-effect."""
    from connectors.builtin import get_registry
    import connectors.builtin.browser as bmod
    reg = get_registry()
    # auto_grant=True (fresh_home default) so gate passes; handler fails at TCP
    r = await reg.call("browser_connect", agent="browser", goal_id="g-cdp",
                       args={"host": "127.0.0.1", "port": 9999})
    assert r["ok"] is True          # gate passed
    assert r["result"]["ok"] is False           # CDP connect failed (no Chrome on 9999)
    assert bmod._browser is None, (
        "browser_connect launched Galaxy's own Chromium as a side-effect — "
        "_ensure_browser() bug was not removed."
    )


@pytest.mark.asyncio
async def test_browser_connect_cleans_up_cdp_browser_on_failure(fresh_home):
    """Old browser_connect stored the CDP handle in a local var `b` that was
    GC'd immediately, dropping the connection. Fixed: stored in _cdp_browser.
    On failure, _cdp_browser must be cleaned up to None (not a dangling object)."""
    from connectors.builtin import get_registry
    import connectors.builtin.browser as bmod
    reg = get_registry()
    r = await reg.call("browser_connect", agent="browser", goal_id="g-cdp2",
                       args={"host": "127.0.0.1", "port": 9998})
    assert r["ok"] is True          # gate passed
    assert r["result"]["ok"] is False           # CDP connect failed
    assert bmod._cdp_browser is None, (
        "Failed CDP connect left a dangling _cdp_browser — "
        "cleanup on failure is broken."
    )
