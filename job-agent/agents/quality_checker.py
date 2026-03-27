from utils.json_llm import parse_json_object
from utils.openrouter import call_llm


def check_quality(rewritten_resume: str, cover_letter: str, jd_parsed: dict) -> dict:
    system = """You are an ATS (Applicant Tracking System) expert and hiring coach.
Evaluate the resume and cover letter and return ONLY valid JSON:
{
  "ats_score": 0-100,
  "keyword_coverage_percent": 0-100,
  "missing_keywords": [],
  "formatting_issues": [],
  "suggestions": [],
  "interview_likelihood": "low|medium|high",
  "one_line_verdict": ""
}"""
    user = f"""
RESUME:
{rewritten_resume}

COVER LETTER:
{cover_letter}

REQUIRED KEYWORDS: {jd_parsed.get("keywords", [])}
"""
    result = call_llm(system, user)
    return parse_json_object(result)
