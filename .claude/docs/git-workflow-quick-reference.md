# Git Workflow Quick Reference

**Updated:** 2026-03-01  
**Keep this handy - the new workflow after reconfiguration**

---

## Daily Work (Private Repo)

```bash
# Morning: Get latest
git checkout working
git pull private working

# Work, work, work...

# Save your work
git add -A
git commit -m "Session: [what you did]"
git push private working
```

**That's it. No staging repo. No sanitization. Just work and push.**

---

## Publishing (When Ready for Public)

```bash
# Switch to sanitized branch
git checkout sanitized

# Run sanitization (script coming soon)
python .claude/scripts/sanitize-for-public.py

# Verify no PII
git diff working..sanitized  # Review changes
# Check for: names, emails, locations, private project names

# Push to public
git push public main
```

---

## Remotes

**private** = `git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git`
- Your daily work
- Full PII
- All personal details
- Only you see this

**public** = `git@github.com:continuity-bridge/continuity-bridge.git`
- Templates only
- No PII
- Example files
- World can see this

---

## Branches

**working** = Your daily work branch
- Push to: `private` remote
- Contains: Everything

**sanitized** = Public-ready templates
- Push to: `public` remote  
- Contains: Templates, examples, no PII

**main** = (optional, can be protected)

---

## Common Tasks

**Check which branch:**
```bash
git branch --show-current
```

**Check which remote:**
```bash
git remote -v
```

**Switch branches:**
```bash
git checkout working     # Daily work
git checkout sanitized   # Publishing
```

**See what changed:**
```bash
git status              # Uncommitted changes
git log --oneline -5    # Recent commits
```

**Undo mistakes:**
```bash
git restore <file>      # Undo changes to file
git reset HEAD~1        # Undo last commit (keep changes)
```

---

## When Things Go Wrong

**Pushed to wrong remote?**
```bash
# Can't un-push, but can fix:
# If pushed PII to public by mistake:
# 1. Contact GitHub support to purge commit
# 2. Force push corrected version
# 3. Rotate any exposed credentials
```

**Merge conflict?**
```bash
# Pull shows conflict:
git status              # See conflicted files
# Edit files to resolve
git add <resolved-files>
git commit -m "Resolved merge conflict"
git push private working
```

**Lost? Start over:**
```bash
git stash               # Save current work
git checkout working    # Go to safe branch
git stash pop           # Get work back
```

---

## Files That Never Go to Public

These are in `.gitignore` for `public` remote:

```
.credentials-local/     # NEVER push credentials
*.local                 # Local-only files
*-private.md           # Explicitly private
/Projects/*/           # Project work
/Sessions/*/           # May contain PII
```

---

## Emergency: Restore Old Config

If reconfiguration fails:

```bash
cd /home/the Architect/Claude
ls -la .git/config.backup-*  # Find backup
cp .git/config.backup-YYYYMMDD-HHMMSS .git/config
git remote -v  # Verify restoration
```

---

**Remember:** 
- `working` → `private` = Daily work, push freely
- `sanitized` → `public` = Publishing, check carefully

**One repo. Two remotes. Different branches. Simple.**
