"""Parse resume markdown into blocks for DOCX/PDF export."""


def parse_resume_markdown(md: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    current_section = ""
    section_bullet_limits = {
        "professional experience": 16,
        "relevant projects": 8,
        "technical skills": 12,
        "certifications": 10,
    }
    section_bullet_counts: dict[str, int] = {}

    lines = (md or "").splitlines()
    for raw in lines:
        line = raw.strip()
        if not line:
            if blocks and blocks[-1]["type"] != "blank":
                blocks.append({"type": "blank", "value": ""})
            continue

        if line.startswith("# "):
            blocks.append({"type": "name", "value": line[2:].strip()})
            continue
        if line.startswith("## "):
            current_section = line[3:].strip()
            blocks.append({"type": "section", "value": current_section})
            continue
        if line.startswith("### "):
            blocks.append({"type": "subsection", "value": line[4:].strip()})
            continue

        if line.startswith(("- ", "* ", "• ")):
            section_key = current_section.lower()
            limit = section_bullet_limits.get(section_key, 12)
            used = section_bullet_counts.get(section_key, 0)
            if used < limit:
                section_bullet_counts[section_key] = used + 1
                blocks.append({"type": "bullet", "value": line[2:].strip()})
            continue

        blocks.append({"type": "text", "value": line})

    normalized: list[dict[str, str]] = []
    for block in blocks:
        if block["type"] == "blank":
            if not normalized:
                continue
            if normalized[-1]["type"] in {"blank", "section"}:
                continue
        normalized.append(block)
    return normalized
