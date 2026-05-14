from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem, Paragraph, Preformatted, SimpleDocTemplate, Spacer

INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")


def _inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = BOLD_RE.sub(r"<b>\1</b>", escaped)
    escaped = INLINE_CODE_RE.sub(r"<font face='Courier'>\1</font>", escaped)
    return escaped


def _page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(doc.pagesize[0] - 0.6 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def markdown_to_story(text: str):
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "GuideBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        spaceAfter=6,
    )
    title = ParagraphStyle(
        "GuideTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=18,
    )
    h1 = ParagraphStyle(
        "GuideH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        spaceBefore=12,
        spaceAfter=8,
    )
    h2 = ParagraphStyle(
        "GuideH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        spaceBefore=10,
        spaceAfter=6,
    )
    h3 = ParagraphStyle(
        "GuideH3",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=8,
        spaceAfter=4,
    )
    code_style = ParagraphStyle(
        "GuideCode",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8.8,
        leading=10.5,
        leftIndent=18,
        rightIndent=18,
        spaceBefore=6,
        spaceAfter=8,
    )
    bullet_style = ParagraphStyle(
        "GuideBullet",
        parent=body,
        leftIndent=10,
        firstLineIndent=0,
        spaceAfter=2,
    )

    story = []
    paragraph_lines: list[str] = []
    bullet_lines: list[str] = []
    numbered_lines: list[str] = []
    code_lines: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            story.append(Paragraph(_inline_markup(" ".join(paragraph_lines).strip()), body))
            paragraph_lines = []

    def flush_bullets() -> None:
        nonlocal bullet_lines
        if bullet_lines:
            items = [ListItem(Paragraph(_inline_markup(line), bullet_style)) for line in bullet_lines]
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=18))
            story.append(Spacer(1, 4))
            bullet_lines = []

    def flush_numbered() -> None:
        nonlocal numbered_lines
        if numbered_lines:
            items = [
                ListItem(Paragraph(_inline_markup(line), bullet_style), value=i + 1)
                for i, line in enumerate(numbered_lines)
            ]
            story.append(ListFlowable(items, bulletType="1", leftIndent=18))
            story.append(Spacer(1, 4))
            numbered_lines = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            story.append(Preformatted("\n".join(code_lines), code_style))
            code_lines = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        if line.startswith("```"):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            continue

        if line.startswith("# "):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            story.append(Paragraph(_inline_markup(line[2:].strip()), title))
            continue

        if line.startswith("## "):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            story.append(Paragraph(_inline_markup(line[3:].strip()), h1))
            continue

        if line.startswith("### "):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            story.append(Paragraph(_inline_markup(line[4:].strip()), h2))
            continue

        if line.startswith("#### "):
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            story.append(Paragraph(_inline_markup(line[5:].strip()), h3))
            continue

        if line.startswith("- "):
            flush_paragraph()
            flush_numbered()
            bullet_lines.append(line[2:].strip())
            continue

        numbered_match = re.match(r"^\d+\.\s+(.*)$", line)
        if numbered_match:
            flush_paragraph()
            flush_bullets()
            numbered_lines.append(numbered_match.group(1).strip())
            continue

        if line.strip() == "---":
            flush_paragraph()
            flush_bullets()
            flush_numbered()
            story.append(Spacer(1, 12))
            continue

        paragraph_lines.append(line.strip())

    flush_paragraph()
    flush_bullets()
    flush_numbered()
    flush_code()
    return story


def build_pdf(markdown_path: Path, output_path: Path) -> None:
    story = markdown_to_story(markdown_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.65 * inch,
        title=markdown_path.stem,
    )
    doc.build(story, onFirstPage=_page_number, onLaterPages=_page_number)


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print("Usage: py tools/build_markdown_pdf.py <input.md> [output.pdf]")
        return 1

    markdown_path = Path(argv[1]).resolve()
    output_path = Path(argv[2]).resolve() if len(argv) == 3 else markdown_path.with_suffix(".pdf")
    build_pdf(markdown_path, output_path)
    print(f"Built PDF: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
