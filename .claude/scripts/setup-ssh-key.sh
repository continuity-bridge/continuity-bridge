#!/bin/bash
# setup-ssh-key.sh
# Creates dedicated SSH key for Continuity Bridge (won't conflict with existing keys)

set -e  # Exit on error

echo "==================================="
echo "Continuity Bridge - SSH Key Setup"
echo "==================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Determine user's home directory
if [ -d "/sdcard" ]; then
    # Android/Termux
    USER_HOME="$HOME"
    SSH_DIR="$HOME/.ssh"
else
    # Linux/Mac/Windows Git Bash
    USER_HOME="$HOME"
    SSH_DIR="$HOME/.ssh"
fi

KEY_NAME="continuity-bridge"
KEY_PATH="$SSH_DIR/$KEY_NAME"
PUB_KEY_PATH="${KEY_PATH}.pub"

echo -e "${BLUE}This script will:${NC}"
echo "  1. Create a NEW SSH key ONLY for Continuity Bridge"
echo "  2. NOT touch your existing SSH keys (if any)"
echo "  3. Configure git to use this key for your private repo"
echo "  4. Show you how to add it to GitHub"
echo ""
echo -e "${YELLOW}Location: $KEY_PATH${NC}"
echo ""

# Check if key already exists
if [ -f "$KEY_PATH" ]; then
    echo -e "${YELLOW}⚠ SSH key already exists at $KEY_PATH${NC}"
    read -p "Overwrite? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Using existing key."
        SKIP_KEYGEN=true
    else
        echo "Will create new key (old one will be backed up)"
        mv "$KEY_PATH" "${KEY_PATH}.backup.$(date +%s)"
        mv "$PUB_KEY_PATH" "${PUB_KEY_PATH}.backup.$(date +%s)" 2>/dev/null || true
        SKIP_KEYGEN=false
    fi
else
    SKIP_KEYGEN=false
fi

# Get user email for SSH key
echo ""
echo -e "${BLUE}What email should be associated with this SSH key?${NC}"
echo "(This is just a label - use the email for your GitHub account)"
read -p "Email: " USER_EMAIL

if [ -z "$USER_EMAIL" ]; then
    echo -e "${RED}✗ Email required${NC}"
    exit 1
fi

# Create .ssh directory if needed
mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

# Generate SSH key
if [ "$SKIP_KEYGEN" = false ]; then
    echo ""
    echo -e "${BLUE}Generating SSH key...${NC}"
    
    ssh-keygen -t ed25519 -C "$USER_EMAIL" -f "$KEY_PATH" -N ""
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ SSH key created successfully${NC}"
        chmod 600 "$KEY_PATH"
        chmod 644 "$PUB_KEY_PATH"
    else
        echo -e "${RED}✗ Failed to create SSH key${NC}"
        exit 1
    fi
fi

# Configure SSH to use this key for GitHub
echo ""
echo -e "${BLUE}Configuring SSH...${NC}"

SSH_CONFIG="$SSH_DIR/config"

# Check if config already has entry for continuity-bridge
if [ -f "$SSH_CONFIG" ] && grep -q "Host github.com-continuity-bridge" "$SSH_CONFIG"; then
    echo -e "${YELLOW}⚠ SSH config already has continuity-bridge entry${NC}"
else
    # Add config entry
    cat >> "$SSH_CONFIG" << EOF

# Continuity Bridge - Dedicated key
Host github.com-continuity-bridge
    HostName github.com
    User git
    IdentityFile $KEY_PATH
    IdentitiesOnly yes

EOF
    echo -e "${GREEN}✓ SSH config updated${NC}"
fi

chmod 600 "$SSH_CONFIG"

# Configure git to use this SSH host for the private repo
echo ""
echo -e "${BLUE}Git Configuration:${NC}"
echo ""
echo "Your private repo URL should use: github.com-continuity-bridge"
echo "Example: git@github.com-continuity-bridge:username/continuity-bridge_username-anchor.git"
echo ""
echo "This ensures git uses your dedicated Continuity Bridge key."
echo ""

# Display public key
echo ""
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}Your SSH Public Key (copy this):${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
cat "$PUB_KEY_PATH"
echo ""
echo -e "${GREEN}=====================================${NC}"
echo ""

# Instructions for adding to GitHub
echo -e "${BLUE}Next Steps - Adding Key to GitHub:${NC}"
echo ""
echo "1. Copy the public key above (from 'ssh-ed25519' to the end)"
echo ""
echo "2. Go to: https://github.com/settings/keys"
echo ""
echo "3. Click: 'New SSH key'"
echo ""
echo "4. Title: 'Continuity Bridge'"
echo ""
echo "5. Key type: 'Authentication Key'"
echo ""
echo "6. Paste the public key into the 'Key' field"
echo ""
echo "7. Click: 'Add SSH key'"
echo ""
echo -e "${YELLOW}⚠ Important: Use the FULL key including 'ssh-ed25519' and the email at the end${NC}"
echo ""

# Test connectivity (if GitHub key already added)
echo -e "${BLUE}Testing SSH Connection:${NC}"
echo "(This will fail if you haven't added the key to GitHub yet)"
echo ""

ssh -T git@github.com-continuity-bridge 2>&1 | grep -q "successfully authenticated" && \
    echo -e "${GREEN}✓ SSH connection successful!${NC}" || \
    echo -e "${YELLOW}⚠ Not connected yet - add the key to GitHub first${NC}"

echo ""
echo -e "${GREEN}Setup Complete!${NC}"
echo ""
echo "Key files created:"
echo "  Private: $KEY_PATH (keep this SECRET)"
echo "  Public:  $PUB_KEY_PATH (safe to share)"
echo "  Config:  $SSH_CONFIG"
echo ""
echo "To test after adding to GitHub:"
echo "  ssh -T git@github.com-continuity-bridge"
echo ""
echo "To clone your private repo:"
echo "  git clone git@github.com-continuity-bridge:username/repo.git"
echo ""
