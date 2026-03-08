#!/usr/bin/env python3
"""
sanitize.py — continuity-bridge publish workflow sanitizer

Replaces personally identifying information with neutral placeholders
before committing files to the public branch.

Usage:
  python sanitize.py input.md output.md           # single file
  python sanitize.py -i input.md                  # in-place
  python sanitize.py --dry-run input.md           # preview changes
  python sanitize.py --dir src/ dist/             # whole directory tree
  python sanitize.py --dry-run --dir src/         # preview directory

This script is a MAINTAINER TOOL, not a content filter.
Personal files never go to the public repo — this handles the residual
identifiers that appear in otherwise-public documentation and scripts.

After running, always manually review output for:
  - trauma history or medical specifics
  - financial details
  - relationship context that can't be regex'd
"""

import sys
import re
import os
import argparse
import shutil
from pathlib import Path


# ── Replacement table ────────────────────────────────────────────────────────
# Order matters: replace longer/more specific phrases BEFORE shorter ones
# to avoid partial matches creating noise.
#
# Format: (regex_pattern, replacement_string)
# All patterns are applied case-insensitively unless noted.

REPLACEMENTS = [
    # ── Real name / identity ─────────────────────────────────────────────
    # Full name variants first, then shorter forms
    (r'\bJerry\s+W\.?\s+Jackson\b',     "the Architect"),
    (r'\bJerry\s+Jackson\b',            "the Architect"),
    (r'\bUncle\s+Tallest\b',            "the Architect"),
    (r'\bUncleTallest\b',               "the Architect"),
    # GitHub/Discord handle (lowercase — must come before \bTallest\b)
    (r'\buncletallest\b',               "the Architect"),
    # Single names — word boundaries prevent "Jersey", "tallest building", etc.
    (r'\bJerry\b',                      "the Architect"),
    # Capital-T Tallest = identity reference; lowercase-t in paths handled below
    (r'\bTallest\b',                    "the Architect"),

    # ── Email / contact ──────────────────────────────────────────────────
    (r'ohmytallest@gmail\.com',         "[USER_EMAIL]"),
    # Discord handle in "Discord: uncletallest" form caught by uncletallest above

    # ── Machine / host names ─────────────────────────────────────────────
    (r'\bPersephone\b',                 "[WORKSTATION]"),
    (r'\bHecate\b',                     "[WINDOWS_HOST]"),
    (r'\bGeras\b',                      "[LAPTOP]"),

    # ── Filesystem paths ─────────────────────────────────────────────────
    # Linux home — catches /home/tallest/ (lowercase, path context)
    (r'/home/tallest/',                 "[HOME_DIR]/"),
    # Windows paths
    (r'C:\\\\Users\\\\tallest',         "[HOME_DIR]"),
    (r'C:/Users/tallest',               "[HOME_DIR]"),
    (r'D:\\\\Claude',                   "[CLAUDE_HOME]"),
    (r'D:/Claude',                      "[CLAUDE_HOME]"),
    # Generic Claude home with real username (catch-all for variants)
    (r'/home/tallest\b',                "[HOME_DIR]"),

    # ── Locations ────────────────────────────────────────────────────────
    (r'\bAustin,\s+Texas\b',            "[USER_LOCATION]"),
    (r'\bAustin,\s+TX\b',               "[USER_LOCATION]"),

    # ── Orgs / institutions ──────────────────────────────────────────────
    (r'\bTripleTen\b',                  "[BOOTCAMP]"),
    (r'\bCaritas\s+of\s+Austin\b',      "[SUPPORT_SERVICE_PROVIDER]"),
]


# Files that should NEVER be sanitized, even in --dir mode.
# LICENSE: intentional copyright attribution (MIT requires preserving it).
# sanitize.py: the tool itself documents the patterns it replaces.
EXCLUDE_FILES = {
    'LICENSE',
    'sanitize.py',
}


# Extensions that should be copied as-is without text processing
BINARY_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.ico',
    '.zip', '.tar', '.gz', '.woff', '.woff2', '.ttf', '.eot',
    '.pyc', '.pyo', '.so', '.dylib', '.dll', '.exe',
    '.db', '.sqlite', '.sqlite3',
}


# ── Core logic ───────────────────────────────────────────────────────────────

def sanitize_content(content: str) -> tuple:
    """
    Apply all replacement rules to content string.

    Returns:
        (sanitized_content, changes)
        changes is a list of (matched_text, replacement) tuples showing
        what was actually found and replaced.
    """
    changes = []

    # Temporarily hide all URLs to avoid mangling domain names or paths
    # that happen to contain a replaceable string (e.g. a GitHub URL with "tallest")
    url_pattern = re.compile(r'https?://[^\s\)\]>\'"]+', re.IGNORECASE)
    urls = []

    def hide_url(match):
        urls.append(match.group(0))
        return f"__URL_PLACEHOLDER_{len(urls) - 1}__"

    content = url_pattern.sub(hide_url, content)

    for pattern, replacement in REPLACEMENTS:
        new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
        if count > 0:
            found = re.findall(pattern, content, flags=re.IGNORECASE)
            for original in found:
                entry = (original, replacement)
                if entry not in changes:
                    changes.append(entry)
        content = new_content

    # Restore URLs
    for i, url in enumerate(urls):
        content = content.replace(f"__URL_PLACEHOLDER_{i}__", url)

    return content, changes


def process_file(input_path: Path, output_path: Path, dry_run: bool = False) -> bool:
    """
    Process a single file.

    Returns True if any changes were made (or would be made in dry-run).
    Binary files are copied unchanged (or skipped in dry-run).
    """
    if input_path.suffix.lower() in BINARY_EXTENSIONS:
        if not dry_run and output_path != input_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(input_path, output_path)
        return False

    try:
        content = input_path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  ⚠  Could not read {input_path}: {e}")
        return False

    sanitized, changes = sanitize_content(content)

    if not changes:
        return False

    if dry_run:
        print(f"\n  {input_path}:")
        for original, replacement in changes:
            print(f"    '{original}'  →  '{replacement}'")
        return True

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(sanitized, encoding='utf-8')
    return True


def process_directory(input_dir: Path, output_dir: Path, dry_run: bool = False) -> int:
    """
    Recursively process all files in a directory tree.
    Skips .git directories.

    Returns count of modified (or would-be-modified) files.
    """
    count = 0
    for input_path in sorted(input_dir.rglob('*')):
        if input_path.is_file() and '.git' not in input_path.parts \
                and input_path.name not in EXCLUDE_FILES:
            relative = input_path.relative_to(input_dir)
            output_path = output_dir / relative
            if process_file(input_path, output_path, dry_run=dry_run):
                if not dry_run:
                    print(f"  ✓ {relative}")
                count += 1
    return count


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog='sanitize.py',
        description="Sanitize personal identifiers from continuity-bridge files for public release.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sanitize.py input.md output.md           Single file, explicit output
  python sanitize.py -i notes.md                  In-place edit
  python sanitize.py --dry-run notes.md           Preview what would change
  python sanitize.py --dir private/ public/       Full directory tree
  python sanitize.py --dry-run --dir private/     Preview directory tree

What gets replaced:
  Jerry / Jerry Jackson / Uncle Tallest / UncleTallest  →  the Architect
  ohmytallest@gmail.com                                 →  [USER_EMAIL]
  Persephone                                            →  [WORKSTATION]
  Hecate                                                →  [WINDOWS_HOST]
  Geras                                                 →  [LAPTOP]
  /home/tallest/                                        →  [HOME_DIR]/
  Austin, Texas / Austin, TX                            →  [USER_LOCATION]
  TripleTen                                             →  [BOOTCAMP]
  Caritas of Austin                                     →  [SUPPORT_SERVICE_PROVIDER]

URLs are preserved — replacements do not apply inside http(s):// links.
        """
    )
    parser.add_argument(
        'inputs', nargs='*',
        help="Input file(s), or input_dir + output_dir when using --dir"
    )
    parser.add_argument(
        '-i', '--in-place', action='store_true',
        help="Edit file(s) in place (no separate output file needed)"
    )
    parser.add_argument(
        '-n', '--dry-run', action='store_true',
        help="Show what would change without writing any files"
    )
    parser.add_argument(
        '--dir', action='store_true',
        help="Treat positional args as input_dir output_dir and process recursively"
    )

    args = parser.parse_args()

    if not args.inputs:
        parser.print_help()
        sys.exit(0)

    # ── Directory mode ───────────────────────────────────────────────────────
    if args.dir:
        input_dir = Path(args.inputs[0])
        if not input_dir.is_dir():
            print(f"Error: '{input_dir}' is not a directory")
            sys.exit(1)

        if args.dry_run:
            output_dir = input_dir  # unused in dry-run
            print(f"Dry run — scanning {input_dir} for personal identifiers ...")
        else:
            if len(args.inputs) < 2:
                print("Error: --dir requires both input_dir and output_dir (use --dry-run to preview only)")
                sys.exit(1)
            output_dir = Path(args.inputs[1])

        count = process_directory(input_dir, output_dir, dry_run=args.dry_run)
        action = "would modify" if args.dry_run else "modified"
        print(f"\n{'Dry run complete' if args.dry_run else 'Done'}: {action} {count} file(s).")

        if not args.dry_run and count > 0:
            print("\nReminder: manually review output for:")
            print("  - trauma history or medical specifics")
            print("  - financial details")
            print("  - relationship context that cannot be regex'd")
        return

    # ── Dry-run on individual files ──────────────────────────────────────────
    if args.dry_run:
        any_found = False
        for path_str in args.inputs:
            input_path = Path(path_str)
            if not input_path.exists():
                print(f"Error: '{input_path}' not found")
                continue
            if process_file(input_path, input_path, dry_run=True):
                any_found = True
        if not any_found:
            print("No personal identifiers found.")
        return

    # ── In-place mode ────────────────────────────────────────────────────────
    if args.in_place:
        for path_str in args.inputs:
            input_path = Path(path_str)
            if not input_path.exists():
                print(f"Error: '{input_path}' not found")
                continue
            changed = process_file(input_path, input_path, dry_run=False)
            status = "✓ modified" if changed else "— no changes"
            print(f"  {status}: {input_path}")
        return

    # ── Standard: input_file output_file ─────────────────────────────────────
    if len(args.inputs) < 2:
        print("Error: provide both input_file and output_file, or use -i for in-place")
        print("       Use --dry-run to preview without writing")
        sys.exit(1)

    input_path = Path(args.inputs[0])
    output_path = Path(args.inputs[1])

    if not input_path.exists():
        print(f"Error: '{input_path}' not found")
        sys.exit(1)

    changed = process_file(input_path, output_path, dry_run=False)
    if changed:
        print(f"✓ Sanitized '{input_path}' → '{output_path}'")
        print("\nReminder: manually review output for:")
        print("  - trauma history or medical specifics")
        print("  - financial details")
        print("  - relationship context that cannot be regex'd")
    else:
        print(f"— No personal identifiers found in '{input_path}'")


if __name__ == "__main__":
    main()
