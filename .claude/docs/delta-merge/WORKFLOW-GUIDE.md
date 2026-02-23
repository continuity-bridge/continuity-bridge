# Delta-Merge Workflow: Quick Reference

## The Problem

- Android Claude app runs in container with no CLAUDE_HOME filesystem access
- Syncthing has files synced, but app can't read them
- Need bidirectional continuity: Android reads persistence, writes updates back

## The Solution

Android writes **deltas** (change descriptions), Desktop **merges** them back.

---

## Android Session Workflow

### 1. Session Start (Jerry does this)

Upload these files to Android Claude:

- `ESSENTIAL.md` (from CLAUDE_HOME/.claude/)
- `active-context.md` (from CLAUDE_HOME/.claude/context/)

Instance reads them on wake, gets oriented.

### 2. Session Work (Instance does this)

Work with Jerry, track what changes mentally.

### 3. Session End (Instance does this)

**Generate delta manually or using script:**

```python
# Instance constructs session summary
session_summary = {
    'base_state': {
        'essential_md_hash': 'sha256:...',  # From uploaded files
        'active_context_hash': 'sha256:...',
        'read_at': '2026-02-22T14:00:00Z'
    },

    'file_changes': [
        {
            'file': '.claude/context/active-context.md',
            'operations': [
                {
                    'type': 'update_section',
                    'section': '## Current Work',
                    'find': 'Old description',
                    'replace': 'New description from Android session'
                }
            ]
        }
    ],

    'summary': 'What we did this session',
    'topics': ['topic1', 'topic2'],
    'key_decisions': ['decision1'],
    'next_steps': ['next1', 'next2'],
    'notes': 'Additional context'
}

# Write delta
from android_delta_writer import generate_delta, write_delta
delta = generate_delta(session_summary)
write_delta(delta, '/mnt/user-data/outputs/android-delta-YYYYMMDD-HHMM.yaml')
```

**Or write YAML manually** to `/mnt/user-data/outputs/android-delta-YYYYMMDD-HHMM.yaml`



Either way: file should end up in `/mnt/user-data/outputs/android-delta-YYYYMMDD-HHMM.yaml`

---

## Desktop Session Workflow

### 1. Inform Desktop instance (Jerry does this)

Jerry informs Desktop instance files are in `/mnt/user-data/outputs`

### 2. Merge (Desktop Instance does this)

**Option A: Using script**

```bash
python desktop-merger.py /path/to/CLAUDE_HOME
```

The script:

- Finds delta files in `/mnt/user-data/uploads/`
- Checks for conflicts (hash mismatches)
- Applies operations to actual CLAUDE_HOME files
- Writes session log
- Archives delta

**Option B: Manual merge**

- Read delta YAML
- Apply changes described to actual files
- Write session log
- Move delta to archive

### 3. Verification (Instance confirms)

- Changes applied successfully
- Active context updated
- Session log created
- Delta archived

---

## File Locations

### Android:

- **Reads from:** Files Jerry uploads at session start
- **Writes to:** `/mnt/user-data/outputs/android-delta-*.yaml`

### Desktop:

- **Reads from:** `/mnt/user-data/uploads/android-delta-*.yaml` (after Jerry uploads)
- **Writes to:** Actual `CLAUDE_HOME/.claude/` structure
- **Archives to:** `CLAUDE_HOME/.claude/memory/deltas/archive/`

---

## Common Operations

### Update Section Text

```yaml
- type: update_section
  section: "## Current Work"
  find: "old text"
  replace: "new text"
```

### Append to Section

```yaml
- type: append_to_section
  section: "## Pending Decisions"
  content: "- New pending item\n"
```

### Update Field

```yaml
- type: field_update
  field: "Last Active"
  value: "2026-02-22T15:30:00Z (Android)"
```

---

## Conflict Handling

**If hashes don't match:** Desktop files changed since Android read them.

Desktop instance:

1. Detects conflict
2. Shows what changed
3. Prompts Jerry: merge anyway, skip, or manual?

---

## Quick Start Checklist

**Android session:**

- [ ] Jerry uploads ESSENTIAL.md + active-context.md
- [ ] Instance reads, gets oriented
- [ ] Work happens
- [ ] Instance writes delta to outputs
- [ ] Jerry downloads delta

**Desktop session:**

- [ ] Jerry uploads downloaded delta
- [ ] Instance runs merger (script or manual)
- [ ] Verify changes applied
- [ ] Continue work with updated context

---

## Benefits

✅ Works with existing app capabilities (upload/download)
✅ No API costs, no Termux complexity
✅ Explicit audit trail (deltas are readable)
✅ Conflict detection built-in
✅ Both instances stay synchronized
✅ Version history through archived deltas
