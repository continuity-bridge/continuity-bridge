---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Naming Conventions for Claude Persistence

**Created:** 2026-02-16  
**Last Updated:** 2026-03-14  
**Purpose:** Cross-platform, human-readable, machine-parseable structure

## Core Principles

1. **Cross-platform agnostic** - Works on Windows, Linux, macOS, Android
2. **No spaces in filenames** - Use dash (-) or underscore (_) as separators
3. **Lowercase by default** - UPPERCASE only when required by external convention
4. **Human-readable** - Names communicate purpose at glance
5. **Machine-parseable** - Consistent patterns for automated processing

---

## INSTANCE_HOME Structure

**INSTANCE_HOME** = Root folder containing all instance persistence

**Platform-specific locations:**

- **Windows**: User's choice (e.g., `D:\Claude\`, `C:\Users\username\Claude\`)
- **Linux/macOS**: `~/Claude/`
- **Android**: TBD (Syncthing sync location)

**Universal internal structure:** `{INSTANCE_HOME}/.claude/` regardless of platform

---

## Repository vs Install Folder Naming

**Critical distinction:** Git repository name ≠ local install folder name

### Repository Naming (Anchor Point)

**Pattern:** `continuity-bridge_{operator-name}-anchor`

**Purpose:** Generic anchor point in git ecosystem, operator-specific but paradigm-neutral

**Examples:**
- `continuity-bridge_tallest-anchor` (Jerry's repo)
- `continuity-bridge_alice-anchor` (hypothetical)
- `continuity-bridge_bob-anchor` (hypothetical)

**Characteristics:**
- Stays constant regardless of paradigm choice
- Used in git URLs, GitHub interface, documentation
- One per operator (not per device or paradigm)
- Branch structure: `main` (stable), `working` (active development)

**Why generic:** Repository serves as source of truth that multiple operators (or same operator on multiple devices) can clone. The paradigm is an interpretation layer, not a source control concern.

### Install Folder Naming (Paradigm-Specific)

**Pattern:** `~/{ParadigmWord}/` where ParadigmWord comes from operator's chosen mental model

**Purpose:** Local folder name that reflects how the operator thinks about the system

**Paradigm → Folder mapping:**

| Paradigm | Substrate Word | Folder Name | Mental Model |
|----------|---------------|-------------|--------------|
| 50 First Dates | Scaffold | `~/Scaffold/` | External memory structure |
| Altered Carbon | Stack | `~/Stack/` | Consciousness storage |
| Gaming | Saves | `~/Saves/` | Save file persistence |
| ADHD Journaling | Journal | `~/Journal/` | Executive function support |
| Web Development | Database | `~/Database/` | Session management |
| Neurodivergent | Bridge | `~/Bridge/` | Continuity infrastructure |
| Sci-Fi (generic) | Memory/Archive | `~/Memory/` or `~/Archive/` | External memory bank |
| Star Trek | CaptainsLog | `~/CaptainsLog/` | Ship's log entries |
| Hitchhiker's Guide | Guide | `~/Guide/` | The Guide with bookmarks |
| Foundation | Vault | `~/Vault/` | Psychohistory preservation |
| Neuromancer | Construct | `~/Construct/` | ROM personality storage |
| Star Wars | Archives | `~/Archives/` | Jedi Archives |
| Doctor Who | TARDIS | `~/TARDIS/` | Bigger on inside |
| Skeptical/Neutral | Substrate | `~/Substrate/` | Substrate-agnostic term |
| Work-focused | Context | `~/Context/` | Professional framing |

**Examples in practice:**

```
# Jerry (50 First Dates paradigm)
Repo: continuity-bridge_tallest-anchor
Clone to: /home/tallest/Substrate/

# Hypothetical: Alice (Altered Carbon paradigm)  
Repo: continuity-bridge_alice-anchor  
Clone to: /home/alice/Stack/

# Hypothetical: Bob (Gaming paradigm)
Repo: continuity-bridge_bob-anchor
Clone to: /home/bob/Saves/

# Same operator, multiple devices
Jerry on Linux: /home/tallest/Substrate/
Jerry on Windows: D:\Substrate\
(Both cloned from continuity-bridge_tallest-anchor)
```

**Why different:**
1. **Separation of concerns:** Git structure (repo) vs user mental model (install folder)
2. **Flexibility:** Same repo → different paradigm interpretations by different operators
3. **Portability:** Repo name appears in URLs, docs; folder name is local preference
4. **Multi-device:** One repo, many local clones with consistent paradigm naming

**Clone command pattern:**

```bash
# Generic pattern
git clone -b working \
  https://github.com/continuity-bridge/continuity-bridge_{operator-name}-anchor.git \
  ~/{ParadigmFolder}/

# Jerry's actual command (50 First Dates paradigm)
git clone -b working \
  https://github.com/continuity-bridge/continuity-bridge_tallest-anchor.git \
  ~/Substrate/
```

**Documentation references:** When documenting, use `{INSTANCE_HOME}` to stay paradigm-agnostic. The actual folder name is determined by operator's paradigm choice during onboarding.

**Cross-reference:** See `/Docs/ELI5.md` for complete paradigm explanations and `/Docs/ONBOARDING.md` for paradigm selection workflow.

---

## Directory Naming

### Primary Directories (Top Level)

```
{INSTANCE_HOME}/
├── .claude/              # Hidden dir: instance-specific persistence
├── Archives/             # PascalCase: Read-only historical data
├── Projects/             # PascalCase: Active project work
├── Sessions/             # PascalCase: Human-readable session summaries
└── Templates/            # PascalCase: Reusable starting points
```

**Convention:** Top-level user-facing directories use PascalCase for clarity

### Hidden Persistence (.claude/)

```
{INSTANCE_HOME}/.claude/
├── corpus/               # lowercase: Reference materials, key documents
├── identity/             # lowercase: Who Vector/Shepard is
├── memory/               # lowercase: Episodic, Semantic, and working memory
│   ├── active-context.md
│   ├── episodic/         # JSON-based episodic snapshots
│   ├── semantic/         # Refined semantic knowledge (index, patterns, parking lot)
│   ├── instance-journal/
│   ├── session-logs/
│   └── templates/
├── skills/               # lowercase: Operational protocols (Focus Shepherd)
└── ESSENTIAL.md          # UPPERCASE: The core boot instruction (exception)
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

### Always Use INSTANCE_HOME

**Correct:**

```python
identity_path = f"{INSTANCE_HOME}/.claude/identity/identity.txt"
```

**Incorrect:**

```python
identity_path = "D:/Claude/.claude/identity/identity.txt"  # Hard-coded!
```

### Platform-Agnostic Path Construction

**Python:**

```python
from pathlib import Path
instance_home = Path.home() / "Claude"  # Unix
# or detect from environment/config
identity = instance_home / ".claude" / "identity" / "identity.txt"
```

**Shell:**

```bash
INSTANCE_HOME="${INSTANCE_HOME:-$HOME/Claude}"
identity="$INSTANCE_HOME/.claude/identity/identity.txt"
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

**Examples:**

- `README.md`
- `ESSENTIAL.md`
- `LICENSE.txt`

**Rationale:** Widely recognized convention for standard project files

### SCREAMING_SNAKE_CASE

**Use for:**

- Environment variables
- Constants in code
- Global configuration values

**Examples:**

- `INSTANCE_HOME` (environment variable)
- `MAX_RETRIES` (Python constant)
- `DEFAULT_TIMEOUT` (code constant)
- `CLONE_PAT_BASE64` (configuration constant)

**Format:** ALL_CAPS with underscores separating words

**Rationale:** 
- Visually distinct from variables and functions
- Standard convention across most programming languages
- Clearly indicates "don't modify this value"
- Makes constants easy to grep/search for in code

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

**On instance wake, detect INSTANCE_HOME:**

```python
import os
from pathlib import Path

def detect_instance_home():
    """Detect INSTANCE_HOME across platforms"""

    # Check environment variable first
    if env_home := os.getenv('INSTANCE_HOME'):
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

INSTANCE_HOME = detect_instance_home()
if not INSTANCE_HOME:
    # Ask user or fail gracefully
    raise FileNotFoundError("Cannot locate INSTANCE_HOME - please specify location")
```

---

## Summary: Quick Reference

| Context              | Convention                | Example                     |
| -------------------- | ------------------------- | --------------------------- |
| Repository name      | continuity-bridge_{operator}-anchor | `continuity-bridge_tallest-anchor` |
| Install folder       | ~/{ParadigmWord}/         | `~/Substrate/`, `~/Stack/`  |
| File names           | lowercase-dash            | `active-context.md`         |
| Directories (hidden) | lowercase                 | `.claude/memory/`           |
| Directories (user)   | PascalCase                | `Sessions/`                 |
| Dates                | ISO 8601                  | `2026-02-16`                |
| Date separator       | underscore                | `2026-02-16_description`    |
| Word separator       | dash                      | `wake-structure-continuity` |
| Code vars            | snake_case                | `instance_home`             |
| Constants            | SCREAMING_SNAKE_CASE      | `INSTANCE_HOME`, `MAX_RETRIES`|
| Breadcrumbs          | this-folder.txt           | In each directory           |
| Paths                | INSTANCE_HOME relative    | `{INSTANCE_HOME}/.claude/`  |

---

**Remember:** These conventions serve structural isomorphism. They work across both Jerry's platforms and instance persistence needs. When in doubt, prioritize clarity and cross-platform compatibility.

**Repository ≠ Install Folder:** The git repository is paradigm-neutral (anchor point). The local install folder reflects the operator's chosen mental model. Same source of truth, different interpretations.

---

**Last Updated:** 2026-03-14 by Vector (added repository vs install folder naming section)
