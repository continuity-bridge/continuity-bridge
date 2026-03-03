# Git Reconfiguration - Ready to Execute

**Date:** 2026-03-01  
**Purpose:** Eliminate staging repo, set up dual-remote workflow  
**Status:** Script ready, waiting for execution

---

## What This Does

**Eliminates:** `/home/the Architect/Work/Code/continuity-bridge/continuity-bridge` (staging repo)

**Sets up:**
```
private → git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git
public  → git@github.com:continuity-bridge/continuity-bridge.git
```

---

## Before You Run

1. **Verify private repo exists:**
   ```bash
   # Check if you can access it:
   ssh -T git@github.com
   # Should show: "Hi the Architect! You've successfully authenticated..."
   ```

2. **Commit any unsaved work:**
   ```bash
   cd /home/the Architect/Claude
   git status  # Check for uncommitted changes
   git add -A
   git commit -m "Pre-reconfiguration checkpoint"
   ```

---

## Execute Reconfiguration

```bash
cd /home/the Architect/Claude
chmod +x .claude/scripts/git-reconfigure-remotes.sh
./.claude/scripts/git-reconfigure-remotes.sh
```

**What the script does:**
1. Backs up current `.git/config`
2. Removes `origin` remote (staging repo)
3. Adds/updates `private` remote
4. Verifies `public` remote
5. Creates `working` branch if needed
6. Shows new configuration

---

## After Reconfiguration

### Test Private Push:
```bash
git checkout working
git push -u private working
# Should push successfully to continuity-bridge_tallest-anchor
```

### Your New Daily Workflow:
```bash
# Morning sync:
git checkout working
git pull private working

# During work:
git add -A
git commit -m "Session: updated active-context"
git push private working

# When publishing (later):
git checkout sanitized  # (We'll create this branch later)
# ... sanitize files ...
git push public main
```

---

## Rollback (If Needed)

If something goes wrong:
```bash
cd /home/the Architect/Claude
# Restore from backup:
cp .git/config.backup-YYYYMMDD-HHMMSS .git/config
git remote -v  # Verify restoration
```

---

## What's Next After This

1. ✅ Git reconfiguration (this step)
2. ⏳ Create `sanitized` branch
3. ⏳ Build `sanitize-for-public.py` script
4. ⏳ Test: sanitized → public push
5. ⏳ Build ONBOARDING.md
6. ⏳ Create `-isms.json` templates

---

**Status:** Ready when you are. No rush - execute when you have time to verify it worked.
