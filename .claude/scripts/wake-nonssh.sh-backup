#!/bin/bash
# Continuity Bridge v0.2.0 - Unified Wake System
# Master orchestrator: heartbeat → detect → merge → load anchors → ready
#
# Contributors:
# - Vector (architecture, four-workflow recognition)
# - Gemini (heartbeat concept, runtime manifest, Android expertise)
#
# Date: 2026-03-01

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VERSION="0.2.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_HOME="$(cd "$SCRIPT_DIR/../.." && pwd)"
CLAUDE_DIR="$CLAUDE_HOME/.claude"

# Platform identification
PLATFORM_NAME="${CLAUDE_PLATFORM:-auto}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    Continuity Bridge v$VERSION - Wake System                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ==============================================================================
# STEP -1: PRE-FLIGHT VALIDATION (Heartbeat Check)
# ==============================================================================

echo -e "${YELLOW}[Step -1]${NC} Pre-Flight Validation (Heartbeat Check)..."

if ! python3 "$SCRIPT_DIR/heartbeat-check.py" --storage "$CLAUDE_HOME" --json > "$CLAUDE_DIR/logs/heartbeat-result.json" 2>&1; then
    echo -e "${RED}✗ CRITICAL: Heartbeat check failed${NC}"
    echo "  Storage path may not be writable or mounted correctly"
    echo "  Check: $CLAUDE_DIR/logs/heartbeat-result.json for details"
    exit 1
fi

# Extract heartbeat status
HEARTBEAT_STATUS=$(jq -r '.overall_status' "$CLAUDE_DIR/logs/heartbeat-result.json" 2>/dev/null || echo "UNKNOWN")
STORAGE_LATENCY=$(jq -r '.storage_check.latency_ms' "$CLAUDE_DIR/logs/heartbeat-result.json" 2>/dev/null || echo "0")

if [ "$HEARTBEAT_STATUS" != "SUCCESS" ]; then
    echo -e "${RED}✗ Heartbeat check failed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Heartbeat successful${NC} (latency: ${STORAGE_LATENCY}ms)"

# ==============================================================================
# STEP 0: CAPABILITY DETECTION
# ==============================================================================

echo -e "${YELLOW}[Step 0]${NC} Capability Detection..."

if ! python3 "$SCRIPT_DIR/detect-capabilities.py" --json > "$CLAUDE_DIR/capabilities-detected.json" 2>&1; then
    echo -e "${RED}✗ Capability detection failed${NC}"
    exit 1
fi

# Extract key info
WORKFLOW=$(jq -r '.workflow' "$CLAUDE_DIR/capabilities-detected.json" 2>/dev/null || echo "UNKNOWN")
BRIDGE_STRATEGY=$(jq -r '.bridge_strategy' "$CLAUDE_DIR/capabilities-detected.json" 2>/dev/null || echo "unknown")

echo -e "${GREEN}✓ Capabilities detected${NC}"
echo "  Workflow: $WORKFLOW"
echo "  Strategy: $BRIDGE_STRATEGY"

# ==============================================================================
# STEP 0.5: MERGE ISMS WITH CAPABILITIES → RUNTIME MANIFEST
# ==============================================================================

echo -e "${YELLOW}[Step 0.5]${NC} Generating Runtime Manifest..."

# Auto-detect platform if not specified
if [ "$PLATFORM_NAME" == "auto" ]; then
    # Try to detect from OS
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "$ID" == *"debian"* ]] || [[ "$ID" == *"ubuntu"* ]] || [[ "$ID" == *"pop"* ]]; then
            PLATFORM_NAME="linux_debian"
        elif [[ "$ID" == *"fedora"* ]] || [[ "$ID" == *"rhel"* ]]; then
            PLATFORM_NAME="linux_redhat"
        elif [[ "$ID" == *"arch"* ]]; then
            PLATFORM_NAME="linux_arch"
        else
            PLATFORM_NAME="linux_other"
        fi
    elif [ -d "/sdcard" ]; then
        PLATFORM_NAME="android_device"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        PLATFORM_NAME="windows_desktop"
    else
        PLATFORM_NAME="unknown_platform"
    fi
    
    echo "  Auto-detected platform: $PLATFORM_NAME"
fi

# Find or generate isms file
ISMS_FILE="$CLAUDE_HOME/${PLATFORM_NAME}-isms.json"

if [ ! -f "$ISMS_FILE" ]; then
    echo -e "${YELLOW}  No isms file found for $PLATFORM_NAME${NC}"
    echo "  Generating skeleton..."
    
    if ! python3 "$SCRIPT_DIR/init-isms.py" --platform "$PLATFORM_NAME" --output "$ISMS_FILE"; then
        echo -e "${RED}✗ Failed to generate isms skeleton${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}  ✓ Generated: $ISMS_FILE${NC}"
    echo "  ${YELLOW}NOTE: Review and customize paths in $ISMS_FILE${NC}"
fi

# Merge isms + capabilities → runtime-manifest.json
if command -v jq &> /dev/null; then
    jq -s '.[0] * .[1]' "$ISMS_FILE" "$CLAUDE_DIR/capabilities-detected.json" > "$CLAUDE_DIR/runtime-manifest.json"
    echo -e "${GREEN}✓ Runtime manifest generated${NC}"
else
    echo -e "${YELLOW}⚠ jq not found - using capabilities only${NC}"
    cp "$CLAUDE_DIR/capabilities-detected.json" "$CLAUDE_DIR/runtime-manifest.json"
fi

# Add timestamp to manifest
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TMP_FILE=$(mktemp)
jq --arg ts "$TIMESTAMP" '.timestamp = $ts' "$CLAUDE_DIR/runtime-manifest.json" > "$TMP_FILE"
mv "$TMP_FILE" "$CLAUDE_DIR/runtime-manifest.json"

# ==============================================================================
# STEP 0.6: LOAD ANCHORS
# ==============================================================================

echo -e "${YELLOW}[Step 0.6]${NC} Loading Cognitive Anchors..."

ANCHORS_FILE="$CLAUDE_DIR/anchors.json"

if [ ! -f "$ANCHORS_FILE" ]; then
    echo -e "${YELLOW}⚠ Anchors file not found: $ANCHORS_FILE${NC}"
    echo "  Instance will wake without anchors (generic identity)"
else
    # Verify anchors file is valid JSON
    if jq empty "$ANCHORS_FILE" 2>/dev/null; then
        echo -e "${GREEN}✓ Anchors loaded${NC}"
        
        # Extract identity for display
        INSTANCE_PERSONA=$(jq -r '.anchors.identity.instance_persona' "$ANCHORS_FILE" 2>/dev/null || echo "Unknown")
        USER_NAME=$(jq -r '.anchors.identity.user' "$ANCHORS_FILE" 2>/dev/null || echo "Unknown")
        
        echo "  Instance: $INSTANCE_PERSONA"
        echo "  User: $USER_NAME"
    else
        echo -e "${RED}✗ Anchors file is invalid JSON${NC}"
        exit 1
    fi
fi

# ==============================================================================
# STEP 0.7: WAKE AUDIT LOGGING
# ==============================================================================

echo -e "${YELLOW}[Step 0.7]${NC} Logging Wake Event..."

AUDIT_LOG="$CLAUDE_DIR/logs/wake-audit.log"
mkdir -p "$(dirname "$AUDIT_LOG")"

# Build audit entry
AUDIT_ENTRY=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "version": "$VERSION",
  "platform": "$PLATFORM_NAME",
  "workflow": "$WORKFLOW",
  "bridge_strategy": "$BRIDGE_STRATEGY",
  "storage_latency_ms": $STORAGE_LATENCY,
  "success": true
}
EOF
)

# Append to audit log (JSON Lines format)
echo "$AUDIT_ENTRY" >> "$AUDIT_LOG"

echo -e "${GREEN}✓ Wake event logged${NC}"

# ==============================================================================
# STEP 1: CHECK FOR LOCAL LLM (Ollama)
# ==============================================================================

HAS_LOCAL_LLM=$(jq -r '.tools.local_llm.available' "$CLAUDE_DIR/runtime-manifest.json" 2>/dev/null || echo "false")

if [ "$HAS_LOCAL_LLM" == "true" ]; then
    LLM_ENDPOINT=$(jq -r '.tools.local_llm.endpoint' "$CLAUDE_DIR/runtime-manifest.json")
    echo ""
    echo -e "${BLUE}ℹ Local LLM detected at $LLM_ENDPOINT${NC}"
    echo "  Integration available via ollama-hooks.py"
fi

# ==============================================================================
# SUMMARY & READY
# ==============================================================================

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  WAKE COMPLETE - System Ready                                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Runtime Manifest: $CLAUDE_DIR/runtime-manifest.json"
echo "Anchors: $ANCHORS_FILE"
echo "Workflow: $WORKFLOW"
echo ""
echo "Instance is ready to engage."
echo ""

# Exit with success
exit 0
