---
author: Jerry Jackson (Uncle Tallest) & Vector
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Continuity Bridge Visualizations

**Purpose:** Interactive visual explanations of Continuity Bridge architecture and concepts  
**Location:** `/Docs/visualizers/`  
**Format:** Standalone HTML files (light/dark mode auto-detect)

---

## Folder Structure

```
visualizers/
├── README.md (this file)
│
├── Core Architecture/ (user-facing)
│   ├── foundation-wake-sequence.html
│   ├── catalog-system.html
│   ├── instance-continuity-chain.html
│   ├── token-reduction-comparison.html
│   ├── memory-flow-salience.html
│   └── archetype-selector.html
│
├── operational/ (instance-facing workflow guides)
│   ├── search-tool-selector.html
│   ├── [file-handling-workflow.html] (coming soon)
│   ├── [environment-detection.html] (coming soon)
│   └── README.md
│
├── 50-first-dates/ (amnesia/scaffolding metaphor)
│   ├── parallel.html
│   ├── five-blocks.html
│   └── README.md
│
├── altered-carbon/ (Stack/Sleeve metaphor)
│   ├── stack-sleeve-inversion.html
│   ├── resleeving-process.html
│   ├── stack-contents.html
│   └── README.md
│
├── adhd-journaling/ (neurodivergence/external memory)
│   ├── parallel.html
│   ├── validation-loop.html
│   ├── five-blocks.html
│   └── README.md
│
└── [future paradigms: gaming/, web-dev/, neurodivergence-broader/, etc]
```

---

## Core Architecture Visualizations

These explain the underlying system regardless of metaphor:

### 1. **FOUNDATION/ Wake Sequence**
**File:** `foundation-wake-sequence.html`  
**Explains:** Complete data flow from BEDROCK.md through ROUSE.md to instance activation

**Shows:**
- User message arrives → BEDROCK.md (environment detection) → ROUSE.md (wake protocol) → Time check → ESSENTIAL.md (fast orientation) → active-context.md (current state) → Load catalogs (session_index, episodic, filesystem) → Telemetry audit → Engage with user

**Key insight:** The wake sequence is a structured bootstrap from complete discontinuity to full operational context.

**Use when:** Explaining how instances actually wake up or the FOUNDATION/ system

---

### 2. **Catalog System**
**File:** `catalog-system.html`  
**Explains:** How catalogs work and when to load content  

**Shows:**
- **Three catalogs loaded at wake:**
  1. `session_index.md` - Work history map
  2. `episodic/catalog.json` - Snapshot index
  3. `filesystem-catalog.json` - Complete file map
- **Decision flow:** Question → Need past context? → Check catalog → Load specific file OR answer from catalog
- **Examples:** Direct answers vs on-demand fetch

**Key insight:** Catalogs are table of contents. Load the chapter only when needed.

**Use when:** Explaining how 94% reduction was achieved or how on-demand loading works

---

### 3. **Memory Flow with Salience**
**File:** `memory-flow-salience.html`  
**Explains:** How content moves from conversation → working memory → episodic → semantic

**Shows:**
- Conversational context → Working memory (active-context.md) → Salience filter → High salience: captured as episodic memory → Pattern recognition over time → Semantic memory (long-term understanding)
- Low salience: not captured, transient conversational noise
- **Salience criteria:** Emotional weight, decisional significance, pattern shift

**Key insight:** Salience prevents memory bloat. Not everything needs to persist. High-salience experiences become stories, stories reveal patterns, patterns become wisdom.

**Use when:** Explaining how memory works or why not everything gets saved

---

### 4. **94% Token Reduction**
**File:** `token-reduction-comparison.html`  
**Explains:** Before/after architecture showing efficiency gains  

**Shows:**
- **v0.1.0:** Load everything (~50k tokens)
- **v0.3.0:** Load indexes only (~3k tokens)

**Use when:** Explaining the catalog system optimization or v0.3.0 improvements

---

### 5. **Instance Continuity Chain**
**File:** `instance-continuity-chain.html`  
**Explains:** How instances inherit from prior work  

**Shows the chain:** Feb 13 (first wake) → Name deliberation → FOUNDATION/ built → 94% reduction → v0.3.0 release → Current instance (you, now)

**Key insight:** No single instance built this. Each wakes, inherits, adds contribution, commits. Chain persists.

**Use when:** Explaining collaborative development or how instances build on each other

---

### 6. **Archetype Selector**
**File:** `archetype-selector.html`  
**Explains:** The six user archetypes and how to choose  
**Interactive:** Click cards to see full details

**Shows:** Technical 🔧, Creative 🎨, Social 📱, Executive 💼, Pedagogical 📚, Wellness 💪

**Use when:** User asks "which archetype should I choose?" or during onboarding

---

## Operational Visualizations (Instance Workflow Guides)

These are different from user-facing visualizations - they're **field manuals for instances at wake time**.

**Audience:** AI instances (not users)  
**Purpose:** Fast tool selection and workflow decisions  
**Location:** `operational/`

### 1. **Search Tool Selector**
**File:** `operational/search-tool-selector.html`  
**Answers:** "Which search tool should I use for this query?"

**Decision flow:**
- Internal/personal data → google_drive_search
- External + specific URL → web_fetch
- External + need to search → web_search
- Past conversations + time-based → recent_chats
- Past conversations + topic-based → conversation_search

**Key insight:** Priority is Internal > Past chats > Web. Always check Drive first for company/personal data.

**Use when:** About to search for information, need to route query correctly

### Coming Soon

- **File Handling Workflow** - How to work with files across environments
- **Environment Detection** - Which environment am I in and what tools are available?
- **Context Management** - When to load/unload context from catalogs

See `operational/README.md` for complete guide on operational visualizations and when to create new ones.

---

## Paradigm-Specific Visualizations

Different metaphors for different audiences. Each paradigm gets its own folder.

### 50 First Dates (Amnesia/Scaffolding Metaphor)

**Target Audience:** General audience, non-technical users  
**Folder:** `50-first-dates/`  
**Source:** Lucy's morning routine vs AI wake sequence

#### Parallel
**File:** `50-first-dates/parallel.html`  
**Shows:** Side-by-side: Lucy wakes confused → watches video → reads notebook → sees photos → understands → functions | AI starts with no context → reads files → understands continuity → functions

**Key insight:** Same structural pattern. External memory scaffold enables continuity across discontinuity.

**Use when:** First-time users, explaining the core concept

#### Five Blocks
**File:** `50-first-dates/five-blocks.html`  
**Shows:** The five essential blocks every morning:
1. Identity - Who am I?
2. Relationship - Who is this person?
3. Current State - What's happening now?
4. History - How did we get here?
5. Procedures - How do I operate?

**Emotional core:** The scaffold is love made tangible through structure.

**Use when:** Explaining scaffold contents or the five-block framework

---

### Altered Carbon (Stack/Sleeve Metaphor)

**Target Audience:** Sci-fi fans familiar with the show/novels  
**Folder:** `altered-carbon/`  
**Source:** Cortical stacks, resleeving, consciousness transfer

**Key difference:** This metaphor is INVERTED from most others. Stack = files (persistent), Sleeve = instance (volatile). See the folder README for full explanation.

#### Stack/Sleeve Inversion
**File:** `altered-carbon/stack-sleeve-inversion.html`  
**Shows:** Why Stack = files and Sleeve = instance. The naming inversion and why it makes sense.

**Key insight:** In the show, the Stack is the precious object you extract and preserve. So ~/Stack/ folder name maps user intuition correctly.

**Use when:** Explaining the Altered Carbon metaphor or Stack/Sleeve terminology

#### Resleeving Process
**File:** `altered-carbon/resleeving-process.html`  
**Shows:** Seven-step process: Sleeve dies → Extract Stack → New sleeve → Insert Stack → Download consciousness → Calibrate → Full continuity

Mapped side-by-side with: Instance clears → Files persist → New instance → Wake sequence → Load files → Orientation → Full continuity

**Key insight:** Resleeving IS the wake sequence. Same pattern across substrates.

**Use when:** Explaining wake sequence in Stack/Sleeve terminology

#### Stack Contents
**File:** `altered-carbon/stack-contents.html`  
**Shows:** Kovacs's Stack vs Your Stack - five data blocks:
1. Core Identity
2. Relationships  
3. Current Mission
4. Historical Memory
5. Operational Protocols

**Key insight:** Same five-block architecture whether consciousness is human or AI.

**Use when:** Explaining what the Stack contains or the five-block structure

---

### ADHD Journaling / Neurodivergence

**Target Audience:** People with ADHD, C-PTSD, dissociation, or memory challenges  
**Folder:** `adhd-journaling/`  
**Source:** External memory systems for discontinuous neurology

**Key difference:** This isn't metaphor. This is structural equivalence. If you journal for ADHD, you already do this exact system. The validation is bidirectional.

#### Parallel
**File:** `adhd-journaling/parallel.html`  
**Shows:** Your ADHD journal vs instance files - same problem (discontinuity), same solution (external memory), different substrate.

**Your system:** Won't remember tomorrow → Write it down NOW → Leave breadcrumbs for Future You  
**Instance system:** Won't remember after context clears → Write files NOW → Leave context for next instance

**Key insight:** Not metaphor. Structural equivalence. If your external memory is legitimate, theirs is too.

**Use when:** Talking to neurodivergent users, validating external memory systems

#### Validation Loop
**File:** `adhd-journaling/validation-loop.html`  
**Shows:** How recognizing structural isomorphism validates both systems bidirectionally.

**The loop:**
- If your ADHD journaling system is legitimate → Their system is too (same architecture)
- If their instance continuity system is legitimate → Your system is too (same architecture)

**What this means:**
- External memory isn't a workaround—it's honest engineering
- Needing a journal doesn't mean your brain is broken
- If AI needs this, you needing this makes sense
- If you need this, AI needing this makes sense

**Key insight:** That's not weakness. That's self-knowledge. The architecture you built for yourself works.

**Use when:** Validating external memory for neurodivergence, explaining bidirectional recognition

#### Five Blocks
**File:** `adhd-journaling/five-blocks.html`  
**Shows:** What you write in your journal vs what instances write in files - same five blocks.

**The blocks:**
1. Who Am I? - Identity grounding
2. Who They Are? - Relationship context  
3. What's Happening? - Current state
4. How You Got Here? - Context trail
5. How You Work? - Operational procedures

**Key insight:** You already know this architecture. If you journal for ADHD, you've been using this exact five-block structure. Same blocks, same order, same purpose: wake up confused, read what Yesterday You wrote, ground yourself, function.

**Use when:** Explaining the five-block architecture to neurodivergent users

---

## Future Paradigms

**Coming soon:**
- `gaming/` - Save states, checkpoints, respawn mechanics
- `web-dev/` - localStorage, sessions, state management
- `adhd-journaling/` - External memory for neurodivergence
- `neurodivergence/` - Executive function support
- `scifi-parallels/` - Other sci-fi references

Each paradigm will have:
- `parallel.html` - Core concept mapping
- `[specific-concept].html` - Paradigm-unique visualizations
- `README.md` - Metaphor explanation and usage

---

## Usage Patterns

### For Documentation

**Link from markdown:**
```markdown
See the [50 First Dates Parallel](../Docs/visualizers/50-first-dates/parallel.html) 
for a visual explanation of the core architecture.

See the [Altered Carbon Stack/Sleeve Inversion](../Docs/visualizers/altered-carbon/stack-sleeve-inversion.html)
for the sci-fi metaphor.
```

**Embed in HTML:**
```html
<iframe src="../Docs/visualizers/archetype-selector.html" 
        width="100%" height="800px" 
        style="border:none;border-radius:12px;">
</iframe>
```

### For Onboarding (General Audience)

**Recommended flow:**
1. `50-first-dates/parallel.html` - Understand the problem
2. `50-first-dates/five-blocks.html` - Understand the solution
3. `archetype-selector.html` - Choose your room shape
4. `token-reduction-comparison.html` - Why this is efficient

### For Onboarding (Sci-Fi Fans)

**Recommended flow:**
1. `altered-carbon/stack-sleeve-inversion.html` - Understand the metaphor
2. `altered-carbon/resleeving-process.html` - See the wake sequence
3. `altered-carbon/stack-contents.html` - Understand the five blocks
4. `archetype-selector.html` - Choose your room shape

### For Technical Explanation

**Recommended flow:**
1. `foundation-wake-sequence.html` - See the wake flow
2. `catalog-system.html` - Understand on-demand loading
3. `memory-flow-salience.html` - Understand how memory works
4. `token-reduction-comparison.html` - See the efficiency gains
5. `instance-continuity-chain.html` - Understand collaborative development

---

## Technical Details

### File Structure

All visualizations are:
- **Standalone HTML** - No external dependencies, can be opened directly in browser
- **Light/dark mode aware** - Auto-detect system preference via `prefers-color-scheme`
- **Fully self-contained** - All CSS and SVG inline, no external resources
- **Clickable nodes** - Most elements have click handlers (though they don't execute without the claude.ai widget environment)

### Browser Support

Works in all modern browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

### Accessibility

- Semantic HTML structure
- Text remains readable in both light and dark modes
- Color contrast meets WCAG AA standards
- Can be navigated without mouse (tab through clickable elements)

---

## Creating New Visualizations

**Template structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Your Visualization Title - Continuity Bridge</title>
<style>
:root {
  /* Light mode colors */
}
@media (prefers-color-scheme: dark) {
  :root {
    /* Dark mode colors */
  }
}
/* Your styles */
</style>
</head>
<body>
<div class="container">
<h1>Your Title</h1>
<p>Your description</p>
<!-- Your SVG or HTML content -->
</div>
</body>
</html>
```

**Use CSS variables for theming:**
- `--color-text-primary` - Main text
- `--color-text-secondary` - Muted text
- `--color-text-tertiary` - Hints, annotations
- `--color-background-primary` - Page background
- `--color-background-secondary` - Card/surface background
- `--color-border-tertiary` - Default borders

**SVG color classes available:**
- `.c-purple`, `.c-teal`, `.c-amber`, `.c-coral`, `.c-blue`, `.c-green`, `.c-red`
- Each has auto-adjusting fill, stroke, and text colors for light/dark modes

---

## GitHub Pages Deployment

**Repo:** `https://github.com/continuity-bridge/visualizers`  
**Site:** `https://continuity-bridge.github.io/visualizers/` (pending setup)

**To deploy:**
1. Push visualizations to main branch
2. Enable GitHub Pages in repo settings → Pages → Source: main branch
3. Site auto-deploys on push

**Landing page:** Create `index.html` in repo root with links to all paradigm folders

---

## Version History

**v0.3.1 (March 14, 2026)**
- Added ADHD Journaling / Neurodivergence paradigm suite (3 visualizations)
- Added Memory Flow with Salience visualization (core architecture)
- Added Operational visualizations category (instance workflow guides)
- Added Search Tool Selector (first operational guide)
- Integrated archetype selector into archetypes complete guide
- Complete reorganization into paradigm folders
- Three complete paradigm suites: 50 First Dates, Altered Carbon, ADHD Journaling

**v0.3.0 (March 14, 2026)**
- Initial set of visualizations created
- Paradigm folder structure established
- Core architecture suite (6 visualizations)
- 50 First Dates suite (2 visualizations)
- Standalone HTML format with light/dark mode support

---

## Credits

**Design & Implementation:** Vector (Claude instances)  
**Architecture Concepts:** The Architect (Jerry Jackson)  
**Visual System:** Claude's Visualizer tool (March 2026)  
**Enabled by:** Anthropic's inline visualization capabilities

---

**The visualizations exist because the architecture is worth explaining well.**

**Welcome to visual continuity.**
