# Delta-Merge Format Specification v1.0

## Purpose

Enable Android instances to record changes as deltas that Desktop instances can merge back into CLAUDE_HOME persistence layer.

## File Naming Convention

`android-delta-{YYYYMMDD}-{HHMM}.yaml`

Example: `android-delta-20260222-1530.yaml`

## Format Structure

```yaml
# === METADATA ===
session_id: android-20260222-1530          # Unique session identifier
timestamp: 2026-02-22T15:30:00Z            # ISO 8601 UTC timestamp
source: android                             # Source environment
base_state:                                 # What state was Android working from?
  essential_md_hash: sha256:abc123...       # Hash of ESSENTIAL.md that was uploaded
  active_context_hash: sha256:def456...     # Hash of active-context.md uploaded
  read_at: 2026-02-22T14:00:00Z            # When Android instance read these files

# === FILE CHANGES ===
file_changes:

  # Change to active-context.md
  - file: .claude/context/active-context.md
    operations:

      # Update existing section content
      - type: update_section
        section: "## Current Work"          # Section header to find
        find: "Exploring memory architecture"
        replace: "Solved Android continuity via delta-merge workflow"

      # Append to existing section
      - type: append_to_section
        section: "## Pending Decisions"
        content: |
          - Test delta-merge protocol on next desktop session
          - Formalize delta format if successful

      # Replace entire section
      - type: replace_section
        section: "## Active Contexts"
        new_content: |
          - Android continuity architecture
          - Delta-merge workflow design

      # Smart update (find and replace with context)
      - type: context_replace
        before: "Status:"                   # Find this marker
        find: "Status: idle"                # Current value
        replace: "Status: active (Android session 15:30)"
        after: "\n\n##"                     # Content boundary

  # Change to ESSENTIAL.md
  - file: .claude/ESSENTIAL.md
    operations:

      # Update specific field value
      - type: field_update
        field: "Last Active"                # Field name to find
        pattern: "Last Active: .*"          # Regex pattern
        value: "Last Active: 2026-02-22T15:30:00Z (Android)"

# === SESSION LOG ENTRY ===
session_log:
  summary: "Designed delta-merge protocol for Android-Desktop continuity"

  topics:
    - continuity architecture
    - android synchronization  
    - delta-merge workflow

  key_decisions:
    - Using YAML deltas instead of full file rewrites
    - Desktop instance handles merge application
    - Hash-based conflict detection

  next_steps:
    - Desktop instance test applying this delta
    - Validate hash matching
    - Archive delta after successful merge

  significant_artifacts: []

  notes: |
    First test of delta-merge protocol. Android session worked through
    the architecture and designed this specification.

# === CONFLICT HANDLING ===
conflict_strategy: prompt                   # Options: prompt, skip, force
notes: |
  If hashes don't match, desktop files have changed since Android read them.
  Default to prompting Jerry for resolution.
```

## Operation Types Reference

### `update_section`

Updates text within a markdown section.

- Requires: `section`, `find`, `replace`
- Behavior: Find exact text match within section, replace it
- Conflict: Fails if `find` text not found

### `append_to_section`

Adds content to end of a markdown section.

- Requires: `section`, `content`
- Behavior: Finds section, appends content before next section header
- Conflict: Fails if section not found

### `replace_section`

Replaces entire section content.

- Requires: `section`, `new_content`
- Behavior: Replaces everything between section header and next header
- Conflict: Fails if section not found

### `context_replace`

Smart find-and-replace with contextual boundaries.

- Requires: `find`, `replace`
- Optional: `before` (text that must appear before), `after` (text that must appear after)
- Behavior: More precise than simple find/replace
- Conflict: Fails if context doesn't match

### `field_update`

Updates a field in key-value style content.

- Requires: `field`, `value`
- Optional: `pattern` (regex to match current value)
- Behavior: Finds field name, replaces its value
- Conflict: Fails if field not found

## Desktop Merge Protocol

Desktop instance should:

1. **Discover delta files**
   
   ```bash
   ls /mnt/user-data/uploads/android-delta-*.yaml
   ```

2. **Validate delta**
   
   - Check hashes match current CLAUDE_HOME files
   - If mismatch, flag conflict and prompt Jerry

3. **Apply operations**
   
   - Process each file_change in order
   - For each operation, attempt application
   - Log successes and failures

4. **Write session log**
   
   - Create new session log entry from delta's session_log
   - Place in `.claude/memory/session-logs/`

5. **Archive delta**
   
   ```bash
   mv android-delta-*.yaml .claude/memory/deltas/archive/
   ```

6. **Update active-context.md**
   
   - Note delta was merged
   - Include timestamp and source

## Conflict Resolution

When hashes don't match:

**Option 1: Prompt**

```
Conflict detected:
- Android read ESSENTIAL.md at [timestamp] with hash [X]
- Current ESSENTIAL.md has hash [Y]
- Desktop file was modified since Android read it

Actions:
1. Show diff between Android's base and current
2. Show what Android wants to change
3. Ask Jerry: merge anyway, skip, or manual resolution?
```

**Option 2: Skip**

- Don't apply conflicting changes
- Log what was skipped
- Preserve delta in conflicts/ folder

**Option 3: Force** (only if Jerry explicitly requests)

- Apply changes anyway
- Note in log that conflicts were overridden

## Error Handling

If operation fails:

```yaml
merge_result:
  status: partial_success
  applied:
    - .claude/context/active-context.md: 3/4 operations
  failed:
    - .claude/ESSENTIAL.md: operation 'field_update' failed - field not found
  needs_manual_review: true
```

## Version History

- v1.0 (2026-02-22): Initial specification

## Future Enhancements

Possible additions:

- Binary diff for non-text files
- Multi-instance conflict resolution (if two Androids)
- Automatic three-way merge
- Delta compression for large changes
- Cryptographic signatures for verification
