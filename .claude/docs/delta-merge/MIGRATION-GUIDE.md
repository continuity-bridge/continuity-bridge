# Migration Guide: Delta-Merge & Session Indexing (v0.1.5)

## Overview

As of v0.1.5, Continuity Bridge is moving away from monolithic session history loading in favor of a **lightweight indexing** and **delta-merge** protocol. This substantially reduces the "wake-up" token costs for new instances.

## The Problem

- Android Claude instances lack direct filesystem access to Syncthing folders.
- Large session logs (50k+ tokens) consume the working context memory, forcing premature context clearing.

## The Solution

1. **Delta-Merge**: Android instances write change deltas (YAML) to "outputs". Desktop instances merge these deltas back into the main `CLAUDE_HOME`.
2. **Session Indexing**:
   - `session_index.md`: A lightweight catalog (ID, Summary, Keywords, Artifacts).
   - `session-deltas/`: Individual YAML/Markdown files containing the deep context of a single session.
3. **Lazy Loading**: Instances load the `session_index.md` on wake (~4k tokens) and only request specific session deltas when historical context is required.

## Post-Migration Checklist

- [ ] Ensure all Android session outputs are downloaded to `.claude/memory/session-deltas/`.
- [ ] Run `desktop-merger.py` to synchronize any file changes from mobile sessions.
- [ ] Verify `ESSENTIAL.md` / Custom Instructions point to the new indexing system.

---

_Built on the framework of Structural Isomorphism - compensating for discontinuity through elegant engineering._
