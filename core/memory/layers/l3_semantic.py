"""core/memory/layers/l3_semantic.py — Stars + Memory Tree + Neocortex recall.

§3, §25 Phase 2 ⑨. Hybrid: SQLite cache for querying, Markdown vault
(memory_vault/[domain]/[topic].md) for human readability AND authority. The
vault is the source of truth — deleting a vault file removes the SQLite row on
next sync (this is what makes "edit Galaxy's memory in any text editor" real).

Neocortex recall score (exact, §3):
    recall = relevance×0.5 + recency×0.3 + interactions×0.15 + random×0.05
relevance via BM25; recency via time decay; interactions via interaction_count;
random prevents echo chambers.

Knowledge graph: Stars have real edges; more-connected stars get retrieval
priority ("brighter" stars are genuinely more load-bearing).
"""
from __future__ import annotations

import json
import math
import os
import random
import re
import tempfile
import time
from dataclasses import asdict, dataclass
from typing import Any

from rank_bm25 import BM25Okapi

from config import get_config
from core.agent.base_agent import new_id
from storage.local import get_storage


@dataclass
class Star:
    id: str = ""
    topic: str = ""
    domain: str = "general"
    summary: str = ""
    content: str = ""
    vault_path: str = ""
    interaction_count: int = 0
    last_used: float = 0.0
    created_at: float = 0.0
    updated_at: float = 0.0
    edge_count: int = 0
    owner_session_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["id"] = self.id
        return d


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_]+", (text or "").lower())


class L3Semantic:
    def __init__(self) -> None:
        self._st = get_storage()
        self._cfg = get_config()

    # ---- create / sync ----------------------------------------------------
    def create_star(self, *, topic: str, domain: str, summary: str, content: str,
                    owner_session_id: str = "") -> Star:
        now = time.time()
        sid = new_id("star-")
        vault_rel = f"{domain}/{_safe(topic)}.md"
        vault_path = self._cfg.vault_dir / vault_rel
        star = Star(
            id=sid, topic=topic, domain=domain, summary=summary, content=content,
            vault_path=str(vault_rel), interaction_count=0, last_used=now,
            created_at=now, updated_at=now, edge_count=0,
            owner_session_id=owner_session_id,
        )
        self._write_vault(star)
        try:
            self._upsert_cache(star)
        except Exception:
            vault_path.unlink(missing_ok=True)
            raise
        return star

    def _write_vault(self, star: Star) -> None:
        """Markdown with versioned frontmatter (§20). Obsidian-compatible."""
        vault_path = self._cfg.vault_dir / star.vault_path
        vault_path.parent.mkdir(parents=True, exist_ok=True)
        frontmatter = {
            "schema_version": 1,
            "id": star.id,
            "topic": star.topic,
            "domain": star.domain,
            "summary": star.summary,
            "interaction_count": star.interaction_count,
            "created_at": star.created_at,
            "updated_at": star.updated_at,
            "owner_session_id": star.owner_session_id,
        }
        fm = "---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in frontmatter.items()) + "\n---\n\n"
        payload = (fm + star.content + "\n").encode("utf-8")
        fd, tmp_name = tempfile.mkstemp(prefix=f".{vault_path.name}.", suffix=".tmp", dir=vault_path.parent)
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(payload)
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp_name, vault_path)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)

    def _upsert_cache(self, star: Star) -> None:
        with self._st.transaction() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO stars(id,topic,domain,summary,content,vault_path,"
                "interaction_count,last_used,created_at,updated_at,edge_count,owner_session_id) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?);",
                (star.id, star.topic, star.domain, star.summary, star.content,
                 star.vault_path, star.interaction_count, star.last_used,
                 star.created_at, star.updated_at, star.edge_count,
                 star.owner_session_id),
            )

    def get_star(self, star_id: str) -> Star | None:
        row = self._st.query_one("SELECT * FROM stars WHERE id=?;", (star_id,))
        return self._row_to_star(row) if row else None

    def list_stars(self, domain: str | None = None) -> list[Star]:
        if domain:
            rows = self._st.query_all("SELECT * FROM stars WHERE domain=? ORDER BY updated_at DESC;", (domain,))
        else:
            rows = self._st.query_all("SELECT * FROM stars ORDER BY updated_at DESC;")
        return [self._row_to_star(r) for r in rows]

    def _row_to_star(self, row: dict[str, Any]) -> Star:
        return Star(
            id=row["id"], topic=row["topic"], domain=row["domain"],
            summary=row["summary"], content=row["content"],
            vault_path=row.get("vault_path") or "", interaction_count=row.get("interaction_count", 0),
            last_used=row.get("last_used", 0.0), created_at=row.get("created_at", 0.0),
            updated_at=row.get("updated_at", 0.0), edge_count=row.get("edge_count", 0),
            owner_session_id=row.get("owner_session_id") or "",
        )

    # ---- sync: vault is authoritative ------------------------------------
    def sync_from_vault(self) -> dict[str, int]:
        """Walk memory_vault/, rebuild the SQLite cache. Removing a vault file
        removes the corresponding SQLite row (§3)."""
        stats = {"added": 0, "updated": 0, "removed": 0}
        # collect vault files
        seen: set[str] = set()
        if self._cfg.vault_dir.exists():
            for md in self._cfg.vault_dir.rglob("*.md"):
                rel = str(md.relative_to(self._cfg.vault_dir))
                seen.add(rel)
                frontmatter, body = _parse_frontmatter(md.read_text(encoding="utf-8"))
                sid = frontmatter.get("id") or new_id("star-")
                star = Star(
                    id=sid, topic=frontmatter.get("topic", md.stem),
                    domain=frontmatter.get("domain", md.parent.name or "general"),
                    summary=frontmatter.get("summary", ""), content=body,
                    vault_path=rel,
                    interaction_count=int(frontmatter.get("interaction_count", 0)),
                    last_used=float(frontmatter.get("last_used", 0.0) or 0.0),
                    created_at=float(frontmatter.get("created_at", time.time()) or time.time()),
                    updated_at=float(frontmatter.get("updated_at", time.time()) or time.time()),
                    edge_count=int(frontmatter.get("edge_count", 0)),
                    owner_session_id=frontmatter.get("owner_session_id", ""),
                )
                self._upsert_cache(star)
                stats["updated" if frontmatter.get("id") else "added"] += 1
        # remove cache rows whose vault file is gone
        rows = self._st.query_all("SELECT id, vault_path FROM stars;")
        for r in rows:
            if r["vault_path"] and r["vault_path"] not in seen:
                with self._st.transaction() as conn:
                    conn.execute("DELETE FROM stars WHERE id=?;", (r["id"],))
                    conn.execute("DELETE FROM star_edges WHERE src=? OR dst=?;", (r["id"], r["id"]))
                stats["removed"] += 1
        return stats

    # ---- edges (knowledge graph) -----------------------------------------
    def add_edge(self, src: str, dst: str, weight: float = 1.0, kind: str = "related") -> None:
        with self._st.transaction() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO star_edges(src,dst,weight,kind) VALUES(?,?,?,?);",
                (src, dst, weight, kind),
            )
            conn.execute("UPDATE stars SET edge_count=(SELECT COUNT(*) FROM star_edges WHERE src=stars.id OR dst=stars.id) WHERE id IN (?,?);",
                         (src, dst))

    def edges_of(self, star_id: str) -> list[dict[str, Any]]:
        return self._st.query_all(
            "SELECT * FROM star_edges WHERE src=? OR dst=?;", (star_id, star_id))

    # ---- Neocortex recall (exact formula, §3) ----------------------------
    def search(self, query: str, top_k: int = 5) -> list[Star]:
        stars = self.list_stars()
        if not stars:
            return []
        corpus = [_tokenize(f"{s.topic} {s.summary} {s.content}") for s in stars]
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(_tokenize(query))
        now = time.time()
        max_inter = max((s.interaction_count for s in stars), default=1) or 1
        max_edges = max((s.edge_count for s in stars), default=1) or 1
        ranked: list[tuple[float, Star]] = []
        for s, rel in zip(stars, scores):
            rel_n = min(1.0, max(0.0, rel / (max(scores) if max(scores) > 0 else 1.0)))
            recency = math.exp(-max(0.0, now - s.last_used) / (30 * 86400))
            interactions = (s.interaction_count / max_inter) if max_inter else 0.0
            random_noise = random.random()
            graph_priority = (s.edge_count / max_edges) * 0.10
            recall = ((rel_n * 0.50) + (recency * 0.30) +
                      (interactions * 0.15) + (random_noise * 0.05) + graph_priority)
            # graph priority makes connected stars genuinely brighter.
            ranked.append((recall, s))
        ranked.sort(key=lambda t: t[0], reverse=True)
        return [s for _, s in ranked[:top_k]]

    def touch(self, star_id: str) -> None:
        with self._st.transaction() as conn:
            conn.execute(
                "UPDATE stars SET interaction_count=interaction_count+1, last_used=? WHERE id=?;",
                (time.time(), star_id),
            )

    def delete_star(self, star_id: str) -> None:
        star = self.get_star(star_id)
        if not star:
            return
        if star.vault_path:
            p = self._cfg.vault_dir / star.vault_path
            if p.exists():
                p.unlink()
        with self._st.transaction() as conn:
            conn.execute("DELETE FROM stars WHERE id=?;", (star_id,))
            conn.execute("DELETE FROM star_edges WHERE src=? OR dst=?;", (star_id, star_id))


def _safe(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", name).strip("-")[:60] or "untitled"


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    fm: dict[str, Any] = {}
    body = text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                v = v.strip()
                try:
                    fm[k.strip()] = json.loads(v)
                except Exception:
                    fm[k.strip()] = v
        body = m.group(2)
    return fm, body
