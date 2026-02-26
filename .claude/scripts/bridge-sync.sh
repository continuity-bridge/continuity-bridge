#!/bin/bash

# bridge-sync.sh - Continuity Bridge Automation
# Purpose: Sync work between Personal (Claude) and Public (continuity-bridge) repos.
# Usage: ./bridge-sync.sh [push|pull|status]

# --- OS DETECTION & PATH CONFIG ---

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PERSONAL_REPO="/home/tallest/Claude"
    PUBLIC_REPO="/home/tallest/Work/Code/continuity-bridge"
    OS_LABEL="Linux (Pop OS)"
elif [[ "$OSTYPE" == "msys" ]]; then
    PERSONAL_REPO="/d/Claude"
    PUBLIC_REPO="/d/Code/Work/continuity-bridge/continuity-bridge"
    OS_LABEL="Windows (Git Bash/MSYS)"
else
    echo "Error: Unknown OSTYPE ($OSTYPE). Manually verify paths in script."
    exit 1
fi

# --- COLORS ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- LOGGING HELPERS ---
log_old_business() {
    echo -e "${BLUE}--- OLD BUSINESS: $1 ---${NC}"
}

log_new_business() {
    echo -e "${GREEN}--- NEW BUSINESS: $1 ---${NC}"
}

log_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# --- FUNCTIONS ---

check_status() {
    log_old_business "Status Check ($OS_LABEL)"
    echo "Personal Repo: $PERSONAL_REPO"
    cd "$PERSONAL_REPO" && git status -s
    echo ""
    echo "Public Repo: $PUBLIC_REPO"
    cd "$PUBLIC_REPO" && git status -s
}

sync_push() {
    log_new_business "Initiating Bridge Push (Syncing Personal -> Public -> GitHub)"
    
    # 1. Check Personal Status
    cd "$PERSONAL_REPO"
    if [[ -n $(git status -s) ]]; then
        log_error "Personal repo has uncommitted changes. Commit first."
        exit 1
    fi

    # 2. Push to local Public repo
    echo "Pushing Personal -> Local Public..."
    git push origin main
    if [ $? -ne 0 ]; then log_error "Local push failed."; exit 1; fi

    # 3. Push to GitHub from Public repo
    cd "$PUBLIC_REPO"
    echo "Pushing Local Public -> GitHub (origin)..."
    git push origin main
    if [ $? -ne 0 ]; then log_error "GitHub push from Public failed."; exit 1; fi

    # 4. Push to GitHub from Personal repo (direct target)
    cd "$PERSONAL_REPO"
    echo "Pushing Personal -> GitHub (public remote)..."
    git push public main
    if [ $? -ne 0 ]; then log_error "GitHub push from Personal failed."; exit 1; fi

    log_new_business "Bridge synchronization complete."
}

sync_pull() {
    log_new_business "Initiating Bridge Pull (Syncing GitHub -> Public -> Personal)"
    
    # 1. Pull GitHub -> local Public
    cd "$PUBLIC_REPO"
    echo "Pulling GitHub -> Local Public..."
    git pull origin main
    if [ $? -ne 0 ]; then log_error "GitHub pull to Public failed."; exit 1; fi

    # 2. Pull local Public -> Personal
    cd "$PERSONAL_REPO"
    echo "Pulling Local Public -> Personal..."
    git pull origin main
    if [ $? -ne 0 ]; then log_error "Local pull to Personal failed."; exit 1; fi

    log_new_business "Bridge update complete."
}

# --- MAIN ---

case "$1" in
    push)
        sync_push
        ;;
    pull)
        sync_pull
        ;;
    status)
        check_status
        ;;
    *)
        echo "Usage: $0 [push|pull|status]"
        exit 1
        ;;
esac
