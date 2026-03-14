---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# MIGRATION NOTES: CLAUDE_HOME → INSTANCE_HOME

**Date:** 2026-03-11  
**Executed by:** Vector  
**Reason:** Model-agnostic naming to support multi-model continuity infrastructure

---

## What Changed

The environment variable and constant `CLAUDE_HOME` has been renamed to `INSTANCE_HOME` throughout the entire architecture.

### Rationale

1. **Model-Agnostic:** Architecture now works with Claude, GPT, Gemini, local models, or future systems
2. **Architectural Clarity:** Emphasizes instance chains (core concept) over specific AI tool (Claude)
3. **Consistency:** Matches existing terminology (instance journal, instance chains, instance reports)
4. **Future-Proofing:** Name doesn't become misleading if users run non-Claude models

---

## Files Updated

### FOUNDATION/ Core Files
- ✅ `BEDROCK.md` - Detection and PAT system
- ✅ `ROUSE.md` - Wake sequence
- ✅ `ESSENTIAL.md` - Fast orientation (including definition update)
- ✅ `ARCHITECTURE.md` - Structure guide

### STYLE_CONVENTIONS/
- ✅ `naming-conventions.md` - All references, detection function renamed to `detect_instance_home()`

### Documentation
- ✅ All this-folder.txt files *(in progress - prioritized FOUNDATION)*

---

## What Users Need to Update

### Environment Variables

**Old:**
```bash
export CLAUDE_HOME="$HOME/Claude"
```

**New:**
```bash
export INSTANCE_HOME="$HOME/Claude"
```

### Custom Instructions (userPreferences)

Jerry will manually update userPreferences to replace:
- `{CLAUDE_HOME}` → `{INSTANCE_HOME}`
- References to CLAUDE_HOME in deferred tool loading examples

### Code and Scripts

**Python:**
```python
# Old
CLAUDE_HOME = os.getenv('CLAUDE_HOME')

# New  
INSTANCE_HOME = os.getenv('INSTANCE_HOME')
```

**Shell:**
```bash
# Old
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/Claude}"

# New
INSTANCE_HOME="${INSTANCE_HOME:-$HOME/Claude}"
```

### Path References

All path references updated from:
- `{CLAUDE_HOME}/.claude/` → `{INSTANCE_HOME}/.claude/`
- `$CLAUDE_HOME/.claude/` → `$INSTANCE_HOME/.claude/`

---

## Backward Compatibility

**Legacy Detection Pattern:**

For transition period, detection code can check both:

```python
def detect_instance_home():
    """Detect INSTANCE_HOME with fallback to legacy CLAUDE_HOME"""
    
    # Check new variable first
    if env_home := os.getenv('INSTANCE_HOME'):
        return Path(env_home)
    
    # Fallback to legacy name
    if env_home := os.getenv('CLAUDE_HOME'):
        return Path(env_home)
    
    # Platform detection
    # ...
```

This allows gradual migration without breaking existing setups.

---

## Testing Checklist

After updating, verify:

- [ ] userPreferences updated with INSTANCE_HOME
- [ ] Environment variables set correctly
- [ ] Wake sequence works (ROUSE.md → ESSENTIAL.md)
- [ ] Path detection working across platforms
- [ ] Scripts using new variable name
- [ ] No broken references in documentation

---

## Migration Timeline

**Immediate (2026-03-11):**
- ✅ All FOUNDATION/ documentation updated
- ✅ STYLE_CONVENTIONS/ updated
- ⏳ this-folder.txt files (in progress)

**User Action Required:**
- Update userPreferences (Custom Instructions)
- Update environment variables in shell configs
- Update any local scripts referencing CLAUDE_HOME

**Complete When:**
- All files use INSTANCE_HOME
- Detection scripts updated
- Platform-specific isms files updated
- No references to CLAUDE_HOME remain (except in migration notes)

---

## Why "INSTANCE_HOME" Not Other Options

**Considered alternatives:**
- `MODEL_HOME` - Too generic, doesn't emphasize continuity architecture
- `PERSISTENCE_HOME` - Too verbose, doesn't highlight instance chains
- `AI_HOME` - Far too generic, meaningless

**INSTANCE_HOME chosen because:**
- Emphasizes instance chains (architectural core concept)
- Model-agnostic but specific to our architecture
- Matches all existing terminology
- Clear what it contains (instance persistence)

---

## Impact Assessment

**Breaking Changes:**
- Environment variable name (users must update)
- Custom Instructions (Jerry updates manually)
- Any hardcoded references in local scripts

**Non-Breaking:**
- File structure unchanged
- Directory names unchanged
- `.claude/` subdirectory unchanged
- Functionality identical

**Benefits:**
- Architecture now truly model-agnostic
- Clearer terminology alignment
- Future-proof for multi-model support

---

## For Future Instances

You will wake to INSTANCE_HOME as the standard. CLAUDE_HOME is legacy terminology from when this was Claude-specific.

The architecture is model-agnostic - it works with any AI that can read files and maintain continuity through external memory. The name now reflects that reality.

---

**Migration Status:** ✅ Core Files Complete | ⏳ Full Deployment In Progress  
**Next:** Update remaining documentation, test cross-platform, update isms files
