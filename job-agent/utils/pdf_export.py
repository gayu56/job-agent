"""ATS-style resume PDF using ReportLab Platypus."""

import io

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from utils.resume_blocks import parse_resume_markdown


def build_resume_pdf_bytes(markdown_body: str, title: str = "Resume") -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title=title,
    )
    styles = getSampleStyleSheet()
    name_style = ParagraphStyle(
        "ResumeName",
        parent=styles["Heading1"],
        fontSize=14,
        spaceAfter=6,
        textColor=styles["Heading1"].textColor,
    )
    section_style = ParagraphStyle(
        "ResumeSection",
        parent=styles["Heading2"],
        fontSize=11,
        spaceBefore=10,
        spaceAfter=6,
        textTransform="uppercase",
    )
    sub_style = ParagraphStyle(
        "ResumeSub",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "ResumeBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=12,
        spaceAfter=3,
    )
    bullet_style = ParagraphStyle(
        "ResumeBullet",
        parent=body_style,
        leftIndent=12,
        bulletIndent=6,
    )

    story = []
    blocks = parse_resume_markdown(markdown_body)

    def esc(t: str) -> str:
        return (
            (t or "")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    for block in blocks:
        btype = block["type"]
        value = esc(block.get("value", ""))
        if btype == "name":
            story.append(Paragraph(value, name_style))
        elif btype == "section":
            story.append(Spacer(1, 4))
            story.append(Paragraph(value, section_style))
        elif btype == "subsection":
            story.append(Paragraph(value, sub_style))
        elif btype == "bullet":
            story.append(Paragraph(f"• {value}", bullet_style))
        elif btype == "text":
            story.append(Paragraph(value, body_style))
        elif btype == "blank":
            story.append(Spacer(1, 6))

    doc.build(story)
    return buf.getvalue()
