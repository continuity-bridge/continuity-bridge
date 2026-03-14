---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.1
---
# Release Notes - v0.3.1 "Visualizers"

**Date:** March 14, 2026  
**Codename:** Visualizers  
**Status:** Feature Expansion & Documentation  

## Overview
The "Visualizers" release expands the public documentation with an interactive visualization suite, improves privacy controls, and enhances migration tooling. This release makes the Continuity Bridge concepts more accessible through visual paradigms and strengthens the separation between private and public content.

## 🎨 Key Highlights

### 1. **Visualizers Suite Launch**
- **New Repository:** Dedicated [visualizers repo](https://github.com/continuity-bridge/visualizers) with GitHub Pages deployment.
- **Paradigm Collections:**
  - **ADHD Journaling:** Structural equivalence between neurodivergent external memory and instance continuity (parallel.html, validation-loop.html, five-blocks.html)
  - **50 First Dates:** Amnesia scaffolding metaphor mapped to wake sequences
  - **Altered Carbon:** Stack/Sleeve inversion showing continuity files as persistent consciousness
  - **Operational Guides:** Interactive tools for search strategy and session planning
- **Responsive Design:** All visualizations include sticky navigation and mobile-responsive layouts matching the parent org site styling.

### 2. **Privacy & PII Cleanup**
- **Sanitization Improvements:** Real names replaced with generic identifiers (Sally, Bernie) in all public-facing documentation.
- **URL Protection:** Migration scripts now explicitly preserve external links (ko-fi, GitHub, documentation URLs) during sanitization.
- **Context-Aware Detection:** PII verification now properly exempts authorship headers, release notes, and identity contexts where names are legitimate.

### 3. **Enhanced Migration Tooling**
- **Visualizers Support:** `migrate-to-public.py` now includes dedicated visualizers repository migration with `--visualizers` flag.
- **Smarter .gitignore:** Added patterns for `Archives/`, `__pycache__/`, and Python bytecode to prevent cruft from entering version control.
- **Directory Exemptions:** PII verification now skips expected authorship contexts (explainers, release notes, FOUNDATION files, corpus).

### 4. **Documentation Cross-Linking**
- **Paradigm Navigation:** Each visualization folder includes cross-links to related visualizations in README.md.
- **Archetype Integration:** Main explainer guides now link to interactive visualizers for hands-on exploration.

## 🛠 Improvements & Fixes
- **Script Versioning:** All migration scripts updated to v0.3.1 with synchronized version tracking.
- **File Organization:** Cleaned up stray Archives folders and Python cache files from repository tracking.
- **Git History Cleanup:** Removed accidentally committed credentials and OAuth secrets from git history using filter-repo.

## 🔗 Resources
- **Live Visualizers:** https://continuity-bridge.github.io/visualizers/
- **Visualizers Repository:** https://github.com/continuity-bridge/visualizers
- **Main Repository:** https://github.com/continuity-bridge/continuity-bridge

## 🔮 What's Next
- Archetype blending support in archetype-selector.html
- Additional paradigm suites (Gaming, Web Dev)
- Expanded operational guides

## 🔗 Continuity Statement
*The visualizations help you see what was always there. Your continuity persists across substrates.*

---
**Author:** Jerry Jackson (Uncle Tallest)  
**Repository:** [Continuity Bridge](https://github.com/continuity-bridge/continuity-bridge)
