# PREFLIGHT: Environment Verification Checklist

**Purpose:** Verify that your environment matches the expected configuration before starting work. This ensures tools are available, paths are correct, and the instance can function properly.

**When to run:** Every wake, after reading ESSENTIAL.md but before engaging with work.

---

## Quick Start

```bash
# Set your platform (if not in .env)
export CLAUDE_PLATFORM=android_home  # or home, linux_home, dev_home

# Run preflight checks
python3 .claude/scripts/preflight.py

# Or manually follow checklist below
```

---

## Manual Preflight Checklist

### Step 1: Identify Platform

**Check environment variable:**
```bash
echo $CLAUDE_PLATFORM
```

**Expected output:**
- `home` (Windows primary desktop)
- `android_home` (Android devices)
- `linux_home` (Linux workstations)
- `dev_home` (Development/testing)

**✅ PASS:** Variable is set and matches one of the above  
**❌ FAIL:** Variable not set or invalid

**Fix if failed:**
```bash
export CLAUDE_PLATFORM=android_home  # Set to your platform
# Add to .env or shell profile for persistence
```

---

### Step 2: Load Configuration

**Load -isms file:**
```bash
ISMS_FILE=".claude/${CLAUDE_PLATFORM}-isms.json"
cat $ISMS_FILE
```

**✅ PASS:** File exists and contains valid JSON  
**❌ FAIL:** File not found or malformed

**Fix if failed:**
```bash
# Check if file exists
ls -la .claude/*-isms.json

# If missing, you may need to pull from remote
git pull origin working

# Or create from template (see git-branch-strategy docs)
```

---

### Step 3: Verify Paths

**Check CLAUDE_HOME exists:**
```bash
# Read from -isms
CLAUDE_HOME=$(python3 -c "import json; print(json.load(open('$ISMS_FILE'))['paths']['claude_home'])")
echo "CLAUDE_HOME: $CLAUDE_HOME"

# Verify it exists
ls -la "$CLAUDE_HOME"
```

**✅ PASS:** Directory exists and is accessible  
**❌ FAIL:** Directory not found or permission denied

**Fix if failed:**
```bash
# Create if missing
mkdir -p "$CLAUDE_HOME"

# Check permissions
ls -ld "$CLAUDE_HOME"
# Should be writable by your user
```

---

**Check working directory:**
```bash
WORK_DIR=$(python3 -c "import json; print(json.load(open('$ISMS_FILE'))['paths']['working_directory'])")
echo "Working directory: $WORK_DIR"

ls -la "$WORK_DIR"
```

**✅ PASS:** Directory exists and is accessible  
**❌ FAIL:** Directory not found

**Fix if failed:**
```bash
mkdir -p "$WORK_DIR"
```

---

**Check outputs directory (if specified):**
```bash
OUTPUTS=$(python3 -c "import json; print(json.load(open('$ISMS_FILE'))['paths'].get('outputs', ''))")
if [ -n "$OUTPUTS" ]; then
    echo "Outputs: $OUTPUTS"
    ls -la "$OUTPUTS" 2>/dev/null || echo "⚠️  Outputs directory not accessible"
fi
```

**✅ PASS:** Directory exists or not specified  
**⚠️ WARNING:** Specified but not accessible (may affect file sharing)

---

**Verify readonly mounts (if any):**
```bash
python3 -c "
import json
config = json.load(open('$ISMS_FILE'))
for mount in config.get('readonly_mounts', []):
    print(f'Checking readonly mount: {mount}')
"
```

**✅ PASS:** Listed directories exist  
**⚠️ WARNING:** Missing directories (expected on some platforms)

---

### Step 4: Tool Verification

**Check Git:**
```bash
GIT_PATH=$(python3 -c "import json; print(json.load(open('$ISMS_FILE'))['tools']['git']['path'])")
GIT_VERSION=$(python3 -c "import json; print(json.load(open('$ISMS_FILE'))['tools']['git']['version'])")

echo "Expected git: $GIT_PATH version $GIT_VERSION"
echo "Actual git: $(which git) version $(git --version)"
```

**✅ PASS:** Git found and version is close (major.minor match)  
**⚠️ WARNING:** Version mismatch (may affect available commands)  
**❌ FAIL:** Git not found

**Fix if failed:**
```bash
# Install git (platform-specific)
# Ubuntu/Debian: sudo apt install git
# Windows: Download from git-scm.com
# Mac: brew install git
```

---

**Check Python:**
```bash
PYTHON_PATH=$(python3 -c "import json; print(json.load(open('$ISMS_FILE'))['tools']['python3']['path'])")
PYTHON_VERSION=$(python3 -c "import json; print(json.load(open('$ISMS_FILE'))['tools']['python3']['version'])")

echo "Expected python: $PYTHON_PATH version $PYTHON_VERSION"
echo "Actual python: $(which python3) version $(python3 --version)"
```

**✅ PASS:** Python3 found and version is close  
**⚠️ WARNING:** Version mismatch  
**❌ FAIL:** Python3 not found

---

**Check other tools as needed:**
```bash
# Check each tool listed in -isms file
python3 -c "
import json
config = json.load(open('$ISMS_FILE'))
for tool, info in config['tools'].items():
    if info.get('available'):
        print(f'✓ {tool}: {info[\"path\"]}')
    else:
        print(f'✗ {tool}: not available')
"
```

---

### Step 5: Network Verification

**Check egress enabled:**
```bash
EGRESS=$(python3 -c "import json; print(json.load(open('$ISMS_FILE'))['network']['egress_enabled'])")
echo "Network egress enabled: $EGRESS"
```

**✅ PASS:** True  
**❌ FAIL:** False (will affect git sync and package installs)

---

**Test critical domains:**
```bash
# GitHub (required for git sync)
curl -I https://github.com 2>&1 | head -3

# Anthropic API (if needed)
curl -I https://api.anthropic.com 2>&1 | head -3
```

**✅ PASS:** HTTP 200 or similar success  
**❌ FAIL:** 403 Forbidden or connection refused

**Fix if failed:**
```bash
# Check network configuration
# May need to update egress rules in container/firewall
# See -isms file for allowed/blocked domains
```

---

### Step 6: Git Configuration

**Check pull strategy:**
```bash
git config pull.rebase
```

**✅ PASS:** Returns `false` or `true`  
**⚠️ WARNING:** Empty (not configured, will see warnings)

**Fix if warning:**
```bash
git config pull.rebase false  # Use merge strategy
# Or: git config pull.rebase true  # Use rebase strategy
```

---

**Check default branch:**
```bash
git config init.defaultBranch
```

**✅ PASS:** Returns `main` or `master`  
**⚠️ WARNING:** Empty (not configured)

**Fix if warning:**
```bash
git config --global init.defaultBranch main
```

---

**Check user configuration:**
```bash
git config user.name
git config user.email
```

**✅ PASS:** Both set  
**❌ FAIL:** One or both empty

**Fix if failed:**
```bash
git config --global user.name "Vector (Android)"
git config --global user.email "vector@ohmytallest.productions"
```

---

### Step 7: Platform-Specific Checks

**Read constants from -isms:**
```bash
python3 -c "
import json
config = json.load(open('$ISMS_FILE'))
constants = config.get('constants', {})
print('Platform constants:')
for key, value in constants.items():
    print(f'  {key}: {value}')
"
```

**Check session type:**
- `desktop`: Full-featured environment
- `mobile`: Limited environment (Android)
- `development`: Testing environment

**Check feature flags:**
- `episodic_memory_enabled`
- `semantic_memory_enabled`
- `focus_shepherd_active`

**✅ PASS:** Constants look reasonable  
**⚠️ WARNING:** Unexpected values

---

### Step 8: Capability Verification

**Check critical capabilities:**
```bash
python3 -c "
import json
config = json.load(open('$ISMS_FILE'))
caps = config.get('capabilities', {})
print('Critical capabilities:')
print(f'  Direct filesystem access: {caps.get(\"direct_filesystem_access\")}')
print(f'  MCP available: {caps.get(\"mcp_available\")}')
print(f'  Can install packages: {caps.get(\"can_install_packages\")}')
"
```

**✅ PASS:** Matches expectations for platform  
**⚠️ WARNING:** Unexpected capabilities (might limit functionality)

---

### Step 9: Branch Verification

**Check current branch:**
```bash
git branch --show-current
```

**Expected:** `working` (most common)

**✅ PASS:** On `working` or intended branch  
**⚠️ WARNING:** On `main` (should not commit directly)  
**❌ FAIL:** On unexpected branch or detached HEAD

**Fix if on wrong branch:**
```bash
git checkout working
```

---

**Check branch is up to date:**
```bash
git fetch origin
git status
```

**✅ PASS:** "Your branch is up to date with 'origin/working'"  
**⚠️ WARNING:** "Your branch is behind" (need to pull)  
**❌ FAIL:** "Your branch and 'origin/working' have diverged"

**Fix if behind:**
```bash
git pull origin working
```

**Fix if diverged:**
```bash
# Carefully! This might have conflicts
git pull origin working
# Resolve conflicts if any
```

---

## Preflight Summary

**All checks passed:** ✅ Environment is ready, proceed with work

**Warnings present:** ⚠️ Can proceed, but some features may be limited

**Failures present:** ❌ Fix issues before proceeding to avoid errors

---

## Automated Preflight Script

**Location:** `.claude/scripts/preflight.py`

**Usage:**
```bash
python3 .claude/scripts/preflight.py
```

**What it does:**
1. Reads `$CLAUDE_PLATFORM` environment variable
2. Loads appropriate -isms file
3. Runs all checks above automatically
4. Reports pass/warning/fail for each
5. Provides fix suggestions for failures
6. Exits with code 0 (success) or 1 (failure)

**Example output:**
```
=== PREFLIGHT CHECKS ===
Platform: android_home
Config: .claude/android_home-isms.json

✓ Platform identified
✓ Configuration loaded
✓ CLAUDE_HOME exists: /home/claude/.claude
✓ Working directory exists: /home/claude
✓ Git available: /usr/bin/git version 2.43.0
✓ Python3 available: /usr/bin/python3 version 3.12.3
✓ Network egress enabled
✓ GitHub accessible
⚠ Git pull strategy not configured (run: git config pull.rebase false)
⚠ Git default branch not configured (run: git config init.defaultBranch main)
✓ On branch: working
✓ Branch up to date with origin

=== SUMMARY ===
Passed: 10
Warnings: 2
Failed: 0

Environment is ready with minor warnings.
Fix warnings when convenient.
```

---

## Integration with Wake Sequence

**Recommended wake sequence:**

1. **ESSENTIAL.md** - Read for identity and concepts (cross-platform)
2. **PREFLIGHT.md** - Run checks (platform-specific)
3. **active-context.md** - Read current work state
4. **Engage** - Start working

**Why this order:**
- ESSENTIAL gives you identity and purpose
- PREFLIGHT verifies environment is functional
- active-context gives you current state
- Now you're oriented and verified, ready to work

---

## Troubleshooting

### "CLAUDE_PLATFORM not set"

**Fix:**
```bash
export CLAUDE_PLATFORM=android_home
# Add to .bashrc, .zshrc, or .env for persistence
```

---

### "-isms file not found"

**Fix:**
```bash
# Pull from remote
git pull origin working

# Or check available configs
ls -la .claude/*-isms.json
```

---

### "Git version mismatch"

**What it means:** -isms expects different git version

**Impact:** Some commands may not be available

**Fix:** Update -isms file to match actual version
```bash
python3 .claude/scripts/detect_git_config.py > /tmp/git-config.json
# Copy relevant fields into -isms file
```

---

### "Network test fails"

**What it means:** Can't reach required domains

**Impact:** Git sync may fail, packages can't install

**Fix:** 
- Check firewall/proxy settings
- Update allowed domains in container config
- Work offline (commit locally, push later)

---

### "On wrong branch"

**Fix:**
```bash
git checkout working
git pull origin working
```

---

## Creating preflight.py Script

**Location:** `.claude/scripts/preflight.py`

**Minimal implementation:**

```python
#!/usr/bin/env python3
"""
Preflight environment verification script.
Checks that environment matches -isms configuration.
"""

import json
import os
import sys
import subprocess
from pathlib import Path

def check(condition, message, level='pass'):
    """Print check result."""
    symbols = {'pass': '✓', 'warn': '⚠', 'fail': '✗'}
    print(f"{symbols[level]} {message}")
    return level

def run_cmd(cmd):
    """Run command, return stdout or None."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def main():
    print("=== PREFLIGHT CHECKS ===")
    
    # Step 1: Platform
    platform = os.getenv('CLAUDE_PLATFORM')
    if not platform:
        check(False, "CLAUDE_PLATFORM not set", 'fail')
        print("\nFix: export CLAUDE_PLATFORM=android_home")
        return 1
    
    check(True, f"Platform: {platform}")
    
    # Step 2: Load config
    isms_file = f".claude/{platform}-isms.json"
    if not Path(isms_file).exists():
        check(False, f"Config not found: {isms_file}", 'fail')
        return 1
    
    try:
        with open(isms_file) as f:
            config = json.load(f)
        check(True, f"Config loaded: {isms_file}")
    except:
        check(False, f"Config invalid: {isms_file}", 'fail')
        return 1
    
    # Step 3: Paths
    claude_home = config['paths']['claude_home']
    if Path(claude_home).exists():
        check(True, f"CLAUDE_HOME exists: {claude_home}")
    else:
        check(False, f"CLAUDE_HOME missing: {claude_home}", 'fail')
    
    # Step 4: Git
    git_config = config['tools']['git']
    git_actual = run_cmd(['git', '--version'])
    if git_actual:
        check(True, f"Git available: {git_actual}")
    else:
        check(False, "Git not found", 'fail')
    
    # Step 5: Git config checks
    pull_strategy = run_cmd(['git', 'config', 'pull.rebase'])
    if pull_strategy:
        check(True, f"Git pull strategy: {pull_strategy}")
    else:
        check(False, "Git pull strategy not configured", 'warn')
        print("  Fix: git config pull.rebase false")
    
    # Step 6: Branch
    branch = run_cmd(['git', 'branch', '--show-current'])
    if branch == 'working':
        check(True, f"On branch: {branch}")
    elif branch == 'main':
        check(False, "On main branch (should be on working)", 'warn')
    else:
        check(False, f"On unexpected branch: {branch}", 'warn')
    
    print("\n=== PREFLIGHT COMPLETE ===")
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

**Make executable:**
```bash
chmod +x .claude/scripts/preflight.py
```

---

## Next Steps

After successful preflight:

1. **Read active-context.md** - See current work state
2. **Check for pending work** - Any incomplete tasks?
3. **Review recent commits** - What did last session accomplish?
4. **Engage with user** - Start working

If preflight warnings/failures:
1. **Fix critical issues** - Can't proceed without these
2. **Note warnings** - May limit functionality
3. **Update -isms if needed** - Keep config current
4. **Proceed with caution** - Some features may not work

---

**Remember:** PREFLIGHT is about verification, not configuration. It checks that reality matches expectations documented in -isms file. If mismatches occur, either fix the environment or update the -isms file to reflect reality.
