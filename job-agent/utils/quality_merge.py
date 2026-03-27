"""Merge LLM quality report with deterministic keyword stats."""


def merge_quality_report(llm_report: dict, keyword_stats: dict) -> dict:
    out = dict(llm_report or {})
    out["keyword_coverage_percent"] = keyword_stats.get("coverage_percent", out.get("keyword_coverage_percent", 0))
    out["missing_keywords"] = keyword_stats.get("missing", out.get("missing_keywords", []))
    out["matched_keywords"] = keyword_stats.get("matched", [])
    return out
