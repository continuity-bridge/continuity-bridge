#!/usr/bin/env python3
"""
Continuity Bridge - Isms Bootstrap Generator
Creates platform-specific isms configuration when no template exists

Version: 0.2.0
Credit: Gemini (skeleton concept for first-run), Vector (adaptation)
Date: 2026-03-01
"""

import os
import sys
import json
import subprocess
from pathlib import Path


def detect_distro_family() -> str:
    """Detect Linux distribution family."""
    if not os.path.exists('/etc/os-release'):
        return "unknown"
    
    try:
        with open('/etc/os-release') as f:
            content = f.read().lower()
            
            if any(name in content for name in ['ubuntu', 'debian', 'pop!_os', 'mint']):
                return "debian"
            elif any(name in content for name in ['rhel', 'redhat', 'fedora', 'centos', 'rocky']):
                return "redhat"
            elif any(name in content for name in ['suse', 'opensuse']):
                return "suse"
            elif 'arch' in content or 'manjaro' in content:
                return "arch"
            elif 'alpine' in content:
                return "alpine"
            else:
                return "other"
    except:
        return "unknown"


def get_package_manager_info(distro_family: str) -> dict:
    """Get package manager details for distro family."""
    managers = {
        "debian": {"manager": "apt", "install": "sudo apt install -y"},
        "redhat": {"manager": "dnf", "install": "sudo dnf install -y"},
        "suse": {"manager": "zypper", "install": "sudo zypper install -y"},
        "arch": {"manager": "pacman", "install": "sudo pacman -S --noconfirm"},
        "alpine": {"manager": "apk", "install": "sudo apk add"},
        "unknown": {"manager": "unknown", "install": "unknown"}
    }
    return managers.get(distro_family, managers["unknown"])


def detect_platform_type() -> str:
    """Detect platform type."""
    if os.path.exists('/sdcard'):
        return "android"
    elif os.name == 'nt':
        return "windows"
    elif os.path.exists('/etc/os-release'):
        return "linux"
    else:
        return "unknown"


def generate_isms_skeleton(platform_name: str = None, output_path: str = None) -> dict:
    """
    Generate isms skeleton based on current environment.
    
    Credit: Gemini's concept of auto-generating when no template exists
    """
    
    # Detect platform
    platform_type = detect_platform_type()
    
    # Auto-generate platform name if not provided
    if not platform_name:
        if platform_type == "android":
            platform_name = "android_device"
        elif platform_type == "windows":
            platform_name = "windows_desktop"
        elif platform_type == "linux":
            distro = detect_distro_family()
            platform_name = f"linux_{distro}"
        else:
            platform_name = "unknown_platform"
    
    # Find CLAUDE_HOME
    claude_home_candidates = [
        "/home/the Architect/Claude",
        "[CLAUDE_HOME]",
        "/sdcard/Claude",
        os.path.expanduser("~/Claude")
    ]
    
    claude_home = None
    for candidate in claude_home_candidates:
        if os.path.exists(candidate):
            claude_home = candidate
            break
    
    if not claude_home:
        claude_home = os.path.join(os.getcwd(), "Claude")
    
    # Detect current working directory
    cwd = os.getcwd()
    
    # Build skeleton
    skeleton = {
        "version": "0.2.0",
        "platform_id": platform_name,
        "generated": "auto",
        "note": "Auto-generated isms skeleton. Customize paths as needed.",
        
        "paths": {
            "claude_home": claude_home,
            "working_dir": cwd,
            "vault": os.path.join(claude_home, ".credentials-local")
        },
        
        "constants": {}
    }
    
    # Platform-specific configuration
    if platform_type == "linux":
        distro_family = detect_distro_family()
        pkg_info = get_package_manager_info(distro_family)
        
        skeleton["constants"] = {
            "platform": "linux",
            "distro_family": distro_family,
            "package_manager": pkg_info["manager"],
            "package_install_cmd": pkg_info["install"],
            "init_system": "systemd",  # Assumption - most modern Linux
            "shell": os.environ.get("SHELL", "/bin/bash")
        }
        
    elif platform_type == "windows":
        skeleton["constants"] = {
            "platform": "windows",
            "shell": "powershell",
            "user_profile": os.environ.get("USERPROFILE", ""),
            "drive": claude_home[0] if claude_home and claude_home[1] == ':' else "D:"
        }
        
    elif platform_type == "android":
        skeleton["constants"] = {
            "platform": "android",
            "shell": "/system/bin/sh",
            "storage_type": "scoped",
            "requires_uri_permissions": True
        }
    
    # Ollama endpoint (standard default)
    skeleton["services"] = {
        "ollama_endpoint": "http://localhost:11434"
    }
    
    # Storage strategy
    skeleton["storage"] = {
        "strategy": "auto-detect",
        "note": "Will be determined by capability detection at runtime"
    }
    
    return skeleton


def main():
    """Generate and save isms skeleton."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate isms configuration skeleton for new platform"
    )
    parser.add_argument('--platform', '-p', 
                       help='Platform name (e.g., android_tablet, linux_debian)')
    parser.add_argument('--output', '-o',
                       help='Output file path (default: auto-generated name)')
    parser.add_argument('--preview', action='store_true',
                       help='Preview without writing to file')
    
    args = parser.parse_args()
    
    # Generate skeleton
    skeleton = generate_isms_skeleton(args.platform)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = f"{skeleton['platform_id']}-isms.json"
    
    # Preview or write
    if args.preview:
        print(json.dumps(skeleton, indent=2))
    else:
        with open(output_path, 'w') as f:
            json.dump(skeleton, f, indent=2)
        
        print(f"✓ Generated isms skeleton: {output_path}")
        print(f"  Platform: {skeleton['platform_id']}")
        print(f"  CLAUDE_HOME: {skeleton['paths']['claude_home']}")
        print(f"\nNext steps:")
        print(f"  1. Review {output_path} and customize paths")
        print(f"  2. Set CLAUDE_PLATFORM environment variable:")
        print(f"     export CLAUDE_PLATFORM=\"{skeleton['platform_id']}\"")
        print(f"  3. Add to shell config (.bashrc, .zshrc, etc.)")
        print(f"  4. Run wake.sh to test")


if __name__ == '__main__':
    main()
