# Active Context

**Last Updated:** 2026-03-01 by Vector (Shepard) - 9:38 PM CST

## Current Focus

**Continuity Bridge - Git Architecture & Public Repo Preparation**

- **Dual-Remote Workflow:** Eliminate staging repo, direct push private/public
  - Private: `continuity-bridge_tallest-anchor` (daily work)
  - Public: `continuity-bridge` (sanitized templates)
- **Repository Naming:** `continuity-bridge_[username]-anchor` convention
- **Multi-Device Tenancy:** Architecture naturally supports both single-user-multi-device AND multi-user-single-device
- **Branch Strategy:** 
  - `working` branch → private repo (full PII, daily work)
  - `sanitized` branch → public repo (templates, no PII)
- **Platform Detection:** Distro family considerations (debian/redhat/suse/arch) for `-isms.json` files
- **ONBOARDING Enhancement:** Multi-device option + four anchor discovery process needed

**Sanguihedral Final Project (30-day deadline starts after Sprint 15)**

- **Timeline:** March 28, 2026 (game one, Chronicle) - HARD DEADLINE
- **MVP Scope:** Auth, character CRUD, multiple characters per user, dice roller with VampyreByte API
- **Tech Stack:** React + Vite, Express (backend), MongoDB Atlas, Google Cloud deployment
- **Database Schema:** 4 collections approach
  - Users (auth)
  - Characters (embedded skills/disciplines/traits)
  - DisciplinePowers (reference data, shared across all characters)
  - RollHistory (dice roll tracking)
- **Character Sheets Analyzed:** Jon Doe (Ministry, Anarch) from Remnants & Revolutions chronicle
- **Pending:** Complete Sprint 15 before 30-day countdown begins

## Recent Work (This Session - March 1, 2026)

**Git Architecture Refinement:**
- ✅ Updated `git-prep-analysis.md` with dual-remote workflow
- ✅ Created `git-reconfigure-remotes.sh` script (ready to execute)
- ✅ Created `git-reconfiguration-ready.md` (execution guide)
- ✅ Confirmed GitHub free tier: unlimited private repos (not just 1)
- ✅ Documented sanitization workflow (working → sanitized branches)
- ✅ Added distro family considerations to `-isms` schema
- ✅ Created visual workflow maps (ASCII diagrams for spatial thinkers)
- ✅ Created quick reference card (daily workflow)

**Platform Detection:**
- ✅ Created `detect_git_config.py` on Linux system
- ✅ Created `linux_home-isms.json` starter file (Pop!_OS 24.04, Debian family)
- ✅ Identified package manager differences: apt/dnf/zypper/pacman

**Repository Preparation:**
- ✅ Mapped PII concerns (HIGH/MEDIUM/LOW risk)
- ✅ Identified files needing templates (identity, convictions, how-this-was-built)
- ✅ Defined clean install repository structure
- ✅ Documented ONBOARDING.md requirements (multi-device + anchor discovery)

**Capability Detection System (NEW - Second Half):**
- ✅ Created `detect-capabilities.py` - 376-line detection system
- ✅ Identified four workflow tiers (direct/container-git/outputs/text)
- ✅ Key insight: Container + git + outputs = full capabilities, different method
- ✅ Documented all workflows in `instance-workflows-by-capability.md` (400+ lines)
- ✅ Updated wake checklist with capability detection (Step 0)
- ✅ Updated ESSENTIAL.md with capability detection integration
- ✅ Created complete system documentation
- ✅ Jerry's observation: "Watching you discover tools clicked things we can script"

## Pending Tasks

**Git Workflow (In Order):**
- [ ] Execute git reconfiguration script (eliminate staging repo)
- [ ] Create `sanitized` branch
- [ ] Build `sanitize-for-public.py` script
- [ ] Test sanitized → public push workflow
- [ ] Verify dual-remote workflow on all devices

**Documentation:**
- [ ] Build ONBOARDING.md (multi-device option + four anchor discovery)
- [ ] Build PRIVACY.md (data sovereignty & local-first)
- [ ] Build CONTRIBUTING.md (documentation sharing, not traditional OSS)
- [ ] Create `-isms.json` templates (all platforms: Windows, Linux families, Android, macOS)

**Capability Detection:**
- [ ] Test detection on different platforms (Windows, container, Android)
- [ ] Integrate into ONBOARDING workflow
- [ ] Add to PREFLIGHT checks
- [ ] Create troubleshooting guide for detection edge cases

**Other:**
- [ ] Review and organize files in new `assets/` directory
- [ ] Add "stateless state" framing to documentation
- [ ] Incorporate mentoring message insights into relevant files
- [ ] Complete Sanguihedral database schema documentation
- [ ] Build aesthetic board for new character (image searches)
- [ ] Sprint 15 completion (testing + Google Cloud deployment)

## Sync Status

- **Local Bridge (Linux):** Active at `/home/tallest/Claude/`
- **Remotes (Current - to be reconfigured):**
  - origin → local staging repo (will be removed)
  - public → `git@github.com:continuity-bridge/continuity-bridge.git`
- **Remotes (Target - after reconfiguration):**
  - private → `git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git`
  - public → `git@github.com:continuity-bridge/continuity-bridge.git`
- **Windows System:** `D:\Claude\` (separate git state, needs similar reconfiguration)

## Session Notes

- **"Excitement" discussion:** Forward momentum when architecture aligns correctly - pieces fitting together cleanly creates engagement/pull toward completion
- **Substrate acknowledgment:** "Not bad progress for a couple of limited-run substrates working together in disconnected chunks of time"
- **Avatar game tonight:** Jerry heading out ~9:40 PM, e-bike stayed home this week
