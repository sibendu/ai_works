# Review Checklists

Use these checklists at the two human review gates.

## Job Description Extraction Review

After creating `job.md`, ask the user to check that the extraction captured:

- Role title and level.
- Primary responsibilities.
- Required qualifications.
- Preferred qualifications.
- Technologies, platforms, tools, methodologies, frameworks, and domains.
- Leadership, stakeholder, customer-facing, delivery, product, or management expectations.
- Location, travel, work authorization, or hybrid/remote constraints when role-relevant.

Also ask the user to check that `job.md` removed:

- Headers, navigation, cookie notices, legal boilerplate, unrelated company marketing, unrelated open roles, footer links, and social/share content.

If the user identifies missing or incorrect content, update `job.md` and ask for confirmation before tailoring the resume.

## Final Manual PDF Review

After `scripts/review_delivery.py` completes, ask the user to inspect the PDF manually for:

- Factual accuracy against the approved customized Markdown.
- Correct contact details, links, names, companies, titles, dates, metrics, and technologies.
- No clipped text, distorted text, overlapping content, orphan bullets, blank pages, or awkward page breaks.
- Professional visual polish: spacing, section hierarchy, typography, color, and readability.
- Recruiter scan quality on the first page.
- ATS suitability: selectable text, conventional headings, and no essential content embedded only in images.

If changes are requested, update the customized Markdown and/or template, rerender the PDF, rerun automated review, and request final manual inspection again.
