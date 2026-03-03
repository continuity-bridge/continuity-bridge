#!/bin/bash
# copy-ssh-integration.sh
# Copies all SSH integration files from outputs to your repo

set -e

OUTPUTS="/mnt/user-data/outputs"
REPO="$HOME/Claude"

echo "=== SSH Integration File Copy ==="
echo ""
echo "This will copy SSH integration files to your repo:"
echo "  From: $OUTPUTS"
echo "  To: $REPO"
echo ""
read -p "Continue? [Y/n]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ ! -z $REPLY ]]; then
    echo "Aborted."
    exit 0
fi

# Create directories if needed
mkdir -p "$REPO/.claude/scripts"
mkdir -p "$REPO/.claude/docs"
mkdir -p "$REPO/Docs"

# Copy scripts
echo "Copying scripts..."
cp "$OUTPUTS/setup-ssh-key.sh" "$REPO/.claude/scripts/"
cp "$OUTPUTS/verify-ssh.sh" "$REPO/.claude/scripts/"
cp "$OUTPUTS/preflight-with-ssh.py" "$REPO/.claude/scripts/preflight.py"
cp "$OUTPUTS/wake-with-preflight.sh" "$REPO/.claude/scripts/wake.sh"

# Make executable
chmod +x "$REPO/.claude/scripts/setup-ssh-key.sh"
chmod +x "$REPO/.claude/scripts/verify-ssh.sh"
chmod +x "$REPO/.claude/scripts/preflight.py"
chmod +x "$REPO/.claude/scripts/wake.sh"

echo "✓ Scripts copied and made executable"

# Copy documentation
echo "Copying documentation..."
cp "$OUTPUTS/SSH-SETUP-GUIDE.md" "$REPO/.claude/docs/"
cp "$OUTPUTS/SSH-SETUP-GUIDE.md" "$REPO/Docs/" # Public copy too
cp "$OUTPUTS/SSH-INTEGRATION-COMPLETE.md" "$REPO/.claude/docs/"

echo "✓ Documentation copied"

# Summary
echo ""
echo "=== Files Copied ==="
echo ""
echo "Scripts:"
echo "  .claude/scripts/setup-ssh-key.sh (executable)"
echo "  .claude/scripts/verify-ssh.sh (executable)"
echo "  .claude/scripts/preflight.py (updated, executable)"
echo "  .claude/scripts/wake.sh (updated, executable)"
echo ""
echo "Documentation:"
echo "  .claude/docs/SSH-SETUP-GUIDE.md"
echo "  .claude/docs/SSH-INTEGRATION-COMPLETE.md"
echo "  Docs/SSH-SETUP-GUIDE.md (public)"
echo ""
echo "=== Integration Complete ==="
echo ""
echo "Next steps:"
echo "  1. Test on your system: ./.claude/scripts/wake.sh"
echo "  2. If it works, commit to your repo"
echo "  3. Push to private repo"
echo "  4. Test on Android/other devices"
echo ""
