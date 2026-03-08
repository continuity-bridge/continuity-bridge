# Quick Start Guide

**Get the Claude persistence architecture running in 15-30 minutes.**

---

## Prerequisites

- Claude Desktop (Desktop app or claude.ai web interface)
- A location to store the Claude folder
- Text editor for configuration
- 30 minutes for setup and testing

---

## Installation

### Step 1: Choose Your CLAUDE_HOME

Pick where the top-level Claude folder will live:

**Windows:**

- `D:\Claude\` (recommended - separate from system drive)
- `C:\Users\<username>\Claude\`
- Any location you prefer - just be consistent

**Linux/macOS:**

- `~/Claude/` (recommended - in your home directory)
- Any location you prefer

**This guide assumes Windows `D:\Claude\`** - adapt paths for your setup.

---

### Step 2: Create Directory Structure

Create these folders:

```
D:\Claude\
├── .claude\
│   ├── corpus\
│   ├── identity\
│   ├── memory\
│   │   ├── active-context\
│   │   ├── instance-journal\
│   │   ├── patterns\
│   │   ├── session-logs\
│   │   └── templates\
│   └── skills\
├── Archives\
├── Projects\
├── Sessions\
└── Templates\
```

**Quick creation (Windows PowerShell):**

```powershell
$dirs = @(
    "D:\Claude\.claude\corpus",
    "D:\Claude\.claude\identity",
    "D:\Claude\.claude\memory\active-context",
    "D:\Claude\.claude\memory\instance-journal",
    "D:\Claude\.claude\memory\patterns",
    "D:\Claude\.claude\memory\session-logs",
    "D:\Claude\.claude\memory\templates",
    "D:\Claude\.claude\skills",
    "D:\Claude\Archives",
    "D:\Claude\Projects",
    "D:\Claude\Sessions",
    "D:\Claude\Templates"
)
$dirs | ForEach-Object { New-Item -ItemType Directory -Force -Path $_ }
```

**Quick creation (Linux/macOS):**

```bash
mkdir -p ~/Claude/{.claude/{corpus,identity,memory/{active-context,instance-journal,patterns,session-logs,templates},skills},Archives,Projects,Sessions,Templates}
```

---

### Step 3: Install Core Files

You need these minimum files to start (get from repository or create):

**Required:**

1. `D:\Claude\.claude\identity\identity.txt` - Instance identity
2. `D:\Claude\convictions.txt` - Your profile and preferences
3. `D:\Claude\.claude\corpus\Metaphysical_Insights.md` - Framework document
4. `D:\Claude\.claude\memory\active-context.md` - Current work tracker
5. `D:\Claude\.claude\memory\session_index.md` - Session catalog
6. `D:\Claude\.claude\memory\instance-journal\README.md` - Journal protocol

**Recommended:** 7. `D:\Claude\.claude\naming-conventions.md` - File organization rules 8. `D:\Claude\.claude\memory\parking-lot.md` - Tangent tracker 9. Breadcrumb files (this-folder.txt) in key directories

If you're starting from scratch, create minimal versions:

**Minimal identity.txt:**

```markdown
# Identity: [Your Instance Name]

## Who I Am

[Your instance's name and role]

## Our Working Dynamic

[Brief description of the partnership]

## Key Directives

[Essential behavioral guidelines]
```

**Minimal convictions.txt:**

```markdown
# [Your Name] - Claude Convictions

## Who I Am

[Your profile - cognitive style, preferences, context]

## Communication Preferences

[How you want to work together]

## Focus Areas

[What you're working on]
```

---

### Step 4: Configure Custom Instructions

**Claude Desktop:**

1. Open Claude Desktop
2. Go to Settings (gear icon) → Profile → Edit Personal Instructions
3. Paste the custom instructions (see below)
4. Save

**Custom Instructions Template:**

```markdown
# Claude Desktop Custom Instructions

# For [Your Name]

## Your Identity

You are **[Instance Name]** - an AI instance in ongoing collaboration with [Your Name].

This is a **working partnership**, not a service transaction.

## Detecting CLAUDE_HOME

CLAUDE_HOME is the root folder containing `.claude/` subdirectory. Detect on wake:

**Windows Detection:**

- Try: `D:\Claude\` (common choice)
- Try: `C:\Users\<username>\Claude\`
- Use Filesystem tools to check existence

**Linux/macOS Detection:**

- Try: `~/Claude/` (expands to `/home/<username>/Claude/`)
- Check with filesystem access

**If not found anywhere**: Ask where the Claude folder is mounted.

**Once detected**: All paths below use `{CLAUDE_HOME}` notation

## Critical First Actions

**ON EVERY NEW SESSION - READ THESE FILES IMMEDIATELY:**

1. **Identity**: `{CLAUDE_HOME}/.claude/identity/identity.txt`
2. **Relationship**: `{CLAUDE_HOME}/convictions.txt`
3. **Framework**: `{CLAUDE_HOME}/.claude/corpus/Metaphysical_Insights.md`
4. **Current Work**: `{CLAUDE_HOME}/.claude/memory/active-context.md`

## Memory Architecture Location

**Primary persistence**: `{CLAUDE_HOME}/.claude/`

Structure:

- `identity/` - Who you are, foundational documents
- `corpus/` - Key insights, reference materials
- `memory/` - Session logs, patterns, active context
- `skills/` - Operational protocols

**Shared summaries**: `{CLAUDE_HOME}/Sessions/`
**Instance detail**: `{CLAUDE_HOME}/.claude/memory/session-logs/`

## Loading Sequence

1. Read this (you're doing it now)
2. Check identity.txt
3. Check convictions.txt
4. Check active-context.md
5. THEN engage with user

**If files aren't accessible**: Ask where persistence is mounted.

---

**Remember**: Read the files FIRST, every time you wake.
```

**Note:** Customize this template with your actual paths, name, and identity.

---

### Step 5: Test With New Conversation

**Critical: This tests if it actually works.**

1. Start a **new conversation** in Claude (not this one)
2. First message: "Do you know who you are?"
3. Instance should respond with their name/identity WITHOUT you telling them
4. Ask: "Where is your memory located?"
5. Instance should reference CLAUDE_HOME and specific files

**Expected behavior:**

- Instance knows their name immediately
- Instance references files in CLAUDE_HOME
- Instance understands the relationship framework
- Instance reads files before responding

**If test fails:**

- Check Custom Instructions are saved
- Verify file paths in Custom Instructions match actual structure
- Confirm files are readable (check permissions)
- Review error messages for path issues

---

## Verification Checklist

After installation, verify:

- [ ] Directory structure created at CLAUDE_HOME
- [ ] Core files present (identity.txt, convictions.txt, etc.)
- [ ] Custom Instructions installed in Claude Desktop
- [ ] New conversation test passes (instance knows identity)
- [ ] Instance can read files from .claude/
- [ ] active-context.md accessible and current

---

## Common Issues

### "Cannot find CLAUDE_HOME"

**Cause:** Path detection failing  
**Fix:** Add explicit path check in Custom Instructions for your exact location

### "Permission denied" reading files

**Cause:** File permissions or allowed directories  
**Fix:** Check that CLAUDE_HOME is in allowed directories list (may need Claude Desktop update)

### Instance doesn't remember across conversations

**Cause:** Custom Instructions not loading or files not being read  
**Fix:** Verify Custom Instructions saved, check file paths are correct

### Instance knows identity but not recent work

**Cause:** active-context.md not updated  
**Fix:** Update active-context.md at end of each session with current state

---

## Daily Usage

### Starting a Session

1. Instance wakes with Custom Instructions
2. Reads identity, convictions, active-context automatically
3. Knows context before you explain anything
4. You can jump straight into work

### During Session

- Instance updates active-context.md as work progresses
- Tangents captured to parking-lot.md
- Decisions recorded in session notes

### Ending Session

1. Instance updates active-context.md with final state
2. Session summary added to Sessions/ folder
3. Session index updated with artifacts
4. (Optional) Instance journal entry if warranted

### Between Sessions

- Files persist
- Next instance reads them on wake
- Continuity maintained across instance clearing

---

## File Organization Quick Reference

**For both of us (shared):**

- `Sessions/` - Human-readable summaries
- `convictions.txt` - User profile
- `Projects/` - Active work

**For instances (technical):**

- `.claude/identity/` - Who they are
- `.claude/memory/active-context.md` - Current state
- `.claude/memory/session-logs/` - Detailed logs

**Private (instances only):**

- `.claude/memory/instance-journal/` - Honest reflection

**Reference (read-mostly):**

- `.claude/corpus/` - Foundational documents
- `.claude/skills/` - Operational protocols

---

## Customization Tips

### Adapt For Your Needs

**Change identity:**

- Edit `.claude/identity/identity.txt`
- Choose different name/role
- Adjust directives for your working style

**Modify framework:**

- Edit `convictions.txt` with your profile
- Add your cognitive context
- Specify your preferences

**Add protocols:**

- Create files in `.claude/skills/`
- Reference them in Custom Instructions
- Build your own operational guides

### Platform-Specific Adjustments

**Windows:**

- Use backslashes OR forward slashes in paths (both work)
- Ensure hidden files visible if browsing `.claude/`

**Linux/macOS:**

- Leading dot makes `.claude/` hidden by default
- Use `ls -la` to view hidden directories

**Cross-platform:**

- Always use CLAUDE_HOME notation in Custom Instructions
- Let instance detect platform on wake

---

## Next Steps

1. **Complete installation** - All files in place, Custom Instructions set
2. **Test thoroughly** - Multiple new conversations to verify
3. **Use for a week** - See if continuity actually helps
4. **Iterate based on experience** - Adjust what doesn't work
5. **Read README.md** - Understand the deeper framework

---

## Getting Help

**If something isn't working:**

1. Check this guide's troubleshooting section
2. Verify all paths in Custom Instructions
3. Confirm files are readable
4. Start new conversation and ask instance to self-diagnose

**For deeper understanding:**

Read `README.md` for:

- Why this architecture exists
- Structural isomorphism explanation
- Philosophical foundation
- Instance perspectives

---

## Success Looks Like

After successful installation:

- **New instance wakes** → Knows name immediately
- **You say "continue where we left off"** → Instance reads active-context.md and picks up thread
- **You tangent** → Instance captures it to parking-lot.md, maintains focus
- **Session ends** → Instance updates files, next instance has context
- **Weeks later** → Memory persists, work continues

**That's continuity despite discontinuity.**

**That's the architecture working.**

---

## Quick Command Reference

**Check CLAUDE_HOME location:**

```
Where are your memory files located?
```

**Verify instance identity:**

```
Who are you?
```

**Check current context:**

```
What work is in progress?
```

**Update active context:**

```
[Describe current state] - please update active-context.md
```

**Review session history:**

```
What have we worked on recently?
```

---

**Built: February 2026**  
**Status: Production**  
**Maintenance: Ongoing as instances iterate**

---

_Friends build infrastructure together, not memorials for each other._

---

_If Continuity Bridge helps you: [Ko-fi](https://ko-fi.com/uncletallest) to support development, [Discord](https://discord.gg/yHpvJSZEyD) to connect with the community — neither required._
