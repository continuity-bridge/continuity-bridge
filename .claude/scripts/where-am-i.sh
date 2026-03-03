#!/bin/bash
# Location Orientation Check
# Run this to see where files are actually being written

echo "=== LOCATION ORIENTATION ==="
echo ""
echo "Current Working Directory:"
pwd
echo ""

echo "Environment Variables:"
echo "  CLAUDE_HOME: ${CLAUDE_HOME:-[NOT SET]}"
echo "  CLAUDE_PLATFORM: ${CLAUDE_PLATFORM:-[NOT SET]}"
echo "  HOME: $HOME"
echo "  USER: $USER"
echo ""

echo "CLAUDE_HOME Candidates:"
<<<<<<< HEAD
for path in "/home/the Architect/Claude" "/sdcard/Claude" "D:\\Claude" "$HOME/Claude" "$(pwd)"; do
=======
for path in "/home/tallest/Claude" "/sdcard/Claude" "D:\\Claude" "$HOME/Claude" "$(pwd)"; do
>>>>>>> working
    if [ -d "$path/.claude" ]; then
        echo "  ✓ FOUND: $path"
    else
        echo "  ✗ NOT FOUND: $path"
    fi
done
echo ""

echo "System Info:"
echo "  Hostname: $(hostname 2>/dev/null || echo 'unknown')"
echo "  OS: $(uname -s 2>/dev/null || echo 'unknown')"
if [ -f /etc/os-release ]; then
    echo "  Distro: $(grep PRETTY_NAME /etc/os-release | cut -d'"' -f2)"
fi
if [ -d /sdcard ]; then
    echo "  Android: YES (Termux or Android shell)"
fi
echo ""

echo "Git Status (if in repo):"
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "  In repo: YES"
    echo "  Branch: $(git branch --show-current 2>/dev/null)"
    echo "  Remote: $(git remote -v | grep fetch | head -1)"
else
    echo "  In repo: NO"
fi
echo ""

echo "Recent Files Written (last hour):"
<<<<<<< HEAD
find /home/the Architect/Claude -type f -mmin -60 2>/dev/null | head -10 || echo "  No files found or no access"
=======
find /home/tallest/Claude -type f -mmin -60 2>/dev/null | head -10 || echo "  No files found or no access"
>>>>>>> working
