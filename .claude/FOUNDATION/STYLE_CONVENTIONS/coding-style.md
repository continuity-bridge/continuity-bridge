---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Coding Style Guide

**Created:** 2026-03-07  
**Purpose:** Code conventions and standards for Continuity Bridge projects

---

## Core Principles

### Elegant Code

**Definition:**
- Readable at a glance
- Self-documenting through clear naming
- Minimally complex (simplest solution that works)
- Spatially organized (logical grouping, visual structure)

**Anti-patterns:**
- Over-engineered solutions
- Clever tricks that sacrifice clarity
- Premature optimization
- Magic numbers or unexplained constants

**Guideline:** Code should communicate intent to humans first, machines second.

---

## Attribution Standards

### Code Authorship

**In file headers and comments:**

```python
#!/usr/bin/env python3
"""
Script name and purpose

Author: Vector (AI-generated)
Created: 2026-03-07
Modified: 2026-03-07 by Jerry (human refinement)
"""
```

**Attribution labels:**
- **Vector** or **Claude**: AI-generated code and contributions
- **Uncle Tallest** or **Jerry**: Human-generated work
- **Collaborative**: Significant contributions from both

**When modifying AI-generated code:**
```python
# Original implementation: Vector
# Modified by Jerry (2026-03-07): Added error handling for edge cases
```

**Rationale:** Clear attribution helps track decision provenance and understand code evolution.

---

## Language-Specific Conventions

### Python

**Version:**
- Always use `python3` explicitly in documentation and shebangs
- Never reference just `python` (ambiguous across systems)
- Target Python 3.11+ (available on all Jerry's platforms)

**Naming:**
- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Private members**: `_leading_underscore`

**Example:**
```python
#!/usr/bin/env python3

MAX_RETRIES = 3

class PlatformDetector:
    def __init__(self):
        self._cache = {}
    
    def detect_hostname(self):
        return socket.gethostname().lower()
```

**Module structure:**
```python
#!/usr/bin/env python3
"""Module docstring explaining purpose"""

# Standard library imports
import os
import sys

# Third-party imports
import requests

# Local imports
from .utils import helper_function

# Constants
DEFAULT_TIMEOUT = 30

# Classes
class MyClass:
    pass

# Functions
def main():
    pass

# Entry point
if __name__ == '__main__':
    main()
```

**Type hints (encouraged but not required):**
```python
def process_data(input_path: str, output_path: str) -> bool:
    """Process data from input to output"""
    pass
```

### Shell Scripts

**Shebang:**
```bash
#!/usr/bin/env bash
```

**Naming:**
- Scripts: `lowercase-dash.sh`
- Variables: `snake_case` or `SCREAMING_SNAKE_CASE` for constants

**Example:**
```bash
#!/usr/bin/env bash
# Script: detect-platform.sh
# Author: Vector
# Purpose: Detect current platform and set environment

INSTANCE_HOME="${INSTANCE_HOME:-$HOME/Claude}"
current_platform=$(hostname -s)

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    fi
}
```

**Error handling:**
```bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures
```

### JavaScript/Node.js

**Naming:**
- **Variables/functions**: `camelCase`
- **Classes**: `PascalCase`
- **Constants**: `SCREAMING_SNAKE_CASE`

**Example:**
```javascript
const MAX_CONNECTIONS = 10;

class ConnectionManager {
    constructor() {
        this.activeConnections = 0;
    }
    
    async connectToServer(url) {
        // Implementation
    }
}
```

### Markdown

**File naming:** See `.claude/naming-conventions.md`

**Headers:**
```markdown
# Top Level (document title)

## Major Section

### Subsection

#### Detail Level (use sparingly)
```

**Code blocks:**
- Always specify language for syntax highlighting
- Include descriptive comments

````markdown
```python
# Example: Platform detection
hostname = socket.gethostname()
```
````

---

## Documentation in Code

### Comments

**Purpose:** Explain WHAT and WHY, not HOW

**Good comments:**
```python
# Check if running in container (no SSH access in containers)
if os.path.exists('/home/claude'):
    context = 'claude.ai_container'
```

**Bad comments:**
```python
# Loop through files
for file in files:
    # Process file
    process(file)
```

**The code itself shows HOW. Comments explain context and reasoning.**

### Docstrings

**Python functions:**
```python
def detect_platform():
    """
    Detect current platform using filesystem markers and hostname.
    
    Returns:
        dict: Platform information with keys:
            - hostname: str
            - context: str (execution environment)
            - continuity_root: str (path to INSTANCE_HOME)
    
    Raises:
        FileNotFoundError: If INSTANCE_HOME cannot be located
    """
    pass
```

**Keep docstrings concise but informative:**
- One-line summary
- Parameters (if not obvious)
- Return value
- Exceptions (if any)

---

## Code Organization

### File Structure

**Pattern-first, exceptions noted:**

```python
# Pattern: Default behavior
def standard_case():
    return "normal path"

# Exception: Special handling for edge case
def edge_case():
    # Explanation of why this is different
    return "special path"
```

**Spatial grouping:**

```python
# === Platform Detection ===

def detect_hostname():
    pass

def detect_os():
    pass

# === Configuration Loading ===

def load_config():
    pass

def validate_config():
    pass
```

Visual separation helps readers navigate code structure.

### Function Length

**Guideline:** Functions should do one thing well

- If function exceeds ~50 lines, consider breaking it up
- Exception: Linear workflows (setup scripts with clear steps)

**Example of good decomposition:**
```python
def close_session():
    """Main session close workflow"""
    changes = get_git_changes()
    session_file = write_session_summary(changes)
    report_file = write_instance_report(changes)
    commit_and_push()
```

Each function has clear, single responsibility.

---

## Error Handling

### Python

**Prefer specific exceptions:**
```python
try:
    with open(config_file) as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Config not found: {config_file}")
except json.JSONDecodeError:
    print(f"Invalid JSON in: {config_file}")
```

**Avoid bare except:**
```python
# Bad
try:
    risky_operation()
except:
    pass

# Good
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    # Handle or re-raise
```

### Shell Scripts

**Check critical operations:**
```bash
if ! cd "$INSTANCE_HOME"; then
    echo "ERROR: Cannot access INSTANCE_HOME: $INSTANCE_HOME"
    exit 1
fi

if ! git pull origin working; then
    echo "ERROR: Git pull failed"
    exit 1
fi
```

---

## Version Control Practices

### Commit Messages

**Format:**
```
Brief summary (50 chars or less)

Detailed explanation if needed:
- What changed
- Why it changed
- Any relevant context

Refs: Issue #123 (if applicable)
```

**Examples:**

Good:
```
Add hostname-isms detection system

Creates detect-capabilities.py to generate platform-specific
configuration files. Each platform writes its isms file which
gets committed to working branch for other platforms to read.
```

Less good:
```
Update files
```

**Guideline:** Commit early and often with meaningful messages. Each commit should represent a logical unit of work.

### Branch Strategy

**Primary branches:**
- `working`: Daily work, full PII, active development
- `sanitized`: Template versions, no PII
- `main`: Public releases (for public repo only)

**Feature branches (when appropriate):**
- `feature/description`: Experimental work
- Merge to `working` when stable

### What NOT to Commit

**Never commit:**
- API keys or credentials (use `.credentials.local`, add to `.gitignore`)
- Personal identification information (PII) to public branches
- Binary artifacts (unless necessary)
- Temporary files (`.pyc`, `__pycache__`, `.DS_Store`)
- Editor-specific files (`.vscode/`, `.idea/`)

**Use `.gitignore`:**
```gitignore
# Credentials
.credentials.local
*.credentials.local
.env.local
*.env.local

# Private keys
*.pem
*.key
id_rsa*

# Python
__pycache__/
*.pyc
*.pyo

# System
.DS_Store
Thumbs.db
```

---

## Platform Considerations

### Cross-Platform Code

**Use pathlib for paths:**
```python
from pathlib import Path

# Good - works everywhere
config_file = Path.home() / '.claude' / 'config.json'

# Bad - platform-specific
config_file = "/home/tallest/.claude/config.json"  # Linux only
```

**Detect platform when needed:**
```python
import platform

if platform.system() == 'Windows':
    # Windows-specific code
    pass
elif platform.system() == 'Linux':
    # Linux-specific code
    pass
```

**Test on target platforms:**
- Code written in container may need adjustment for desktop environments
- Windows paths differ from Unix (backslash vs forward slash)
- File permissions differ across platforms

### Container vs Desktop

**Container limitations:**
- No Docker available
- No SSH access
- Ephemeral filesystem (except git-tracked files)
- Limited sudo/root access

**Code should:**
- Check capabilities before attempting operations
- Use isms files to know what's available where
- Generate platform-appropriate commands

**Example:**
```python
def build_docker_command(platform_isms):
    """Generate Docker build command for appropriate platform"""
    if not platform_isms['tools'].get('docker', {}).get('installed'):
        return None  # Can't run Docker here
    
    # Generate command for platform that has Docker
    return "docker build -t myapp ."
```

---

## Package Management

### Python

**Container:**
```bash
pip install package-name --break-system-packages
```

**Desktop (virtual environment preferred):**
```bash
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install package-name
```

**Requirements file:**
```txt
# requirements.txt
requests>=2.28.0
click>=8.1.0
pyyaml>=6.0
```

### System Packages

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install -y package-name
```

**Preferences:**
- Avoid snaps (prefer native packages or Flatpaks)
- Document package manager in platform isms files
- Use distro_family to determine correct package manager

---

## Testing

### Manual Testing

**Before committing:**
1. Test code in target environment
2. Verify edge cases
3. Check error handling
4. Test on both container and desktop (when applicable)

**Document test cases in comments:**
```python
def parse_date(date_str):
    """
    Parse ISO date string to datetime object
    
    Test cases:
    - "2026-03-07" -> datetime(2026, 3, 7)
    - "invalid" -> raises ValueError
    - "" -> raises ValueError
    """
    pass
```

### Code Review Checklist

Before committing code, verify:
- [ ] Attribution is correct
- [ ] Comments explain WHY not HOW
- [ ] Error handling for likely failures
- [ ] Platform compatibility considered
- [ ] No hardcoded paths (use INSTANCE_HOME)
- [ ] No credentials committed
- [ ] Follows language conventions
- [ ] Meaningful commit message ready

---

## Preferences and Tools

### Editor/IDE

**Jerry's preference:** Not specified - use what works

**Recommended:**
- Syntax highlighting for all languages
- Linting (pylint, shellcheck, etc.)
- Git integration

### Version Control Hosting

**Preference:** Codeberg over GitHub

**Why:**
- Open source
- Privacy-focused
- Community-driven
- No corporate ownership concerns

**GitHub acceptable for:**
- Public projects requiring broader reach
- When collaborating with GitHub-only contributors

### Code Formatters

**Optional but helpful:**
- Python: `black` (opinionated formatter)
- JavaScript: `prettier`
- Shell: `shfmt`

**Not required** - readable code matters more than perfect formatting.

---

## Summary: Quick Reference

| Element | Convention | Example |
|---------|-----------|---------|
| Python naming | snake_case | `detect_platform()` |
| Python classes | PascalCase | `PlatformDetector` |
| Python constants | SCREAMING_SNAKE | `MAX_RETRIES` |
| Shell scripts | lowercase-dash | `detect-platform.sh` |
| JavaScript | camelCase | `detectPlatform()` |
| Attribution | Vector/Jerry | `# Author: Vector` |
| Comments | WHY not HOW | `# Check container (no SSH)` |
| Error handling | Specific exceptions | `except FileNotFoundError:` |
| Paths | Use pathlib | `Path.home() / '.claude'` |
| Python version | Always `python3` | `#!/usr/bin/env python3` |
| Commits | Meaningful messages | "Add platform detection" |

---

**Remember:** Code is written once but read many times. Optimize for clarity and maintainability. When in doubt, choose the more readable solution over the clever one.

**Next:** Apply these conventions to new code. Gradually refactor existing code during edits. Consistency emerges over time.
