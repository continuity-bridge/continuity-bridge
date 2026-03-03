#!/usr/bin/env python3
"""
Continuity Bridge - Capability Detection System v0.2.0
Detects hardware/software capabilities and determines optimal workflow

Contributors: 
- Vector (four-workflow architecture, container git recognition)
- Gemini (probe_write technique, local LLM detection, git integration)

Date: 2026-03-01
"""

import os
import sys
import json
import socket
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple


def probe_write(path: str) -> bool:
    """
    Real-world check: Is directory actually persistent and writable?
    
    Credit: Gemini's contribution for robust testing
    """
    if not path or not os.path.isdir(path):
        return False
    
    test_file = os.path.join(path, '.probe_write')
    try:
        with open(test_file, 'w') as f:
            f.write('continuity-test')
        os.remove(test_file)
        return True
    except:
        return False


def check_local_llm() -> Dict[str, any]:
    """
    Check for Ollama/Local LLM gateway.
    
    Credit: Gemini's contribution for local LLM detection
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect(('localhost', 11434))
        return {"available": True, "endpoint": "http://localhost:11434"}
    except:
        return {"available": False, "endpoint": None}
    finally:
        s.close()


def get_git_info(path: Optional[str] = None) -> Dict:
    """
    Check git availability and repo status.
    
    Credit: Gemini's base logic, extended by Vector
    """
    # First check if git command exists
    try:
        subprocess.run(['git', '--version'], 
                      capture_output=True, timeout=2, check=True)
        git_available = True
    except:
        return {"available": False, "in_repo": False}
    
    # If path provided, check if it's a repo
    if path and os.path.isdir(path):
        try:
            branch = subprocess.check_output(
                ['git', '-C', path, 'rev-parse', '--abbrev-ref', 'HEAD'],
                stderr=subprocess.DEVNULL, timeout=2
            ).decode().strip()
            
            # Get remote info
            try:
                remotes = subprocess.check_output(
                    ['git', '-C', path, 'remote', '-v'],
                    stderr=subprocess.DEVNULL, timeout=2
                ).decode().strip()
                has_private_remote = 'private' in remotes or 'anchor' in remotes
            except:
                has_private_remote = False
            
            return {
                "available": True, 
                "in_repo": True, 
                "branch": branch,
                "has_private_remote": has_private_remote
            }
        except:
            return {"available": True, "in_repo": False}
    
    return {"available": True, "in_repo": False}


def detect_platform() -> str:
    """Detect platform type."""
    # Android check FIRST (most specific)
    if os.path.exists('/sdcard/Claude') or os.path.exists('/sdcard'):
        return 'android'
    
    # Container check
    if os.path.exists('/home/claude'):
        return 'claude.ai_container'
    
    # Windows check
    if os.name == 'nt':
        return 'windows'
    
    # Linux desktop check
    if os.path.exists('/etc/os-release'):
        try:
            with open('/etc/os-release') as f:
                content = f.read()
                # Explicitly NOT Android (already checked above)
                return 'linux_desktop'
        except:
            pass
    
    return 'unknown'


def detect_distro_family() -> str:
    """
    Detect Linux distribution family for package management.
    
    Families: debian, redhat, suse, arch, alpine, gentoo, android, other
    """
    # Android check FIRST (before /etc/os-release)
    if os.path.exists('/sdcard/Claude') or os.path.exists('/sdcard'):
        return "android"
    
    if not os.path.exists('/etc/os-release'):
        return "unknown"
    
    try:
        with open('/etc/os-release') as f:
            content = f.read().lower()
            
            if any(name in content for name in ['ubuntu', 'debian', 'pop!_os', 'mint', 'elementary']):
                return "debian"
            elif any(name in content for name in ['rhel', 'redhat', 'fedora', 'centos', 'rocky', 'alma']):
                return "redhat"
            elif any(name in content for name in ['suse', 'opensuse']):
                return "suse"
            elif 'arch' in content or 'manjaro' in content:
                return "arch"
            elif 'alpine' in content:
                return "alpine"
            elif 'gentoo' in content:
                return "gentoo"
            else:
                return "other"
    except:
        return "unknown"


def get_package_manager(distro_family: str) -> Dict[str, str]:
    """Map distro family to package manager."""
    package_managers = {
        "debian": {"manager": "apt", "install_cmd": "sudo apt install -y"},
        "redhat": {"manager": "dnf", "install_cmd": "sudo dnf install -y"},
        "suse": {"manager": "zypper", "install_cmd": "sudo zypper install -y"},
        "arch": {"manager": "pacman", "install_cmd": "sudo pacman -S --noconfirm"},
        "alpine": {"manager": "apk", "install_cmd": "sudo apk add"},
        "gentoo": {"manager": "emerge", "install_cmd": "sudo emerge"},
        "other": {"manager": "unknown", "install_cmd": "unknown"},
        "unknown": {"manager": "unknown", "install_cmd": "unknown"}
    }
    return package_managers.get(distro_family, package_managers["unknown"])


def detect_claude_home() -> str:
    """Find CLAUDE_HOME across platforms."""
    candidates = [
        "/home/tallest/Claude",
        "D:\\Claude",
        "/sdcard/Claude",
        os.path.expanduser("~/Claude"),
        os.getcwd()
    ]
    
    for path in candidates:
        if os.path.exists(os.path.join(path, '.claude')):
            return path
    
    return os.getcwd()


def detect_bash_context() -> str:
    """Determine if bash runs in container or local system."""
    try:
        pwd = subprocess.check_output(['pwd'], 
                                     text=True, timeout=2).strip()
        if '/home/claude' in pwd:
            return 'container'
        elif '/home' in pwd:
            return 'local_system'
        return 'unknown'
    except:
        return 'none'


def detect_environment() -> Dict:
    """
    Complete environment detection with workflow determination.
    
    Four workflows (Vector's key contribution):
    1. DIRECT_WRITE - Direct MCP access to CLAUDE_HOME
    2. CONTAINER_GIT_WITH_BRIDGE - Clone repo in container, full git workflow
    3. BRIDGE_ONLY - Outputs bridge, manual integration
    4. TEXT_ONLY - No write access, manual copy-paste
    """
    
    # Detect CLAUDE_HOME
    claude_home = detect_claude_home()
    
    # Test write access using Gemini's probe_write
    has_direct_write = probe_write(claude_home)
    has_bridge = probe_write("/mnt/user-data/outputs")
    
    # Platform detection
    platform = detect_platform()
    is_android = os.path.exists("/sdcard") or \
                 ("android" in os.uname().release.lower() if hasattr(os, 'uname') else False)
    
    # Git and bash context
    git_info = get_git_info(claude_home)
    bash_context = detect_bash_context()
    
    # Local LLM (Gemini's contribution)
    local_llm = check_local_llm()
    
    # Distro family (for Linux)
    distro_family = detect_distro_family() if platform.startswith('linux') else None
    package_info = get_package_manager(distro_family) if distro_family else {}
    
    # Build manifest
    manifest = {
        "manifest_version": "0.2.0",
        "timestamp": None,  # Will be set by wake.sh
        "substrate": {
            "claude_home": claude_home,
            "platform": platform,
            "write_access": "direct" if has_direct_write else \
                           ("bridge" if has_bridge else "none"),
            "is_android": is_android,
            "bash_context": bash_context,
            "distro_family": distro_family,
            "package_manager": package_info.get("manager"),
            "package_install_cmd": package_info.get("install_cmd")
        },
        "tools": {
            "git": git_info,
            "local_llm": local_llm,
            "python": True
        },
        "capabilities": {
            "can_clone_in_container": git_info['available'] and bash_context == 'container',
            "can_write_direct": has_direct_write,
            "can_use_bridge": has_bridge,
            "has_local_llm": local_llm['available']
        }
    }
    
    # Determine workflow (VECTOR'S KEY CONTRIBUTION)
    # This is where we recognize container git as full capability
    if has_direct_write:
        manifest["workflow"] = "DIRECT_WRITE"
        manifest["bridge_strategy"] = "direct_write"
        manifest["instruction"] = f"Write files directly to {claude_home}"
        manifest["workflow_description"] = "Optimal: Direct MCP access to CLAUDE_HOME"
        
    elif git_info['available'] and bash_context == 'container' and has_bridge:
        manifest["workflow"] = "CONTAINER_GIT_WITH_BRIDGE"
        manifest["bridge_strategy"] = "container_git_with_bridge"
        manifest["instruction"] = (
            f"Clone private repo in container (/home/claude/work), "
            "work with full git access, push commits. "
            "Use bridge for session summaries only."
        )
        manifest["workflow_description"] = "Good: Full git workflow in container"
        manifest["container_workflow"] = {
            "clone_location": "/home/claude/work",
            "steps": [
                "cd /home/claude",
                "git clone git@github.com:continuity-bridge/continuity-bridge_tallest-anchor.git work",
                "cd work",
                "git checkout working"
            ]
        }
        
    elif has_bridge:
        manifest["workflow"] = "BRIDGE_ONLY"
        manifest["bridge_strategy"] = "outputs_bridge_only"
        manifest["instruction"] = "Write to /mnt/user-data/outputs, user integrates manually"
        manifest["workflow_description"] = "Acceptable: Outputs bridge with manual integration"
        
    else:
        manifest["workflow"] = "TEXT_ONLY"
        manifest["bridge_strategy"] = "text_only"
        manifest["instruction"] = "Output code blocks only; user must copy manually"
        manifest["workflow_description"] = "Minimal: No write access, manual copy-paste"
    
    return manifest


def main():
    """Run capability detection and output results."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Continuity Bridge capability detection"
    )
    parser.add_argument('--json', '-j', action='store_true',
                       help='Output JSON format')
    
    args = parser.parse_args()
    
    manifest = detect_environment()
    
    # Output format
    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        # Human-readable
        print("=" * 70)
        print("CONTINUITY BRIDGE - CAPABILITY DETECTION v0.2.0")
        print("=" * 70)
        print(f"\nCLAUDE_HOME: {manifest['substrate']['claude_home']}")
        print(f"Platform: {manifest['substrate']['platform']}")
        print(f"Write Access: {manifest['substrate']['write_access']}")
        print(f"Bash Context: {manifest['substrate']['bash_context']}")
        
        if manifest['substrate']['distro_family']:
            print(f"Distro Family: {manifest['substrate']['distro_family']}")
            print(f"Package Manager: {manifest['substrate']['package_manager']}")
        
        print(f"\nGit Available: {manifest['tools']['git']['available']}")
        if manifest['tools']['git']['in_repo']:
            print(f"Git Branch: {manifest['tools']['git']['branch']}")
        
        print(f"Local LLM: {manifest['tools']['local_llm']['available']}")
        if manifest['tools']['local_llm']['available']:
            print(f"LLM Endpoint: {manifest['tools']['local_llm']['endpoint']}")
        
        print(f"\nOPTIMAL WORKFLOW: {manifest['workflow']}")
        print(f"Description: {manifest['workflow_description']}")
        print(f"\nINSTRUCTION: {manifest['instruction']}")
        
        if manifest.get('container_workflow'):
            print(f"\nContainer Setup Steps:")
            for step in manifest['container_workflow']['steps']:
                print(f"  {step}")
        
        print("\n" + "=" * 70)
    
    # Save manifest for instance to read
    manifest_path = os.path.join(
        manifest['substrate']['claude_home'],
        '.claude',
        'capabilities-manifest.json'
    )
    try:
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        if not args.json:
            print(f"\nCapabilities saved to: {manifest_path}")
    except Exception as e:
        print(f"\nWarning: Could not save manifest: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
