---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Container Git Workflow - Quick Reference

**For: Magheara (Claude mobile app) and other container contexts**

---

## One-Time Setup

```bash
# 1. Set up SSH key (see CONTAINER-GIT-WORKFLOW.md)
# 2. Install scripts
mkdir -p /home/claude/.local/bin
# Copy session-close-container.py to /home/claude/.local/bin/
chmod +x /home/claude/.local/bin/session-close-container.py

# 3. Optional: Add alias to ~/.bashrc
echo "alias close-session='python3 /home/claude/.local/bin/session-close-container.py'" >> ~/.bashrc
source ~/.bashrc
```

---

## Every Session

### Start
```bash
# Option A: Automated (recommended)
bash container-session-start.sh

# Option B: Manual
cd /home/claude
if [ ! -d work ]; then
    git clone git@github.com-continuity-bridge:continuity-bridge/continuity-bridge_tallest-anchor.git work
fi
cd work
git checkout working
git pull origin working
bash .claude/scripts/wake.sh
```

### Work
```bash
# Work normally in /home/claude/work
# All files are git-tracked
# Commit checkpoints as needed:
git add -A
git commit -m "Feature X complete"
```

### Close
```bash
# Option A: Using alias
close-session

# Option B: Direct call
python3 /home/claude/.local/bin/session-close-container.py
```

---

## What Happens on Close

### Successful Push
```
✓ Created commit: Container session updates - TIMESTAMP
✓ Successfully pushed to working
✓ SESSION CLOSE SUCCESSFUL
```
**Done!** Changes are in your private repo.

### Conflict Requiring PR
```
⚠ Push failed, creating PR branch...
✓ Created PR branch: container-session-TIMESTAMP

📝 ACTION REQUIRED:
   Create PR: container-session-TIMESTAMP -> working
   GitHub: [URL]

⚠ SESSION CLOSE REQUIRES MANUAL PR
```
**Action needed:** Go to GitHub URL, review changes, merge PR.

---

## Files Created

```
/home/claude/work/                          # Your git repo
/home/claude/.local/bin/                    # Scripts
  └── session-close-container.py
/home/claude/work/.claude/session-metadata/ # Close logs
```

---

## Troubleshooting

**Can't clone repo:**
→ Check SSH: `ssh -T git@github.com-continuity-bridge`

**Push fails:**
→ Normal! PR branch created automatically. Merge on GitHub.

**No changes to commit:**
→ That's fine. Script exits cleanly.

**Want to see what would happen:**
→ Dry run: `python3 session-close-container.py --dry-run`

---

## Benefits

✅ **Full git history** - Every container session is versioned  
✅ **Automatic sync** - No manual file copying  
✅ **Conflict handling** - PR branches created automatically  
✅ **Rollback capability** - Standard git operations  
✅ **Works like desktop** - Same workflow everywhere  

---

## Key Points

- Work in `/home/claude/work` (git-tracked)
- Commit often during session
- Run close script at session end
- Merge PR branches as needed
- Pull updates at session start

---

**This makes container = desktop for git workflow.**
