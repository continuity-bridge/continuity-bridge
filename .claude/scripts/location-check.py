#!/usr/bin/env python3
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
"""
Location Check - Establishes WHERE instance is running
Run this FIRST to set environment variables for all other scripts

Version: 0.2.1
Updated: Cross-platform support for all 6 systems
"""

import os
import sys
import socket
from pathlib import Path


def detect_physical_system():
    """Identify which physical machine we're on"""
    hostname = socket.gethostname().lower()
    
    # Jerry's systems from Device_and_Network_Naming_Scheme.md
    if hostname == 'persephone':
        return 'persephone'  # Desktop Pop!_OS 24.04
    elif hostname == 'hecate':
        return 'hecate'      # Desktop Windows (dual boot with Persephone)
    elif hostname == 'geras':
        return 'geras'       # Laptop P71 - Elementary OS 8.1
    elif hostname == 'ixion':
        return 'ixion'       # Ubuntu Server 24.04
    elif hostname == 'orpheus':
        return 'orpheus'     # Fire HD 8 (FireOS 6 / Android 7)
    elif 'magheara' in hostname or 'pixel' in hostname:
        return 'magheara'    # Pixel 10 Pro (Android 14)
    # Fallbacks for detection failures
    elif 'fire' in hostname or os.path.exists('/system/build.prop'):
        return 'fire_tablet'
    elif 'server' in hostname:
        return 'server'
    else:
        return 'unknown'


def detect_execution_context():
    """
    Identify HOW we're running (execution environment)
    
    CRITICAL ORDER:
    1. Android FIRST (/sdcard check)
    2. Container (/home/claude check)
    3. Windows (os.name == 'nt')
    4. Linux/Mac (last, safe fallback)
    
    Android must be first because some Android contexts can have /home/claude
    """
    
    # 1. ANDROID DETECTION MUST BE FIRST
    # Android can have /home/claude in some contexts (Termux, containers)
    # /sdcard is unique to Android
    if os.path.exists('/sdcard'):
        return 'android_termux'
    
    # 2. Container environments (Linux-based)
    # Check after Android to avoid misidentification
    if os.path.exists('/home/claude'):
        return 'claude.ai_container'
    
    # 3. Windows desktop
    # Check os.name for Windows (always 'nt' on Windows)
    if os.name == 'nt':
        return 'windows_desktop'
    
    # 4. Linux/Mac desktop (last, safe for Unix-like systems)
    # By this point we've ruled out Android and containers
    if os.path.exists('/home/tallest/Claude'):
        return 'linux_desktop'
    
    # Mac detection (if needed in future)
    if sys.platform == 'darwin':
        return 'macos_desktop'
    
    # Fallback
    return 'unknown'


def get_claude_home_for_context(context, physical_system='unknown'):
    """
    Return correct CLAUDE_HOME for execution context
    
    Args:
        context: Execution context (linux_desktop, windows_desktop, etc.)
        physical_system: Physical machine name (for system-specific paths)
    
    Returns:
        str: Path to CLAUDE_HOME
    """
    
    # Android paths (FIRST in logic flow)
    if context == 'android_termux':
        return '/sdcard/Claude'
    
    # Container paths
    elif context == 'claude.ai_container':
        # Container can't write to host, but this is the logical path
        return '/home/tallest/Claude'
    
    # Windows paths
    elif context == 'windows_desktop':
        # Primary location
        if os.path.exists('D:\\Claude'):
            return 'D:\\Claude'
        # Fallback location
        elif os.path.exists('C:\\Users\\tallest\\Claude'):
            return 'C:\\Users\\tallest\\Claude'
        else:
            # Default assumption for Hecate
            return 'D:\\Claude'
    
    # Linux desktop paths
    elif context == 'linux_desktop':
        return '/home/tallest/Claude'
    
    # Mac paths (future)
    elif context == 'macos_desktop':
        return '/Users/tallest/Claude'
    
    # Unknown - use current directory as fallback
    else:
        return os.getcwd()


def verify_claude_home(claude_home):
    """
    Verify CLAUDE_HOME exists and has expected structure
    
    Returns: (bool, str) - (success, message)
    """
    claude_path = Path(claude_home)
    
    # Check if path exists
    if not claude_path.exists():
        return False, f"CLAUDE_HOME does not exist: {claude_home}"
    
    # Check for .claude directory
    claude_subdir = claude_path / '.claude'
    if not claude_subdir.exists():
        return False, f"CLAUDE_HOME exists but missing .claude/ subdirectory: {claude_home}"
    
    return True, f"CLAUDE_HOME verified: {claude_home}"


def main():
    # Detect where we are
    physical = detect_physical_system()
    context = detect_execution_context()
    claude_home = get_claude_home_for_context(context, physical)
    
    # Verify CLAUDE_HOME
    success, message = verify_claude_home(claude_home)
    
    if not success:
        print(f"ERROR: {message}", file=sys.stderr)
        sys.exit(1)
    
    # Output for wake.sh to source (stdout)
    print(f"export CURRENT_SYSTEM={physical}")
    print(f"export EXECUTION_CONTEXT={context}")
    print(f"export CLAUDE_HOME={claude_home}")
    
    # Human-readable status (stderr)
    print(f"# Location: {physical} running in {context}", file=sys.stderr)
    print(f"# CLAUDE_HOME: {claude_home}", file=sys.stderr)
    print(f"# Status: {message}", file=sys.stderr)


if __name__ == '__main__':
    main()