import json

from utils.json_llm import parse_json_object
from utils.openrouter import call_llm


def score_match(resume_text: str, jd_parsed: dict) -> dict:
    system = """You are a ruthlessly honest hiring manager.
Score how well this resume matches the job. Return ONLY valid JSON:
{
  "overall_fit_percent": 0-100,
  "strong_matches": [],
  "gaps": [],
  "transferable_skills": [],
  "red_flags": [],
  "top_3_angles_to_emphasize": []
}"""
    user = f"""
RESUME:
{resume_text}

JOB REQUIREMENTS:
{json.dumps(jd_parsed, indent=2)}
"""
    result = call_llm(system, user)
    return parse_json_object(result)
