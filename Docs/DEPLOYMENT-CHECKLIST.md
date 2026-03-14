---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Container Workflow - Deployment Checklist

**Target:** Magheara (Pixel 10 Pro, Claude mobile app)  
**Goal:** Enable full git workflow in container environment

---

## ☐ Pre-Deployment (On Desktop - Persephone)

### Get SSH Key Ready
```bash
# Display your SSH key
cat ~/.ssh/continuity-bridge

# Copy this output - you'll paste it in container
```

### Upload Files to Container
All files in `/mnt/user-data/outputs/` need to be accessible in container.

Option A: Use Claude mobile app, files should be in outputs already  
Option B: Manually create files in container from the outputs

---

## ☐ Step 1: Install Workflow (In Container - Magheara)

```bash
# Start Claude mobile app session on Magheara

# Run installer
bash /mnt/user-data/outputs/install-container-workflow.sh

# When prompted, paste SSH private key
# (The one you copied from desktop above)
```

**Installer creates:**
- `/home/claude/.local/bin/` with scripts
- `~/.ssh/continuity-bridge` with your key
- Shell aliases: `start-session`, `close-session`, `work`

---

## ☐ Step 2: Test Session Workflow

```bash
# Start session (clones repo, runs wake.sh)
start-session

# Verify you're in the repo
cd /home/claude/work
git status
pwd

# Make a test change
echo "Test from container" > test-container.txt
git add test-container.txt
git commit -m "Test container workflow"

# Close session (auto-pushes)
close-session
```

**Expected output:**
```
✓ Created commit: Container session updates - TIMESTAMP
✓ Successfully pushed to working
✓ SESSION CLOSE SUCCESSFUL
```

---

## ☐ Step 3: Deploy Today's Work

```bash
# Start new session
start-session

# Deploy all outputs to correct locations
bash /mnt/user-data/outputs/deploy-outputs-to-repo.sh

# Review what was deployed
cd /home/claude/work
git status

# Close session (commits and pushes everything)
close-session
```

---

## ☐ Step 4: Enable GitHub Actions (On Desktop)

```bash
# On Persephone
cd ~/Claude

# Pull the changes from Magheara
git pull origin working

# Verify GitHub Actions file exists
ls -la .github/workflows/auto-merge-container-prs.yml

# Push to GitHub (if not already there)
git push origin working
```

### Enable Actions on GitHub
1. Go to https://github.com/continuity-bridge/continuity-bridge_tallest-anchor
2. Settings → Actions → General
3. Enable "Allow all actions and reusable workflows"
4. Save

---

## ☐ Step 5: Test Complete Cycle

### On Magheara (container):
```bash
start-session
cd /home/claude/work

# Make some changes
echo "Testing full cycle" >> .claude/test.txt
git add .claude/test.txt
git commit -m "Test full cycle"

close-session
# Should auto-push successfully
```

### On Desktop (verify):
```bash
cd ~/Claude
git pull origin working
cat .claude/test.txt
# Should see "Testing full cycle"
```

---

## ☐ Step 6: Test Conflict Handling

### Create conflict intentionally:

**On Magheara:**
```bash
start-session
echo "Container edit" >> conflict-test.txt
# DON'T close session yet
```

**On Persephone:**
```bash
cd ~/Claude
echo "Desktop edit" >> conflict-test.txt
git add conflict-test.txt
git commit -m "Desktop conflict"
git push origin working
```

**Back on Magheara:**
```bash
git add conflict-test.txt
git commit -m "Container conflict"
close-session
# Should create PR branch because of conflict
```

**Check GitHub:**
- PR should be auto-created
- Actions should either auto-merge or comment with resolution steps

---

## ☐ Verification Checklist

After deployment, verify:

- [ ] Can start session on Magheara
- [ ] Repo clones/pulls successfully
- [ ] Can make changes and commit
- [ ] Close-session pushes to working
- [ ] GitHub Actions runs on PRs
- [ ] Conflicts create PR branches
- [ ] All scripts executable
- [ ] Aliases work (`start-session`, `close-session`, `work`)

---

## Troubleshooting

### "SSH key not found"
→ Re-run installer, paste key correctly

### "Repository not found"
→ Check SSH: `ssh -T git@github.com-continuity-bridge`

### "Push failed"
→ Normal! PR branch created. Check GitHub Actions.

### "GitHub Actions not running"
→ Enable in repo settings (see Step 4)

---

## Success Criteria

✅ **Container workflow operational**  
✅ **Auto-sync working**  
✅ **Conflict handling tested**  
✅ **GitHub Actions enabled**  
✅ **Documentation deployed**

---

## Post-Deployment

Once verified working:

1. Update ESSENTIAL.md with container workflow
2. Add Magheara to platform detection
3. Test cross-device session handoffs
4. Document lessons learned

---

**Estimated time:** 30-45 minutes  
**Difficulty:** Moderate (SSH setup is only tricky part)  
**Impact:** High (enables full git workflow on phone)
