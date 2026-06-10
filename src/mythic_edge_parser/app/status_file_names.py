from __future__ import annotations

import hashlib
import re

SAFE_STATUS_STEM_RE = re.compile(r"[^A-Za-z0-9._-]+")
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{index}" for index in range(1, 10)),
    *(f"LPT{index}" for index in range(1, 10)),
}


def safe_status_file_stem(value: object, *, fallback: str = "status") -> str:
    raw = str(value or "").strip()
    digest = hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()[:12]
    candidate = SAFE_STATUS_STEM_RE.sub("_", raw).strip("._-")
    if not candidate:
        candidate = fallback
    if candidate.upper() in WINDOWS_RESERVED_NAMES:
        candidate = fallback
    if candidate != raw or len(candidate) > 80:
        candidate = f"{candidate[:67].rstrip('._-')}_{digest}"
    return candidate
