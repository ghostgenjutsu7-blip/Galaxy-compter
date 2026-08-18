"""Portable, integrity-checked Galaxy state export/import."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import time
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from config import get_config

MANIFEST_NAME = "MANIFEST.yaml"


def _canonical_manifest(manifest: dict[str, Any]) -> bytes:
    data = dict(manifest)
    data.pop("manifest_sha256", None)
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _manifest_bytes(manifest: dict[str, Any]) -> bytes:
    # JSON is valid YAML 1.2 and avoids a lossy hand-written parser.
    return json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8")


def _read_manifest(raw: bytes) -> dict[str, Any]:
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"unsupported manifest format: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("files"), dict):
        raise ValueError("manifest must contain a files mapping")
    return data


def _add_file(zf: zipfile.ZipFile, path: Path, arc: str, files: dict[str, str]) -> None:
    zf.write(path, arc)
    files[arc] = _sha256(path)


def _audit_last_30_days(path: Path) -> bytes:
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    kept: list[str] = []
    if path.exists():
        for line in path.read_text("utf-8").splitlines():
            try:
                payload = json.loads(line)
                ts = datetime.strptime(payload["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                if ts >= cutoff:
                    kept.append(json.dumps(payload, ensure_ascii=False))
            except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                # Malformed lines cannot be dated safely and are not portable audit records.
                continue
    return ("\n".join(kept) + ("\n" if kept else "")).encode("utf-8")


def export_all() -> Path:
    cfg = get_config()
    cfg.ensure_dirs()
    ts = time.strftime("%Y%m%d-%H%M%S")
    archive = cfg.home / f"galaxy-export-{ts}.zip"
    files: dict[str, str] = {}
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(cfg.vault_dir.rglob("*.md")) if cfg.vault_dir.exists() else []:
            _add_file(zf, path, f"memory_vault/{path.relative_to(cfg.vault_dir)}", files)
        st = _storage()
        orbits = st.query_all("SELECT id,kind,solar_system_id,data,updated_at FROM orbits;")
        zf.writestr("orbits/orbits.json", json.dumps(orbits, ensure_ascii=False, indent=2))
        files["orbits/orbits.json"] = _sha256_bytes(zf.read("orbits/orbits.json") if False else
                                                     json.dumps(orbits, ensure_ascii=False, indent=2).encode("utf-8"))
        for path in sorted(cfg.skills_dir.rglob("*")) if cfg.skills_dir.exists() else []:
            if path.is_file():
                _add_file(zf, path, f"skills/{path.relative_to(cfg.skills_dir)}", files)
        connectors = _safe_query("SELECT id,kind,name,config,connected_at FROM connectors;")
        connector_bytes = json.dumps(connectors, ensure_ascii=False, indent=2, default=str).encode("utf-8")
        zf.writestr("connectors/connectors.json", connector_bytes)
        files["connectors/connectors.json"] = _sha256_bytes(connector_bytes)
        audit_bytes = _audit_last_30_days(cfg.audit_log)
        if audit_bytes:
            zf.writestr("audit.log", audit_bytes)
            files["audit.log"] = _sha256_bytes(audit_bytes)
        if cfg.eval_history.exists():
            _add_file(zf, cfg.eval_history, "eval-history.json", files)
        manifest: dict[str, Any] = {
            "schema_version": 1,
            "galaxy_version": "1.0.0",
            "exported_at": ts,
            "files": files,
        }
        manifest["manifest_sha256"] = hashlib.sha256(_canonical_manifest(manifest)).hexdigest()
        zf.writestr(MANIFEST_NAME, _manifest_bytes(manifest))
    return archive


def _safe_member(name: str) -> bool:
    path = Path(name)
    return not path.is_absolute() and ".." not in path.parts and not name.startswith("\\")


def _write_member(zf: zipfile.ZipFile, name: str, target: Path) -> None:
    if not _safe_member(name):
        raise ValueError(f"unsafe archive member: {name}")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(zf.read(name))
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, target)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def import_all(archive_path: str, *, mode: str = "merge") -> str:
    """Validate and restore a portable archive. Existing rows are upserted."""
    cfg = get_config()
    p = Path(archive_path).expanduser().resolve()
    if not p.exists():
        return f"Archive not found: {archive_path}"
    try:
        from schema.migrations import ensure_latest
        ensure_latest()
        with zipfile.ZipFile(p, "r") as zf:
            manifest = _read_manifest(zf.read(MANIFEST_NAME))
            expected_manifest_hash = hashlib.sha256(_canonical_manifest(manifest)).hexdigest()
            if expected_manifest_hash != manifest.get("manifest_sha256"):
                raise ValueError("manifest integrity check failed")
            names = set(zf.namelist())
            for name, expected_hash in manifest["files"].items():
                if name not in names or not _safe_member(name):
                    raise ValueError(f"manifest member missing or unsafe: {name}")
                actual_hash = _sha256_bytes(zf.read(name))
                if actual_hash != expected_hash:
                    raise ValueError(f"hash mismatch for {name}")
            for name in manifest["files"]:
                if name.startswith("memory_vault/"):
                    _write_member(zf, name, cfg.vault_dir / name.removeprefix("memory_vault/"))
                elif name.startswith("skills/"):
                    _write_member(zf, name, cfg.skills_dir / name.removeprefix("skills/"))
                elif name == "eval-history.json":
                    _write_member(zf, name, cfg.eval_history)
            _restore_orbits(json.loads(zf.read("orbits/orbits.json")) if "orbits/orbits.json" in names else [])
            _restore_connectors(json.loads(zf.read("connectors/connectors.json")) if "connectors/connectors.json" in names else [])
            if "audit.log" in names:
                _write_member(zf, "audit.log", cfg.audit_log)
        from core.memory import get_memory
        get_memory().vault_sync()
        return f"Imported from {archive_path}. Re-add API keys via /provider add."
    except (OSError, zipfile.BadZipFile, ValueError, json.JSONDecodeError) as exc:
        return f"Import failed: {exc}"


def _restore_orbits(rows: list[dict[str, Any]]) -> None:
    if not isinstance(rows, list):
        raise ValueError("orbits payload must be a list")
    st = _storage()
    with st.transaction() as conn:
        for row in rows:
            conn.execute("INSERT OR REPLACE INTO orbits(id,kind,solar_system_id,data,updated_at) VALUES(?,?,?,?,?);",
                         (row["id"], row["kind"], row.get("solar_system_id"), row.get("data", "{}"), row.get("updated_at", time.time())))


def _restore_connectors(rows: list[dict[str, Any]]) -> None:
    if not isinstance(rows, list):
        raise ValueError("connectors payload must be a list")
    st = _storage()
    with st.transaction() as conn:
        for row in rows:
            conn.execute("INSERT OR REPLACE INTO connectors(id,kind,name,config,connected_at) VALUES(?,?,?,?,?);",
                         (row["id"], row["kind"], row["name"], row.get("config", "{}"), row.get("connected_at", time.time())))


def forget_all() -> str:
    cfg = get_config()
    if cfg.home.exists():
        shutil.rmtree(cfg.home)
    cfg.ensure_dirs()
    from schema.migrations import ensure_latest
    ensure_latest()
    return "Wiped ~/.galaxy. Run /setup to reconfigure."


def _storage():
    from storage.local import get_storage
    return get_storage()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_query(sql: str) -> list[dict[str, Any]]:
    return _storage().query_all(sql)
