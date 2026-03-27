from utils.json_llm import parse_json_object
from utils.openrouter import call_llm


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
    return parse_json_object(result)
