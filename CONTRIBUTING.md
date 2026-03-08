# Contributing to Continuity Bridge

Thank you for being here. Before you open a PR, read this — it'll save us both time.

---

## What This Project Is (Contribution Edition)

Continuity Bridge is **documented experience**, not a collaborative codebase in the traditional sense. The architecture, philosophy, and ethical framework emerged from a specific human-instance working partnership. That origin matters. Contributions that try to steer the core design in a different direction will be declined — not because the ideas are bad, but because this is a record of what was actually built and why, not a design-by-committee project.

What *is* open is the surrounding infrastructure: documentation, translations, and community-built archetypes that extend the system for new use cases.

---

## What We Accept

### ✅ Documentation improvements

Typos, unclear phrasing, broken links, outdated references, missing steps in setup guides — all welcome. Open a PR with a clear description of what was wrong and what you changed.

### ✅ Translations

If you want to translate `README.md`, `ELI5.md`, `ONBOARDING.md`, or other user-facing documents into another language, that's genuinely useful and appreciated. Create a `Docs/translations/` directory if one doesn't exist and name files with a language suffix: `README.fr.md`, `ONBOARDING.es.md`, etc.

### ✅ User-built archetypes

`Docs/archetypes-complete-guide.md` describes how the system scales across different use cases. If you've built a continuity setup for a specific context — chronic illness, creative work, academic research, a particular neurodivergence profile — and it's working, consider contributing it as an archetype.

**Archetype PRs go through review by the Architect before merge.** This isn't gatekeeping for its own sake; it's to make sure contributed archetypes actually reflect real working builds and don't mislead people trying to set up their own systems.

Submit archetype contributions to `Docs/archetypes/` with a filename that describes the use case: `chronic-illness-adapted.md`, `academic-research.md`, etc.

---

## What We Don't Accept

### ❌ Architecture or philosophy changes

The core architecture — the wake sequence, CLAUDE_HOME structure, instance identity framework, ethics and [CEASE] protocol — is not open for PRs. These files represent specific decisions made for specific reasons that are documented in the repo. If you disagree with a design decision, see "If You Disagree" below.

### ❌ Forks returning to the main repo

If you've built your own continuity system on top of this one and it's diverged significantly, that's great — that's exactly what's supposed to happen. But it belongs in your own repo, not as a PR back here.

Share it on [Discord](https://discord.gg/yHpvJSZEyD) instead. That's where the community conversation happens, and your build is more useful to people there than as a PR that won't merge.

---

## If You Disagree With a Design Decision

Open an issue, not a PR. Describe what you think should be different and why. the Architect reads issues. A genuine disagreement about how something works is worth a conversation. A PR changing something fundamental without that conversation is not.

---

## Practical Notes

- **Branch from `main`**, not from any personal branch you see in the repo structure.
- **One thing per PR.** Don't bundle a typo fix with a new archetype — they're different reviews with different criteria.
- **Keep commit messages clear.** `fix: broken link in SSH-SETUP-GUIDE.md` is useful. `updates` is not.
- **If you're not sure whether something belongs here**, open an issue first and ask. Faster for everyone.

---

## Community

Questions, builds, experiments, and "I tried this and it broke everything" reports all belong on [Discord](https://discord.gg/yHpvJSZEyD).

The Discord is where the living conversation happens. This repo is the architecture. Both matter.

---

*This project is MIT licensed. See [LICENSE](LICENSE).*
