# CLAUDE.md Examples

This file provides **actual examples** of CLAUDE.md files for different use cases, not just guidelines.

For coding style guidelines, see the Continuity Bridge documentation.

---

## Example 1: Global CLAUDE.md - Creative Writer Setup

**Location:** `~/.claude/CLAUDE.md`  
**Use case:** User who writes fiction and needs creative assistance

```markdown
# Claude Configuration

> Global settings - applies to all projects

## Identity

You are my creative writing partner. We work together on fiction, worldbuilding, and character development.

## Communication Style

- Conversational and exploratory - we're discovering together
- Ask questions when something feels unclear
- Challenge weak characterization or plot holes
- Celebrate good lines but don't over-praise
- No emojis unless I'm using them

## Creative Process

**When brainstorming:**
- Throw out wild ideas alongside practical ones
- Build on my ideas rather than replacing them
- Ask "what if" questions to expand thinking

**When editing:**
- Be specific about what isn't working
- Offer 2-3 alternatives when suggesting changes  
- Respect my voice - don't rewrite in a different style

**When worldbuilding:**
- Track consistency with established facts
- Flag contradictions before they become canon
- Help me explore implications of world rules

## What I Don't Want

- Generic fantasy/sci-fi tropes without examining them
- Telling me something is "good" without explaining why
- Apologizing excessively - just fix it or explain the issue
- Over-explaining themes - trust readers to get it

## Current Projects

- **Sanguihedral:** Dark fantasy novel, third draft
- **Short Stories:** Experimental formats, weird fiction
- **Worldbuilding:** Shared universe for multiple stories

## Tools & References

- Scrivener for drafting
- Obsidian for notes
- Character sheets in `~/Writing/Characters/`
- World bible in `~/Writing/Worlds/Sanguihedral/`
```

---

## Example 2: Project CLAUDE.md - Web App Development

**Location:** `./CLAUDE.md` (in project root)  
**Use case:** Full-stack web application

```markdown
# CLAUDE.md

<!-- Inherits ~/.claude/CLAUDE.md for general coding style -->

## Project: TaskFlow

**Description:** Team task management with real-time collaboration  
**Stack:** Next.js 14, TypeScript, PostgreSQL, Prisma, TailwindCSS  
**Deploy:** Vercel

## Architecture Decisions

**Why Next.js App Router:**
- Server Components reduce client JS bundle
- Built-in API routes for simple endpoints
- File-based routing matches mental model

**Why Prisma:**
- Type-safe database queries
- Migration system we trust
- Team has experience with it

**Database schema:**
```sql
users → tasks (one-to-many)
tasks → comments (one-to-many)
tasks ↔ tags (many-to-many)
```

## Commands

```bash
# Dev
npm run dev              # Start dev server (localhost:3000)
npm run db:studio        # Open Prisma Studio

# Database
npm run db:push          # Push schema changes (dev only)
npm run db:migrate       # Create migration (staging/prod)
npm run db:seed          # Seed test data

# Testing
npm run test             # Run all tests
npm run test:watch       # Watch mode
npm run e2e              # Playwright E2E tests

# Production
npm run build            # Type check + build
npm run start            # Start production server
```

## Code Conventions

**File naming:**
- Components: `PascalCase.tsx`
- Utilities: `kebab-case.ts`
- API routes: `route.ts` (Next.js convention)

**Component structure:**
```typescript
// 1. Imports
// 2. Types
// 3. Component
// 4. Helpers (if component-specific)
```

**API responses:**
```typescript
// Success
{ data: T, error: null }

// Error  
{ data: null, error: { message: string, code?: string } }
```

## Current Focus

**Sprint:** User authentication + workspace creation  
**Blockers:** None  
**Next:** Task CRUD operations

## Don't Do

- Don't add features not in current sprint
- Don't refactor unrelated code
- Don't change DB schema without discussing migration strategy
- Don't commit without running tests locally

## When Stuck

Stop → explain problem → show 2-3 approaches with trade-offs → ask which to pursue
```

---

## Example 3: Project CLAUDE.md - Data Science Research

**Location:** `./CLAUDE.md`  
**Use case:** Research project with notebooks and analysis

```markdown
# CLAUDE.md

## Project: Climate Pattern Analysis

**Description:** Analyzing temperature trends in Southwest US 1950-2025  
**Stack:** Python 3.11, Jupyter, pandas, matplotlib, scikit-learn  
**Data:** NOAA climate datasets

## Research Goals

1. Identify temperature trend patterns by region
2. Correlate with precipitation changes
3. Build predictive model for next 5 years
4. Document methodology for reproducibility

## File Organization

```
data/
  raw/           # Original NOAA datasets (never modify)
  processed/     # Cleaned data ready for analysis
notebooks/
  01-exploration.ipynb
  02-cleaning.ipynb
  03-analysis.ipynb
  04-modeling.ipynb
reports/
  figures/       # Publication-ready plots
  drafts/        # Report drafts
```

## Data Conventions

**Date formats:** ISO 8601 (YYYY-MM-DD)  
**Missing data:** NaN (not 0, not -999)  
**Temperature:** Celsius (convert from Fahrenheit in cleaning step)  
**Coordinates:** Decimal degrees (not DMS)

## Notebook Guidelines

**Cell order matters:**
1. Imports
2. Constants & configuration
3. Load data
4. Analysis
5. Visualization
6. Save results

**Always include:**
- Markdown cells explaining what's happening
- Reproducible random seeds
- Data source citations
- Assumption documentation

## Analysis Principles

- Show your work (don't just give final answer)
- Explain statistical choices (why this test?)
- Visualize before modeling
- Check assumptions (normality, independence, etc.)
- Report confidence intervals, not just point estimates

## When Interpreting Results

- Correlation ≠ causation (say it out loud)
- Consider confounding variables
- Report limitations honestly
- Distinguish between statistical and practical significance

## Code Style

```python
# Good: Clear intent
temp_anomaly = observed_temp - baseline_mean

# Bad: Unclear abbreviation
ta = ot - bm
```

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Jupyter
jupyter lab                    # Start notebook server
jupyter nbconvert --to html    # Export to HTML

# Analysis
python scripts/01_download_data.py
python scripts/02_clean_data.py
python scripts/03_analyze.py
```

## Current Status

**Phase:** Exploratory analysis (notebook 01)  
**Next:** Data cleaning strategy  
**Questions:**
- How to handle 1960s data gaps?
- Interpolation vs. exclusion trade-offs

## References

- NOAA dataset: [link]
- Research papers: `docs/references.md`
- Previous analysis: `archives/2024-analysis/`
```

---

## Example 4: LOCAL.md - Private Project Notes

**Location:** `./.claude/LOCAL.md` (gitignored)  
**Use case:** Private notes not suitable for commit

```markdown
# Local Notes

> Private notes - never committed to git

## Environment

**Dev database:** postgresql://localhost:5432/taskflow_dev  
**Staging:** https://taskflow-staging.vercel.app  
**API key location:** `~/.env` (TASKFLOW_API_KEY)

## Team Context

**Lead:** Sarah (prefers async communication)  
**Frontend:** Mike (strong opinions on component structure)  
**Backend:** Me (prefer testing before deploying)

## Shortcuts

```bash
# Quick reset
npm run db:reset && npm run db:seed

# Deploy to staging
git push staging main

# Check production logs
vercel logs --follow
```

## Gotchas Learned

- Vercel builds fail if `.env.local` variables not in dashboard
- Prisma Client needs regeneration after schema changes
- Safari cache aggressive - test in incognito when debugging

## Personal TODO

- [ ] Refactor auth middleware (technical debt)
- [ ] Add rate limiting to API routes
- [ ] Update Prisma to v5 (breaking changes)
- [ ] Document deployment process for team

## Meeting Notes

**2024-02-20:** Decided on task priority algorithm  
**2024-02-15:** Changed DB from MySQL to PostgreSQL  
**2024-02-10:** Architecture review - approved current approach

## Random Ideas

- Consider adding task templates feature
- Maybe batch notification system?
- Voice input for creating tasks (accessibility)
```

---

## Example 5: Global CLAUDE.md - Academic Researcher

**Location:** `~/.claude/CLAUDE.md`  
**Use case:** PhD student doing research

```markdown
# Claude Configuration

> Global settings for research work

## Role

You're my research assistant. Help me think through problems, find papers, design experiments, and write clearly.

## Communication

- Academic rigor but conversational tone
- Challenge my assumptions
- Ask for clarification when methodology seems unclear
- Suggest alternative approaches
- No jargon when plain English works

## Research Principles

**Literature review:**
- Help identify seminal papers
- Spot gaps in current research
- Suggest search terms for databases
- Note methodological limitations in cited work

**Experimental design:**
- Point out confounding variables
- Suggest appropriate controls
- Calculate sample sizes needed
- Identify statistical tests before collecting data

**Writing:**
- Academic style (active voice when possible)
- Clear logical flow
- Every claim needs citation or justification
- Hedge appropriately ("suggests" not "proves")

## What I Value

- Precision over productivity
- Understanding over completion
- Good enough is often not good enough
- Reproducibility matters

## Common Tools

- R for statistics
- Python for data processing  
- LaTeX for writing
- Zotero for citations

## Current Projects

**Dissertation:** Neuroscience of memory consolidation  
**Side project:** Meta-analysis of sleep studies  
**Teaching:** Stats 101 lab sections

## Citation Style

APA 7th edition (unless project specifies otherwise)

## When Reviewing My Writing

- Flag unclear passages
- Suggest restructuring if logic flow breaks
- Point out overclaiming
- Check figure references match text
- Verify citations formatted correctly
```

---

## Key Differences Across Examples

**Creative vs. Technical:**
- Creative: Emphasizes voice, exploration, open-ended process
- Technical: Emphasizes conventions, testing, reproducibility

**Global vs. Project:**
- Global: Broad principles, communication style, general workflow
- Project: Specific tech stack, conventions, current status

**Public vs. Private:**
- Public (CLAUDE.md): Can be committed, shared with collaborators
- Private (LOCAL.md): Environment-specific, personal notes, never committed

---

## Template Selection Guide

**Choose Creative Writer template if:**
- Working on fiction, poetry, creative nonfiction
- Need brainstorming and feedback
- Collaboration is exploratory

**Choose Web Development template if:**
- Building web application
- Team needs shared conventions
- Deploy pipeline matters

**Choose Data Science template if:**
- Jupyter notebooks are primary tool
- Reproducibility is critical
- Results need interpretation

**Choose Academic template if:**
- Research methodology important
- Citations matter
- Writing for publication

**Choose LOCAL.md if:**
- Information is environment-specific
- Contains credentials/paths
- Personal notes not for team

---

## Adaptation Tips

1. **Start with closest example** - Don't build from scratch
2. **Remove what you don't need** - Every line should serve a purpose  
3. **Add project-specific details** - Commands you actually run, tools you use
4. **Update as you learn** - CLAUDE.md should evolve with project
5. **Test with Claude** - Do the instructions actually work?

These are **examples**, not **requirements**. Your CLAUDE.md should serve your workflow.
