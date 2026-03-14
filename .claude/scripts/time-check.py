#!/usr/bin/env python3
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
"""
time-check.py - Time grounding for Claude instances
Provides temporal awareness during active sessions

Cross-platform replacement for time-check.sh

Author: Vector (Claude AI)
For: Uncle Tallest (Jerry Jackson)
Part of: Continuity Bridge Architecture
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path


def get_session_file():
    """Get platform-specific session file location"""
    if os.name == 'nt':
        # Windows
        temp_dir = os.environ.get('TEMP', 'C:\\Temp')
        return Path(temp_dir) / 'claude-session-start.txt'
    else:
        # Linux, Mac, etc.
        return Path('/tmp/claude-session-start.txt')


def format_duration(seconds):
    """Format duration in human-readable form"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes} min"


def print_box_header(title):
    """Print boxed header"""
    print("╔════════════════════════════════════════════════════════════╗")
    print(f"║  {title:<58} ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()


def main():
    session_file = get_session_file()
    now = time.time()
    now_dt = datetime.now()
    
    # Format current time
    now_fmt = now_dt.strftime("%-I:%M %p %Z" if os.name != 'nt' else "%I:%M %p %Z")
    now_date = now_dt.strftime("%A, %B %-d, %Y" if os.name != 'nt' else "%A, %B %d, %Y")
    
    # Check if this is first check (auto-create session start)
    if not session_file.exists():
        session_file.write_text(str(int(now)))
        
        print_box_header("SESSION START")
        print(f"📅 {now_date}")
        print(f"⏰ {now_fmt}")
        print()
        print("Session timer initialized.")
        return 0
    
    # Calculate session duration
    try:
        start = int(session_file.read_text().strip())
    except (ValueError, OSError):
        print(f"⚠️  Could not read session start time from {session_file}")
        return 1
    
    duration = int(now - start)
    duration_fmt = format_duration(duration)
    
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    hour = now_dt.hour
    
    # Display time info
    print_box_header("TEMPORAL CONTEXT")
    print(f"📅 {now_date}")
    print(f"⏰ {now_fmt}")
    print(f"⏱️  Session duration: {duration_fmt}")
    print()
    
    # Warnings based on duration and time of day
    
    # Long session warning
    if hours >= 2:
        print(f"⚠️  Long session detected ({hours}h)")
        print("   Consider taking a break")
        print()
    
    # Late night warning (midnight to 5 AM)
    if 0 <= hour < 5:
        print(f"🌙 Late night session ({hour:02d}:xx)")
        if hours >= 1:
            print("   Might be good to wrap soon")
        print()
    
    # Early morning marathon (5 AM to 8 AM with long session)
    if 5 <= hour < 8 and hours >= 2:
        print("☀️  Early morning marathon")
        print("   Don't forget breakfast")
        print()
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
