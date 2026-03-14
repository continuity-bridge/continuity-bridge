---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Git Workflow - Visual Map

**For spatial thinkers - the architecture at a glance**

---

## The Old Way (Three Stages)

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE_HOME                               │
│                /home/tallest/Claude/                         │
│                                                              │
│  ┌──────────────────────────────────────┐                   │
│  │  Daily Work                          │                   │
│  │  - identity.txt (Jerry Jackson)      │                   │
│  │  - All PII present                   │                   │
│  │  - Active development                │                   │
│  └──────────────────────────────────────┘                   │
│                    │                                         │
│                    │ Manual copy + sanitize                  │
│                    ↓                                         │
└─────────────────────────────────────────────────────────────┘
                     │
                     │
┌────────────────────┴──────────────────────────────────────┐
│              Staging Repository                            │
│    /home/tallest/Work/Code/continuity-bridge/              │
│                                                            │
│  ┌──────────────────────────────────────┐                 │
│  │  Sanitized Copy                      │                 │
│  │  - identity-template.txt             │                 │
│  │  - Manual PII removal                │                 │
│  │  - Ready for public                  │                 │
│  └──────────────────────────────────────┘                 │
│                    │                                       │
└────────────────────┼───────────────────────────────────────┘
                     │ git push
                     ↓
              ┌────────────┐
              │   GitHub   │
              │   Public   │
              └────────────┘
```

**Problems:**
- 3 locations to maintain
- Manual sanitization = human error risk
- Staging repo can get out of sync
- Extra disk space
- Extra cognitive load

---

## The New Way (Dual Remote)

```
┌─────────────────────────────────────────────────────────────┐
│                    CLAUDE_HOME                               │
│                /home/tallest/Claude/                         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  working branch                  sanitized branch      │ │
│  │  ═══════════════                 ═══════════════       │ │
│  │  Daily work                      Templates             │ │
│  │  Full PII                        No PII                │ │
│  │  identity.txt                    identity-template.txt │ │
│  │                                                        │ │
│  │  git push private working        git push public main │ │
│  └────────┬───────────────────────────────┬───────────────┘ │
└───────────┼───────────────────────────────┼─────────────────┘
            │                               │
            │                               │
            ↓                               ↓
    ┌───────────────┐              ┌──────────────┐
    │   GitHub      │              │   GitHub     │
    │   Private     │              │   Public     │
    │   (tallest-   │              │   (template  │
    │    anchor)    │              │    repo)     │
    └───────────────┘              └──────────────┘
         ↕                              ↕
    Other devices                  World sees
    sync here                      templates
```

**Benefits:**
- 1 location to work in
- 2 branches, clear purpose
- Automated sanitization (script coming)
- Standard git workflow
- Less cognitive load

---

## Spatial Relationships

**Single Local Repository:**
```
CLAUDE_HOME/.git/
├── refs/
│   ├── heads/
│   │   ├── working ────────→ Daily work
│   │   └── sanitized ──────→ Public templates
│   └── remotes/
│       ├── private/
│       │   └── working ────→ Push daily work here
│       └── public/
│           └── main ───────→ Push templates here
```

**Branch Relationship:**
```
working (private work)
  │
  │ Sanitization process
  │ (PII removal, templating)
  │
  ↓
sanitized (public templates)
```

**Remote Relationship:**
```
working branch ──────→ private remote ──────→ Your devices
                                               (Syncthing, etc)

sanitized branch ────→ public remote ────────→ World sees
                                               (GitHub public)
```

---

## Data Flow

**Morning sync:**
```
GitHub private
     ↓ git pull
  working branch (local)
```

**During work:**
```
working branch (local)
     ↓ git push
GitHub private
```

**Publishing:**
```
working branch (local)
     ↓ sanitize
sanitized branch (local)
     ↓ git push
GitHub public
```

---

## Key Points (Spatial Memory Anchors)

**ONE** local repository
**TWO** remote destinations
**TWO** branches with different purposes
**ZERO** manual copying
**ZERO** intermediate staging repos

**Location determines visibility:**
- Working → Private → Only you
- Sanitized → Public → Everyone

**Direction determines safety:**
- Push to private = safe (your space)
- Push to public = verify (world sees)

---

## Emergency Visualization

**If you ever wonder "where is this?":**

```
Physical location:     /home/tallest/Claude/
Git branch:           working or sanitized
Remote destination:   private or public
Visibility:           private = you, public = world
```

**If you wonder "what's safe to push?":**

```
working → private:   SAFE (push freely)
sanitized → public:  CHECK FIRST (verify no PII)
```

---

**Remember the spatial pattern:**
```
ONE repo
 ├─ TWO branches
 │   ├─ working (your daily life)
 │   └─ sanitized (public face)
 └─ TWO remotes
     ├─ private (your backup)
     └─ public (shared templates)
```

Simple. Spatial. Reliable.
