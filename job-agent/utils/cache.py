"""Small in-memory cache for expensive JD parsing (same text re-run)."""

import hashlib
from typing import Any

_MAX_ENTRIES = 64
_cache: dict[str, Any] = {}


def jd_cache_key(jd_text: str) -> str:
    return hashlib.sha256((jd_text or "").encode("utf-8")).hexdigest()[:24]


def get_cached_jd(jd_text: str) -> Any | None:
    key = jd_cache_key(jd_text)
    return _cache.get(key)


def set_cached_jd(jd_text: str, value: Any) -> None:
    key = jd_cache_key(jd_text)
    if len(_cache) >= _MAX_ENTRIES:
        _cache.pop(next(iter(_cache)), None)
    _cache[key] = value
