# Git Version Tracking Implementation Summary

**Date:** February 28, 2026
**Session:** Android Testing & Architecture Design
<<<<<<< HEAD
**Authors:** the Architect (the Architect) & Vector (Shepard)
=======
**Authors:** the Architect (the Architect) & Vector (Shepard)
>>>>>>> working

---

## Problem Statement

Git's UI changes frequently across versions. Commands that work on one machine fail on another. Documentation that says "run git switch" is useless if you're on git 2.17.

**Example pain points:**
- `git switch` doesn't exist before 2.23
- Pull strategy warnings added in 2.27
- Default branch name changed from `master` to `main` around 2.28
- Muscle memory breaks when moving between systems

---

## Solution: Two-Part Approach

### Part 1: Documentation (Human-Facing)

**File:** `foolproof-git-pr-workflow.md`

**Added Section:** "Git Version Differences (What Commands Actually Work)"

**Contents:**
- Version detection instructions
- Command compatibility table (old vs new syntax)
- Version-specific behavior explanations
- Practical advice for multi-version environments
- Default branch name confusion guide

**Key Features:**
- Shows exactly which commands work on which versions
- Explains WHY commands changed (not just "use this instead")
- Provides fallback strategies
- Includes table of old→new command mappings

<<<<<<< HEAD
**Use Case:** the Architect reads this when confused about which git command to use on which machine.
=======
**Use Case:** the Architect reads this when confused about which git command to use on which machine.
>>>>>>> working

---

### Part 2: Machine-Readable Config (Instance-Facing)

**File:** `git-branch-strategy-and-isms-schema.md`

**Added:** Enhanced git tool configuration in -isms file schema

**Schema Fields:**
```json
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
  "notes": "..."
}
```

**Benefits:**
- Instance knows which commands are available
- Scripts adapt to environment automatically
- No guessing about version capabilities
- Self-documenting (notes field explains)

**Use Case:** Instance reads -isms file at wake and knows whether to use `git switch` or `git checkout`.

---

### Part 3: Automation Script

**File:** `detect_git_config.py`

**Purpose:** Automatically generate git configuration block for -isms files

**Features:**
- Detects git version and parses into major.minor.patch
- Checks for modern commands (switch/restore)
- Reads git config (pull strategy, default branch)
- Checks for advanced features (worktrees)
- Outputs clean JSON for copy-paste into -isms file
- Warns about missing configurations

**Usage:**
```bash
python3 detect_git_config.py
# Copy output into -isms file's "tools.git" section
```

**Example Output:**
```json
{
  "available": true,
  "path": "/usr/bin/git",
  "version": "2.43.0",
  "version_major": 2,
  "version_minor": 43,
  "version_patch": 0,
  "has_switch_command": true,
  "has_restore_command": true,
  "default_pull_strategy": "not_configured",
  "default_branch": "not_configured",
  "supports_worktrees": true,
  "notes": "Git 2.43.0; modern commands available (switch/restore); WARN: pull strategy not configured; worktrees supported"
}
```

---

## Version Milestones Documented

**Git 2.23 (August 2019):**
- Added `git switch` (clearer branch switching)
- Added `git restore` (clearer file restoration)
- Backward compatible - old commands still work

**Git 2.27 (June 2020):**
- Pull strategy warning for divergent branches
- Requires explicit configuration
- Annoying but well-intentioned

**Git 2.28 (July 2020):**
- Configurable default branch name
- Enables `main` instead of `master`
- Source of much confusion

**Git 2.43 (Current):**
- Modern, stable
- All features present
- Recommended version

---

## Integration with Branch Strategy

The git version tracking integrates seamlessly with the multi-branch sync architecture:

1. **Each branch's -isms file** declares its git capabilities
2. **Instances read -isms** at wake to know environment
3. **Scripts adapt** to use correct commands
4. **Workflows document** version-specific gotchas
5. **Detection script** automates -isms generation

**Example Flow:**

```
Android Wake
    ↓
Load android_home-isms.json
    ↓
Read git.version = "2.43.0"
Read git.has_switch_command = true
    ↓
Use modern commands in scripts
    ↓
"git switch main" works perfectly
```

Versus:

```
Old Linux Wake
    ↓
Load linux_home-isms.json
    ↓
Read git.version = "2.17.1"
Read git.has_switch_command = false
    ↓
Use legacy commands in scripts
    ↓
"git checkout main" works perfectly
```

---

## Command Compatibility Table

| Operation | Git < 2.23 | Git 2.23+ | Status |
|-----------|-----------|-----------|--------|
| Switch branch | `git checkout main` | `git switch main` | Both work on 2.23+ |
| Restore file | `git checkout -- file.txt` | `git restore file.txt` | Both work on 2.23+ |
| Create branch | `git checkout -b new` | `git switch -c new` | Both work on 2.23+ |
| Discard changes | `git checkout -- .` | `git restore .` | Both work on 2.23+ |

**Key Insight:** Old commands still work on new git. New commands don't work on old git. When in doubt, use old commands in scripts for maximum compatibility.

---

## Files Delivered

1. **foolproof-git-pr-workflow.md** (Updated)
   - Added "Git Version Differences" section
   - Human-readable guide to version quirks
   - Command compatibility reference

2. **git-branch-strategy-and-isms-schema.md** (Updated)
   - Enhanced git tool schema
   - Added "Git Version Tracking" section
   - Instance usage patterns
   - Detection methodology

3. **detect_git_config.py** (New)
   - Standalone detection script
   - Generates JSON for -isms files
   - Warns about missing configs
   - Tested and working on Android

---

## Next Steps

### Immediate (Before Creating sync-private Repo)

1. **Run detection script on each environment:**
   ```bash
   # On Windows (home)
   python detect_git_config.py > home-git-config.json
   
   # On Linux (linux_home)
   python detect_git_config.py > linux-git-config.json
   
   # On Android (android_home) - already done
   # Results saved in this session
   ```

2. **Incorporate into -isms files:**
   - Copy JSON output into appropriate section
   - Verify paths are correct
   - Add any platform-specific notes

3. **Configure git if needed:**
   ```bash
   # If pull strategy not set:
   git config --global pull.rebase false
   
   # If default branch not set:
   git config --global init.defaultBranch main
   ```

### During sync-private Setup

4. **Document git version per branch** in metadata
5. **Test workflows on each environment** to verify commands work
6. **Update workflow doc** if any environment-specific issues found

### Ongoing Maintenance

7. **Add detection to wake script** (optional):
   ```bash
   # In wake.sh
   python3 .claude/scripts/detect_git_config.py > /tmp/git-check.json
   # Compare with -isms file, warn if mismatch
   ```

8. **Update -isms when git is upgraded** on any system
9. **Test new git versions** in dev_home before deploying

---

## Benefits Realized

<<<<<<< HEAD
**For the Architect:**
=======
**For the Architect:**
>>>>>>> working
- Clear guide to which commands work where
- No more "why doesn't git switch work?" confusion
- Version-specific gotchas documented once
- Can reference table when writing scripts

**For Instances:**
- Know environment capabilities at wake
- Adapt behavior to available commands
- No hardcoded assumptions about git version
- Self-documenting through -isms file

**For Architecture:**
- Extensible to other tool version tracking
- Same pattern works for python, npm, etc.
- Machine-readable AND human-readable
- Low maintenance (update when git upgrades)

---

## Pattern for Other Tools

This git version tracking pattern can be applied to any tool where version matters:

**Python:**
```json
"python3": {
  "version": "3.12.3",
  "version_major": 3,
  "version_minor": 12,
  "has_match_statement": true,  // 3.10+
  "has_walrus_operator": true,  // 3.8+
  "f_string_debug": true        // 3.8+
}
```

**Node/npm:**
```json
"npm": {
  "version": "10.8.2",
  "node_version": "20.11.0",
  "has_workspaces": true,       // npm 7+
  "has_overrides": true         // npm 8.3+
}
```

The -isms file becomes a complete environment capability manifest.

---

## Test Results

**Environment:** Android (Ubuntu 24 container)
**Git Version:** 2.43.0
**Script Status:** ✅ Tested and working

**Script Output:**
```json
{
  "available": true,
  "path": "/usr/bin/git",
  "version": "2.43.0",
  "version_major": 2,
  "version_minor": 43,
  "version_patch": 0,
  "has_switch_command": true,
  "has_restore_command": true,
  "default_pull_strategy": "not_configured",
  "default_branch": "not_configured",
  "supports_worktrees": true,
  "notes": "Git 2.43.0; modern commands available (switch/restore); WARN: pull strategy not configured; worktrees supported"
}
```

**Warnings Generated:**
- Pull strategy not configured (needs: `git config pull.rebase false`)
- Default branch not configured (needs: `git config init.defaultBranch main`)

Both warnings are correct and actionable.

---

## Conclusion

Git's UI instability is now documented and tracked. Two-part solution (human docs + machine config) addresses the problem from both sides. Detection script makes it easy to maintain. Pattern is extensible to other tools.

**The elegance:** Version tracking is declarative (in -isms file) rather than discovered (by trial-and-error at runtime). Instance knows capabilities before attempting operations.

<<<<<<< HEAD
**the Architect's request:** "It would help if the UI didn't change so often."
=======
**the Architect's request:** "It would help if the UI didn't change so often."
>>>>>>> working
**Our response:** Can't fix git's design, but we can document and adapt to it systematically.

Problem understood. Problem addressed. Ready to implement.
