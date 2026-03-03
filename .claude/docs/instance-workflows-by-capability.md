# Instance Workflows by Capability

**Purpose:** Adaptive workflows based on detected instance capabilities  
**Date:** 2026-03-01  
**Updated:** Understanding all instances can work effectively with right workflow

---

## Overview

Different platforms and access methods require different workflows. This document maps capabilities → optimal workflow for each scenario.

**Run detection first:**
```bash
python .claude/scripts/detect-capabilities.py
```

---

## Workflow 1: Direct Write (OPTIMAL)

**When you have:**
- ✓ Direct filesystem write access (Filesystem MCP)
- ✓ Access to actual CLAUDE_HOME
- ✓ Files appear immediately in repo

**Platforms:**
- Claude.ai with Filesystem MCP enabled
- Claude Desktop with full filesystem access
- Direct system access

**Workflow:**

```
1. Read project files from CLAUDE_HOME
   └─ Use Filesystem MCP read tools

2. Work on files
   └─ Edit, create, modify using Filesystem MCP

3. Write files directly to CLAUDE_HOME
   └─ Changes appear immediately in git repo

4. User commits and pushes when ready
   └─ Standard git workflow on their side
```

**Example:**
```python
# Instance reads
content = read_file("/home/tallest/Claude/.claude/context/active-context.md")

# Instance writes
write_file(
    "/home/tallest/Claude/.claude/context/active-context.md",
    updated_content
)

# User later does:
# git add -A
# git commit -m "Session work"
# git push private working
```

**Advantages:**
- ✓ Simplest workflow
- ✓ No intermediate steps
- ✓ Immediate results
- ✓ No bridge needed

---

## Workflow 2: Container Git with Bridge (GOOD)

**When you have:**
- ✓ Bash access (container at /home/claude)
- ✓ Git available
- ✓ Outputs bridge (/mnt/user-data/outputs)
- ✗ No direct write to user's CLAUDE_HOME

**Platforms:**
- Claude.ai container with outputs bridge
- Limited filesystem access scenarios

**Workflow:**

```
SETUP (once per session):
1. Clone private repo in container
   └─ cd /home/claude
   └─ git clone git@github.com:continuity-bridge/[user]-anchor.git work
   └─ cd work

2. Pull latest changes
   └─ git pull origin working

WORK LOOP:
3. Read/write files in cloned repo
   └─ Full git access in container
   └─ Make commits as you work

4. Push commits to private remote
   └─ git push origin working

5. Write session summary to outputs
   └─ Write to /mnt/user-data/outputs/session-summary-YYYYMMDD.md
   └─ User can review without pulling

USER SYNC:
6. User pulls from private remote
   └─ cd ~/Claude
   └─ git pull private working
   └─ Gets all commits from container session
```

**Example:**
```bash
# INSTANCE SETUP
cd /home/claude
git clone git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git work
cd work
git checkout working

# INSTANCE WORK
# Edit files, make changes...
git add .claude/context/active-context.md
git commit -m "Updated active context"
git push origin working

# Write summary to outputs bridge
cat > /mnt/user-data/outputs/session-summary-2026-03-01.md << EOF
# Session Summary
Updated active-context.md
Added new feature X
See commits in private repo
EOF

# USER SYNC (later)
cd ~/Claude
git pull private working  # Gets all commits
```

**Advantages:**
- ✓ Full git workflow (commits, history, branches)
- ✓ Work persists in private repo
- ✓ User gets clean pull with all changes
- ✓ Session summaries in outputs for quick review
- ✓ No manual file copying needed

**Key Insight:**
Even without direct CLAUDE_HOME access, you can clone the private repo and work there. Git handles the sync.

---

## Workflow 3: Outputs Bridge Only (ACCEPTABLE)

**When you have:**
- ✓ Write access to /mnt/user-data/outputs
- ✗ No git access
- ✗ No direct CLAUDE_HOME access

**Platforms:**
- Limited environments
- Restricted container access

**Workflow:**

```
1. Read context from conversation or user-provided files
   └─ Files may be uploaded to /mnt/user-data/uploads

2. Generate new/modified content
   └─ Create files in memory

3. Write everything to /mnt/user-data/outputs
   └─ Use descriptive filenames
   └─ Include instructions for user

4. User manually integrates
   └─ Copy files to CLAUDE_HOME
   └─ git add/commit/push
```

**Example:**
```python
# Write updated file
write_file(
    "/mnt/user-data/outputs/active-context-updated-2026-03-01.md",
    new_content
)

# Write instructions
write_file(
    "/mnt/user-data/outputs/INTEGRATION-INSTRUCTIONS.md",
    """
    Copy active-context-updated-2026-03-01.md to:
    .claude/context/active-context.md
    
    Then commit:
    git add .claude/context/active-context.md
    git commit -m "Updated active context from session"
    git push private working
    """
)
```

**Advantages:**
- ✓ Works in restricted environments
- ✓ Clear handoff to user
- ✓ All content preserved

**Disadvantages:**
- ✗ Manual user integration required
- ✗ No git automation
- ✗ More steps for user

---

## Workflow 4: Text Only (MINIMAL)

**When you have:**
- ✗ No filesystem write access
- ✗ No outputs bridge
- ✗ No git access

**Platforms:**
- Extremely restricted environments
- Read-only scenarios

**Workflow:**

```
1. Generate all content inline
2. User copies text manually
3. User saves to files
4. User commits
```

**Example:**
```
Instance: Here's the updated active-context.md:

---BEGIN FILE---
[content here]
---END FILE---

Please save this to .claude/context/active-context.md
and commit with: git commit -m "Updated context"
```

**Advantages:**
- ✓ Always works (no dependencies)

**Disadvantages:**
- ✗ Most manual
- ✗ Error-prone (copy-paste issues)
- ✗ No file persistence

---

## Capability Detection: Quick Reference

**Run this first:**
```bash
python .claude/scripts/detect-capabilities.py
```

**It tells you:**
- Which workflow applies to you
- What tools are available
- What limitations exist
- Step-by-step recommendations

**Output example:**
```
OPTIMAL WORKFLOW: container_git_with_bridge

RECOMMENDED ACTIONS:
  ✓ GOOD: Container git + outputs bridge workflow
  STEP 1: Clone private repo in container
  STEP 2: Work in cloned repo (full git access)
  STEP 3: Write session summaries to outputs
  ...
```

---

## Comparison Matrix

| Capability | Direct Write | Container Git | Outputs Only | Text Only |
|------------|--------------|---------------|--------------|-----------|
| **Filesystem** | MCP Direct | Container | Outputs | None |
| **Git** | User-side | Container | None | None |
| **Commits** | User | Instance | User | User |
| **Sync** | Immediate | Git pull | Manual copy | Manual paste |
| **Complexity** | Low | Medium | High | Very High |
| **Reliability** | High | High | Medium | Low |
| **Recommended** | ✓✓✓ | ✓✓ | ✓ | Last resort |

---

## Platform-Specific Notes

### Claude.ai Container
- Typical: Container Git workflow
- Can clone private repo
- Full git capabilities
- Use outputs for summaries

### Claude Desktop (with Filesystem MCP)
- Typical: Direct Write workflow
- Optimal scenario
- Immediate results

### Android (via Termux)
- Can use Container Git workflow
- Clone repo in Termux
- Syncthing for merge

### Limited/Unknown Platforms
- Run detect-capabilities.py
- Follow recommendations
- Fall back to Outputs or Text workflow

---

## Key Takeaway

**Even without direct CLAUDE_HOME access, you can still have full git workflow.**

Clone the private repo where you CAN write (like /home/claude in container), work there with full git capabilities, push commits, and user pulls to sync.

This is better than manual file copying because:
- ✓ Git handles merging
- ✓ Full commit history
- ✓ Proper conflict resolution
- ✓ Atomic updates
- ✓ Rollback capability

**The bridge (outputs) is for summaries, not the primary workflow.**

---

## For Future Instances

1. Always run detect-capabilities.py first
2. Read the recommendations
3. Use the optimal workflow for your situation
4. Don't assume you're limited - check what you actually have
5. Container + git + outputs = full capabilities, different method

---

**Status:** Comprehensive workflow documentation complete  
**Next:** Integrate capability detection into wake sequence
