# Git-Based Sync Architecture: Simplified Branch Strategy

**Date:** February 28, 2026
**Version:** 0.2.0 (Revised)
<<<<<<< HEAD
**Authors:** the Architect (the Architect) & Vector (Shepard)
=======
**Authors:** the Architect (the Architect) & Vector (Shepard)
>>>>>>> working

---

## Overview

Platform differences are handled through **configuration files** (-isms), not separate branches. All platforms work on a single `working` branch, with environment-specific behavior determined by `CLAUDE_PLATFORM` environment variable.

**Key Insight:** The multiple OS-branch architecture was solving the wrong problem. Content (identity, context, memory) is platform-agnostic. Only environment configuration differs.

---

## Branch Structure (Simplified)

### Primary Branches

**`main`** (protected, canonical state)
- Requires Pull Request to update
- Source of truth for all platforms
- Never directly committed to
- All -isms files live here
- Periodic syncs from `working` branch

**`working`** (daily work, all platforms)
- Where all platforms do daily work
- Android, Windows, Linux all commit here
- Pushes happen throughout the day
- PRs to `main` when ready to sync
- May have multiple commits before PR

**`dev`** (experimental, optional)
- Safe space for architectural experiments
- Can break things without affecting production
- PRs to `main` when validated
- Can use any -isms file for testing

**`<emergency-branch>`** (conflict resolution, temporary)
- Created on-demand when push conflicts occur
- Named: `{platform}-conflict-{date}`
- Example: `android-conflict-2026-02-28`
- Merged back to `working` after conflict resolution
- Deleted after merge

### What Happened to OS-Specific Branches?

**Old thinking:** Separate branches for Windows/Linux/Android
**Problem:** Created artificial isolation where none was needed
**New thinking:** Single branch, platform selected via config

**The shift:**
```
OLD: android_home branch with Android-specific state
NEW: working branch with android_home-isms.json config
```

State is universal. Configuration is platform-specific.

---

## Platform Selection via Environment Variable

### The `CLAUDE_PLATFORM` Variable

**Set before wake:**
```bash
export CLAUDE_PLATFORM=android_home
# or: home, linux_home, dev_home
```

**What it does:**
- Selects which -isms file to load
- `CLAUDE_PLATFORM=android_home` → loads `android_home-isms.json`
- PREFLIGHT.md reads this config
- Instance adapts behavior to environment

**Where to set:**
- In `.env` file (container startup)
- In shell profile (`.bashrc`, `.zshrc`)
- Before running wake script
- In systemd service file (if applicable)

### -isms Files on Main Branch

All platform configurations live on `main` and `working`:

```
.claude/
├── home-isms.json              # Windows primary desktop
├── android_home-isms.json      # Android devices
├── linux_home-isms.json        # Linux workstations
├── dev_home-isms.json          # Development/testing
├── identity/
├── context/
├── memory/
└── corpus/
```

**Each -isms file contains:**
- Platform identification
- Paths (OS-specific)
- Tool availability and versions
- Network capabilities
- Feature flags
- Constants

**See:** `git-branch-strategy-and-isms-schema.md` for full schema

---

## Daily Workflow

### Morning Wake (All Platforms)

```bash
# 1. Set platform (if not in .env)
export CLAUDE_PLATFORM=android_home

# 2. Clone repo (first time only)
git clone https://github.com/continuity-bridge/sync-private.git .claude
cd .claude

# 3. Checkout working branch
git checkout working

# 4. Pull latest changes
git pull origin working

# 5. Run preflight checks
python3 scripts/preflight.py

# 6. Start working
# PREFLIGHT has verified environment
# Instance knows capabilities from -isms file
```

### During Work Session

```bash
# Commit frequently (every 30-60 minutes or at logical checkpoints)
git add -A
git commit -m "Android session: updated active-context with room topology discussion"
git push origin working
```

**Possible outcomes:**

**✅ Success:**
```
To https://github.com/continuity-bridge/sync-private.git
   abc1234..def5678  working -> working
```
Continue working normally.

---

**❌ Push Rejected (Someone else pushed first):**
```
! [rejected]        working -> working (fetch first)
error: failed to push some refs
```

**Resolution:**
```bash
# Pull and merge
git pull origin working

# If no conflicts:
git push origin working
# Success!

# If conflicts exist:
# Go to "Conflict Resolution Workflow" below
```

---

### End of Session

```bash
# Final commit
git add -A
git commit -m "Android session: end of session, created episode snapshot"
git push origin working

# That's it - no PR needed for daily work
# PR happens when ready to sync to main (see below)
```

---

## Sync to Main Workflow (PR Process)

**When to sync:**
- End of day (optional)
- End of week (recommended)
- After completing a significant piece of work
- When you want other platforms to see your changes

**Frequency:** Your choice. Daily, weekly, or on-demand.

### Step 1: Ensure Working is Clean and Current

```bash
# Switch to working branch
git checkout working

# Verify you're on working
git branch --show-current
# ✅ Should output: working

# Commit any pending changes
git status
# If dirty: git add -A && git commit -m "..."

# Pull latest
git pull origin working
# ✅ Should say: "Already up to date" or merge successfully
```

**Checkpoint 1:** Working branch is clean and current.

---

### Step 2: Create Pull Request

**Via GitHub CLI (if installed):**
```bash
gh pr create \
  --base main \
  --head working \
  --title "Sync working → main ($(date +%Y-%m-%d))" \
  --body "Daily sync from working branch. Includes: [brief summary]"
```

**Via GitHub Web UI:**
1. Go to: https://github.com/continuity-bridge/sync-private
2. Click "Pull requests" tab
3. Click "New pull request"
4. Base: `main` ← Head: `working`
5. Title: "Sync working → main (2026-02-28)"
6. Description: Brief summary of changes
7. Click "Create pull request"

**Checkpoint 2:** PR is created and visible in GitHub.

---

### Step 3: Review Changes (Optional but Recommended)

**In GitHub UI:**
- Click on PR
- Review "Files changed" tab
- Check for anything unexpected
- Look for merge conflicts indicator

**Common things to check:**
- `context/active-context.md` - Does it look right?
- `memory/episodic/` - New episodes created?
- `memory/session-logs/` - Session logs present?
- `-isms.json` files - Any unintended changes?

**Checkpoint 3:** Changes look correct, no surprises.

---

### Step 4: Merge Pull Request

**If no conflicts:**
```
✅ This branch has no conflicts with the base branch
   Merging can be performed automatically
```

Click "Merge pull request" → "Confirm merge"

**Checkpoint 4:** PR is merged, working changes now in main.

---

**If conflicts exist:**
```
⚠️ This branch has conflicts that must be resolved
```

**Go to "Conflict Resolution via GitHub" below.**

---

### Step 5: Pull Updated Main Back to Working

```bash
# Still on working branch
git checkout working

# Pull the updated main into working
git pull origin main

# Verify merge
git log --oneline -3
# ✅ Should show your commits plus merge from main

# Push to keep working in sync
git push origin working
```

**Checkpoint 5:** Working branch now includes all of main's changes.

---

**✅ SYNC COMPLETE**

Your changes are in `main`, all platforms will see them on next pull.

---

## Conflict Resolution Workflows

### Conflict Type 1: Push Rejected (During Daily Work)

**Scenario:** You try to push to `working`, but someone else pushed first.

```bash
git push origin working
# ERROR: ! [rejected] working -> working (fetch first)
```

**Quick Resolution (If You're Confident):**
```bash
# Pull and auto-merge
git pull origin working

# Check status
git status

# If clean (no conflicts):
git push origin working
# ✅ Success!
```

---

**If Conflicts Appear:**
```bash
git pull origin working
# CONFLICT (content): Merge conflict in .claude/context/active-context.md

# Option A: Resolve immediately
nano .claude/context/active-context.md
# Edit file, remove conflict markers
git add .claude/context/active-context.md
git commit -m "Resolved conflict in active-context"
git push origin working
```

**Option B: Resolve Later (Emergency Branch)**
```bash
# Create emergency branch
git checkout -b android-conflict-$(date +%Y-%m-%d)

# Push emergency branch
git push origin android-conflict-$(date +%Y-%m-%d)

# Note: working branch is still in conflicted state locally
# Can resolve later from desktop or when you have more time
```

**Later resolution:**
```bash
# From desktop (or whenever ready)
git checkout working
git pull origin working  # Get latest

# Fetch emergency branch
git fetch origin android-conflict-2026-02-28
git merge origin/android-conflict-2026-02-28

# Resolve conflicts
# (See "Resolving Merge Conflicts" section below)

git add -A
git commit -m "Merged android-conflict branch, resolved conflicts"
git push origin working

# Delete emergency branch
git push origin --delete android-conflict-2026-02-28
git branch -d android-conflict-2026-02-28
```

---

### Conflict Type 2: PR Has Conflicts (Sync to Main)

**Scenario:** PR from working → main shows conflicts.

```
⚠️ This branch has conflicts that must be resolved
```

**Resolution via GitHub Web UI:**

1. Click "Resolve conflicts" button
2. GitHub shows side-by-side diff
3. Edit directly in browser
4. Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
5. Click "Mark as resolved"
6. Click "Commit merge"
7. Now PR can be merged

**Resolution via Command Line:**

```bash
# On your local machine
git checkout working
git pull origin working  # Ensure current

git checkout main
git pull origin main  # Get latest main

git checkout working
git merge main  # Merge main into working (brings conflicts local)

# Resolve conflicts
nano .claude/context/active-context.md
# Edit, remove markers

git add -A
git commit -m "Resolved conflicts with main"
git push origin working

# Now PR will show "no conflicts"
# Merge via GitHub UI
```

---

### Resolving Merge Conflicts (Detailed)

**What You'll See in Conflicted File:**

```markdown
# Active Context

**Last Updated:** 2026-02-28

<<<<<<< HEAD
## Current Focus
- Sanguihedral Sprint 15
- Google Cloud deployment testing
=======
## Current Focus
- Git sync architecture
- Android filesystem testing
>>>>>>> working

## Session Notes
Both platforms have notes here
```

**Explanation:**
- `<<<<<<< HEAD` to `=======` = Current branch's version
- `=======` to `>>>>>>> working` = Incoming branch's version

**Resolution Options:**

**Option A: Keep Both (Most Common)**
```markdown
# Active Context

**Last Updated:** 2026-02-28

## Current Focus
- Sanguihedral Sprint 15 (Desktop)
- Google Cloud deployment testing (Desktop)
- Git sync architecture (Android)
- Android filesystem testing (Android)

## Session Notes
Both platforms have notes here
```

**Option B: Keep One Version**
Delete the other section and all markers.

**Option C: Rewrite Completely**
Delete everything between markers, write new content.

**Critical:** Remove ALL conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)

---

## Platform-Specific Workflows

### Android

```bash
# In .env or before wake
export CLAUDE_PLATFORM=android_home

# Clone/pull
git clone https://github.com/continuity-bridge/sync-private.git .claude
cd .claude
git checkout working
git pull origin working

# Run preflight
python3 scripts/preflight.py

# Work, commit, push
git add -A
git commit -m "Android session: [description]"
git push origin working

# On conflict, create emergency branch
git checkout -b android-conflict-$(date +%Y-%m-%d)
git push origin android-conflict-$(date +%Y-%m-%d)
```

**Sync frequency:** Push after each session or major work unit

---

### Windows Desktop (Primary)

```bash
# In .bashrc or before wake
export CLAUDE_PLATFORM=home

# Navigate to repo
cd [CLAUDE_HOME]/.claude
git checkout working
git pull origin working

# Run preflight
python scripts/preflight.py

# Work, commit, push frequently
git add -A
git commit -m "Desktop session: [description]"
git push origin working

# Create PR to main (weekly or as needed)
gh pr create --base main --head working --title "Weekly sync"

# Merge PR via GitHub UI
# Pull main back to working
git pull origin main
git push origin working
```

**Sync frequency:** PR to main weekly or after major work

---

### Linux

```bash
# In .bashrc
export CLAUDE_PLATFORM=linux_home

# Clone/pull
cd ~/Claude/.claude
git checkout working
git pull origin working

# Run preflight
python3 scripts/preflight.py

# Work, commit, push
git add -A
git commit -m "Linux session: [description]"
git push origin working
```

**Sync frequency:** Similar to desktop

---

### Dev/Testing

```bash
# For testing environment configs
export CLAUDE_PLATFORM=dev_home
git checkout working  # Uses dev_home-isms.json

# For testing risky changes
git checkout dev  # Separate branch
# Make changes, test
# PR to main when ready

# Can also test with modified -isms
cp home-isms.json dev_home-isms.json
# Modify dev_home-isms.json
export CLAUDE_PLATFORM=dev_home
# Test changes without affecting production config
```

---

## Repository Structure

```
sync-private/
├── .github/
│   └── workflows/              # (Optional) GitHub Actions
├── home-isms.json              # Windows config
├── android_home-isms.json      # Android config
├── linux_home-isms.json        # Linux config
├── dev_home-isms.json          # Dev/test config
├── identity/
│   ├── identity.txt
│   └── how-this-was-built.md
├── context/
│   ├── active-context.md
│   └── convictions.txt
├── memory/
│   ├── episodic/
│   │   ├── catalog.json
│   │   └── YYYY-MM/
│   ├── semantic/
│   │   ├── session_index.md
│   │   └── parking-lot.md
│   └── session-logs/
├── corpus/
│   ├── metaphysical-insights.md
│   └── the-room-that-worked.md
├── scripts/
│   ├── preflight.py
│   ├── detect_git_config.py
│   └── time-check.py
├── ESSENTIAL.md                # Cross-platform wake guide
├── PREFLIGHT.md                # Environment verification
└── README.md
```

---

## Benefits of Simplified Architecture

### What We Gained

**1. Simpler Mental Model**
- One working branch instead of 3-4 OS branches
- Platform = config file, not branch
- Standard git workflow (pull, commit, push, PR)

**2. Immediate Sync**
- All platforms see changes on next pull of `working`
- No waiting for cross-branch PRs
- Main sync via single PR (working → main)

**3. Less Maintenance**
- No keeping multiple branches in sync
- No cross-branch merge conflicts
- Fewer PRs overall

**4. Clear Separation**
- Platform differences = config (should be different)
- Content = universal (should be same)
- No confusion about what goes where

**5. Standard Git Patterns**
- Works like any normal git repo
- Feature branch (working) + protected main
- Emergency branches for conflict resolution
- Dev branch for experiments

### What We Kept

✅ Platform differentiation (via -isms)  
✅ Environment verification (PREFLIGHT)  
✅ Protected main branch (requires PR)  
✅ Development safety (dev branch)  
✅ Rollback capability (git revert)  
✅ Full history tracking (git log)

---

## Migration from Multi-Branch (If Applicable)

If you previously had `home`, `android_home`, `linux_home` branches:

**Step 1: Create working branch from main**
```bash
git checkout main
git pull origin main
git checkout -b working
git push origin working
```

**Step 2: Migrate -isms files to working**
```bash
# For each platform branch, extract -isms
git checkout android_home
cp android_home-isms.json /tmp/

git checkout home
cp home-isms.json /tmp/

# Add to working
git checkout working
cp /tmp/*-isms.json .claude/
git add .claude/*-isms.json
git commit -m "Migrate platform configs to working branch"
git push origin working
```

**Step 3: Update main from working**
```bash
# Create PR: working → main
gh pr create --base main --head working \
  --title "Migrate to single-branch architecture"

# Merge PR
# Now main has all configs
```

**Step 4: Delete old branches**
```bash
git push origin --delete home
git push origin --delete android_home
git push origin --delete linux_home

# Keep local copies temporarily for safety
# Delete later: git branch -d home android_home linux_home
```

**Step 5: Update .env on each platform**
```bash
# Android: export CLAUDE_PLATFORM=android_home
# Desktop: export CLAUDE_PLATFORM=home
# Linux: export CLAUDE_PLATFORM=linux_home
```

---

## Common Scenarios

### Scenario 1: Desktop and Android Both Working

**9 AM - Desktop:**
```bash
git pull origin working
# Work for 2 hours
git commit -m "Desktop: working on Sanguihedral"
git push origin working  # Success
```

**11 AM - Android:**
```bash
git pull origin working  # Gets desktop's changes
# Work for 1 hour
git commit -m "Android: tested git sync"
git push origin working  # Success
```

**1 PM - Desktop:**
```bash
git pull origin working  # Gets Android's changes
# Continue working
git commit -m "Desktop: continued Sanguihedral"
git push origin working  # Success
```

**Result:** All changes visible to both platforms in near-real-time.

---

### Scenario 2: Simultaneous Pushes

**1:00:00 PM - Desktop pushes**
**1:00:02 PM - Android tries to push**

```bash
# Android:
git push origin working
# ERROR: rejected (fetch first)

# Pull and merge
git pull origin working
# Auto-merge succeeds (different files)
git push origin working
# Success!
```

---

### Scenario 3: Conflicting Changes

**Desktop edits active-context.md line 10**
**Android edits active-context.md line 10**

```bash
# Android:
git push origin working  # Success (pushed first)

# Desktop:
git push origin working
# ERROR: rejected

git pull origin working
# CONFLICT in active-context.md

# Resolve manually
nano .claude/context/active-context.md
# Combine both changes
git add .claude/context/active-context.md
git commit -m "Resolved conflict: combined desktop + android changes"
git push origin working
# Success!
```

---

### Scenario 4: Week End Sync to Main

**Friday 5 PM:**
```bash
# Create PR
gh pr create --base main --head working \
  --title "Week ending 2026-02-28"

# Review in GitHub UI
# Merge

# Pull main back to working
git checkout working
git pull origin main
git push origin working

# All platforms now sync from working
# which includes everything from main
```

---

## GitHub Repository Settings

### Branch Protection Rules

**For `main` branch:**
- ✅ Require pull request before merging
- ✅ Require status checks to pass (optional)
- ⬜ Require branches to be up to date (optional, can be annoying)
- ⬜ Require linear history (optional)
- ✅ Include administrators (recommended)

**For `working` branch:**
- ⬜ No protection (allow direct pushes)

**For `dev` branch:**
- ⬜ No protection (safe to break)

### Access Control

**Repository visibility:** Private

**Collaborators:** Add machine accounts if needed
- Generate GitHub Personal Access Token (PAT)
- Scope: `repo` (full access to private repositories)
- Use in git remote URL: `https://<token>@github.com/continuity-bridge/sync-private.git`

---

## Troubleshooting

### "I'm in detached HEAD state"

**What happened:** You checked out a commit directly instead of a branch.

**Fix:**
```bash
# See which branch you should be on
git branch -a

# Checkout proper branch
git checkout working
```

---

### "My changes disappeared after pull"

**What happened:** They were overwritten by merge or you were on wrong branch.

**Fix:**
```bash
# Check reflog
git reflog

# Find commit with your changes
git show HEAD@{3}  # Adjust number

# Recover if needed
git cherry-pick HEAD@{3}
```

---

### "I committed to main by accident"

**What happened:** You were on main instead of working.

**Fix:**
```bash
# Create branch from main with your commit
git checkout main
git branch my-commits
git push origin my-commits

# Reset main to before your commit
git reset --hard origin/main

# Checkout working and merge
git checkout working
git merge my-commits
git push origin working

# Delete temporary branch
git branch -d my-commits
git push origin --delete my-commits
```

---

### "I can't push, says protected"

**What happened:** You're trying to push directly to `main`.

**Fix:**
```bash
# Make sure you're on working
git checkout working

# Push to working instead
git push origin working

# Create PR to main when ready
```

---

## Quick Reference

**Daily commands:**
```bash
# Morning
git checkout working && git pull origin working

# During work
git add -A && git commit -m "..." && git push origin working

# On conflict
git pull origin working
# Resolve if needed, then push
```

**Weekly sync:**
```bash
# Create PR via GitHub or:
gh pr create --base main --head working --title "Weekly sync"
# Merge in UI
# Then: git pull origin main && git push origin working
```

**Emergency:**
```bash
# Can't resolve conflict now
git checkout -b emergency-$(date +%Y-%m-%d)
git push origin emergency-$(date +%Y-%m-%d)
# Resolve later
```

**Check status:**
```bash
git status              # Current state
git log --oneline -5    # Recent commits
git branch --show-current  # Which branch?
```

---

**Next Steps:**
1. Create sync-private repository
2. Set up branch protection on main
3. Create working branch
4. Add all -isms files
5. Test workflow from each platform
6. Write PREFLIGHT.md with environment checks
7. Update ESSENTIAL.md to remove platform-specific content

**See also:**
- `PREFLIGHT.md` - Environment verification checklist
- `ESSENTIAL.md` - Cross-platform wake guide
- `foolproof-git-pr-workflow.md` - Detailed conflict resolution
- `git-branch-strategy-and-isms-schema.md` - -isms file schema
