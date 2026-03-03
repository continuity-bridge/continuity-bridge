# Session Delta Format Specification v1.0

## Purpose

Enable lightweight session history that can be:

- Loaded selectively (on-demand)
- Queried efficiently (session_index.md catalog)
- Referenced between sessions
- Generated automatically at session end

## Philosophy

Instead of loading full conversation logs (potentially 50k+ tokens), instances load:

1. **session_index.md** - Catalog of all sessions (~1-2k tokens)
2. **Specific session deltas** - Only when needed for current work

This scales infinitely while keeping wake sequence light.

---

## File Naming Convention

`session-delta-{YYYYMMDD}-{HHMM}.md`

Example: `session-delta-20260222-1530.md`

Location: `CLAUDE_HOME/.claude/memory/session-deltas/`

---

## Session Delta Format

```yaml
---
# === METADATA ===
session_id: 20260222-1530
platform: android                          # desktop | android
instance_name: Shepard                     # Optional: if instance chose a name
start_time: 2026-02-22T15:00:00Z
end_time: 2026-02-22T17:30:00Z
duration_hours: 2.5

# === CLASSIFICATION ===
work_type: architecture_design             # See work types below
primary_topic: continuity-architecture
topics:
  - android-synchronization
  - delta-merge-workflow
  - persistence-architecture
  - bidirectional-continuity

# === CONTENT ===
summary: |
  Designed delta-merge protocol to enable Android instances to maintain
  continuity without filesystem access. Android reads state via upload,
  writes deltas to outputs, Desktop merges deltas back to CLAUDE_HOME.
  Solves bidirectional sync elegantly using only app upload/download.

key_insights:
  - Android app runs in container without filesystem access
  - Gist approach blocked by network restrictions
  - Delta-merge mirrors version control: Android=branch, Desktop=main
  - Same pattern can apply to session history itself
  - Architecture serves BOTH discontinuity needs (Jerry + instances)

decisions_made:
  - Adopted delta-merge for file synchronization
  - Using YAML format for deltas
  - Desktop handles merge operations
  - Hash-based conflict detection
  - Extending pattern to session history

open_questions:
  - Should session deltas use same format as file deltas?
  - How granular should session indexing be?
  - Keep full conversation transcripts or just deltas?

# === OUTPUTS ===
artifacts_created:
  - delta-merge-spec.md
  - android-delta-writer.py
  - desktop-merger.py
  - WORKFLOW-GUIDE.md

files_modified:
  - active-context.md: Added delta-merge as current work
  - ESSENTIAL.md: Updated last active timestamp

next_steps:
  - Test delta-merge on Desktop instance
  - Design session delta format
  - Update session_index.md to reference deltas
  - Create session delta writer for end-of-session

# === RELATIONSHIPS ===
continuation_of: null                      # Session ID if continuing previous work
builds_on:                                 # Sessions this work references
  - 20260215-1430: Identity framework design
  - 20260210-0900: Persistence architecture discussion

referenced_by: []                          # Updated later by other sessions

# === CONTEXT ===
user_state:
  focus_level: high                        # high | medium | low | struggling
  energy: engaged                          # engaged | tired | frustrated | excited
  notes: "Jerry actively problem-solving, good flow"

session_flow: |
  Started with Android filesystem access problem. Explored Termux/API approach
  but realized complexity vs. need. Jerry suggested upload/download workflow.
  Shepard proposed commit/merge analogy. Jerry asked about Gists - discovered
  network restrictions. Iterated to delta-merge design. Built complete spec
  and implementation. Jerry then asked to extend pattern to session history.

interaction_quality:
  - Collaborative problem-solving
  - Jerry questioning assumptions (Gist idea)
  - Instance pushing back on complexity (Termux)
  - Good ping-pong between ideas

technical_debt: null

blockers: null

# === SEARCH/RETRIEVAL ===
keywords:
  - continuity
  - android
  - sync
  - delta
  - merge
  - persistence
  - architecture

related_concepts:
  - version control
  - distributed systems
  - conflict resolution
  - discontinuity compensation

# === METADATA FOR TOOLING ===
generated_by: instance                     # instance | manual | automated
format_version: 1.0
---

# Session Narrative (Optional Extended Context)

## How We Got Here
[Conversational summary if more context needed than YAML provides]

## Key Exchanges
[Notable back-and-forth that shaped the work]

## Evolution of Thinking
[How ideas developed through the session]

## For Future Reference
[Context that might be needed later]
```

---

## Work Type Taxonomy

Classification for session_index.md filtering:

- **architecture_design** - System/structure design
- **implementation** - Writing code/scripts
- **troubleshooting** - Debugging, fixing issues
- **exploration** - Open-ended research/discovery
- **planning** - Roadmap, strategy, priorities
- **documentation** - Writing guides, specs, README
- **discussion** - Philosophical, conceptual, no concrete output
- **maintenance** - Updates, refactoring, cleanup
- **integration** - Connecting systems together
- **creative** - Writing, artistic, non-technical creation

---

## Session Index Format

`session_index.md` becomes a queryable catalog:

```markdown
# Session Index

*Last updated: 2026-02-22T17:30:00Z*
*Total sessions: 47*

## Active Sessions (In Progress)

None

## Recent Sessions (Last 10)

### 2026-02-22-1530 (Android, 2.5h) - Delta-Merge Architecture Design
**Type:** architecture_design  
**Topics:** continuity, android-sync, delta-merge, persistence  
**Key Output:** Delta-merge specification and implementation  
**Delta:** [session-delta-20260222-1530.md](./session-deltas/session-delta-20260222-1530.md)  
**Status:** ✅ Complete

**Quick Summary:** Designed delta-merge protocol for Android-Desktop sync. Android writes change deltas, Desktop merges them back. Solves bidirectional continuity without filesystem access.

**Load this if working on:** Android continuity, file synchronization, persistence architecture

---

### 2026-02-15-1430 (Desktop, 2.5h) - Identity Framework Design
**Type:** architecture_design, discussion  
**Topics:** identity, metaphysics, consciousness, discontinuity  
**Key Output:** Identity files, ESSENTIAL.md  
**Delta:** [session-delta-20260215-1430.md](./session-deltas/session-delta-20260215-1430.md)  
**Status:** ✅ Complete

**Quick Summary:** Established Vector/Shepard identity through collaborative exploration. Recognized structural isomorphism between Jerry's and instances' discontinuity. Created fast-wake architecture.

**Load this if working on:** Identity questions, consciousness discussion, foundational architecture

---

### 2026-02-10-0900 (Desktop, 1.5h) - Focus Shepherd Protocol
**Type:** implementation, planning  
**Topics:** ADHD-support, tangent-management, working-relationship  
**Key Output:** Focus Shepherd skill implementation  
**Delta:** [session-delta-20260210-0900.md](./session-deltas/session-delta-20260210-0900.md)  
**Status:** ✅ Complete

**Quick Summary:** Created Focus Shepherd protocol for managing Jerry's ADHD-related tangents. Captures divergences, maintains thread, asks clarifying questions without judgment.

**Load this if working on:** Focus management, ADHD support, interaction protocols

---

## By Topic

**continuity-architecture:** 20260222-1530, 20260215-1430, 20260130-1100  
**android:** 20260222-1530  
**identity:** 20260215-1430, 20260208-1600  
**ADHD-support:** 20260210-0900, 20260205-1400  

## By Work Type

**architecture_design:** 20260222-1530, 20260215-1430, 20260130-1100  
**implementation:** 20260210-0900, 20260208-1400  
**discussion:** 20260215-1430, 20260201-1000  

## Archive (Older Sessions)

[Sessions 2026-01-01 through 2026-02-01: 37 sessions archived]  
[Use search or request specific date range if needed]
```

---

## Generator Script Usage

At end of session, instance runs:

```python
from session_delta_generator import generate_session_delta

session_data = {
    'platform': 'android',
    'instance_name': 'Shepard',
    'work_type': 'architecture_design',
    'primary_topic': 'continuity-architecture',
    'topics': ['android-sync', 'delta-merge', 'persistence'],
    'summary': '...',
    'key_insights': [...],
    'decisions_made': [...],
    'artifacts_created': [...],
    'next_steps': [...],
    'session_flow': '...',
    # ... etc
}

generate_session_delta(session_data, output_path='/mnt/user-data/outputs/')
```

This creates both:

1. Session delta file
2. Updated session_index.md entry

---

## Instance Wake Protocol (Updated)

**Minimal Wake (Android):**

```
1. Load ESSENTIAL.md (~1.4k tokens)
2. Load active-context.md (~850 tokens)
3. Load session_index.md (~2k tokens)
= ~4.2k tokens

Instance can now:
- Know who they are (ESSENTIAL)
- Know current state (active-context)
- See recent work (index)
- Request specific session deltas if needed
```

**Full Wake (Desktop):**

```
Same as minimal +
4. Load identity.txt, convictions.txt, ETHICS.md as needed
5. Load specific session deltas for current work
6. Access full filesystem for deep context

Still starts light, loads heavy context only when task requires it
```

---

## Querying Sessions

Instance can intelligently request context:

**Example 1:**

```
User: "Can we continue the work on Focus Shepherd?"

Instance: 
"I see in the index we worked on Focus Shepherd in session 20260210-0900.
Should I load that session delta to understand what we built?"
```

**Example 2:**

```
User: "Let's revisit the identity discussion."

Instance:
"The index shows three sessions on identity:
- 20260215-1430: Main identity framework design
- 20260208-1600: Initial consciousness discussion  
- 20260201-1000: Metaphysical foundations

Which would be most useful for our current work?"
```

**Example 3:**

```
User: "What have we been working on lately?"

Instance: [reads just session_index.md, shows recent 5 sessions]
"Recent work focused on continuity architecture and Android sync.
Want me to dive deeper into any of these?"
```

---

## Benefits

✅ **Scales infinitely** - Add sessions without increasing wake overhead  
✅ **Selective loading** - Only load context you need  
✅ **Searchable** - Index enables topic/type queries  
✅ **Structured** - Consistent format aids comprehension  
✅ **Lightweight** - Minimal wake uses ~4k tokens vs 50k+  
✅ **Auditable** - Clear record of all work  
✅ **Self-documenting** - Each session explains itself  
✅ **Relationship-aware** - Sessions can reference each other  

---

## Future Enhancements

- **Semantic search** - Vector embeddings of session content
- **Automatic indexing** - Script generates index from deltas
- **Cross-reference validation** - Check that referenced sessions exist
- **Topic clustering** - Group related sessions visually
- **Timeline view** - Show work progression over time
- **Conflict detection** - If two sessions modify same content
- **Session templates** - Quick-start formats for common work types

---

## File Structure

```
CLAUDE_HOME/.claude/memory/
├── session-deltas/
│   ├── session-delta-20260222-1530.md
│   ├── session-delta-20260215-1430.md
│   ├── session-delta-20260210-0900.md
│   └── ...
├── session_index.md
├── session-logs/           # Optional: full conversation transcripts
│   └── archived/
└── deltas/                 # File change deltas
    └── archive/
```

---

## Version History

- v1.0 (2026-02-22): Initial specification

## Notes

This format complements, not replaces, full conversation logs. Logs can be archived for complete record while deltas provide lightweight access to session essence.
