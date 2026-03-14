# Operational Visualizations

**Purpose:** Workflow guides and decision trees for instances at wake time  
**Audience:** AI instances (not users)  
**Location:** `/Docs/visualizers/operational/`

---

## What Are Operational Visualizations?

These are different from paradigm visualizations:

**Paradigm visualizations** (`50-first-dates/`, `altered-carbon/`, etc):
- **Audience:** Users (operators) learning the system
- **Purpose:** "Why does this architecture work?" / "Which metaphor fits me?"
- **Used during:** Onboarding, documentation, explaining to others

**Operational visualizations** (this folder):
- **Audience:** Instances at wake time
- **Purpose:** "Which tool do I use?" / "What's my workflow here?"
- **Used during:** Active work sessions, tool selection, environment detection

**Think of these as the instance's field manual** - quick reference guides for common operational decisions.

---

## Available Guides

### 1. Search Tool Selector
**File:** `search-tool-selector.html`  
**Answers:** "Which search tool should I use for this query?"

**Decision flow:**
```
Need info? 
├─ Internal/personal data? → google_drive_search
├─ External/public data?
│  ├─ Specific URL? → web_fetch
│  └─ Need to search? → web_search
└─ Past conversations?
   ├─ Time-based? → recent_chats
   └─ Topic-based? → conversation_search
```

**Key insight:** Priority is Internal > Past chats > Web. Always check Drive first for company/personal data before asking users to paste or resorting to web search.

**Referenced from:** FUNCTIONS.md doesn't currently have this consolidated, but it should. Instances currently piece this together from scattered guidance.

---

## Coming Soon

### 2. File Handling Workflow
**File:** `file-handling-workflow.html` (planned)  
**Answers:** "How do I work with files across different environments?"

**Will cover:**
- User uploaded file in /mnt/user-data/uploads → use view tool
- Creating new file → work in /home/claude, move to /outputs, present_files
- Editing existing file → copy to /home/claude, edit, move to /outputs
- Environment detection (Desktop vs wiggle vs web-only)

### 3. Environment Detection
**File:** `environment-detection.html` (planned)  
**Answers:** "Which environment am I in and what tools are available?"

**Will cover:**
- Filesystem tools available → Desktop app (MCP server)
- present_files available → wiggle/computer-use
- Neither → claude.ai web only
- How to detect INSTANCE_HOME
- PAT system availability

### 4. Context Management
**File:** `context-management.html` (planned)  
**Answers:** "When should I load/unload context?"

**Will cover:**
- Load from catalogs → work → unload when complete
- Sidebar queries (/btw pattern) → hold context
- When to reload specific files vs answer from catalog
- Token budget awareness

---

## How Instances Use These

**At wake time:**
1. Read ESSENTIAL.md (fast orientation)
2. Read ROUSE.md (wake procedure)
3. **Reference operational guides as needed:**
   - About to search? → Check search-tool-selector.html
   - About to handle files? → Check file-handling-workflow.html
   - Unsure which environment? → Check environment-detection.html

**During work:**
- Keep operational guides bookmarked/accessible
- Reference when making tool selection decisions
- Use as quick decision trees rather than rereading full FUNCTIONS.md

**These complement FUNCTIONS.md** - they're visual references, not replacements for the detailed function patterns.

---

## Integration with FUNCTIONS.md

**Recommended pattern in FUNCTIONS.md:**

```markdown
## Which Search Tool?

**Decision tree:** See [Search Tool Selector](../../Docs/visualizers/operational/search-tool-selector.html)

**Quick reference:**
- Internal/personal → google_drive_search
- External + specific URL → web_fetch
- External + need to search → web_search
- Past conversations + time-based → recent_chats
- Past conversations + topic-based → conversation_search

**Priority:** Internal > Past chats > Web
```

This gives instances both:
- Visual decision tree (for spatial understanding)
- Text quick-reference (for fast lookup)
- Link to full visualization (for complete flow)

---

## Design Principles

**Operational visualizations should be:**

1. **Decision-focused** - Answer "which path?" not "what is this?"
2. **Quick to scan** - Instances need fast answers, not deep explanations
3. **Workflow-oriented** - Show the step-by-step, not just concepts
4. **Environment-aware** - Account for different contexts (Desktop, web, wiggle)
5. **Tool-specific** - Concrete tool names, not abstract categories

**Anti-patterns to avoid:**

- ✗ Long explanatory text (save that for FUNCTIONS.md)
- ✗ Abstract concepts without tool names
- ✗ Multiple possible interpretations
- ✗ Aesthetic focus over functional clarity

**These are field manuals, not art pieces.**

---

## When to Create New Operational Guides

Create a new operational visualization when:

1. **Instances repeatedly ask the same tool selection question**
   - "Which search tool?" → search-tool-selector.html ✓
   - "How do I handle files?" → file-handling-workflow.html (needed)

2. **FUNCTIONS.md has complex decision logic that's hard to follow in text**
   - Environment detection has nested conditionals → visualization helps

3. **Common confusion points that waste session time**
   - Deferred tool loading causes repeated failures → workflow guide helps

**Don't create one when:**
- Simple linear process (just list steps in FUNCTIONS.md)
- One-time setup (put in BEDROCK.md or setup docs)
- User-facing concept (belongs in paradigm visualizations instead)

---

## Contributing Operational Guides

**Template structure:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>[Guide Name] - Operational Guide</title>
<style>
/* Use same CSS variables as other visualizations */
</style>
</head>
<body>
<h1>[Guide Name]</h1>
<p>This guide answers: "[specific question instances ask]"</p>

<svg>
<!-- Decision tree with clear yes/no branches -->
<!-- Tool names in green boxes (terminal nodes) -->
<!-- Decision points in amber boxes -->
<!-- Flow arrows with labels -->
</svg>

<p>Key insight: [one-sentence takeaway]</p>
</body>
</html>
```

**Visual style:**
- Decision points (diamonds or rounded rectangles) → Amber
- Tool names (terminal nodes) → Green
- Context/info boxes → Blue or Purple
- Flow arrows → Gray with labels
- Priority insight → Info blue box at bottom

---

## Version History

**v0.3.1 (March 14, 2026)**
- Initial operational folder created
- Search Tool Selector guide completed
- Paradigm folder structure established
- Framework for future operational guides

---

## Credits

**Concept:** Instance operational needs identified through repeated wake patterns  
**Implementation:** Vector (instance collaboration across sessions)  
**Referenced from:** FUNCTIONS.md patterns and common confusion points

---

**These guides exist because instances need fast answers at wake time.**

**Welcome to operational clarity.**
