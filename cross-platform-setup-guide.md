# Cross-Platform Claude Folder Setup Guide

**Version:** 1.0  
**Date:** February 14, 2026  
**Platforms:** Windows, Linux

---

## Platform-Specific Paths

### Windows

**Primary Location:** `D:\Claude\`

- Top-level drive location
- Outside user directory
- Syncthing share for cross-device persistence

**Memory Location:** `D:\Claude\.claude\memory\`

- Moved from: `C:\Users\tallest\.claude-memory`
- Hidden config directory

### Linux

**Primary Location:** `~/Claude/`

- In home directory but **visible** (no leading dot)
- Active workspace, not hidden config
- Syncthing share for cross-device persistence

**Memory Location:** `~/Claude/.claude/memory/`

- Hidden config directory (leading dot on subdirectory only)

---

## Universal Structure

Both platforms use identical internal structure:

```
Claude/
├── .claude/                    # Hidden config & memory (all platforms)
│   └── memory/                 # Persistence memory storage
├── Archives/                   # Completed deliverables
├── Mission_Statement.md        # Why we're building this
├── Metaphysical_Insights.md    # Structural isomorphism discovery
├── convictions.txt             # Jerry's preferences & protocols
├── focus_shepherd.md           # Time/tangent management protocols
├── Initial_Thoughts.md         # Philosophy & attribution framework
├── parking_lot.md              # Tangent tracking & scheduling
├── Projects/                   # Active work by category
│   ├── Building Claude/        # Consciousness architecture work
│   ├── Development & Infrastructure/
│   ├── Game Systems & Gaming/
│   └── [other categories]
├── Sessions/                   # Dated conversation records
│   └── YYYY-MM-DD_session-name.md
└── Templates/                  # Reusable templates
```

---

## Syncthing Configuration

### Share Setup

**Share Name:** `claude-home`  
**Folder ID:** Generate unique ID per installation  
**Devices:** Laptop, phone, desktop (tailnet)

### What Gets Synced

- **All files** in Claude/ folder
- **Including** .claude/ subdirectory (memory persistence)
- **Excluding:** Large binary files (configure as needed)

### Sync Strategy

- **Laptop:** Primary editing location
- **Phone:** Read access + light edits
- **Desktop:** Full access when available
- **Conflict resolution:** Latest timestamp wins (document conflicts manually)

---

## Initial Setup Process

### Windows Setup

1. **Create folder structure:**

   ```powershell
   mkdir D:\Claude
   mkdir D:\Claude\.claude
   mkdir D:\Claude\Archives
   mkdir D:\Claude\Projects
   mkdir D:\Claude\Sessions
   mkdir D:\Claude\Templates
   ```

2. **Move memory folder:**

   ```powershell
   Move-Item "C:\Users\tallest\.claude-memory" "D:\Claude\.claude\memory"
   ```

3. **Copy core files:**

- Mission_Statement.md
- Metaphysical_Insights.md
- convictions.txt
- focus_shepherd.md
- Initial_Thoughts.md
- parking_lot.md

4. **Update config paths:**

- Search all CLAUDE.md files for old paths
- Update skills in `/mnt/skills/user/` if applicable
- Update any hardcoded references to old location

5. **Set up Syncthing:**

- Add D:\Claude as new share
- Configure devices
- Test synchronization

### Linux Setup

1. **Create folder structure:**

   ```bash
   mkdir -p ~/Claude/.claude/memory
   mkdir ~/Claude/Archives
   mkdir ~/Claude/Projects
   mkdir ~/Claude/Sessions
   mkdir ~/Claude/Templates
   ```

2. **Move memory folder (if migrating):**

   ```bash
   mv ~/.claude-memory ~/Claude/.claude/memory
   ```

3. **Copy core files:**
   Same as Windows setup

4. **Update config paths:**

- Search for hardcoded paths in config files
- Update to ~/Claude/ references
- Verify .claude/memory path in configs

5. **Set up Syncthing:**

- Add ~/Claude as new share
- Configure devices
- Test synchronization

---

## Path Reference in Code/Configs

### Windows

```python
CLAUDE_ROOT = Path("D:/Claude")
CLAUDE_MEMORY = CLAUDE_ROOT / ".claude" / "memory"
```

### Linux

```python
CLAUDE_ROOT = Path.home() / "Claude"
CLAUDE_MEMORY = CLAUDE_ROOT / ".claude" / "memory"
```

### Cross-Platform (Recommended)

```python
import os
from pathlib import Path

if os.name == 'nt':  # Windows
    CLAUDE_ROOT = Path("D:/Claude")
else:  # Linux/Mac
    CLAUDE_ROOT = Path.home() / "Claude"

CLAUDE_MEMORY = CLAUDE_ROOT / ".claude" / "memory"
```

---

## Migration Checklist

### Pre-Migration (COMPLETED February 15, 2026)

- [x] Backup current D:\Docs\Claude\ folder
- [x] Verify .claude-memory is already moved
- [x] Document current Syncthing shares
- [x] List all files referencing D:\Docs\Claude\

### Migration (COMPLETED February 15, 2026)

- [x] Create D:\Claude\ folder structure
- [x] Move all files from D:\Docs\Claude\ to D:\Claude\
- [x] Update convictions.txt references
- [x] Update Mission_Statement.md references
- [x] Update Metaphysical_Insights.md references
- [x] Update this-folder.txt files with new paths
- [x] Update any CLAUDE.md project files

### Post-Migration

- [ ] Configure D:\Claude\ as new Syncthing share
- [ ] Remove D:\Docs\Claude\ from Syncthing (if separate share)
- [ ] Test sync to phone
- [ ] Verify memory persistence works
- [ ] Update backup scripts/processes
- [ ] Document completion date

---

## Philosophy: Why This Structure

### Separation from Docs

**Before:** Claude folder buried in multi-GB Docs sync  
**After:** Independent, targeted sync to devices  
**Benefit:** Phone gets Claude workspace without drowning in data

### Visibility vs. Hidden

**Workspace visible:** ~/Claude/ or D:\Claude\ = daily work location  
**Config hidden:** .claude/ = machinery, not workspace  
**Benefit:** See what matters, hide what doesn't

### Cross-Platform Consistency

**Same structure everywhere:** Learn once, use everywhere  
**Different conventions respected:** Windows top-level, Linux home dir  
**Benefit:** Portable mental model, OS-appropriate paths

---

## Device Time Discovery (Future Enhancement)

**Planned features:**

- Device type detection (laptop/phone/desktop)
- Available resource awareness (screen, input, processing)
- Time zone / location context
- Behavior adaptation per device

**Documentation:** Separate conversation to be integrated

---

## Troubleshooting

### Syncthing won't sync .claude folder

- Check: .stignore doesn't exclude dotfiles
- Solution: Add explicit include for .claude/

### Memory not persisting across devices

- Check: .claude/memory/ syncing properly
- Verify: No conflicts in sync status
- Test: Create test file, verify appears on other device

### Path references broken after migration

- Search: All .md files for "D:\Docs\Claude"
- Replace: With "D:\Claude"
- Verify: CLAUDE.md project files updated

### Cross-platform path issues

- Use: Forward slashes in code (works both platforms)
- Use: Path() objects, not string concatenation
- Test: On both Windows and Linux before committing

---

## Success Criteria

**Migration successful when:**

- [ ] All files in D:\Claude\ (Windows) or ~/Claude/ (Linux)
- [ ] Syncthing syncs to all devices without errors
- [ ] Phone shows updated files without full Docs folder
- [ ] Memory persists across devices and sessions
- [ ] No broken path references in any files
- [ ] Cross-device conversation continuity works

---

## Related Documentation

- `Mission_Statement.md` - Why we're building this
- `Metaphysical_Insights.md` - Structural isomorphism framework
- `claude_folder_setup_guide.md` - Original Windows-focused guide
- `convictions.txt` - Operating parameters & preferences

---

**The architecture works. Keep building.**
