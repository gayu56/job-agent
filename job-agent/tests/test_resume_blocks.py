from utils.resume_blocks import parse_resume_markdown


def test_parse_headings():
    md = """# Name Here
Line contact

## Professional Summary
Summary text

## Technical Skills
- Cat: a, b
"""
    blocks = parse_resume_markdown(md)
    types = [b["type"] for b in blocks if b["type"] != "blank"]
    assert "name" in types
    assert "section" in types
