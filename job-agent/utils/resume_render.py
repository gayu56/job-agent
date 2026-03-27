"""Render structured resume JSON to ATS markdown and apply length presets."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def trim_resume_data(data: dict[str, Any], preset: str) -> dict[str, Any]:
    """preset: one_page | two_page"""
    out = deepcopy(data)
    one = preset == "one_page"

    max_roles = 3 if one else 5
    max_bullets_role = 3 if one else 4
    max_projects = 2 if one else 4
    max_bullets_proj = 2 if one else 3
    max_summary_lines = 2 if one else 4

    summ = out.get("summary") or []
    if isinstance(summ, str):
        summ = [summ]
    out["summary"] = summ[:max_summary_lines]

    skills = out.get("skills") or []
    if isinstance(skills, list):
        for block in skills:
            if not isinstance(block, dict):
                continue
            items = block.get("items") or []
            if isinstance(items, list) and one:
                block["items"] = items[:6]
    out["skills"] = skills

    exp = out.get("experience") or []
    if isinstance(exp, list):
        exp = exp[:max_roles]
        for role in exp:
            if not isinstance(role, dict):
                continue
            bullets = role.get("bullets") or []
            if isinstance(bullets, list):
                role["bullets"] = bullets[:max_bullets_role]
        out["experience"] = exp

    proj = out.get("projects") or []
    if isinstance(proj, list):
        proj = proj[:max_projects]
        for p in proj:
            if not isinstance(p, dict):
                continue
            bullets = p.get("bullets") or []
            if isinstance(bullets, list):
                p["bullets"] = bullets[:max_bullets_proj]
        out["projects"] = proj

    edu = out.get("education") or []
    if isinstance(edu, list) and one:
        out["education"] = edu[:2]

    certs = out.get("certifications") or []
    if isinstance(certs, list) and one:
        out["certifications"] = certs[:6]

    return out


def render_resume_markdown(data: dict[str, Any]) -> str:
    """Convert structured resume dict to markdown string."""
    lines: list[str] = []

    name = (data.get("full_name") or "").strip()
    contact = (data.get("contact_line") or "").strip()
    if name:
        lines.append(f"# {name}")
    if contact:
        lines.append(contact)
        lines.append("")

    summary = data.get("summary") or []
    if isinstance(summary, str):
        summary = [summary]
    if summary:
        lines.append("## Professional Summary")
        for s in summary:
            if str(s).strip():
                lines.append(str(s).strip())
        lines.append("")

    skills = data.get("skills") or []
    if skills:
        lines.append("## Technical Skills")
        for block in skills:
            if not isinstance(block, dict):
                continue
            cat = (block.get("category") or "").strip()
            items = block.get("items") or []
            if isinstance(items, list):
                joined = ", ".join(str(x).strip() for x in items if str(x).strip())
            else:
                joined = str(items)
            if cat or joined:
                lines.append(f"- {cat}: {joined}" if cat else f"- {joined}")
        lines.append("")

    exp = data.get("experience") or []
    if exp:
        lines.append("## Professional Experience")
        for role in exp:
            if not isinstance(role, dict):
                continue
            title = (role.get("title") or "").strip()
            company = (role.get("company") or "").strip()
            dates = (role.get("dates") or "").strip()
            header = " | ".join(x for x in [title, company, dates] if x)
            if header:
                lines.append(f"### {header}")
            for b in role.get("bullets") or []:
                if str(b).strip():
                    lines.append(f"- {str(b).strip()}")
            lines.append("")

    proj = data.get("projects") or []
    if proj:
        lines.append("## Relevant Projects")
        for p in proj:
            if not isinstance(p, dict):
                continue
            pname = (p.get("name") or "").strip()
            if pname:
                lines.append(f"### {pname}")
            for b in p.get("bullets") or []:
                if str(b).strip():
                    lines.append(f"- {str(b).strip()}")
            lines.append("")

    edu = data.get("education") or []
    if edu:
        lines.append("## Education")
        for e in edu:
            if str(e).strip():
                lines.append(f"- {str(e).strip()}")
        lines.append("")

    certs = data.get("certifications") or []
    if certs:
        lines.append("## Certifications")
        for c in certs:
            if str(c).strip():
                lines.append(f"- {str(c).strip()}")

    return "\n".join(lines).strip() + "\n"
