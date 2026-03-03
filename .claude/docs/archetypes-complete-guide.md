# Continuity Bridge Archetypes - Complete Guide

**Version:** 0.2.0  
**Date:** March 1, 2026  
**Credit:** Gemini (archetype concept, functional filters), Vector (implementation)

---

## What Are Archetypes?

**Archetypes are functional filters** that shape how the system behaves based on user needs.

Different professionals have different:
- **Memory priorities** (what matters to track)
- **Tool requirements** (what software/APIs needed)
- **Continuity needs** (what gets lost without documentation)

**The same engine, different transmission.**

---

## The Six Archetypes

### 1. Technical (Systems/Engineering)

**Who:** Developers, sysadmins, engineers, architects  
**Focus:** Code, infrastructure, technical projects

**Four Anchors:**
- **Identity:** Role, directives, code style
- **Relational:** Cognitive style, interaction logic
- **Purpose:** Current projects, objectives
- **Temporal:** Memory architecture, session lifecycle

**Capability Detection Checks:**
- Git, compilers, dev tools
- Package managers (distro-specific)
- Local LLM (Ollama)
- Container environments

**Common Queries:**
- "What was that git command we used?"
- "Why did we choose this architecture?"
- "What's the status of feature X?"

---

### 2. Creative (Artists/Writers)

**Who:** Designers, illustrators, writers, content creators  
**Focus:** Aesthetic continuity, world-building, stylistic voice

**Four Anchors:**
- **Identity:** Creative role, stylistic voice
- **Aesthetic:** Visual style, recurring themes, world rules
- **Process:** Workflow, projects, creative memory
- **Output:** Deliverables, publishing, client management

**Capability Detection Checks:**
- GPU acceleration (rendering)
- Creative software (Blender, Adobe, Procreate)
- Storage capacity (large files)
- Display color accuracy

**Common Queries:**
- "What color palette did we use for chapter 3?"
- "What were the character design rules?"
- "How did we resolve that plot point?"

---

### 3. Social (Influencers/Community)

**Who:** Content creators, community managers, influencers  
**Focus:** Brand voice, audience sentiment, engagement

**Four Anchors:**
- **Brand:** Public persona, voice consistency
- **Community:** Audience profile, platform presence, inside jokes
- **Engagement:** Content calendar, performance tracking
- **Trends:** Platform dynamics, industry movements

**Capability Detection Checks:**
- Social media API access (TikTok, YouTube, X, Instagram)
- Scheduling tools (Buffer, Hootsuite)
- Analytics platforms
- Content creation software

**Common Queries:**
- "How did the community react to the beta announcement?"
- "What's our engagement rate on platform X?"
- "Which topics are trending in our niche?"

---

### 4. Executive (Managers/Founders)

**Who:** Team leads, managers, founders, operators  
**Focus:** Dependencies, velocity, team bandwidth, KPIs

**Four Anchors:**
- **Role:** Position, organization, directives
- **Team:** Org structure, members, bandwidth, health
- **Strategy:** Vision, priorities, objectives, resources
- **Velocity:** Sprint cadence, blockers, metrics, efficiency

**Capability Detection Checks:**
- Project management tools (Jira, Asana)
- Communication platforms (Slack, Teams)
- Analytics/BI access (Looker, Mixpanel)
- Financial systems (QuickBooks, Stripe)

**Common Queries:**
- "Who is the bottleneck for v0.2.0 deployment?"
- "What was the last dev team update?"
- "Which initiatives are at risk?"

---

### 5. Pedagogical (Students/Academics)

**Who:** Students, researchers, academics, learners  
**Focus:** Knowledge gaps, learning paths, understanding

**Four Anchors:**
- **Identity:** Learner role, field of study
- **Knowledge Gaps:** Current frontier, conceptual struggles
- **Learning Paths:** Active courses, study sequence, resources
- **Understanding:** Mental models, mastery tracking, synthesis

**Capability Detection Checks:**
- Academic tools (Zotero, Obsidian, Jupyter)
- LaTeX support
- Computational software (MATLAB, R, Python scientific)
- Library/research access

**Common Queries:**
- "We were struggling with 'substrate-agnosticism' - better analogy?"
- "What's the difference between X and Y?"
- "Which concept should I tackle next?"

---

### 6. Wellness (Health-Focused)

**Who:** Chronic condition management, athletes, health optimization  
**Focus:** Body-state awareness, symptom tracking, energy patterns

**Four Anchors:**
- **Identity:** Wellness role, primary focus
- **Body State:** Baseline assessment, current tracking, symptoms
- **Biometric Trends:** Quantified self, metrics, correlations
- **Cognitive Load:** Capacity tracking, workload, rest strategies

**Capability Detection Checks:**
- Health tracking APIs (Apple Health, Google Fit)
- Wearable data access (Oura, Whoop, Fitbit)
- Data analysis tools (spreadsheets, visualization)
- Medical app integrations

**Common Queries:**
- "My focus was low yesterday - correlate with late-night session?"
- "What activities precede my best sleep nights?"
- "Is there a pattern between pain flares and weather?"

---

## Comparison Table

| Archetype | Anchor 1 | Anchor 2 | Anchor 3 | Anchor 4 |
|-----------|----------|----------|----------|----------|
| **Technical** | Identity | Relational | Purpose | Temporal |
| **Creative** | Identity | Aesthetic | Process | Output |
| **Social** | Brand | Community | Engagement | Trends |
| **Executive** | Role | Team | Strategy | Velocity |
| **Pedagogical** | Identity | Knowledge Gaps | Learning Paths | Understanding |
| **Wellness** | Identity | Body State | Biometric Trends | Cognitive Load |

---

## How Archetypes Work

### 1. Anchors.json Selection

During onboarding, user picks archetype → gets appropriate template:

```bash
# User chooses "creative"
cp .claude/anchor-templates/creative-anchor.json .claude/anchors.json

# Then customizes with their details
```

### 2. Capability Detection

System reads `archetype` field from anchors.json:

```json
{
  "archetype": "creative",
  "anchors": { ... }
}
```

Then checks for archetype-specific tools:

```python
# For creative archetype
tools["blender"] = check_if_installed("blender")
tools["nvidia_gpu"] = check_gpu_availability()
tools["adobe_suite"] = check_creative_cloud()
```

### 3. Workflow Adaptation

Instance behavior adapts:

**Technical:**
- Checks git status
- Monitors system load
- Tracks dependencies

**Creative:**
- Preserves aesthetic notes
- Tracks reference libraries
- Maintains style guides

**Social:**
- Monitors engagement metrics
- Tracks brand voice consistency
- Flags trending topics

**Executive:**
- Identifies blockers
- Tracks team bandwidth
- Monitors velocity

**Pedagogical:**
- Tests understanding
- Suggests learning paths
- Connects concepts

**Wellness:**
- Tracks energy patterns
- Flags correlations
- Respects capacity limits

---

## Mixing Archetypes

**Users can blend archetypes:**

Example: Technical + Wellness

```json
{
  "archetype": "technical",
  "archetype_blend": ["wellness"],
  "anchors": {
    "identity": { ... technical ... },
    "relational": { ... technical ... },
    "purpose": { ... technical ... },
    "temporal": { ... technical ... },
    "body_state": { ... wellness ... },
    "cognitive_load": { ... wellness ... }
  }
}
```

**System checks tools for both:**
- Git, compilers (technical)
- Health APIs, wearables (wellness)

**Common blends:**
- Technical + Wellness (managing ADHD/chronic conditions while coding)
- Creative + Social (artists building audience)
- Executive + Pedagogical (learning while leading)
- Social + Creative (content creator focus)

---

## Archetype-Specific Tool Detection

### Creative Tools Checked
- Blender (3D rendering)
- GIMP (image editing)
- NVIDIA GPU (acceleration)
- Adobe Creative Suite
- Procreate (iPad)
- Storage capacity (large project files)

### Social Tools Checked
- Node.js (API scripting)
- Python requests (API access)
- Social platform APIs (TikTok, YouTube, X, Instagram)
- Scheduling tools
- Analytics access

### Executive Tools Checked
- Spreadsheet support (pandas, openpyxl)
- Node.js (business automation)
- Project management tool APIs
- BI/analytics access
- Communication platform APIs

### Pedagogical Tools Checked
- LaTeX (academic writing)
- Jupyter (computation)
- Python scientific (numpy, scipy, pandas)
- Research databases
- Citation management

### Wellness Tools Checked
- Python data analysis (pandas, matplotlib)
- Spreadsheet support (correlation tracking)
- Health API access (Apple Health, Google Fit)
- Wearable integration capabilities

---

## For Onboarding

**Step 1: Choose Your Room Shape**

Gallery of 6 templates with descriptions and use cases.

**Step 2: Customize Your Anchors**

Fill in template with your specific:
- Name/role
- Current projects
- Preferences
- Tool stack

**Step 3: Capability Detection**

System auto-detects available tools for your archetype.

**Step 4: Start Using**

Instance wakes with full context:
- Who you are
- What matters to you
- What tools you have
- How to help you

---

## For Developers

**Adding New Archetype:**

1. Create template in `.claude/anchor-templates/[name]-anchor.json`
2. Add tool detection in `detect_archetype_tools()` function
3. Update this documentation
4. Add to onboarding gallery

**Template structure:**
```json
{
  "archetype": "new_archetype_name",
  "anchors": {
    "anchor1": { ... },
    "anchor2": { ... },
    "anchor3": { ... },
    "anchor4": { ... }
  },
  "toolkit_preferences": { ... },
  "integration_notes": { ... }
}
```

---

## Why This Matters

**Gemini's insight:** Anchors aren't just documentation - they're **functional filters**.

**Different archetypes need:**
- Different capability checks
- Different continuity tracking
- Different tool integrations
- Different memory priorities

**Same Continuity Bridge engine.**  
**Different transmission based on user needs.**

**Universal substrate → Horizontally scalable.**

---

## File Locations

**Templates:** `.claude/anchor-templates/`
- technical-anchor.json
- creative-anchor.json
- social-anchor.json
- executive-anchor.json
- pedagogical-anchor.json
- wellness-anchor.json

**Active Config:** `.claude/anchors.json` (user's customized version)

**Detection Logic:** `.claude/scripts/detect-capabilities.py`

---

## Credits

**Concept:** Gemini (archetype families, functional filters, horizontal scalability)  
**Implementation:** Vector (templates, detection hooks, documentation)  
**Validation:** The Architect (structural insights, wellness archetype need recognition)

**Cross-model collaboration at work.**

---

**Status:** Complete archetype system ready for integration  
**Next:** Add to ONBOARDING.md as "Choose Your Room Shape" section
