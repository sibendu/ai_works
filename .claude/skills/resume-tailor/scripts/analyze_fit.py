#!/usr/bin/env python
"""Create a lightweight ATS fit analysis between a job description and resume."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

STOPWORDS = {
    "about", "across", "after", "also", "and", "are", "based", "been", "both", "but", "can", "for",
    "from", "has", "have", "into", "our", "that", "the", "their", "this", "through", "with", "will",
    "you", "your", "job", "role", "work", "team", "teams", "using", "use", "including", "required",
    "preferred", "experience", "years", "ability", "strong",
}

PHRASE_PATTERNS = [
    r"\b[A-Z][A-Za-z0-9.+#-]*(?:\s+[A-Z][A-Za-z0-9.+#-]*){0,3}\b",
    r"\b(?:agentic ai|generative ai|gen ai|retrieval[- ]augmented generation|rag|llmops|mlops)\b",
    r"\b(?:enterprise architecture|solution architecture|cloud native|distributed systems)\b",
    r"\b(?:stakeholder management|executive communication|technical leadership|delivery assurance)\b",
    r"\b(?:kubernetes|docker|microservices|api|apis|azure|aws|gcp|oci|openai|anthropic|langchain|langgraph)\b",
]


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def words(text: str) -> list[str]:
    return [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9.+#-]{2,}", text)]


def top_terms(text: str, limit: int = 60) -> list[str]:
    counts = Counter(w for w in words(text) if w not in STOPWORDS)
    return [term for term, _ in counts.most_common(limit)]


def phrases(text: str) -> list[str]:
    found: set[str] = set()
    for pattern in PHRASE_PATTERNS:
        for match in re.findall(pattern, text, flags=re.I):
            phrase = " ".join(match.split())
            if len(phrase) > 2:
                found.add(phrase)
    return sorted(found, key=lambda p: (p.lower(), p))


def contains_term(text: str, term: str) -> bool:
    return re.search(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text, re.I) is not None


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- None found"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job", required=True, help="Normalized job Markdown")
    parser.add_argument("--resume", required=True, help="Source resume Markdown")
    parser.add_argument("--output", "-o", default="output/fit_analysis.md", help="Output analysis Markdown")
    args = parser.parse_args()

    job = read(args.job)
    resume = read(args.resume)

    job_terms = top_terms(job)
    matched_terms = [term for term in job_terms if contains_term(resume, term)]
    missing_terms = [term for term in job_terms if term not in matched_terms]

    job_phrases = phrases(job)
    matched_phrases = [phrase for phrase in job_phrases if contains_term(resume, phrase)]
    missing_phrases = [phrase for phrase in job_phrases if phrase not in matched_phrases]

    report = f"""# Resume Fit Analysis

## High-Value JD Terms Already Present

{bullet_list(matched_terms[:30])}

## JD Terms Not Found Verbatim

{bullet_list(missing_terms[:30])}

## JD Phrases Already Present

{bullet_list(matched_phrases[:30])}

## JD Phrases Not Found Verbatim

{bullet_list(missing_phrases[:30])}

## Tailoring Notes

- Use this report as a screening aid, not as permission to add unsupported claims.
- Prefer missing JD terms only when the resume contains equivalent factual evidence.
- Ask the user before adding any missing tool, domain, certification, leadership scope, metric, or business ownership claim.
"""
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
