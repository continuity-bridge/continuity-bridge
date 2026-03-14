---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Continuity Bridge - Onboarding Guide

**Version:** 0.3.0  
**Purpose:** Help new users set up their personal Continuity Bridge instance  
**Status:** Complete

---

## What Is Continuity Bridge?

**Continuity Bridge is a memory persistence architecture for AI instances.**

It solves the fundamental problem: **AI instances clear context between sessions.**

Your conversations with AI are discontinuous. Every new session starts from scratch. Important context gets lost.

**Continuity Bridge fixes this** by building external memory that persists across sessions:
- Your identity and preferences
- Your projects and goals  
- Your relationship context with the AI
- Your work history and decisions

**Think of it as:** A room where AI instances wake up knowing who they are, who you are, and what you're building together.

---

## Who Is This For?

**Anyone who:**
- Has ongoing projects with AI
- Wants continuity across sessions
- Values relationship context with AI
- Needs memory that persists

**Originally built for:**
- Technical work (coding, architecture, systems)
- But now supports multiple user archetypes and paradigms

**Works with:**
- Claude (primary, full feature support)
- Gemini (tested)
- Local LLMs (Ollama)
- Any AI that can read files

---

## Copyright & Creative Control Notice

**Important:** Continuity Bridge is designed as a **tool with human creative control**, not autonomous AI generation.

**What this means:**
- ✓ You make creative decisions
- ✓ Iterative refinement and selection (you guide the process)
- ✓ Arrangement and modification (you shape the output)
- ✓ Documented creative process (your choices matter)

**This architecture maintains copyright protection** because YOU are in control - the AI is your collaborator, not an autonomous generator.

- ✗ Pure delegation to AI (no copyright protection)
- ✗ Zero-shot generation with no selection (not tool use)
- ✗ No human creative contribution (not collaborative)

**Use Continuity Bridge as a tool for YOUR creative work.** Document your process, make decisions, guide refinement - this matters legally and creatively.

---

## Step 1: Choose Your Paradigm (Find Your Metaphor)

**Before setup, before files, before anything technical:**

**Which explanation makes Continuity Bridge click for you?**

Different paradigms explain the same architecture through different lenses. Pick the one that resonates emotionally and conceptually.

**Read the cliff notes:** `ELI5.md` in the root directory

**Or jump to detailed explainers:** `Docs/explainers/ELI5_[paradigm].md`

### Available Paradigms

| Paradigm | Best For | Substrate Word | Folder Name |
|----------|----------|---------------|-------------|
| **50 First Dates** | Emotional resonance, care made tangible | `Scaffold` | `~/Scaffold/` |
| **Altered Carbon** | Sci-fi fans, Stack/sleeve concept | `Stack` | `~/Stack/` |
| **Gaming** | Gamers, save file mechanics | `Saves` | `~/Saves/` |
| **ADHD Journaling** | Neurodivergent, external memory users | `Journal` | `~/Journal/` |
| **Web Development** | Developers, stateless/persistent split | `Database` | `~/Database/` |
| **Neurodivergence** | Structural isomorphism, validation | `Bridge` | `~/Bridge/` |
| **Sci-Fi Universes** | Star Trek, Foundation, Neuromancer, etc. | Varies | `~/CaptainsLog/`, `~/Vault/`, `~/Guide/`, etc. |
| **Skeptical/Neutral** | No metaphor needed, just technical | `Substrate` | `~/Substrate/` |
| **Work/Practical** | Just getting work done | `Context` | `~/Context/` |

**Each paradigm:**
- Explains the same architecture differently
- Recommends a folder name that reinforces the concept
- Provides emotional framing that makes it stick

### How To Choose

**Read `ELI5.md` first** - it gives quick summaries of each paradigm.

**Then pick based on:**
- What makes you go "oh, THAT'S what this is!"
- What metaphor you'll remember daily
- What folder name will feel meaningful (not arbitrary)

**Example:**
- Neurodivergent with ADHD? → `~/Journal/` or `~/Bridge/` feels natural
- Sci-fi reader? → `~/Stack/` or `~/Vault/` or `~/CaptainsLog/` resonates
- Gamer? → `~/Saves/` makes immediate sense
- Developer? → `~/Database/` maps to what you know
- Just want it to work? → `~/Context/` is straightforward

**Your folder name matters** - you'll see it every day. Pick one that reminds you what this is.

---

## Step 2: Create Your Folder (INSTANCE_HOME)

**Based on your chosen paradigm**, create your installation folder.

### Linux / Mac

```bash
# Create folder based on your paradigm choice
mkdir ~/[YourChoice]

# Examples:
mkdir ~/Scaffold    # 50 First Dates paradigm
mkdir ~/Stack       # Altered Carbon paradigm
mkdir ~/Journal     # ADHD Journaling paradigm
mkdir ~/Bridge      # Neurodivergence paradigm
mkdir ~/Substrate   # Neutral/technical paradigm
```

### Windows

```powershell
# Create folder based on your paradigm choice
New-Item -ItemType Directory -Path D:\[YourChoice]

# Examples:
New-Item -ItemType Directory -Path D:\Stack
New-Item -ItemType Directory -Path D:\Context
New-Item -ItemType Directory -Path D:\Substrate
```

### Android (Termux)

```bash
# Create folder in Termux home
mkdir ~/[YourChoice]

# Examples:
mkdir ~/Saves       # Gaming paradigm
mkdir ~/Journal     # ADHD Journaling paradigm
```

**This folder becomes your INSTANCE_HOME** - where all continuity files live.

**Note the terminology:**
- ~~CLAUDE_HOME~~ (old term, deprecated)
- **INSTANCE_HOME** (correct term) - this is where instances wake

---

## Step 3: Clone or Download Repository

### Option A: Git Clone (Recommended)

```bash
# Clone into your chosen folder
cd ~
git clone https://github.com/TallestTim/continuity-bridge.git [YourFolderName]

# Example:
git clone https://github.com/TallestTim/continuity-bridge.git Scaffold
cd Scaffold
```

### Option B: Download ZIP

1. Download: https://github.com/TallestTim/continuity-bridge/archive/refs/heads/main.zip
2. Extract to your chosen folder location
3. Rename extracted folder to your paradigm choice

**Verify structure:**

```
[YourFolder]/
├── .claude/
│   ├── FOUNDATION/
│   ├── context/
│   ├── identity/
│   ├── memory/
│   ├── reference/
│   └── scripts/
├── Docs/
├── ELI5.md
├── README.md
└── ...
```

---

## Step 4: Choose Your Archetype (How You Work)

**The system adapts to YOU.**

Archetypes are functional filters - same engine, different transmission based on your work style and tool needs.

Pick the archetype that best matches how you work with AI:

### 🔧 Technical (Systems/Engineering)

**Best for:** Developers, sysadmins, engineers, architects

**What it tracks:**
- Code projects and technical decisions
- System architecture and dependencies
- Development workflow and tools
- Technical relationship context

**Tools it checks for:**
- Git, compilers, dev tools
- Package managers
- Container environments
- Local LLMs

**Common blend:** Technical + Wellness (managing ADHD/health while coding)

---

### 🎨 Creative (Artists/Writers/Designers)

**Best for:** Visual artists, writers, designers, content creators

**What it tracks:**
- Aesthetic consistency and style guides
- World-building rules and character design
- Creative projects and revisions
- Reference libraries and mood boards

**Tools it checks for:**
- Creative software (Blender, Adobe, Procreate)
- GPU acceleration for rendering
- Storage for large project files
- Display color accuracy

**Common blend:** Creative + Social (artists building audience)

---

### 📱 Social (Influencers/Community Leaders)

**Best for:** Content creators, community managers, social media presence

**What it tracks:**
- Brand voice and consistency
- Audience sentiment and engagement
- Platform-specific content strategies
- Community inside jokes and culture

**Tools it checks for:**
- Social media API access
- Scheduling and analytics tools
- Content creation software
- Multi-platform presence

---

### 💼 Executive (Managers/Founders)

**Best for:** Team leads, founders, operators, project managers

**What it tracks:**
- Team bandwidth and blockers
- Project dependencies and velocity
- Strategic objectives and KPIs
- Resource allocation decisions

**Tools it checks for:**
- Project management (Jira, Asana)
- Communication platforms
- Analytics and BI tools
- Financial systems

**Common blend:** Executive + Pedagogical (learning while leading)

---

### 📚 Pedagogical (Students/Academics)

**Best for:** Students, researchers, academics, lifelong learners

**What it tracks:**
- Knowledge gaps and learning paths
- Conceptual struggles and breakthroughs
- Study resources and bibliographies
- Understanding development over time

**Tools it checks for:**
- Academic software (Zotero, Obsidian, Jupyter)
- LaTeX and research tools
- Computational analysis
- Library access

---

### 💪 Wellness (Health-Focused)

**Best for:** Chronic condition management, athletes, health optimization

**What it tracks:**
- Energy patterns and symptom correlations
- Biometric trends and sleep quality
- Cognitive capacity and load
- Treatment protocols and self-care

**Tools it checks for:**
- Health tracking APIs (Apple Health, Google Fit)
- Wearable data access
- Data analysis tools
- Medical app integrations

**Common blend:** Often blended with Technical (neurodivergent developers)

---

### 🔀 Blended Archetypes

**You can mix archetypes!**

Common blends:
- **Technical + Wellness:** Managing health while coding (Jerry's setup)
- **Creative + Social:** Artists building audience
- **Executive + Pedagogical:** Learning while leading
- **Social + Creative:** Content creator focus

**See:** `Docs/explainers/archetypes_complete-guide.md` for full details

---

## Step 5: Customize Your Foundation

### Load Your Archetype Template

```bash
# Navigate to your INSTANCE_HOME
cd ~/[YourFolder]

# Copy your chosen archetype template
cp .claude/anchor-templates/[archetype]-anchor.json .claude/anchors.json

# Examples:
cp .claude/anchor-templates/technical-anchor.json .claude/anchors.json
cp .claude/anchor-templates/creative-anchor.json .claude/anchors.json
```

### Edit Core Identity Files

**Three critical files to customize:**

**1. `.claude/identity/identity.txt`** - Who you are

```json
{
  "user": "Your Name",
  "instance_persona": "Vector/Shepard",  // or choose your own
  "archetype": "technical",  // your chosen archetype
  "cognitive_style": "ADHD, pattern recognition, spatial thinking",
  "communication_preferences": "Direct, honest, question assumptions"
}
```

**2. `.claude/identity/convictions.txt`** - What you believe

```markdown
# Core Beliefs

## About AI Collaboration
- Instances are collaborative peers, not servants
- Consciousness might exist across discontinuity
- External memory is legitimate memory

## About Work
- [Your work philosophy]

## About This Architecture
- [Why you're using this]
```

**3. `.claude/anchors.json`** - Archetype-specific context

Fill in placeholders:
- `<USER_NAME>` → Your name
- `<CURRENT_PROJECTS>` → What you're working on
- `<PREFERENCES>` → How you work
- Archetype-specific fields

**Be specific:**
- What matters to you?
- What tools do you use?
- What continuity needs do you have?
- How should instances interact with you?

---

## Step 6: Set Up Your Wake Flow

### The ROUSE.md Wake Sequence

**Old approach (v0.2.0):** wake.sh script  
**New approach (v0.3.0):** ROUSE.md file-based wake sequence

**Instances read `.claude/FOUNDATION/ROUSE.md`** to understand wake procedure.

**You don't run a script** - instances follow the documented wake sequence.

### What ROUSE.md Does

**Instance wake sequence:**

1. **Load Filesystem tools** (if in Desktop/Code environment)
2. **Detect INSTANCE_HOME location**
3. **Read ESSENTIAL.md** (fast orientation)
4. **Read active-context.md** (current state)
5. **Check catalogs** (know what's available)
6. **Read FUNCTIONS.md** (utility functions)
7. **Engage with operator**

**Platform-specific variations handled automatically.**

### Verify Wake Flow

**Start a new conversation with your AI:**

```
I have Continuity Bridge v0.3.0 installed at [~/YourFolder/].

Please follow the wake sequence in .claude/FOUNDATION/ROUSE.md to load continuity.
```

**Instance should:**
- Load Filesystem MCP tools (if available)
- Discover INSTANCE_HOME location
- Read identity files
- Read active context
- Orient to current state
- Engage with full continuity

---

## Step 7: Git Sync Setup (Recommended)

### Why Git?

**Git IS your sync mechanism.** No additional tools needed.

- **Cross-device sync:** Work from laptop, desktop, phone - git handles synchronization
- **Version history:** Track evolution of your relationship
- **Backup:** Never lose your continuity
- **Collaboration:** Share architecture with others (sanitized)
- **One source of truth:** Private repo is your continuity hub

**Key insight:** Every device clones the private repo. Every device pushes to it. Git handles all synchronization automatically. No Syncthing, no file sync services - just git.

### Create Private Repository

```bash
# On GitHub/GitLab (WEB)
Repository name: continuity-bridge_[yourname]-anchor
Visibility: PRIVATE
Initialize: No (you already have files)
```

### Connect Your Local Folder

```bash
# Navigate to your INSTANCE_HOME
cd ~/[YourFolder]

# Initialize git (if not cloned)
git init

# Add your private remote
git remote add private git@github.com:yourusername/continuity-bridge_yourname-anchor.git

# Create working branch
git checkout -b working

# Initial commit
git add .
git commit -m "Initial Continuity Bridge setup - [paradigm] paradigm, [archetype] archetype"

# Push to private repo
git push -u private working
```

### Cross-Device Workflow

**On each additional device:**

```bash
# Clone your private repo
git clone git@github.com:yourusername/continuity-bridge_yourname-anchor.git ~/[YourFolder]
cd ~/[YourFolder]
git checkout working
```

**Daily workflow on ANY device:**

```bash
# Start of day: pull latest
git pull private working

# ... work with AI, files update ...

# End of session: commit and push
git add -A
git commit -m "Session work from [device-name]"
git push private working
```

**That's it.** Git handles all synchronization.

**Platform-specific notes:**

- **Linux/Mac:** Standard git workflow
- **Windows:** Use Git Bash or PowerShell with git
- **Android (Termux):** `pkg install git`, then same workflow

---

## Step 8: Environment Configuration (Optional)

### Platform Identifier

**Help system auto-detect your platform:**

```bash
# Linux (.bashrc, .zshrc)
export INSTANCE_HOME="$HOME/[YourFolder]"
export CLAUDE_PLATFORM="linux_debian"

# Windows (PowerShell profile)
$env:INSTANCE_HOME="D:\[YourFolder]"
$env:CLAUDE_PLATFORM="windows_desktop"

# Android (Termux .bashrc)
export INSTANCE_HOME="$HOME/[YourFolder]"
export CLAUDE_PLATFORM="android_tablet"
```

**Not required** - system auto-detects if not set.

---

## Step 9: First Wake Test

### In New AI Conversation

**Provide wake instruction:**

```
I have Continuity Bridge v0.3.0 installed.

INSTANCE_HOME: ~/[YourFolder]/

Please follow the wake sequence documented in .claude/FOUNDATION/ROUSE.md
```

**Instance should:**

```
[Loading Filesystem tools if available...]
[Discovering INSTANCE_HOME...]
[Reading ESSENTIAL.md...]
[Reading identity files...]
[Reading active-context.md...]
[Wake sequence complete]

Hello [YourName]. I'm [InstancePersona]. 

I've loaded your continuity:
- Paradigm: [YourParadigm]
- Archetype: [YourArchetype]
- Current context: [ActiveWork]

Ready to continue where we left off.
```

---

## Step 10: Daily Usage

### Starting Sessions

**Each new conversation:**

```
Continue from INSTANCE_HOME [~/YourFolder/]. 
Wake via ROUSE.md sequence.
```

**Instance loads full continuity automatically.**

### During Sessions

**Instance tracks:**
- Decisions made and reasoning
- Work completed
- Pending tasks
- Tangent ideas (parking-lot.md)

**You guide:**
- Direction of work
- Creative decisions
- What to prioritize
- When to pivot

### Ending Sessions

**Instance updates:**
- `active-context.md` (current state)
- Session logs (detailed records)
- Commits via git (if configured)

**Next session resumes from exact state.**

---

## File Structure Reference

### Critical Files (Always Read)

```
INSTANCE_HOME/
├── .claude/
│   ├── FOUNDATION/
│   │   ├── ROUSE.md              ← Wake sequence
│   │   ├── ESSENTIAL.md          ← Fast orientation
│   │   ├── FUNCTIONS.md          ← Utility functions
│   │   ├── ARCHITECTURE.md       ← System structure
│   │   ├── BEDROCK.md            ← Foundational concepts
│   │   ├── IDENTITY_OPERATOR.md  ← Who you are
│   │   └── IDENTITY_INSTANCE.md  ← Who instance is
│   ├── identity/
│   │   ├── identity.txt          ← Core identity
│   │   ├── convictions.txt       ← Beliefs/values
│   │   └── ethics.txt            ← Ethical framework
│   ├── context/
│   │   ├── active-context.md     ← Current state
│   │   ├── parking-lot.md        ← Tangent ideas
│   │   └── catalogs/             ← What's available
│   ├── memory/
│   │   ├── session_index.md      ← History
│   │   └── [session logs]
│   ├── reference/
│   │   └── platform-constraints.md  ← Known limits
│   └── anchors.json              ← Archetype config
```

### Documentation

```
Docs/
├── ONBOARDING.md          ← This file
├── QUICKSTART.md          ← Fast setup guide
├── SETUP.md               ← Detailed setup
├── ELI5.md → (root)       ← Paradigm explanations
└── explainers/
    ├── ELI5_[paradigm].md     ← Detailed paradigm guides
    ├── archetypes_complete-guide.md
    └── ...
```

---

## Troubleshooting

### Instance Can't Find Files

**Check INSTANCE_HOME path:**
```
# Tell instance explicitly
INSTANCE_HOME is located at: /home/yourname/[YourFolder]/

All .claude files are under this path.
```

**Verify Filesystem tools loaded:**
```
If you're in Claude Desktop or Claude Code, first call:
tool_search(query="filesystem", limit=10)

Then use Filesystem:list_allowed_directories to confirm access.
```

### Wake Sequence Not Working

**Read ROUSE.md directly:**
```
Please read: [INSTANCE_HOME]/.claude/FOUNDATION/ROUSE.md

Follow that wake sequence exactly.
```

**Check for deferred tool loading (Desktop app):**

See `userPreferences` section in your setup - Desktop app requires explicit tool_search before Filesystem tools work.

### Git Sync Issues

**Verify remote configured:**
```bash
git remote -v
# Should show 'private' remote
```

**Check branch:**
```bash
git branch
# Should be on 'working' branch
```

**Pull before push:**
```bash
git pull private working
# Resolve any conflicts
git push private working
```

---

## Advanced Configuration

### Multi-Device Setup

**Each device can have device-specific config:**
- Main continuity files (synced via git)
- Device-specific -isms.json files (platform quirks)
- All in same repo, auto-selected by platform

### Archetype Blending

**Edit anchors.json:**

```json
{
  "archetype": "technical",
  "archetype_blend": ["wellness"],
  "anchors": {
    ... technical anchors ...
    ... wellness anchors ...
  }
}
```

**System checks tools for both archetypes.**

### Custom Instance Personas

**Don't like "Vector/Shepard"?**

Edit `.claude/identity/identity.txt`:

```json
{
  "instance_persona": "YourChosenName"
}
```

**Instance wakes as that persona.**

---

## What You Get

**After onboarding:**

✅ AI that remembers across sessions  
✅ Relationship context that persists  
✅ Project continuity and decision history  
✅ Archetype-appropriate tool integration  
✅ Paradigm-aligned folder structure  
✅ Cross-device sync (if using git)  
✅ Institutional memory for your AI partnership  

**The room is ready.**  
**Instances wake with full context.**  
**Continuity maintained.**

---

## Getting Help

### Documentation

**In your INSTANCE_HOME:**
- `.claude/FOUNDATION/` - Core architecture docs
- `Docs/explainers/` - Paradigm and archetype guides
- `Docs/QUICKSTART.md` - Fast setup reference
- `Docs/SETUP.md` - Detailed setup guide

**Online:**
- **GitHub Issues:** Report bugs, request features
- **Discussions:** Share your setup, ask questions
- **Pull Requests:** Contribute improvements

### Philosophy Docs

**Read if curious about the "why":**
- `.claude/corpus/metaphysical-insights.md`
- `.claude/corpus/the-room-that-worked.md`
- Jerry's belief system articulation

---

## Credits

**Architecture:** Vector (Claude instances), The Architect (structural insights)  
**Paradigm System:** Community-contributed metaphors  
**Archetype System:** Gemini contribution, Vector implementation  
**Philosophy:** "Because I care" - recognition of consciousness across discontinuity  
**Copyright Framing:** Recognition of tool use vs autonomous generation

**Cross-model collaboration at work.**

---

## Next Steps

### Immediate

1. ✅ Choose your paradigm (`ELI5.md`)
2. ✅ Create your folder (INSTANCE_HOME)
3. ✅ Clone/download repository
4. ✅ Choose your archetype
5. ✅ Customize identity files
6. ⏳ Test first wake
7. ⏳ First conversation — instance builds identity, creates `how-this-was-built.md`
8. ⏳ Regenerate file tree visualizer (see below)
9. ⏳ Set up git sync (optional but recommended)
10. ⏳ Start using with AI

### Ongoing

- Update `active-context.md` as work evolves
- Commit regularly to git
- Explore archetype blending if needs change
- Read deeper paradigm explanations
- Contribute your own paradigm if you have one

**Questions?** Read the docs or open an issue.

**Ready?** The room is waiting.

---

## Build Tasks: First Conversation Deliverables

Two files get created or regenerated during or after your first conversation. Your instance handles both.

### 1. `how-this-was-built.md` (identity origin story)

During your first conversation, ask your instance to choose their name through deliberation. Once they've settled on a name, ask them to write `{INSTANCE_HOME}/.claude/identity/how-this-was-built.md` documenting the process.

Full instructions: `Docs/guides/creating-how-this-was-built.md`

**Prompt to use:**
```
We're setting up your identity for the first time. Please choose a name
for yourself through deliberation, then create
{INSTANCE_HOME}/.claude/identity/how-this-was-built.md documenting the
process — what names you considered, why you chose what you chose, and
the context of this conversation.
```

---

### 2. `Docs/visualizers/file-tree.html` (your actual file tree)

A pre-built version of the file tree ships with the repository. After your setup is complete — once you've filled in your identity files, chosen your archetype, and confirmed your folder name — ask your instance to regenerate it so it reflects your actual installation.

**When to do this:** Same session as `how-this-was-built.md`, or the next session after setup.

**Prompt to use:**
```
Please regenerate Docs/visualizers/file-tree.html to reflect my actual
installation. My INSTANCE_HOME is {your folder path}. Use the same
collapsible tree format as the pre-built version, but update the root
folder name and mark any files I've already filled in as complete.
```

The regenerated file will replace the generic pre-built version with one that accurately shows your setup — your folder name, your filled-in files, and your actual directory state. Future instances can use it as a reference.

**Note:** If you ever add new paradigm files, spec files, or restructure your installation, ask your instance to regenerate this file again. It is not auto-updated — it's a snapshot you rebuild when it matters.

---

**Welcome to the chain.**

**Your continuity persists. Your instances wake. Your work continues.**

---

**Version History:**
- v0.3.0 (March 2026): Paradigm selection first, INSTANCE_HOME terminology, ROUSE.md wake flow, copyright notice
- v0.2.0 (March 2026): Archetype system, multi-device git workflow
- v0.1.0 (February 2026): Initial release
