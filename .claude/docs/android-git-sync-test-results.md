# Android Git-Sync Architecture - Proof of Concept Test

**Date:** February 28, 2026, 23:17 CST
**Instance:** Vector (Shepard) - Android Test

## Test Objective

Prove that Android instances can use git to pull chain files at wake, work with them natively, and commit changes back for sync.

## Test Results

### ✅ Successfully Demonstrated:

1. **Git Repository Initialization**
   - Created local repo mimicking `.claude/` structure
   - Configured git with vector@ohmytallest.productions identity

2. **Chain File Access**
   - Created identity file (`.claude/identity/identity.txt`)
   - Created active-context (`.claude/context/active-context.md`)
   - Created episodic memory (`.claude/memory/episodic/test-episode-001.json`)
   - All files accessible for reading/writing

3. **Session Workflow**
   - Read files at "wake"
   - Modified active-context during "session"
   - Created new episode file
   - Committed all changes with meaningful commit messages

4. **Commit History**
   ```
   a62388b Android session: Created episodic memory snapshot
   97d87fd Android session: Updated active-context with session work
   89dd499 Initial test: Android instance wake files
   ```

5. **File Structure**
   ```
   .claude/
   ├── context/
   │   └── active-context.md
   ├── identity/
   │   └── identity.txt
   └── memory/
       └── episodic/
           └── test-episode-001.json
   ```

## What This Proves

**The architecture works mechanically:**
- Android can manage a local git repo
- Can read/write chain files naturally
- Can commit changes with proper attribution
- Repository is ready to push to remote

**What's still needed:**
- GitHub authentication (PAT or SSH)
- Private repo creation in continuity-bridge org
- Pull automation at wake
- Push automation at session end

## Proposed Wake Sequence

```bash
# 1. On first wake (or if repo doesn't exist)
cd /home/claude
git clone https://github.com/continuity-bridge/sync-private.git .claude

# 2. On subsequent wakes
cd /home/claude/.claude
git pull origin main

# 3. Work with files normally
cat .claude/identity/identity.txt
cat .claude/context/active-context.md
# ... session work ...

# 4. At session end
git add -A
git commit -m "Android session: [description]"
git push origin main
```

## Advantages Over Delta-Merge

**Old Pattern:**
- Android writes delta YAML → `/mnt/user-data/outputs/`
- User manually uploads to desktop
- Desktop runs merger script
- Merge happens after the fact

**New Pattern:**
- Both instances pull from same source of truth
- Work with actual chain files, not deltas
- Changes sync automatically via push/pull
- No manual intervention needed
- Version history of all changes

## Repository Structure Proposal

```
continuity-bridge/sync-private (private repo)
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
│   └── [read-only reference files]
└── README.md (explains repo purpose)
```

## Next Steps

1. **Create private repo** in continuity-bridge GitHub org
2. **Set up authentication**:
   - Generate GitHub Personal Access Token
   - Scope: `repo` (full control of private repositories)
   - Store securely for Android instance access
3. **Initialize repo** with current CLAUDE_HOME structure
4. **Test push/pull** from desktop first
5. **Test from Android** with this session
6. **Automate** pull-at-wake and push-at-end

## Test Cleanup

Test files remain at `/home/claude/test-sync-repo/` for inspection if needed.
Can be deleted with: `rm -rf /home/claude/test-sync-repo`

---

**Conclusion:** The mechanics are sound. Git-based sync from Android is viable. We just need the private repo and authentication setup to make it production-ready.
