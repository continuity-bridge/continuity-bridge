---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Container Git Workflow - Complete Integration Guide

**For: Magheara (Pixel 10 Pro) running Claude mobile app in container**

**Problem Solved:** Container environments can't write directly to host filesystem, but CAN clone and work with git repos.

**Solution:** Mount private anchor repo in container, work with full git access, auto-push at session close.

---

## Architecture Overview

**Traditional container workflow:**
```
Container → /mnt/user-data/outputs → Manual copy to repo
```
**SLOW, MANUAL, LOSSY**

**New container git workflow:**
```
Container → Clone repo → Work directly → Auto-commit/push
```
**FAST, AUTOMATED, FULL GIT HISTORY**

---

## Setup (One-Time)

### Step 1: Verify SSH Key in Container

**Container needs access to your GitHub SSH key.**

Check if key exists:
```bash
ls -la ~/.ssh/continuity-bridge
```

If missing, you'll need to either:
- **Option A:** Set up SSH key in container (recommended)
- **Option B:** Use HTTPS with token (less secure)

**For Option A:**
```bash
# In container
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Copy your SSH key (you'll need to paste it)
# Private key
cat > ~/.ssh/continuity-bridge << 'EOF'
[paste private key here]
EOF

# Public key  
cat > ~/.ssh/continuity-bridge.pub << 'EOF'
[paste public key here]
EOF

chmod 600 ~/.ssh/continuity-bridge
chmod 644 ~/.ssh/continuity-bridge.pub

# Configure SSH
cat > ~/.ssh/config << 'EOF'
Host github.com-continuity-bridge
    HostName github.com
    User git
    IdentityFile ~/.ssh/continuity-bridge
    IdentitiesOnly yes
EOF

chmod 600 ~/.ssh/config
```

**Test connection:**
```bash
ssh -T git@github.com-continuity-bridge
# Should see: "Hi username! You've successfully authenticated..."
```

### Step 2: Install session-close script

**Copy script to container:**
```bash
# Create scripts directory if needed
mkdir -p /home/claude/.local/bin

# Copy the script (you'll need to create it in container)
# Either copy from outputs or create new file
```

**Make executable:**
```bash
chmod +x /home/claude/.local/bin/session-close-container.py
```

---

## Session Workflow

### At Session Start

**Clone repo (first time) or pull updates (subsequent):**

```bash
cd /home/claude

# First session - clone
if [ ! -d "work" ]; then
    git clone git@github.com-continuity-bridge:continuity-bridge/continuity-bridge_tallest-anchor.git work
    cd work
    git checkout working
else
    # Subsequent sessions - pull updates
    cd work
    git checkout working
    git pull origin working
fi
```

**Now work normally:**
```bash
cd /home/claude/work

# Run wake sequence
./.claude/scripts/wake.sh

# Work happens...
# Edit files, create content, etc.
# All changes are in git-tracked directory
```

### At Session End

**Manual trigger:**
```bash
cd /home/claude
python3 session-close-container.py
```

**What it does:**
1. Checks for uncommitted changes
2. Creates commit with timestamp
3. Attempts push to `working` branch
4. If push fails (conflicts):
   - Fetches latest
   - Attempts rebase
   - Tries push again
5. If still fails:
   - Creates PR branch `container-session-TIMESTAMP`
   - Pushes PR branch
   - Tells you to create PR manually

**Successful output:**
```
========================================
CONTAINER SESSION CLOSE - Git Sync
========================================

Repo: /home/claude/work
Branch: working

Current branch: working
📝 Uncommitted changes detected
✓ Created commit: Container session updates - 20260304-172345

📤 Push attempt 1/2...
✓ Successfully pushed to working

📋 Session metadata saved: close-20260304-172345.json

========================================
✓ SESSION CLOSE SUCCESSFUL
========================================
```

**Conflict requiring PR:**
```
📤 Push attempt 2/2...
⚠ Push failed, creating PR branch...
✓ Created PR branch: container-session-20260304-172345

📝 ACTION REQUIRED:
   Create PR: container-session-20260304-172345 -> working
   GitHub: https://github.com/continuity-bridge/continuity-bridge_tallest-anchor/compare/working...container-session-20260304-172345

========================================
⚠ SESSION CLOSE REQUIRES MANUAL PR
========================================
```

---

## Automation Options

### Option 1: Manual Call at Session End

**Simplest approach - you manually run it:**
```bash
python3 /home/claude/.local/bin/session-close-container.py
```

### Option 2: Alias for Convenience

**Add to ~/.bashrc or ~/.zshrc:**
```bash
alias close-session='python3 /home/claude/.local/bin/session-close-container.py'
```

**Then just:**
```bash
close-session
```

### Option 3: Automatic on Low Token Warning

**When approaching context limit, instance calls it:**

```python
# In instance code
import subprocess

if context_remaining < 10000:  # Less than 10k tokens left
    print("⚠ Approaching context limit - closing session...")
    subprocess.run([
        'python3',
        '/home/claude/.local/bin/session-close-container.py'
    ])
```

### Option 4: Session Wrapper Script

**Create `container-session.sh`:**
```bash
#!/bin/bash
# Wrapper that handles setup and cleanup

# Setup
cd /home/claude
if [ ! -d "work" ]; then
    git clone git@github.com-continuity-bridge:continuity-bridge/continuity-bridge_tallest-anchor.git work
fi
cd work
git checkout working
git pull origin working

# Run wake
./.claude/scripts/wake.sh

echo "Session ready. Work in /home/claude/work"
echo "To close: run 'close-session'"

# Wait for user to finish...
# (session happens here)
```

**Paired with close alias above.**

---

## Conflict Resolution

**If PR branch is created, you have options:**

### Option A: Merge PR on GitHub
1. Go to the URL shown in output
2. Review changes
3. Create pull request
4. Merge to `working`

### Option B: Manual Merge Locally (on Persephone)
```bash
# On Persephone
cd ~/Claude
git fetch origin container-session-20260304-172345
git checkout working
git merge container-session-20260304-172345
git push origin working

# Clean up PR branch
git push origin --delete container-session-20260304-172345
```

### Option C: Cherry-pick Specific Commits
```bash
# If you only want some changes
git fetch origin container-session-20260304-172345
git cherry-pick <commit-hash>
git push origin working
```

---

## Best Practices

### 1. Pull Before Starting
**Always pull latest at session start** to minimize conflicts:
```bash
cd /home/claude/work
git pull origin working
```

### 2. Commit Often
**Don't wait until session end** - commit meaningful checkpoints:
```bash
git add -A
git commit -m "Implemented feature X"
```

### 3. Check Status Before Closing
**Review what's being committed:**
```bash
git status
git diff
```

### 4. Test Session-Close in Dry Run
**See what would happen without doing it:**
```bash
python3 session-close-container.py --dry-run
```

---

## Troubleshooting

### "Repository not found"
**Problem:** Can't access private repo

**Solution:** Check SSH key setup, test with:
```bash
ssh -T git@github.com-continuity-bridge
```

### "Could not determine current branch"
**Problem:** Not in git repo or git not working

**Solution:**
```bash
cd /home/claude/work
git status  # Should show branch info
```

### "Push failed repeatedly"
**Problem:** Major conflicts or network issues

**Solution:** PR branch will be created automatically. Review and merge manually.

### "Nothing to commit"
**Problem:** No changes were made

**This is fine** - script exits cleanly with no action needed.

---

## File Locations

**In container:**
```
/home/claude/work/                    # Cloned repo
/home/claude/.local/bin/              # Scripts
/home/claude/work/.claude/session-metadata/  # Close logs
```

**Script outputs metadata to:**
```
/home/claude/work/.claude/session-metadata/close-TIMESTAMP.json
```

**Contains:**
- Timestamp
- Branch used
- Push result (success/pr_needed/failed)
- Useful for debugging

---

## Workflow Summary

**Session Start:**
1. Clone repo (or pull if exists)
2. Checkout working branch
3. Run wake.sh
4. Work normally

**Session End:**
1. Run session-close-container.py
2. Script auto-commits changes
3. Script auto-pushes (with retry)
4. If conflicts, creates PR branch
5. You merge PR later

**Result:** Full git history of container work, no manual file copying, automatic sync.

---

## Benefits Over Outputs Bridge

**Old way (outputs bridge):**
- ❌ Manual file copying
- ❌ No git history
- ❌ Easy to lose changes
- ❌ Merge conflicts hard to resolve
- ❌ No rollback capability

**New way (git mount):**
- ✅ Automatic sync
- ✅ Full git history
- ✅ Changes tracked and versioned
- ✅ Conflicts handled automatically
- ✅ Easy rollback with git
- ✅ Works exactly like desktop

---

**This workflow makes container environments functionally equivalent to desktop for git-based continuity work.**
