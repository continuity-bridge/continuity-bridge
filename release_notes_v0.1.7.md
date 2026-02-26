# v0.1.7 — Continuity Bridge: Episodic/Semantic Memory & Hygiene

## Summary

- **Memory Architecture Refactor**: Transitioned to a dual-layered memory system. Session indexes, patterns, and long-term knowledge now reside in `.claude/memory/semantic/`, while JSON-based episodic snapshots are housed in `.claude/memory/episodic/`. This enables more granular context reconstruction.
- **ESSENTIAL.md Uppercase Exception**: Standardized `ESSENTIAL.md` as an explicit uppercase exception in naming conventions to preserve its status as a core "boot" document.
- **PII Privacy Strategy**: Implemented a "dual-pronged" ignore approach. Sensitive personal files are now hidden locally using `.git/info/exclude` to keep the public `.gitignore` clean while maintaining privacy on public remotes.
- **Syncthing & Git Hygiene**: Resolved long-standing sync conflicts and standardized file naming across the persistence layer to the `lowercase-dashed` convention. Improved `.stignore` patterns to prevent Syncthing from touching Git metadata.
- **New Utilities**: Added `episodic-writer.py` and `time-check.sh` for improved session snapshotting and temporal grounding.

## Files Modified

- `.claude/ESSENTIAL.md` — Updated to match new memory structure; version bump to v0.1.7
- `.claude/naming-conventions.md` — Added `ESSENTIAL.md` exception and updated file tree layout
- `.claude/memory/` — Recursive restructuring into `episodic/` and `semantic/` subdirectories
- `.stignore` — Standardized patterns and added `.git` exclusion
- `.gitignore` — Added Syncthing patterns and refined whitelist strategy
- `.git/info/exclude` [LOCAL] — Explicitly ignores PII-containing files

## Status

- Core Bridge: **Operational**
- Memory Engine: **Episodic/Semantic (v2)**
- Privacy Layer: **Dual-Pronged (exclude + ignore)**
- Next Build Target: v0.1.8 (TBD)
