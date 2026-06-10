from __future__ import annotations

import re
from urllib.parse import urlparse

URL_TOKEN_RE = re.compile(r"https?://[^\s)>\]}\"]+", re.IGNORECASE)


def contains_runtime_artifact_url(value: str) -> bool:
    """Return true for known runtime/webhook URL hosts without substring trust."""
    for match in URL_TOKEN_RE.finditer(value):
        parsed = urlparse(match.group(0))
        host = (parsed.hostname or "").lower()
        if host == "script.google.com" or host.startswith("hooks."):
            return True
    return False
