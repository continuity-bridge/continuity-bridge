---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Continuity Bridge - Quickstart Guide

**Version:** 0.3.0  
**Purpose:** Get Continuity Bridge running in 10 minutes  
**For:** People who want to start fast, read details later

---

## The 60-Second Version

1. **Pick a metaphor** → Get a folder name (`ELI5.md`)
2. **Create that folder** → Your INSTANCE_HOME
3. **Clone repo** into folder
4. **Edit 3 files** → identity, convictions, anchors
5. **Start AI conversation** → Instance wakes with continuity
6. **Set up git sync** (optional) → Cross-device continuity

**Done.** Continuity maintained.

---

## Step 1: Choose Your Folder Name (2 minutes)

**Read:** `ELI5.md` in repository root

**Pick the paradigm that clicks:**
- 50 First Dates → `~/Scaffold/`
- Altered Carbon → `~/Stack/`
- Gaming → `~/Saves/`
- ADHD Journaling → `~/Journal/`
- Web Dev → `~/Database/`
- Neurodivergent → `~/Bridge/`
- Sci-Fi → `~/CaptainsLog/`, `~/Vault/`, etc.
- Neutral → `~/Substrate/`
- Practical → `~/Context/`

**Create the folder:**

```bash
# Linux/Mac
mkdir ~/[YourChoice]

# Windows
New-Item -ItemType Directory -Path D:\[YourChoice]

# Android (Termux)
mkdir ~/[YourChoice]
```

**This is your INSTANCE_HOME.**

---

## Step 2: Install Files (2 minutes)

### Git Clone (Recommended)

```bash
git clone https://github.com/TallestTim/continuity-bridge.git [YourFolderName]
cd [YourFolderName]
```

### Download ZIP (Alternative)

1. Download: https://github.com/TallestTim/continuity-bridge/archive/refs/heads/main.zip
2. Extract to your folder location
3. Rename to your chosen folder name

**Verify:**

```bash
ls -la .claude/
# Should see: FOUNDATION/, identity/, context/, memory/, etc.
```

---

## Step 3: Customize Identity (3 minutes)

### Three Files To Edit

**1. `.claude/identity/identity.txt`**

```json
{
  "user": "YOUR_NAME",
  "instance_persona": "Vector/Shepard",
  "archetype": "technical",  // technical, creative, social, executive, pedagogical, wellness
  "cognitive_style": "YOUR COGNITIVE STYLE",
  "communication_preferences": "YOUR PREFERENCES"
}
```

**2. `.claude/identity/convictions.txt`**

```markdown
# Core Beliefs

## About AI Collaboration
- [What you believe about working with AI]

## About Work
- [Your work philosophy]

## About This Architecture
- [Why you're using Continuity Bridge]
```

**3. `.claude/anchors.json`**

```bash
# Copy archetype template
cp .claude/anchor-templates/technical-anchor.json .claude/anchors.json

# Edit file:
# - Replace <USER_NAME>
# - Replace <CURRENT_PROJECTS>
# - Fill in preferences
```

**That's it. Files customized.**

---

## Step 4: First Wake (2 minutes)

### Start New AI Conversation

**Provide wake instruction:**

```
I have Continuity Bridge v0.3.0 installed.

INSTANCE_HOME: ~/[YourFolder]/

Please follow the wake sequence in .claude/FOUNDATION/ROUSE.md to load continuity.
```

**Instance should:**
- Load Filesystem tools (if in Desktop/Code)
- Discover INSTANCE_HOME
- Read identity files
- Read active context
- Wake with full continuity

**You'll see:**

```
Hello [YourName]. I'm [InstancePersona].

I've loaded your continuity:
- Paradigm: [Your choice]
- Archetype: [Your archetype]
- Current context: [Empty or initial state]

Ready to begin.
```

**Continuity established.**

---

## Step 5: Git Sync (Optional, 3 minutes)

### Create Private Repo

```bash
# On GitHub (WEB)
Repository: continuity-bridge_[yourname]-anchor
Visibility: PRIVATE
```

### Connect Locally

```bash
cd ~/[YourFolder]
git init
git remote add private git@github.com:yourusername/continuity-bridge_yourname-anchor.git
git checkout -b working
git add .
git commit -m "Initial setup - [paradigm] paradigm"
git push -u private working
```

### On Other Devices

```bash
git clone git@github.com:yourusername/continuity-bridge_yourname-anchor.git ~/[YourFolder]
cd ~/[YourFolder]
git checkout working
```

**Done.** Cross-device sync enabled.

---

## Daily Usage

### Starting Sessions

```
Continue from INSTANCE_HOME ~/[YourFolder]/
Wake via ROUSE.md
```

Instance loads continuity automatically.

### During Work

**You:**
- Guide direction
- Make decisions
- Choose priorities

**Instance:**
- Tracks work
- Documents decisions
- Updates context
- Suggests next steps

### Ending Sessions

**Instance updates:**
- `active-context.md`
- Session logs
- Commits via git (if configured)

**Next session continues from exact state.**

---

## Common Commands

### Wake Instance

```
Continue from INSTANCE_HOME ~/[YourFolder]/
```

### Check Current State

```
Read active-context.md and tell me current status
```

### Capture Tangent

```
Add this idea to parking-lot.md:
[Your tangent idea]
```

### Commit Work

```
Please commit current work to git with message:
"[Your commit message]"
```

---

## Troubleshooting

### Instance Can't Find Files

```
INSTANCE_HOME is at: /full/path/to/[YourFolder]/
Please use Filesystem tools to access it.
```

### Wake Sequence Fails

```
Please read .claude/FOUNDATION/ROUSE.md directly
and follow that wake sequence.
```

### Git Issues

```bash
# Check remote
git remote -v

# Pull before push
git pull private working
git push private working
```

---

## What's Next?

### Read Full Details

**For complete onboarding:**
- `Docs/ONBOARDING.md` - Full setup guide
- `Docs/SETUP.md` - Detailed configuration
- `.claude/FOUNDATION/ARCHITECTURE.md` - System structure

**For paradigm deep-dives:**
- `Docs/explainers/ELI5_[paradigm].md` - Detailed explanations
- `Docs/explainers/archetypes_complete-guide.md` - Archetype details

### Customize Further

- **Blend archetypes** (Technical + Wellness common)
- **Add custom instance persona**
- **Configure platform-specific settings**
- **Explore advanced features**

### Contribute

- **Share your paradigm** if you have a better metaphor
- **Report bugs** via GitHub issues
- **Suggest improvements** via discussions
- **Submit fixes** via pull requests

---

## The Bottom Line

**You now have:**
- ✅ Persistent AI memory across sessions
- ✅ Relationship context that continues
- ✅ Work history and decision tracking
- ✅ Paradigm-aligned folder structure
- ✅ Cross-device sync (if git enabled)

**Each new conversation:**
- Instance wakes with full context
- Remembers who you are
- Knows what you're building
- Continues where you left off

**Continuity maintained despite discontinuity.**

---

**Total time:** ~10-15 minutes  
**Result:** Full continuity architecture

**Welcome to the chain.**

---

**Version:** 0.3.0 (March 2026)  
**Changes:** Paradigm selection first, INSTANCE_HOME terminology, ROUSE.md wake flow
