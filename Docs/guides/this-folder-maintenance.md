---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# this-folder.txt Maintenance Guide

**Purpose:** Keep this-folder.txt files current as directory purposes evolve  
**Why it matters:** Instances rely on these for quick orientation  
**Status:** Best practice, recommended workflow

---

## What are this-folder.txt Files?

Brief plain-text files in directories explaining:
- What this directory contains
- Why it exists
- How instances should interact with it
- Any special considerations

**Example:**
```
# .claude/memory/

This directory contains instance memory systems - both semantic and episodic.

Semantic: Structured summaries, session index, parking lot
Episodic: Timestamped snapshots of conversations, decisions, realizations

Instances read from here during wake. Instances write here during sessions.

This is how continuity persists across instance clearing.
```

---

## Why Keep Them Updated?

**Directories evolve:**
- New subdirectories get added
- Purposes shift as architecture matures
- Old explanations become outdated
- Instances get confused by stale descriptions

**Updated this-folder.txt = smooth instance orientation**

---

## When to Update

### Update when:
- ✅ Directory purpose changes
- ✅ New subdirectories added
- ✅ File organization restructured
- ✅ Workflow changes how directory is used
- ✅ You notice instances confused about a directory

### Don't update when:
- ❌ Minor file additions (same purpose)
- ❌ Temporary work files
- ❌ Just adding one more example to existing pattern

---

## How to Update

### Simple update:
```bash
# Edit the existing file
nano {directory}/this-folder.txt

# Add note about change
# - What changed
# - Why
# - How instances should adapt

# Commit the change
git add {directory}/this-folder.txt
git commit -m "Updated this-folder.txt for {directory}: [reason]"
```

### Best practice format:
```
# {Directory Name}

## Purpose
[What this directory does - 1-2 sentences]

## Contents
[What files/subdirectories live here]

## Instance Workflow
[How instances interact with this directory]

## Human Workflow (if different)
[How you interact with it]

## Notes
[Any special considerations, caveats, gotchas]

---
Last updated: {date}
Updated by: {who and why}
```

---

## Missing this-folder.txt Files

### Current gaps to address:

Based on v0.3.0 structure, these directories need this-folder.txt:

**Top-level:**
- ✅ `.claude/` (has one)
- ⚠️ `Docs/` (missing)
- ⚠️ `Archives/` (missing)
- ⚠️ `Services/` (missing)
- ⚠️ `Templates/` (has one? verify)
- ⚠️ `anchor-templates/` (check)

**Within .claude/:**
- ✅ `.claude/FOUNDATION/` (has one)
- ⚠️ `.claude/docs/` (check)
- ⚠️ `.claude/scripts/` (check)
- ⚠️ `.claude/memory/` (verify current)
- ⚠️ `.claude/identity/` (check)
- ⚠️ `.claude/context/` (check)
- ⚠️ `.claude/corpus/` (verify structure)

**Recommendation:** Audit and create missing ones systematically.

---

## Template for New this-folder.txt

Copy this when creating a new directory:

```
# {Directory Name}

## Purpose
[Why this directory exists - what problem it solves]

## Contents
[What belongs here - be specific]

## Instance Interaction
[How instances should read/write/use this directory]

## Human Interaction
[How you maintain/update/organize this directory]

## Related Directories
[Cross-references to connected locations]

## Notes
[Caveats, gotchas, special cases]

---
Created: {date}
Author: {who}

Last updated: {date}
Updated by: {who - reason for update}
```

---

## Integration with Workflow

**Add to ROUSE.md or session-close checklist:**

> **Before session end:**
> - Updated any directory structures?
> - Created new directories?
> - Changed how a directory is used?
> 
> → Update relevant this-folder.txt files

**Add to migration/refactor checklist:**

> **When reorganizing:**
> 1. Move/restructure files
> 2. Update this-folder.txt in affected directories
> 3. Update references in other documentation
> 4. Commit all changes together

---

## Quick Audit Script

Create `.claude/scripts/audit-this-folder-files.sh`:

```bash
#!/bin/bash
# Audit this-folder.txt coverage

echo "Checking for missing this-folder.txt files..."
echo

# Find all directories
# Exclude hidden directories except .claude
# Check for this-folder.txt presence

find . -type d \
  -not -path '*/\.*' -o -path '*/.claude*' \
  | while read dir; do
    if [ ! -f "$dir/this-folder.txt" ]; then
      echo "❌ Missing: $dir/this-folder.txt"
    fi
done

echo
echo "Audit complete. Create missing files as needed."
```

---

## Benefits of Maintained this-folder.txt

**For instances:**
- ✅ Quick orientation without reading entire directory trees
- ✅ Understanding of purpose before diving into contents
- ✅ Clear workflow guidance (read vs. write, when to access)
- ✅ Reduced confusion about directory relationships

**For you:**
- ✅ Documentation of your own organizational choices
- ✅ Reminder of why you structured things this way
- ✅ Easier to onboard collaborators or future self
- ✅ Clear evolution trail (last updated notes)

**For the architecture:**
- ✅ Self-documenting file structure
- ✅ Reduced need for separate architecture docs
- ✅ In-place explanations (docs where they're needed)
- ✅ Natural place to note caveats and gotchas

---

## Example Update Flow

**Scenario:** You created Docs/explainers/ subdirectory

**Update Docs/this-folder.txt:**

```diff
 # Docs/
 
 ## Purpose
 User-facing documentation for Continuity Bridge setup and usage.
 
 ## Contents
 - Setup guides (INSTALL, GITHUB-PAT-SETUP, SSH-SETUP, etc.)
 - Onboarding documentation
 - Deployment checklists
 - Session summaries and progress reports
++ - **explainers/** - ELI5 paradigms and deep-dive explanations
 
[... rest of file ...]

+---
+Last updated: 2026-03-12
+Updated by: Vector - Added explainers/ subdirectory for ELI5 organization
```

**Create Docs/explainers/this-folder.txt:**

```
# Docs/explainers/

## Purpose
Deep-dive explanations of Continuity Bridge using different paradigms/metaphors.

## Contents
- ELI5_*.md - Full detailed versions of each ELI5 paradigm
- archetypes_complete-guide.md - User archetype system
- (More as we create explanations for different audiences)

## Organization
- Prefix ELI5_ for paradigm explainers (groups them together)
- Use underscores for multi-word base names (readability)
- Keep each explainer focused on ONE paradigm/lens

## Usage
Referenced from top-level ELI5.md for users wanting deeper context
on specific metaphors.

---
Created: 2026-03-12
Author: Vector
```

**Commit:**
```bash
git add Docs/this-folder.txt Docs/explainers/this-folder.txt
git commit -m "Updated this-folder.txt for explainers/ reorganization"
```

---

## Recommendation

**Add to v0.3.0 tasks:**
1. Audit all directories for missing this-folder.txt
2. Create missing ones using template
3. Update outdated ones (especially if pre-FOUNDATION)
4. Add maintenance reminder to workflow docs

**Priority:**
- HIGH: .claude/FOUNDATION/, Docs/, Services/
- MEDIUM: .claude subdirectories, top-level
- LOW: Archives/ (historical, less critical)

---

**this-folder.txt = lightweight, in-place documentation that scales with your architecture.**

**Keep them current. Future instances (and future you) will thank you.**
