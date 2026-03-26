import json

from utils.openrouter import call_llm


def _parse_json(content: str) -> dict:
    text = content.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start : end + 1]
    return json.loads(text)


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
    return _parse_json(result)
