# /// script
# dependencies = [
#   "weasyprint>=62.0",
#   "jinja2>=3.1",
# ]
# ///

"""
Resume PDF Generator — Renders a parsed resume JSON into a styled PDF.

Usage:
    python3 scripts/generate_pdf.py --input parsed.json --style modern --output resume.pdf
    python3 scripts/generate_pdf.py --input parsed.json --style classic
    python3 scripts/generate_pdf.py --help

Styles: modern, classic, compact

Exit Codes:
    0 — Success
    1 — File not found or read error
    2 — Template not found
    3 — PDF generation error
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from weasyprint import HTML
    from jinja2 import Template
except ImportError:
    print('Error: Missing dependencies. Install with:', file=sys.stderr)
    print('  pip install weasyprint jinja2', file=sys.stderr)
    sys.exit(1)


STYLE_MAP = {
    'modern': 'template_modern.html',
    'classic': 'template_classic.html',
    'compact': 'template_compact.html',
}

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / 'assets'


def load_template(style: str) -> str:
    """Load the HTML template for the given style."""
    filename = STYLE_MAP.get(style)
    if not filename:
        available = ', '.join(STYLE_MAP.keys())
        print(f'Error: Unknown style "{style}". Available styles: {available}', file=sys.stderr)
        sys.exit(2)

    template_path = ASSETS_DIR / filename
    if not template_path.exists():
        print(f'Error: Template not found: {template_path}', file=sys.stderr)
        print(f'       Expected in: {ASSETS_DIR}/', file=sys.stderr)
        sys.exit(2)

    return template_path.read_text(encoding='utf-8')


def render_html(template_str: str, resume: dict) -> str:
    """Render the Jinja2 HTML template with resume data."""
    template = Template(template_str)
    return template.render(resume=resume)


def check_page_overflow(html_content: str, max_pages: int = 2) -> dict:
    """Check if the rendered PDF exceeds the desired page count."""
    doc = HTML(string=html_content).render()
    page_count = len(doc.pages)
    return {
        'page_count': page_count,
        'overflow': page_count > max_pages,
    }


def generate_pdf(html_content: str, output_path: str):
    """Generate the PDF from rendered HTML."""
    try:
        HTML(string=html_content).write_pdf(output_path)
    except Exception as e:
        print(f'Error: PDF generation failed: {e}', file=sys.stderr)
        sys.exit(3)


def main():
    parser = argparse.ArgumentParser(
        description='Generate a professional PDF resume from parsed JSON.',
        epilog='Styles:\n'
               '  modern  — Clean sans-serif, subtle color accents\n'
               '  classic — Traditional serif, conservative layout\n'
               '  compact — Dense layout, smaller margins, more content\n\n'
               'Examples:\n'
               '  python3 scripts/generate_pdf.py --input parsed.json --style modern --output resume.pdf\n'
               '  python3 scripts/generate_pdf.py --input parsed.json --style classic\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', required=True, help='Path to parsed resume JSON')
    parser.add_argument('--style', default='modern', choices=STYLE_MAP.keys(),
                        help='Resume style template (default: modern)')
    parser.add_argument('--output', default='resume.pdf', help='Output PDF path (default: resume.pdf)')
    parser.add_argument('--max-pages', type=int, default=2,
                        help='Warn if PDF exceeds this many pages (default: 2)')
    args = parser.parse_args()

    # Load resume data
    input_path = Path(args.input)
    if not input_path.exists():
        print(f'Error: File not found: {args.input}', file=sys.stderr)
        print(f'       Run parse_resume.py first to generate the JSON.', file=sys.stderr)
        sys.exit(1)

    try:
        resume = json.loads(input_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        print(f'Error: Invalid JSON in {args.input}: {e}', file=sys.stderr)
        sys.exit(1)

    # Load and render template
    template_str = load_template(args.style)
    html_content = render_html(template_str, resume)

    # Check page overflow
    overflow_info = check_page_overflow(html_content, args.max_pages)
    if overflow_info['overflow']:
        print(f'Warning: Resume renders to {overflow_info["page_count"]} pages '
              f'(max recommended: {args.max_pages}). Consider using "compact" style '
              f'or trimming content.', file=sys.stderr)

    # Generate PDF
    generate_pdf(html_content, args.output)

    # Summary output
    result = {
        'status': 'success',
        'output': args.output,
        'style': args.style,
        'pages': overflow_info['page_count'],
        'overflow_warning': overflow_info['overflow'],
    }
    print(json.dumps(result))


if __name__ == '__main__':
    main()
