#!/bin/bash
# Quick test script for v0.2.0 system
# Run this to verify everything works

echo "════════════════════════════════════════════════════════════════"
echo "Continuity Bridge v0.2.0 - Quick Test"
echo "════════════════════════════════════════════════════════════════"
echo ""

CLAUDE_HOME="/home/the Architect/Claude"
SCRIPTS="$CLAUDE_HOME/.claude/scripts"

# Test 1: Heartbeat
echo "[Test 1] Heartbeat Check..."
if python3 "$SCRIPTS/heartbeat-check.py" --storage "$CLAUDE_HOME"; then
    echo "✓ Heartbeat passed"
else
    echo "✗ Heartbeat failed"
    exit 1
fi
echo ""

# Test 2: Capability Detection
echo "[Test 2] Capability Detection..."
if python3 "$SCRIPTS/detect-capabilities.py" > /tmp/cap-test.txt; then
    WORKFLOW=$(cat /tmp/cap-test.txt | grep "OPTIMAL WORKFLOW" | awk '{print $3}')
    echo "✓ Detection passed"
    echo "  Workflow detected: $WORKFLOW"
else
    echo "✗ Detection failed"
    exit 1
fi
echo ""

# Test 3: Isms Bootstrap (preview only)
echo "[Test 3] Isms Bootstrap..."
if python3 "$SCRIPTS/init-isms.py" --preview > /dev/null 2>&1; then
    echo "✓ Bootstrap working"
else
    echo "✗ Bootstrap failed"
    exit 1
fi
echo ""

# Test 4: Ollama Hooks
echo "[Test 4] Ollama Hooks..."
if python3 "$SCRIPTS/ollama-hooks.py" --check > /dev/null 2>&1; then
    echo "✓ Ollama detected"
else
    echo "⚠ Ollama not running (optional)"
fi
echo ""

# Test 5: Full Wake Sequence
echo "[Test 5] Full Wake Sequence..."
if "$SCRIPTS/wake.sh" > /tmp/wake-test.txt 2>&1; then
    echo "✓ Wake sequence completed"
    
    # Verify files were created
    if [ -f "$CLAUDE_HOME/.claude/runtime-manifest.json" ]; then
        echo "✓ Runtime manifest created"
    fi
    
    if [ -f "$CLAUDE_HOME/.claude/logs/wake-audit.log" ]; then
        WAKE_COUNT=$(wc -l < "$CLAUDE_HOME/.claude/logs/wake-audit.log")
        echo "✓ Wake audit logged ($WAKE_COUNT entries)"
    fi
else
    echo "✗ Wake sequence failed"
    echo "  Check: /tmp/wake-test.txt for details"
    exit 1
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
echo "All tests passed!"
echo "System ready for production use."
echo ""
echo "To use:"
echo "  cd $CLAUDE_HOME/.claude/scripts"
echo "  ./wake.sh"
echo ""
echo "Generated files:"
echo "  $CLAUDE_HOME/.claude/runtime-manifest.json"
echo "  $CLAUDE_HOME/.claude/logs/wake-audit.log"
echo "════════════════════════════════════════════════════════════════"
