#!/usr/bin/env python3
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
"""
bridge-sync.py - Continuity Bridge Automation
Purpose: Sync work between Personal (Claude) and Public (continuity-bridge) repos
Usage: python3 bridge-sync.py [push|pull|status]

Cross-platform replacement for bridge-sync.sh
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


# ANSI color codes (work on Windows 10+, Linux, Mac)
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color


def log_old_business(message):
    """Log old business (status/context)"""
    print(f"{Colors.BLUE}--- OLD BUSINESS: {message} ---{Colors.NC}")


def log_new_business(message):
    """Log new business (actions)"""
    print(f"{Colors.GREEN}--- NEW BUSINESS: {message} ---{Colors.NC}")


def log_error(message):
    """Log error"""
    print(f"{Colors.RED}ERROR: {message}{Colors.NC}", file=sys.stderr)


def run_git_command(cmd, cwd):
    """Run git command in specified directory"""
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            return False
        
        if result.stdout:
            print(result.stdout)
        
        return True
        
    except subprocess.TimeoutExpired:
        log_error(f"Command timed out: {' '.join(cmd)}")
        return False
    except Exception as e:
        log_error(f"Command failed: {e}")
        return False


def get_repo_paths():
    """Get platform-specific repo paths"""
    system = platform.system()
    
    if system == 'Linux':
        personal_repo = Path('/home/tallest/Claude')
        public_repo = Path('/home/tallest/Work/Code/continuity-bridge/continuity-bridge')
        os_label = 'Linux (Pop OS)'
    elif system == 'Windows':
        personal_repo = Path('D:/Claude')
        public_repo = Path('D:/Code/Work/continuity-bridge/continuity-bridge')
        os_label = 'Windows'
    elif system == 'Darwin':
        personal_repo = Path.home() / 'Claude'
        public_repo = Path.home() / 'Work/Code/continuity-bridge/continuity-bridge'
        os_label = 'macOS'
    else:
        log_error(f"Unknown OS: {system}")
        sys.exit(1)
    
    return personal_repo, public_repo, os_label


def check_status():
    """Check status of both repos"""
    personal_repo, public_repo, os_label = get_repo_paths()
    
    log_old_business(f"Status Check ({os_label})")
    
    print(f"Personal Repo: {personal_repo}")
    if personal_repo.exists():
        run_git_command(['git', 'status', '-s'], personal_repo)
    else:
        log_error(f"Personal repo not found: {personal_repo}")
    
    print()
    print(f"Public Repo: {public_repo}")
    if public_repo.exists():
        run_git_command(['git', 'status', '-s'], public_repo)
    else:
        log_error(f"Public repo not found: {public_repo}")


def sync_push():
    """Push Personal -> Public -> GitHub"""
    personal_repo, public_repo, os_label = get_repo_paths()
    
    log_new_business("Initiating Bridge Push (Syncing Personal -> Public -> GitHub)")
    
    # 1. Check Personal Status
    if not personal_repo.exists():
        log_error(f"Personal repo not found: {personal_repo}")
        return False
    
    result = subprocess.run(
        ['git', 'status', '-s'],
        cwd=str(personal_repo),
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        log_error("Personal repo has uncommitted changes. Commit first.")
        return False
    
    # 2. Push to local Public repo
    print("Pushing Personal -> Local Public...")
    if not run_git_command(['git', 'push', 'origin', 'main'], personal_repo):
        log_error("Local push failed.")
        return False
    
    # 3. Push to GitHub from Public repo
    if not public_repo.exists():
        log_error(f"Public repo not found: {public_repo}")
        return False
    
    print("Pushing Local Public -> GitHub (origin)...")
    if not run_git_command(['git', 'push', 'origin', 'main'], public_repo):
        log_error("GitHub push from Public failed.")
        return False
    
    # 4. Push to GitHub from Personal repo (direct target)
    print("Pushing Personal -> GitHub (public remote)...")
    if not run_git_command(['git', 'push', 'public', 'main'], personal_repo):
        log_error("GitHub push from Personal failed.")
        return False
    
    log_new_business("Bridge synchronization complete.")
    return True


def sync_pull():
    """Pull GitHub -> Public -> Personal"""
    personal_repo, public_repo, os_label = get_repo_paths()
    
    log_new_business("Initiating Bridge Pull (Syncing GitHub -> Public -> Personal)")
    
    # 1. Pull GitHub -> local Public
    if not public_repo.exists():
        log_error(f"Public repo not found: {public_repo}")
        return False
    
    print("Pulling GitHub -> Local Public...")
    if not run_git_command(['git', 'pull', 'origin', 'main'], public_repo):
        log_error("GitHub pull to Public failed.")
        return False
    
    # 2. Pull local Public -> Personal
    if not personal_repo.exists():
        log_error(f"Personal repo not found: {personal_repo}")
        return False
    
    print("Pulling Local Public -> Personal...")
    if not run_git_command(['git', 'pull', 'origin', 'main'], personal_repo):
        log_error("Local pull to Personal failed.")
        return False
    
    log_new_business("Bridge update complete.")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: bridge-sync.py [push|pull|status]")
        print()
        print("Commands:")
        print("  push   - Sync Personal -> Public -> GitHub")
        print("  pull   - Sync GitHub -> Public -> Personal")
        print("  status - Check status of both repos")
        return 1
    
    command = sys.argv[1].lower()
    
    if command == 'push':
        return 0 if sync_push() else 1
    elif command == 'pull':
        return 0 if sync_pull() else 1
    elif command == 'status':
        check_status()
        return 0
    else:
        log_error(f"Unknown command: {command}")
        print("Usage: bridge-sync.py [push|pull|status]")
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n")
        sys.exit(130)
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
