#!/usr/bin/env python3
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
"""
Git Configuration Detection Script
Generates git tool configuration for -isms files
"""

import subprocess
import json
import sys
from typing import Dict, Any, Optional

def run_command(cmd: list) -> Optional[str]:
    """Run a shell command and return stdout, or None on failure."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None

def parse_version(version_str: str) -> tuple:
    """Parse git version string into (major, minor, patch)."""
    # Example: "git version 2.43.0" -> (2, 43, 0)
    try:
        parts = version_str.split()
        if len(parts) >= 3 and parts[0] == "git" and parts[1] == "version":
            version_parts = parts[2].split('.')
            major = int(version_parts[0]) if len(version_parts) > 0 else 0
            minor = int(version_parts[1]) if len(version_parts) > 1 else 0
            patch = int(version_parts[2]) if len(version_parts) > 2 else 0
            return (major, minor, patch)
    except Exception:
        pass
    return (0, 0, 0)

def detect_git_config() -> Dict[str, Any]:
    """Detect git configuration and capabilities."""
    
    # Get version
    version_output = run_command(["git", "--version"])
    if not version_output:
        return {"error": "Git not found or not executable"}
    
    major, minor, patch = parse_version(version_output)
    
    # Get config values
    pull_strategy = run_command(["git", "config", "--global", "pull.rebase"])
    if not pull_strategy:
        pull_strategy = run_command(["git", "config", "--global", "pull.ff"])
    default_branch = run_command(["git", "config", "--global", "init.defaultBranch"])
    
    # Determine capabilities based on version
    has_switch = major > 2 or (major == 2 and minor >= 23)
    has_restore = major > 2 or (major == 2 and minor >= 23)
    supports_worktrees = major > 2 or (major == 2 and minor >= 5)
    
    config = {
        "version": f"{major}.{minor}.{patch}",
        "version_major": major,
        "version_minor": minor,
        "version_patch": patch,
        "has_switch_command": has_switch,
        "has_restore_command": has_restore,
        "default_pull_strategy": pull_strategy or "merge",
        "default_branch": default_branch or "main",
        "supports_worktrees": supports_worktrees,
        "notes": "Auto-detected git configuration"
    }
    
    return config

if __name__ == "__main__":
    config = detect_git_config()
    print(json.dumps(config, indent=2))
