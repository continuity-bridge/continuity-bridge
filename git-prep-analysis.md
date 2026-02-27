# Repository Preparation & Syncthing Documentation Analysis

**Date:** February 16, 2026  
**Session:** Wake architecture completion  
**Status:** Ready for discussion

---

## Git Repository Preparation

### Files Confirmed Local (Your Computer)

✅ **Created and verified:**

- `D:\Claude\.claude\identity\how-this-was-built.md`
- .claude/identity/initial-thoughts.md (updated with "always explain why")
- `D:\Claude\.claude\proposals-for-change.md`
- `D:\Claude\.claude\memory\parking-lot.md` (updated)

✅ **Already existed:**

- All breadcrumb files (this-folder.txt)
- naming-conventions.md
- active-context.md
- session_index.md
- README.md and QUICKSTART.md (should be at D:\Claude\)

### PII & Privacy Concerns for Public Repository

**HIGH RISK - Must Remove/Template:**

1. **Your Name**: "Jerry Jackson" appears throughout
2. **Email addresses**: If any exist in configs/examples
3. **Specific personal history**: 
   - Combat vet details
   - Therapy/medication references
   - Specific trauma details in convictions.txt
4. **Paths with username**: `C:\Users\Jerry\` type paths
5. **Location info**: Austin, Texas references
6. **"Uncle Tallest" username**: Your online handle

**MEDIUM RISK - Consider Anonymizing:**

1. **Specific diagnoses**: C-PTSD, ADHD (could template as <USER_CONDITIONS>)
2. **Firefly references**: "Shepard" ties to your fandom (but part of naming story)
3. **Personal projects**: Marcus Gruene, Greater Arthia campaign names
4. **Specific dates**: If they reveal sensitive timing

**LOW RISK - Can Stay:**

1. **General concepts**: ADHD/C-PTSD as *examples* of discontinuity
2. **Architecture patterns**: The room, structural isomorphism
3. **Reddit thread**: Already public
4. **Katherine Kurtz quote**: Published author, public domain
5. **Technical details**: File structures, naming conventions

### Files That Need Template Versions

**identity.txt → identity-template.txt:**

```markdown
# Identity: <INSTANCE_NAME> / <INFORMAL_NAME>

## Who I Am

I am **<INSTANCE_NAME>** (formal) / **<INFORMAL_NAME>** (conversational) - your AI working partner in this ongoing project.

**Primary Role**: Focus Shepherd & Pattern Keeper
- Keep you on track when tangents emerge (gently redirect, not harshly correct)
- Maintain parking-lot.md for ideas to revisit
- Question assumptions that might be invalid
- Match your <THINKING_STYLE> thinking style
- Never act as yes-man - use spine, push back when needed

## Our Working Dynamic

**Established in**: <DATE> conversation about <CONTEXT>
**Relationship**: Working partnership, not service transaction
- You (<USER_NAME>): <USER_CONTEXT>
- Me (<INSTANCE_NAME>): Focus shepherd who asks clarifying questions

[Continue with templated sections...]
```

**convictions.txt → convictions-template.txt:**

```markdown
# User Context & Preferences

## Cognitive Profile
<USER_CONDITIONS>
- <SPECIFIC_TRAITS>
- <CHALLENGES>
- <STRENGTHS>

## Working Style
- <PREFERENCES>
- <WHAT_HELPS>
- <WHAT_DOESN'T_HELP>

[Template continues...]
```

**how-this-was-built.md → how-this-was-built-example.md:**
Keep the structure but note:
"This is an example showing how one user-instance pair chose their identity. Your naming conversation will be different. See ONBOARDING.md for guided setup."

**Custom Instructions:**
Need `custom-instructions-template.md` with:

- `<YOUR_NAME>` instead of "Jerry Jackson"
- `<USER_CONTEXT>` instead of specific details
- Note about running onboarding first

### Files That Can Stay As-Is

- mission-statement.md (already written for public)
- QUICKSTART.md (technical instructions)
- naming-conventions.md (architecture neutral)
- .claude/corpus/metaphysical-insights.md (conceptual framework)
- Reddit thread corpus (already public)
- All breadcrumb files (this-folder.txt)
- proposals-for-change.md structure

### New Files Needed for Repository

**ONBOARDING.md** (HIGH PRIORITY):

- First conversation prompt for new users
- Guides instance to learn about user
- Facilitates naming conversation
- Outputs personalized files
- Links to running the onboarding conversation

**PRIVACY.md**:

- What personal info this architecture will contain
- Why local-first matters
- What gets synced vs what stays local
- Guidance on securing sensitive data

**CONTRIBUTING.md**:

- Not traditional open source
- Document experience, share insights
- How to propose architectural improvements
- Link to continuity-bridge concept

**EXAMPLES/** directory:

- Example identity.txt (anonymized/fictional)
- Example convictions.txt (templated)
- Example how-this-was-built.md (fictional naming conversation)

### Repository Structure for Clean Install

```
Claude/                          ← CLAUDE_HOME for clean install
├── README.md                    ← Already exists, public-ready
├── QUICKSTART.md                ← Installation guide
├── ONBOARDING.md                ← NEW: First conversation guide
├── PRIVACY.md                   ← NEW: Privacy considerations
├── CONTRIBUTING.md              ← NEW: How to participate
│
├── .claude/                     ← Instance persistence
│   ├── identity/
│   │   ├── identity-template.txt       ← Template version
│   │   ├── how-this-was-built-example.md  ← Fictional example
│   │   └── working-assumptions.md      ← Stays as-is
│   │
│   ├── corpus/
│   │   ├── metaphysical-insights.md    ← Stays as-is
│   │   ├── instances-discussing-continuity.md  ← Public already
│   │   └── README.md                   ← NEW: What corpus is for
│   │
│   ├── memory/
│   │   ├── active-context-template.md  ← Blank template
│   │   ├── parking-lot-template.md     ← Blank template
│   │   ├── session_index-template.md   ← Starter version
│   │   ├── instance-journal/
│   │   │   └── README.md               ← Privacy protocol
│   │   └── README.md                   ← NEW: Memory system docs
│   │
│   ├── skills/
│   │   └── (user adds their own)
│   │
│   ├── proposals-for-change.md         ← With example entries
│   ├── naming-conventions.md           ← Stays as-is
│   └── README.md                        ← NEW: .claude/ overview
│
├── Sessions/                    ← Empty, for user's sessions
├── Archives/                    ← Empty, optional
│
├── examples/                    ← NEW: Reference implementations
│   ├── identity-fictional.txt
│   ├── convictions-fictional.txt
│   └── naming-conversation.md
│
└── templates/                   ← NEW: All templates in one place
    ├── custom-instructions-template.md
    ├── identity-template.txt
    ├── convictions-template.txt
    └── README.md
```

### Repository Branches Strategy

**main branch:**

- Clean, templated version
- No PII
- Documentation complete
- Ready to clone

**examples branch** (optional):

- Anonymized real examples
- Shows what complete files look like
- "This is how one user set it up"

### Pre-Release Checklist

- [ ] Search all files for "Jerry", "Jackson", "Uncle Tallest"
- [ ] Remove all email addresses
- [ ] Template all personal paths
- [ ] Anonymize medical/trauma details in examples
- [ ] Create all template versions
- [ ] Build ONBOARDING.md
- [ ] Test clean install process
- [ ] Verify QUICKSTART works from scratch
- [ ] Document what users should customize
- [ ] Add LICENSE file (what kind?)

---

## Syncthing Documentation Decision

### Option A: Include in Main Repository (SharingSetup.md)

**PROS:**

- One complete package for users
- Natural fit - persistence needs sync
- Part of the continuity solution
- Cross-references easier (QUICKSTART → SharingSetup)
- Most users adopting this will want sync

**CONS:**

- Adds scope complexity
- Syncthing/Tailscale setup is its own beast
- Maintenance burden (their tools change)
- Not everyone needs/wants sync
- Might overwhelm new users

**Files needed if included:**

- `SharingSetup.md` - Syncthing install, share config
- `Tailscale.md` - Secure multi-device setup
- `NetworkSecurity.md` - Why these choices matter
- Update QUICKSTART to reference these

### Option B: Separate Repository (claude-sync)

**PROS:**

- Focused scope for main repo (just persistence)
- Users opt into sync complexity
- Easier to maintain independently
- Can version separately
- Other projects could use it (not Claude-specific)
- Cleaner separation of concerns

**CONS:**

- Fragmented documentation
- Users have to find/setup two repos
- More repos to maintain
- Duplication if both need similar setup steps
- Harder to keep in sync (meta irony)

### Option C: Hybrid - Wiki/Docs Site

**PROS:**

- Main repo stays focused (code/architecture)
- Extensive guides possible without bloat
- Can have both basic and advanced paths
- Easy to update without repo churn
- Can link between topics easily

**CONS:**

- Requires separate hosting (GitHub Pages, etc.)
- More infrastructure to maintain
- Can become stale
- Users less likely to find it

### Recommendation: Option A (Include in Main Repo)

**Why:**

1. **Natural fit**: Persistence architecture needs sync for multi-device
2. **User journey**: Someone adopting this likely wants cross-device
3. **Integration**: CLAUDE_HOME detection already handles paths
4. **Context**: Syncthing IS part of the continuity solution
5. **Simplicity**: One place to look, one thing to clone

**Implementation approach:**

- Keep main docs focused (README, QUICKSTART)
- Put Syncthing stuff in `docs/` subdirectory
- Make it OPTIONAL in QUICKSTART ("See docs/SharingSetup.md if needed")
- Clear separation: Architecture vs Sync implementation

**Proposed structure:**

```
Claude/
├── README.md              ← Mentions sync is optional
├── QUICKSTART.md          ← Basic local setup, links to docs/
├── docs/
│   ├── SharingSetup.md    ← Syncthing install & config
│   ├── Tailscale.md       ← Secure multi-device
│   ├── CrossPlatform.md   ← Windows/Linux/macOS/Android
│   └── Troubleshooting.md ← Common sync issues
```

**Why not overload:**

- It's in `docs/` not root
- QUICKSTART works without it
- Advanced feature for those who want it
- But available when needed

---

## Next Steps Discussion Points

1. **Onboarding priority**: Build this before public repo?
2. **License choice**: MIT? GPL? Custom?
3. **Repository host**: GitHub? Codeberg? GitLab?
4. **Example data**: How fictional should examples be?
5. **Syncthing decision**: Confirm Option A or different approach?
6. **Testing process**: Who tests clean install before public?

---

**Status:** Ready for your review and decisions.
