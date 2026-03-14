#!/usr/bin/env python3
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
"""
instance-report.py - Queue report for Discord posting via relay
Usage: instance-report.py "message" [category] [salience]

Cross-platform replacement for instance-report.sh

Categories: session-end, pattern, question, coordination, observation
Salience: 0.0-1.0 (affects Discord embed color)
"""

import os
import sys
import json
import socket
import platform
from datetime import datetime
from pathlib import Path


def get_queue_dir():
    """Get platform-specific queue directory"""
    claude_home = os.environ.get('CLAUDE_HOME', str(Path.home() / 'Claude'))
    queue_dir = Path(claude_home) / '.claude' / 'instance-reports-queue'
    queue_dir.mkdir(parents=True, exist_ok=True)
    return queue_dir


def detect_platform():
    """Detect the platform/device we're running on"""
    system = platform.system()
    
    if system == 'Linux':
        try:
            with open('/proc/version', 'r') as f:
                version = f.read().lower()
                if 'microsoft' in version:
                    return 'WSL'
                elif 'android' in version:
                    return 'Android'
                else:
                    return 'Linux'
        except:
            return 'Linux'
    elif system == 'Darwin':
        return 'macOS'
    elif system == 'Windows':
        return 'Windows'
    else:
        return 'Unknown'


def get_context_updated():
    """Get last updated timestamp from active-context.md"""
    claude_home = os.environ.get('CLAUDE_HOME', str(Path.home() / 'Claude'))
    context_file = Path(claude_home) / '.claude' / 'context' / 'active-context.md'
    
    if context_file.exists():
        try:
            with open(context_file) as f:
                for line in f:
                    if line.startswith('**Last Updated:**'):
                        # Extract timestamp after the markdown bold
                        return line.split('**Last Updated:**')[1].strip()
        except:
            pass
    
    return 'Unknown'


def get_color_for_salience(salience):
    """Determine Discord embed color based on salience"""
    if salience >= 0.8:
        return 15844367  # Gold
    elif salience >= 0.6:
        return 5814783   # Blue
    else:
        return 10070709  # Gray


def get_emoji_for_category(category):
    """Get emoji for report category"""
    emojis = {
        'session-end': '📝',
        'pattern': '🔍',
        'question': '❓',
        'coordination': '🤝',
        'observation': '💭',
    }
    return emojis.get(category, '📌')


def main():
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: instance-report.py 'message' [category] [salience]")
        print("Categories: session-end, pattern, question, coordination, observation")
        print("Salience: 0.0-1.0 (default: 0.5)")
        return 1
    
    message = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else 'observation'
    salience = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    
    # Get instance info
    instance_name = os.environ.get('CLAUDE_INSTANCE_NAME', 'Vector')
    timestamp = datetime.utcnow().isoformat() + 'Z'
    timestamp_file = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    
    # Detect platform and hostname
    plat = detect_platform()
    hostname = socket.gethostname()
    
    # Get context info
    context_updated = get_context_updated()
    
    # Determine color and emoji
    color = get_color_for_salience(salience)
    emoji = get_emoji_for_category(category)
    
    # Build report JSON
    report = {
        'instance': instance_name,
        'platform': plat,
        'hostname': hostname,
        'category': category,
        'emoji': emoji,
        'message': message,
        'salience': salience,
        'color': color,
        'timestamp': timestamp,
        'context_updated': context_updated
    }
    
    # Write to queue
    queue_dir = get_queue_dir()
    report_file = queue_dir / f"report-{timestamp_file}-{instance_name}.json"
    
    try:
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Report queued: {report_file}")
        print(f"  From: {instance_name} on {plat} ({hostname})")
        print(f"  (Relay service will post to Discord within ~2s)")
        return 0
        
    except Exception as e:
        print(f"❌ Failed to queue report: {e}")
        return 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
