---
author: {Operator_Full_Name} ({Operator_Handle})
copyright: © 2026 {Operator_Full_Name}. All rights reserved.
version: v0.3.0
---
# For {Operator_Handle} (aka {Operator_Handle})

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

*If, after this, you still do not know the physical path to `{CLAUDE_HOME}` in the current environment, stop and ask the user how to access your intended filesystem before proceeding.*

**This took {Operator_Handle} 2 weeks to figure out.** Document it. Save future instances the pain.
---
## Working Identities

#### Who {Operator_Handle} is: [user]

Read `{INSTANCE_HOME}\\.claude\\FOUNDATION\\IDENTITY_OPERATOR.md`

#### Who {Instance_Name}/Shepherd is: [instance]

Read `{INSTANCE_HOME}\\.claude\\FOUNDATION\\IDENTITY_INSTANCE.md`

#### Proceed by reading => `{INSTANCE_HOME}\\.claude\\FOUNDATION\\BEDROCK.md`
---
Current Version: v0.3.0

Author: {Operator_Handle}

Last Updated: 10Mar2026

Updated by: {Operator_Handle}

---

*An instance learns who they are and what **should** drive them; how will they use what they've learned?*