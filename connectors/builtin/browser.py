"""connectors/builtin/browser.py — 10 Playwright-backed browser tools.

§6 + Phase 1 expansion. Default mode is HEADED (visible): the operator wants to
see the browser work so there's no room for an unnoticed mistake. Falls back to
headless ONLY when no display is available, with a logged warning — never
silent. Override via the GALAXY_BROWSER_HEADLESS env var:
    GALAXY_BROWSER_HEADLESS=1  force headless
    GALAXY_BROWSER_HEADLESS=0  force headed (will fail without a display)

The Capability Gate calls every handler — sync OR async. Browser handlers are
async (Playwright's natural API); the gate's `enforce()` awaits coroutine
handlers. Each handler tags any retrieved page text with [UNTRUSTED:web] so it
can never be followed as an instruction (§10).

A single shared browser instance lives for the lifetime of the process; tabs
are managed by browser_tabs / browser_navigate(tab=...).
"""
from __future__ import annotations

import asyncio
import base64
import logging
import os
import time
from typing import Any

from core.agent.base_agent import Tool
from connectors.builtin import ToolRegistry

_log = logging.getLogger("galaxy.browser")

# Module-level state. Lazily initialised on first browser_* call so importing
# this module is free; the cost is paid only when a browser tool actually runs.
# IMPORTANT: _loop_at_create records the event loop the browser was started on.
# pytest-asyncio (function scope) gives every test a fresh loop — if we don't
# detect that and restart, all calls after the first test will hang waiting on
# a browser bound to a dead loop.
_state_lock = asyncio.Lock()
_pw: Any = None            # Playwright instance
_browser: Any = None       # Galaxy's own Chromium (launched by _ensure_browser)
_cdp_browser: Any = None   # User's real browser, attached via CDP (browser_connect)
_pages: dict[str, Any] = {}  # tab_id -> Page
_active_tab: str = "default"
_loop_at_create: Any = None


async def reset_browser_for_tests() -> None:
    """Force-close the shared browser. Tests call this between cases so the
    next call starts a fresh browser on the test's own event loop."""
    global _pw, _browser, _cdp_browser, _active_tab, _loop_at_create
    async with _state_lock:
        try:
            if _cdp_browser is not None:
                await _cdp_browser.disconnect()
        except Exception:
            pass
        try:
            if _browser is not None:
                await _browser.close()
        except Exception:
            pass
        try:
            if _pw is not None:
                await _pw.stop()
        except Exception:
            pass
        _cdp_browser = None
        _browser = None
        _pw = None
        _pages.clear()
        _active_tab = "default"
        _loop_at_create = None


def _want_headless() -> bool:
    """Decide headed vs headless. Headed is the default everywhere. Headless
    only when (a) explicitly forced via GALAXY_BROWSER_HEADLESS=1, or (b) no
    display is detected and the user hasn't forced headed."""
    env = os.environ.get("GALAXY_BROWSER_HEADLESS", "").strip().lower()
    if env == "1":
        return True
    if env == "0":
        return False
    if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        _log.warning(
            "browser: no DISPLAY/WAYLAND_DISPLAY available — falling back to "
            "headless. Set GALAXY_BROWSER_HEADLESS=0 to force headed (will "
            "fail without a display server).")
        return True
    return False


async def _ensure_playwright() -> Any:
    """Start the Playwright process without launching any browser.
    Used by browser_connect which only needs _pw.chromium to issue a CDP
    connect — it must NOT trigger a full Chromium launch via _ensure_browser()
    because that wastes resources and pollutes module state that belongs to
    Galaxy's own Chromium session."""
    global _pw
    if _pw is not None:
        return _pw
    async with _state_lock:
        if _pw is not None:
            return _pw
        from playwright.async_api import async_playwright
        _pw = await async_playwright().start()
    return _pw


async def _ensure_browser() -> Any:
    """Lazily start Playwright + Chromium. Idempotent under the state lock.
    Detects a stale event loop (pytest-asyncio function scope gives every test
    a fresh loop) and restarts cleanly instead of hanging on a dead browser."""
    global _pw, _browser, _loop_at_create
    current_loop = asyncio.get_running_loop()
    if (_browser is not None and _loop_at_create is current_loop
            and _browser.is_connected()):
        return _browser
    # Either first start, or the event loop changed under us — clean up the
    # stale browser if any, then start fresh. (Cleanup is best-effort: a
    # browser bound to a dead loop will fail its close() call.)
    if _browser is not None or _pw is not None:
        try:
            await reset_browser_for_tests()
        except Exception:
            _browser = None
            _pw = None
            _pages.clear()
            _loop_at_create = None
    async with _state_lock:
        if _browser is not None and _loop_at_create is current_loop:
            return _browser
        from playwright.async_api import async_playwright
        _pw = await async_playwright().start()
        _browser = await _pw.chromium.launch(headless=_want_headless())
        _loop_at_create = current_loop
        if "default" not in _pages:
            _pages["default"] = await _browser.new_page()
    return _browser


async def _page(tab: str | None = None) -> Any:
    """Return the page for `tab`, creating it if needed."""
    await _ensure_browser()
    t = tab or _active_tab
    if t not in _pages:
        _pages[t] = await _browser.new_page()
    return _pages[t]


# ---- the 10 tool handlers -------------------------------------------------

async def browser_navigate(url: str, wait_until: str = "load",
                           tab: str = "default", timeout_ms: int = 30000) -> dict:
    """Open a URL in a new or existing tab. Waits for load. Returns final URL +
    title. Default consent: auto (navigating is low-risk)."""
    p = await _page(tab)
    resp = await p.goto(url, wait_until=wait_until, timeout=timeout_ms)
    return {"ok": True, "url": p.url, "title": await p.title(),
            "status": resp.status if resp else None, "tab": tab}


async def browser_click(selector: str | None = None,
                        description: str | None = None,
                        tab: str | None = None,
                        timeout_ms: int = 10000) -> dict:
    """Click an element by CSS selector, or by a textual description resolved
    against the current accessibility snapshot (text=... match). Exactly one of
    selector / description must be provided."""
    if not selector and not description:
        return {"ok": False, "error": "browser_click requires selector or description"}
    p = await _page(tab)
    if selector:
        await p.click(selector, timeout=timeout_ms)
        return {"ok": True, "clicked": "selector", "selector": selector}
    # description: try text=, role-based, and aria-label selectors in order
    candidates = [
        f"text={description}",
        f"button:has-text({description!r})",
        f"a:has-text({description!r})",
        f"[aria-label={description!r}]",
    ]
    last_err = None
    for sel in candidates:
        try:
            await p.click(sel, timeout=timeout_ms)
            return {"ok": True, "clicked": "description", "selector": sel,
                    "description": description}
        except Exception as e:
            last_err = str(e)
    return {"ok": False, "error": f"could not resolve description "
                                  f"{description!r}: {last_err}"}


async def browser_fill(fields: dict, tab: str | None = None,
                       timeout_ms: int = 10000) -> dict:
    """Fill one or more form fields. `fields` maps CSS selector -> value."""
    if not isinstance(fields, dict) or not fields:
        return {"ok": False, "error": "browser_fill requires fields={selector: value}"}
    p = await _page(tab)
    filled = []
    for sel, val in fields.items():
        await p.fill(sel, str(val), timeout=timeout_ms)
        filled.append(sel)
    return {"ok": True, "filled": filled, "tab": tab or _active_tab}


async def browser_snapshot(tab: str | None = None,
                           max_chars: int = 20000) -> dict:
    """Return the page's accessibility tree — the default lightweight way an
    agent 'reads' a page. Tagged [UNTRUSTED:web]. Uses Playwright's ARIA
    snapshot when available, falling back to body.innerText so it works across
    Playwright versions (page.accessibility was removed in 1.46+)."""
    p = await _page(tab)
    text = ""
    method = None
    # Try the modern ARIA snapshot first
    try:
        text = await p.locator("body").aria_snapshot()
        method = "aria_snapshot"
    except Exception:
        pass
    # Fall back to the old page.accessibility API if present
    if not text:
        acc = getattr(p, "accessibility", None)
        if acc is not None:
            try:
                snap = await acc.snapshot()
                import json as _json
                text = _json.dumps(snap, ensure_ascii=False) if snap else ""
                method = "accessibility"
            except Exception:
                pass
    # Last resort: visible text — still a faithful representation of what's on the page
    if not text:
        try:
            text = await p.evaluate("() => document.body.innerText")
            method = "body_innerText"
        except Exception as e:
            return {"ok": False, "error": f"snapshot failed: {e}"}
    return {"ok": True, "url": p.url,
            "snapshot": f"[UNTRUSTED:web] {text[:max_chars]}",
            "truncated": len(text) > max_chars,
            "method": method,
            "tab": tab or _active_tab}


async def browser_screenshot(path: str | None = None,
                             full_page: bool = True,
                             tab: str | None = None) -> dict:
    """Capture a PNG screenshot. If `path` is given, saves there; otherwise
    returns the image as base64. Hook for vision models: when a vision-capable
    provider is configured, the orchestrator can pass the returned base64 to
    the model for description (see Design Agent's vision_analyze tool)."""
    p = await _page(tab)
    if path:
        await p.screenshot(path=path, full_page=full_page)
        try:
            size = os.path.getsize(path)
        except OSError:
            size = 0
        return {"ok": True, "path": path, "full_page": full_page,
                "bytes": size, "tab": tab or _active_tab}
    png = await p.screenshot(full_page=full_page)
    b64 = base64.b64encode(png).decode("ascii")
    return {"ok": True, "image_base64": b64,
            "image_mime": "image/png", "full_page": full_page,
            "bytes": len(png), "tab": tab or _active_tab}


async def browser_extract(selectors: dict | None = None,
                          tab: str | None = None,
                          max_chars: int = 20000, url: str = "",
                          **_: Any) -> dict:
    """Pull structured data out of the current page. With no args, extracts
    every <table> as a list of row-dicts and every <ul>/<ol> as a list of text
    items. With `selectors={key: css_selector}`, returns {key: extracted_text}
    for each. Tagged [UNTRUSTED:web]."""
    if url:
        await browser_navigate(url=url, tab=tab or "default")
    p = await _page(tab)
    if selectors:
        out: dict[str, Any] = {}
        for key, sel in selectors.items():
            try:
                els = await p.query_selector_all(sel)
                vals = []
                for el in els:
                    t = await el.text_content()
                    vals.append(t.strip() if t else "")
                out[key] = vals
            except Exception as e:
                out[key] = {"error": str(e)}
        return {"ok": True, "url": p.url,
                "data": f"[UNTRUSTED:web] " + str(out)[:max_chars],
                "tab": tab or _active_tab}
    # default: extract tables + lists via DOM
    tables = await p.evaluate(
        """() => Array.from(document.querySelectorAll('table')).map(t =>
            Array.from(t.rows).map(r => Array.from(r.cells).map(c => c.innerText.trim())))""")
    lists = await p.evaluate(
        """() => Array.from(document.querySelectorAll('ul,ol')).map(l =>
            Array.from(l.children).map(li => li.innerText.trim()))""")
    data = {"tables": tables, "lists": lists}
    import json as _json
    text = _json.dumps(data, ensure_ascii=False)
    return {"ok": True, "url": p.url,
            "data": f"[UNTRUSTED:web] {text[:max_chars]}",
            "truncated": len(text) > max_chars,
            "tab": tab or _active_tab}


async def browser_console(action: str = "read",
                          js: str | None = None,
                          tab: str | None = None,
                          timeout_ms: int = 10000) -> dict:
    """Read browser console logs (action='read') OR evaluate arbitrary JS
    (action='eval', requires `js`). Tagged [UNTRUSTED:web]."""
    p = await _page(tab)
    if action == "read":
        # collect messages seen since the page was opened
        msgs: list[dict] = []
        try:
            msgs = await p.evaluate(
                "() => (window.__galaxy_console = window.__galaxy_console || []).slice()")
        except Exception:
            pass
        return {"ok": True, "messages": msgs, "tab": tab or _active_tab}
    if action == "eval":
        if not js:
            return {"ok": False, "error": "browser_console eval requires `js`"}
        try:
            val = await p.evaluate(js)
            import json as _json
            text = _json.dumps(val, ensure_ascii=False, default=str) \
                if not isinstance(val, str) else val
            return {"ok": True,
                    "value": f"[UNTRUSTED:web] {text[:20000]}",
                    "tab": tab or _active_tab}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    return {"ok": False, "error": f"unknown action {action!r}; use 'read' or 'eval'"}


async def browser_tabs(action: str = "list",
                       tab: str | None = None,
                       url: str | None = None) -> dict:
    """Open / switch / close / list tabs.
    - action='open'  : open a new tab; if `url` given, navigate to it. Returns new tab id.
    - action='switch': make `tab` the active tab.
    - action='close' : close `tab`. If closing the active tab, switches to 'default'.
    - action='list'  : return all open tabs with their current URLs.
    """
    global _active_tab
    await _ensure_browser()
    if action == "list":
        out = {}
        for tid, pg in _pages.items():
            try:
                out[tid] = {"url": pg.url, "active": tid == _active_tab}
            except Exception:
                out[tid] = {"url": None, "active": tid == _active_tab}
        return {"ok": True, "tabs": out, "active": _active_tab}
    if action == "open":
        # generate a unique tab id
        new_id = tab or f"tab{len(_pages) + 1}"
        _pages[new_id] = await _browser.new_page()
        _active_tab = new_id
        if url:
            await _pages[new_id].goto(url)
        return {"ok": True, "tab": new_id, "url": url or "about:blank"}
    if action == "switch":
        if tab not in _pages:
            return {"ok": False, "error": f"unknown tab {tab!r}"}
        _active_tab = tab
        return {"ok": True, "active": _active_tab}
    if action == "close":
        if not tab:
            return {"ok": False, "error": "browser_tabs close requires `tab`"}
        if tab not in _pages:
            return {"ok": False, "error": f"unknown tab {tab!r}"}
        try:
            await _pages[tab].close()
        except Exception:
            pass
        del _pages[tab]
        if _active_tab == tab:
            _active_tab = "default" if "default" in _pages else next(iter(_pages), "default")
        return {"ok": True, "closed": tab, "active": _active_tab}
    return {"ok": False, "error": f"unknown action {action!r}"}


async def browser_upload(selector: str, file_path: str,
                         tab: str | None = None,
                         timeout_ms: int = 30000) -> dict:
    """Upload a local file into a page's <input type=file>. Touches the user's
    filesystem, so the gate's consent policy for connector.run applies."""
    if not os.path.exists(file_path):
        return {"ok": False, "error": f"file not found: {file_path}"}
    p = await _page(tab)
    try:
        async with p.expect_file_chooser(timeout=timeout_ms) as fc_info:
            await p.click(selector, timeout=timeout_ms)
        fc = await fc_info.value
        await fc.set_files(file_path)
        return {"ok": True, "selector": selector, "file": file_path,
                "tab": tab or _active_tab}
    except Exception as e:
        return {"ok": False, "error": str(e)}


async def browser_connect(cdp_url: str = "",
                          host: str = "127.0.0.1",
                          port: int = 9222) -> dict:
    """Attach via CDP to the user's OWN running Chrome/Brave instance, reusing
    their real sessions and cookies. Gated behind explicit consent: this
    touches the user's real logged-in browser. Requires the user to launch
    Chrome with --remote-debugging-port=PORT.

    The connection is stored in module state (_cdp_browser) so it persists
    for the lifetime of the process — subsequent browser_navigate / click /
    snapshot calls can then be routed through it. Calling browser_connect
    again disconnects the previous session first.
    """
    global _cdp_browser
    if not cdp_url:
        cdp_url = f"http://{host}:{port}"
    # Only need the Playwright process, not a full Chromium launch.
    # _ensure_browser() would wastefully open Galaxy's own browser and
    # pollute module state that belongs to the Galaxy-owned session.
    pw = await _ensure_playwright()
    # Disconnect any existing CDP session before opening a new one.
    if _cdp_browser is not None:
        try:
            await _cdp_browser.disconnect()
        except Exception:
            pass
        _cdp_browser = None
    try:
        b = await pw.chromium.connect_over_cdp(cdp_url)
        _cdp_browser = b  # persist in module state — NOT a local var
        ctxs = b.contexts
        pages = []
        for c in ctxs:
            for pg in c.pages:
                pages.append({"url": pg.url, "title": "..."})
        return {"ok": True, "cdp_url": cdp_url,
                "contexts": len(ctxs), "pages": pages[:10],
                "note": "connected to user's running browser"}
    except Exception as e:
        _cdp_browser = None
        return {"ok": False, "error": f"CDP connect to {cdp_url} failed: {e}"}


# ---- registration ---------------------------------------------------------

def register(reg: ToolRegistry) -> None:
    """Register all 10 browser tools. Consents follow the existing convention:
    navigating/snapshot/extract/console-read are low-risk (auto); upload + CDP
    touch the user's filesystem/real sessions (per_goal / explicit)."""
    reg.register(Tool(
        name="browser_navigate", capability="network.req",
        description="Open a URL in a tab and wait for load",
        handler=browser_navigate, consent="auto",
        resources=["url:https://*", "url:http://*", "url:file://*"],
    ))
    reg.register(Tool(
        name="browser_click", capability="network.req",
        description="Click an element by selector or text description",
        handler=browser_click, consent="auto",
        resources=["url:https://*"],
    ))
    reg.register(Tool(
        name="browser_fill", capability="network.req",
        description="Fill one or more form fields",
        handler=browser_fill, consent="auto",
        resources=["url:https://*"],
    ))
    reg.register(Tool(
        name="browser_snapshot", capability="network.req",
        description="Return the page accessibility tree (tagged [UNTRUSTED:web])",
        handler=browser_snapshot, consent="auto",
        resources=["url:https://*"],
    ))
    reg.register(Tool(
        name="browser_screenshot", capability="network.req",
        description="Capture a PNG screenshot (path or base64)",
        handler=browser_screenshot, consent="auto",
        resources=["url:https://*"],
    ))
    reg.register(Tool(
        name="browser_extract", capability="network.req",
        description="Pull tables/lists/structured data from a page as JSON",
        handler=browser_extract, consent="auto",
        resources=["url:https://*"],
    ))
    reg.register(Tool(
        name="browser_console", capability="network.req",
        description="Read browser console logs OR evaluate JS (tagged [UNTRUSTED:web])",
        handler=browser_console, consent="auto",
        resources=["url:https://*"],
    ))
    reg.register(Tool(
        name="browser_tabs", capability="network.req",
        description="Open / switch / close / list browser tabs",
        handler=browser_tabs, consent="auto",
        resources=["url:https://*"],
    ))
    reg.register(Tool(
        name="browser_upload", capability="connector.run",
        description="Upload a local file into a page's file input",
        handler=browser_upload, consent="per_goal",
        resources=["path:glob:**/*", "url:https://*"],
    ))
    reg.register(Tool(
        name="browser_connect", capability="connector.run",
        description="Attach via CDP to the user's running Chrome/Brave instance",
        handler=browser_connect, consent="explicit",
        resources=["url:http://127.0.0.1:*"],
    ))
