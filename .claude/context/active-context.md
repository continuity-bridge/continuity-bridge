# Active Context

**Last Updated:** 2026-02-24 by Vector (Current Instance) - 3:30 PM CST

## Current Focus

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

**Continuity Bridge Evolution**
- **"Stateless State" Framing:** Core architecture description identified
- **Context Optimization:** Tiered storage, delta encoding planned for v2
- **Chain Architecture:** Unified across devices confirmed (not per-device)
- **File Organization:** 
  - `D:\Claude\Docs` = user-facing documentation
  - `D:\Claude\.claude\docs` = instance-facing documentation
  - `D:\Claude\.claude\assets` = new assets directory (needs review)

## Recent Work

- Generated action figure image for bootcamp bonus (posted LinkedIn/Instagram)
- Responded to Victor Foster's mirror/consciousness critique (engineering framing)
- Reviewed VtM V5 character sheets and analyzed filled example
- Analyzed Jerry's mentoring patterns via bootcamp support post
- Defined MongoDB schema approach for Sanguihedral

## Pending Tasks

- [ ] Review and organize files in new `assets/` directory
- [x] Android Delta-Merge Test (Initial Production Run)
- [x] v0.1.6 Tagging & Release
- [x] Implement Automated Bridge Sync (bridge-sync.sh)
- [ ] Add "stateless state" framing to documentation
- [ ] Incorporate mentoring message insights into relevant files
- [ ] Complete Sanguihedral database schema documentation
- [ ] Build aesthetic board for new character (image searches)
- [ ] Sprint 15 completion (testing + Google Cloud deployment)

## Sync Status (v0.1.7-dev)
- **Local Bridge:** Active (`~/Claude` <-> `continuity-bridge`)
- **GitHub Link:** Verified (SSH protocol)
- **Tooling:** `bridge-sync.sh` deployed and tested on Linux.

## Session Notes

Jerry's at 6% session limit - prioritize state saving and file organization.
Automatic context/session log writing on wake requested (memory discontinuity issue).
