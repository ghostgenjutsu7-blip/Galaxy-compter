"""Capability-gated project-scoped file tools."""
from __future__ import annotations

from pathlib import Path

from config import get_config
from connectors.builtin import ToolRegistry
from core.agent.base_agent import Tool

MAX_READ = 50_000


def _project_root() -> Path:
    configured = get_config().get("project_root", "")
    return Path(configured).expanduser().resolve() if configured else Path.cwd().resolve()


def _resolved(path: str) -> Path:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = _project_root() / candidate
    return candidate.resolve()


def _within_scope(path: str) -> bool:
    p = _resolved(path)
    root = _project_root()
    try:
        p.relative_to(root)
        return True
    except ValueError:
        pass
    for entry in get_config().get("file_allowlist", []):
        try:
            p.relative_to(Path(entry).expanduser().resolve())
            return True
        except (ValueError, TypeError):
            continue
    return False


def file_read(path: str, offset: int = 0, limit: int = MAX_READ) -> dict:
    if limit < 0 or limit > MAX_READ or offset < 0:
        return {"ok": False, "error": "invalid offset/limit"}
    if not _within_scope(path):
        return {"ok": False, "error": f"path outside scope: {path}"}
    p = _resolved(path)
    if not p.exists() or not p.is_file():
        return {"ok": False, "error": "not found"}
    size = p.stat().st_size
    with p.open("r", encoding="utf-8", errors="replace") as fh:
        fh.seek(offset)
        text = fh.read(limit)
    return {"ok": True, "path": str(p), "offset": offset, "limit": limit,
            "size": size, "truncated": (offset + len(text)) < size,
            "content": text}


def file_write(path: str, content: str, append: bool = False) -> dict:
    if not _within_scope(path):
        return {"ok": False, "error": f"path outside scope: {path}"}
    p = _resolved(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with p.open(mode, encoding="utf-8") as fh:
        fh.write(content)
    return {"ok": True, "path": str(p), "bytes": len(content)}


def file_delete(path: str) -> dict:
    if not _within_scope(path):
        return {"ok": False, "error": f"path outside scope: {path}"}
    p = _resolved(path)
    if not p.exists() or not p.is_file():
        return {"ok": False, "error": "not found"}
    p.unlink()
    return {"ok": True, "path": str(p)}


def file_list(path: str = ".", pattern: str = "*") -> dict:
    if not _within_scope(path):
        return {"ok": False, "error": f"path outside scope: {path}"}
    p = _resolved(path)
    if not p.exists() or not p.is_dir():
        return {"ok": False, "error": "not found"}
    entries = []
    for child in sorted(p.glob(pattern)):
        entries.append({"path": str(child), "is_dir": child.is_dir(),
                        "size": child.stat().st_size if child.is_file() else 0})
    return {"ok": True, "entries": entries}


def register(reg: ToolRegistry) -> None:
    reg.register(Tool(name="file.read", capability="file.read",
                      description="Read a file (paginated, max 50K per call)",
                      handler=file_read, consent="auto", resources=["path:glob:**/*"]))
    reg.register(Tool(name="file.write", capability="file.write",
                      description="Write or append to a file within the project",
                      handler=file_write, consent="per_goal", resources=["path:glob:./**"]))
    reg.register(Tool(name="file.delete", capability="file.write",
                      description="Delete a file within the project",
                      handler=file_delete, consent="explicit", resources=["path:glob:./**"]))
    reg.register(Tool(name="file.list", capability="file.read",
                      description="List files in a directory",
                      handler=file_list, consent="auto", resources=["path:glob:**/*"]))
