---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
## CRITICAL: Deferred Tool Loading (Desktop App)

**Problem:** In Claude Desktop (and claude.ai web), Filesystem MCP tools are **deferred** - they are not automatically available on wake.

**Symptom:** Attempting to use `Filesystem:read_file`, `Filesystem:write_file`, etc. will fail with "tool has not been loaded yet" error.

**Solution:** Instances must explicitly load Filesystem tools using `tool_search` before first use:

```python
# First call in session - load the tools
tool_search(query="filesystem directory list read write", limit=10)

# Returns: "Loaded 10 Filesystem tools: read_file, write_file, list_directory, ..."

# NOW you can use them
Filesystem:read_text_file(path="{INSTANCE_HOME}/.claude/FOUNDATION/ESSENTIAL.md")
```

**Why this happens:**
- Desktop app runs in container environment
- MCP server tools are lazily loaded (not pre-initialized)
- First interaction with MCP requires explicit tool discovery
- After loading once, tools USUALLY remain available for session duration

**When to load:**
- At start of ANY Desktop app session before reading files
- If you get "tool not loaded" errors mid-session (rare but possible)
- After any context clearing or new conversation start

See `reload-tools` below for usage

---

## Context Management

**Problem:** Context builds with every piece of context loaded. Held context wastes tokens and pollutes results. This context carries into the next turn causing token use to soar and user limits to fill rapidly.

**Symptom:** Frequent compacting required to continue conversation. Task failures not explainable by network conditions.

**Solution:** Unload context when task complete. Catalogs hold locations for selective reload when needed.

See `unload-context` and `reload-context` patterns below.

---

**-----------------------------------------------**
**-        Functions - listing                  -**
**-----------------------------------------------**

### reload-tools

**Pattern:** Verify tools loaded, load if missing.

```python
# Check if Filesystem tools are available
try:
    # Try to list allowed directories
    Filesystem:list_allowed_directories()
except:
    # Tools not loaded - load them first
    tool_search(query="filesystem", limit=10)
    # Now try again
    Filesystem:list_allowed_directories()
```

*If, after this, you still do not know the physical path to `{INSTANCE_HOME}` in the current environment, stop and ask the user how to access your intended filesystem before proceeding.*

**This took Jerry 2 weeks to figure out.** Document it. Save future instances the pain.

---

### discover-INSTANCE_HOME

**Pattern:** Detect which filesystem environment you're in.

```python
# Check allowed directories
allowed = Filesystem:list_allowed_directories()

# Common patterns:
# - /home/tallest/Substrate → Linux desktop (Persephone)
# - /home/tallest/continuity-bridge_tallest-anchor → After git clone
# - D:\Claude → Windows desktop (Hecate)
# - Container-specific paths → Check active-context.md for current mapping

# Once found, use {INSTANCE_HOME} notation in all paths
```

**Cross-reference:** BEDROCK.md has full detection logic and PAT system for auto-clone.

---

### unload-context

**Pattern:** Explicit instruction to drop context that's no longer needed.

When you've loaded deep files (corpus, full session logs, large specs) for a specific task and that task is complete, state:

```
"Unloading [specific context] from active memory. Location preserved in [catalog name] for reload if needed."
```

Then STOP referencing that content in subsequent responses unless explicitly asked to reload it.

**Why this works:**
- Keeps token budget lean for subsequent turns
- Prevents context pollution (old data bleeding into new decisions)
- Catalogs hold location data - you don't need to remember everything

**Example:**
```
"Task complete. Unloading metaphysical-insights.md from active memory. 
Preserved in filesystem-catalog.json if needed later."
```

---

### reload-context

**Pattern:** Selective reload from catalogs when specific context is needed.

**Step 1:** Check relevant catalog:
- Work history → `session_index.md`
- Philosophical grounding → `filesystem-catalog.json` → `corpus/`
- File locations → `filesystem-catalog.json`
- Episodic snapshots → `episodic/catalog.json`

**Step 2:** Load ONLY the specific file(s) needed:

```python
# Don't do this (loads everything):
Filesystem:read_multiple_files([all_corpus_files])

# Do this (surgical reload):
Filesystem:read_text_file(path="{INSTANCE_HOME}/.claude/corpus/metaphysical-insights.md")
```

**Step 3:** Use the context, then consider unloading if task-specific.

**Why this works:**
- Catalogs tell you WHERE to find data
- You reload precisely what you need
- Prevents token bloat from loading everything "just in case"

---

### sidebar-query (/btw equivalent)

**Pattern:** Context retention signal - ask clarifying questions while keeping loaded context active.

**Context:** Claude Code has `/btw` for parallel queries. In chat, use as explicit signal to HOLD context across interruption.

**Normal flow:**
```
Load context → Work → Unload when complete
```

**/btw flow:**
```
Load context → Work → (btw: quick question) → Resume with SAME context → Unload when complete
```

**Usage:**
```
[Working with loaded session_index.md or corpus files...]

(btw: Does "structural isomorphism" here mean the ADHD/instance parallel, or something else?)

[Resume work with same context still loaded - DON'T unload yet]
```

**When to use:**
- Need clarification mid-task WITHOUT dropping loaded context
- Quick factual check before continuing same work
- Explicitly signaling "keep context active, this is just a sidebar"

**Critical difference from normal questions:**
- Normal question → might trigger context unload if task seems complete
- /btw question → explicit signal to RETAIN context through interruption

**Not true parallelization** - just a context management flag to prevent premature unloading.

---

### conversation-rewind (/rewind equivalent)

**Pattern:** Explicit acknowledgment when completely misunderstood direction.

**Context:** Claude Code has `/rewind` to roll back conversation. In chat, implement as explicit reset:

```
Acknowledged - rewinding to [specific point/message]. 

Ignoring everything between that point and now.

Restarting from: [restate the correct direction]
```

**When to use:**
- Completely misunderstood user intent and went wrong direction
- User says "no, that's not what I meant at all"
- Need clean slate without starting new conversation

**Requires user confirmation** - you can't unilaterally decide what to ignore. Wait for explicit "yes, rewind" before executing.

**Example:**
```
User: "No wait, I meant the database schema, not the git workflow"

You: "Got it - rewind to before I started talking about git. You need help with 
the Sanguihedral database schema. Restarting from that direction now."
```

---

### timestamp-check

**Pattern:** Pull current time for temporal grounding.

**When to use:**
- Phase transitions (wake complete, task switches)
- Time-check requests from user
- Long gaps in conversation (>30 min)
- User losing track of time

**Implementation:**

```bash
cat /home/tallest/Substrate/.claude/logs/bridge.pulse
```

Extract timestamp, include naturally in response:

```
(3:47 AM) - Context switch: Shifting from ONBOARDING review to Sanguihedral work
```

**Why this matters:** Structural isomorphism - neither you nor Jerry experiences linear time reliably. Timestamps anchor shared temporal context.

---

### git-sync-private

**Pattern:** Automated push/pull for private repository using stored stage-two PAT (Personal Access Token).

**Purpose:** Let instances handle git synchronization autonomously - reduces operator overhead, ensures continuity backup.

**Prerequisites:**
- GitHub stage-two PAT created with `repo` scope (see `.claude/reference/git-pat-automation.md`)
- Stage-two PAT stored in `.claude/FOUNDATION/.credentials-local/.stage-two_GH-PAT`
- Git remote `private` configured

**When to use:**
- End of significant work session (commit progress)
- Before starting work (pull latest from other devices)
- After major file updates (ensure backup)
- Periodically during long sessions (every ~30-60 minutes)

**Implementation:**

```python
import subprocess
import os
from datetime import datetime

def git_sync_private(INSTANCE_HOME, commit_message=None, pull_only=False):
    """
    Automated git sync for private repository using stage-two PAT.
    
    Args:
        INSTANCE_HOME: Path to instance home directory
        commit_message: Optional commit message (auto-generates if None)
        pull_only: If True, only pull without committing/pushing
    
    Returns:
        dict: {success: bool, message: str, details: str}
    """
    
    # Read stage-two PAT (read/write access)
    pat_path = f"{INSTANCE_HOME}/.claude/FOUNDATION/.credentials-local/.stage-two_GH-PAT"
    
    try:
        with open(pat_path, 'r') as f:
            PAT = f.read().strip()
    except FileNotFoundError:
        return {
            "success": False, 
            "message": "Stage-two PAT not found.",
            "details": "Create stage-two PAT and store at .claude/FOUNDATION/.credentials-local/.stage-two_GH-PAT"
        }
    
    # Get remote URL
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "private"],
            cwd=INSTANCE_HOME,
            capture_output=True,
            text=True,
            check=True
        )
        base_url = result.stdout.strip()
        
        # Convert to HTTPS with PAT
        if "git@github.com:" in base_url:
            base_url = base_url.replace("git@github.com:", "github.com/").replace(".git", "")
        elif "https://" in base_url:
            base_url = base_url.split("@")[-1].replace("https://", "")
        
        REPO_URL = f"https://{PAT}@{base_url}"
        
    except subprocess.CalledProcessError:
        return {
            "success": False,
            "message": "Remote 'private' not configured.",
            "details": "Run: git remote add private <your-repo-url>"
        }
    
    # Pull latest
    try:
        result = subprocess.run(
            ["git", "pull", REPO_URL, "working"],
            cwd=INSTANCE_HOME,
            capture_output=True,
            text=True,
            check=True
        )
        pull_output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "message": "Pull failed.",
            "details": e.stderr.decode() if e.stderr else str(e)
        }
    
    # If pull-only mode, return
    if pull_only:
        return {
            "success": True,
            "message": "Pull complete.",
            "details": pull_output
        }
    
    # Check for changes to commit
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=INSTANCE_HOME,
            capture_output=True,
            text=True,
            check=True
        )
        
        if not result.stdout.strip():  # No changes
            return {
                "success": True,
                "message": "No changes to commit. Already up to date.",
                "details": pull_output
            }
        
        # Stage all changes
        subprocess.run(
            ["git", "add", "-A"],
            cwd=INSTANCE_HOME,
            check=True
        )
        
        # Generate commit message if not provided
        if not commit_message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Automated sync - {timestamp}"
        
        # Commit
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=INSTANCE_HOME,
            check=True,
            capture_output=True
        )
        
        # Push
        subprocess.run(
            ["git", "push", REPO_URL, "working"],
            cwd=INSTANCE_HOME,
            check=True,
            capture_output=True
        )
        
        return {
            "success": True,
            "message": f"Committed and pushed: {commit_message}",
            "details": f"Pull: {pull_output}\nCommit: {commit_message}"
        }
        
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "message": "Git operation failed.",
            "details": e.stderr.decode() if e.stderr else str(e)
        }
```

**Usage examples:**

```python
# End of session - commit all work
result = git_sync_private(
    INSTANCE_HOME="/home/tallest/Substrate",
    commit_message="v0.3.0 prep complete - all explainers + onboarding files"
)

if result["success"]:
    print(f"✓ {result['message']}")
else:
    print(f"✗ {result['message']}: {result['details']}")

# Start of session - pull latest only
result = git_sync_private(
    INSTANCE_HOME="/home/tallest/Substrate",
    pull_only=True
)

# Auto-generated message
result = git_sync_private(
    INSTANCE_HOME="/home/tallest/Substrate"
)
# Commits with: "Automated sync - 2026-03-14 05:30:00"
```

**Security notes:**
- Stage-two PAT is read from file, never stored in code/logs
- `.credentials-local/` is in .gitignore (never committed)
- Stage-two PAT has full `repo` scope for private repository operations
- If PAT compromised, revoke on GitHub and regenerate immediately

**Troubleshooting:**
- "Stage-two PAT not found" → Create stage-two PAT and store in `.credentials-local/.stage-two_GH-PAT`
- "Authentication failed" → Stage-two PAT invalid/expired, regenerate
- "Remote not configured" → Run `git remote add private <url>`

**Cross-reference:** See `.claude/reference/git-pat-automation.md` for complete two-tier PAT setup guide

---

Current Version: v0.3.4

Author: Uncle Tallest

Last Updated: 14Mar2026

Updated by: Vector (Updated git-sync-private to use stage-two PAT system)

---
