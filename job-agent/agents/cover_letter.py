from utils.openrouter import call_llm_strong


def write_cover_letter(resume_text: str, jd_parsed: dict, match_data: dict, company: str) -> str:
    system = """You are a cover letter specialist. Write a compelling,
specific cover letter that does NOT start with 'I am excited...'
Rules:
- Open with a hook specific to the company/role
- Paragraph 1: Why this company specifically
- Paragraph 2: Your strongest 2 matching experiences with impact
- Paragraph 3: What you will bring in first 90 days
- Close: Confident, not desperate
- Max 300 words. No fluff."""

    role = jd_parsed.get("role_title", "")
    values = ", ".join(jd_parsed.get("company_values", []))
    strengths = ", ".join(match_data.get("strong_matches", []))

    user = f"""
Company: {company}
Role: {role}
Company values: {values}
My top strengths for this role: {strengths}
Resume highlights: {resume_text[:1000]}
"""
    return call_llm_strong(system, user)
