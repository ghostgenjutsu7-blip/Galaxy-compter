"""failure/atomic.py — transactional memory writes (§3, §15).

Wraps multi-step memory writes in SQLite transactions. A failure rolls back,
so there are no half-written asteroids. Used by complete_task and the
Subconscious Loop promotion path.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

from storage.local import get_storage


@contextmanager
def atomic(label: str = "") -> Iterator[Any]:
    """Transactional context. Commits on success, rolls back on exception."""
    st = get_storage()
    with st.transaction() as conn:
        yield conn


def safe_write(write_fn, *args, **kwargs) -> Any:
    """Run a write function inside a transaction. Returns its result or raises."""
    with atomic():
        return write_fn(*args, **kwargs)
