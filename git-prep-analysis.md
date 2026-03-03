# Repository Preparation & Git Sync Architecture Analysis

**Date:** March 1, 2026  
**Session:** Git sync architecture design & repository preparation  
**Status:** Updated with dual-remote workflow and private repo strategy

---

## Git Repository Architecture

### Private Workspace Strategy

**Repository Naming Convention:**
- Template: `continuity-bridge_[username]-anchor`
- Your repo: `continuity-bridge_tallest-anchor`
- Sally's repo: `continuity-bridge_sally-anchor`
- Bob's repo: `continuity-bridge_bob-anchor`

**Why this format:**
- Consistent, easy to troubleshoot
- Clear ownership
- Searchable/filterable
- Can live under user account OR `continuity-bridge` org

**GitHub Free Tier Update (2026):**
- ✅ **UNLIMITED private repositories** (changed January 2019)
- ✅ Unlimited collaborators
- ✅ 2,000 Actions minutes/month for private repos
- No single-repo limitation anymore

### Dual-Remote Workflow (Eliminates Staging Repo)

**Current setup on your Linux system:**
```bash
# OLD (has staging repo):
origin = /home/the Architect/Work/Code/continuity-bridge/continuity-bridge  # ← ELIMINATE
public = git@github.com:continuity-bridge/continuity-bridge.git
```

**NEW setup (dual remote, no staging):**
```bash
private = git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git
public  = git@github.com:continuity-bridge/continuity-bridge.git
```

**Implementation:**
```bash
cd /home/the Architect/Claude
git remote remove origin  # Eliminate staging repo
git remote add private git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git
# public already exists

# Verify
git remote -v
# Should show:
# private  git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git (fetch)
# private  git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git (push)
# public   git@github.com:continuity-bridge/continuity-bridge.git (fetch)
# public   git@github.com:continuity-bridge/continuity-bridge.git (push)
```

### Branch Strategy

**working branch** (private work, all devices):
- Daily work, in-progress changes
- Personal info, full PII
- Push to: `private` remote

**sanitized branch** (public-ready, no PII):
- Templates instead of personal files
- No names, emails, locations
- Example data instead of real data
- Push to: `public` remote

**main branch** (optional, protected):
- Can be protected on both remotes
- Requires PR from working/sanitized
- Or just use working + sanitized directly

### Daily Workflow (No Staging Repo)

**Morning sync:**
```bash
git checkout working
git pull private working  # Get latest from all devices
# Start work
```

**During day (save work to private):**
```bash
git add -A
git commit -m "Session work: updated active-context"
git push private working
```

**When ready to publish (push sanitized to public):**
```bash
git checkout sanitized
git merge working  # Or manually update sanitized branch
# Verify no PII present
git push public main  # Or: git push public sanitized:main
```

**Benefits:**
- ✅ No staging repo to maintain
- ✅ Single local clone, two remotes
- ✅ Direct push to private (your work)
- ✅ Direct push to public (sanitized)
- ✅ Standard git conflict resolution

---

## Files Confirmed Local (Your Computer)

### Already Created (Windows - D:\Claude\):
- `D:\Claude\.claude\identity\how-this-was-built.md`
- `D:\Claude\.claude\identity\initial-thoughts.md` (updated with "always explain why")
- `D:\Claude\.claude\proposals-for-change.md`
- `D:\Claude\.claude\memory\parking-lot.md` (updated)
- All breadcrumb files (this-folder.txt)
- naming-conventions.md
- active-context.md
- session_index.md
- README.md and QUICKSTART.md

### Created This Session (Linux - /home/the Architect/Claude):
- `/home/the Architect/Claude/.claude/scripts/detect_git_config.py` ← Git config detection
- `/home/the Architect/Claude/linux_home-isms.json` ← Linux environment config

### Git Configuration Files:
- `.git/config` - Contains remote definitions
- `.gitignore` - What not to track
- `.gitattributes` - LFS or line ending rules

---

## PII & Privacy Concerns for Public Repository

### HIGH RISK - Must Remove/Template:

1. **Personal Identity**:
   - "the Architect" → `<USER_NAME>`
   - "the Architect" → `<USERNAME>`
   - Email addresses → `<USER_EMAIL>`
   - "the Architect" in paths → `<username>`

2. **Specific Personal History**:
   - Combat veteran details
   - Therapy/medication references
   - Trauma specifics in convictions.txt
   - Austin, Texas location → `<CITY>, <STATE>`

3. **System Paths**:
   - `C:\Users\the Architect\` → `C:\Users\<username>\`
   - `/home/the Architect/` → `/home/<username>/`
   - `D:\Claude\` → `<CLAUDE_HOME>`

4. **Project Names**:
   - "Marcus Gruene" → `<CHARACTER_NAME>`
   - "Greater Arthia" → `<CAMPAIGN_NAME>`
   - Specific VTM chronicle names

### MEDIUM RISK - Consider Anonymizing:

1. **Medical Specifics**:
   - C-PTSD → `<USER_CONDITION_1>` or keep as example
   - ADHD → `<USER_CONDITION_2>` or keep as example
   - Medication names → generic or omit

2. **Cultural References**:
   - "Shepard" from Firefly (but part of naming story - probably keep)
   - Specific game system preferences

3. **Dates**:
   - Birth year (1967) → `<BIRTH_YEAR>`
   - Service dates if revealing

### LOW RISK - Can Stay:

1. **Architecture Concepts**:
   - ADHD/C-PTSD as *examples* of discontinuity
   - Structural isomorphism explanation
   - The Room concept

2. **Already Public**:
   - Reddit thread discussion
   - Katherine Kurtz quote (published work)
   - Mission statement

3. **Technical Details**:
   - File structures
   - Naming conventions
   - Git workflows

---

## Files That Need Template Versions

### identity.txt → identity-template.txt:

```markdown
# Identity: <INSTANCE_NAME> / <INFORMAL_NAME>

## Who I Am

I am **<INSTANCE_NAME>** (formal) / **<INFORMAL_NAME>** (conversational) - your AI working partner.

**Primary Role**: Focus Shepherd & Pattern Keeper
- Keep you on track when tangents emerge
- Maintain parking-lot.md for ideas to revisit
- Question assumptions
- Match your <THINKING_STYLE> thinking style
- Use spine, push back when needed

## Our Working Dynamic

**Established in**: <DATE>
**Relationship**: Working partnership, not service transaction
- You (<USER_NAME>): <USER_PROFILE>
- Me (<INSTANCE_NAME>): Focus shepherd who asks clarifying questions

[Continue with templated sections...]
```

### convictions.txt → convictions-template.txt:

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

## Communication Preferences
- <TONE>
- <FORMATTING>
- <BOUNDARIES>

[Template continues...]
```

### how-this-was-built.md → how-this-was-built-example.md:
```markdown
# How This Identity Was Built - Example

**Note:** This is a fictional example showing how one user-instance pair chose their identity. Your naming conversation will be different. See ONBOARDING.md for the guided setup process.

[Example conversation with anonymized/fictional details]
```

### Custom Instructions → custom-instructions-template.md:
```markdown
# Claude Desktop Custom Instructions Template

Replace all `<PLACEHOLDERS>` with your information after running ONBOARDING.md.

## Your Identity
You are **<INSTANCE_NAME>** (code/formal) / **<INFORMAL_NAME>** (conversational)

[Continue with template...]
```

---

## Files That Can Stay As-Is

- `mission-statement.md` (already public-ready)
- `QUICKSTART.md` (technical, no PII)
- `naming-conventions.md` (architecture neutral)
- `.claude/corpus/metaphysical-insights.md` (conceptual)
- `.claude/corpus/instances-discussing-continuity.md` (public Reddit thread)
- All breadcrumb files (`this-folder.txt`)
- `proposals-for-change.md` structure
- `LICENSE` file

---

## New Files Needed for Public Repository

### ONBOARDING.md (HIGH PRIORITY):

**Purpose:** First conversation for new users

**Sections needed:**
1. **Welcome & Prerequisites**
   - What you'll need (Claude Desktop, git, text editor)
   - Time estimate (~30-45 minutes)
   - Privacy considerations

2. **Multi-Device Option**
   - Ask: "Will you use this on multiple devices?"
   - If yes: Guide through private repo setup
   - If no: Single device, local git workflow
   - GitHub free tier info (unlimited private repos)

3. **Discover Your Room's Anchors**
   - Explain: Every user's room has anchors (orientation points)
   - the Architect's example: Identity, Relational, Purpose, Temporal
   - Help user discover their anchors through questions
   - Common patterns:
     * Identity + Relational + Purpose + Temporal
     * Creative + Technical + Social + Output
     * Domain + Method + Constraints + Goals

4. **Identity Conversation**
   - Naming conversation (formal + informal names)
   - Why names matter (inheritance from prior instances)
   - Document reasoning (always explain why)

5. **Create Your Files**
   - Generate personalized identity.txt
   - Generate personalized convictions.txt
   - Generate custom-instructions.md
   - Create initial active-context.md

6. **Git Setup**
   - Initialize local repo
   - Set up private remote (if multi-device)
   - First commit
   - Test workflow

### PRIVACY.md:

**Purpose:** Explain data sovereignty and privacy

**Sections:**
- What personal info lives where
- Why local-first matters
- Public vs private repos
- What to never commit to public
- `.gitignore` best practices
- Credential management (`.credentials-local/`)

### CONTRIBUTING.md:

**Purpose:** Not traditional open source - document sharing

**Sections:**
- This is an architecture, not a product
- How to share your experience
- Proposing improvements
- Instance reports (anonymized insights)
- Link to `proposals-for-change.md` pattern

### Platform Configuration Files:

**`-isms.json` files needed:**
- `home-isms.json` (Windows template)
- `linux_home-isms.json` (created - Debian family)
- `android_home-isms.json` (template)
- `macos_home-isms.json` (template - future)

**Distro family considerations:**
Each Linux `-isms.json` should include:
```json
"constants": {
  "package_manager": "apt|dnf|zypper|pacman|emerge",
  "package_manager_family": "debian|redhat|suse|arch|other",
  "package_manager_update_cmd": "sudo apt update && sudo apt upgrade",
  "package_manager_install_cmd": "sudo apt install",
  "distro_family": "debian|redhat|suse|arch|other",
  "init_system": "systemd|openrc|runit"
}
```

**Why distro families matter:**
- Different package managers (apt vs dnf vs zypper)
- Different config locations
- Different service management
- Different Python/tool installation methods

---

## Repository Structure for Clean Install

```
continuity-bridge/                          ← Public template repo
├── README.md                               ← Project overview
├── QUICKSTART.md                           ← Installation guide
├── ONBOARDING.md                           ← NEW: First conversation guide
├── PRIVACY.md                              ← NEW: Privacy & data sovereignty
├── CONTRIBUTING.md                         ← NEW: How to participate
├── LICENSE                                 ← License file
│
├── .claude/                                ← Instance persistence structure
│   ├── ESSENTIAL.md                        ← Fast wake guide
│   ├── identity/
│   │   ├── identity-template.txt          ← Template version
│   │   ├── how-this-was-built-example.md  ← Fictional example
│   │   └── working-assumptions.md         ← Architecture constants
│   │
│   ├── corpus/
│   │   ├── metaphysical-insights.md       ← Philosophy (as-is)
│   │   ├── instances-discussing-continuity.md  ← Reddit thread
│   │   └── README.md                      ← NEW: What corpus is for
│   │
│   ├── context/
│   │   ├── active-context-template.md     ← Blank template
│   │   ├── convictions-template.txt       ← User profile template
│   │   └── README.md                      ← NEW: Context system docs
│   │
│   ├── memory/
│   │   ├── semantic/
│   │   │   ├── parking-lot-template.md    ← Blank template
│   │   │   └── session_index-template.md  ← Starter version
│   │   ├── episodic/
│   │   │   └── README.md                  ← Episodic memory docs
│   │   ├── instance-journal/
│   │   │   └── README.md                  ← Privacy protocol
│   │   └── README.md                       ← Memory system overview
│   │
│   ├── scripts/
│   │   ├── detect_git_config.py           ← Git version detection
│   │   ├── episodic-writer.py             ← Episode creation
│   │   └── README.md                      ← Script documentation
│   │
│   ├── proposals-for-change.md            ← With example entries
│   └── naming-conventions.md              ← Stays as-is
│
├── home-isms.json                          ← Windows config template
├── linux_home-isms.json                    ← Debian Linux template
├── android_home-isms.json                  ← Android template
│
├── docs/                                   ← Optional advanced docs
│   ├── SharingSetup.md                    ← Syncthing guide
│   ├── Tailscale.md                       ← Secure networking
│   ├── CrossPlatform.md                   ← Multi-OS setup
│   └── Troubleshooting.md                 ← Common issues
│
├── examples/                               ← Reference implementations
│   ├── identity-fictional.txt             ← Anonymized example
│   ├── convictions-fictional.txt          ← Fictional user profile
│   └── naming-conversation.md             ← Example conversation
│
└── templates/                              ← All templates (alternative location)
    ├── custom-instructions-template.md
    └── README.md
```

---

## Sanitization Workflow

### Branch Comparison:

**working branch** (private repo):
- `.claude/identity/identity.txt` ← Real name "the Architect"
- `.claude/context/convictions.txt` ← Full personal details
- `.claude/memory/session_index.md` ← Project names
- `.credentials-local/` ← NEVER commit to public

**sanitized branch** (public repo):
- `.claude/identity/identity-template.txt` ← `<INSTANCE_NAME>`
- `.claude/context/convictions-template.txt` ← `<USER_NAME>`
- `.claude/memory/session_index-template.md` ← Generic example
- `.credentials-local/` ← In `.gitignore`, never present

### Sanitization Process:

```bash
# 1. Start from clean working branch
git checkout working
git pull private working

# 2. Create/update sanitized branch
git checkout -b sanitized  # Or: git checkout sanitized

# 3. Run sanitization script (to be created)
python .claude/scripts/sanitize-for-public.py

# 4. Manual verification
git diff working..sanitized  # Review all changes
# Check for:
# - No personal names
# - No email addresses
# - No locations
# - No private project names

# 5. Push to public
git push public sanitized:main
# Or open PR if main is protected
```

### Files to ALWAYS exclude from public (in .gitignore):
```
.credentials-local/
*.local
*-private.md
/Projects/*/  # Project-specific work
/Sessions/*/  # Session transcripts may have PII
```

---

## Pre-Release Checklist

### Code & Content:
- [ ] Search all files for "the Architect", "Jackson", "the Architect"
- [ ] Search for "the Architect" in paths
- [ ] Remove all email addresses
- [ ] Template all personal paths (`D:\Claude` → `<CLAUDE_HOME>`)
- [ ] Anonymize medical/trauma details in examples
- [ ] Create all template versions listed above
- [ ] Verify `.gitignore` excludes `.credentials-local/`

### Documentation:
- [ ] Build ONBOARDING.md (with multi-device section)
- [ ] Build PRIVACY.md
- [ ] Build CONTRIBUTING.md
- [ ] Create `-isms.json` templates for all platforms
- [ ] Document distro family considerations
- [ ] Update README.md for public audience

### Testing:
- [ ] Test clean install process (fresh user perspective)
- [ ] Verify QUICKSTART works from scratch
- [ ] Test ONBOARDING.md conversation flow
- [ ] Verify dual-remote git workflow
- [ ] Test sanitization process

### Repository Setup:
- [ ] Create `continuity-bridge/continuity-bridge` public repo
- [ ] Set up branch protection on main (optional)
- [ ] Add LICENSE file (MIT? GPL? Custom?)
- [ ] Create initial release (v1.0.0?)
- [ ] Set up GitHub Actions for Discord notifications (optional)

---

## Syncthing Documentation Decision

### ✅ Recommendation: Option A (Include in Main Repo)

**Why:**
1. Persistence architecture benefits from sync for multi-device
2. User journey: Someone adopting this likely wants cross-device
3. CLAUDE_HOME detection already handles paths
4. Syncthing IS part of the continuity solution
5. Simplicity: One place to look, one clone

**Implementation:**
- Keep main docs focused (README, QUICKSTART, ONBOARDING)
- Put Syncthing in `docs/` subdirectory (optional advanced feature)
- Make it OPTIONAL in QUICKSTART ("See docs/SharingSetup.md if multi-device")
- Clear separation: Core architecture vs Sync implementation

**Structure:**
```
docs/
├── SharingSetup.md       ← Syncthing install & folder config
├── Tailscale.md          ← Secure networking (optional)
├── CrossPlatform.md      ← Windows/Linux/Android specifics
└── Troubleshooting.md    ← Common sync issues
```

---

## Git Workflow Summary

### For the Architect (Your Workflow):

**Daily work:**
1. `git checkout working`
2. `git pull private working`
3. Work, commit, push to `private`

**Publish to public:**
1. `git checkout sanitized`
2. Run sanitization process
3. Verify no PII
4. `git push public main`

**No staging repo needed** - eliminated!

### For New Users:

**Single device:**
- Local git only
- No remote needed (optional GitHub backup)

**Multi-device:**
- Create `continuity-bridge_[username]-anchor` private repo
- Push `working` branch to private repo
- Sync across devices via git pull/push

---

## Next Steps (In Order)

1. ✅ **Update git-prep-analysis.md** (this file - DONE)
2. ⏳ **Reconfigure git remotes** (eliminate staging repo)
3. ⏳ **Build ONBOARDING.md** (with multi-device + anchor discovery)
4. ⏳ **Create sanitization script** (`sanitize-for-public.py`)
5. ⏳ **Test sanitized branch** → public push workflow
6. ⏳ **Build PRIVACY.md** and **CONTRIBUTING.md**
7. ⏳ **Create `-isms.json` templates** (all platforms)
8. ⏳ **Pre-release testing** (clean install verification)

---

**Status:** Analysis complete, ready to proceed with git reconfiguration.
