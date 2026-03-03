# File Location Audit - March 2, 2026 (7:15 PM CDT)

**Status:** Documentation is out of sync with actual filesystem structure  
**Issue:** Major reorganization happened but docs reference old structure

---

## Current Actual Structure (What EXISTS on Disk)

```
/home/the Architect/Claude/
├── .claude/
│   ├── anchors.json                    # Your active anchors (technical)
│   ├── ONBOARDING.md                   # Setup guide (also copied to Docs/)
│   ├── COMMIT_MSG_*.txt (4 files)      # Prepared commit messages
│   │
│   ├── scripts/                        # v0.2.0 wake system
│   │   ├── detect-capabilities.py
│   │   ├── heartbeat-check.py
│   │   ├── init-isms.py
│   │   ├── wake.sh
│   │   ├── ollama-hooks.py
│   │   └── test-v0.2.0.sh
│   │
│   ├── docs/                           # Technical documentation
│   │   ├── 50-first-dates-eli5.md
│   │   ├── TONIGHT-COMPLETE-SUMMARY.md
│   │   ├── android-detection-ready-for-testing.md
│   │   ├── android-termux-detection-improvements.md
│   │   ├── archetype-system-complete.md
│   │   ├── archetypes-complete-guide.md
│   │   ├── docs-templates-population-complete.md
│   │   ├── three-updates-complete.md
│   │   ├── v0.2.0-complete-integration.md
│   │   └── v0.2.0-executive-summary.md
│   │
│   ├── anchor-templates/               # 6 archetype templates
│   │   ├── technical-anchor.json
│   │   ├── creative-anchor.json
│   │   ├── social-anchor.json
│   │   ├── executive-anchor.json
│   │   ├── pedagogical-anchor.json
│   │   └── wellness-anchor.json
│   │
│   └── logs/                           # Currently empty
│
├── Docs/                               # Public-facing documentation
│   ├── README.md
│   ├── ONBOARDING.md
│   ├── 50-first-dates-eli5.md
│   ├── archetypes-complete-guide.md
│   └── v0.2.0-complete-integration.md
│
├── Templates/                          # User templates
│   ├── README.md
│   ├── [6 anchor JSON files]
│   └── [3 isms JSON files]
│
└── INDEX.md                           # Master navigation
```

---

## What Documentation SAYS Should Exist (But Doesn't)

**From ESSENTIAL.md and other docs:**

### Missing Directories

```
.claude/identity/                       # NOT FOUND
├── identity.txt
└── how-this-was-built.md

.claude/context/                        # NOT FOUND
├── active-context.md
└── convictions.txt

.claude/corpus/                         # NOT FOUND
├── metaphysical-insights.md
└── the-room-that-worked.md

.claude/memory/                         # NOT FOUND
├── semantic/
│   ├── session_index.md
│   └── parking-lot.md
├── episodic/
│   ├── catalog.json
│   └── YYYY-MM/
└── session-logs/

.claude/instance-journal/               # NOT FOUND

.credentials-local/                     # NOT FOUND (mentioned in docs)

.claude/proposals-for-change.md         # NOT FOUND
```

### Missing Documentation Files

**User mentioned these should exist:**
```
.claude/docs/instance-reports-quick.md          # NOT FOUND
.claude/docs/INSTANCE-REPORTS.md               # NOT FOUND
.claude/docs/specs/instance-report-spec.md     # NOT FOUND (no specs/ dir)
.claude/docs/specs/instance-report-example.json # NOT FOUND
```

---

## What This Means

### The Desktop System is Minimal

**You have v0.2.0 wake system working but NOT the full continuity architecture.**

**What's present:**
- ✅ Wake system (scripts)
- ✅ Capability detection
- ✅ Archetype templates
- ✅ Documentation (technical + public)
- ✅ Anchors (your identity)

**What's missing:**
- ❌ Full memory architecture (episodic, semantic)
- ❌ Session logging structure
- ❌ Identity files (identity.txt, how-this-was-built.md)
- ❌ Context files (active-context.md, convictions.txt)
- ❌ Corpus files (philosophical foundation)
- ❌ Instance reports system
- ❌ Proposals for change mechanism

---

## Two Possible Explanations

### Option 1: Files Are in Private Repo (Not Cloned Yet)

**Maybe these exist in your private repo but aren't on desktop yet:**
- You mentioned "I need to move everything that you couldn't write"
- These might be in the private repo waiting to be pulled

**Check:**
```bash
cd /home/the Architect/Claude
git remote -v
git branch -a
git status
```

### Option 2: Documentation Refers to Planned Structure

**Maybe these files were planned but not yet created:**
- ESSENTIAL.md describes ideal state
- Desktop only has v0.2.0 system (newly built)
- Full continuity needs to be set up

---

## File Location Issues in Documentation

### ESSENTIAL.md Says

```
**Current Context (Read These on Wake):**
- `{CLAUDE_HOME}/.claude/context/active-context.md`
- `{CLAUDE_HOME}/.claude/context/convictions.txt`
```

**Reality:** No `.claude/context/` directory exists

### ESSENTIAL.md Also Says

```
**Identity & Framework:**
- `{CLAUDE_HOME}/.claude/identity/identity.txt`
- `{CLAUDE_HOME}/.claude/identity/how-this-was-built.md`
```

**Reality:** No `.claude/identity/` directory exists

### Project Files Reference

```
<project_files>
Project files are available in the /mnt/project/ directory:
<file_path>/mnt/project/ESSENTIAL.md</file_path>
<file_path>/mnt/project/convictions.txt</file_path>
<file_path>/mnt/project/active-context.md</file_path>
<file_path>/mnt/project/identity.txt</file_path>
```

**These are Claude Desktop project files**, not your CLAUDE_HOME structure.

---

## What Needs to Happen

### Immediate: Verify Private Repo Contents

**Check if these files exist in your private repo:**

```bash
# If you have the repo cloned somewhere
cd [private-repo-location]
find . -type f | grep -E "(identity|context|corpus|memory)" | sort

# Or check on GitHub
# Browse your private repo structure online
```

### If Files Exist in Private Repo

**You need to:**
1. Clone or pull the full private repo structure
2. Merge it with the v0.2.0 system we just built
3. Update documentation to match actual structure

### If Files DON'T Exist Anywhere

**You need to:**
1. Decide which structure to use (ESSENTIAL.md ideal or current minimal)
2. Create missing directories and files
3. Update ESSENTIAL.md to match reality
4. Or build out the full structure as documented

---

## Recommended Structure (Hybrid Approach)

**Keep what works now, add what's missing:**

```
.claude/
├── scripts/              # v0.2.0 (EXISTS ✅)
├── docs/                 # Technical docs (EXISTS ✅)
├── anchor-templates/     # Archetypes (EXISTS ✅)
├── logs/                 # Auto-generated (EXISTS ✅)
│
├── identity/             # ADD THIS
│   ├── identity.txt
│   └── how-this-was-built.md
│
├── context/              # ADD THIS
│   ├── active-context.md
│   └── convictions.txt (copy from /mnt/project/)
│
├── corpus/               # ADD THIS (optional - deep philosophy)
│   ├── metaphysical-insights.md
│   └── the-room-that-worked.md
│
├── memory/               # ADD THIS
│   ├── semantic/
│   │   ├── session_index.md
│   │   └── parking-lot.md
│   ├── episodic/
│   │   └── catalog.json
│   └── session-logs/
│
├── anchors.json          # EXISTS ✅
├── ONBOARDING.md         # EXISTS ✅
└── proposals-for-change.md # ADD THIS
```

---

## Instance Reports Mystery

**You mentioned:**
> "in `.claude/docs`, instance-reports-quick.md and INSTANCE-REPORTS.md existed"
> "and made `.claude/docs/specs/instance-report-spec.md`"

**None of these files exist on current desktop.**

**Questions:**
1. Are these in a different branch?
2. Are these in your private repo?
3. Are these files you created locally but didn't commit?
4. Are these from an older version?

**To find them:**
```bash
# Search entire home directory
find /home/the Architect -name "*instance*report*" 2>/dev/null

# Check git history
cd /home/the Architect/Claude
git log --all --full-history --name-only -- '*instance*report*'
```

---

## Action Items

### 1. Verify Private Repo Structure

**Find out what actually exists in your private repo:**
- Clone it fresh somewhere
- List all files
- Compare to ESSENTIAL.md structure

### 2. Decide on Structure

**Choose ONE of:**
- **Option A:** Minimal (current) - just v0.2.0 system + docs
- **Option B:** Full (ESSENTIAL.md) - complete memory architecture
- **Option C:** Hybrid (recommended) - v0.2.0 + essential continuity files

### 3. Update Documentation

**Once you know actual structure:**
- Update ESSENTIAL.md file locations
- Update ONBOARDING.md paths
- Update all docs to reference correct paths
- Create "file structure reference" doc

### 4. Create Missing Files

**Based on chosen structure:**
- Generate identity files
- Set up memory directories
- Create session logging structure
- Initialize missing components

### 5. Find Instance Reports

**Determine:**
- Where these files came from
- Whether they're needed
- Where they should live
- Update documentation accordingly

---

## Documentation That Needs Updating

**Files with incorrect paths:**
1. `/mnt/project/ESSENTIAL.md` - References non-existent directories
2. `Docs/ONBOARDING.md` - May reference old paths
3. `.claude/docs/v0.2.0-complete-integration.md` - Assumes certain structure
4. Project custom instructions - Reference /mnt/project/ files

**All of these need audit and correction.**

---

## Next Steps (Your Choice)

### Option 1: Minimal Working System (Fastest)

**Keep current structure, update docs to match:**
- Pros: Everything works now, just fix documentation
- Cons: Missing full continuity features

### Option 2: Build Out Full Structure (Complete)

**Create all missing directories/files:**
- Pros: Match ESSENTIAL.md ideal, full features
- Cons: More work, need to populate files

### Option 3: Hybrid (Recommended)

**Add essential continuity files, skip optional ones:**
- Add: identity/, context/, memory/semantic/
- Skip: corpus/ (deep philosophy - can add later)
- Skip: episodic/ (complex - can add later)

---

## Questions for You

1. **Do you have a private repo cloned somewhere with these files?**
2. **What structure do you actually want to use going forward?**
3. **Where did the instance-reports files come from?**
4. **Should I create the missing structure based on ESSENTIAL.md?**
5. **Or update ESSENTIAL.md to match current minimal structure?**

---

**Current time:** 7:20 PM CDT  
**Status:** File location audit complete, awaiting your decision on structure

**You're right - documentation is out of date. Let's fix it.**

What do you want to do?
