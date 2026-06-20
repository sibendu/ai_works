---
name: resume-tailor
description: Tailor a Markdown resume to a specific job description and render an ATS-friendly PDF. Use when Codex needs to customize a resume/CV for a role from a job URL, pasted job description, or local job file; compare the job against a Markdown resume; create a truthful recruiter-ready customized resume; run job-description and resume review iterations; and generate a professional PDF using classic, executive, or modern templates.
---

# Resume Tailor

Create a truthful, ATS-friendly customized resume from a job description and a source Markdown resume, then render the approved version to PDF.

## Inputs

- `job`: Required. Accept a public URL, a local text/Markdown/HTML file, or pasted job description text.
- `resume`: Optional. Default to `sample_resume.md` in the working directory when not provided.
- `template`: Optional. Default to `classic`. Supported values: `classic`, `executive`, `modern`.

## Core Workflow

1. Resolve input paths and derive output names:
   - Create an `output/` directory in the working directory unless the user requests another location.
   - Save every generated artifact under `output/`: normalized JD, fit analysis, customized Markdown, HTML debug output, final PDF, final review report, and rendered PDF page PNGs.
   - Save the normalized job description as `output/job.md` unless the user requests another name.
   - Save the customized resume as `output/<resume_file_stem>_customized.md`.
   - Save the final PDF as `output/<resume_file_stem>_customized.pdf`.
2. Normalize the job description:
   - For a URL or HTML file, run `scripts/extract_job.py` and keep only role-relevant content.
   - For a text or Markdown file, run `scripts/extract_job.py` to normalize headings and spacing.
   - If the user pasted the job description directly, create a temporary `.txt` file or write `output/job.md` from the pasted content.
3. Pause for job-description review:
   - Read `references/review-checklists.md` and use the "Job Description Extraction Review" checklist.
   - Summarize the extracted role title, responsibilities, required qualifications, preferred qualifications, technologies, leadership expectations, and any content intentionally excluded as non-role material.
   - Stop and ask the user to manually review `output/job.md` before tailoring begins, especially when the JD came from a URL.
   - If the user edits `output/job.md` manually, reread the edited file before continuing.
   - If the user says something was missed or incorrectly included, update `output/job.md`, summarize the correction, and ask for confirmation again.
   - Continue only after the user approves `output/job.md` or explicitly says to skip this review.
4. Analyze the fit:
   - Run `scripts/analyze_fit.py --job output/job.md --resume <resume.md> --output output/fit_analysis.md`.
   - Read `references/tailoring-policy.md` before editing the resume.
   - Read `references/ats-keyword-guidance.md` when deciding keyword coverage and phrasing.
   - Identify high-value JD keywords: required tools, platforms, architecture patterns, cloud providers, domain terms, leadership scope, compliance terms, and role-title language.
   - Represent each important JD keyword somewhere in the resume only when the source resume contains matching factual evidence.
   - Do not fabricate tools, platforms, industries, responsibilities, seniority, metrics, certifications, direct reports, budget ownership, compliance exposure, or hands-on experience.
   - Preserve seniority and truthfulness over keyword density. If a keyword is important but only implied, ask the user a direct clarification question before adding it. If support remains unclear, leave it out.
5. Draft the customized resume:
   - Use the original resume as the only source of factual claims.
   - Preserve the source resume's main `##` section structure. Do not invent new main sections to pad length.
   - Do not add generic sections such as `Strategic Impact`, `Accomplishments`, `Leadership Highlights`, or similar unless the same section already exists in the source resume or the user explicitly requests it.
   - If the resume is short, enrich existing sections only: summary, experience bullets, existing highlights/strengths, existing skills, and existing education.
   - Reorder, emphasize, compress, and rephrase existing evidence to match the job.
   - Prefer the job description's terminology when the resume contains matching substance.
   - Do not invent employers, roles, dates, metrics, tools, industries, certifications, publications, patents, degrees, direct reports, budget ownership, or hands-on experience.
   - Preserve seniority and truthfulness over keyword density.
   - Draft for exactly 2 well-filled PDF pages by default for job submissions. A few lines of final whitespace is acceptable; a half-empty second page is not.
   - Keep the summary to one tight, coherent paragraph of 4-6 lines.
   - Make the summary sound like a senior architect's positioning statement, not a keyword collage. Avoid oddly narrow parenthetical examples unless they are essential to the JD.
   - Highlight differentiators with evidence: production-grade GenAI/Agentic AI systems, measurable ROI, enterprise integration, scale, regulated environments, stakeholder influence, and architecture leadership when supported by the source resume.
   - Avoid redundant technology name-dropping in the summary when the skills section already covers those tools.
   - Prioritize recent and job-relevant experience bullets; keep 4-6 bullets for the current role, 4-5 for the next most relevant role, and 2-4 for older roles unless the JD strongly depends on older evidence.
   - Compress older experience into high-signal scope, architecture impact, domains, and delivery scale rather than exhaustive responsibilities.
   - Group skills into compact, keyword-rich lines by category. Keep JD-critical keywords, remove duplicates, and avoid long tool inventories that do not support the target role.
   - Keep education minimal. Omit interests from job-submission PDFs unless the user explicitly asks to retain them.
   - If the first draft is too short, add truthful high-value evidence before adding low-value filler: production details, architecture scope, delivery scale, regulated-domain context, stakeholder scope, integration complexity, or JD-relevant older-role evidence already present in the source resume.
6. Ask before using uncertain claims:
   - If the JD requires a capability that is implied but not stated in the resume, ask the user a direct clarification question before adding it.
   - Mark unresolved gaps in a short "Questions before finalizing" list rather than guessing.
7. Reflect and refine the draft:
   - Before asking the user to review, reread the source resume, normalized JD, fit analysis, and customized draft.
   - Critically check whether the draft sounds credible to an experienced recruiter or senior technical leader.
   - Refine generic, random, or overfit language. Remove phrases that feel like filler, hype, or disconnected keyword stacking.
   - Verify the summary has a clear senior positioning arc: role identity, scale/domain, differentiating expertise, production outcomes, and leadership/stakeholder value.
   - Verify all high-value JD keywords are either truthfully represented, explicitly unsupported, or captured as clarification questions.
   - Verify the customized resume did not introduce any new main sections compared with the source resume.
   - Verify content balance for a 2-page PDF: not over 2 pages, not a sparse 1.3-1.6 pages, and no half-empty second page.
   - Prefer expanding with meaningful, source-supported accomplishments over restoring low-value sections such as interests.
8. Run pre-review layout and structure check:
   - Write `output/<resume_file_stem>_customized.md`.
   - Render a temporary pre-review PDF: `scripts/render_resume.py output/<customized.md> --template <template> --output output/<customized_pre_review.pdf> --html-output output/<customized_pre_review.html>`.
   - Run `scripts/review_delivery.py --resume-md output/<customized.md> --source-resume-md <resume.md> --pdf output/<customized_pre_review.pdf> --output output/pre_review.md --render-dir output/pre_review_pages`.
   - The pre-review must pass page count, page balance, extractable text, visual layout, and section-structure checks before asking the user to review the Markdown.
   - If the second page is sparse, expand only within existing sections using meaningful, source-supported evidence. Do not add new sections as padding.
9. Save the draft Markdown:
   - Write `output/<resume_file_stem>_customized.md`.
   - Summarize what changed and what still needs user review.
   - Stop and ask the user to manually review the Markdown before PDF generation.
10. Iterate resume Markdown review:
   - If the user edits the Markdown manually, reread the edited file before continuing.
   - If the user asks for changes, update only the customized Markdown unless they explicitly ask to modify the source resume.
   - Repeat until the user approves the customized Markdown for PDF generation.
11. Render the PDF:
   - Run `scripts/render_resume.py output/<customized.md> --template <template> --output output/<customized.pdf> --html-output output/<customized.html>`.
   - Use `classic` if the template name is omitted or unknown, after telling the user.
12. Run automated final review:
   - Run `scripts/review_delivery.py --resume-md output/<customized.md> --source-resume-md <resume.md> --pdf output/<customized.pdf> --output output/final_review.md --render-dir output/pdf_review`.
   - Confirm the PDF is 2 well-filled pages by default, has extractable text, key Markdown content appears in the PDF, pages render successfully, and no rendered page has content clipped at the edges.
   - Inspect any rendered PNGs in `output/pdf_review/` if the report shows warnings or failures.
   - If the PDF exceeds 2 pages, condense the Markdown first, then adjust template density only modestly. Do not solve length by making text uncomfortably small.
   - If the PDF is under 2 pages or the second page is less than 80% filled, enrich existing sections with truthful, JD-relevant evidence already present in the source resume rather than adding filler or new sections.
   - Fix the Markdown, template, or rendering problem and rerun render/review until the report is `PASS` or the user explicitly accepts a known warning.
13. Pause for final manual PDF review:
   - Read `references/review-checklists.md` and use the "Final Manual PDF Review" checklist.
   - Share the PDF path, `output/final_review.md` path, and rendered page PNG directory.
   - Stop and ask the user to manually inspect the PDF for visual polish, factual accuracy, ordering, spacing, typography, page breaks, and any final discrepancies.
   - If the user requests final-touch changes, update the customized Markdown and/or template, rerender the PDF, rerun automated final review, and ask for final manual review again.
   - Deliver the final PDF only after the automated review passes and the user gives final approval.

## Script Usage

Normalize a job source:

```bash
python scripts/extract_job.py <url-or-file> --output output/job.md
```

Create a fit analysis report:

```bash
python scripts/analyze_fit.py --job output/job.md --resume sample_resume.md --output output/fit_analysis.md
```

Render a reviewed resume:

```bash
python scripts/render_resume.py output/sample_resume_customized.md --template classic --output output/sample_resume_customized.pdf --html-output output/sample_resume_customized.html
```

Run final review before delivery:

```bash
python scripts/review_delivery.py --resume-md output/sample_resume_customized.md --pdf output/sample_resume_customized.pdf --output output/final_review.md --render-dir output/pdf_review
```

Pass `--source-resume-md <resume.md>` when reviewing customized resumes to prevent invented main sections.

The final review defaults to `--target-pages 2 --max-pages 2 --min-final-page-fill 0.80` for balanced job-submission resumes.

Manual review checklists:

```text
references/review-checklists.md
```

## Template Guidance

- `classic`: Conservative executive resume with serif typography and strong section rules.
- `executive`: Senior leadership layout with compact spacing, premium typography, and restrained accent color.
- `modern`: Clean technology leadership layout with sans-serif typography and crisp hierarchy.

All templates must remain ATS-friendly: selectable text, conventional section headings, no image-based text, no chart-heavy layout, and no essential content hidden in icons or decorative elements.

For job-submission PDFs, prefer clean visual polish over presentation styling: balanced whitespace, readable compact typography, clear section hierarchy, and no decorative cover page. Keep links as plain selectable text. Avoid icons, complex columns, heavy backgrounds, and slide-like layouts.

In the generated PDF, check that the heading lines are in tact as per template - it should have two lines after name: 1st line showing Email, Phone, Location; followed by 2nd line showing LinkedIn, GitHub and Website URL

If WeasyPrint is unavailable, `scripts/render_resume.py` falls back to a pure-Python PDF renderer with conservative typography, section bands, accent colors, and selectable text. Treat the fallback PDF as acceptable only after `scripts/review_delivery.py` passes.

## Review Gate

Never begin tailoring until the normalized `output/job.md` has been reviewed when the JD came from a URL, unless the user explicitly says to skip that review.

Never deliver the final PDF immediately after the first customized Markdown draft unless the user explicitly says to skip review. The workflow may render a temporary pre-review PDF to check page length, section structure, text extraction, and visual balance before asking the user to review the Markdown.

## Final Delivery Gate

Never deliver a generated PDF without running `scripts/review_delivery.py`. If the report fails because content is clipped, missing, blank, or not text-extractable, correct the issue and rerun both rendering and review.

After automated review passes, pause for the user's final manual PDF inspection. Do not treat an automated `PASS` as final delivery approval.
