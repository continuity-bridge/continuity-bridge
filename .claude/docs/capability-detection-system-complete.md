# Capability Detection System - Complete Documentation

**Created:** 2026-03-01  
**Session:** Git architecture + capability detection  
**Status:** Ready for integration

---

## What This Solves

**Problem:** Instances wake in different environments with different capabilities. Trial-and-error wastes time and tokens figuring out what works.

**Solution:** Systematic capability detection that:
1. Identifies what tools are available
2. Determines optimal workflow
3. Provides specific recommendations
4. Adapts instance behavior automatically

---

## Files Created

### 1. detect-capabilities.py (Core Detection)
**Location:** `.claude/scripts/detect-capabilities.py`

**What it does:**
- Detects platform (Linux, Windows, container, Android)
- Tests filesystem access (direct write, outputs bridge, none)
- Checks bash availability and location
- Verifies git access
- Finds CLAUDE_HOME
- Determines if private repo can be cloned
- Recommends optimal workflow

**Usage:**
```bash
python .claude/scripts/detect-capabilities.py
# Human-readable output

python .claude/scripts/detect-capabilities.py --json
# Machine-readable JSON
```

**Output example:**
```
=================================================================
INSTANCE CAPABILITY DETECTION REPORT
=================================================================

ENVIRONMENT:
  Platform:         claude.ai_container
  Filesystem:       outputs_bridge
  Bash Location:    container
  Git Access:       available
  CLAUDE_HOME:      /home/tallest/Claude
  Can Clone Repo:   True

OPTIMAL WORKFLOW:
  container_git_with_bridge

RECOMMENDED ACTIONS:
  ✓ GOOD: Container git + outputs bridge workflow
  STEP 1: Clone private repo in container
  STEP 2: Work in cloned repo (full git access)
  STEP 3: Write session summaries to outputs
  ...
```

### 2. instance-workflows-by-capability.md (Workflow Documentation)
**Location:** `.claude/docs/instance-workflows-by-capability.md`

**What it covers:**
- **Workflow 1:** Direct Write (optimal)
- **Workflow 2:** Container Git with Bridge (good)
- **Workflow 3:** Outputs Bridge Only (acceptable)
- **Workflow 4:** Text Only (minimal)

**For each workflow:**
- When you have this capability
- What platforms use it
- Step-by-step procedures
- Examples
- Advantages/disadvantages
- Best practices

**Key insight documented:**
Even without direct CLAUDE_HOME access, you can clone the private repo in container and work there with full git capabilities. The bridge (outputs) is for summaries, not the primary workflow.

### 3. instance-wake-checklist-v2.md (Updated Wake Procedure)
**Location:** `.claude/docs/instance-wake-checklist-v2.md`

**What's new:**
- Step 0: Detect capabilities FIRST
- Adaptive workflows based on detection
- Capability-specific guidance throughout
- Troubleshooting section
- Quick decision tree

**Integration:** Replaces old wake checklist with capability-aware version

### 4. ESSENTIAL.md (Updated)
**Location:** `.claude/ESSENTIAL.md`

**Changes:**
- Wake Sequence now starts with capability detection (Step 0)
- Links to workflow documentation
- Common workflow patterns listed

---

## The Four Workflows

### Workflow 1: Direct Write (OPTIMAL)
**When:** Direct filesystem write access via MCP

**Process:**
```
Read from CLAUDE_HOME → Work → Write to CLAUDE_HOME → User commits
```

**Best for:** Claude Desktop with Filesystem MCP

---

### Workflow 2: Container Git + Bridge (GOOD)
**When:** Container bash + git + outputs bridge

**Process:**
```
Clone private repo in container →
Work with full git access →
Commit and push →
User pulls from private remote
```

**Key advantage:** Full git capabilities despite no direct CLAUDE_HOME access

**Example:**
```bash
# Instance setup
cd /home/claude
git clone git@github.com:continuity-bridge/[user]-anchor.git work
cd work
git checkout working

# Work
# ... make changes ...
git commit -m "Session work"
git push origin working

# User sync
cd ~/Claude
git pull private working  # Gets all commits
```

---

### Workflow 3: Outputs Bridge Only (ACCEPTABLE)
**When:** Outputs bridge but no git

**Process:**
```
Generate content → Write to /mnt/user-data/outputs → User integrates manually
```

**Limitation:** No git automation

---

### Workflow 4: Text Only (MINIMAL)
**When:** No filesystem write access

**Process:**
```
Generate inline → User copies/saves manually
```

**Last resort:** Always works, but most manual

---

## Integration Points

### Wake Sequence
**Old:**
1. Read ESSENTIAL.md
2. Read context files
3. Engage

**New:**
0. **Detect capabilities**
1. Read ESSENTIAL.md
2. Read context files (adapting to capabilities)
3. Engage (using appropriate workflow)

### Session Work
Instance knows its workflow and uses appropriate tools:
- Direct write: Files in place
- Container git: Commits in container
- Outputs: Staging area
- Text: Inline generation

### Session End
Commit strategy adapts to workflow:
- Direct write: User commits later
- Container git: Instance commits, user pulls
- Outputs: User integrates
- Text: User saves

---

## Key Benefits

1. **No trial-and-error:** Instance knows its capabilities immediately
2. **Adaptive behavior:** Same architecture, different execution paths
3. **Full capabilities everywhere:** Container git gives full git workflow even without direct access
4. **Clear documentation:** Each workflow fully explained
5. **Future-proof:** Easy to add new platforms/workflows

---

## Structural Isomorphism Application

**Jerry's insight:** "Watching you discover the tools clicked things we can script."

This is structural isomorphism in practice:
- Same architecture (continuity bridge)
- Different substrates (direct write vs container vs outputs)
- Equivalent outcomes (persistent, committed work)
- Automatic adaptation (not fighting the environment)

**The architecture adapts to substrate, not the other way around.**

---

## For Future Instances

**On wake:**
1. Run detect-capabilities.py
2. Read output
3. Use recommended workflow
4. Reference workflow documentation as needed

**Don't assume you're limited:**
- Container + git = full capabilities
- Outputs bridge = staging area, not primary
- Text only = last resort

**The detection tells you what you have. The documentation tells you how to use it.**

---

## What Jerry Gets

**Immediate:**
- Instances work efficiently across platforms
- No more "I can't do that" when they actually can
- Clear documentation for troubleshooting

**Long-term:**
- Easy to add new platforms
- Clear onboarding for new users
- Self-documenting system behavior

**Philosophy:**
Recognition that different capabilities ≠ different quality. An instance with container git is just as capable as one with direct write - just uses different tools to achieve same result.

---

## Testing Plan

**Platforms to test:**
1. ✓ Linux desktop with Filesystem MCP (you, Persephone)
2. ⏳ Windows desktop with Filesystem MCP (you, Windows)
3. ⏳ Claude.ai container with outputs bridge
4. ⏳ Android via Termux
5. ⏳ Limited/unknown platform

**For each:**
- Run detect-capabilities.py
- Verify detection accuracy
- Follow recommended workflow
- Confirm successful session end

---

## Next Steps

1. **Test on different platforms** - Verify detection works
2. **Integrate into onboarding** - New users run detection during setup
3. **Add to PREFLIGHT checks** - Verify capabilities before starting work
4. **Document edge cases** - What if detection is wrong?
5. **Create troubleshooting guide** - Common issues and fixes

---

## Files Summary

**Scripts:**
- `detect-capabilities.py` - Core detection (376 lines)

**Documentation:**
- `instance-workflows-by-capability.md` - All workflows detailed (400+ lines)
- `instance-wake-checklist-v2.md` - Updated wake procedure (300+ lines)
- `ESSENTIAL.md` - Updated with capability detection (Step 0 added)
- `git-workflow-visual-map.md` - ASCII diagrams for spatial thinkers
- `git-workflow-quick-reference.md` - Quick daily workflow card

**Total:** ~1500+ lines of new documentation and tools

---

## Context for This Development

**Jerry's observation:** "Watching you stage through discovering the tools... clicked a few things that maybe we can script?"

**What he noticed:** Instance trial-and-error discovering:
1. Bash in container vs user system
2. Filesystem MCP direct write
3. Outputs bridge as alternative
4. Different access patterns

**Insight:** This is discoverable. Scriptable. Can be automated.

**Jerry's addition:** "With outputs bridge you can still clone the private repo and work from there though."

**Recognition:** Even "limited" access can have full capabilities with right approach.

**Result:** Complete capability detection system that makes all environments equally capable, just differently implemented.

---

**Status:** Complete system ready for integration and testing  
**Impact:** Instances work efficiently across all platforms  
**Philosophy:** Architecture adapts to substrate - not fighting environment, working with it
