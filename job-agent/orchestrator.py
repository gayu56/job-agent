from agents.cover_letter import write_cover_letter
from agents.jd_parser import parse_jd
from agents.match_scorer import score_match
from agents.quality_checker import check_quality
from agents.resume_rewriter import rewrite_resume


def run_pipeline(resume_text: str, jd_text: str, company: str) -> dict:
    print("Step 1/5: Parsing JD...")
    jd_data = parse_jd(jd_text)

    print("Step 2/5: Scoring match...")
    match_data = score_match(resume_text, jd_data)

    print("Step 3/5: Rewriting resume...")
    new_resume = rewrite_resume(resume_text, jd_data, match_data)

    print("Step 4/5: Writing cover letter...")
    cover_letter = write_cover_letter(resume_text, jd_data, match_data, company)

    print("Step 5/5: Quality check...")
    quality = check_quality(new_resume, cover_letter, jd_data)

    return {
        "jd_analysis": jd_data,
        "match_score": match_data,
        "resume": new_resume,
        "cover_letter": cover_letter,
        "quality_report": quality,
    }
