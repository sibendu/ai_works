#!/usr/bin/env python
"""Review a generated resume PDF for text accuracy and visible layout problems."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"[*_#>`\\]", " ", text)
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"[^a-z0-9+#.@/-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text: str) -> list[str]:
    return [t for t in normalize(text).split() if len(t) > 2]


def extract_pdf_text(pdf_path: Path) -> tuple[str, int, list[tuple[float, float, int]]]:
    try:
        import pdfplumber

        pages = []
        metrics = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                pages.append(page_text)
                metrics.append((float(page.width), float(page.height), len(page.extract_words())))
        return "\n".join(pages), len(metrics), metrics
    except Exception:
        from pdfminer.high_level import extract_text

        text = extract_text(str(pdf_path))
        try:
            import pypdfium2 as pdfium

            pdf = pdfium.PdfDocument(str(pdf_path))
            return text, len(pdf), []
        except Exception:
            return text, 0, []


def important_lines(markdown_text: str) -> list[str]:
    selected: list[str] = []
    for raw in markdown_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(("# ", "## ", "### ")):
            selected.append(line.strip("# ").strip())
            continue
        if "@" in line or "http" in line or "Phone:" in line or "Location:" in line:
            selected.append(line)
            continue
        if line.startswith(("* ", "- ")) and len(selected) < 80:
            selected.append(line[2:].strip())
    return selected


def section_titles(markdown_text: str) -> list[str]:
    return [line[3:].strip() for line in markdown_text.splitlines() if line.startswith("## ")]


def normalize_section(title: str) -> str:
    title = title.lower().strip()
    title = title.replace("&", "and")
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def line_coverage(line: str, pdf_norm: str) -> float:
    line_tokens = tokens(line)
    if not line_tokens:
        return 1.0
    hits = sum(1 for token in line_tokens if token in pdf_norm)
    return hits / len(line_tokens)


def render_pages(pdf_path: Path, output_dir: Path) -> tuple[list[Path], list[str], list[float]]:
    warnings: list[str] = []
    images: list[Path] = []
    page_fills: list[float] = []
    try:
        import pypdfium2 as pdfium
        from PIL import Image, ImageChops
    except Exception as exc:
        return images, [f"Could not render page images for visual QA: {exc}"], page_fills

    output_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    for index, page in enumerate(pdf):
        image = page.render(scale=1.5).to_pil().convert("RGB")
        image_path = output_dir / f"{pdf_path.stem}_page_{index + 1}.png"
        image.save(image_path)
        images.append(image_path)

        background = Image.new(image.mode, image.size, (255, 255, 255))
        diff = ImageChops.difference(image, background)
        bbox = diff.getbbox()
        if bbox is None:
            page_fills.append(0.0)
            warnings.append(f"Page {index + 1} appears blank.")
            continue
        left, top, right, bottom = bbox
        page_fills.append(bottom / image.height)
        margin = 10
        if left <= margin or top <= margin or right >= image.width - margin or bottom >= image.height - margin:
            warnings.append(
                f"Page {index + 1} has content very close to an edge; inspect for clipping or distorted layout."
            )
    return images, warnings, page_fills


def write_report(
    output: Path,
    status: str,
    resume_md: Path,
    pdf_path: Path,
    checks: list[tuple[str, str, str]],
    images: list[Path],
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Final Review and Delivery Report",
        "",
        f"Status: **{status}**",
        "",
        f"- Resume Markdown: `{resume_md}`",
        f"- PDF: `{pdf_path}`",
        "",
        "## Checks",
        "",
        "| Status | Check | Detail |",
        "| --- | --- | --- |",
    ]
    for check_status, name, detail in checks:
        lines.append(f"| {check_status} | {name} | {detail.replace('|', '/')} |")
    if images:
        lines.extend(["", "## Rendered Pages", ""])
        lines.extend(f"- `{image}`" for image in images)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume-md", required=True, help="Approved customized Markdown resume")
    parser.add_argument("--pdf", required=True, help="Generated PDF resume")
    parser.add_argument("--source-resume-md", help="Original source resume Markdown for section-structure checks")
    parser.add_argument("--output", default="output/final_review.md", help="Review report path")
    parser.add_argument("--render-dir", default="output/pdf_review", help="Directory for rendered page PNGs")
    parser.add_argument("--max-pages", type=int, default=2, help="Maximum acceptable page count for final delivery")
    parser.add_argument("--target-pages", type=int, default=2, help="Expected page count for balanced final delivery")
    parser.add_argument(
        "--min-final-page-fill",
        type=float,
        default=0.80,
        help="Minimum rendered vertical fill ratio for the final page when target page count is met",
    )
    args = parser.parse_args()

    resume_md = Path(args.resume_md)
    pdf_path = Path(args.pdf)
    report_path = Path(args.output)
    render_dir = Path(args.render_dir)

    checks: list[tuple[str, str, str]] = []
    failures = 0
    warnings = 0

    if not resume_md.exists():
        checks.append(("FAIL", "Markdown exists", f"Missing source Markdown: {resume_md}"))
        failures += 1
        markdown_text = ""
    else:
        markdown_text = resume_md.read_text(encoding="utf-8", errors="replace")
        checks.append(("PASS", "Markdown exists", "Source Markdown found."))

    if args.source_resume_md:
        source_resume_md = Path(args.source_resume_md)
        if not source_resume_md.exists():
            checks.append(("FAIL", "Section structure", f"Missing original source resume: {source_resume_md}"))
            failures += 1
        else:
            source_sections = {normalize_section(title) for title in section_titles(source_resume_md.read_text(encoding="utf-8", errors="replace"))}
            customized_sections = section_titles(markdown_text)
            invented_sections = [
                title for title in customized_sections
                if normalize_section(title) and normalize_section(title) not in source_sections
            ]
            if invented_sections:
                checks.append((
                    "FAIL",
                    "Section structure",
                    f"Customized resume introduces section(s) not present in the source resume: {', '.join(invented_sections[:6])}.",
                ))
                failures += 1
            else:
                checks.append(("PASS", "Section structure", "Customized resume uses source resume section headings."))

    if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
        checks.append(("FAIL", "PDF exists", f"Missing or unexpectedly small PDF: {pdf_path}"))
        failures += 1
        pdf_text, page_count, page_metrics = "", 0, []
    else:
        pdf_text, page_count, page_metrics = extract_pdf_text(pdf_path)
        checks.append(("PASS", "PDF exists", f"PDF size is {pdf_path.stat().st_size} bytes."))

    if page_count:
        if page_count > args.max_pages:
            checks.append(("FAIL", "Page count", f"{page_count} pages; final submission resumes must be {args.max_pages} pages or fewer."))
            failures += 1
        elif page_count < args.target_pages:
            checks.append(("FAIL", "Page count", f"{page_count} page(s); final submission resumes should use {args.target_pages} balanced pages."))
            failures += 1
        else:
            checks.append(("PASS", "Page count", f"{page_count} page(s), matching the {args.target_pages}-page target."))
        sparse = [str(i + 1) for i, (_, _, words) in enumerate(page_metrics) if words < 40]
        if sparse:
            checks.append(("FAIL", "Text extraction", f"Very low extracted word count on page(s): {', '.join(sparse)}."))
            failures += 1
        elif page_metrics:
            checks.append(("PASS", "Text extraction", "PDF text is extractable on every page."))
        else:
            checks.append(("PASS", "Text extraction", "PDF text is extractable; page-level word counts were unavailable in this environment."))

    pdf_norm = normalize(pdf_text)
    missing_lines: list[str] = []
    for line in important_lines(markdown_text):
        threshold = 0.65 if len(tokens(line)) > 10 else 0.8
        if line_coverage(line, pdf_norm) < threshold:
            missing_lines.append(line)
    if missing_lines:
        sample = "; ".join(missing_lines[:6])
        checks.append(("FAIL", "Content accuracy", f"{len(missing_lines)} important Markdown line(s) not found in PDF text. Examples: {sample}"))
        failures += 1
    else:
        checks.append(("PASS", "Content accuracy", "Important headings, contact lines, and bullets are present in extracted PDF text."))

    images, visual_warnings, page_fills = render_pages(pdf_path, render_dir)
    if page_count == args.target_pages and page_fills:
        final_fill = page_fills[-1]
        if final_fill < args.min_final_page_fill:
            checks.append((
                "FAIL",
                "Page balance",
                f"Final page uses about {final_fill:.0%} of page height; target is at least {args.min_final_page_fill:.0%}.",
            ))
            failures += 1
        else:
            checks.append(("PASS", "Page balance", f"Final page uses about {final_fill:.0%} of page height."))
    if visual_warnings:
        checks.append(("FAIL", "Visual layout", " ".join(visual_warnings[:4])))
        failures += 1
    else:
        checks.append(("PASS", "Visual layout", "Rendered page images show no blank pages or edge-clipping signals."))

    status = "FAIL" if failures else "WARN" if warnings else "PASS"
    write_report(report_path, status, resume_md, pdf_path, checks, images)
    print(f"Wrote {report_path} with status {status}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
