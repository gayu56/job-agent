"""Lightweight comparison of original vs rewritten resume for unsupported claims."""

import json

from utils.json_llm import parse_json_object
from utils.openrouter import call_llm


def fact_check_resume(original_resume: str, rewritten_markdown: str) -> dict:
    system = """You compare an ORIGINAL resume with a REWRITTEN resume.
Return ONLY valid JSON:
{
  "risk_level": "low|medium|high",
  "flags": [
    {"issue": "short description", "severity": "info|warn|high"}
  ]
}
Rules:
- Flag only potential fabrication: new employers, degrees, certifications, metrics, or tools not plausibly implied by the original.
- If uncertain, use severity info and keep risk_level low or medium.
- Maximum 8 flags. Empty flags array is OK."""

    user = f"""ORIGINAL RESUME:
{original_resume[:12000]}

REWRITTEN RESUME:
{rewritten_markdown[:12000]}
"""
    raw = call_llm(system, user)
    try:
        return parse_json_object(raw)
    except (json.JSONDecodeError, ValueError):
        return {"risk_level": "low", "flags": [], "parse_error": True}
