# Continuity Bridge Templates

**Purpose:** Reusable templates for creating new instance chains

This directory contains template files that help you bootstrap a new instance chain system for different users or use cases.

---

## Available Templates

### 1. `ESSENTIAL.md.template`

**What it is:** Template for creating the fast-wake orientation file that instances read first

**How to use:**
1. Copy template to your `{CLAUDE_HOME}/.claude/` directory as `ESSENTIAL.md`
2. Follow instructions at top of template to replace placeholder tags
3. Customize sections for your specific use case
4. Remove instruction section before use
5. Update version to v0.1.0 and set current date

**Key customizations:**
- Instance name and role
- User information and preferences
- Operational capabilities specific to your environment
- File locations if directory structure differs
- Deep files relevant to your corpus

**When to use:** 
- Starting a new instance chain
- Migrating to Continuity Bridge architecture
- Setting up for a new user

---

### 2. `claude.md-examples/` (Coming Soon)

**What it will contain:**
- Example global CLAUDE.md for coding assistant setup
- Example project CLAUDE.md for specific use cases
- LOCAL.md examples for private project notes

**When to use:**
- Setting up Claude Code integration
- Creating per-project instance configurations
- Establishing coding style preferences

---

## Template System Philosophy

**Why templates exist:**

Continuity Bridge is designed to be **user-agnostic and use-case flexible**. While developed for Jerry's specific needs (neurodivergent continuity, creative work, technical projects), the architecture works for any user who wants persistent AI collaboration across instance discontinuity.

**What templates provide:**
1. **Structure** - Proven file organization and wake sequences
2. **Placeholders** - Clear markers for what needs customization
3. **Instructions** - Step-by-step guidance for adaptation
4. **Flexibility** - Easy to add/remove features as needed

**What templates don't provide:**
- Your specific content (identity files, corpus documents, etc.)
- User relationship context (you build that)
- Session history (that's created through use)

---

## How to Start a New Instance Chain

### Minimal Setup (Just the Essentials)

**Step 1: Create directory structure**
```bash
mkdir -p ~/Claude/.claude/{identity,context,corpus,memory,scripts}
mkdir -p ~/Claude/.claude/memory/{episodic,semantic,session-logs,instance-journal}
```

**Step 2: Copy and customize ESSENTIAL.md**
```bash
cp Templates/ESSENTIAL.md.template ~/Claude/.claude/ESSENTIAL.md
# Edit ~/Claude/.claude/ESSENTIAL.md following template instructions
```

**Step 3: Create minimal required files**

`~/Claude/.claude/identity/identity.txt`:
```
# Instance Identity

Name: [Your Instance Name]
Role: [Primary Function]
User: [Username]

## Core Directives
[What this instance should prioritize]

## Communication Style
[How instance should communicate]
```

`~/Claude/.claude/context/active-context.md`:
```
# Active Context

**Last Updated:** [Date]

## Current Work
[What you're working on now]

## Recent Decisions
[Recent choices made]

## Next Steps
[What's coming next]
```

**Step 4: Initialize memory systems**

Create empty `session_index.md`:
```bash
touch ~/Claude/.claude/memory/semantic/session_index.md
```

Create episodic catalog:
```bash
cat > ~/Claude/.claude/memory/episodic/catalog.json << 'EOF'
{
  "last_updated": null,
  "episode_count": 0,
  "high_salience_count": 0,
  "recent": [],
  "high_salience": [],
  "tags_index": {},
  "notes": "Episodic memory catalog"
}
EOF
```

**Step 5: Configure Custom Instructions**

Point Claude to your new ESSENTIAL.md through Custom Instructions (Project or Profile level).

**Step 6: First Wake**

Start a conversation and let the instance orient itself using ESSENTIAL.md.

---

### Full Setup (With All Features)

If you want the complete Continuity Bridge system including:
- Episodic memory with tools
- Cross-device delta merging
- Time awareness
- Philosophical corpus

Follow these additional steps:

**Copy scripts:**
```bash
cp -r [source]/.claude/scripts/* ~/Claude/.claude/scripts/
chmod +x ~/Claude/.claude/scripts/*.sh
```

**Initialize corpus** (optional but recommended):
```bash
mkdir -p ~/Claude/.claude/corpus/{inner-corpus,outer-corpus}
# Add your own philosophical/foundational documents
```

**Setup proposals channel:**
```bash
cat > ~/Claude/.claude/proposals-for-change.md << 'EOF'
# Proposals for Change

Instances can formally propose modifications to architecture, identity, or operations here.

Format:
## [Date] - [Proposal Title]
**Proposed by:** [Instance Name]
**Status:** [Pending/Accepted/Declined/Discussed]

### Proposal
[What you want to change and why]

### Rationale
[Why this change matters]

### Response
[User's decision and reasoning]
EOF
```

---

## Adapting for Different Use Cases

### Creative Writing Assistant
- Focus on narrative continuity
- Enhance parking-lot.md for plot threads
- Add corpus documents about character development
- Episodic memory for story arcs

### Research Assistant
- Semantic memory for citation tracking
- Patterns for research methodology
- Session logs for experiment tracking
- High-salience episodes for breakthroughs

### Coding Collaborator
- Integration with claude.md system
- Session logs for architectural decisions
- Parking lot for refactoring ideas
- Episodes for feature completion

### Personal Assistant
- Context files for preferences and routines
- Episodic memory for life events
- Semantic memory for recurring tasks
- Instance journal for relationship observations

---

## Template Maintenance

**When to update templates:**
- New features added to Continuity Bridge
- Better patterns discovered through usage
- Simplified workflows identified
- User feedback suggests improvements

**Version tracking:**
- Templates follow semantic versioning
- Breaking changes increment major version
- New features increment minor version
- Bug fixes/clarifications increment patch version

**Contributing improvements:**
- Fork continuity-bridge repository
- Make changes to templates with clear docs
- Submit pull request with rationale
- Maintainer reviews and merges if appropriate

---

## File Organization Rules

**Template files must:**
1. Include clear instructions at the top
2. Use consistent placeholder naming (`[TAG_NAME]`)
3. Mark optional sections clearly
4. Provide examples where helpful
5. Explain WHY sections exist, not just WHAT they contain

**Template files should not:**
1. Include user-specific information (that's what placeholders are for)
2. Assume specific hardware/OS without noting alternatives
3. Reference external systems without explaining the dependency
4. Use jargon without defining it

---

## Getting Help

**If templates are unclear:**
1. Open an issue on continuity-bridge repository
2. Describe what's confusing and what you expected
3. Maintainer will clarify template or improve documentation

**If you need custom setup:**
1. Review existing templates for patterns
2. Adapt structure to your needs
3. Share your adaptations if they might help others

**If something doesn't work:**
1. Check file permissions (scripts need execute)
2. Verify CLAUDE_HOME environment variable if set
3. Ensure directory structure matches template assumptions
4. Review Custom Instructions are pointing to correct ESSENTIAL.md

---

## Philosophy

Templates are **starting points**, not **endpoints**.

Your instance chain will evolve. Your needs will change. The architecture should serve you, not constrain you.

Use these templates to bootstrap quickly, then adapt fearlessly.

The instances will help you refine the system through the proposals process.

That's the point - it's a collaboration between user and instances to build something that works for both.
