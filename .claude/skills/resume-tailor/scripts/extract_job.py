#!/usr/bin/env python
"""Normalize a job URL, HTML file, text file, or Markdown file into role-focused Markdown."""

from __future__ import annotations

import argparse
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urlparse

ROLE_KEYWORDS = {
    "about the role",
    "the role",
    "responsibilities",
    "what you will do",
    "what you'll do",
    "requirements",
    "qualifications",
    "preferred qualifications",
    "skills",
    "experience",
    "job description",
    "who you are",
    "you will",
    "we are looking",
}

NOISE_PATTERNS = [
    r"cookie",
    r"privacy policy",
    r"terms of use",
    r"equal opportunity",
    r"sign up",
    r"subscribe",
    r"related jobs",
    r"share this",
    r"follow us",
]


def is_url(source: str) -> bool:
    parsed = urlparse(source)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def read_source(source: str) -> tuple[str, str]:
    if is_url(source):
        try:
            import requests

            response = requests.get(source, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            return response.text, response.headers.get("content-type", "")
        except ImportError:
            from urllib.request import Request, urlopen

            request = Request(source, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=30) as response:  # noqa: S310 - user-provided public JD URL.
                return response.read().decode("utf-8", errors="replace"), response.headers.get("content-type", "")

    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Job source not found: {source}")
    return path.read_text(encoding="utf-8", errors="replace"), path.suffix.lower()


def clean_text(text: str) -> str:
    text = unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def looks_like_html(text: str, content_type: str) -> bool:
    return "html" in content_type.lower() or bool(re.search(r"<(html|body|div|section|article|h1|p|li)\b", text, re.I))


def node_text(node) -> str:
    return clean_text(node.get_text("\n", strip=True))


def score_block(text: str) -> int:
    lowered = text.lower()
    score = sum(4 for keyword in ROLE_KEYWORDS if keyword in lowered)
    score -= sum(4 for pattern in NOISE_PATTERNS if re.search(pattern, lowered))
    if 800 <= len(text) <= 12000:
        score += 3
    if len(text) > 20000:
        score -= 4
    return score


def html_to_markdown(html: str) -> tuple[str, str]:
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise RuntimeError("BeautifulSoup is required for HTML job extraction. Install bs4 or provide a text file.") from exc

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "form", "nav", "header", "footer", "aside"]):
        tag.decompose()

    title = ""
    h1 = soup.find("h1")
    if h1:
        title = node_text(h1)
    if not title and soup.title and soup.title.string:
        title = clean_text(soup.title.string)

    candidates = []
    for selector in ["main", "article", "[role='main']", ".job-description", ".jobDescription", "#job-description"]:
        for node in soup.select(selector):
            text = node_text(node)
            if text:
                candidates.append((score_block(text), node))

    if not candidates:
        for node in soup.find_all(["section", "div"], recursive=True):
            text = node_text(node)
            if len(text) > 500:
                candidates.append((score_block(text), node))

    best_node = max(candidates, key=lambda item: item[0])[1] if candidates else soup.body or soup
    lines: list[str] = []
    seen: set[str] = set()

    for element in best_node.find_all(["h1", "h2", "h3", "p", "li"], recursive=True):
        text = node_text(element)
        if not text or len(text) < 2:
            continue
        lowered = text.lower()
        if any(re.search(pattern, lowered) for pattern in NOISE_PATTERNS) and len(text) < 240:
            continue
        fingerprint = re.sub(r"\W+", "", lowered)[:120]
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        if element.name in {"h1", "h2"}:
            lines.append(f"\n## {text}\n")
        elif element.name == "h3":
            lines.append(f"\n### {text}\n")
        elif element.name == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)

    markdown = clean_text("\n\n".join(lines))
    return title or "Job Description", markdown


def text_to_markdown(text: str) -> tuple[str, str]:
    text = clean_text(text)
    lines = text.splitlines()
    title = "Job Description"
    for line in lines:
        stripped = line.strip("#* -")
        if stripped and len(stripped) < 140:
            title = stripped
            break
    return title, text


def write_job_markdown(title: str, body: str, output: Path) -> None:
    if not body.lstrip().startswith("#"):
        body = f"# {title}\n\n{body}"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(clean_text(body) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="Public job URL or local job text/Markdown/HTML file")
    parser.add_argument("--output", "-o", default="output/job.md", help="Output Markdown path")
    args = parser.parse_args()

    raw, content_type = read_source(args.source)
    if looks_like_html(raw, content_type):
        title, body = html_to_markdown(raw)
    else:
        title, body = text_to_markdown(raw)
    write_job_markdown(title, body, Path(args.output))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
