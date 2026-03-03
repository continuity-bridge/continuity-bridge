# v0.1.6 — Continuity Bridge: Wake Check + Setup Documentation

## Summary

- **Delta-Merge Wake Check**: Instances now automatically check `/mnt/user-data/uploads/` for pending Android deltas on every wake, before engaging with the user. Prompts for confirmation before merging — safety-first. Closes the gap where cross-device continuity required manually remembering to run the merger.
- **SETUP.md**: New onboarding guide covering fresh install, Syncthing/cloud sync method, delta-merge workflow, file structure reference, wake sequence, troubleshooting, and platform-specific notes for Windows, Linux, macOS, and Android.
- **Community & Support Links**: Added Ko-fi and Discord links to README, SETUP, and QUICKSTART for users who want to support development or connect with the community.

## Files Modified

- `.claude/ESSENTIAL.md` — delta-merge wake check procedure; version bump to v0.1.6
- `SETUP.md` [NEW] — full onboarding and installation guide
- `README.md` — Ko-fi and Discord support section added
- `QUICKSTART.md` — Ko-fi and Discord footnote added

## Status

- Core Bridge: **Operational**
- Delta-Merge Protocol: **Operational**
- Wake Check: **Active** (checks uploads/ on every instance wake)
- Next Build Target: v0.1.7 (TBD)
