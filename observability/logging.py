"""observability/logging.py — loguru config (TTY + JSON).

§11, §25 Phase 10 ㊼. Per-component loggers (galaxy.orchestrator, galaxy.agent.code,
galaxy.memory.l3, galaxy.security, ...). Sensitive data filtered at the log
boundary by security/secret_filter.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from config import get_config
from security.secret_filter import redact


_configured = False


def configure_logging(*, level: str = "INFO", json_mode: bool = False) -> None:
    global _configured
    if _configured:
        return
    cfg = get_config()
    cfg.home.mkdir(parents=True, exist_ok=True)
    log_path = cfg.home / "galaxy.log"
    logger.remove()
    # TTY handler (or stderr in non-TTY)
    fmt = ("{time:HH:mm:ss} | {level:<7} | {name}:{function}:{line} | {message}")
    logger.add(sys.stderr, format=fmt, level=level, colorize=True,
               filter=lambda record: _redact_filter(record))
    # file handler
    logger.add(log_path, format=fmt, level=level, rotation="10 MB", retention="30 days",
               filter=lambda record: _redact_filter(record))
    if json_mode:
        logger.add(log_path.with_suffix(".jsonl"),
                   serialize=True, level=level, rotation="10 MB", retention="30 days",
                   filter=lambda record: _redact_filter(record))
    _configured = True


def _redact_filter(record) -> bool:
    """Redact secrets from log messages before they're written."""
    msg = record.get("message", "")
    if msg:
        record["message"] = redact(msg)
    return True


def get_logger(name: str):
    """Get a per-component logger."""
    if not _configured:
        configure_logging()
    return logger.bind(name=name)
