# /// script
# dependencies = [
#   "markdown-it-py>=3.0",
# ]
# ///

"""
Resume Markdown Parser — Converts a Markdown resume into structured JSON.

Usage:
    python3 scripts/parse_resume.py --input resume.md --output parsed.json
    python3 scripts/parse_resume.py --input resume.md  # prints to stdout
    python3 scripts/parse_resume.py --help

Exit Codes:
    0 — Success
    1 — File not found or read error
    2 — Parse error (invalid Markdown structure)
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_contact_line(line: str) -> dict:
    """Extract contact info from the line(s) below the H1 name."""
    contact = {}
    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
    if email_match:
        contact['email'] = email_match.group()

    phone_match = re.search(r'[\d()+-][\d()\s.+-]{6,}[\d)]', line)
    if phone_match:
        contact['phone'] = phone_match.group().strip()

    # LinkedIn / GitHub / Portfolio URLs
    links = re.findall(r'https?://[^\s|*\]]+', line)
    if links:
        contact['links'] = links

    # Location — typically after "Location:" or as a standalone city, state
    loc_match = re.search(r'(?:Location:\s*\*{0,2}|📍\s*)([^|*\n]+)', line)
    if loc_match:
        contact['location'] = loc_match.group(1).strip()
    else:
        # Try pattern: City, ST or City, State
        loc_match2 = re.search(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s*[A-Z]{2}(?:\s\d{5})?)', line)
        if loc_match2:
            contact['location'] = loc_match2.group(1).strip()

    return contact


def parse_resume_markdown(content: str) -> dict:
    """Parse a Markdown resume into structured JSON."""
    lines = content.strip().split('\n')
    resume = {
        'name': '',
        'contact': {},
        'sections': []
    }

    current_section = None
    current_entry = None
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # H1 — Name
        if line.startswith('# ') and not line.startswith('## '):
            resume['name'] = line[2:].strip()
            # Next non-empty lines before next heading are contact info
            contact_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('#'):
                if lines[i].strip():
                    contact_lines.append(lines[i].strip())
                i += 1
            if contact_lines:
                contact_text = ' '.join(contact_lines)
                # Clean markdown bold markers
                contact_text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', contact_text)
                resume['contact'] = parse_contact_line(contact_text)
            continue

        # H2 — Section
        elif line.startswith('## '):
            section_name = line[3:].strip()
            current_section = {
                'title': section_name,
                'entries': [],
                'content': []
            }
            resume['sections'].append(current_section)
            current_entry = None
            i += 1
            continue

        # H3 — Entry within a section
        elif line.startswith('### '):
            if current_section is None:
                i += 1
                continue
            entry_text = line[4:].strip()
            # Parse pattern: Title — Organization (Date)
            entry = {'raw': entry_text, 'bullets': []}
            # Try: Role — Company (Date)
            match = re.match(
                r'(.+?)\s*[—–-]\s*(.+?)\s*\((\d{4}\s*[—–-]\s*(?:\d{4}|[Pp]resent))\)',
                entry_text
            )
            if match:
                entry['title'] = match.group(1).strip()
                entry['organization'] = match.group(2).strip()
                entry['dates'] = match.group(3).strip()
            else:
                # Try: Degree, Institution (Year)
                match2 = re.match(r'(.+?)\s*[—–-]\s*(.+?)\s*\((\d{4})\)', entry_text)
                if match2:
                    entry['title'] = match2.group(1).strip()
                    entry['organization'] = match2.group(2).strip()
                    entry['dates'] = match2.group(3).strip()
                else:
                    entry['title'] = entry_text

            current_entry = entry
            current_section['entries'].append(entry)
            i += 1
            continue

        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            bullet_text = line[2:].strip()
            # Clean markdown formatting
            bullet_text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', bullet_text)
            if current_entry:
                current_entry['bullets'].append(bullet_text)
            elif current_section:
                current_section['content'].append(bullet_text)
            i += 1
            continue

        # Plain text content within a section
        elif line and current_section and not current_entry:
            # Clean markdown formatting
            clean = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', line)
            current_section['content'].append(clean)
            i += 1
            continue

        else:
            i += 1
            continue

    return resume


def main():
    parser = argparse.ArgumentParser(
        description='Parse a Markdown resume into structured JSON.',
        epilog='Examples:\n'
               '  python3 scripts/parse_resume.py --input resume.md --output parsed.json\n'
               '  python3 scripts/parse_resume.py --input resume.md\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', required=True, help='Path to Markdown resume file')
    parser.add_argument('--output', help='Output JSON file path (default: stdout)')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f'Error: File not found: {args.input}', file=sys.stderr)
        print(f'       Check the path and try again.', file=sys.stderr)
        sys.exit(1)

    try:
        content = input_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f'Error: Could not read {args.input}: {e}', file=sys.stderr)
        sys.exit(1)

    if not content.strip():
        print(f'Error: File is empty: {args.input}', file=sys.stderr)
        sys.exit(1)

    try:
        resume = parse_resume_markdown(content)
    except Exception as e:
        print(f'Error: Failed to parse Markdown: {e}', file=sys.stderr)
        sys.exit(2)

    output_json = json.dumps(resume, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output_json, encoding='utf-8')
        print(f'Parsed resume written to {args.output}', file=sys.stderr)
        # Summary to stdout for the agent
        section_names = [s['title'] for s in resume['sections']]
        print(json.dumps({
            'status': 'success',
            'name': resume['name'],
            'sections_found': section_names,
            'total_entries': sum(len(s['entries']) for s in resume['sections'])
        }))
    else:
        print(output_json)


if __name__ == '__main__':
    main()
