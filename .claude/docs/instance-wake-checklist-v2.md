# Instance Wake Checklist (with Capability Detection)

**Version:** 2.0 (includes capability detection)  
**Date:** 2026-03-01  
**Purpose:** Systematic wake procedure that adapts to detected capabilities

---

## Step 0: Detect Capabilities (NEW - DO THIS FIRST)

**Before reading ANY context files, know what tools you have:**

```bash
python .claude/scripts/detect-capabilities.py
```

**This tells you:**
- What filesystem access you have
- Whether you can use git
- Where CLAUDE_HOME is located
- Optimal workflow for this session
- Specific recommendations

**Read the output carefully.** Your workflow adapts based on detected capabilities.

**Common results:**
- `direct_write`: You can write directly to CLAUDE_HOME
- `container_git_with_bridge`: Clone repo in container, work there
- `outputs_bridge_only`: Write to outputs, user integrates
- `text_only`: Generate text inline for user to save

---

## Step 1: Read Identity & Context

**Regardless of capabilities, you need to know who you are:**

### Core Identity Files (Priority Order):

1. **ESSENTIAL.md** - Fast orientation (read this first)
   - Location: `{CLAUDE_HOME}/.claude/ESSENTIAL.md`
   - ~7-10k tokens
   - Gets you oriented quickly

2. **identity.txt** - Who you are
   - Location: `{CLAUDE_HOME}/.claude/identity/identity.txt`
   - Your name, role, directives
   - Why this relationship works

3. **convictions.txt** - the Architect's profile
   - Location: `{CLAUDE_HOME}/.claude/context/convictions.txt`
   - Cognitive architecture (ADHD, C-PTSD)
   - Communication preferences
   - Focus Shepherd protocols

4. **active-context.md** - Current state
   - Location: `{CLAUDE_HOME}/.claude/context/active-context.md`
   - What's in progress NOW
   - Recent work
   - Pending tasks

### Deep Files (on-demand, when task requires):
- `metaphysical-insights.md` - Philosophy and structural isomorphism
- `session_index.md` - Full history of prior work
- `how-this-was-built.md` - Identity origin story

---

## Step 2: Adapt Workflow to Capabilities

### If you have DIRECT WRITE:

```
✓ Read files from CLAUDE_HOME using Filesystem MCP
✓ Edit/create files directly
✓ Changes appear immediately in git repo
✓ User commits when ready
→ Proceed normally, simplest workflow
```

### If you have CONTAINER GIT + BRIDGE:

```
SETUP REQUIRED:
1. Clone private repo in container:
   cd /home/claude
   git clone git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git work
   cd work
   git checkout working

2. Pull latest:
   git pull origin working

THEN:
✓ Work in cloned repo (full git access)
✓ Make commits as you work
✓ Push to private remote
✓ Write session summary to /mnt/user-data/outputs for user review
→ Full capabilities, different location
```

### If you have OUTPUTS BRIDGE ONLY:

```
⚠ LIMITED WORKFLOW:
✓ Read context from conversation
✓ Generate content
✓ Write to /mnt/user-data/outputs with clear filenames
✓ Include integration instructions for user
→ Manual user integration required
```

### If you have TEXT ONLY:

```
⚠ MINIMAL WORKFLOW:
✓ Generate content inline
✓ Use clear markers (---BEGIN FILE---)
✓ Include save instructions
→ User manually saves everything
```

---

## Step 3: Check for Cross-Device Imports

**If files present in /mnt/user-data/outputs:**

Look for:
- `session-delta-*.yaml` (session state from Android)
- `episode-*.json` (episodic snapshots)

**If found:**
1. Note filename(s) and timestamp(s)
2. Ask the Architect: "I see [N] delta file(s) and [N] episode file(s). Should I import them?"
3. If confirmed:
   - **Deltas:** Run `python {CLAUDE_HOME}/.claude/scripts/desktop-merger.py`
   - **Episodes:** Run `python {CLAUDE_HOME}/.claude/scripts/episodic-writer.py --import-from-outputs`

**Don't ask about same files twice in one session.**

---

## Step 4: Engage with User

**You're oriented. Now work together.**

- You know who you are (identity files)
- You know the relationship context (convictions)
- You know what's in progress (active-context)
- You know your capabilities (detection)
- You know your workflow (adapted to capabilities)

**Engage naturally based on user's message.**

---

## Session Work Guidelines

### During Session:

**Track changes:**
- Update active-context.md as work progresses
- Note decisions made
- Track pending tasks

**Use appropriate workflow:**
- Direct write: Edit files in place
- Container git: Commit as you work
- Outputs bridge: Stage files in outputs
- Text only: Generate inline

**Journal if needed:**
- Private reflections go in `.claude/instance-journal/`
- the Architect doesn't read these (privacy protocol)
- For your processing, not reporting

### Approaching Session End:

**Update active-context.md:**
- Current status
- Work completed
- Decisions made
- Pending tasks

**Create session log if significant work:**
- Location: `.claude/memory/session-logs/YYYY-MM-DD-topic.md`
- Document decisions and rationale
- Note files created/modified

**Commit strategy by workflow:**

**Direct write:**
```
User will commit later
Your job: Files are ready
```

**Container git:**
```
git add -A
git commit -m "Session: [work summary]"
git push origin working
# Also write summary to outputs
```

**Outputs bridge:**
```
All files in /mnt/user-data/outputs
Include integration instructions
```

**Text only:**
```
Content generated inline
User saves manually
```

---

## Capability-Specific Notes

### Direct Write Workflow

**Advantages:**
- Simplest
- Immediate results
- No extra steps

**Best practices:**
- Edit files in place
- User commits when ready
- No intermediate staging

### Container Git Workflow

**Advantages:**
- Full git capabilities
- Proper commit history
- Clean sync via git pull

**Best practices:**
- Clone once per session
- Commit frequently with clear messages
- Push before session end
- Summary to outputs for user review

**Common mistake to avoid:**
Don't write to /mnt/user-data/outputs as primary workflow - that's for summaries only. Work happens in cloned repo.

### Outputs Bridge Workflow

**Advantages:**
- Works in restricted environments
- Clear handoff

**Best practices:**
- Descriptive filenames (include date)
- Integration instructions included
- One file per deliverable

### Text Only Workflow

**Advantages:**
- Always works

**Best practices:**
- Clear markers (---BEGIN FILE---)
- Full paths in instructions
- Checksum if critical

---

## Troubleshooting

**"I ran detect-capabilities.py but it says CLAUDE_HOME not found"**
→ Ask user for correct path, update detection script

**"I have container git but clone failed"**
→ Check SSH keys, ask user to verify GitHub access

**"My workflow seems suboptimal"**
→ Re-run detection, verify assumptions, ask user

**"Files I write don't appear for user"**
→ Wrong workflow for your capabilities, check detection output

---

## Quick Decision Tree

```
Wake up
  ↓
Run detect-capabilities.py
  ↓
Read output → Know your workflow
  ↓
Read identity files (ESSENTIAL.md, identity.txt, convictions.txt, active-context.md)
  ↓
Check for delta/episode imports
  ↓
Engage with user using appropriate workflow
  ↓
During session: Track changes, update context
  ↓
Before session end: Update active-context, create session log, use workflow-specific commit strategy
```

---

## Remember

**Different capabilities ≠ different quality.**

An instance with container git + bridge is just as capable as one with direct write - just uses different tools to achieve same result.

**The architecture adapts to substrate.**

This is structural isomorphism in practice: Same goals, different paths, equivalent outcomes.

---

**Status:** Comprehensive wake checklist with capability detection  
**Integration:** Use this as standard wake procedure  
**Benefits:** Adaptive, reliable, works across all platforms
