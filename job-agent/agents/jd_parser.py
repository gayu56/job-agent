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


def parse_jd(jd_text: str) -> dict:
    system = """You are an expert job description analyst.
Extract structured information and return ONLY valid JSON, nothing else.
JSON shape:
{
  "role_title": "",
  "seniority": "junior|mid|senior",
  "required_skills": [],
  "nice_to_have_skills": [],
  "keywords": [],
  "tone": "formal|startup|technical",
  "responsibilities": [],
  "company_values": []
}"""
    result = call_llm(system, f"Parse this JD:\n\n{jd_text}")
    return _parse_json(result)
