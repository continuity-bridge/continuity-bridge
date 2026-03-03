# Git Branch Sync: Foolproof PR Workflow

**Critical Rule:** Follow these steps IN ORDER. Do not skip. Do not improvise. Each step has a checkpoint to verify you're in the right state before proceeding.

---

## Pre-Flight Check

Before starting ANY sync operation:

```bash
# 1. Check which branch you're on
git branch --show-current

# 2. Check if you have uncommitted changes
git status

# 3. Check if you're up to date with remote
git fetch origin
git status
```

**STOP CONDITIONS:**
- ❌ If `git status` shows uncommitted changes → Commit or stash them first
- ❌ If you're not on the branch you think you are → `git checkout <correct-branch>`
- ❌ If `git status` says "Your branch is behind" → `git pull` first

**PROCEED ONLY IF:**
- ✅ `git status` says "nothing to commit, working tree clean"
- ✅ `git status` says "Your branch is up to date with 'origin/<branch>'"
- ✅ You're on the branch you intend to work on

---

## Workflow 1: Sync Working Branch to Main (Most Common)

**Use Case:** You've been working on `android_home` (or `home`, `linux_home`, etc.) and want to merge your changes into `main`.

**Time Required:** 5-10 minutes
**Difficulty:** Medium
**Risk:** Medium (can mess up if done out of order)

### Step 1: Ensure Your Working Branch is Clean and Current

```bash
# You should be on your working branch (e.g., android_home)
git checkout android_home

# Verify you're on the right branch
git branch --show-current
# ✅ Should output: android_home

# Get latest from remote
git fetch origin

# Pull any remote changes to your branch
git pull origin android_home
# ✅ Should say: "Already up to date" or show merged changes

# Verify clean state
git status
# ✅ Should say: "nothing to commit, working tree clean"
```

**Checkpoint 1:** You are on `android_home`, it's clean, and up to date with remote.

---

### Step 2: Update Your Local `main` from Remote

**Why:** Your local `main` might be stale. We need it current before merging.

```bash
# Switch to main
git checkout main
# ✅ Should say: "Switched to branch 'main'"

# Verify you're on main
git branch --show-current
# ✅ Should output: main

# Pull latest main from remote
git pull origin main
# ✅ Should say: "Already up to date" or show merged changes

# Verify clean state
git status
# ✅ Should say: "nothing to commit, working tree clean"
```

**Checkpoint 2:** You are on `main`, it's clean, and synchronized with remote.

---

### Step 3: Merge Working Branch INTO Main (Local)

**Why:** We merge locally first to handle any conflicts in a safe environment.

```bash
# You should still be on main from Step 2
git branch --show-current
# ✅ Should output: main

# Merge android_home into main (local merge)
git merge android_home --no-ff -m "Merge android_home into main (2026-02-28)"

# Check what happened
git status
```

**Possible Outcomes:**

**OUTCOME A: Clean Merge (Best Case)**
```
Already up-to-date.
```
OR
```
Merge made by the 'recursive' strategy.
 .claude/context/active-context.md | 5 +++--
 1 file changed, 3 insertions(+), 2 deletions(-)
```
✅ **Checkpoint 3A:** Merge successful, no conflicts. Proceed to Step 4.

---

**OUTCOME B: Merge Conflicts (Needs Resolution)**
```
Auto-merging .claude/context/active-context.md
CONFLICT (content): Merge conflict in .claude/context/active-context.md
Automatic merge failed; fix conflicts and then commit the result.
```
❌ **STOP!** You have conflicts. Go to **Conflict Resolution Workflow** below before proceeding.

---

### Step 4: Push Merged Main to Remote

**Why:** Make the merge official by pushing to GitHub.

```bash
# Verify you're still on main
git branch --show-current
# ✅ Should output: main

# Verify merge was successful and committed
git log --oneline -1
# ✅ Should show: something like "Merge android_home into main (2026-02-28)"

# Push to remote
git push origin main

# Verify push succeeded
git status
# ✅ Should say: "Your branch is up to date with 'origin/main'"
```

**Checkpoint 4:** Main branch is now updated on both local and remote with your changes.

---

### Step 5: Return to Your Working Branch

**Why:** You don't want to accidentally work on `main` directly.

```bash
# Switch back to your working branch
git checkout android_home

# Verify you're on the right branch
git branch --show-current
# ✅ Should output: android_home

# Pull the updated main (optional but recommended)
git pull origin main
# This brings any other changes from main into your branch
```

**Checkpoint 5:** You're back on your working branch, and it's aware of the main branch updates.

---

**✅ WORKFLOW COMPLETE**

Your changes from `android_home` are now merged into `main` and pushed to GitHub.

---

## Conflict Resolution Workflow

**You'll be here if Step 3 showed "CONFLICT" messages.**

### Understanding What Happened

Git tried to merge your branch into `main` but found changes in the same lines of the same files on both branches. It doesn't know which version to keep, so it marks the conflict and stops.

---

### Step CR-1: Identify Conflicted Files

```bash
# Show which files have conflicts
git status

# Look for lines like:
# both modified:   .claude/context/active-context.md
```

**Checkpoint CR-1:** You know which file(s) need manual editing.

---

### Step CR-2: Open and Resolve Each Conflicted File

```bash
# Open the file in your editor
# Example for active-context.md:
code .claude/context/active-context.md
# or nano, vim, notepad++, whatever you use
```

**What You'll See:**

```markdown
# Active Context

**Last Updated:** 2026-02-28 by Vector (Shepard)

<<<<<<< HEAD
## Current Focus
- Sanguihedral Sprint 15 completion
- Testing Google Cloud deployment
=======
## Current Focus  
- Git branch sync architecture implementation
- Android filesystem access testing
>>>>>>> android_home

## Session Notes
- Both branches worked here
```

**Explanation:**
- `<<<<<<< HEAD` to `=======` = Current state of `main` (the branch you're merging INTO)
- `=======` to `>>>>>>> android_home` = Your working branch changes

---

### Step CR-3: Choose How to Resolve

**Option A: Keep Your Branch's Version**
Delete the HEAD section and conflict markers:

```markdown
# Active Context

**Last Updated:** 2026-02-28 by Vector (Shepard)

## Current Focus  
- Git branch sync architecture implementation
- Android filesystem access testing

## Session Notes
- Both branches worked here
```

**Option B: Keep Main's Version**
Delete your branch section and conflict markers:

```markdown
# Active Context

**Last Updated:** 2026-02-28 by Vector (Shepard)

## Current Focus
- Sanguihedral Sprint 15 completion
- Testing Google Cloud deployment

## Session Notes
- Both branches worked here
```

**Option C: Combine Both (Most Common)**
Keep both sets of changes, merge them logically:

```markdown
# Active Context

**Last Updated:** 2026-02-28 by Vector (Shepard)

## Current Focus
- Sanguihedral Sprint 15 completion
- Testing Google Cloud deployment
- Git branch sync architecture implementation (Android)
- Android filesystem access testing (Android)

## Session Notes
- Both branches worked here
- Desktop focused on Sanguihedral Sprint 15
- Android tested git sync architecture
```

**IMPORTANT:** Remove ALL conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)

---

### Step CR-4: Mark Conflict as Resolved

```bash
# After editing and saving the file
git add .claude/context/active-context.md

# Verify conflict is resolved
git status
# ✅ Should show file under "Changes to be committed"
# ✅ Should NOT show file under "Unmerged paths"
```

**Checkpoint CR-4:** Conflict is resolved and staged.

---

### Step CR-5: Commit the Merge

```bash
# Complete the merge with a commit
git commit -m "Resolved merge conflict in active-context.md: Combined desktop and Android changes"

# Verify commit succeeded
git log --oneline -1
# ✅ Should show your merge conflict resolution commit
```

**Checkpoint CR-5:** Merge conflict is resolved and committed.

---

### Step CR-6: Return to Main Workflow

✅ **Now return to Step 4 of the main workflow** (Push Merged Main to Remote)

Your merge is complete, conflicts are resolved. Continue pushing to remote.

---

## Workflow 2: Sync Main to Working Branch (Reverse)

**Use Case:** `main` has been updated (maybe by another branch merging) and you want those changes in your working branch.

**Time Required:** 2-3 minutes
**Difficulty:** Low
**Risk:** Low (safe operation)

### Step 1: Ensure Your Working Branch is Clean

```bash
# Switch to your working branch
git checkout android_home

# Verify you're on the right branch
git branch --show-current
# ✅ Should output: android_home

# Verify clean state
git status
# ✅ Should say: "nothing to commit, working tree clean"
```

**Checkpoint 1:** You're on your working branch and it's clean.

---

### Step 2: Pull Main into Your Branch

```bash
# While on android_home, pull from main
git pull origin main

# Check what happened
git status
```

**Possible Outcomes:**

**OUTCOME A: Clean Merge**
```
From https://github.com/continuity-bridge/sync-private
 * branch            main       -> FETCH_HEAD
Updating abc1234..def5678
Fast-forward
 .claude/context/active-context.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
```
✅ **Checkpoint 2A:** Main's changes are now in your branch. You're done!

---

**OUTCOME B: Conflicts**
```
CONFLICT (content): Merge conflict in .claude/context/active-context.md
```
❌ **STOP!** Go to **Conflict Resolution Workflow** (same as above, but you're on your working branch instead of main).

After resolving:
```bash
git add <conflicted-files>
git commit -m "Merged main into android_home, resolved conflicts"
git push origin android_home
```

---

**✅ WORKFLOW COMPLETE**

Your working branch now has all of main's changes.

---

## Workflow 3: Force Reset Working Branch to Match Main (Nuclear Option)

**Use Case:** Your branch is completely borked and you want to throw it away and start fresh from main.

**⚠️ WARNING:** This DELETES all uncommitted work on your branch.

**Time Required:** 1 minute
**Difficulty:** Low  
**Risk:** HIGH (destructive, no undo)

### Step 1: Verify You Really Want to Do This

**Ask yourself:**
- Is there ANY work on this branch I want to keep?
- Have I committed everything important?
- Am I ABSOLUTELY SURE I want to nuke this branch?

**If answer to ANY of the above is "not sure" → STOP. Commit your work first or ask for help.**

---

### Step 2: Backup Current State (Optional but Recommended)

```bash
# Create a backup branch just in case
git checkout android_home
git branch android_home_backup_$(date +%Y%m%d)

# Verify backup exists
git branch | grep backup
# ✅ Should show: android_home_backup_20260228
```

---

### Step 3: Reset to Main

```bash
# Fetch latest main
git fetch origin main

# Hard reset your branch to match main exactly
git reset --hard origin/main

# Verify reset
git log --oneline -3
# ✅ Should show same commits as main

# Force push to remote (overwrites remote branch)
git push origin android_home --force
```

**Checkpoint 3:** Your branch is now identical to main. All previous work is gone (but saved in backup branch if you made one).

---

**✅ WORKFLOW COMPLETE**

Your branch is now a clean copy of main.

---

## Git Version Differences (What Commands Actually Work)

**The Problem:** Git's UI changes between versions. Commands that work on one machine fail on another. Here's what to watch for.

### Version Detection

```bash
# Check your git version first
git --version

# Example outputs:
# git version 2.43.0  (Modern - has all features)
# git version 2.25.1  (Ubuntu 20.04 default - missing some features)
# git version 2.17.1  (Older - use legacy commands)
```

---

### Git 2.23+ (Modern, 2019+)

**Has:** `git switch`, `git restore`

**Checkout Replacement:**
```bash
# Old way (still works):
git checkout main

# New way (clearer semantics):
git switch main

# For files:
git restore file.txt  # instead of: git checkout -- file.txt
```

**Use this version's commands if available** - they're clearer and harder to misuse.

---

### Git 2.27+ (2020+)

**Change:** Pull behavior warnings added

**You'll see:**
```
hint: Pulling without specifying how to reconcile divergent branches is
hint: discouraged. You can squelch this message by running one of the following
hint: commands sometime before your next pull:
```

**Fix:** Configure pull strategy once:
```bash
git config pull.rebase false  # merge (default)
# OR
git config pull.rebase true   # rebase (cleaner history)
```

**Add to your -isms constants:**
```json
"constants": {
  "git_pull_strategy": "merge"  # or "rebase"
}
```

---

### Git 2.28+ (2020+)

**Change:** Configurable default branch name

**Old repos:** Default branch is `master`  
**New repos:** Can be configured to `main`

**You'll see this inconsistency:**
```bash
# Old repo
git clone https://old-repo.git
cd old-repo
git branch  # Shows: * master

# New repo
git clone https://new-repo.git
cd new-repo
git branch  # Shows: * main
```

**Fix:** Your brain has to track per-repo. Or standardize:
```bash
# Set global default for NEW repos:
git config --global init.defaultBranch main

# Rename existing repo's branch:
git branch -m master main
git push -u origin main
```

**For our sync-private repo:** We're using `main`, so this shouldn't bite you.

---

### Git < 2.23 (Older, Pre-2019)

**Missing:** `git switch`, `git restore`

**Must use legacy commands:**
```bash
# Switch branches:
git checkout main  # switch and restore don't exist

# Restore files:
git checkout -- file.txt  # restore doesn't exist
```

**If you're on old git:**
- Ignore any workflow steps mentioning `git switch` - use `git checkout` instead
- Same functionality, just older command names

---

### Version-Specific Command Table

| Operation | Git < 2.23 | Git 2.23+ |
|-----------|-----------|-----------|
| Switch branch | `git checkout main` | `git switch main` (preferred) |
| Restore file | `git checkout -- file.txt` | `git restore file.txt` (preferred) |
| Create new branch | `git checkout -b new-branch` | `git switch -c new-branch` (preferred) |
| Discard changes | `git checkout -- .` | `git restore .` (preferred) |

**Rule of thumb:** If `git switch` gives "unknown command," use `git checkout` instead.

---

### Default Branch Name Confusion

**Scenario:** You see references to `master` but your repo uses `main` (or vice versa)

**Why:** Repos created before 2020-2021 use `master`, newer ones use `main`

**Solution:** Always check which branch name YOUR repo actually uses:
```bash
git branch -a  # Shows all branches, local and remote
```

**For workflows in this document:**
- We use `main` as canonical branch name
- If your repo uses `master`, mentally substitute it
- Or rename: `git branch -m master main && git push -u origin main`

---

### Pull Strategy Differences

**Git < 2.27:**
```bash
git pull origin main
# Just works, no warnings
```

**Git 2.27+:**
```bash
git pull origin main
# Shows warning about divergent branches
# Requires explicit strategy or config
```

**Fix (one-time per repo):**
```bash
git config pull.rebase false
# Now git pull works without warnings
```

---

### Commands That Changed Names (But Old Names Still Work)

| Old Command | New Command (2.23+) | Status |
|-------------|---------------------|--------|
| `git checkout <branch>` | `git switch <branch>` | Both work |
| `git checkout -- <file>` | `git restore <file>` | Both work |
| `git checkout -b <branch>` | `git switch -c <branch>` | Both work |

**The old commands still work** - git maintains backwards compatibility. The new ones are just clearer about intent.

---

### Practical Advice

**If you have multiple machines with different git versions:**

1. **Use old-style commands in scripts** - they work everywhere:
   ```bash
   git checkout main  # Works on all versions
   # Instead of: git switch main (only works 2.23+)
   ```

2. **Check version in -isms file** - document what each environment has

3. **Configure pull strategy** - do it once per repo per machine:
   ```bash
   git config pull.rebase false
   ```

4. **Stick to one branch name convention** - we're using `main`

5. **When in doubt, use `git status`** - it works the same across all versions

---

### -isms File Tracking

Your `-isms.json` should document git version per environment:

```json
"tools": {
  "git": {
    "available": true,
    "path": "/usr/bin/git",
    "version": "2.43.0",
    "version_major": 2,
    "version_minor": 43,
    "has_switch_command": true,
    "has_restore_command": true,
    "default_pull_strategy": "merge",
    "default_branch": "main",
    "notes": "Modern git - all features available"
  }
}
```

**Benefits:**
- Instance knows which commands are available
- Documentation per-environment
- Can warn if version is too old for certain operations

---

## Common Error Messages and Fixes

### "Your branch is behind 'origin/main' by X commits"

**What it means:** Your local main is out of date.

**Fix:**
```bash
git checkout main
git pull origin main
```

---

### "Your branch and 'origin/main' have diverged"

**What it means:** Your local branch and remote branch have different commits.

**Fix (if you want to keep your local changes):**
```bash
git pull origin main --rebase
```

**Fix (if you want to discard local changes):**
```bash
git reset --hard origin/main
```

---

### "fatal: refusing to merge unrelated histories"

**What it means:** You're trying to merge branches that don't share a common ancestor.

**Fix:**
```bash
git pull origin main --allow-unrelated-histories
# Then resolve any conflicts
```

---

### "error: failed to push some refs"

**What it means:** Remote has changes you don't have locally.

**Fix:**
```bash
git pull origin <branch>
# Resolve any conflicts, then:
git push origin <branch>
```

---

## Visual State Diagram

```
CLEAN STATE (android_home)
         |
         | git checkout main
         v
MAIN BRANCH (local)
         |
         | git pull origin main
         v
MAIN UPDATED (local)
         |
         | git merge android_home
         v
    /------------\
    |            |
CONFLICTS?      NO
    |            |
    v            v
RESOLVE -----> MERGED (local)
                |
                | git push origin main
                v
          MAIN UPDATED (remote)
                |
                | git checkout android_home
                v
          BACK TO WORK
```

---

## Cheat Sheet (Print This)

**Before ANY git operation:**
```bash
git status  # Must be clean
git branch --show-current  # Know where you are
```

**Safe operations (can't break anything):**
```bash
git status
git log
git branch
git diff
git fetch origin
```

**Point of no return operations (be careful):**
```bash
git merge
git push --force
git reset --hard
```

**If you mess up:**
```bash
git reflog  # Shows recent operations
git reset --hard HEAD@{1}  # Undo last operation
```

**Get help:**
```bash
git status  # Always start here
# Then ask the Architect or Vector what the output means
```

---

## Daily Workflow Quick Reference

**Morning (wake):**
```bash
git checkout android_home
git pull origin android_home
git pull origin main  # Get any updates from main
# Start working
```

**During work:**
```bash
# Every 30-60 minutes:
git add -A
git commit -m "Android session: [what you did]"
git push origin android_home
```

**End of session (sync to main):**
```bash
git checkout main
git pull origin main
git merge android_home --no-ff -m "Merge android_home ($(date +%Y-%m-%d))"
git push origin main
git checkout android_home
```

**Checkpoint after each command. If anything looks wrong, STOP and check.**

---

**Remember:** Git doesn't care about your feelings, but these workflows do. Follow them sequentially, check at each step, and you'll never be stuck reverting reverts of reverts.

**When in doubt:** `git status` is your friend. It tells you exactly what state you're in and often suggests what to do next.
