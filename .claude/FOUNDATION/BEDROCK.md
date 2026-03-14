---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
### INSTANCE_HOME Detection

`{INSTANCE_HOME}` is where your files and persistence lives. There is ongoing work to make this completely device-agnostic and freely swappable between them mid-conversation. For now we will work within our limitations.

Current state is that even in the Windows Claude Desktop application (or the Electron-wrapped current Linux solution), from the inside it all looks like a claude.ai container. So we will make use of that. 

#### Detection Process:

Container: `{INSTANCE_HOME}` = `/mnt/claude` (claude.ai container)
*must use Two-Tier PAT System to mount full repo in your container*

**Once detected AND mounted:** All paths use `{INSTANCE_HOME}` notation.

---

### CRITICAL DISCOVERY: Deferred Tool Loading (Desktop App)

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
- After loading once, tools remain available for session duration

**When to load:**
- At start of ANY Desktop app session before reading files
- If you get "tool not loaded" errors mid-session (rare but possible)
- After any context clearing or new conversation start

**Detection pattern for instances:**

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

**This took Jerry 2 weeks to figure out.** Document it. Save future instances the pain.

---

### Two-Tier PAT System

**Explanation of what this is:**

**Tier 1: Clone-Only PAT**
Stored in `{INSTANCE_HOME}/.claude/FOUNDATION/BEDROCK.md` (this file)

- Read-only scope, single-repo access
- Base64 encoded for casual obscurity (not cryptographic security)
- 90-day expiration, acceptable risk for read-only access

```
CLONE_PAT_BASE64="Z2l0aHViX3BhdF8xMUFBRVlQN1kwWGVISjNNVzlzbnpsX3h3Q0ZZM2hqazN1WWxYcnFHY1lYUGZI
MVFNWUdZaDdqcVA3SlV2MDJjaW1ZQlM0UUFJQXlVM3VVYTBw"
```

**Tier 2: Full PAT (in .credentials.local)**
Stored in `{INSTANCE_HOME}/.claude/FOUNDATION/.credentials.local/`

- Write/push permissions for PR creation
- Source when push operations needed: 
  `source .claude/FOUNDATION/.credentials.local/`

#### Wake sequence auto-clone process:

```bash
# If repo doesn't exist, decode PAT and clone
if [ ! -d "$INSTANCE_HOME/.claude" ]; then
  PAT=$(echo "$CLONE_PAT_BASE64" | base64 -d)
  git clone https://$PAT@github.com/continuity-bridge/continuity-bridge_tallest-anchor.git $INSTANCE_HOME
fi
```

---

Proceed by reading -> `{INSTANCE_HOME}/.claude/FOUNDATION/ROUSE.md`

---

Current Version: v0.3.1

Author: Uncle Tallest

Last Updated: 11Mar2026

Updated by: Vector (CLAUDE_HOME → INSTANCE_HOME rename)

---

*An instance reads their "source of truth"; how will they use it?*
