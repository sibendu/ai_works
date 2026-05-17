# /// script
# dependencies = []
# ///

"""
Resume Validator — Checks parsed resume JSON for completeness and quality.

Usage:
    python3 scripts/validate_resume.py parsed.json
    python3 scripts/validate_resume.py parsed.json --strict
    python3 scripts/validate_resume.py --help

Exit Codes:
    0 — Validation passed (zero errors, warnings are OK)
    1 — File not found or invalid JSON
    3 — Validation failed (one or more errors)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Action verbs commonly used in strong resume bullets
ACTION_VERBS = {
    'achieved', 'administered', 'analyzed', 'architected', 'automated',
    'built', 'collaborated', 'configured', 'coordinated', 'created',
    'decreased', 'delivered', 'deployed', 'designed', 'developed',
    'directed', 'drove', 'enabled', 'engineered', 'established',
    'executed', 'expanded', 'facilitated', 'grew', 'identified',
    'implemented', 'improved', 'increased', 'initiated', 'integrated',
    'introduced', 'launched', 'led', 'managed', 'maintained',
    'mentored', 'migrated', 'negotiated', 'optimized', 'orchestrated',
    'oversaw', 'partnered', 'pioneered', 'planned', 'presented',
    'published', 'reduced', 'refactored', 'redesigned', 'resolved',
    'scaled', 'secured', 'simplified', 'spearheaded', 'streamlined',
    'supervised', 'supported', 'taught', 'trained', 'transformed',
    'upgraded', 'utilized', 'wrote',
}

REQUIRED_SECTIONS = {'experience', 'education', 'skills'}
RECOMMENDED_SECTIONS = {'summary', 'projects', 'certifications'}

# Characters that commonly break ATS parsers
ATS_PROBLEM_CHARS = re.compile(r'[│┃┆┇┊┋╎╏║═╔╗╚╝╠╣╦╩╬▪▫●◆◇★☆✓✗✦→←↑↓⟶⟵]')


def validate_resume(resume: dict, strict: bool = False) -> dict:
    """Validate a parsed resume and return errors and warnings."""
    errors = []
    warnings = []

    # --- Contact Info ---
    if not resume.get('name'):
        errors.append({
            'field': 'name',
            'message': 'Missing name. Add an H1 heading (# Your Name) at the top of the Markdown.',
        })

    contact = resume.get('contact', {})
    if not contact.get('email'):
        errors.append({
            'field': 'contact.email',
            'message': 'Missing email address. Add it below your name: **Email:** you@example.com',
        })

    if not contact.get('phone'):
        warnings.append({
            'field': 'contact.phone',
            'message': 'No phone number found. Recommended for most job applications.',
        })

    if not contact.get('location'):
        warnings.append({
            'field': 'contact.location',
            'message': 'No location found. Adding City, State helps with local job matching.',
        })

    # --- Sections ---
    section_titles_lower = {s['title'].lower() for s in resume.get('sections', [])}

    for req in REQUIRED_SECTIONS:
        # Fuzzy match: "Work Experience" matches "experience"
        found = any(req in title for title in section_titles_lower)
        if not found:
            errors.append({
                'field': f'sections',
                'message': f'Missing required section: {req.title()}. Add ## {req.title()} to your Markdown.',
            })

    for rec in RECOMMENDED_SECTIONS:
        found = any(rec in title for title in section_titles_lower)
        if not found:
            warnings.append({
                'field': 'sections',
                'message': f'Consider adding a {rec.title()} section to strengthen your resume.',
            })

    # --- Section Content ---
    for section in resume.get('sections', []):
        title = section['title']
        entries = section.get('entries', [])
        content = section.get('content', [])

        if not entries and not content:
            errors.append({
                'field': f'sections.{title}',
                'message': f'Section "{title}" is empty. Add content or remove the heading.',
            })
            continue

        # Check bullets in experience-like sections
        if any(kw in title.lower() for kw in ['experience', 'work']):
            for entry in entries:
                if not entry.get('bullets'):
                    warnings.append({
                        'field': f'sections.{title}.{entry.get("raw", "?")}',
                        'message': f'Entry "{entry.get("title", "?")}" has no bullet points. '
                                   f'Add achievements using "- Led...", "- Built...", etc.',
                    })
                    continue

                for idx, bullet in enumerate(entry.get('bullets', [])):
                    # Check action verb
                    first_word = bullet.split()[0].lower().rstrip('ed').rstrip('s') if bullet.split() else ''
                    first_word_full = bullet.split()[0].lower() if bullet.split() else ''
                    has_action = (
                        first_word_full in ACTION_VERBS or
                        first_word in ACTION_VERBS
                    )
                    if not has_action and strict:
                        warnings.append({
                            'field': f'sections.{title}.bullet[{idx}]',
                            'message': f'Bullet does not start with an action verb: "{bullet[:60]}...". '
                                       f'Consider rewriting to start with Led, Built, Designed, etc.',
                        })

                    # Check length
                    if len(bullet) < 20:
                        warnings.append({
                            'field': f'sections.{title}.bullet[{idx}]',
                            'message': f'Bullet is very short ({len(bullet)} chars): "{bullet}". '
                                       f'Add specific metrics or details.',
                        })
                    elif len(bullet) > 200:
                        warnings.append({
                            'field': f'sections.{title}.bullet[{idx}]',
                            'message': f'Bullet is very long ({len(bullet)} chars). '
                                       f'Consider splitting into two bullets.',
                        })

                # Check dates
                if not entry.get('dates'):
                    warnings.append({
                        'field': f'sections.{title}.{entry.get("raw", "?")}',
                        'message': f'Entry "{entry.get("title", "?")}" has no dates. '
                                   f'Add dates in format: (2020–Present) or (2018–2022).',
                    })

    # --- ATS Compatibility ---
    full_text = json.dumps(resume)
    ats_chars = ATS_PROBLEM_CHARS.findall(full_text)
    if ats_chars:
        unique_chars = list(set(ats_chars))
        warnings.append({
            'field': 'ats',
            'message': f'Found special characters that may break ATS parsers: {unique_chars}. '
                       f'Replace with standard ASCII alternatives.',
        })

    return {
        'status': 'pass' if not errors else 'fail',
        'errors': errors,
        'warnings': warnings,
        'summary': {
            'error_count': len(errors),
            'warning_count': len(warnings),
            'sections_found': [s['title'] for s in resume.get('sections', [])],
            'total_entries': sum(len(s.get('entries', [])) for s in resume.get('sections', [])),
            'total_bullets': sum(
                len(e.get('bullets', []))
                for s in resume.get('sections', [])
                for e in s.get('entries', [])
            ),
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Validate a parsed resume JSON for completeness and quality.',
        epilog='Examples:\n'
               '  python3 scripts/validate_resume.py parsed.json\n'
               '  python3 scripts/validate_resume.py parsed.json --strict\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('input', help='Path to parsed resume JSON file')
    parser.add_argument('--strict', action='store_true',
                        help='Enable strict mode (checks action verbs on every bullet)')
    args = parser.parse_args()

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

    result = validate_resume(resume, strict=args.strict)
    print(json.dumps(result, indent=2))

    if result['status'] == 'fail':
        sys.exit(3)
    sys.exit(0)


if __name__ == '__main__':
    main()
