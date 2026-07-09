# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Repository Overview

**AI Works** is a collection of reusable Codex skills, prompt templates, and utilities for AI-assisted professional workflows. It is **not a traditional software project** with builds, tests, or a deployed application. Instead, it houses:

1. **Reusable skills** (in `.agents/skills/` and `.Codex/skills/`) — Codex extensions that solve specific workflows
2. **Prompt templates** (in `useful_prompts/`) — Markdown prompt guides for professional tasks
3. **Utilities** (in `talktoprompt/`) — Standalone HTML/JS tools for speech-to-prompt conversion

## Python environment
Always use the active venv. Before installing any package, check with:
`python -c "import pkg_name"` — only install if that fails.

## Resume Formatting Standards

When using resume-tailor skill or editing resume_sdas.md:
- **Contact line formatting:** Must have a blank line between the email/phone/location line and the LinkedIn/GitHub/website line. This ensures they render as separate paragraphs in PDF, not merged together. Markdown requires `\n\n` (blank line) to create separate paragraphs, not just `\n`.
