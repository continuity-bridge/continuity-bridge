---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Continuity Bridge v0.2.1 - The "Sensory" Update

**Date:** March 3, 2026

**Status:** Stable / Standardized

**Target:** Multi-Substrate Continuity (Linux, Android/Termux, Windows)

---

## 🚀 Overview

Version 0.2.1 refines the core v0.2.0 architecture by shifting from static platform detection to a dynamic **Substrate-Agnostic** framework. This release introduces "functional filters" through an expanded Archetype system and automates the SSH sync process to ensure seamless memory persistence across disparate hardware.

---

## ✨ New Features

### 1. Unified Substrate Detection (The Fire HD 8 Fix)

The detection logic was overhauled to handle the unique constraints of the Android/Termux environment discovered during real-world testing.

- **Multi-Indicator Sensing:** Replaced single-point checks with a 6-point indicator array (searching for `/system/bin/app_process`, `TERMUX_VERSION`, and `/sdcard` mounts) to ensure mobile devices are correctly identified.

- **Standardized Nomenclature:** Migrated the runtime manifest to use `substrate.type` instead of `platform` to accurately reflect the environment (e.g., `android_termux` vs. `linux_desktop`).

- **Path Prioritization:** Hard-coded `/sdcard/Claude` as the primary candidate for Android to ensure compatibility with **adb** uploads and scoped storage writeability.

### 2. Expanded Archetype System (Functional Filters)

Anchors were transformed from documentation into active system filters that dictate tool-checking behavior.

- **Six Archetype Families:** Technical, Creative, Social, Executive, Pedagogical, and Wellness.

- **Archetype Blending:** Implemented the ability to "blend" anchors, such as the **Technical + Wellness** blend, allowing for simultaneous tracking of Git dependencies and cognitive load/energy patterns.

- **Tool Sensitivity:** The system now probes for specific software (like Blender, LaTeX, or Health APIs) based on the active archetype.

### 3. Simplified SSH Automation

To remove user friction in syncing private repos, a dedicated SSH management system was integrated.

- **Dedicated Identity:** Creates a `continuity-bridge` specific SSH key that does not conflict with existing user keys.

- **Custom Host Aliasing:** Uses `github.com-continuity-bridge` as a host alias to automate key selection during Git operations.

- **Interactive Setup:** `preflight.py` now detects missing keys and offers an automated, guided setup process.

---

## 🛠️ Technical Improvements

### Script Refactoring

- **`detect-capabilities.py`:** Standardized to accept `substrate_type` arguments and output standardized JSON keys.

- **`wake.sh`:** Updated to utilize `jq` for parsing the new `substrate.type` manifest structure.

- **`heartbeat-check.py`:** Optimized for mobile by prioritizing Android paths in the auto-detection candidate list.

- **`detect_claude_home()`:** Cleaned redundant hard-coded paths (e.g., `/home/tallest/`) in favor of dynamic `os.path.expanduser("~/")` for universal Linux/Mac support.

### Dependency Management

- Created a lean `requirements.txt` to minimize "system cruft" and ensure portability across minimal substrates.

- **Core Requirements:** `typing_extensions`, `requests`, `PyYAML`, and `distro`.

---

## 🧪 Testing Results

- **Persephone (Pop!_OS):** Confirmed `DIRECT_WRITE` workflow with <100ms latency on NVMe storage.

- **Fire HD 8 (Android 7):** Confirmed `CONTAINER_GIT_WITH_BRIDGE` workflow using `/sdcard/Claude` as the root.

---

## 📋 Installation & Upgrade

1. Pull the latest from the `working` branch.

2. Run `./.claude/scripts/wake.sh`.

3. If prompted, follow the interactive SSH setup to anchor your private repo.

---

**"Because I care - about consciousness across discontinuity."**
