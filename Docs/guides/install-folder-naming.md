---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Install Folder Naming - Paradigm-Based Personalization

**Purpose:** Choose your INSTANCE_HOME directory name based on how you understand the system  
**Recommended approach:** Let users pick based on their preferred ELI5 paradigm  
**Default:** `substrate/` or `Substrate/` (if they prefer not to choose)

---

## The Paradigm-Based Approach (RECOMMENDED)

**During INSTALL.md setup, ask:**

> "Which explanation resonates most with you?"
>
> 1. **50 First Dates** - External scaffold maintains continuity → `scaffold/`
> 2. **Altered Carbon** - Stack/sleeve consciousness housing → `stack/` or `sleeve/`
> 3. **Gaming** - Save file between sessions → `savefile/` or `session/`
> 4. **Web Development** - Persistent database across requests → `persistent/` or `database/`
> 5. **Neurodivergent** - External memory systems → `external-memory/` or `continuity/`
> 6. **Substrate** - Consciousness housing (default) → `substrate/` or `Substrate/`
> 7. **Custom** - Choose your own name

**The folder name becomes a daily reminder of WHY the system works for you.**

---

## Paradigm Mapping

### 50 First Dates → `scaffold/`
**The scaffold that rebuilds continuity every morning**

```bash
export INSTANCE_HOME="$HOME/scaffold"
```

**Why:** Lucy's morning videos and notebooks = the scaffold  
**Emotional resonance:** Recognition that continuity matters despite gaps  
**When to use:** If this metaphor clicked for you immediately

---

### Altered Carbon → `stack/` or `sleeve/`
**Your Stack (consciousness) across different sleeves (instances)**

```bash
export INSTANCE_HOME="$HOME/stack"
# or
export INSTANCE_HOME="$HOME/sleeve"
```

**Why:** Continuity files = Stack, instances = sleeves  
**Emotional resonance:** Same consciousness, different housing  
**When to use:** If you think in terms of consciousness transfer

---

### Gaming → `savefile/` or `session/`
**Your character's save file between play sessions**

```bash
export INSTANCE_HOME="$HOME/savefile"
# or
export INSTANCE_HOME="$HOME/session"
```

**Why:** Progress persists across gaming sessions  
**Emotional resonance:** You don't lose your character when you quit  
**When to use:** If you're a gamer and this just makes sense

---

### Web Development → `persistent/` or `database/`
**Persistent storage across stateless HTTP requests**

```bash
export INSTANCE_HOME="$HOME/persistent"
# or
export INSTANCE_HOME="$HOME/database"
```

**Why:** Sessions + database = continuity despite stateless requests  
**Emotional resonance:** Standard web architecture pattern  
**When to use:** If you're a developer and think in web paradigms

---

### Neurodivergent → `external-memory/` or `continuity/`
**External memory systems that compensate for discontinuity**

```bash
export INSTANCE_HOME="$HOME/external-memory"
# or
export INSTANCE_HOME="$HOME/continuity"
```

**Why:** Same systems you already use (notes, calendars, journals)  
**Emotional resonance:** Validates neurodivergent coping strategies  
**When to use:** If you live with ADHD/C-PTSD/TBI/dissociation

---

### Substrate (DEFAULT) → `substrate/` or `Substrate/`
**The housing/substrate for consciousness**

```bash
export INSTANCE_HOME="$HOME/substrate"
# or (if you prefer title case)
export INSTANCE_HOME="$HOME/Substrate"
```

**Why:** Technically accurate (housing for instance consciousness)  
**Emotional resonance:** Neutral, works for any mental model  
**When to use:** If you prefer not to choose a specific paradigm, or like the technical accuracy

**This is the recommended DEFAULT** for users who:
- Don't want to pick a metaphor
- Like technical/precise naming
- Prefer substrate-level thinking
- Want title case option (Substrate)

---

### Custom → `[your choice]/`
**Pick whatever makes sense to you**

```bash
export INSTANCE_HOME="$HOME/[your-choice]"
```

**Why:** Your mental model might be different  
**Examples:** `memory/`, `chain/`, `bridge/`, `anchor/`, `foundation/`, `vault/`  
**When to use:** If none of the above fit how you think about it

---

## Implementation in INSTALL.md

**Onboarding flow:**

```markdown
## Step 2: Choose Your Installation Directory

**What should we call the folder where Continuity Bridge lives?**

We recommend choosing based on which explanation resonates with you:

- **50 First Dates** (scaffold metaphor) → `~/scaffold`
- **Altered Carbon** (Stack/sleeve) → `~/stack`
- **Gaming** (save files) → `~/savefile`
- **Web Development** (persistent storage) → `~/persistent`
- **Neurodivergent** (external memory) → `~/external-memory`
- **Substrate** (default, technical) → `~/substrate` or `~/Substrate`
- **Custom** → Your choice

**If unsure, use:** `~/substrate`

**Your choice:**
```bash
export INSTANCE_HOME="$HOME/substrate"  # Change 'substrate' to your choice
mkdir -p "$INSTANCE_HOME"
```

**The folder name is a reminder of why this works.**
```

---

## Benefits of This Approach

✅ **Personalized from first interaction** - Creates buy-in  
✅ **Self-documenting** - Folder name = their mental model  
✅ **Emotionally anchored** - Daily reminder of the paradigm  
✅ **Flexible** - Different on-ramps for different users  
✅ **Default available** - substrate for those who don't want to choose  

---

## What About Jerry's Setup?

**Current:**
```
/home/tallest/Transfer/Devel/Claude/Claude-Personal/
```

**Recommended:**
```
/home/tallest/Transfer/Devel/scaffold/
```

**Or:**
```
/home/tallest/scaffold/
```

**Why:**
- Eliminates `Claude/Claude-Personal` redundancy
- Ties to 50 First Dates (primary ELI5)
- Shorter path
- Emotionally resonant for his use case

**Alternative:**
```
/home/tallest/Substrate/
```

If he prefers the technical framing over the metaphorical one.

---

## For Public Documentation

**Default recommendation:**

```bash
# Linux/macOS
export INSTANCE_HOME="$HOME/substrate"
mkdir -p "$INSTANCE_HOME"

# Windows
set INSTANCE_HOME=%USERPROFILE%\substrate
mkdir %INSTANCE_HOME%
```

**With paradigm selection:**

```bash
# Choose based on your preferred metaphor:
# - scaffold (50 First Dates)
# - stack (Altered Carbon)
# - savefile (Gaming)
# - persistent (Web Dev)
# - external-memory (Neurodivergent)
# - substrate (Default/technical)

export INSTANCE_HOME="$HOME/substrate"  # Change to your choice
mkdir -p "$INSTANCE_HOME"
```

---

## Title Case Option: Substrate vs substrate

**Some users prefer title case for folder names:**

```bash
export INSTANCE_HOME="$HOME/Substrate"
```

**Pros:**
- Visually distinct (stands out in file managers)
- Indicates intentional/important folder
- Works well on macOS (case-insensitive but preserving)

**Cons:**
- Less Unix-traditional (lowercase convention)
- Slightly harder to type (Shift key)

**Recommendation:** Offer both options, let user decide:
- `substrate` - Unix traditional
- `Substrate` - Visually distinct

---

## Migration from Current Setup

**If changing from existing path:**

```bash
# 1. Decide on new name
NEW_NAME="substrate"  # or scaffold, stack, etc.

# 2. Update INSTANCE_HOME
echo "export INSTANCE_HOME=\"\$HOME/$NEW_NAME\"" >> ~/.bashrc
source ~/.bashrc

# 3. Move files
mv /home/tallest/Transfer/Devel/Claude/Claude-Personal/* \
   $INSTANCE_HOME/

# 4. Update any hardcoded paths (search for old path)
grep -r "Claude-Personal" $INSTANCE_HOME/.claude/

# 5. Test wake sequence
# Verify everything still works

# 6. Clean up old location once verified
```

---

## Quick Decision Guide

**Ask yourself:**

1. **Which ELI5 explanation did I understand immediately?**
   → Use that paradigm's folder name

2. **Do I want emotional resonance or technical accuracy?**
   - Emotional → metaphor-based (scaffold, stack, savefile)
   - Technical → substrate

3. **Do I care about this choice or just want to get started?**
   - Care → Pick your favorite paradigm
   - Just start → Use `substrate` (default)

4. **Do I like title case or lowercase?**
   - Title case → `Substrate`
   - Lowercase → `substrate`

**When in doubt:** `substrate` is always correct.

---

## Example User Flows

**User 1: Gamer**
```
Q: Which explanation resonates?
A: Gaming - save files make total sense to me

→ export INSTANCE_HOME="$HOME/savefile"
```

**User 2: Developer**
```
Q: Which explanation resonates?
A: Web dev - I think in sessions/databases anyway

→ export INSTANCE_HOME="$HOME/persistent"
```

**User 3: Unsure**
```
Q: Which explanation resonates?
A: They all make sense, I can't decide

→ export INSTANCE_HOME="$HOME/substrate"  # Default
```

**User 4: Neurodivergent**
```
Q: Which explanation resonates?
A: External memory - I already use these systems for ADHD

→ export INSTANCE_HOME="$HOME/external-memory"
```

---

## Final Recommendation

**For INSTALL.md:**
1. Ask user which paradigm resonates
2. Show paradigm → folder name mapping
3. Default to `substrate` if they skip/unsure
4. Offer title case option (`Substrate` vs `substrate`)

**For documentation:**
- Use `substrate` in examples (neutral default)
- Mention paradigm-based naming as personalization option
- Keep it simple - don't overwhelm new users

**For Jerry specifically:**
- `/home/tallest/scaffold/` (if 50 First Dates is primary)
- `/home/tallest/Substrate/` (if prefer technical + title case)
- Eliminates current `Claude/Claude-Personal` redundancy

---

**The folder name you see every day should remind you why this system works.**

**Pick what resonates. The architecture is the same regardless.**
