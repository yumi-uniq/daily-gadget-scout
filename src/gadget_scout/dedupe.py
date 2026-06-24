from __future__ import annotations

import hashlib
import re
from urllib.parse import urlparse


def normalize_text(value: str) -> str:
    lowered = value.strip().lower()
    cleaned = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", " ", lowered)
    return re.sub(r"\s+", " ", cleaned).strip()


def _canonical_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def make_dedupe_id(product_name: str, source_url: str) -> str:
    key = f"{normalize_text(product_name)}|{_canonical_domain(source_url)}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
