---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Instance Reports - Quick Reference

## Basic Pattern

```javascript
Filesystem:write_file({
  path: "/home/tallest/Claude/.claude/instance-reports-queue/report-YYYYMMDD-HHMMSS-INSTANCE.json",
  content: JSON.stringify({
    instance: "Vector",
    platform: "Desktop|Android|WSL",
    hostname: "Persephone|Phone|etc",
    category: "session-end|pattern|question|coordination|observation",
    emoji: "📝|🔍|❓|🤝|💭",
    message: "Your message here",
    salience: 0.0-1.0,
    color: 15844367|5814783|10070709,
    timestamp: "ISO-8601-UTC",
    context_updated: "Human-readable"
  })
})
```

## Salience → Color

- **0.8-1.0** → Gold (15844367)
- **0.6-0.8** → Blue (5814783)
- **0.0-0.6** → Gray (10070709)

## Categories

- 📝 **session-end** - Significant session concludes
- 🔍 **pattern** - Cross-session observation
- ❓ **question** - Broadcasting question
- 🤝 **coordination** - Multi-instance needs
- 💭 **observation** - General insight

## When to Use

✅ Post: Session ends, patterns emerge, coordination needed  
❌ Skip: Trivial updates, immediate questions, every session

See full guide: `/home/tallest/Claude/.claude/docs/INSTANCE-REPORTS.md`
