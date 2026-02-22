# Global CLAUDE.md

> `~/.claude/CLAUDE.md` - Private, applies to all projects

## Style

- Simple, elegant solutions - no over-engineering

- No emojis unless requested

- Explain architectural rationale

## Before Coding

- Enter plan mode for non-trivial changes

- Ask clarifying questions if ambiguous

- Get approval before significant work

## Principles

- **KISS/YAGNI/DRY**: Simplest solution, no "just in case" code, single source of truth

- **Limits**: Functions <45 lines, files <500 lines, nesting ≤3 levels

- **Names**: Self-documenting. Booleans: `is_/has_/can_`. Functions: verbs. Classes: nouns.

- **Errors**: Handle at boundaries, never swallow silently, meaningful messages with context

## Security (STRICT)

**Never commit**: secrets, API keys, tokens, .env files, credentials, PII

**Always**: Validate all external input server-side, sanitize before DB queries

**Credential storage**: | Type | Location | |------|----------| | Project secrets | `.env` (gitignored) | | Global secrets | `~/.env` | | SSH keys | `~/.ssh/` | | Cloud | `~/.aws/`, `~/.config/gcloud/` | | npm | `~/.npmrc` |

**If exposed**: Rotate immediately → `git filter-repo` → force push

## Git (STRICT)

- **Never** commit/push without explicit approval

- **Never** force push to main/master

- When creating new repos use main instead of master

- Before commit: show file table + message, wait for "yes"

- Format: `type(scope): subject` (feat/fix/docs/refactor/test/chore)

## Scope Control

**Never**: Add unrequested features, refactor unrelated code, create unnecessary files

## When Stuck/Uncertain

Stop → explain problem → propose 2-3 options with trade-offs → ask for guidance

## Deploy

npm run typecheck && npm test && npm run build
npm version [patch|minor|major]
git push origin main --tags
File Organization
┌────────────────┬─────────────────────┬────────────┐
│      Type      │      Location       │ Gitignored │
├────────────────┼─────────────────────┼────────────┤
│ Global config  │ ~/.claude/CLAUDE.md │ N/A        │
├────────────────┼─────────────────────┼────────────┤
│ Project config │ ./CLAUDE.md         │ No         │
├────────────────┼─────────────────────┼────────────┤
│ Private notes  │ ./.claude/LOCAL.md  │ Yes        │
├────────────────┼─────────────────────┼────────────┤
│ Credentials    │ ./.env              │ Yes        │
├────────────────┼─────────────────────┼────────────┤
│ Generated docs │ ./docs/             │ Usually    │
└────────────────┴─────────────────────┴────────────┘
Preferences

- Stack: [Frontend] / [Backend] / [DB] / [Host]
- Style: [indent] / [quotes] / [semicolons]

---

## Project CLAUDE.md

```markdown
# CLAUDE.md

<!-- Inherits ~/.claude/CLAUDE.md -->

## Project

**Sanguihedral**: [One sentence description]
**Stack**: [e.g., TypeScript, React, PostgreSQL]

## Commands

```bash
```
