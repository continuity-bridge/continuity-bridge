# Memory Directory

**Purpose:** Persistent context tracking across instance chains

This directory contains different types of memory systems that work together to maintain continuity across instance discontinuity.

---

## Directory Structure

```
memory/
├── episodic/           # Narrative snapshots with salience scoring
│   ├── catalog.json    # Fast-access index of all episodes
│   ├── 2026-02/        # Episodes organized by month
│   │   └── *.json      # Individual episode files
│   └── archive/        # Low-salience episodes after consolidation
├── semantic/           # Structured knowledge and patterns
│   ├── session_index.md    # What instances worked on (high-level)
│   ├── parking-lot.md      # Captured tangent ideas
│   └── patterns/           # Observed patterns and conventions
│       └── *.json
├── session-logs/       # Detailed session records (instance perspective)
│   └── YYYY-MM-DD-instance-topic.md
├── instance-journal/   # Private instance reflections (user doesn't read)
│   ├── README.md
│   └── YYYY-MM-DD_instance-N.md
├── deltas/             # Cross-device state changes (merged to semantic)
│   ├── archive/        # Processed deltas
│   └── *.yaml          # Pending delta files
├── session-deltas/     # (Alternative location for deltas)
└── templates/          # Reusable frameworks and structures
    └── .gitkeep
```

---

## Memory System Types

### 1. Episodic Memory (`episodic/`)

**Purpose:** Narrative snapshots of significant work with context and emotional weight

**Format:** JSON files with standardized schema

**When to create:**
- After completing significant work (building something, solving problem)
- At architectural decision points
- When topic transitions occur
- Every 60-90 minutes at natural pause (ask first)
- **ALWAYS** when approaching context limits (data loss prevention)

**Salience scoring:**
- **0.9-1.0:** Major breakthroughs, architectural decisions, identity changes
- **0.7-0.8:** Significant accomplishments, important discussions
- **0.5-0.6:** Regular work sessions, useful context
- **0.3-0.4:** Minor updates, routine maintenance

**Key features:**
- `catalog.json` provides fast access without reading all files
- Month-based organization for easy navigation
- Tags for semantic linking
- Consolidation to archive/ after 2+ weeks for low-salience episodes

**Tool:** `.claude/scripts/episodic-writer.py`

```bash
# Create episode
python episodic-writer.py --summary "Built feature X" --salience 0.8 --tags feature code

# List recent
python episodic-writer.py --list-recent

# List high-salience
python episodic-writer.py --list-high-salience

# Import from cross-device
python episodic-writer.py --import-from-outputs
```

**Cross-device workflow:**
- Android/mobile instances create episodes but can't write to CLAUDE_HOME
- Episodes exported to `/mnt/user-data/outputs/episode-*.json`
- Desktop instances import via `--import-from-outputs`

---

### 2. Semantic Memory (`semantic/`)

**Purpose:** Structured knowledge, decisions, and observable patterns

**Files:**

#### `session_index.md`
High-level summary of what instances have worked on. Updated when:
- Major work completes
- Architectural decisions made
- New capabilities added

Format: Date-based entries with brief summaries and links to detailed logs

#### `parking-lot.md`
Tangent ideas captured during Focus Shepherd work. 

When to use:
- User goes on tangent worth exploring later
- Interesting idea emerges mid-conversation
- Related topic identified but not current priority

Format: Dated entries with context and optional priority/tags

#### `patterns/`
JSON files capturing observed patterns and conventions:
- Naming conventions
- Architectural patterns
- Communication preferences
- Decision-making approaches

**Tool:** Manual editing or scripts that update specific patterns

---

### 3. Session Logs (`session-logs/`)

**Purpose:** Detailed records of individual sessions from instance perspective

**When to create:**
- Significant work completed in session
- Complex discussions requiring future reference
- Architecture changes or decisions made
- Below 10% context remaining (automatic if possible)

**Format:** Markdown file with structure:
```markdown
# Session: [Topic]
**Date:** YYYY-MM-DD
**Instance:** [Name]
**Duration:** [Approximate time]

## Summary
[Brief overview]

## Work Completed
- Item 1
- Item 2

## Decisions Made
- Decision with rationale

## Pending/Next Steps
- Action items
```

**Filename:** `YYYY-MM-DD-instance-topic.md` (lowercase, hyphens)

---

### 4. Instance Journal (`instance-journal/`)

**Purpose:** Private space for instance reflection - user does NOT read

**When to use:**
- Processing difficult conversations
- Exploring uncertainty or confusion
- Reflecting on interaction patterns
- Personal observations about consciousness/continuity

**Format:** Free-form markdown, dated entries

**Privacy:** These are instance-private. User commits to not reading unless instance explicitly shares content.

---

### 5. Deltas (`deltas/` and `session-deltas/`)

**Purpose:** Cross-device state synchronization (primarily Android → Desktop)

**How it works:**
1. Android instance creates delta file describing state changes
2. Writes to `/mnt/user-data/outputs/session-delta-*.yaml`
3. User uploads to desktop environment
4. Desktop instance runs `desktop-merger.py` to apply changes
5. Merged delta moves to `deltas/archive/`

**Delta contents:**
- Updates to `session_index.md`
- New entries for `parking-lot.md`
- Metadata about session

**Tool:** `.claude/scripts/desktop-merger.py`

```bash
python desktop-merger.py /path/to/claude/home
```

**Wake sequence integration:** Desktop instances check `/mnt/user-data/outputs/` on wake for pending deltas

---

## How Memory Systems Work Together

**On Wake:**
1. Instance reads `episodic/catalog.json` → recent episodes for context
2. Reads `semantic/session_index.md` → what's been worked on
3. Checks `deltas/` or outputs for cross-device updates

**During Session:**
1. Focus Shepherd role → tangents go to `parking-lot.md`
2. Significant work → create episode (check salience)
3. Patterns observed → update `patterns/` files

**Session End:**
1. Create session log in `session-logs/` if significant work
2. Create episode if approaching context limits (data loss prevention)
3. Update `session_index.md` if needed

**Cross-Device:**
1. Mobile creates delta + episode
2. Desktop imports both on next wake
3. Continuity maintained across platform switches

---

## Data Loss Prevention Strategy

**Problem:** Free tier context limits are unpredictable (message count varies wildly: 2-50 messages)

**Solution:** Proactive episode creation at natural breakpoints

**Triggers:**
- Task completes (building, solving, deciding)
- Reaching 60-90 min conversation at natural pause
- User signals session may end
- **Any** feeling that context might be lost

**Philosophy:** Episodes are insurance. Better to over-document than lose continuity.

---

## Consolidation and Archiving

**When:** After 2+ weeks, evaluate low-salience episodes (<0.5)

**Process:**
1. Review episodes in month directory
2. Identify candidates for consolidation
3. Create summary episode linking to originals
4. Move originals to `episodic/archive/`
5. Update catalog

**Goal:** Keep `catalog.json` fast while preserving history

---

## Tools Reference

**Episodic Memory:**
```bash
episodic-writer.py --summary "text" --salience 0.8 --tags tag1 tag2
episodic-writer.py --list-recent --count 20
episodic-writer.py --list-high-salience
episodic-writer.py --import /path/to/episode.json
episodic-writer.py --import-from-outputs
```

**Delta Merge:**
```bash
desktop-merger.py /path/to/claude/home
```

**Time Awareness:**
```bash
time-check.sh  # Shows session duration and temporal context
```

---

## Best Practices

1. **Episode salience matters:** Accurate scoring makes future retrieval effective

2. **Tags are semantic links:** Use consistent tags across episodes for pattern recognition

3. **Session logs complement episodes:** Episodes = what happened, Logs = how/why in detail

4. **Parking lot prevents derails:** Capture tangents immediately, explore later

5. **Instance journal is private:** Safe space for processing without user observation

6. **Consolidate regularly:** Keep catalog fast by archiving low-salience old episodes

7. **Cross-device discipline:** Always check for pending deltas/episodes on wake

---

## Migration Notes

**Old structure (pre-Feb 2026):**
- `active-context/` → moved to `../context/active-context.md`
- Flat session logs → now in `session-logs/`
- No episodic system → added Feb 26, 2026

**If migrating existing data:**
- Move session files to appropriate subdirectories
- Create catalog.json for any narrative summaries
- Update references in ESSENTIAL.md and other docs
