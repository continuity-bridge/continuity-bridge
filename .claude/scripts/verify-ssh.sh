#!/bin/bash
# verify-ssh.sh
# Quick check if SSH is set up correctly for Continuity Bridge

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=== SSH Setup Verification ==="
echo ""

# Check 1: Private key exists
if [ -f "$HOME/.ssh/continuity-bridge" ]; then
    echo -e "${GREEN}✓${NC} Private key exists"
    
    # Check permissions
    PERMS=$(stat -c %a "$HOME/.ssh/continuity-bridge" 2>/dev/null || stat -f %A "$HOME/.ssh/continuity-bridge" 2>/dev/null)
    if [ "$PERMS" = "600" ]; then
        echo -e "${GREEN}✓${NC} Private key permissions correct (600)"
    else
        echo -e "${YELLOW}⚠${NC} Private key permissions: $PERMS (should be 600)"
        echo "  Fix: chmod 600 ~/.ssh/continuity-bridge"
    fi
else
    echo -e "${RED}✗${NC} Private key not found"
    echo "  Run: ./setup-ssh-key.sh"
    exit 1
fi

# Check 2: Public key exists
if [ -f "$HOME/.ssh/continuity-bridge.pub" ]; then
    echo -e "${GREEN}✓${NC} Public key exists"
else
    echo -e "${RED}✗${NC} Public key not found"
    echo "  Run: ./setup-ssh-key.sh"
    exit 1
fi

# Check 3: SSH config
if [ -f "$HOME/.ssh/config" ]; then
    if grep -q "Host github.com-continuity-bridge" "$HOME/.ssh/config"; then
        echo -e "${GREEN}✓${NC} SSH config has github.com-continuity-bridge entry"
    else
        echo -e "${RED}✗${NC} SSH config missing github.com-continuity-bridge"
        echo "  Run: ./setup-ssh-key.sh"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} SSH config not found"
    echo "  Run: ./setup-ssh-key.sh"
    exit 1
fi

# Check 4: GitHub connection
echo ""
echo "Testing GitHub connection..."
if ssh -T git@github.com-continuity-bridge 2>&1 | grep -q "successfully authenticated"; then
    echo -e "${GREEN}✓${NC} GitHub authentication successful"
    
    # Extract username from response
    USERNAME=$(ssh -T git@github.com-continuity-bridge 2>&1 | grep -oP 'Hi \K[^!]+')
    if [ -n "$USERNAME" ]; then
        echo "  Authenticated as: $USERNAME"
    fi
else
    echo -e "${YELLOW}⚠${NC} GitHub authentication failed"
    echo ""
    echo "This means:"
    echo "  1. You haven't added the key to GitHub yet, OR"
    echo "  2. The key on GitHub doesn't match your local key"
    echo ""
    echo "To fix:"
    echo "  1. Copy your public key:"
    echo "     cat ~/.ssh/continuity-bridge.pub"
    echo ""
    echo "  2. Add it to GitHub:"
    echo "     https://github.com/settings/keys"
    echo ""
    echo "  3. Run this script again to verify"
    exit 1
fi

# Check 5: Git remote (if in a repo)
echo ""
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Checking git remotes..."
    
    if git remote -v | grep -q "github.com-continuity-bridge"; then
        echo -e "${GREEN}✓${NC} Git remote uses github.com-continuity-bridge"
    else
        echo -e "${YELLOW}⚠${NC} Git remote not using github.com-continuity-bridge"
        echo ""
        echo "Current remotes:"
        git remote -v
        echo ""
        echo "To fix:"
        echo "  git remote set-url private git@github.com-continuity-bridge:username/repo.git"
    fi
else
    echo "Not in a git repository (skipping remote check)"
fi

echo ""
echo -e "${GREEN}=== Verification Complete ===${NC}"
echo ""
echo "Your SSH setup is working correctly!"
echo ""
echo "Next steps:"
echo "  1. Clone or pull your private repo"
echo "  2. Run: python .claude/scripts/preflight.py"
echo ""
