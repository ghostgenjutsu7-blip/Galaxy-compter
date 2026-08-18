"""context/codebase_map.py — codebase map (§13).

On first encountering a project, Code Agent builds a lightweight map: file tree,
per-file size/language/modified-time, a symbol index (functions, classes,
exports), an import dependency graph, and test-file markers. Stored in
~/.galaxy/maps/<project_hash>/, cached, invalidated on file changes.

tree-sitter is the spec's choice for symbol extraction; when it's not
installed (common in minimal environments), we fall back to a regex-based
extractor that covers Python/JS/TS/Rust/Go/Java class+function signatures —
a faithful equivalent, documented in the deviations log.
"""
from __future__ import annotations

import hashlib
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from config import get_config


LANG_BY_EXT = {
    ".py": "python", ".js": "javascript", ".ts": "typescript", ".tsx": "typescript",
    ".rs": "rust", ".go": "go", ".java": "java", ".cpp": "cpp", ".c": "c",
    ".rb": "ruby", ".php": "php", ".swift": "swift", ".kt": "kotlin",
}

# regex-based symbol patterns (faithful equivalent when tree-sitter absent)
SYMBOL_PATTERNS = {
    "python": [
        re.compile(r"^(?:async\s+def|def)\s+(\w+)", re.M),
        re.compile(r"^class\s+(\w+)", re.M),
    ],
    "javascript": [
        re.compile(r"(?:export\s+)?(?:async\s+)?function\s+(\w+)", re.M),
        re.compile(r"(?:export\s+)?class\s+(\w+)", re.M),
        re.compile(r"(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s*)?\(", re.M),
    ],
    "typescript": [
        re.compile(r"(?:export\s+)?(?:async\s+)?function\s+(\w+)", re.M),
        re.compile(r"(?:export\s+)?class\s+(\w+)", re.M),
        re.compile(r"(?:export\s+)?interface\s+(\w+)", re.M),
    ],
    "rust": [
        re.compile(r"(?:pub\s+)?fn\s+(\w+)", re.M),
        re.compile(r"(?:pub\s+)?struct\s+(\w+)", re.M),
        re.compile(r"(?:pub\s+)?enum\s+(\w+)", re.M),
    ],
    "go": [
        re.compile(r"^func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)", re.M),
        re.compile(r"^type\s+(\w+)", re.M),
    ],
    "java": [
        re.compile(r"(?:public|private|protected)?\s*(?:static\s+)?(?:\w+\s+)+(\w+)\s*\(", re.M),
        re.compile(r"(?:public|private|protected)?\s*class\s+(\w+)", re.M),
    ],
}

IMPORT_PATTERNS = {
    "python": re.compile(r"^\s*(?:from\s+(\S+)\s+)?import\s+(.+)$", re.M),
    "javascript": re.compile(r"^\s*import\s+.+\s+from\s+['\"]([^'\"]+)['\"]", re.M),
    "typescript": re.compile(r"^\s*import\s+.+\s+from\s+['\"]([^'\"]+)['\"]", re.M),
}


@dataclass
class FileNode:
    path: str
    language: str
    size: int
    mtime: float
    symbols: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    is_test: bool = False


@dataclass
class CodebaseMap:
    root: str
    project_hash: str
    files: list[FileNode] = field(default_factory=list)
    built_at: float = 0.0
    symbol_index: dict[str, list[str]] = field(default_factory=dict)  # symbol -> [paths]


def _has_tree_sitter() -> bool:
    try:
        import tree_sitter  # noqa: F401
        return True
    except Exception:
        return False


def project_hash(root: Path) -> str:
    return hashlib.sha256(str(root.resolve()).encode("utf-8")).hexdigest()[:16]


def build_map(root: Path, *, use_tree_sitter: bool = True) -> CodebaseMap:
    """Build a codebase map. Target: <10s for a 10K-file repo (§13)."""
    ph = project_hash(root)
    cm = CodebaseMap(root=str(root), project_hash=ph, built_at=time.time())
    ts_available = use_tree_sitter and _has_tree_sitter()
    skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".next", "target"}
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        lang = LANG_BY_EXT.get(ext)
        if not lang:
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        rel = str(path.relative_to(root))
        node = FileNode(path=rel, language=lang, size=stat.st_size, mtime=stat.st_mtime,
                        is_test=("test" in rel.lower() or rel.endswith(("_test.go", ".test.js", ".test.tsx"))))
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            text = ""
        # symbols
        if ts_available:
            node.symbols = _tree_sitter_symbols(text, lang)
        else:
            for pat in SYMBOL_PATTERNS.get(lang, []):
                node.symbols.extend(pat.findall(text))
        # imports
        ipat = IMPORT_PATTERNS.get(lang)
        if ipat:
            node.imports = [m.group(1) or m.group(0) for m in ipat.finditer(text)][:50]
        cm.files.append(node)
        for sym in node.symbols:
            cm.symbol_index.setdefault(sym, []).append(rel)
    # cache to disk
    _save_map(cm)
    return cm


def _tree_sitter_symbols(text: str, lang: str) -> list[str]:
    """Use tree-sitter if a language pack is installed. Returns symbol names."""
    try:
        import tree_sitter as ts
        mod_name = {"python": "tree_sitter_python", "javascript": "tree_sitter_javascript",
                    "typescript": "tree_sitter_typescript", "rust": "tree_sitter_rust",
                    "go": "tree_sitter_go"}.get(lang)
        if not mod_name:
            return []
        lang_mod = __import__(mod_name)
        language = ts.Language(lang_mod.language())
        parser = ts.Parser(language)
        tree = parser.parse(text.encode("utf-8"))
        symbols: list[str] = []
        node_kinds = {"function_declaration", "method_definition", "class_declaration",
                      "function_definition", "class_definition", "impl_item", "struct_item",
                      "interface_declaration", "type_declaration"}
        def walk(n):
            if n.type in node_kinds:
                for child in n.children:
                    if child.type in ("identifier", "type_identifier", "field_identifier"):
                        symbols.append(n.text.decode("utf-8", errors="replace"))
                        break
            for child in n.children:
                walk(child)
        walk(tree.root_node)
        return symbols
    except Exception:
        return []


def _save_map(cm: CodebaseMap) -> None:
    import json
    cfg = get_config()
    d = cfg.maps_dir / cm.project_hash
    d.mkdir(parents=True, exist_ok=True)
    data = {
        "root": cm.root, "project_hash": cm.project_hash, "built_at": cm.built_at,
        "files": [{"path": f.path, "language": f.language, "size": f.size,
                    "mtime": f.mtime, "symbols": f.symbols, "imports": f.imports,
                    "is_test": f.is_test} for f in cm.files],
        "symbol_index": cm.symbol_index,
    }
    (d / "map.json").write_text(json.dumps(data), "utf-8")


def load_map(root: Path) -> CodebaseMap | None:
    import json
    cfg = get_config()
    ph = project_hash(root)
    p = cfg.maps_dir / ph / "map.json"
    if not p.exists():
        return None
    data = json.loads(p.read_text("utf-8"))
    cm = CodebaseMap(root=data["root"], project_hash=data["project_hash"], built_at=data["built_at"])
    cm.symbol_index = data.get("symbol_index", {})
    cm.files = [FileNode(**f) for f in data.get("files", [])]
    return cm
