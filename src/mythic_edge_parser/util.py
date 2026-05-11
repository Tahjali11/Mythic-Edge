from __future__ import annotations

import gzip
import hashlib


def compress_log(text: str) -> bytes:
    return gzip.compress(text.encode("utf-8"))


def content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()
