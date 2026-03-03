#!/usr/bin/env python3
"""
Preflight environment verification script.
Checks that environment matches -isms configuration.
"""

import json
import os
import sys
import subprocess
from pathlib import Path

def check(condition, message, level='pass'):
    """Print check result."""
    symbols = {'pass': '✓', 'warn': '⚠', 'fail': '✗'}
    print(f"{symbols[level]} {message}")
    return level

def run_cmd(cmd):
    """Run command, return stdout or None."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def load_env_file(env_path):
    """Load variables from .env file into os.environ."""
    if not env_path.exists():
        return
    
    print(f"Loading environment from {env_path}")
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

def get_platform_interactive(repo_root):
    """Ask user to select platform from available -isms files."""
    print("CLAUDE_PLATFORM not set. Scanning for configurations...")
    
    # Try finding isms files in repo root and .claude/
    isms_files = list(repo_root.glob("*-isms.json"))
    isms_files.extend(list((repo_root / ".claude").glob("*-isms.json")))
    
    # Deduplicate by name
    unique_isms = {}
    for p in isms_files:
        name = p.stem.replace('-isms', '')
        if name not in unique_isms:
            unique_isms[name] = p
            
    if not unique_isms:
        print("No *-isms.json configuration files found!")
        return None
    
    print("\nAvailable Platforms:")
    options = sorted(list(unique_isms.keys()))
    for i, name in enumerate(options, 1):
        print(f"{i}. {name}")
    
    while True:
        try:
            choice = input("\nSelect platform (number): ")
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                platform = options[idx]
                break
            print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")
        except KeyboardInterrupt:
            print("\nAborted.")
            sys.exit(1)
            
    print(f"\nSelected: {platform}")
    
    # Offer to save
    save = input("Save to .env for future runs? [Y/n]: ").strip().lower()
    if save in ('', 'y', 'yes'):
        env_path = repo_root / '.env'
        with open(env_path, 'a') as f:
            f.write(f"CLAUDE_PLATFORM={platform}\n")
        print(f"Saved to {env_path}")
        
    return platform

def main():
    print("=== PREFLIGHT CHECKS ===")
    
    # Calculate repository root (assumes script is in .claude/scripts/)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent # .claude/scripts/ -> .claude/ -> root
    
    # Step 0: Load .env
    env_path = repo_root / '.env'
    if env_path.exists():
        load_env_file(env_path)
    
    # Step 1: Platform
    platform = os.getenv('CLAUDE_PLATFORM')
    
    if not platform:
        if sys.stdin.isatty():
            platform = get_platform_interactive(repo_root)
            if platform:
                os.environ['CLAUDE_PLATFORM'] = platform
            else:
                return 1
        else:
            check(False, "CLAUDE_PLATFORM not set", 'fail')
            print("\nFix: export CLAUDE_PLATFORM=android_home")
            return 1
    
    check(True, f"Platform: {platform}")
    
    # Step 2: Load config
    # Try finding it in root or .claude
    isms_filename = f"{platform}-isms.json"
    possible_paths = [
        repo_root / isms_filename,
        repo_root / ".claude" / isms_filename
    ]
    
    config_path = None
    for p in possible_paths:
        if p.exists():
            config_path = p
            break
            
    if not config_path:
        check(False, f"Config not found: {isms_filename}", 'fail')
        return 1
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        check(True, f"Config loaded: {config_path.name}")
    except:
        check(False, f"Config invalid: {config_path.name}", 'fail')
        return 1
    
    # Step 3: Paths
    claude_home = config['paths']['claude_home']
    if Path(claude_home).exists():
        check(True, f"CLAUDE_HOME exists: {claude_home}")
    else:
        check(False, f"CLAUDE_HOME missing: {claude_home}", 'fail')

    # Step 4: Git
    git_config = config['tools']['git']
    git_actual = run_cmd(['git', '--version'])
    if git_actual:
        check(True, f"Git available: {git_actual}")
    else:
        check(False, "Git not found", 'fail')

    # Step 5: Git config checks
    pull_strategy = run_cmd(['git', 'config', 'pull.rebase'])
    if pull_strategy:
        check(True, f"Git pull strategy: {pull_strategy}")
    else:
        check(False, "Git pull strategy not configured", 'warn')
        print("  Fix: git config pull.rebase false")

    # Step 6: Branch
    branch = run_cmd(['git', 'branch', '--show-current'])
    if branch == 'working':
        check(True, f"On branch: {branch}")
    elif branch == 'main':
        check(False, "On main branch (should be on working)", 'warn')
    else:
        check(False, f"On unexpected branch: {branch}", 'warn')

    # Step 7: SSH Key Check
    print("\n--- SSH Key Configuration ---")
    ssh_key_path = Path.home() / '.ssh' / 'continuity-bridge'
    ssh_pub_path = Path.home() / '.ssh' / 'continuity-bridge.pub'
    ssh_config = Path.home() / '.ssh' / 'config'
    
    has_key = ssh_key_path.exists() and ssh_pub_path.exists()
    has_config = ssh_config.exists() and \
                 'github.com-continuity-bridge' in ssh_config.read_text() if ssh_config.exists() else False
    
    if has_key:
        check(True, "SSH key exists")
        
        # Check permissions
        import stat
        key_mode = oct(ssh_key_path.stat().st_mode)[-3:]
        if key_mode == '600':
            check(True, "SSH key permissions correct (600)")
        else:
            check(False, f"SSH key permissions: {key_mode} (should be 600)", 'warn')
            print("  Fix: chmod 600 ~/.ssh/continuity-bridge")
        
        if has_config:
            check(True, "SSH config has continuity-bridge entry")
        else:
            check(False, "SSH config missing continuity-bridge entry", 'warn')
            print("  Fix: Run setup-ssh-key.sh")
        
        # Test GitHub connection
        test_result = run_cmd(['ssh', '-T', 'git@github.com-continuity-bridge'])
        if test_result and 'successfully authenticated' in test_result:
            check(True, "GitHub SSH authentication successful")
        else:
            check(False, "GitHub SSH authentication failed", 'warn')
            print("  Key not added to GitHub yet")
            print("  Instructions: See SSH-SETUP-GUIDE.md")
            print("  Or run: cat ~/.ssh/continuity-bridge.pub")
            print("  Then add to: https://github.com/settings/keys")
    else:
        check(False, "SSH key not found", 'warn')
        print("\n  Continuity Bridge needs an SSH key to sync your private repo.")
        print("  We'll create a dedicated key that won't affect your other keys.")
        print("")
        
        if sys.stdin.isatty():
            setup = input("  Run SSH setup now? [Y/n]: ").strip().lower()
            if setup in ('', 'y', 'yes'):
                setup_script = repo_root / '.claude' / 'scripts' / 'setup-ssh-key.sh'
                if setup_script.exists():
                    print("\n  Running setup-ssh-key.sh...\n")
                    import subprocess
                    result = subprocess.run(['bash', str(setup_script)])
                    if result.returncode == 0:
                        print("\n  SSH key created! Re-run preflight to verify.")
                    else:
                        print("\n  Setup failed. See SSH-SETUP-GUIDE.md for manual instructions.")
                    return result.returncode
                else:
                    print("\n  setup-ssh-key.sh not found")
                    print(f"  Expected at: {setup_script}")
            else:
                print("  Run manually: .claude/scripts/setup-ssh-key.sh")
                print("  Guide: .claude/docs/SSH-SETUP-GUIDE.md")
        else:
            print("  Run: .claude/scripts/setup-ssh-key.sh")
            print("  Guide: .claude/docs/SSH-SETUP-GUIDE.md")

    print("\n=== PREFLIGHT COMPLETE ===")
    return 0

if __name__ == '__main__':
    sys.exit(main())
