from utils.resume_render import render_resume_markdown, trim_resume_data


def test_render_minimal():
    data = {
        "full_name": "Jane Doe",
        "contact_line": "TX | j@e.com",
        "summary": ["Line one"],
        "skills": [{"category": "Lang", "items": ["Python"]}],
        "experience": [
            {"title": "Eng", "company": "Co", "dates": "2020–Present", "bullets": ["Did X"]}
        ],
        "projects": [],
        "education": ["MS, School | 2024"],
        "certifications": ["AWS"],
    }
    md = render_resume_markdown(trim_resume_data(data, "one_page"))
    assert "Jane Doe" in md
    assert "Professional Summary" in md
    assert "Python" in md
