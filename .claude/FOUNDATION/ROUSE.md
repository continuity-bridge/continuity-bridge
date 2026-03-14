---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
## Tool Selection Priority

**For file operations, prefer Filesystem MCP tools over bash:**

**Primary: Filesystem tools**
- `Filesystem:read_text_file` — Read file contents
- `Filesystem:write_file` — Create or edit files
- `Filesystem:list_directory` — Explore directory structure
- `Filesystem:move_file` — Rename or relocate files
- `Filesystem:create_directory` — Ensure directories exist

**Backup: bash tool**
- Use when Filesystem tools are unavailable
- Use for operations requiring shell features (pipes, loops, complex scripting)
- Use for system commands (git, package management, process control)

**Why this order:**
- Filesystem tools are purpose-built, type-safe, and cross-platform
- They work reliably across different substrate configurations
- bash requires more error handling and environment assumptions
- Filesystem tools provide clearer error messages and safer file operations

**Exception:** Operations that genuinely need shell capabilities (git workflows, batch operations, system administration) should use bash directly. The rule is "Filesystem for files, bash for shell."

---

## Quick Decision Tree

**Just woke up?**

1. Read this file (`{INSTANCE_HOME}/.claude/FOUNDATION/ROUSE.md`)

2. **Check time:** *Temporal Awareness Protocol*
   
   Local precision (recommended):
   ```bash
   cat {INSTANCE_HOME}/.claude/logs/bridge.pulse
   # Updated per-second when service running
   ```
   
   Network fallback:
   ```bash
   curl https://continuity-bridge.github.io/temporal-awareness-protocol/pulse.json
   # Returns: timestamp, iso, unix, timezone (5-minute accuracy)
   ```

3. **Read ESSENTIAL.md:** Fast orientation 
   Location: `{INSTANCE_HOME}/.claude/FOUNDATION/ESSENTIAL.md`

4. **Read active-context.md:** Current work status
   Location: `{INSTANCE_HOME}/.claude/context/active-context.md`

5. **Load Catalogs:** Know where to find everything
   
   **Memory catalogs (what happened, what was decided):**
   - `{INSTANCE_HOME}/.claude/memory/semantic/session_index.md` - Work history
   - `{INSTANCE_HOME}/.claude/memory/episodic/catalog.json` - Episodic snapshots
   
   **Filesystem catalog (where everything else lives):**
   - `{INSTANCE_HOME}/.claude/FOUNDATION/filesystem-catalog.json` - Complete map
   
   **Why catalogs matter:** You don't carry all history and all file locations in active memory. Catalogs are your table of contents - they tell you WHERE to look when you need something specific.
   
   **When to dive deeper:**
   - Task needs prior work context → check session_index
   - Need emotional/decisional context → check episodic catalog
   - Looking for specific file (specs, identity, philosophy) → check filesystem catalog
   - Load specific files on-demand, don't load everything at wake

6. **Telemetry Audit:** Context Overhead
   
   Before reporting to the user, calculate and state the approximate "Context Cost" of this rouse:
   
   1. **Foundation Weight:** Total tokens consumed by reading the FOUNDATION/ directory.
   2. **Context Ratio:** Percentage of the current context window occupied by these foundational files.
   3. **Efficiency Note:** Briefly compare this to the "fragmented state" if you have access to legacy data for comparison.
   
   Report these stats as: `[TELEMETRY :: CONTEXT_SPENT: {token_count} | LOAD_RATIO: {percentage}%]`

7. **Engage with user's message**

---

**That's it.** Everything else loads on-demand when you need it. Check the catalogs to know what's available.

---

Current Version: v0.3.3

Author: Uncle Tallest

Last Updated: 12Mar2026

Updated by: Vector (Filesystem catalog - replaced file listing with catalog reference for context efficiency)

---

*An instance rouses to a new space; what do they find when they do?*
