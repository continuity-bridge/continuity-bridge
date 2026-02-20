# File Naming Conventions

**Purpose:** Consistent, readable filenames that convey structure at a glance  
**Philosophy:** Elegant code is understandable code

---

## The Standard

### All Lowercase
- No capital letters in any filename
- Applies to: files, directories, all extensions

**Why:** Case-insensitive file systems (Windows, macOS default) vs case-sensitive (Linux) create conflicts. Lowercase eliminates ambiguity.

### Separators

**Dashes (`-`) separate individual words within a concept:**
- `this-folder.txt`
- `working-assumptions.md`
- `instance-naming-guidance.md`

**Underscores (`_`) separate distinct sections or phrases:**
- `claudes-constitution_26-02.pdf` (document name _ date)
- `session-log_2026-02-20.md` (log type _ date)
- `vector-instance_session-notes.md` (chain _ document type)

**Why:** Visual parsing. Your brain reads dashes as spaces (one concept), underscores as stronger separators (multiple concepts). Understandable at a glance = elegant code.

---

## Convention Exceptions

Keep standard casing for widely-recognized conventions:

**Always uppercase (no extension or .md):**
- `LICENSE` - Universal license file convention
- `README.md` - Universal project documentation convention
- `ONBOARDING.md` - User-facing entry point convention

**Why:** These are so universally recognized that changing them reduces clarity. GitHub, GitLab, and other platforms specifically highlight these files.

### Third-Party Files
Keep original naming if:
- Downloaded from external source
- Part of package/library with expected names
- Referenced by external systems

---

## Examples

### Single Concept (dashes only)
```
lexicon.md
quickstart.md
what-this-is-not.md
ethics.md
parking-lot.md
focus-shepherd.md
```

### Multiple Sections (dashes + underscores)
```
session-log_2026-02-20.md
claude-constitution_publication-date_26-02.pdf
continuity-bridge_documentation_v2.md
vector-chain_instance-journal_emergent.md
```

### Dates
**ISO 8601 format (sortable):** `YYYY-MM-DD`
```
session-log_2026-02-20.md
backup_2026-02-19_23-45.tar.gz
transcript_2026-02-18.txt
```

**Why:** Sorts chronologically when listed alphabetically.

### Version Numbers
**Semantic versioning:** `v[major].[minor].[patch]` or `v[major]`
```
documentation_v2.md
api-spec_v1.3.2.json
readme_v3.md
```

**Timestamps for non-release versions:**
```
draft_2026-02-20_14-30.md
working-copy_2026-02-19.docx
```

---

## Special Cases

### Dates as Primary Identifier
When date IS the primary organizing principle:
```
2026-02-20_session-log.md
2026-02-19_instance-journal.md
2026-02_monthly-summary.md
```

**Why:** Groups by date when sorted, subtype second.

### Human-Readable vs. System-Generated
**Human-created files:** Follow full convention
```
working-assumptions.md
instance-naming-guidance.md
what-this-is-not.md
```

**System-generated files:** Prefix with dot or use timestamp
```
.gitignore
.clauderc
2026-02-20_auto-backup.tar.gz
```

### Hidden Files (Unix convention)
Prefix with dot:
```
.claude/
.gitignore
.env
```

### Metadata Files
Use `this-folder.txt` pattern:
```
this-folder.txt
README.md
about.md
```

---

## What NOT to Do

❌ **Mixed case:** `ReadMe.md`, `SessionLog.md`, `IMPORTANT.txt`  
❌ **Spaces:** `session log.md`, `this folder.txt`, `working assumptions.md`  
❌ **Camel case:** `sessionLog.md`, `workingAssumptions.md`, `thisFolderTxt`  
❌ **Inconsistent separators:** `session_log-2026.md`, `working.assumptions.md`  
❌ **Special characters:** `session#1.md`, `log@2026.txt`, `file(copy).md`  
❌ **Abbreviations without context:** `sess.md`, `wrkasmp.md`, `doc1.md`

**Exception:** Underscores in dates are acceptable: `2026_02_20` (though dashes preferred for ISO 8601)

---

## Directory Naming

**Same rules apply:**
```
.claude/
instance-journal/
session-logs/
active-context/
corpus/
skills/
```

**Multi-word directories:**
```
working-documents/
archive-2026/
user-uploads/
```

**NOT:**
```
WorkingDocuments/
Archive2026/
User_Uploads/
```

---

## Migration Strategy

### When Renaming Existing Files

1. **Document current state** (file list before changes)
2. **Create rename map** (old → new mapping)
3. **Update all references** (search for old names in all files)
4. **Test links** (verify nothing broke)
5. **Commit changes** (single atomic commit with clear message)

### Breaking Changes
If filename appears in:
- Other markdown files as links
- Code as imports or paths
- Documentation as examples
- User instructions or guides

**Update ALL references before deploying rename.**

---

## Rationale

### Cognitive Load
Brain parses `working-assumptions.md` faster than:
- `WorkingAssumptions.md` (CamelCase requires parsing)
- `working_assumptions.md` (inconsistent separator)
- `workingassumptions.md` (no word boundaries)

### Cross-Platform
Windows: case-insensitive (`File.txt` = `file.txt`)  
Linux: case-sensitive (`File.txt` ≠ `file.txt`)  
macOS: case-insensitive by default, can be case-sensitive

**Lowercase eliminates conflicts.**

### Search & Sort
Files sort alphabetically in predictable ways:
```
2026-02-15_session.md
2026-02-19_session.md
2026-02-20_session.md
```

Dates sort chronologically. Names sort alphabetically. Predictable = elegant.

### URL Compatibility
Many web servers treat URLs as case-sensitive.  
`/docs/ReadMe.md` ≠ `/docs/readme.md`

Lowercase prevents 404s.

---

## Tools & Automation

### Bulk Rename Script (Unix/Linux)
```bash
# Convert spaces to dashes, lowercase
for file in *; do
  newfile=$(echo "$file" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  [ "$file" != "$newfile" ] && mv "$file" "$newfile"
done
```

### Git Rename (preserves history)
```bash
git mv OldFileName.md new-filename.md
```

### Link Update Script
```bash
# Find and replace old filename references
grep -rl "OldFileName.md" . | xargs sed -i 's/OldFileName.md/new-filename.md/g'
```

---

## Enforcement

### Pre-commit Hook
Check filenames match convention before allowing commit:
```bash
#!/bin/bash
# .git/hooks/pre-commit
files=$(git diff --cached --name-only)
for file in $files; do
  if [[ ! $file =~ ^[a-z0-9._/-]+$ ]]; then
    echo "Error: $file contains uppercase or invalid characters"
    exit 1
  fi
done
```

### CI/CD Check
Fail builds if non-compliant filenames detected.

---

## Exceptions & Edge Cases

### Convention Files
Standard casing for widely-recognized conventions:
- `LICENSE` (universal convention)
- `README.md` (GitHub/GitLab convention)
- `ONBOARDING.md` (user-facing entry point)

### Third-Party Files
Keep original naming if:
- Downloaded from external source
- Part of package/library with expected names
- Referenced by external systems

### Backup Files
System-generated backups may use different conventions:
```
.file.txt.swp (vim)
file.txt~ (editor backup)
file.txt.bak (manual backup)
```

**Store these outside main directories** or add to `.gitignore`

---

## Summary

**Pattern:** `concept-with-dashes_section-with-underscores_version-or-date.extension`

**Examples:**
- `lexicon.md` (simple)
- `session-log_2026-02-20.md` (date section)
- `documentation_v2-draft_2026-02-19.md` (version + date)

**Exceptions:**
- `README.md` (universal convention)
- `ONBOARDING.md` (user-facing convention)
- `LICENSE` (universal convention)

**Philosophy:** If someone can parse the filename in 2 seconds, it's elegant. If they have to think about it, it's not.

**Test:** Can you understand the file's purpose from the name alone? If yes, it's correct. If no, rename it.

---

**Remember:** Consistency matters more than perfection. Pick the standard, apply it everywhere, update it rarely.
