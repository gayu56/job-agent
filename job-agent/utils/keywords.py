"""Deterministic keyword coverage from JD keywords vs resume text."""

import re
from typing import Any


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _tokenize_phrase(phrase: str) -> list[str]:
    s = re.sub(r"[^\w\s\-/]", " ", phrase.lower())
    return [t for t in re.split(r"[\s/]+", s) if len(t) > 1]


def compute_keyword_stats(jd_keywords: list[str], resume_text: str) -> dict[str, Any]:
    """
    Match each keyword/phrase against resume text (substring or token overlap).
    Returns coverage_percent, matched, missing, total_keywords.
    """
    resume_norm = _normalize(resume_text)
    raw = [k for k in (jd_keywords or []) if str(k).strip()]
    if not raw:
        return {
            "coverage_percent": 0,
            "matched": [],
            "missing": [],
            "total_keywords": 0,
        }

    matched: list[str] = []
    missing: list[str] = []
    for kw in raw:
        k = str(kw).strip()
        kn = _normalize(k)
        if len(kn) < 2:
            continue
        if kn in resume_norm or k.lower() in resume_norm:
            matched.append(k)
            continue
        tokens = _tokenize_phrase(k)
        if len(tokens) >= 2:
            if all(t in resume_norm for t in tokens if len(t) > 2):
                matched.append(k)
                continue
        elif tokens and tokens[0] in resume_norm:
            matched.append(k)
            continue
        missing.append(k)

    total = len(matched) + len(missing)
    pct = round(100 * len(matched) / total) if total else 0
    return {
        "coverage_percent": pct,
        "matched": matched,
        "missing": missing,
        "total_keywords": total,
    }
