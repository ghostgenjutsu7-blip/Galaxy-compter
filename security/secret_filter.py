"""security/secret_filter.py — output redaction for logs (§10).

Pattern-matched redaction at every log boundary. The filtered output is what
gets logged AND shown to the user. Plus entropy-based detection for unknown
secret shapes.
"""
from __future__ import annotations

import math
import re
from typing import Any


SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),                              # OpenAI / most providers
    re.compile(r"sk-ant-[A-Za-z0-9-]{20,}"),                         # Anthropic
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),                             # GitHub PAT
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),                     # Slack
    re.compile(r"AIza[A-Za-z0-9_-]{35}"),                            # Google API key
    re.compile(r"eyJ[A-Za-z0-9_=-]+\.eyJ[A-Za-z0-9_=-]+\.?[A-Za-z0-9_.+/=-]*"),  # JWT
    re.compile(r"Bearer\s+[A-Za-z0-9_.-]{20,}"),                     # Bearer tokens
    re.compile(r"(?i)password\s*[:=]\s*\S+"),                        # password= in config
]


_REDACTED = "[REDACTED]"


def _shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq: dict[str, int] = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


def _looks_like_secret(token: str) -> bool:
    """Entropy-based detection for unknown secret shapes (§10)."""
    if len(token) < 20:
        return False
    # high entropy + mixed character classes
    has_upper = any(c.isupper() for c in token)
    has_lower = any(c.islower() for c in token)
    has_digit = any(c.isdigit() for c in token)
    has_special = any(not c.isalnum() for c in token)
    classes = sum([has_upper, has_lower, has_digit, has_special])
    return _shannon_entropy(token) > 4.0 and classes >= 3


def redact(text: str) -> str:
    """Apply all secret patterns + entropy detection. Returns redacted text."""
    if not text:
        return text
    out = text
    for pat in SECRET_PATTERNS:
        out = pat.sub(_REDACTED, out)
    # entropy-based: scan long alphanumeric tokens
    def _entropy_sub(m: re.Match) -> str:
        tok = m.group(0)
        return _REDACTED if _looks_like_secret(tok) else tok
    out = re.sub(r"[A-Za-z0-9_+/=-]{24,}", _entropy_sub, out)
    return out


def redact_dict(d: dict[str, Any]) -> dict[str, Any]:
    """Recursively redact all string values in a dict."""
    out: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, str):
            out[k] = redact(v)
        elif isinstance(v, dict):
            out[k] = redact_dict(v)
        elif isinstance(v, list):
            out[k] = [redact(x) if isinstance(x, str) else (redact_dict(x) if isinstance(x, dict) else x) for x in v]
        else:
            out[k] = v
    return out
