#!/usr/bin/env python
"""Render an approved Markdown resume to ATS-friendly HTML and PDF."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import re
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO


def render_markdown(markdown_text: str) -> str:
    try:
        import markdown
    except ImportError as exc:
        raise RuntimeError("The markdown package is required to render resumes.") from exc

    markdown_text = normalize_markdown_text(markdown_text)
    return markdown.markdown(
        markdown_text,
        extensions=["extra", "sane_lists", "smarty"],
        output_format="html5",
    )


def normalize_markdown_text(markdown_text: str) -> str:
    return markdown_text.replace(r"\&", "&")


def annotate_header_contact(body_html: str) -> str:
    h1_match = re.search(r"</h1>\s*", body_html, flags=re.I)
    if not h1_match:
        return body_html

    cursor = h1_match.end()
    contact_matches: list[re.Match[str]] = []
    paragraph_pattern = re.compile(r"\s*(<p\b[^>]*>.*?</p>)", flags=re.I | re.S)

    while True:
        paragraph_match = paragraph_pattern.match(body_html, cursor)
        if not paragraph_match:
            break
        paragraph_html = paragraph_match.group(1)
        paragraph_text = re.sub(r"<[^>]+>", " ", paragraph_html)
        if not re.search(r"@|https?://|www\.|linkedin|github|Phone:|Email:|Location:", paragraph_text, flags=re.I):
            break
        contact_matches.append(paragraph_match)
        cursor = paragraph_match.end()

    if not contact_matches:
        return body_html

    pieces: list[str] = []
    last_end = 0
    for index, match in enumerate(contact_matches):
        paragraph_html = match.group(1)
        classes = "resume-contact"
        if index == len(contact_matches) - 1:
            classes += " resume-contact-final"
        annotated = re.sub(r"<p\b", f'<p class="{classes}"', paragraph_html, count=1, flags=re.I)
        pieces.append(body_html[last_end:match.start(1)])
        pieces.append(annotated)
        last_end = match.end(1)
    pieces.append(body_html[last_end:])
    return "".join(pieces)


def render_template(template_path: Path, context: dict[str, str]) -> str:
    try:
        from jinja2 import Environment, FileSystemLoader, select_autoescape
    except ImportError as exc:
        raise RuntimeError("The jinja2 package is required to render resume templates.") from exc

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_path.name)
    return template.render(**context)


def write_pdf(html: str, output: Path, base_url: Path) -> None:
    try:
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            from weasyprint import HTML
    except Exception as exc:
        raise RuntimeError(f"WeasyPrint is unavailable: {exc}") from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(base_url)).write_pdf(str(output))


def plain_text(markdown_text: str) -> str:
    text = markdown_text
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\\([&*_#-])", r"\1", text)
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"').replace("\u00a0", " ")
    return text


def safe_pdf_text(text: str) -> str:
    return plain_text(text).encode("latin-1", errors="replace").decode("latin-1")


def fallback_pdf(markdown_text: str, output: Path, template_name: str) -> None:
    try:
        from fpdf import FPDF
    except ImportError as exc:
        raise RuntimeError("Neither WeasyPrint nor fpdf is available for PDF generation.") from exc

    styles = {
        "classic": {
            "font": "Times",
            "body": 9.5,
            "h1": 18.8,
            "h2": 9.7,
            "h3": 9.5,
            "margin": 34,
            "accent": (42, 72, 88),
            "rule": (138, 154, 166),
            "band": (244, 247, 249),
            "text": (24, 24, 24),
            "muted": (70, 78, 86),
        },
        "executive": {
            "font": "Helvetica",
            "body": 9.2,
            "h1": 19,
            "h2": 9.5,
            "h3": 9.2,
            "margin": 32,
            "accent": (30, 58, 95),
            "rule": (110, 132, 155),
            "band": (239, 244, 248),
            "text": (30, 34, 39),
            "muted": (68, 78, 90),
        },
        "modern": {
            "font": "Helvetica",
            "body": 8.65,
            "h1": 19,
            "h2": 9.0,
            "h3": 8.85,
            "margin": 32,
            "accent": (11, 92, 141),
            "rule": (132, 169, 196),
            "band": (238, 246, 250),
            "text": (31, 41, 51),
            "muted": (70, 88, 105),
        },
    }
    style = styles.get(template_name, styles["classic"])
    pdf = FPDF(format="Letter", unit="pt")
    pdf.set_auto_page_break(auto=True, margin=24)
    pdf.set_margins(style["margin"], 28, style["margin"])
    pdf.add_page()
    width = pdf.w - pdf.l_margin - pdf.r_margin
    header_rule_pending = False
    header_contact_seen = False
    lines = markdown_text.splitlines()
    contact_pattern = re.compile(r"@|https?://|www\.|linkedin|github|Phone:|Email:|Location:", flags=re.I)

    def line_gap(points: float) -> None:
        pdf.ln(points)

    def set_rgb(name: str) -> None:
        pdf.set_text_color(*style[name])

    def multicell(text: str, height: float, align: str = "L", fill: bool = False, width_override: float | None = None) -> None:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            width_override or width,
            height,
            text,
            align=align,
            fill=fill,
            new_x="LMARGIN",
            new_y="NEXT",
            wrapmode="WORD",
        )

    def multicell_rich(text: str, height: float, font_name: str, font_size: float) -> None:
        """Render text with inline **bold** markdown support."""
        bold_pattern = re.compile(r"\*\*([^*]+)\*\*")
        parts = bold_pattern.split(text)
        pdf.set_x(pdf.l_margin)
        # parts alternates: plain, bold, plain, bold, ...
        # Use write() for inline mixed formatting, then ln
        for i, part in enumerate(parts):
            if not part:
                continue
            part = safe_pdf_text(part)
            if i % 2 == 1:
                pdf.set_font(font_name, "B", font_size)
            else:
                pdf.set_font(font_name, "", font_size)
            pdf.write(height, part)
        pdf.ln(height)

    def looks_like_contact(text: str) -> bool:
        return bool(contact_pattern.search(text))

    def next_nonempty_is_contact(start: int) -> bool:
        for upcoming_raw in lines[start:]:
            upcoming_line = upcoming_raw.strip()
            if upcoming_line:
                return looks_like_contact(upcoming_line)
        return False

    def draw_pending_header_rule() -> None:
        nonlocal header_rule_pending, header_contact_seen
        if not header_rule_pending:
            return
        pdf.set_draw_color(*style["rule"])
        pdf.set_line_width(0.8)
        pdf.line(pdf.l_margin, pdf.get_y() + 1.5, pdf.w - pdf.r_margin, pdf.get_y() + 1.5)
        line_gap(4)
        header_rule_pending = False
        header_contact_seen = False

    for index, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            if header_rule_pending:
                if header_contact_seen and not next_nonempty_is_contact(index + 1):
                    draw_pending_header_rule()
                elif header_contact_seen:
                    line_gap(2)
                continue
            line_gap(3)
            continue
        if re.fullmatch(r"#+", line):
            continue
        line = safe_pdf_text(line)
        if line.startswith("# "):
            set_rgb("accent")
            pdf.set_font(style["font"], "B", style["h1"])
            multicell(line[2:].strip(), style["h1"] + 3, align="C" if template_name == "classic" else "L")
            line_gap(4)
            header_rule_pending = True
            header_contact_seen = False
        elif line.startswith("## "):
            draw_pending_header_rule()
            line_gap(5)
            title = line[3:].strip().upper()
            pdf.set_fill_color(*style["band"])
            set_rgb("accent")
            pdf.set_font(style["font"], "B", style["h2"])
            multicell(title, style["h2"] + 4, fill=True)
            pdf.set_draw_color(*style["rule"])
            pdf.set_line_width(0.6)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
            line_gap(3.5)
        elif line.startswith("### "):
            draw_pending_header_rule()
            h3_text = safe_pdf_text(line[4:].strip())
            is_subtitle = bool(re.search(r"\|.*\d{4}", h3_text))
            if is_subtitle:
                set_rgb("text")
                pdf.set_font(style["font"], "B", style["body"] + 0.2)
                multicell(h3_text, style["body"] + 3)
            else:
                line_gap(2)
                set_rgb("text")
                pdf.set_font(style["font"], "B", style["h3"] + 0.6)
                multicell(h3_text, style["h3"] + 3.5)
        elif line.startswith(("* ", "- ")):
            draw_pending_header_rule()
            set_rgb("text")
            pdf.set_font(style["font"], "", style["body"])
            bullet = line[2:].strip()
            pdf.set_text_color(*style["text"])
            if "**" in bullet:
                multicell_rich(f"• {bullet}", style["body"] + 3, style["font"], style["body"])
            else:
                multicell(f"- {safe_pdf_text(bullet)}", style["body"] + 3)
        else:
            is_contact = header_rule_pending and looks_like_contact(line)
            if header_rule_pending and not is_contact:
                draw_pending_header_rule()
            pdf.set_font(style["font"], "", style["body"] - 0.4 if is_contact else style["body"])
            set_rgb("muted" if is_contact else "text")
            align = "C" if is_contact and template_name == "classic" else "L"
            multicell(line, style["body"] + 3, align=align)
            if is_contact:
                header_contact_seen = True

    pdf.output(str(output))


def resolve_template(name: str, templates_dir: Path) -> Path:
    candidates = [
        templates_dir / f"{name}.html",
        templates_dir / f"template_{name}.html",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    available = sorted(path.stem.replace("template_", "") for path in templates_dir.glob("*.html"))
    raise FileNotFoundError(f"Template '{name}' not found in {templates_dir}. Available: {', '.join(available)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resume_md", help="Reviewed customized Markdown resume")
    parser.add_argument("--template", default="classic", help="Template name: classic, executive, or modern")
    parser.add_argument("--templates-dir", default=str(Path(__file__).resolve().parents[1] / "assets" / "templates"))
    parser.add_argument("--output", "-o", help="Output PDF path")
    parser.add_argument("--html-output", help="Optional HTML output path for visual debugging")
    args = parser.parse_args()

    resume_path = Path(args.resume_md)
    templates_dir = Path(args.templates_dir)
    output_dir = Path("output")
    output = Path(args.output) if args.output else output_dir / resume_path.with_suffix(".pdf").name
    html_output = Path(args.html_output) if args.html_output else output.with_suffix(".html")

    markdown_text = resume_path.read_text(encoding="utf-8", errors="replace")
    body_html = annotate_header_contact(render_markdown(markdown_text))
    title = resume_path.stem.replace("_", " ").title()
    first_heading = next((line.strip("# ").strip() for line in markdown_text.splitlines() if line.startswith("# ")), "")
    if first_heading:
        title = first_heading

    template_path = resolve_template(args.template, templates_dir)
    html = render_template(template_path, {"title": title, "body_html": body_html, "source_file": str(resume_path)})
    html_output.parent.mkdir(parents=True, exist_ok=True)
    html_output.write_text(html, encoding="utf-8")
    try:
        write_pdf(html, output, template_path.parent)
    except Exception as exc:
        print(f"HTML PDF rendering unavailable; using fpdf fallback. Reason: {exc}", file=sys.stderr)
        output.parent.mkdir(parents=True, exist_ok=True)
        fallback_pdf(markdown_text, output, args.template)
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
