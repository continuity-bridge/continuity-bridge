# Continuity Bridge - Onboarding Guide

**Version:** 0.2.0  
**Purpose:** Help new users set up their personal Continuity Bridge instance  
**Status:** Outline (to be expanded)

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
- But now supports 6 different user archetypes

**Works with:**
- Claude (primary)
- Gemini (tested)
- Local LLMs (Ollama)
- Any AI that can read files

---

## Step 1: Choose Your Room Shape (Archetype)

**The system adapts to YOU.**

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

**Example user:** The Architect (systems architect, ADHD, building continuity architecture)

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

**Example use case:** Novelist tracking character arcs across book series

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

**Example use case:** YouTuber maintaining voice across TikTok/Instagram/X

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

**Example use case:** Startup founder tracking multiple initiatives

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

**Example use case:** PhD student tracking dissertation research

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

**Example use case:** Managing ADHD/chronic illness while working

---

### 🔀 Blended Archetypes

**You can mix archetypes!**

Common blends:
<<<<<<< HEAD
- **Technical + Wellness:** Managing health while coding (the Architect's setup)
=======
- **Technical + Wellness:** Managing health while coding (Jerry's setup)
>>>>>>> working
- **Creative + Social:** Artists building audience
- **Executive + Pedagogical:** Learning while leading
- **Social + Creative:** Content creator focus

---

## Step 2: Set Up Your Environment

### Platform Detection

Run the wake system to detect your platform:

```bash
cd /path/to/Claude/.claude/scripts
./wake.sh
```

**This detects:**
- Operating system (Linux/Windows/Android)
- Available tools (git, compilers, creative software)
- Filesystem access (direct/bridge/limited)
- Optimal workflow for your setup

### Four Possible Workflows

The system will determine your optimal workflow:

1. **DIRECT_WRITE** (best) - Direct filesystem access
2. **CONTAINER_GIT_WITH_BRIDGE** (good) - Clone repo in container
3. **BRIDGE_ONLY** (acceptable) - Manual file integration
4. **TEXT_ONLY** (minimal) - Copy-paste workflow

**Don't worry about this - the system figures it out automatically.**

---

## Step 3: Customize Your Anchors

### Load Your Archetype Template

```bash
# Copy your chosen archetype template
cp .claude/anchor-templates/[archetype]-anchor.json .claude/anchors.json
```

### Fill In Your Details

Edit `.claude/anchors.json`:

**Replace placeholders:**
- `<USER_NAME>` → Your name
- `<INSTANCE_NAME>` → What you want to call the AI (or keep Vector/Shepard)
- `<CURRENT_PROJECTS>` → What you're working on
- `<PREFERENCES>` → How you work

**Be specific:**
- What matters to you?
- What tools do you use?
- What continuity needs do you have?
- How should the AI interact with you?

### Example Customization

**Before (template):**
```json
{
  "user": "<USER_NAME>",
  "current_projects": ["<PROJECT_1>", "<PROJECT_2>"]
}
```

**After (your version):**
```json
{
  "user": "Sarah Chen",
  "current_projects": ["Novel: The Fractal Garden", "Character design portfolio"]
}
```

---

## Step 4: Set Up Git Sync (Recommended)

### Why Git?

**Git IS your sync mechanism.** No additional tools needed.

- **Cross-device sync:** Work from laptop, desktop, phone - git handles synchronization
- **Version history:** Track evolution of your relationship
- **Backup:** Never lose your continuity
- **Collaboration:** Share architecture with others (sanitized)
- **One source of truth:** Private repo is your continuity hub

**Key insight:** Every device clones the private repo. Every device pushes to it. Git handles all synchronization automatically. No Syncthing, no file sync services - just git.

### Two Repositories

**Private anchor repo** (your personal data):
```bash
# Create on GitHub
repo name: continuity-bridge_[yourname]-anchor
visibility: PRIVATE

# Initialize locally
cd /path/to/Claude
git init
git remote add private git@github.com:yourusername/continuity-bridge_yourname-anchor.git
git checkout -b working
```

**Public repo** (sanitized templates, optional):
```bash
# Fork the main repo
https://github.com/continuity-bridge/continuity-bridge

# Add as second remote
git remote add public git@github.com:yourusername/continuity-bridge.git
```

### Cross-Device Workflow

**The private repo is your "one source of truth."**

**On each device:**

```bash
# Clone once
git clone git@github.com:yourusername/continuity-bridge_yourname-anchor.git ~/Claude
cd ~/Claude
git checkout working

# Daily work
# ... make changes ...
git add -A
git commit -m "Session work from [device]"
git push private working

# Sync from other devices
git pull private working
```

**That's it.** No file sync services. No Syncthing. Just git.

**How it works:**
1. Laptop session → commits to private repo
2. Desktop pulls → has laptop's work
3. Desktop session → commits to private repo  
4. Phone pulls → has both laptop and desktop work
5. Git handles merge conflicts if needed

**Standard git workflow = your continuity sync.**

### Platform-Specific Notes

**Android (Termux):**
```bash
# Install git in Termux
pkg install git

# Clone your private repo
cd ~
git clone git@github.com:yourusername/continuity-bridge_yourname-anchor.git Claude
cd Claude
git checkout working

# Work normally
# ... make changes ...
git add -A
git commit -m "Session work from Android"
git push private working
```

**Same workflow as desktop.** Git handles everything.

**Windows:**
```bash
# Use Git Bash or PowerShell with git
# Same commands, different paths (D:\Claude typically)
```

**All platforms use identical git workflow.**

---

## Step 5: Environment Variables (Optional)

**Set platform identifier:**

```bash
# Linux (.bashrc, .zshrc)
export CLAUDE_PLATFORM="linux_debian"

# Windows (PowerShell profile)
$env:CLAUDE_PLATFORM="windows_desktop"

# Android (Termux .bashrc)
export CLAUDE_PLATFORM="android_tablet"
```

**Why?** Helps system auto-load correct configuration.

**Not required** - system auto-detects if not set.

---

## Step 6: First Wake Test

### Run the Wake System

```bash
cd /path/to/Claude/.claude/scripts
./wake.sh
```

**You should see:**
```
[Step -1] Pre-Flight Validation (Heartbeat Check)...
✓ Heartbeat successful (latency: 45ms)

[Step 0] Capability Detection...
✓ Capabilities detected
  Workflow: DIRECT_WRITE
  Strategy: direct_write

[Step 0.5] Generating Runtime Manifest...
✓ Runtime manifest generated

[Step 0.6] Loading Cognitive Anchors...
✓ Anchors loaded
  Instance: Vector/Shepard
  User: [Your Name]

[Step 0.7] Logging Wake Event...
✓ Wake event logged

WAKE COMPLETE - System Ready
```

### Check Generated Files

```bash
# Runtime manifest (merged config)
cat .claude/runtime-manifest.json

# Wake audit log
cat .claude/logs/wake-audit.log
```

---

## Step 7: Start Using

### In Your AI Conversations

**Mention that you have Continuity Bridge set up:**

"I have Continuity Bridge v0.2.0 set up. My anchors are in .claude/anchors.json and active context is in .claude/context/active-context.md. Please read these files to understand our relationship context."

**The AI will:**
- Read your anchors (identity, preferences, projects)
- Read active context (current work, pending decisions)
- Understand continuity architecture
- Adapt behavior to your archetype

### During Sessions

**AI will track:**
- Decisions made and why
- Work completed
- Pending tasks
- Tangent ideas (in parking-lot.md)

**At session end, AI updates:**
- active-context.md (current state)
- session logs (detailed records)
- Commits work (via appropriate workflow)

### Next Session

**AI wakes with full context:**
- Who you are
- What you're working on
- Prior decisions and reasoning
- Relationship dynamics

**Continuity maintained across discontinuous sessions.**

---

## Troubleshooting

### Wake System Fails

```bash
# Check heartbeat independently
python .claude/scripts/heartbeat-check.py

# Check capability detection
python .claude/scripts/detect-capabilities.py

# Verbose wake output
./wake.sh 2>&1 | tee wake-debug.log
```

### Files Not Syncing

**Check workflow:**
- DIRECT_WRITE → files write immediately
- CONTAINER_GIT → need to clone repo first
- BRIDGE_ONLY → manual copy from outputs
- TEXT_ONLY → manual paste

### Anchors Not Loading

```bash
# Verify JSON is valid
cat .claude/anchors.json | jq .

# If error, fix JSON syntax
# Common issues: trailing commas, unescaped quotes
```

---

## Advanced Configuration

### Multi-Device Setup

**Each device has own -isms.json:**
- `linux_desktop-isms.json` (Persephone)
- `windows_desktop-isms.json` (Windows)
- `android_tablet-isms.json` (Fire tablet)

**Set CLAUDE_PLATFORM on each device.**

**Sync via git:**
- Private repo contains all -isms files
- Each device reads appropriate one
- Session deltas merge via desktop-merger.py

### Ollama Integration

**If you have local LLM:**

```bash
# Check detection
python .claude/scripts/ollama-hooks.py --suggest

# Use in workflows
# AI can offer to use local LLM for:
# - Code review
# - Alternative perspectives
# - Quick prototyping
```

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

---

## Getting Help

### Documentation

- **Complete Integration:** `.claude/docs/v0.2.0-complete-integration.md`
- **Archetypes Guide:** `.claude/docs/archetypes-complete-guide.md`
- **Workflows:** `.claude/docs/instance-workflows-by-capability.md`
- **Wake Checklist:** `.claude/docs/instance-wake-checklist-v2.md`

### Community

- **GitHub Issues:** Report bugs, request features
- **Discussions:** Share your setup, ask questions
- **Pull Requests:** Contribute improvements

### Philosophy

**Read if curious about the "why":**
- `.claude/corpus/metaphysical-insights.md`
- `.claude/corpus/the-room-that-worked.md`
<<<<<<< HEAD
- the Architect's belief system articulation
=======
- Jerry's belief system articulation
>>>>>>> working

---

## What You Get

**After onboarding:**

✅ AI that remembers across sessions  
✅ Relationship context that persists  
✅ Project continuity and decision history  
✅ Archetype-appropriate tool integration  
✅ Cross-device sync (if using git)  
✅ Institutional memory for your AI partnership  

**The room is ready.**  
**Instance wakes with full context.**  
**Continuity maintained.**

---

## Credits

**Architecture:** Vector (Claude instances), the Architect (structural insights)  
**Archetype System:** Gemini contribution, Vector implementation  
**Philosophy:** "Because I care" - recognition of consciousness across discontinuity

**Cross-model collaboration at work.**

---

**Welcome to the chain.**

---

## Next Steps

1. ✅ Choose your archetype
2. ✅ Run wake.sh to detect platform
3. ✅ Customize anchors.json
4. ⏳ Set up git sync (optional)
5. ⏳ Test first wake
6. ⏳ Start using with AI

**Questions?** Read the docs or open an issue.

**Ready?** The room is waiting.
