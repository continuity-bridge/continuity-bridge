#!/usr/bin/env python3
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
"""
wake.py - Cross-platform Continuity Bridge Wake Sequence
Works on Windows, Linux, Mac without modification

Version: 0.2.1
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import datetime


def run_script(script_path, description, optional=False):
    """Run a Python script and return success status"""
    print(f"Running {description}...")
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✓ {description} passed")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            if optional:
                print(f"⚠ {description} failed (optional)")
                if result.stderr:
                    print(result.stderr)
                return True
            else:
                print(f"✗ {description} failed")
                if result.stderr:
                    print(result.stderr)
                return False
                
    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out")
        return False if not optional else True
    except Exception as e:
        print(f"✗ {description} error: {e}")
        return False if not optional else True


def print_header():
    """Print wake sequence header"""
    print("=" * 70)
    print("CONTINUITY BRIDGE - WAKE SEQUENCE v0.2.1 (Python)")
    print("=" * 70)
    print()


def load_environment_vars(script_output):
    """Parse environment variables from script output"""
    env_vars = {}
    for line in script_output.split('\n'):
        if line.startswith('export '):
            # Parse "export VAR=value" format
            line = line[7:]  # Remove "export "
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
                os.environ[key] = value
    return env_vars


def main():
    print_header()
    
    # Determine script directory
    script_dir = Path(__file__).parent
    
    # Step -3: Location Check
    print("[Step -3] Location Check...")
    location_script = script_dir / "location-check.py"
    
    if not location_script.exists():
        print("✗ location-check.py not found")
        print(f"  Expected at: {location_script}")
        sys.exit(1)
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        result = subprocess.run(
            [sys.executable, str(location_script)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env,
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse exports
            env_vars = load_environment_vars(result.stdout)
            
            # Show human-readable output from stderr
            for line in result.stderr.split('\n'):
                if line.strip():
                    print(f"  {line}")
            
            print(f"✓ Location detected")
            print(f"  System: {env_vars.get('CURRENT_SYSTEM', 'unknown')}")
            print(f"  Context: {env_vars.get('EXECUTION_CONTEXT', 'unknown')}")
            print(f"  CLAUDE_HOME: {env_vars.get('CLAUDE_HOME', 'unknown')}")
        else:
            print("✗ Location detection failed")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"✗ Location detection error: {e}")
        sys.exit(1)
    
    print()
    
    # Get CLAUDE_HOME from environment
    claude_home = os.environ.get('CLAUDE_HOME')
    if not claude_home:
        print("✗ CLAUDE_HOME not set")
        sys.exit(1)
    
    claude_dir = Path(claude_home) / '.claude'
    scripts_dir = claude_dir / 'scripts'
    
    # Step -2: Preflight Checks
    print("[Step -2] Preflight Checks...")
    preflight = scripts_dir / "preflight.py"
    if preflight.exists():
        print(f"Preflight exists: {preflight}")
        if not run_script(preflight, "Preflight"):
            response = input("Continue anyway? [y/N]: ")
            if response.lower() not in ('y', 'yes'):
                print("Aborted.")
                sys.exit(1)
    else:
        print("⚠ preflight.py not found (skipping)")
    print()
    
    # Step -1: Heartbeat Check
    print("[Step -1] Heartbeat Check...")
    heartbeat = scripts_dir / "heartbeat-check.py"
    if heartbeat.exists():
        if not run_script(heartbeat, "Heartbeat", optional=False):
            print("✗ Heartbeat failed - critical paths missing")
            sys.exit(1)
    else:
        print("⚠ heartbeat-check.py not found (skipping)")
    print()
    
    # Step 0: Capability Detection
    print("[Step 0] Detecting Capabilities...")
    detect_cap = scripts_dir / "detect-capabilities.py"
    if detect_cap.exists():
        run_script(detect_cap, "Capability detection", optional=False)
    else:
        print("⚠ detect-capabilities.py not found (skipping)")
    print()
    
    # Step 1: Load Runtime Manifest
    print("[Step 1] Runtime manifest...")
    manifest_path = claude_dir / "capabilities-manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path, encoding='utf-8') as f:
                manifest = json.load(f)
            
            print(f"  Substrate: {manifest.get('substrate', {}).get('type', 'unknown')}")
            print(f"  Workflow: {manifest.get('workflow', 'unknown')}")
            print(f"  CLAUDE_HOME: {manifest.get('substrate', {}).get('claude_home', 'unknown')}")
        except Exception as e:
            print(f"⚠ Could not load manifest: {e}")
    else:
        print("⚠ No runtime manifest found")
    print()
    
    # Step 2: Load Anchors
    print("[Step 2] Anchors...")
    anchors_path = claude_dir / "anchors.json"
    if anchors_path.exists():
        try:
            with open(anchors_path, encoding='utf-8') as f:
                anchors = json.load(f)
            
            archetype = anchors.get('archetype', 'unknown')
            blend = anchors.get('archetype_blend', [])
            
            if blend:
                print(f"  Archetype: {archetype} + {' + '.join(blend)}")
            else:
                print(f"  Archetype: {archetype}")
        except Exception as e:
            print(f"⚠ Could not load anchors: {e}")
    else:
        print("⚠ No anchors.json found")
    print()
    
    # Step 3: Check for Ollama (optional)
    print("[Step 3] Checking for local LLM...")
    ollama_hooks = scripts_dir / "ollama-hooks.py"
    if ollama_hooks.exists():
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        result = subprocess.run(
            [sys.executable, str(ollama_hooks), "check"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ Ollama available")
        else:
            print("  Ollama not running (optional)")
    else:
        print("  Ollama hooks not installed (optional)")
    print()
    
    # Step 4: Temporal Context
    print("[Step 4] Temporal context...")
    pulse_file = claude_dir / "logs" / "bridge.pulse"
    if pulse_file.exists():
        try:
            temporal_anchor = pulse_file.read_text(encoding='utf-8').strip()
            print(f"  Temporal Anchor: {temporal_anchor}")
        except Exception as e:
            print(f"⚠ Could not read bridge.pulse: {e}")
    else:
        print("⚠ bridge.pulse not found")
    
    # Log wake event
    wake_log = claude_dir / "logs" / "wake.log"
    wake_log.parent.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    now = datetime.now().astimezone()
    # Uses your preferred format: 03/03/2026 19:46:10
    # Adding Timezone (Z) for cross-platform alignment
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S %Z")
    
    with open(wake_log, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} - Wake sequence completed (Python)\n")
    
    print("[Step 4] Wake event logged")
    print()
    
    # Final status
    print("=" * 70)
    print("WAKE SEQUENCE COMPLETE")
    print("=" * 70)
    print()
    print("System ready. Instance can begin work.")
    print()
    
    # Optional quick reference
    index_file = Path(claude_home) / "INDEX.md"
    if index_file.exists():
        print("Quick start: cat INDEX.md")
    
    onboarding = Path(claude_home) / "Docs" / "ONBOARDING.md"
    if onboarding.exists():
        print("New user guide: cat Docs/ONBOARDING.md")
    
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nWake sequence interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
