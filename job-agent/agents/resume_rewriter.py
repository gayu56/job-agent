import json

from utils.json_llm import parse_json_object
from utils.openrouter import call_llm_strong
from utils.resume_render import render_resume_markdown, trim_resume_data


def rewrite_resume(resume_text: str, jd_parsed: dict, match_data: dict, preset: str = "one_page") -> tuple[str, dict]:
    """
    Returns (markdown_resume, structured_dict).
    preset: one_page | two_page
    """
    system = """You are an elite resume writer. Output ONLY valid JSON, no markdown fences, no extra text.
JSON schema:
{
  "full_name": "",
  "contact_line": "City | phone | email | linkedin",
  "summary": ["line1", "line2"],
  "skills": [{"category": "Name", "items": ["a", "b"]}],
  "experience": [{"title": "", "company": "", "dates": "", "bullets": ["..."]}],
  "projects": [{"name": "", "bullets": ["..."]}],
  "education": ["Degree, School | dates"],
  "certifications": ["..."]
}
Rules:
- Mirror JD keywords naturally in bullets and skills.
- Be truthful: reframe only; do not invent employers, degrees, or tools not in the original.
- Keep content appropriate for ATS."""

    keywords = jd_parsed.get("keywords", [])
    emphasis = match_data.get("top_3_angles_to_emphasize", [])
    gaps = match_data.get("gaps", [])
    tone = jd_parsed.get("tone", "technical")

    user = f"""
ORIGINAL RESUME:
{resume_text}

TARGET JD KEYWORDS: {", ".join(keywords)}
SKILLS TO EMPHASIZE: {", ".join(emphasis)}
GAPS TO DOWNPLAY: {", ".join(gaps)}
TONE: {tone}
PRESET: {preset} (one_page = tighter bullet counts; two_page = allow more roles/bullets)
"""
    raw = call_llm_strong(system, user)
    try:
        data = parse_json_object(raw)
    except (json.JSONDecodeError, ValueError):
        raw2 = call_llm_strong(
            "Return ONLY valid JSON matching the schema. No prose.",
            "Fix this to valid JSON only:\n\n" + raw[:8000],
        )
        data = parse_json_object(raw2)

    if not isinstance(data, dict):
        raise ValueError("Resume rewriter did not return an object")

    trimmed = trim_resume_data(data, preset)
    md = render_resume_markdown(trimmed)
    return md, trimmed
