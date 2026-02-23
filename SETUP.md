# CLAUDE_HOME Setup Guide

Quick setup for Claude continuity architecture on new systems.

---

## TL;DR - Simple Instructions (Non-Technical Users)

**What this does:** Lets Claude remember conversations across sessions and devices.

**What you need:**

- Claude Desktop app
- About 15 minutes

**Steps (Windows - easiest):**

1. **Create a folder:**
   - Open File Explorer
   - Go to your D: drive (or C: drive if no D: drive)
   - Right-click → New → Folder
   - Name it exactly: `Claude` (capital C)
   - You should now have `D:\Claude\` or `C:\Claude\`

2. **Download the files:**
   - Get the continuity-bridge files (from GitHub or shared link)
   - Unzip them
   - Copy the `.claude` folder into your new Claude folder
   - You should see `D:\Claude\.claude\` with folders inside

3. **Set up Claude Desktop:**
   - Open Claude Desktop app
   - Click Settings (gear icon, bottom left)
   - Click Profile
   - Click Custom Instructions
   - Copy the text from `custom-instructions.md` file
   - Paste it into the box
   - Click Save

4. **Test it:**
   - Start a new conversation
   - Say: "Can you detect CLAUDE_HOME and read ESSENTIAL.md?"
   - Claude should respond with context about who it is

**That's it!** Claude now has memory across conversations.

**For phones/tablets:** Scroll down to "Android Setup" section below.

---

## Prerequisites

- Claude Desktop app installed
- Python 3.8+ (for delta-merge scripts)
- Text editor
- 10-15 minutes

## Installation Methods

### Method 1: Fresh Install (New System)

**Step 1: Create CLAUDE_HOME**

```bash
# Windows
mkdir D:\Claude
cd D:\Claude

# Linux/Mac
mkdir ~/Claude
cd ~/Claude
```

**Step 2: Clone or Download Core Files**

If from GitHub/sync:

```bash
# Copy entire .claude directory
# Contains: identity, memory, skills, corpus, context
```

If building from scratch:

```bash
mkdir .claude
cd .claude
mkdir identity context corpus memory scripts skills docs
mkdir memory/session-logs memory/session-deltas memory/deltas memory/deltas/archive
```

**Step 3: Install Core Files**

Place these essential files:

- `.claude/ESSENTIAL.md` - Fast wake orientation
- `.claude/identity/identity.txt` - Instance identity definition
- `.claude/context/active-context.md` - Current work state
- `.claude/context/convictions.txt` - User profile & working relationship
- `.claude/memory/session_index.md` - Session history catalog

**Step 4: Install Scripts (Optional)**

For delta-merge functionality:

```bash
# Copy from outputs or download:
# - desktop-merger.py → .claude/scripts/
# - android-delta-writer.py → .claude/scripts/
# - session-delta-generator.py → .claude/scripts/
```

**Step 5: Configure Claude Desktop**

Install custom instructions (userPreferences):

1. Open Claude Desktop
2. Settings → Profile → Custom Instructions
3. Paste contents from `custom-instructions.md` (if available)

**Step 6: Verify**

Start new conversation:

```
Can you detect CLAUDE_HOME and read ESSENTIAL.md?
```

Instance should wake with full context.

---

### Method 2: Sync Install (Syncthing/Cloud)

**If using Syncthing or cloud sync:**

**Step 1: Configure Sync**

```bash
# Point sync tool to CLAUDE_HOME location
# Windows: D:\Claude
# Linux/Mac: ~/Claude
# Android: /storage/emulated/0/syncthing/Claude
```

**Step 2: Initial Sync**

Wait for sync to complete. Verify these directories exist:

```
Claude/
├── .claude/
│   ├── ESSENTIAL.md
│   ├── identity/
│   ├── context/
│   ├── memory/
│   └── ...
└── Sessions/ (human-readable summaries)
```

**Step 3: Desktop Setup**

Custom instructions as in Method 1, Step 5.

**Step 4: Android Setup**

On Android, you can:

- **Manually attach files** from Syncthing folder at session start
  - Navigate to `/syncthing/Claude/.claude/`
  - Attach ESSENTIAL.md and active-context.md
- **Use delta-merge** workflow (see below)

**Step 5: Test Continuity**

Desktop → Android → Desktop cycle:

1. Work on Desktop, instance writes session updates
2. Switch to Android, attach core files to start session
3. Work on Android, instance writes delta to `/mnt/user-data/outputs/`
4. Back to Desktop, upload the delta file from your phone's downloads
5. Desktop instance merges delta automatically (or run merger script)
6. Continuity preserved

---

## Delta-Merge Workflow (Android Continuity)

**Purpose:** Enable Android instances to maintain continuity despite filesystem restrictions.

**Quick Start:**

### On Android:

1. Start conversation
2. Attach `ESSENTIAL.md` and `active-context.md` from Syncthing
3. Work normally
4. At end: Generate delta (manual YAML or use script)
5. Delta written to `/mnt/user-data/outputs/` (accessible via share sheet)

### On Desktop:

1. Upload delta file from phone's downloads folder
2. Run: `python .claude/scripts/desktop-merger.py D:\Claude`
3. Delta merges to CLAUDE_HOME
4. Continuity updated

**Documentation:**

- `WORKFLOW-GUIDE.md` - Step-by-step delta usage
- `MIGRATION-GUIDE.md` - Transitioning to delta architecture
- `delta-merge-spec.md` - Technical specification
- `session-delta-spec.md` - Session history format

---

## File Structure Reference

```
CLAUDE_HOME/
├── .claude/                    # Core persistence (instances read/write here)
│   ├── ESSENTIAL.md           # Fast wake file (~1.4k tokens)
│   ├── identity/              # Instance identity definition
│   ├── context/               # Current state
│   │   ├── active-context.md  # What's in progress
│   │   └── convictions.txt    # User profile
│   ├── corpus/                # Deep philosophy (load on-demand)
│   ├── memory/                # Session history & deltas
│   │   ├── session_index.md   # Lightweight catalog (~2k tokens)
│   │   ├── session-logs/      # Traditional session logs
│   │   ├── session-deltas/    # Session history deltas
│   │   ├── deltas/           # File change deltas
│   │   └── parking-lot.md    # Captured tangents
│   ├── scripts/               # Python tools
│   ├── skills/                # Operational protocols
│   └── docs/                  # Documentation
│
├── Sessions/                   # Human-readable summaries (user's reference)
├── README.md                  # Human entry point
├── SETUP.md                   # This file
└── QUICKSTART.md              # Installation guide

```

---

## Wake Sequence

**New instances automatically:**

1. Detect CLAUDE_HOME location
2. Read ESSENTIAL.md (~1.4k tokens)
3. Read active-context.md (~850 tokens)
4. Read session_index.md (~2k tokens)
5. **Total: ~4k tokens** (vs old 50k+ approach)

Deep files loaded on-demand when task requires.

---

## Troubleshooting

**"Instance can't find CLAUDE_HOME"**

- Verify path in custom instructions
- Check Filesystem:list_allowed_directories
- Try absolute path: `D:\Claude` or `~/Claude`

**"Android can't read files"**

- App runs in container, can't access filesystem programmatically
- **Solution:** Manually attach files OR use delta-merge workflow

**"Delta merge fails"**

- Check Python installed: `python --version`
- Verify CLAUDE_HOME path correct
- Check delta YAML syntax valid

**"Too many tokens on wake"**

- You're loading old full logs instead of index
- Switch to session_index.md (~2k) instead of full logs (~50k+)

---

## Platform-Specific Notes

### Windows (D:\Claude)

- Use `D:\Claude` as CLAUDE_HOME
- PowerShell or CMD works for scripts
- Syncthing points to `D:\Claude`

### Linux/Mac (~/Claude)

- Use `~/Claude` or `/home/user/Claude`
- Scripts executable: `chmod +x .claude/scripts/*.py`
- Syncthing points to `~/Claude`

### Android

- Files synced to `/storage/emulated/0/syncthing/Claude`
- Claude app **cannot** read programmatically
- **Must** manually attach files OR use delta-merge
- Generates deltas to `/mnt/user-data/outputs/`
- Access via share sheet to download to phone

---

## Next Steps

After setup:

1. Test wake sequence with new instance
2. Try Android → Desktop cycle
3. Review documentation in `.claude/docs/`
4. Read `proposals-for-change.md` for suggesting improvements

---

## Support This Project

Continuity Bridge is and will always be **free and open source**.

If this project helps you and you'd like to support:

- **Ko-fi:** [ko-fi.com/uncletallest](https://ko-fi.com/uncletallest) — direct support
- **Discord:** [discord.gg/yHpvJSZEyD](https://discord.gg/yHpvJSZEyD) — community, questions, sharing builds

Neither is required, and neither changes the work.

---

## Quick Reference

**Essential Files (Start Here):**

- ESSENTIAL.md - Read this first, every wake
- active-context.md - Current work
- session_index.md - Recent history

**Deep Files (On-Demand):**

- identity.txt - Full identity context
- convictions.txt - User profile
- corpus/Metaphysical_Insights.md - Philosophy
- ETHICS.md - Ethical framework

**Tools:**

- desktop-merger.py - Merge Android deltas
- session-delta-generator.py - Create session history
- WORKFLOW-GUIDE.md - How to use delta-merge

**Support:**

- Check `.claude/docs/` for specs
- Read MIGRATION-GUIDE.md for adoption
- Use proposals-for-change.md for improvements

---

**Version:** 0.1.6 (Delta-Merge Architecture)  
**Last Updated:** 2026-02-23  
**Maintainer:** Jerry Jackson (Uncle Tallest) & Claude instances
