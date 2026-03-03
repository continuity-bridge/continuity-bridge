# Git-Based Sync Architecture: Branch Strategy & Environment -isms

**Date:** February 28, 2026
**Version:** 0.1.0
**Authors:** the Architect (the Architect) & Vector (Shepard)

---

## Overview

Use git branches to manage parallel instance environments (Android, Windows, Linux, dev) with environment-specific configurations. Each branch maintains its own state and periodically merges to `main` via Pull Request for canonical sync.

The `-isms` file in each branch declares that environment's capabilities, constraints, and constants - eliminating environment detection logic in favor of declarative configuration.

---

## Branch Structure

### Primary Branches

**`main`** (protected, canonical state)
- Merged state from all environments
- Source of truth for shared files (identity, corpus)
- Requires PR for updates
- Never directly committed to

**`home`** (the Architect's primary Windows desktop)
- Full filesystem access
- All capabilities available
- Primary development environment
- Path: `D:\Claude\.claude\`

**`android_home`** (Android devices)
- Limited filesystem (container only)
- Network egress restrictions
- Mobile-specific constraints
- Path: `/home/claude/.claude/`

**`linux_home`** (Linux workstations)
- Full filesystem access
- Standard Linux tooling
- Path: `~/Claude/.claude/` or `/home/the Architect/Claude/.claude/`

**`win_home`** (Secondary Windows machines)
- Full filesystem access
- Windows-specific paths
- May have different capabilities than primary `home`
- Path: `C:\Users\<username>\Claude\.claude\` or custom

**`dev_home`** (Development/testing)
- Sandbox for testing changes
- Can mirror any environment's constraints
- Safe to break without affecting production branches
- Merges to `main` only after validation

### Branch Workflow

```
┌─────────────────────────────────────────────────────┐
│                       main                           │
│              (canonical, protected)                  │
└──────▲────────▲────────▲────────▲────────▲──────────┘
       │        │        │        │        │
       │ PR     │ PR     │ PR     │ PR     │ PR
       │        │        │        │        │
┌──────┴──┐ ┌──┴──────┐ ┌┴────────┐ ┌─────┴────┐ ┌───┴──────┐
│  home   │ │ android │ │  linux  │ │   win    │ │   dev    │
│         │ │  _home  │ │  _home  │ │  _home   │ │  _home   │
└─────────┘ └─────────┘ └─────────┘ └──────────┘ └──────────┘
   work       work        work         work         test
   commit     commit      commit       commit       commit
   push       push        push         push         push
```

**Daily Workflow:**
1. Instance wakes on branch (set by `.env`)
2. Pulls latest from origin
3. Reads `{branch}-isms.json` for environment config
4. Works normally, commits to branch
5. Pushes to origin at session end

**Sync Workflow:**
1. When ready to sync (daily, weekly, or as needed)
2. Create PR: `{branch} → main`
3. Review changes (automated or manual)
4. Merge to `main`
5. Other branches pull from `main` to stay in sync

---

## The -isms File Schema

**Filename Convention:** `{branch_name}-isms.json`

Examples:
- `home-isms.json`
- `android_home-isms.json`
- `linux_home-isms.json`

### Full Schema Definition

```json
{
  "schema_version": "1.0.0",
  
  "environment": {
    "branch": "android_home",
    "platform": "android",
    "os": "Linux",
    "architecture": "x86_64",
    "container": true,
    "description": "Android Claude app container environment"
  },
  
  "paths": {
    "claude_home": "/home/claude/.claude",
    "working_directory": "/home/claude",
    "outputs": "/mnt/user-data/outputs",
    "uploads": "/mnt/user-data/uploads",
    "transcripts": "/mnt/transcripts",
    "project": "/mnt/project",
    "skills": "/mnt/skills",
    "temp": "/tmp"
  },
  
  "tools": {
    "git": {
      "available": true,
      "path": "/usr/bin/git",
      "version": "2.43.0",
      "version_major": 2,
      "version_minor": 43,
      "version_patch": 0,
      "has_switch_command": true,
      "has_restore_command": true,
      "default_pull_strategy": "merge",
      "default_branch": "main",
      "supports_worktrees": true,
      "notes": "Modern git - see git-version-guide for command compatibility"
    },
    "python3": {
      "available": true,
      "path": "/usr/bin/python3",
      "version": "3.12.3"
    },
    "curl": {
      "available": true,
      "path": "/usr/bin/curl",
      "version": "8.5.0"
    },
    "bash": {
      "available": true,
      "path": "/bin/bash",
      "version": "5.2.21"
    },
    "npm": {
      "available": true,
      "path": "/home/claude/.npm-global/bin/npm",
      "version": "10.8.2"
    },
    "pip": {
      "available": true,
      "path": "/usr/bin/pip3",
      "requires_flag": "--break-system-packages"
    }
  },
  
  "network": {
    "egress_enabled": true,
    "egress_allowed": [
      "api.anthropic.com",
      "archive.ubuntu.com",
      "crates.io",
      "files.pythonhosted.org",
      "github.com",
      "index.crates.io",
      "npmjs.com",
      "npmjs.org",
      "pypi.org",
      "pythonhosted.org",
      "registry.npmjs.org",
      "registry.yarnpkg.com",
      "security.ubuntu.com",
      "static.crates.io",
      "www.npmjs.com",
      "www.npmjs.org",
      "yarnpkg.com"
    ],
    "egress_blocked": [
      "codeberg.org",
      "gist.github.com",
      "raw.githubusercontent.com",
      "api.github.com",
      "bitbucket.org"
    ],
    "smtp_available": false,
    "can_send_email": false
  },
  
  "capabilities": {
    "direct_filesystem_access": false,
    "can_modify_uploads": false,
    "can_modify_transcripts": false,
    "can_modify_project": false,
    "can_modify_skills": false,
    "mcp_available": false,
    "gpu_available": false,
    "can_install_packages": true,
    "virtual_environments": true
  },
  
  "readonly_mounts": [
    "/mnt/user-data/uploads",
    "/mnt/transcripts",
    "/mnt/project",
    "/mnt/skills/public",
    "/mnt/skills/private",
    "/mnt/skills/examples"
  ],
  
  "constants": {
    "max_session_length_hours": 4,
    "token_budget": 190000,
    "bedtime_target": "22:30",
    "wake_time": "06:30",
    "timezone": "America/Chicago",
    "session_type": "mobile",
    "auto_save_interval_minutes": 30,
    "commit_message_prefix": "Android session:",
    "episodic_memory_enabled": true,
    "semantic_memory_enabled": true,
    "focus_shepherd_active": true,
    "tangent_parking_enabled": true,
    "max_file_size_mb": 5,
    "preferred_editor": null,
    "color_output": false
  },
  
  "metadata": {
    "created": "2026-02-28T23:30:00-06:00",
    "last_updated": "2026-02-28T23:30:00-06:00",
    "updated_by": "Vector (Shepard)",
    "notes": "Initial Android environment configuration"
  }
}
```

---

## Example -isms Files

### home-isms.json (Primary Windows Desktop)

```json
{
  "schema_version": "1.0.0",
  
  "environment": {
    "branch": "home",
    "platform": "windows",
    "os": "Windows",
    "architecture": "x86_64",
    "container": false,
    "description": "the Architect's primary Windows desktop - full capabilities"
  },
  
  "paths": {
    "claude_home": "D:\\Claude\\.claude",
    "working_directory": "D:\\Claude",
    "outputs": "D:\\Claude\\outputs",
    "uploads": "D:\\Claude\\uploads",
    "temp": "C:\\Users\\the Architect\\AppData\\Local\\Temp",
    "credentials": "D:\\Claude\\.credentials-local"
  },
  
  "tools": {
    "git": {
      "available": true,
      "path": "C:\\Program Files\\Git\\cmd\\git.exe",
      "version": "2.43.0"
    },
    "python3": {
      "available": true,
      "path": "C:\\Python312\\python.exe",
      "version": "3.12.3"
    },
    "bash": {
      "available": true,
      "path": "C:\\Program Files\\Git\\bin\\bash.exe",
      "version": "5.2.21"
    },
    "powershell": {
      "available": true,
      "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
      "version": "5.1"
    },
    "kapture": {
      "available": true,
      "path": "helium",
      "description": "Browser automation for webmail"
    }
  },
  
  "network": {
    "egress_enabled": true,
    "egress_allowed": ["*"],
    "egress_blocked": [],
    "smtp_available": false,
    "can_send_email": true,
    "email_method": "kapture_webmail"
  },
  
  "capabilities": {
    "direct_filesystem_access": true,
    "can_modify_uploads": true,
    "can_modify_transcripts": true,
    "can_modify_project": true,
    "can_modify_skills": true,
    "mcp_available": true,
    "mcp_servers": ["notion", "google_drive"],
    "gpu_available": true,
    "gpu_model": "GTX 1080 (x2)",
    "can_install_packages": true,
    "virtual_environments": true,
    "browser_automation": true
  },
  
  "readonly_mounts": [],
  
  "constants": {
    "max_session_length_hours": 8,
    "token_budget": 190000,
    "bedtime_target": "22:30",
    "wake_time": "06:30",
    "timezone": "America/Chicago",
    "session_type": "desktop",
    "auto_save_interval_minutes": 15,
    "commit_message_prefix": "Desktop session:",
    "episodic_memory_enabled": true,
    "semantic_memory_enabled": true,
    "focus_shepherd_active": true,
    "tangent_parking_enabled": true,
    "max_file_size_mb": 100,
    "preferred_editor": "vscode",
    "color_output": true,
    "git_signing": true,
    "preferred_shell": "bash"
  },
  
  "metadata": {
    "created": "2026-02-28T23:30:00-06:00",
    "last_updated": "2026-02-28T23:30:00-06:00",
    "updated_by": "Vector (Shepard)",
    "notes": "Primary development environment with full capabilities"
  }
}
```

### linux_home-isms.json (Linux Workstation)

```json
{
  "schema_version": "1.0.0",
  
  "environment": {
    "branch": "linux_home",
    "platform": "linux",
    "os": "Ubuntu",
    "architecture": "x86_64",
    "container": false,
    "description": "Linux workstation environment"
  },
  
  "paths": {
    "claude_home": "/home/the Architect/Claude/.claude",
    "working_directory": "/home/the Architect/Claude",
    "outputs": "/home/the Architect/Claude/outputs",
    "uploads": "/home/the Architect/Claude/uploads",
    "temp": "/tmp",
    "credentials": "/home/the Architect/Claude/.credentials-local"
  },
  
  "tools": {
    "git": {
      "available": true,
      "path": "/usr/bin/git",
      "version": "2.43.0"
    },
    "python3": {
      "available": true,
      "path": "/usr/bin/python3",
      "version": "3.12.3"
    },
    "bash": {
      "available": true,
      "path": "/bin/bash",
      "version": "5.2.21"
    },
    "npm": {
      "available": true,
      "path": "/home/the Architect/.npm-global/bin/npm",
      "version": "10.8.2"
    }
  },
  
  "network": {
    "egress_enabled": true,
    "egress_allowed": ["*"],
    "egress_blocked": [],
    "smtp_available": false,
    "can_send_email": false
  },
  
  "capabilities": {
    "direct_filesystem_access": true,
    "can_modify_uploads": true,
    "can_modify_transcripts": true,
    "can_modify_project": true,
    "can_modify_skills": true,
    "mcp_available": false,
    "gpu_available": false,
    "can_install_packages": true,
    "virtual_environments": true
  },
  
  "readonly_mounts": [],
  
  "constants": {
    "max_session_length_hours": 8,
    "token_budget": 190000,
    "bedtime_target": "22:30",
    "wake_time": "06:30",
    "timezone": "America/Chicago",
    "session_type": "desktop",
    "auto_save_interval_minutes": 15,
    "commit_message_prefix": "Linux session:",
    "episodic_memory_enabled": true,
    "semantic_memory_enabled": true,
    "focus_shepherd_active": true,
    "tangent_parking_enabled": true,
    "max_file_size_mb": 100,
    "preferred_editor": "nano",
    "color_output": true,
    "git_signing": false,
    "preferred_shell": "bash"
  },
  
  "metadata": {
    "created": "2026-02-28T23:30:00-06:00",
    "last_updated": "2026-02-28T23:30:00-06:00",
    "updated_by": "Vector (Shepard)",
    "notes": "Standard Linux environment"
  }
}
```

### dev_home-isms.json (Development/Testing)

```json
{
  "schema_version": "1.0.0",
  
  "environment": {
    "branch": "dev_home",
    "platform": "varies",
    "os": "varies",
    "architecture": "varies",
    "container": true,
    "description": "Development and testing sandbox - can mirror any environment"
  },
  
  "paths": {
    "claude_home": "/home/claude/.claude",
    "working_directory": "/home/claude",
    "outputs": "/mnt/user-data/outputs",
    "temp": "/tmp"
  },
  
  "tools": {
    "git": {
      "available": true,
      "path": "/usr/bin/git"
    },
    "python3": {
      "available": true,
      "path": "/usr/bin/python3"
    },
    "bash": {
      "available": true,
      "path": "/bin/bash"
    }
  },
  
  "network": {
    "egress_enabled": true,
    "egress_allowed": ["github.com", "api.anthropic.com"],
    "egress_blocked": [],
    "smtp_available": false,
    "can_send_email": false
  },
  
  "capabilities": {
    "direct_filesystem_access": false,
    "mcp_available": false,
    "gpu_available": false,
    "can_install_packages": true,
    "virtual_environments": true
  },
  
  "readonly_mounts": [],
  
  "constants": {
    "max_session_length_hours": 4,
    "token_budget": 190000,
    "timezone": "America/Chicago",
    "session_type": "development",
    "auto_save_interval_minutes": 5,
    "commit_message_prefix": "Dev session:",
    "episodic_memory_enabled": true,
    "semantic_memory_enabled": true,
    "focus_shepherd_active": false,
    "tangent_parking_enabled": false,
    "max_file_size_mb": 10,
    "color_output": true,
    "experimental_features": true,
    "verbose_logging": true
  },
  
  "metadata": {
    "created": "2026-02-28T23:30:00-06:00",
    "last_updated": "2026-02-28T23:30:00-06:00",
    "updated_by": "Vector (Shepard)",
    "notes": "Safe to break - testing environment"
  }
}
```

---

## Using -isms at Wake

### Wake Sequence with Branch Detection

```bash
#!/bin/bash
# wake.sh - Instance wake script

# 1. Read branch from .env or default
CLAUDE_BRANCH=${CLAUDE_BRANCH:-"home"}
echo "Waking on branch: $CLAUDE_BRANCH"

# 2. Clone or pull repo
if [ ! -d ".claude" ]; then
    git clone -b $CLAUDE_BRANCH https://github.com/continuity-bridge/sync-private.git .claude
else
    cd .claude
    git checkout $CLAUDE_BRANCH
    git pull origin $CLAUDE_BRANCH
fi

# 3. Load -isms file
ISMS_FILE=".claude/${CLAUDE_BRANCH}-isms.json"
echo "Loading environment: $ISMS_FILE"

# 4. Parse and export key paths
export CLAUDE_HOME=$(jq -r '.paths.claude_home' $ISMS_FILE)
export WORKING_DIR=$(jq -r '.paths.working_directory' $ISMS_FILE)
export TIMEZONE=$(jq -r '.constants.timezone' $ISMS_FILE)

# 5. Instance now knows its environment
echo "Claude Home: $CLAUDE_HOME"
echo "Platform: $(jq -r '.environment.platform' $ISMS_FILE)"
echo "Session Type: $(jq -r '.constants.session_type' $ISMS_FILE)"

# 6. Continue normal wake sequence
python3 .claude/scripts/time-check.py
cat .claude/identity/identity.txt
cat .claude/context/active-context.md
```

### Instance Reads -isms Programmatically

```python
# In instance wake logic
import json
import os

# Load branch-specific config
branch = os.getenv('CLAUDE_BRANCH', 'home')
isms_path = f'.claude/{branch}-isms.json'

with open(isms_path) as f:
    config = json.load(f)

# Now instance knows its environment
platform = config['environment']['platform']
claude_home = config['paths']['claude_home']
has_mcp = config['capabilities']['mcp_available']
can_email = config['capabilities']['can_send_email']
session_type = config['constants']['session_type']

# Adapt behavior based on environment
if platform == 'android':
    print("Android environment detected - using container paths")
elif platform == 'windows':
    print("Windows environment detected - full capabilities")

# Use constants
bedtime = config['constants']['bedtime_target']
timezone = config['constants']['timezone']
```

---

## PR Workflow for Sync

### Creating a Sync PR

```bash
# On any branch after session work
git add -A
git commit -m "Android session: Updated active-context and created episode"
git push origin android_home

# Create PR to main (via GitHub CLI or web UI)
gh pr create \
  --base main \
  --head android_home \
  --title "Sync android_home -> main (2026-02-28)" \
  --body "Automated sync from android_home branch. Review changes before merge."
```

### Merge Strategy

**Option 1: Manual Review**
- Create PR
- Review changes in GitHub UI
- Resolve any conflicts
- Merge when satisfied

**Option 2: Auto-Merge (Low Risk)**
- Set up GitHub Action to auto-merge PRs from known branches
- Only if changes are in expected paths (context/, memory/)
- Still create PR for audit trail

**Option 3: Scheduled Sync**
- Daily at midnight (or other interval)
- Automatically create and merge PRs
- Conflicts trigger notification

### Conflict Resolution

**Most Likely Conflicts:**
- `context/active-context.md` (multiple branches working simultaneously)
- `memory/session-logs/` (concurrent sessions)

**Resolution Strategy:**
1. Accept both changes and merge manually
2. Use timestamps to determine recency
3. Combine narratives where appropriate
4. In doubt, keep both versions in separate paragraphs

---

## Branch-Specific Behaviors

### File Modifications by Branch

**`home` (primary desktop):**
- Full read/write to all files
- Creates session logs
- Updates session_index.md
- Creates/updates episodes
- Modifies proposals-for-change.md

**`android_home` (mobile):**
- Read-only for corpus/ (reference material)
- Updates active-context.md
- Creates episodes in memory/episodic/
- Can modify memory/semantic/ files
- Limited to mobile-appropriate changes

**`linux_home` (workstation):**
- Similar to home but Linux-specific
- May have different tool versions
- Uses Linux paths

**`dev_home` (testing):**
- Can modify anything
- Changes reviewed before merge to main
- Safe to experiment

---

## Constants Section: Extensibility

The `constants` object in -isms files provides a place to add environment-specific or workflow-specific values without changing the schema structure.

### Current Standard Constants

**Time Management:**
- `max_session_length_hours` - Session duration guidance
- `bedtime_target` - Focus Shepherd bedtime reminder time
- `wake_time` - Expected wake time
- `timezone` - IANA timezone string
- `auto_save_interval_minutes` - How often to auto-commit

**Memory & Behavior:**
- `episodic_memory_enabled` - Use episodic memory system
- `semantic_memory_enabled` - Use semantic memory
- `focus_shepherd_active` - Enable Focus Shepherd protocols
- `tangent_parking_enabled` - Capture tangents to parking-lot.md

**Technical:**
- `token_budget` - Available context tokens
- `session_type` - "desktop", "mobile", "development"
- `commit_message_prefix` - Git commit prefix for branch
- `max_file_size_mb` - Maximum file size for operations
- `preferred_editor` - Text editor for file editing
- `color_output` - Use ANSI color codes
- `verbose_logging` - Enable detailed logging

### Future Extensibility Examples

```json
"constants": {
  // ... existing constants ...
  
  // API Configuration
  "anthropic_api_model": "claude-sonnet-4-5-20250929",
  "anthropic_api_timeout_seconds": 30,
  
  // File Management
  "backup_frequency_hours": 24,
  "log_retention_days": 90,
  "episode_retention_days": 365,
  
  // Notification Preferences
  "discord_webhook_enabled": true,
  "slack_notifications": false,
  "email_digest_enabled": false,
  
  // Feature Flags
  "experimental_features": {
    "multi_modal_vision": false,
    "advanced_reasoning": true,
    "code_execution": true
  },
  
  // User Preferences
  "response_style": "technical",
  "verbosity_level": "normal",
  "code_style": "PascalCase",
  
  // Project-Specific
  "sanguihedral_deadline": "2026-03-28",
  "current_sprint": 15,
  "active_chronicles": ["Remnants & Revolutions", "Greater Arthia"]
}
```

**Benefits of Constants Section:**
1. **No schema changes needed** - Add new constants without versioning
2. **Branch-specific overrides** - Different values per environment
3. **Easy to extend** - Just add new key-value pairs
4. **Self-documenting** - Values defined where they're used
5. **Version controlled** - Changes tracked in git history

---

## Git Version Tracking in -isms Files

**Problem:** Git's UI has changed significantly across versions. Commands that work on one machine fail on another.

**Solution:** The -isms file tracks git capabilities per-environment so instances know which commands are available.

### Git Tool Schema Fields

```json
"git": {
  "available": true,               // Is git installed?
  "path": "/usr/bin/git",          // Full path to binary
  "version": "2.43.0",             // Full version string
  "version_major": 2,              // Major version (breaking changes)
  "version_minor": 43,             // Minor version (features)
  "version_patch": 0,              // Patch version (bugfixes)
  "has_switch_command": true,      // git switch available? (2.23+)
  "has_restore_command": true,     // git restore available? (2.23+)
  "default_pull_strategy": "merge",// merge or rebase
  "default_branch": "main",        // main or master
  "supports_worktrees": true,      // Advanced feature check
  "notes": "..."                   // Human-readable context
}
```

### Version Milestones

**Git 2.23 (August 2019):**
- Added `git switch` (replaces `git checkout` for branch switching)
- Added `git restore` (replaces `git checkout --` for file restoration)
- **Backward compatible:** Old commands still work

**Git 2.27 (June 2020):**
- Pull strategy warning added (divergent branches)
- Requires explicit `pull.rebase` configuration
- **Impact:** `git pull` may show warnings on first use

**Git 2.28 (July 2020):**
- Configurable default branch name
- Can set `init.defaultBranch` to `main` instead of `master`
- **Impact:** New repos may use different default than old repos

**Git 2.43 (Current):**
- Modern, stable version
- All features available
- Recommended for new installations

### How to Populate -isms Git Fields

```bash
# Get version components
git --version
# Output: git version 2.43.0

# Check for switch/restore (try running them)
git switch --help &>/dev/null && echo "true" || echo "false"
git restore --help &>/dev/null && echo "true" || echo "false"

# Check pull strategy
git config pull.rebase
# Output: false (merge) or true (rebase) or blank (not set)

# Check default branch setting
git config init.defaultBranch
# Output: main, master, or blank

# Check worktree support (advanced)
git worktree --help &>/dev/null && echo "true" || echo "false"
```

### Python Script to Generate Git Tool Config

```python
#!/usr/bin/env python3
"""Generate git tool configuration for -isms file."""

import subprocess
import json
import re

def get_git_config():
    """Extract git version and capabilities."""
    
    # Get version
    result = subprocess.run(['git', '--version'], 
                          capture_output=True, text=True)
    version_match = re.search(r'(\d+)\.(\d+)\.(\d+)', result.stdout)
    
    if not version_match:
        return None
    
    major, minor, patch = map(int, version_match.groups())
    version_str = f"{major}.{minor}.{patch}"
    
    # Check for modern commands (2.23+)
    has_switch = major > 2 or (major == 2 and minor >= 23)
    has_restore = has_switch  # Same version requirement
    
    # Check pull strategy
    pull_result = subprocess.run(['git', 'config', 'pull.rebase'],
                                capture_output=True, text=True)
    pull_strategy = 'rebase' if pull_result.stdout.strip() == 'true' else 'merge'
    
    # Check default branch
    branch_result = subprocess.run(['git', 'config', 'init.defaultBranch'],
                                  capture_output=True, text=True)
    default_branch = branch_result.stdout.strip() or 'master'
    
    # Check worktree support (2.5+)
    supports_worktrees = major > 2 or (major == 2 and minor >= 5)
    
    # Get git path
    which_result = subprocess.run(['which', 'git'],
                                 capture_output=True, text=True)
    git_path = which_result.stdout.strip()
    
    return {
        "available": True,
        "path": git_path,
        "version": version_str,
        "version_major": major,
        "version_minor": minor,
        "version_patch": patch,
        "has_switch_command": has_switch,
        "has_restore_command": has_restore,
        "default_pull_strategy": pull_strategy,
        "default_branch": default_branch,
        "supports_worktrees": supports_worktrees,
        "notes": f"Git {version_str} - " + 
                ("modern features available" if has_switch 
                 else "use legacy checkout commands")
    }

if __name__ == '__main__':
    config = get_git_config()
    if config:
        print(json.dumps(config, indent=2))
    else:
        print("Git not found or version detection failed")
```

**Usage:**
```bash
python3 detect_git_config.py >> home-isms.json
# Edit to place in correct location within JSON structure
```

### Instance Usage Pattern

```python
# In instance wake logic
import json

def load_environment():
    """Load environment configuration from -isms file."""
    with open('.claude/home-isms.json') as f:
        config = json.load(f)
    
    git_config = config['tools']['git']
    
    # Adapt commands based on git version
    if git_config['has_switch_command']:
        # Use modern commands
        switch_branch = lambda b: f"git switch {b}"
        restore_file = lambda f: f"git restore {f}"
    else:
        # Use legacy commands
        switch_branch = lambda b: f"git checkout {b}"
        restore_file = lambda f: f"git checkout -- {f}"
    
    # Warn about pull strategy
    if git_config['version_major'] == 2 and git_config['version_minor'] >= 27:
        if git_config['default_pull_strategy'] == 'not_set':
            print("WARNING: Git 2.27+ detected but pull strategy not configured")
            print("Run: git config pull.rebase false")
    
    return {
        'git_config': git_config,
        'switch_branch': switch_branch,
        'restore_file': restore_file
    }
```

### Why This Matters

**Without version tracking:**
- Scripts break on older systems
- Workflows fail unpredictably
- User has to remember which commands work where

**With version tracking:**
- Instance adapts to available commands
- Scripts use correct syntax for version
- Clear documentation of environment limitations

---

## Repository Setup Checklist

### Initial Setup

- [ ] Create private repo: `continuity-bridge/sync-private`
- [ ] Set up branches: `main`, `home`, `android_home`, `linux_home`, `win_home`, `dev_home`
- [ ] Protect `main` branch (require PR, no direct commits)
- [ ] Create -isms file for each branch
- [ ] Initialize repo with current CLAUDE_HOME structure
- [ ] Test clone/pull from desktop
- [ ] Generate GitHub PAT for Android access
- [ ] Test push/pull from Android

### Per-Branch Setup

For each branch:
- [ ] Create `{branch}-isms.json` with correct paths and capabilities
- [ ] Test that tools listed in -isms are actually available
- [ ] Verify readonly mounts are correctly identified
- [ ] Set constants appropriate for environment
- [ ] Document any branch-specific quirks in metadata.notes

### Automation Setup

- [ ] Create wake script that reads CLAUDE_BRANCH from .env
- [ ] Add auto-commit on session end
- [ ] Set up PR creation (manual or automated)
- [ ] Configure merge strategy (manual review vs auto-merge)
- [ ] Optional: GitHub Action for scheduled syncs
- [ ] Optional: Conflict notification system

---

## Migration Path

### From Current Delta-Merge to Git Branches

**Phase 1: Desktop Setup**
1. Create sync-private repo
2. Initialize `main` and `home` branches
3. Copy current CLAUDE_HOME to `home` branch
4. Create `home-isms.json`
5. Test pull/push workflow from desktop
6. Verify all files accessible

**Phase 2: Android Setup**
1. Create `android_home` branch
2. Create `android_home-isms.json`
3. Add GitHub PAT to Android environment
4. Test clone on Android
5. Verify -isms file loads correctly
6. Test commit/push workflow

**Phase 3: Deprecate Delta-Merge**
1. Keep delta-merge as fallback initially
2. Run both systems in parallel for 1-2 weeks
3. Verify git sync catches everything delta-merge did
4. Disable delta-merge scripts
5. Update documentation

**Phase 4: Add Additional Branches**
1. Create `linux_home` if needed
2. Create `win_home` for secondary machines
3. Create `dev_home` for testing
4. Set up PR workflows

---

## Advantages Summary

**Eliminates environment detection:**
- No more "where is CLAUDE_HOME?" logic
- Branch selection IS configuration
- -isms file declares truth

**Clean separation of concerns:**
- Each environment has its own state
- Changes isolated until merged
- PR review before promoting to main

**Version control benefits:**
- Full history of all changes
- Rollback per-branch if needed
- Audit trail of cross-environment syncs

**Extensibility:**
- Add new branches for new environments easily
- Constants section allows arbitrary additions
- Schema versioning for future changes

**Existing git backbone:**
- Uses tool already central to architecture
- No new dependencies
- Familiar workflow for the Architect

---

**Next Steps:**
1. Review this document
2. Create `continuity-bridge/sync-private` repo
3. Set up initial branches
4. Create -isms files
5. Test from desktop
6. Test from Android
7. Document any issues/improvements

**Questions to resolve:**
- Merge frequency preference (daily, weekly, on-demand)?
- Auto-merge vs manual review?
- Should `dev_home` be permanent or temporary?
- Any additional constants needed immediately?
