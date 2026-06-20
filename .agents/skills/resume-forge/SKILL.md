---
name: resume-forge
description: >-
  Convert a Markdown resume into a professionally formatted PDF with multiple
  style options and ATS optimization. Use this skill when the user asks to
  create a resume, format a resume, convert a resume to PDF, build a CV,
  generate a professional resume, make a resume ATS-friendly, or restyle an
  existing resume. Triggers include: 'resume', 'CV', 'curriculum vitae',
  'resume PDF', 'format my resume', 'ATS-friendly resume', 'professional resume',
  or any mention of creating career documents from markdown or plain text.
  Do NOT use for: cover letters, job searching, interview preparation,
  LinkedIn profile optimization, or portfolio websites.
license: Apache-2.0
compatibility: Requires Python 3.10+ and weasyprint. No network access needed.
metadata:
  author: sdas
  version: "1.0.0"
  last-updated: "2026-03-17"
  category: document-generation
  tags: "resume, pdf, career, formatting"
allowed-tools: Bash(python3:*) Bash(pip:*) Read Write
---

# Resume Forge — Markdown to Professional PDF

Transform a plain Markdown resume into a polished, ATS-optimized PDF.

## Quick Start

For a fast conversion with the modern template:
```bash
python3 scripts/generate_pdf.py --input resume.md --style modern --output resume.pdf
```

For the full guided workflow with validation, follow the steps below.

## Available Scripts

- **`scripts/parse_resume.py`** — Parses Markdown resume into structured JSON
- **`scripts/validate_resume.py`** — Checks for missing sections, formatting issues, ATS problems
- **`scripts/generate_pdf.py`** — Renders the final PDF from structured JSON + HTML/CSS template

## Workflow

Progress:
- [ ] Step 1: Obtain the Markdown resume
- [ ] Step 2: Parse into structured JSON (`scripts/parse_resume.py`)
- [ ] Step 3: Validate structure and content (`scripts/validate_resume.py`)
- [ ] Step 4: Fix any validation issues (loop until clean)
- [ ] Step 5: Select style and generate PDF (`scripts/generate_pdf.py`)
- [ ] Step 6: Final review and delivery

### Step 1: Obtain the Markdown Resume

Ask the user for their resume in Markdown format. If they don't have one,
help them create one following the structure in
[assets/sample_input.md](assets/sample_input.md).

The expected Markdown structure uses H1 for the name, H2 for sections,
and standard Markdown formatting for content. Example:

```markdown
# Jane Smith
**Email:** jane@example.com | **Phone:** 555-0100 | **Location:** San Francisco, CA

## Summary
Senior software engineer with 8 years of experience...

## Experience
### Senior Engineer — Acme Corp (2020–Present)
- Led migration of monolith to microservices...

## Education
### B.S. Computer Science — MIT (2016)

## Skills
Python, Go, Kubernetes, AWS, PostgreSQL
```

Save the input as `resume.md` in the working directory.

### Step 2: Parse into Structured JSON

```bash
python3 scripts/parse_resume.py --input resume.md --output parsed.json
```

This extracts:
- Contact information (name, email, phone, location, links)
- Sections in order (summary, experience, education, skills, etc.)
- Structured entries with titles, organizations, dates, and bullet points

Review `parsed.json` to confirm the structure was extracted correctly.
If the parser misidentified sections, the Markdown headings may need adjustment.

### Step 3: Validate

```bash
python3 scripts/validate_resume.py parsed.json
```

The validator checks for:
- Missing critical sections (experience, education, skills)
- Empty sections with no content
- Contact info completeness (name, email minimum)
- Date format consistency
- Bullet point quality (starts with action verb, reasonable length)
- ATS compatibility issues (no tables, images, or special characters)

### Step 4: Fix and Re-validate

If validation reports issues:
1. Read the specific error messages — they explain what's wrong and how to fix it
2. Edit `resume.md` to address the issues
3. Re-run Step 2 (parse) and Step 3 (validate)
4. **Only proceed to Step 5 when validation passes with zero errors**

Common fixes:
- "Missing section: Skills" → Add an `## Skills` section
- "No action verb" → Rewrite bullet to start with Led, Built, Designed, etc.
- "Date format inconsistent" → Standardize to `YYYY–Present` or `YYYY–YYYY`

### Step 5: Select Style and Generate PDF

Ask the user which style they prefer:

| Style | Description | Best For |
|-------|------------|----------|
| `modern` | Clean sans-serif, subtle color accents, generous whitespace | Tech, startup, design roles |
| `classic` | Traditional serif font, conservative layout, no color | Finance, law, academia, government |
| `compact` | Dense layout, smaller margins, fits more content | Experienced professionals with extensive history |

Templates live in `assets/`. Each is a self-contained HTML+CSS file.

Generate the PDF:
```bash
python3 scripts/generate_pdf.py --input parsed.json --style modern --output resume.pdf
```

For ATS-specific optimization, read
[references/ats-optimization.md](references/ats-optimization.md)
before generating — it contains keyword placement strategies and formatting
rules that affect how ATS parsers score the resume.

For industry-specific styling guidance (font choices, section ordering,
what to emphasize), read
[references/industry-styles.md](references/industry-styles.md)
only if the user specifies a target industry.

### Step 6: Final Review

Before delivering the PDF:
- Open and visually inspect it — confirm no text is cut off or overflowing
- Verify all sections from `parsed.json` appear in the PDF
- Check that contact info renders correctly at the top
- Confirm the style matches what the user requested
- If the user wanted ATS optimization, verify plain text extractability:
  ```bash
  python3 -c "
  import pdfplumber
  with pdfplumber.open('resume.pdf') as pdf:
      for page in pdf.pages:
          print(page.extract_text())
  "
  ```

## Gotchas

- **WeasyPrint font rendering**: WeasyPrint uses system fonts. If a template
  specifies a font not installed on the system, it silently falls back to
  a default serif font. The scripts install the required fonts automatically,
  but if output looks wrong, check font availability first.
- **Page overflow**: Long resumes may push content onto a second page with
  awkward breaks mid-section. The `compact` style handles this better. For
  `modern` and `classic`, the script auto-adjusts font size down by 0.5pt
  increments if content exceeds one page — but only down to 9pt minimum.
- **Special characters in names**: Accented characters (é, ñ, ü) work fine
  in the PDF but may break some ATS parsers. The validator warns about this.
- **Markdown parsing edge cases**: The parser expects `##` for sections and
  `###` for sub-entries. Using `**bold text**` as a section header instead
  of proper heading syntax will cause the parser to miss that section entirely.
- **Date ranges with em-dashes vs hyphens**: Use `–` (en-dash) not `-`
  (hyphen) for date ranges (2020–2024). The parser normalizes both, but
  the PDF renders en-dashes. If the source uses `--`, it converts automatically.
- **Link formatting**: URLs in contact info should use Markdown link syntax
  `[text](url)`. Raw URLs work but look unprofessional in the PDF output.
