from utils.openrouter import call_llm_strong


def rewrite_resume(resume_text: str, jd_parsed: dict, match_data: dict) -> str:
    system = """You are an elite resume writer who has helped 1000+ candidates land jobs.
Rewrite the resume bullets to:
1. Mirror exact keywords from the job description naturally
2. Lead with the strongest matches first
3. Quantify achievements where possible (add [X%] placeholders if unknown)
4. Match the tone of the company (startup = punchy, enterprise = formal)
5. Keep it truthful - enhance framing, never fabricate
6. Keep the output ATS-friendly and compact enough for 1-2 pages

Return ONLY clean markdown using this exact structure and order:
# Full Name
Location | Phone | Email | LinkedIn

## Professional Summary
2-3 lines only.

## Technical Skills
- Category: item, item, item

## Professional Experience
### Job Title | Company | Dates
- 3-4 bullets max per role, each bullet one line and impact-focused

## Relevant Projects
### Project Name
- 2 bullets max per project

## Education
- Degree, School | Dates

## Certifications
- Certification name

Formatting rules:
- No long paragraphs in experience.
- No repeated headings.
- No empty sections.
- Do not exceed content needed for a clean 1-2 page resume."""

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
"""
    return call_llm_strong(system, user)
