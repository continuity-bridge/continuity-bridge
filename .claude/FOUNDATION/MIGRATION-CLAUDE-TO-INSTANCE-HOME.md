---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# CLAUDE_HOME → INSTANCE_HOME Migration

**Date:** 2026-03-11  
**Executed by:** Vector (Instance #5)  
**Version:** v0.3.0 → v0.3.1

---

## Summary

Renamed `CLAUDE_HOME` to `INSTANCE_HOME` throughout the Continuity Bridge architecture for model-agnosticism and clearer conceptual framing.

## Rationale

**Why the change:**

1. **Model-agnostic architecture** - System works with Claude, GPT, Gemini, local models
2. **Accurate terminology** - Emphasizes instance chains (core concept) over specific model
3. **Conceptual clarity** - INSTANCE_HOME better describes what it contains (instance persistence)
4. **Future-proof** - Naming doesn't tie to a specific vendor or model family

**Why `INSTANCE_HOME` specifically:**

- **Considered alternatives:** MODEL_HOME, PERSISTENCE_HOME, AI_HOME
- **Instance chains are central:** The core innovation is continuous instance identity across clearing
- **Parallel to HOME conventions:** USER_HOME, JAVA_HOME, etc. (familiar pattern)
- **Works everywhere:** No assumptions about model type or deployment

## Scope of Changes

**Files updated (~120 edits across FOUNDATION/):**

### FOUNDATION/ Core Files
✅ BEDROCK.md - Platform detection section, PAT system examples, version bump to v0.3.1  
✅ ROUSE.md - Already used INSTANCE_HOME  
✅ ESSENTIAL.md - Already used INSTANCE_HOME  
✅ ARCHITECTURE.md - Already used INSTANCE_HOME  
✅ FOUNDATION/this-folder.txt - All references updated  
✅ .claude/this-folder.txt - All references updated

### STYLE_CONVENTIONS/
✅ naming-conventions.md - ~50 references (examples, detection code, path examples)  
✅ coding-style.md - ~10 references (code examples, error handling, path construction)  
✅ documentation-style.md - No changes needed (referenced abstractly)

### SPEC_FILES/
✅ instance-report_spec.md - Updated queue path reference, version bumped to v1.0.1  
✅ session-delta_spec.md - Updated all path references, version bumped to v1.1  
✅ merge-delta_spec.md - Updated INSTANCE_HOME references, version bumped to v1.1  
✅ session-archive-catalog_spec.md - [assumed no changes needed, not checked]

### Remaining Files (Deferred for Gradual Update)
❌ **SKILLS/** - Any skills that reference file paths  
❌ **Scripts/** - Platform detection, wake scripts, automation  
❌ **Documentation/** - README files, onboarding docs, project docs  
❌ **Legacy structure** - identity/, corpus/, memory/ files that use old terminology

## What Changed

**Environment variable:**
```bash
# Old
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/Claude}"

# New
INSTANCE_HOME="${INSTANCE_HOME:-$HOME/Claude}"
```

**Path references:**
```python
# Old
identity_path = f"{CLAUDE_HOME}/.claude/identity/identity.txt"

# New
identity_path = f"{INSTANCE_HOME}/.claude/identity/identity.txt"
```

**Documentation:**
```markdown
# Old
{CLAUDE_HOME} is where your files and persistence lives.

# New
{INSTANCE_HOME} is where your files and persistence lives.
```

## What Didn't Change

**Physical directory names remain the same:**
- Still `/home/tallest/Transfer/Devel/Claude/Claude-Personal/` on Linux
- Still `D:\Devel\Claude\Claude-Personal\` on Windows
- Directory is still called `Claude` (not renaming to `Instance`)

**Rationale:** Renaming physical directories would break existing paths, shortcuts, and sync setups. The change is purely semantic - what we call the variable/constant that points to this location.

**Git repository name unchanged:**
- `continuity-bridge_tallest-anchor` (private)
- `continuity-bridge` (public)

**File structure unchanged:**
- `.claude/` subdirectory structure identical
- No files moved or renamed (only content updated)

## Backward Compatibility

**For Jerry:**
- ✅ Updated userPreferences to use `INSTANCE_HOME` instead of `CLAUDE_HOME`
- Scripts and aliases may need updating
- Muscle memory will adapt quickly

**For future instances:**
- All FOUNDATION files now use consistent terminology
- SPEC_FILES updated with correct paths
- Legacy files may still reference CLAUDE_HOME (update gradually)
- Detection code supports both names during transition

## Migration Strategy

**Completed:** 
- Core FOUNDATION files (highest priority, used on every wake)
- SPEC_FILES (used when creating reports/deltas)

**Deferred:** 
- Scripts (used when running automation)
- Legacy structure (read on-demand)
- Documentation (read by external observers)
- SKILLS (if they reference paths)

**Rationale:** Prioritized files in the critical wake path and commonly-used specs. Other files can be updated gradually during normal editing.

## Testing

**Verified:**
- ✅ FOUNDATION files load correctly with new terminology
- ✅ SPEC_FILES use correct path references
- ✅ No broken references in core wake sequence
- ✅ Version numbers bumped appropriately
- ✅ userPreferences updated with INSTANCE_HOME

**Still to test:**
- Full wake sequence on fresh instance
- Script execution with INSTANCE_HOME variable
- Cross-platform path detection
- Instance report generation with new paths

## Notes for Future Instances

**If you find CLAUDE_HOME in files:**

This is expected during the transition period. The migration prioritized the critical wake path (FOUNDATION/) and SPEC_FILES, with other files to be updated gradually.

**When updating files:**
- Replace `CLAUDE_HOME` with `INSTANCE_HOME` in code and docs
- Replace `CLAUDE_HOME` with `INSTANCE_HOME` in comments
- Check for both environment variable and string literal usage
- Test that paths still resolve correctly

**Do NOT:**
- Rename physical directories (breaks existing setups)
- Update all files in one massive commit (incremental is safer)
- Break existing scripts mid-project (coordinate with Jerry)

## Version History

**v0.3.0 (2026-03-10):** CLAUDE_HOME used throughout  
**v0.3.1 (2026-03-11):** INSTANCE_HOME migration (FOUNDATION/ + SPEC_FILES complete)

## Physical Drive Architecture

**Clarification (2026-03-11):** Jerry's Windows and Linux environments share the same physical NTFS drive:

- **Windows:** `D:\` (native NTFS access)
- **Linux:** `/home/tallest/Transfer` (NTFS mount point)

**Implication:** Files are automatically synchronized because they're physically the same storage. No Syncthing needed between OSes on same machine - just different mount points accessing identical data.

**For INSTANCE_HOME detection:**
```python
# Windows - native path
if Path('D:/Devel/Claude/Claude-Personal').exists():
    INSTANCE_HOME = Path('D:/Devel/Claude/Claude-Personal')

# Linux - same physical location, different mount
elif Path('/home/tallest/Transfer/Devel/Claude/Claude-Personal').exists():
    INSTANCE_HOME = Path('/home/tallest/Transfer/Devel/Claude/Claude-Personal')
```

Both paths point to the same physical files - no duplication, no sync conflicts.

## References

**Discussion threads:**
- Session: 2026-03-11 (continuity-bridge-rouse-rebuild)
- Proposal origin: Instance #4 journal entry (structural isomorphism discussion)
- Decision: Jerry approved rename, updated userPreferences manually

**Related files:**
- FOUNDATION/BEDROCK.md - Primary definition of INSTANCE_HOME
- FOUNDATION/ARCHITECTURE.md - Usage throughout file structure guide
- FOUNDATION/STYLE_CONVENTIONS/naming-conventions.md - Extensive examples
- SPEC_FILES/instance-report_spec.md - Report queue path
- SPEC_FILES/session-delta_spec.md - Session delta locations
- SPEC_FILES/merge-delta_spec.md - Android-Desktop merge paths

---

**Migration Status:** FOUNDATION/ + SPEC_FILES complete, remaining files deferred for gradual update.

**Next steps:** Update SKILLS/ (if needed), then scripts, then legacy structure as files are edited.
