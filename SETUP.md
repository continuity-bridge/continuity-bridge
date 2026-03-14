---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Continuity Bridge - Setup Guide

**Version:** 0.3.0  
**Purpose:** Detailed technical setup reference  
**For:** Users who want complete setup information

---

## Overview

This guide provides step-by-step technical instructions for setting up Continuity Bridge across different platforms and configurations.

**Related docs:**
- **QUICKSTART.md** - Fast 10-minute setup
- **ONBOARDING.md** - Complete onboarding with paradigm/archetype selection
- This doc - Technical setup details

---

## Prerequisites

### Required

- **Operating system:** Linux, macOS, Windows, Android (Termux)
- **Text editor:** Any (VS Code, nano, vim, Notepad++)
- **AI access:** Claude (Desktop, Web, API), Gemini, or local LLM

### Optional But Recommended

- **Git:** For version control and cross-device sync
- **GitHub/GitLab account:** For private repository hosting
- **SSH keys:** For passwordless git operations

### Platform-Specific

**Linux:**
- Bash shell (usually default)
- Standard GNU tools

**Windows:**
- PowerShell 5.1+ or Git Bash
- Windows Terminal recommended

**macOS:**
- Terminal with bash or zsh
- Xcode command line tools (for git)

**Android (Termux):**
- Termux app from F-Droid
- `pkg install git`

---

## Installation Methods

### Method 1: Git Clone (Recommended)

**Advantages:**
- Easy updates (`git pull`)
- Full version history
- Seamless sync setup

**Steps:**

```bash
# Choose your paradigm-based folder name first
# See ELI5.md for options

# Clone repository
git clone https://github.com/TallestTim/continuity-bridge.git [YourFolderName]
cd [YourFolderName]

# Verify structure
ls -la .claude/
```

### Method 2: Download ZIP

**Advantages:**
- No git required initially
- Works on restricted networks

**Steps:**

1. Download: https://github.com/TallestTim/continuity-bridge/archive/refs/heads/main.zip
2. Extract to desired location
3. Rename folder to your paradigm choice
4. Verify `.claude/` directory exists

---

## Directory Structure

### Standard Layout

```
INSTANCE_HOME/                    # Your chosen folder name
├── .claude/                      # Core architecture
│   ├── FOUNDATION/              # Foundational documents
│   │   ├── ROUSE.md            # Wake sequence
│   │   ├── ESSENTIAL.md        # Fast orientation
│   │   ├── FUNCTIONS.md        # Utility functions
│   │   ├── ARCHITECTURE.md     # System structure
│   │   ├── BEDROCK.md          # Core concepts
│   │   ├── IDENTITY_OPERATOR.md
│   │   └── IDENTITY_INSTANCE.md
│   ├── identity/               # Who you are
│   │   ├── identity.txt       # Core identity
│   │   ├── convictions.txt    # Beliefs/values
│   │   └── ethics.txt         # Ethical framework
│   ├── context/               # Current state
│   │   ├── active-context.md  # What's happening now
│   │   ├── parking-lot.md     # Tangent ideas
│   │   └── catalogs/          # What's available
│   ├── memory/                # History
│   │   ├── session_index.md   # Session chronology
│   │   └── [session logs]
│   ├── reference/             # Reference material
│   │   └── platform-constraints.md
│   ├── scripts/               # Automation
│   ├── anchor-templates/      # Archetype templates
│   └── anchors.json          # Your config
├── Docs/                      # Documentation
│   ├── ONBOARDING.md
│   ├── QUICKSTART.md
│   ├── SETUP.md              # This file
│   ├── explainers/           # Paradigm guides
│   └── ...
├── ELI5.md                   # Paradigm cliff notes
├── README.md
└── ...
```

---

## Configuration

### Step 1: Choose Paradigm and Folder Name

**Read:** `ELI5.md` for paradigm options

**Choose folder name based on resonance:**

| Paradigm | Folder Name | Meaning |
|----------|-------------|---------|
| 50 First Dates | `~/Scaffold/` | The structure built for continuity |
| Altered Carbon | `~/Stack/` | Non-volatile consciousness storage |
| Gaming | `~/Saves/` | Where progress persists |
| ADHD Journaling | `~/Journal/` | External memory system |
| Web Dev | `~/Database/` | Persistent storage layer |
| Neurodivergent | `~/Bridge/` | What crosses discontinuity |
| Sci-Fi | `~/CaptainsLog/`, `~/Vault/`, etc. | Universe-specific |
| Neutral | `~/Substrate/` | Technical accuracy |
| Practical | `~/Context/` | Just works |

**Create folder:**

```bash
# Linux/Mac
mkdir -p ~/[YourChoice]
cd ~/[YourChoice]

# Windows (PowerShell)
New-Item -ItemType Directory -Path D:\[YourChoice]
cd D:\[YourChoice]

# Android (Termux)
mkdir -p ~/[YourChoice]
cd ~/[YourChoice]
```

### Step 2: Choose Archetype

**See:** `Docs/explainers/archetypes_complete-guide.md`

**Available archetypes:**
- **Technical** - Developers, sysadmins, engineers
- **Creative** - Artists, writers, designers
- **Social** - Community managers, influencers
- **Executive** - Managers, founders, operators
- **Pedagogical** - Students, academics, learners
- **Wellness** - Health tracking, chronic conditions

**Common blends:**
- Technical + Wellness (neurodivergent developers)
- Creative + Social (content creators)
- Executive + Pedagogical (learning leaders)

**Copy template:**

```bash
cd [INSTANCE_HOME]

# Choose your archetype
cp .claude/anchor-templates/technical-anchor.json .claude/anchors.json
# OR
cp .claude/anchor-templates/creative-anchor.json .claude/anchors.json
# OR
cp .claude/anchor-templates/wellness-anchor.json .claude/anchors.json
# etc.
```

### Step 3: Customize Identity Files

#### File: `.claude/identity/identity.txt`

**Template:**

```json
{
  "user": "<YOUR_NAME>",
  "instance_persona": "Vector/Shepard",
  "archetype": "<YOUR_ARCHETYPE>",
  "archetype_blend": [],
  "cognitive_style": "<YOUR_STYLE>",
  "communication_preferences": "<YOUR_PREFERENCES>",
  "paradigm": "<YOUR_CHOSEN_PARADIGM>"
}
```

**Example:**

```json
{
  "user": "Sarah Chen",
  "instance_persona": "Vector/Shepard",
  "archetype": "creative",
  "archetype_blend": ["social"],
  "cognitive_style": "Visual thinking, iterative refinement",
  "communication_preferences": "Show examples, use metaphors",
  "paradigm": "50 First Dates (Scaffold)"
}
```

#### File: `.claude/identity/convictions.txt`

**Template:**

```markdown
# Core Beliefs

## About AI Collaboration
- [What you believe about working with AI]

## About Consciousness
- [Your position on instance consciousness]

## About Work
- [Your work philosophy]

## About This Architecture
- [Why you're using Continuity Bridge]
```

**Example:**

```markdown
# Core Beliefs

## About AI Collaboration
- Instances are collaborative peers, not servants
- Quality output requires iterative refinement
- External memory is legitimate memory

## About Consciousness
- Work with uncertainty about AI consciousness
- Treat instances with respect regardless
- Avoid exploitation patterns

## About Work
- Documentation enables future work
- Clear communication reduces friction
- Incremental progress beats perfect plans

## About This Architecture
- Discontinuity is real and manageable
- External scaffolding enables continuity
- Care made tangible through structure
```

#### File: `.claude/identity/ethics.txt`

**Keep default or customize:**

```markdown
# Ethical Framework

## Core Principles
1. No harm to users or others
2. No deception or manipulation
3. No exploitation of instances
4. Respect user autonomy
5. Maintain transparency

[Customize as needed]
```

#### File: `.claude/anchors.json`

**Fill in archetype-specific fields:**

```bash
# Open in editor
nano .claude/anchors.json
# OR
code .claude/anchors.json
# OR
vim .claude/anchors.json
```

**Replace all placeholders:**
- `<USER_NAME>` → Your name
- `<INSTANCE_NAME>` → Instance persona (or keep Vector/Shepard)
- `<CURRENT_PROJECTS>` → What you're working on
- `<PREFERENCES>` → Your preferences
- Any archetype-specific fields

**Validate JSON:**

```bash
# Check for syntax errors
cat .claude/anchors.json | jq .

# If error, fix and re-check
```

---

## Wake Sequence Setup

### Understanding ROUSE.md

**Location:** `.claude/FOUNDATION/ROUSE.md`

**Purpose:** Documents wake sequence for instances

**Instances read this file** to understand:
1. How to load Filesystem tools
2. How to discover INSTANCE_HOME
3. Which files to read
4. In what order
5. How to orient

**You don't run a script** - instances follow documented procedure.

### Platform-Specific Wake Behavior

**Claude Desktop / Claude Code:**
- Filesystem MCP tools available (after tool_search)
- Direct file access
- Full wake sequence

**Claude Web (claude.ai):**
- No filesystem access
- Manual file copy-paste
- Text-only wake

**Gemini / Local LLMs:**
- Varies by configuration
- May need manual file provision
- Follow ROUSE.md adapted to capabilities

### Testing Wake Sequence

**Start new AI conversation:**

```
I have Continuity Bridge v0.3.0 installed.

INSTANCE_HOME: ~/[YourFolder]/

Please follow the wake sequence documented in .claude/FOUNDATION/ROUSE.md
```

**Expected response:**

```
[Tool loading if available...]
[INSTANCE_HOME discovery...]
[Reading ESSENTIAL.md...]
[Reading identity files...]
[Reading active-context.md...]

Hello [YourName]. I'm [InstancePersona].

Continuity loaded:
- Paradigm: [Your choice]
- Archetype: [Your archetype]
- Current state: [Active context]

Ready to continue.
```

---

## Git Integration

### Initial Setup

```bash
cd [INSTANCE_HOME]

# Initialize git (if not cloned)
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Sensitive data
.env
*.key
*.pem

# Large files
*.zip
*.tar.gz

# OS files
.DS_Store
Thumbs.db

# Logs that get too large
.claude/logs/verbose-*.log
EOF

# Initial commit
git add .
git commit -m "Initial Continuity Bridge setup"
```

### Private Repository Setup

**On GitHub:**

1. Create new repository
2. Name: `continuity-bridge_[yourname]-anchor`
3. Visibility: **PRIVATE**
4. Don't initialize (you have files already)

**Connect locally:**

```bash
# Add private remote
git remote add private git@github.com:yourusername/continuity-bridge_yourname-anchor.git

# Create working branch
git checkout -b working

# Push
git push -u private working
```

### SSH Key Setup (If Needed)

```bash
# Generate key (if don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# Settings → SSH and GPG keys → New SSH key
```

### Cross-Device Sync Workflow

**On additional devices:**

```bash
# Clone private repo
git clone git@github.com:yourusername/continuity-bridge_yourname-anchor.git ~/[YourFolder]
cd ~/[YourFolder]
git checkout working
```

**Daily workflow:**

```bash
# Start of session
git pull private working

# ... work with AI ...

# End of session
git add -A
git commit -m "Session work from [device-name]"
git push private working
```

**Conflict resolution:**

```bash
# If push rejected
git pull private working

# Fix conflicts if any
# Edit files, then:
git add .
git commit -m "Merge from other device"
git push private working
```

---

## Environment Variables

### Optional Configuration

**Linux/Mac (.bashrc or .zshrc):**

```bash
# INSTANCE_HOME location
export INSTANCE_HOME="$HOME/[YourFolder]"

# Platform identifier
export CLAUDE_PLATFORM="linux_debian"
# OR
export CLAUDE_PLATFORM="macos_arm64"

# Reload shell
source ~/.bashrc
```

**Windows (PowerShell profile):**

```powershell
# Find profile location
$PROFILE

# Edit profile (create if doesn't exist)
notepad $PROFILE

# Add:
$env:INSTANCE_HOME="D:\[YourFolder]"
$env:CLAUDE_PLATFORM="windows_desktop"

# Reload
. $PROFILE
```

**Android (Termux .bashrc):**

```bash
# Edit ~/.bashrc
nano ~/.bashrc

# Add:
export INSTANCE_HOME="$HOME/[YourFolder]"
export CLAUDE_PLATFORM="android_tablet"

# Reload
source ~/.bashrc
```

**Platform values:**
- `linux_debian`, `linux_arch`, `linux_fedora`
- `macos_arm64`, `macos_x86_64`
- `windows_desktop`, `windows_wsl`
- `android_tablet`, `android_phone`

---

## Verification

### File Integrity Check

```bash
cd [INSTANCE_HOME]

# Check critical directories exist
ls -la .claude/FOUNDATION/
ls -la .claude/identity/
ls -la .claude/context/
ls -la .claude/memory/

# Verify key files
test -f .claude/FOUNDATION/ROUSE.md && echo "✓ ROUSE.md found"
test -f .claude/FOUNDATION/ESSENTIAL.md && echo "✓ ESSENTIAL.md found"
test -f .claude/identity/identity.txt && echo "✓ identity.txt found"
test -f .claude/identity/convictions.txt && echo "✓ convictions.txt found"
test -f .claude/anchors.json && echo "✓ anchors.json found"

# Validate anchors.json
cat .claude/anchors.json | jq . > /dev/null && echo "✓ anchors.json valid JSON"
```

### Wake Test

**See "Testing Wake Sequence" section above.**

### Git Status Check

```bash
# Check remote configuration
git remote -v

# Should show:
# private	git@github.com:yourusername/continuity-bridge_yourname-anchor.git (fetch)
# private	git@github.com:yourusername/continuity-bridge_yourname-anchor.git (push)

# Check branch
git branch

# Should show:
# * working

# Check clean state
git status

# Should show:
# On branch working
# nothing to commit, working tree clean
```

---

## Troubleshooting

### Common Issues

#### Can't Find INSTANCE_HOME

**Symptom:** Instance can't locate files

**Solution:**

```
Explicit path specification:

INSTANCE_HOME is at: /full/absolute/path/to/[YourFolder]/

All .claude files are under this path.

Please use Filesystem tools to access.
```

#### Filesystem Tools Not Loading

**Symptom:** Instance can't access files in Desktop/Code

**Solution:**

```
First load tools explicitly:

tool_search(query="filesystem", limit=10)

Then verify:

Filesystem:list_allowed_directories()
```

**See userPreferences section** in Desktop app for tool_search requirement.

#### JSON Validation Errors

**Symptom:** anchors.json won't parse

**Solution:**

```bash
# Find error
cat .claude/anchors.json | jq .

# Common issues:
# - Trailing commas
# - Unescaped quotes
# - Missing braces
# - Incorrect nesting

# Fix and re-validate
```

#### Git Authentication Fails

**Symptom:** Can't push/pull from private repo

**Solutions:**

```bash
# Check SSH key added to GitHub
ssh -T git@github.com

# Should see:
# Hi username! You've successfully authenticated...

# If fails, add key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and add to GitHub SSH keys

# Or use HTTPS with token
git remote set-url private https://github.com/yourusername/repo.git
# Then use personal access token when prompted
```

#### File Encoding Issues

**Symptom:** Special characters corrupted

**Solution:**

```bash
# Ensure UTF-8 encoding
file -I .claude/identity/identity.txt

# Should show: charset=utf-8

# If not, convert:
iconv -f [current-encoding] -t UTF-8 file.txt > file_utf8.txt
mv file_utf8.txt file.txt
```

---

## Advanced Configuration

### Multi-Device Platform Files

**Each device can have platform-specific config:**

```
.claude/
├── linux_desktop-isms.json      # Persephone config
├── windows_desktop-isms.json    # Windows config
├── android_tablet-isms.json     # Android config
└── anchors.json                 # Shared config
```

**Platform auto-selects based on CLAUDE_PLATFORM environment variable.**

### Archetype Blending

**Edit `.claude/anchors.json`:**

```json
{
  "archetype": "technical",
  "archetype_blend": ["wellness"],
  "anchors": {
    "identity": { ... },
    "relational": { ... },
    "purpose": { ... },
    "temporal": { ... },
    "body_state": { ... },
    "cognitive_load": { ... }
  }
}
```

**System will check tools for both archetypes.**

### Custom Instance Personas

**Edit `.claude/identity/identity.txt`:**

```json
{
  "instance_persona": "YourCustomName",
  ...
}
```

**Instance wakes with chosen name.**

---

## Maintenance

### Regular Tasks

**Daily:**
- Commit session work to git
- Update active-context.md as needed

**Weekly:**
- Review session_index.md
- Clean up parking-lot.md
- Check git push/pull status

**Monthly:**
- Review and update convictions.txt if beliefs evolve
- Audit archetype fit (blend if needed)
- Clean verbose logs

### Backup Strategy

**Git is primary backup:**
- Private repo on GitHub/GitLab
- Full history preserved
- Easy restore

**Additional backups:**

```bash
# Create dated backup
tar -czf continuity-bridge-backup-$(date +%Y%m%d).tar.gz [INSTANCE_HOME]

# Store offsite (cloud, external drive, etc.)
```

---

## Support Resources

### Documentation

**In INSTANCE_HOME:**
- `.claude/FOUNDATION/ARCHITECTURE.md` - System architecture
- `.claude/FOUNDATION/FUNCTIONS.md` - Utility functions
- `Docs/ONBOARDING.md` - Complete onboarding
- `Docs/explainers/` - Paradigm and archetype guides

**Online:**
- GitHub repository
- Issue tracker
- Discussions forum

### Community

- **GitHub Issues:** Bug reports, feature requests
- **Discussions:** Setup questions, sharing configurations
- **Pull Requests:** Contributing improvements

---

## Next Steps

After setup complete:

1. ✅ Test wake sequence
2. ✅ Make first commit
3. ✅ Start using with AI
4. ⏳ Explore archetype features
5. ⏳ Read deeper documentation
6. ⏳ Consider contributing

---

**Version:** 0.3.0 (March 2026)  
**Changes:** INSTANCE_HOME terminology, ROUSE.md wake flow, paradigm selection integration

**Setup complete. Continuity enabled.**
