#!/bin/bash
# Git Remote Reconfiguration Script
# Eliminates staging repo, sets up dual-remote workflow
# Date: 2026-03-01
# Author: Vector

set -e  # Exit on error

CLAUDE_HOME="/home/tallest/Claude"
PRIVATE_REPO="git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git"
PUBLIC_REPO="git@github.com:continuity-bridge/continuity-bridge.git"

echo "=== Git Remote Reconfiguration ==="
echo "CLAUDE_HOME: $CLAUDE_HOME"
echo ""

cd "$CLAUDE_HOME"

# Show current configuration
echo "Current remotes:"
git remote -v
echo ""

# Backup current config
echo "Backing up current git config..."
cp .git/config .git/config.backup-$(date +%Y%m%d-%H%M%S)
echo "✓ Backup created"
echo ""

# Remove old origin (staging repo)
echo "Removing 'origin' remote (staging repo)..."
if git remote | grep -q "^origin$"; then
    git remote remove origin
    echo "✓ Removed origin"
else
    echo "! origin remote not found (already removed?)"
fi
echo ""

# Add private remote (if not exists)
echo "Adding 'private' remote..."
if git remote | grep -q "^private$"; then
    echo "! private remote already exists, updating URL..."
    git remote set-url private "$PRIVATE_REPO"
else
    git remote add private "$PRIVATE_REPO"
fi
echo "✓ private → $PRIVATE_REPO"
echo ""

# Verify/update public remote
echo "Verifying 'public' remote..."
if git remote | grep -q "^public$"; then
    CURRENT_PUBLIC=$(git remote get-url public)
    if [ "$CURRENT_PUBLIC" != "$PUBLIC_REPO" ]; then
        echo "! Updating public remote URL..."
        git remote set-url public "$PUBLIC_REPO"
    fi
    echo "✓ public → $PUBLIC_REPO"
else
    echo "! public remote not found, adding..."
    git remote add public "$PUBLIC_REPO"
    echo "✓ Added public remote"
fi
echo ""

# Show new configuration
echo "=== NEW CONFIGURATION ==="
git remote -v
echo ""

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Create working branch if needed
if ! git branch | grep -q "working"; then
    echo "Creating 'working' branch from current branch ($CURRENT_BRANCH)..."
    git branch working
    echo "✓ Created working branch"
else
    echo "✓ working branch exists"
fi
echo ""

# Offer to push to private
echo "=== Ready to Push ==="
echo "To push current branch to private:"
echo "  git push private $CURRENT_BRANCH"
echo ""
echo "To push working branch to private:"
echo "  git checkout working"
echo "  git push -u private working"
echo ""
echo "Reconfiguration complete!"
