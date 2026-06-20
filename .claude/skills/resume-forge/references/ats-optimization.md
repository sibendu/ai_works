# ATS Optimization Guide

This reference is loaded only when the user requests ATS-optimized output.

## How ATS Parsers Work

Applicant Tracking Systems (ATS) like Workday, Greenhouse, Lever, and iCIMS
extract text from resumes and attempt to map content to structured fields:
name, email, experience entries, education, skills. They then score the
resume against the job description using keyword matching.

## Formatting Rules for ATS Compatibility

1. **No tables** — ATS parsers read left-to-right, top-to-bottom. Tables
   cause columns to be interleaved, producing garbage text.
2. **No text boxes or graphics** — Invisible to most parsers.
3. **No headers/footers** — Some ATS skip header/footer regions. Put contact
   info in the body.
4. **Standard section headings** — Use exactly: "Experience", "Education",
   "Skills", "Summary". Avoid creative names like "Where I've Been" or
   "My Toolkit" — parsers rely on heading recognition.
5. **Simple bullet points** — Use standard dashes or dots. Unicode bullets
   (▪, ◆, ★) may render as unknown characters.
6. **No columns** — Single-column layout only. Two-column resumes break most
   ATS extraction.

## Keyword Strategy

- **Mirror the job description**: If the posting says "project management",
  use "project management" — not "PM" or "managing projects".
- **Include both acronyms and full forms**: "Amazon Web Services (AWS)",
  "Structured Query Language (SQL)".
- **Place keywords naturally**: In bullet points, not keyword-stuffed lists.
- **Skills section**: Use a comma-separated list matching the job posting's
  exact terminology.

## Section Order for Maximum ATS Score

1. Contact Information (name, email, phone, location)
2. Summary (2-3 sentences with key role keywords)
3. Skills (comma-separated, matching job description)
4. Experience (reverse chronological)
5. Education
6. Certifications (if applicable)

## Date Formats

ATS parsers handle these reliably:
- `January 2020 – Present`
- `Jan 2020 – Dec 2023`
- `2020 – Present`
- `2020 – 2023`

These may fail:
- `1/2020 - 12/2023` (slash format)
- `Q1 2020 – Q4 2023` (quarter format)
- `2020-01 to 2023-12` (ISO-ish format)

## Font Recommendations for ATS

Stick to standard fonts. ATS extracts text regardless of font, but embedded
custom fonts can bloat the PDF and occasionally cause extraction issues:
- **Safe**: Arial, Calibri, Helvetica, Georgia, Times New Roman, Garamond
- **Avoid**: Custom/downloaded fonts, decorative fonts, icon fonts
