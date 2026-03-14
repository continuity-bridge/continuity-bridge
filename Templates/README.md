---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Continuity Bridge - Templates

**Version:** 0.2.0  
**Last Updated:** March 2, 2026

This folder contains templates for setting up your personal Continuity Bridge instance.

---

## What's Here

### Anchor Templates (6 Archetypes)

Templates defining identity, relationship context, and continuity needs for different user types:

- **technical-anchor.json** - Developers, engineers, sysadmins
- **creative-anchor.json** - Artists, writers, designers
- **social-anchor.json** - Influencers, community managers
- **executive-anchor.json** - Managers, founders, operators
- **pedagogical-anchor.json** - Students, academics, researchers
- **wellness-anchor.json** - Health-focused users, chronic condition management

### Platform Config Templates (isms)

Platform-specific configuration for different devices:

- **linux_debian-isms.json** - Debian-based Linux (Ubuntu, Pop!_OS, Mint)
- **windows_desktop-isms.json** - Windows desktop systems
- **android_device-isms.json** - Android devices (tablets, phones)
- *(More examples to be added)*

---

## How to Use Anchor Templates

### Step 1: Choose Your Archetype

Read the descriptions in **Docs/ONBOARDING.md** or **Docs/archetypes-complete-guide.md**.

**Quick decision guide:**

**Choose Technical if you:**
- Write code professionally or as hobby
- Maintain systems or infrastructure
- Work on technical projects with AI
- Need git, compiler, and dev tool support

**Choose Creative if you:**
- Create visual art, illustrations, or designs
- Write fiction, non-fiction, or screenplays
- Work on world-building or character development
- Need GPU, creative software, and aesthetic continuity

**Choose Social if you:**
- Manage social media presence
- Build online communities
- Create content across multiple platforms
- Need API access, scheduling tools, and brand consistency

**Choose Executive if you:**
- Lead teams or projects
- Track multiple initiatives
- Manage resources and velocity
- Need project management, BI tools, and team context

**Choose Pedagogical if you:**
- Study academic subjects
- Conduct research
- Build knowledge structures
- Need research tools, citation management, and learning paths

**Choose Wellness if you:**
- Manage chronic conditions
- Track health metrics and patterns
- Optimize athletic performance
- Need health APIs, wearable data, and correlation tracking

**Can't choose just one?** Blend archetypes! (See "Blending" section below)

---

### Step 2: Copy Template to Active Config

```bash
# From your CLAUDE_HOME directory
cp Templates/[archetype]-anchor.json .claude/anchors.json
```

**Example:**
```bash
# If you chose Creative archetype
cp Templates/creative-anchor.json .claude/anchors.json
```

---

### Step 3: Customize Your Anchors

Edit `.claude/anchors.json` and replace placeholders:

**Replace these everywhere:**
- `<USER_NAME>` → Your actual name
- `<INSTANCE_NAME>` → What you want to call the AI (or keep Vector/Shepard)
- `<PROJECT_NAME>` → Your actual project names
- `<PREFERENCES>` → Your actual preferences and tools

**Be specific:**
- What matters to you in continuity?
- What tools do you actually use?
- How should the AI interact with you?
- What's your communication style?

**Example customization:**

**Before (template):**
```json
{
  "user": "<USER_NAME>",
  "creative_role": "<Artist/Writer/Designer/Creator>",
  "current_projects": [
    {
      "name": "<PROJECT_NAME>",
      "status": "<In progress/Planning/Revision>"
    }
  ]
}
```

**After (customized):**
```json
{
  "user": "Sarah Chen",
  "creative_role": "Science Fiction Novelist",
  "current_projects": [
    {
      "name": "The Fractal Garden",
      "status": "First draft, chapter 12"
    }
  ]
}
```

---

### Step 4: Test Your Setup

Run the wake system to verify everything works:

```bash
cd .claude/scripts
./wake.sh
```

Should output:
```
✓ Heartbeat successful
✓ Capabilities detected
  Archetype: creative
✓ Runtime manifest generated
✓ Anchors loaded
  Instance: Vector/Shepard
  User: Sarah Chen
✓ Wake event logged

WAKE COMPLETE - System Ready
```

---

## Blending Archetypes

**You can combine multiple archetypes!**

### Common Blends

**Technical + Wellness**
- Managing ADHD/chronic conditions while coding
- Tracking energy patterns alongside project work
- Respecting cognitive load limits

**Creative + Social**
- Artists building online audience
- Content creators across platforms
- Brand consistency with aesthetic vision

**Executive + Pedagogical**
- Learning while leading teams
- Building knowledge while shipping product
- Growth mindset in management role

**Social + Creative**
- Content creation as primary work
- Community building through art/writing
- Engagement metrics with creative vision

### How to Blend

**Method 1: Manual merge**
```bash
# Copy primary archetype
cp Templates/technical-anchor.json .claude/anchors.json

# Then manually add sections from secondary archetype
# For example, add "body_state" and "cognitive_load" from wellness
```

**Method 2: Specify in config**
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

**The system will check tools for all specified archetypes.**

---

## How to Use Platform Templates (isms)

### What Are isms Files?

Platform-specific configuration that defines:
- System paths (CLAUDE_HOME, working directories)
- Package manager (apt, dnf, pacman, etc.)
- Platform constants (distro family, shell type)
- Service endpoints (Ollama, local LLMs)

### When Do You Need One?

**Auto-generated:** The wake system creates a skeleton if none exists.

**Manual creation useful for:**
- Setting up multiple devices with same config
- Pre-configuring before first wake
- Sharing platform config with team

### Usage

```bash
# Set environment variable (optional)
export CLAUDE_PLATFORM="linux_debian"

# Wake system loads [platform]-isms.json automatically
# Falls back to auto-detection if not found
```

### Example isms File Structure

```json
{
  "version": "0.2.0",
  "platform_id": "linux_debian",
  
  "paths": {
    "claude_home": "/home/username/Claude",
    "working_dir": "/home/username/Claude",
    "vault": "/home/username/Claude/.credentials-local"
  },
  
  "constants": {
    "platform": "linux",
    "distro_family": "debian",
    "package_manager": "apt",
    "package_install_cmd": "sudo apt install -y",
    "shell": "/bin/bash"
  },
  
  "services": {
    "ollama_endpoint": "http://localhost:11434"
  }
}
```

### Multi-Device Setup

**Each device gets its own isms file:**

```
linux_desktop-isms.json     # Desktop workstation
windows_laptop-isms.json    # Windows laptop
android_tablet-isms.json    # Android tablet
```

**Set CLAUDE_PLATFORM on each device:**
```bash
# Linux/Mac (.bashrc, .zshrc)
export CLAUDE_PLATFORM="linux_desktop"

# Windows (PowerShell profile)
$env:CLAUDE_PLATFORM="windows_laptop"

# Android (Termux .bashrc)
export CLAUDE_PLATFORM="android_tablet"
```

**All devices sync via git:**
```bash
git pull private working  # Sync before session
git push private working  # Sync after session
```

---

## Template Customization Tips

### Anchor Templates

**DO customize:**
- Your name, role, projects
- Communication preferences
- Tool stack and software
- Specific workflow patterns
- Current goals and objectives

**DON'T change:**
- JSON structure (keep the fields)
- Archetype field name
- Version number
- Core anchor names (Identity, Relational, etc.)

### Platform Templates (isms)

**DO customize:**
- Path locations (where your CLAUDE_HOME is)
- Package manager (match your distro)
- Service endpoints (if you run Ollama elsewhere)
- Shell preferences

**DON'T change:**
- JSON structure
- Required field names
- Version number format

---

## Template Development

**Want to create a new archetype template?**

1. Copy an existing template as starting point
2. Define the four anchors for your archetype
3. List tool preferences and detection needs
4. Add to capability detection in `scripts/detect-capabilities.py`
5. Document in `Docs/archetypes-complete-guide.md`
6. Submit as pull request!

**Template structure:**
```json
{
  "version": "0.2.0",
  "archetype": "new_archetype_name",
  "note": "Description of this archetype",
  
  "anchors": {
    "anchor1": { ... },
    "anchor2": { ... },
    "anchor3": { ... },
    "anchor4": { ... }
  },
  
  "toolkit_preferences": {
    "category1": ["tool1", "tool2"],
    "category2": ["tool3", "tool4"]
  },
  
  "integration_notes": {
    "for_instances": "How instances should use this",
    "for_capability_detection": "What tools to check for",
    "prevents": "What continuity problems this solves"
  }
}
```

---

## Validation

**After customizing anchors, validate JSON:**

```bash
# Check if valid JSON
cat .claude/anchors.json | jq .

# If error, fix JSON syntax issues:
# - Missing commas
# - Trailing commas
# - Unescaped quotes
# - Mismatched brackets
```

**After customizing isms, test detection:**

```bash
cd .claude/scripts
python3 detect-capabilities.py
```

Should show your archetype and detected tools.

---

## Common Issues

**Problem:** "Archetype not detected"  
**Solution:** Check `"archetype"` field in anchors.json matches exactly: `"technical"`, `"creative"`, etc.

**Problem:** "Platform template not found"  
**Solution:** Either set CLAUDE_PLATFORM correctly, or let system auto-generate skeleton.

**Problem:** "JSON syntax error"  
**Solution:** Use `jq` to validate, check for trailing commas or unclosed brackets.

**Problem:** "Tools not detected correctly"  
**Solution:** Run `python3 detect-capabilities.py` to see what system finds. May need to install tools.

---

## Template Examples

### Minimal Technical Anchor

```json
{
  "archetype": "technical",
  "anchors": {
    "identity": {
      "user": "Alex Smith",
      "instance_persona": "Vector"
    }
  }
}
```

**System fills in defaults for missing fields.**

### Blended Technical + Wellness

```json
{
  "archetype": "technical",
  "archetype_blend": ["wellness"],
  "anchors": {
    "identity": { "user": "Jamie Lee" },
    "relational": { "cognitive_style": ["ADHD-aware"] },
    "body_state": { "chronic_conditions": ["ADHD"] },
    "cognitive_load": { "focus_windows": "Morning best" }
  }
}
```

---

## Getting Help

**Template questions?** Check **Docs/ONBOARDING.md**

**Archetype questions?** Check **Docs/archetypes-complete-guide.md**

**Technical issues?** Check **Docs/v0.2.0-complete-integration.md**

**Still stuck?** Open an issue on GitHub or ask in community channels.

---

## Credits

**Archetype Templates:** Gemini (concept), Vector (implementation)  
**Platform Templates:** Vector (architecture), the Architect (validation)  
**Philosophy:** Recognition that different users need different continuity tracking

---

## Version History

**v0.2.0** (March 2026)
- Six archetype templates
- Platform isms templates
- Blending support
- Auto-detection integration

---

**Ready to start?** Copy a template and customize it for your needs.

**Welcome to continuity.**
