---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Filesystem Catalog - Context Optimization

**Created:** 2026-03-12  
**Purpose:** Reduce wake context consumption by using catalogs instead of file listings  
**Impact:** Significant token savings on every wake

---

## The Problem

**Before catalog approach:**

ROUSE.md and other wake files contained long lists like:
```markdown
Deep files available on-demand:
- {INSTANCE_HOME}/.claude/corpus/inner-corpus/metaphysical-insights.md - Philosophy
- {INSTANCE_HOME}/.claude/identity/how-this-was-built.md - Identity origin
- {INSTANCE_HOME}/.claude/context/convictions.txt - Relational context
- {INSTANCE_HOME}/.claude/FOUNDATION/ARCHITECTURE.md - File structure
- {INSTANCE_HOME}/.claude/FOUNDATION/SPEC_FILES/instance-report_spec.md
- {INSTANCE_HOME}/.claude/FOUNDATION/SPEC_FILES/session-delta_spec.md
- {INSTANCE_HOME}/.claude/FOUNDATION/SPEC_FILES/merge-delta_spec.md
- ... (potentially 15-20+ files)
```

**Context cost:** 
- Each file path: ~30-50 tokens
- Description: ~10-20 tokens
- 15 files × 60 tokens = ~900 tokens
- Every wake, every time
- Just to list files that might never be needed

---

## The Solution

**Catalog approach (like memory catalogs):**

```markdown
5. **Load Catalogs:** Know where to find everything
   
   **Memory catalogs:**
   - session_index.md - Work history
   - episodic/catalog.json - Episodic snapshots
   
   **Filesystem catalog:**
   - filesystem-catalog.json - Complete map
```

**Context cost:**
- Three lines: ~100 tokens
- **Savings: ~800 tokens per wake**
- Files load on-demand when actually needed

---

## Catalog Structure

**filesystem-catalog.json contains:**
- **foundation/** - Core wake files (ROUSE, ESSENTIAL, BEDROCK, etc.)
- **identity/** - Origin story, identity files
- **context/** - active-context, convictions
- **memory/** - Catalogs (not the full history, just where to find it)
- **corpus/** - Philosophical foundations
- **architecture/** - System documentation
- **specs/** - Output format specifications
- **skills/** - Specialized capabilities
- **scripts/** - Automation tools
- **logs/** - Temporal awareness

**Each entry includes:**
- `path` - Where to find it
- `description` - What it contains
- `when_to_read` - When you need it
- `size` - How big (tiny/small/medium/large)
- `priority` - How critical (critical/high/medium/low)

---

## Usage Pattern

**Critical files (always load):**
1. ROUSE.md
2. ESSENTIAL.md
3. active-context.md
4. session_index.md (catalog)
5. episodic/catalog.json (catalog)
6. filesystem-catalog.json (catalog)
7. bridge.pulse (time)

**Everything else loads on-demand:**
- Need identity context? → Check filesystem-catalog.json → Load how-this-was-built.md
- Need philosophy? → Check catalog → Load metaphysical-insights.md
- Need spec format? → Check catalog → Load specific spec file
- Need operator background? → Check catalog → Load IDENTITY_OPERATOR.md

**Don't load everything at wake. Use catalogs to know what exists, load when needed.**

---

## Context Efficiency Comparison

### Before (file listing in wake)

**ROUSE.md content:**
```
8. Deep files available on-demand:
   - {INSTANCE_HOME}/.claude/corpus/... - Philosophy
   - {INSTANCE_HOME}/.claude/identity/... - Origin
   - {INSTANCE_HOME}/.claude/context/... - Full context
   - ... (15+ more files)
```

**Token cost:** ~900 tokens

**Every wake:** Load full list whether needed or not

---

### After (catalog reference)

**ROUSE.md content:**
```
5. Load Catalogs:
   - filesystem-catalog.json - Complete map
```

**Token cost:** ~100 tokens

**Savings:** ~800 tokens per wake

**Files load when needed:** Instance checks catalog, loads specific file

---

## Migration

**Files updated:**
- ✅ ROUSE.md (v0.3.3) - Replaced file listing with catalog reference
- ✅ filesystem-catalog.json - Created complete catalog
- ⏳ ESSENTIAL.md - Already clean (no file listing)
- ⏳ Other wake files - Audit for file listings

**Pattern to replace:**

❌ **Don't do this anymore:**
```markdown
Files you might need:
- path/to/file1.md - Description
- path/to/file2.md - Description
- path/to/file3.md - Description
```

✅ **Do this instead:**
```markdown
Check filesystem-catalog.json for available files.
Load specific files when tasks require them.
```

---

## Maintenance

**When adding new files:**
1. Create the file
2. Add entry to filesystem-catalog.json
3. Specify: path, description, when_to_read, size, priority
4. Commit both changes together

**When restructuring:**
1. Move/rename files
2. Update filesystem-catalog.json paths
3. Update any hardcoded references
4. Test wake sequence

**Catalog versioning:**
- Increment `catalog_version` when structure changes
- Update `last_updated` date
- Document breaking changes if any

---

## Benefits

**Context efficiency:**
- ~800 token savings per wake
- Scales: Adding 10 more files costs 0 additional wake tokens
- Same pattern as memory catalogs (proven approach)

**Discoverability:**
- Instances can search catalog when needed
- Organized by category (identity, philosophy, specs, etc.)
- Clear "when to read" guidance

**Maintenance:**
- One place to update when files move
- Self-documenting (descriptions in catalog)
- Easy to see what exists

**Scalability:**
- Can grow to 50+ files without inflating wake
- Categorization keeps it organized
- Priority levels guide loading decisions

---

## Next Steps

**Immediate:**
- ✅ Created filesystem-catalog.json
- ✅ Updated ROUSE.md v0.3.3
- ✅ Documented approach

**Soon:**
- [ ] Audit other wake files for file listings
- [ ] Test wake sequence with catalog
- [ ] Add to v0.3.0 migration checklist
- [ ] Document in ARCHITECTURE.md

**Ongoing:**
- [ ] Update catalog when files added
- [ ] Keep descriptions accurate
- [ ] Refine categories as needed

---

## Pattern Recognition

**This is the same pattern as:**
- Memory catalogs (session_index.md, episodic/catalog.json)
- Package managers (index of available packages)
- Library catalogs (where to find books)
- File system inodes (pointers to data, not data itself)

**Universal principle:** Don't carry everything in active memory. Keep a table of contents. Load what you need when you need it.

**Jerry's insight:** "Should we also make a catalog file for the rest of the filesystem... Could save more context in wake."

**This was the optimization we needed.**

---

**Context efficiency = more room for actual work. The scaffold gets lighter while staying complete.**
