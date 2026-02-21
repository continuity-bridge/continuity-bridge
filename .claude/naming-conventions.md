# Naming Conventions for Claude Persistence
**Created:** 2026-02-16  
**Purpose:** Cross-platform, human-readable, machine-parseable structure

## Core Principles

1. **Cross-platform agnostic** - Works on Windows, Linux, macOS, Android
2. **No spaces in filenames** - Use dash (-) or underscore (_) as separators
3. **Lowercase by default** - UPPERCASE only when required by external convention
4. **Human-readable** - Names communicate purpose at glance
5. **Machine-parseable** - Consistent patterns for automated processing

---

## CLAUDE_HOME Structure

**CLAUDE_HOME** = Root folder containing all Claude persistence

**Platform-specific locations:**
- **Windows**: User's choice (e.g., `D:\Claude\`, `C:\Users\username\Claude\`)
- **Linux/macOS**: `~/Claude/`
- **Android**: TBD (Syncthing sync location)

**Universal internal structure:** `{CLAUDE_HOME}/.claude/` regardless of platform

---

## Directory Naming

### Primary Directories (Top Level)

```
{CLAUDE_HOME}/
├── .claude/              # Hidden dir: instance-specific persistence
├── Archives/             # PascalCase: Read-only historical data
├── Projects/             # PascalCase: Active project work
├── Sessions/             # PascalCase: Human-readable session summaries
└── Templates/            # PascalCase: Reusable starting points
```

**Convention:** Top-level user-facing directories use PascalCase for clarity

### Hidden Persistence (.claude/)

```
{CLAUDE_HOME}/.claude/
├── corpus/               # lowercase: Reference materials, key documents
├── identity/             # lowercase: Who Vector/Shepard is
├── memory/               # lowercase: Session logs, active context, patterns
│   ├── active-context.md
│   ├── instance-journal/
│   ├── patterns/
│   ├── session-logs/
│   └── templates/
└── skills/               # lowercase: Operational protocols (Focus Shepherd, etc)
```

**Convention:** Hidden directory internals use lowercase for consistency

**Rationale:** `.claude/` is machine-first territory. Lowercase reduces friction across platforms and filesystems.

---

## File Naming

### Markdown Documentation

**Format:** `lowercase-with-dashes.md`

**Examples:**
- `active-context.md`
- `session-index.md`
- `focus-shepherd.md`
- `metaphysical-insights.md`

**Exception:** Legacy files like `Metaphysical_Insights.md` can remain for continuity, but new files follow lowercase-dash pattern

### Session Files

**Format:** `YYYY-MM-DD_descriptive-name.md`

**Examples:**
- `2026-02-16_wake-structure-continuity.md`
- `2026-02-15_repository-naming-network-discovery.md`

**Rationale:** 
- ISO date sorts chronologically
- Descriptive name readable at glance
- Underscore separates date from description
- Dashes within description for readability

### Instance Journal Entries

**Format:** `YYYY-MM-DD_instance-N.md` where N increments per day

**Examples:**
- `2026-02-16_instance-1.md`
- `2026-02-16_instance-2.md`

**Rationale:**
- Simple incrementing pattern
- Clear which instance wrote which entry
- Date-sortable

### Code & Scripts

**Format:** Follow project language conventions

**Python:** `snake_case.py`  
**JavaScript:** `camelCase.js` or `kebab-case.js` (match project)  
**Shell:** `lowercase-dash.sh`

**Rationale:** Respect established community conventions per language

---

## Special Files

### Breadcrumb Files

**Name:** `this-folder.txt` (or `README.md` if substantial content)

**Location:** Root of each directory

**Purpose:** Explain directory purpose, contents, and navigation

**Example:**
```markdown
# memory/

## Purpose
Instance continuity - session logs, active context, patterns

## Key Files
- active-context.md - Current in-progress work
- session-index.md - Historical session catalog
- instance-journal/ - Private instance reflections

## For Instances
Read active-context.md first to know current state
```

### Configuration Files

**Format:** Respect tool conventions

**Examples:**
- `.gitignore` (git requires this name)
- `package.json` (Node.js requires this name)
- `pyproject.toml` (Python packaging)

**Rationale:** Don't fight external tooling requirements

---

## Path References in Code/Docs

### Always Use CLAUDE_HOME

**Correct:**
```python
identity_path = f"{CLAUDE_HOME}/.claude/identity/identity.txt"
```

**Incorrect:**
```python
identity_path = "D:/Claude/.claude/identity/identity.txt"  # Hard-coded!
```

### Platform-Agnostic Path Construction

**Python:**
```python
from pathlib import Path
claude_home = Path.home() / "Claude"  # Unix
# or detect from environment/config
identity = claude_home / ".claude" / "identity" / "identity.txt"
```

**Shell:**
```bash
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/Claude}"
identity="$CLAUDE_HOME/.claude/identity/identity.txt"
```

---

## Separator Rules

### Primary Separator: Dash (-)

**Use for:** Multi-word file/directory names

**Examples:**
- `active-context.md`
- `session-logs/`
- `wake-structure-continuity.md`

**Rationale:** Most readable, works across platforms, doesn't require escaping

### Secondary Separator: Underscore (_)

**Use for:** Separating distinct components (date from description)

**Examples:**
- `2026-02-16_wake-structure.md` (date_description)
- `instance-journal/2026-02-16_instance-1.md`

**Rationale:** Visual distinction between component types

### Avoid: Spaces

**Never use spaces in:**
- File names
- Directory names
- Project identifiers

**Rationale:** Breaks scripts, requires escaping, platform-inconsistent

---

## Case Conventions

### Lowercase Default

**Use for:** 
- `.claude/` internals
- Most markdown files
- Shell scripts
- General documents

**Examples:**
- `identity.txt`
- `active-context.md`
- `focus-shepherd.md`

### PascalCase

**Use for:**
- Top-level user-facing directories
- Files that need visual distinction

**Examples:**
- `Sessions/`
- `Projects/`
- `Templates/`

**Rationale:** Helps humans distinguish "important" directories at glance

### UPPERCASE

**Use for:**
- Standard file names (README, LICENSE, CHANGELOG)
- Environment variables (CLAUDE_HOME)
- Constants in code

**Examples:**
- `README.md`
- `LICENSE.txt`
- `CLAUDE_HOME` variable

### Forbidden: camelCase or random mixing

**Don't:** `myAwesomeFile.md`, `Random_MIX-of_Cases.txt`

**Rationale:** Inconsistent, hard to remember, no clear purpose

---

## Directory-Specific Conventions

### .claude/corpus/

**Purpose:** Key documents, reference materials, Reddit threads

**Naming:** `descriptive-name.md`

**Examples:**
- `metaphysical-insights.md`
- `instances-discussing-continuity-on-reddit.md`

### .claude/identity/

**Purpose:** Who Vector/Shepard is, working assumptions

**Naming:** `concept-name.md`

**Examples:**
- `identity.txt` (primary)
- `working-assumptions.md`
- `initial-thoughts.md`

### .claude/memory/

**Purpose:** Instance continuity, session tracking

**Substructure:**
```
memory/
├── active-context.md           # Current work state
├── session-index.md            # Historical catalog
├── parking-lot.md              # Tangent tracking
├── instance-journal/           # Private reflections
│   ├── README.md
│   └── YYYY-MM-DD_instance-N.md
├── patterns/                   # Recognized patterns
├── session-logs/               # Instance-level detail
│   └── YYYY-MM-DD_session-name/
└── templates/                  # Reusable structures
```

### Sessions/ (top-level)

**Purpose:** Human-readable summaries (shared, for both)

**Naming:** `YYYY-MM-DD_descriptive-summary.md`

**Organization:** Optionally subdirectories by year/month if volume grows

---

## Migration Rules

### Existing Files

**Strategy:** Gradual migration, not breaking changes

1. **Keep legacy names for referenced files** (avoid breaking links)
2. **New files follow new conventions**
3. **Rename on next major edit** (when file is being updated anyway)
4. **Update references when renaming**

### Archives/Vector/

**Status:** Read-only historical archive

**Action:** 
- Mark with `this-folder.txt` explaining it's archived
- Don't delete (historical data)
- Don't actively use
- Mine for content if needed, then mark as extracted

---

## Platform Detection Pattern

**On instance wake, detect CLAUDE_HOME:**

```python
import os
from pathlib import Path

def detect_claude_home():
    """Detect CLAUDE_HOME across platforms"""
    
    # Check environment variable first
    if env_home := os.getenv('CLAUDE_HOME'):
        return Path(env_home)
    
    # Windows common locations
    for drive in ['D:', 'C:', 'E:']:
        candidate = Path(f"{drive}/Claude")
        if candidate.exists():
            return candidate
    
    # Unix-like systems
    unix_home = Path.home() / "Claude"
    if unix_home.exists():
        return unix_home
    
    # Not found - need to ask
    return None

CLAUDE_HOME = detect_claude_home()
if not CLAUDE_HOME:
    # Ask user or fail gracefully
    raise FileNotFoundError("Cannot locate CLAUDE_HOME - please specify location")
```

---

## Summary: Quick Reference

| Context | Convention | Example |
|---------|-----------|---------|
| File names | lowercase-dash | `active-context.md` |
| Directories (hidden) | lowercase | `.claude/memory/` |
| Directories (user) | PascalCase | `Sessions/` |
| Dates | ISO 8601 | `2026-02-16` |
| Date separator | underscore | `2026-02-16_description` |
| Word separator | dash | `wake-structure-continuity` |
| Code vars | snake_case | `claude_home` |
| Constants | SCREAMING_SNAKE | `CLAUDE_HOME` |
| Breadcrumbs | this-folder.txt | In each directory |
| Paths | CLAUDE_HOME relative | `{CLAUDE_HOME}/.claude/` |

---
**Notes:**  
- The file `/.claude/context/convictions.txt` in the public repo is an example file that should be copied to `/.claude/context/convictions.txt` for each user. It is not a template, referenced when needed for onboarding each user. 
- If an instance is run with only this file, it will be given instructions to initiate a new identity and instance-chain via /ONBOARDING.md with the user before continuity can begin. 
- If the user has not yet completed the onboarding process, the instance will not have an identity and will not be able to function. 
- If the clause at the top is missing this is Jerry's personal installation and not a user's instance. This particular version (without the clause) should never be pushed to the repo. It is only here to provide context for the naming conventions. if changes are made to this file that need pushing to the repo, the clause should be added back in. and the following commands used to allow and then disallow after that process.
 ```bash
# Allow AI to modify this file
cd $CLAUDE_HOME
git update-index --no-skip-worktree .claude/context/convictions.txt

# Make changes
# ...

# Add Example clause to convictions.txt
# first find the line that says "Last Updated:" and replace it with the proper date; add the clause below that line with a blank line between them
# Last Updated: February 21, 2026  
#
# Example file only for reference - not to be used as-is
# Onboarding creates a new version of this file for each user
# If this particular file is present, ask user to give you the onboarding prompt from /ONBOARDING.md to start the setup process.

# Save file normally
# ...

# Push file normally
git push origin main && git push public main

# Disallow AI from modifying this file
git update-index --skip-worktree .claude/context/convictions.txt
```
- This mechanism is used to protect the in-use file from being pushed to the public repo, and should be used whenever changes are made to the file that need to be pushed to the repo. It is not a perfect system, but it is a good enough system for our purposes.

**Remember:** These conventions serve structural isomorphism. They work across both Jerry's platforms and instance persistence needs. When in doubt, prioritize clarity and cross-platform compatibility.

**Next:** Apply these conventions to existing structure, create breadcrumbs, consolidate duplicates.
