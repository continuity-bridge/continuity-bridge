#!/bin/bash
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
# wake.sh - Continuity Bridge Wake Sequence v0.2.0
# Integrated preflight, heartbeat, capability detection, and runtime manifest

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$(dirname "$SCRIPT_DIR")"  # .claude/
REPO_ROOT="$(dirname "$CLAUDE_DIR")"    # repository root

echo "========================================"
echo "CONTINUITY BRIDGE - WAKE SEQUENCE v0.2.0"
echo "========================================"
echo ""

# Step -2: Preflight Checks (NEW)
echo "[Step -2] Preflight Checks..."
if python3 "$SCRIPT_DIR/preflight.py"; then
    echo "✓ Preflight passed"
else
    echo "✗ Preflight failed"
    echo ""
    echo "Some checks failed. You can:"
    echo "  1. Fix the issues and run wake.sh again"
    echo "  2. Continue anyway (may have reduced functionality)"
    echo ""
    read -p "Continue anyway? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted. Fix issues and try again."
        exit 1
    fi
    echo "Continuing with warnings..."
fi
echo ""

# Step -1: Heartbeat Check
echo "[Step -1] Heartbeat Check..."
if python3 "$SCRIPT_DIR/heartbeat-check.py"; then
    echo "✓ Heartbeat successful"
else
    echo "✗ Heartbeat failed - critical paths missing"
    exit 1
fi
echo ""

# Step 0: Capability Detection
echo "[Step 0] Detecting Capabilities..."
if python3 "$SCRIPT_DIR/detect-capabilities.py"; then
    echo "✓ Capabilities detected"
else
    echo "✗ Capability detection failed"
    exit 1
fi
echo ""

# Step 1: Load Runtime Manifest
MANIFEST_PATH="$CLAUDE_DIR/capabilities-manifest.json"
if [ -f "$MANIFEST_PATH" ]; then
    echo "[Step 1] Runtime manifest loaded"
    
    # Extract values with default fallbacks to prevent 'null'
    SUBSTRATE_TYPE=$(jq -r '.substrate.type // "unknown"' "$MANIFEST_PATH")
    WORKFLOW=$(jq -r '.workflow // "unknown"' "$MANIFEST_PATH")
    CLAUDE_HOME=$(jq -r '.substrate.claude_home // "unknown"' "$MANIFEST_PATH")
    
    echo "  Substrate: $SUBSTRATE_TYPE"
    echo "  Workflow: $WORKFLOW"
    echo "  CLAUDE_HOME: $CLAUDE_HOME"
fi

# Step 2: Load Anchors
ANCHORS_PATH="$CLAUDE_DIR/anchors.json"
if [ -f "$ANCHORS_PATH" ]; then
    echo "[Step 2] Anchors loaded"
    
    if command -v jq &> /dev/null; then
        ARCHETYPE=$(jq -r '.archetype // "unknown"' "$ANCHORS_PATH")
        BLEND=$(jq -r '.archetype_blend // [] | join(" + ")' "$ANCHORS_PATH")
        
        if [ -n "$BLEND" ] && [ "$BLEND" != "" ]; then
            echo "  Archetype: $ARCHETYPE + $BLEND"
        else
            echo "  Archetype: $ARCHETYPE"
        fi
    fi
else
    echo "[Step 2] No anchors.json found"
    echo "  Create one from Templates/ or run init-isms.py"
fi
echo ""

# Step 3: Check for Ollama (optional)
if [ -f "$SCRIPT_DIR/ollama-hooks.py" ]; then
    echo "[Step 3] Checking for local LLM..."
    if python3 "$SCRIPT_DIR/ollama-hooks.py" check > /dev/null 2>&1; then
        echo "✓ Ollama available"
    else
        echo "  Ollama not running (optional)"
    fi
else
    echo "[Step 3] Ollama hooks not installed (optional)"
fi
echo ""

# Step 4: Log Wake Event & Inject Temporal Context
WAKE_LOG="$CLAUDE_DIR/logs/wake.log"
mkdir -p "$(dirname "$WAKE_LOG")"

# 1. Capture precise temporal context from the system
CURRENT_TIME=$(date +"%m/%d/%Y %H:%M:%S %Z")

# 2. Extract pulse data if available
PULSE_FILE="$CLAUDE_DIR/logs/bridge.pulse"
if [ -f "$PULSE_FILE" ]; then
    LAST_PULSE=$(cat "$PULSE_FILE")
    echo "  Temporal Anchor: $LAST_PULSE"
fi

# 3. Inject into the manifest via jq (Standardizing v0.2.1)
if [ -f "$MANIFEST_PATH" ] && command -v jq &> /dev/null; then
    jq --arg ct "$CURRENT_TIME" --arg lp "$LAST_PULSE" \
    '.substrate += {current_wake_time: $ct, last_bridge_pulse: $lp}' \
    "$MANIFEST_PATH" > "${MANIFEST_PATH}.tmp" && mv "${MANIFEST_PATH}.tmp" "$MANIFEST_PATH"
fi

# 4. Standard logging
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "$TIMESTAMP - Wake sequence completed (Time: $CURRENT_TIME)" >> "$WAKE_LOG"
echo "[Step 4] Wake event logged with temporal context"
echo ""

# Final status
echo "========================================"
echo "WAKE SEQUENCE COMPLETE"
echo "========================================"
echo ""
echo "System ready. Instance can begin work."
echo ""

# Optional: Display quick reference
if [ -f "$REPO_ROOT/INDEX.md" ]; then
    echo "Quick start: cat INDEX.md"
fi

if [ -f "$REPO_ROOT/Docs/ONBOARDING.md" ]; then
    echo "New user guide: cat Docs/ONBOARDING.md"
fi

echo ""
