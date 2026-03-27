from agents.cover_letter import write_cover_letter
from agents.fact_check import fact_check_resume
from agents.jd_parser import parse_jd
from agents.match_scorer import score_match
from agents.quality_checker import check_quality
from agents.resume_rewriter import rewrite_resume
from utils.cache import get_cached_jd, set_cached_jd
from utils.keywords import compute_keyword_stats
from utils.quality_merge import merge_quality_report


def run_pipeline(
    resume_text: str,
    jd_text: str,
    company: str,
    options: dict | None = None,
) -> dict:
    """
    options:
      resume_preset: one_page | two_page
      fact_check: bool (default True)
    """
    opts = options or {}
    preset = opts.get("resume_preset") or "one_page"
    if preset not in ("one_page", "two_page"):
        preset = "one_page"
    fact_check_enabled = opts.get("fact_check", True)
    if isinstance(fact_check_enabled, str):
        fact_check_enabled = fact_check_enabled.lower() in ("1", "true", "yes", "on")

    meta: dict = {"preset": preset, "jd_cache_hit": False, "steps": []}

    cached = get_cached_jd(jd_text)
    if cached is not None:
        jd_data = cached
        meta["jd_cache_hit"] = True
    else:
        jd_data = parse_jd(jd_text)
        set_cached_jd(jd_text, jd_data)
    meta["steps"].append("jd_parsed")

    match_data = score_match(resume_text, jd_data)
    meta["steps"].append("match_scored")

    new_resume, resume_structured = rewrite_resume(resume_text, jd_data, match_data, preset=preset)
    meta["steps"].append("resume_rewritten")

    cover_letter = write_cover_letter(resume_text, jd_data, match_data, company)
    meta["steps"].append("cover_letter")

    quality = check_quality(new_resume, cover_letter, jd_data)

    kw_stats = compute_keyword_stats(jd_data.get("keywords", []), new_resume)
    quality = merge_quality_report(quality, kw_stats)
    meta["steps"].append("quality_check")

    fact_check_result = None
    if fact_check_enabled:
        fact_check_result = fact_check_resume(resume_text, new_resume)
        meta["steps"].append("fact_check")

    return {
        "jd_analysis": jd_data,
        "match_score": match_data,
        "resume": new_resume,
        "resume_structured": resume_structured,
        "original_resume_excerpt": (resume_text or "")[:4000],
        "cover_letter": cover_letter,
        "quality_report": quality,
        "keyword_stats": kw_stats,
        "fact_check": fact_check_result,
        "meta": meta,
    }
