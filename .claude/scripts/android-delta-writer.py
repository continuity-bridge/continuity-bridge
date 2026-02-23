#!/usr/bin/env python3
"""
Android Session Delta Writer

Usage: At end of Android session, instance calls this to generate delta file.
Output goes to /mnt/user-data/outputs/ for Jerry to download.
"""

import yaml
import hashlib
from datetime import datetime, timezone

def generate_delta(session_summary: dict) -> dict:
    """
    Generate a delta structure from session work.
    
    Args:
        session_summary: Dict with session details, changes made, etc.
    
    Returns:
        Complete delta structure ready to serialize
    """
    
    now = datetime.now(timezone.utc)
    session_id = f"android-{now.strftime('%Y%m%d-%H%M')}"
    
    delta = {
        # Metadata
        'session_id': session_id,
        'timestamp': now.isoformat(),
        'source': 'android',
        'base_state': session_summary.get('base_state', {}),
        
        # File changes
        'file_changes': session_summary.get('file_changes', []),
        
        # Session log
        'session_log': {
            'summary': session_summary.get('summary', ''),
            'topics': session_summary.get('topics', []),
            'key_decisions': session_summary.get('key_decisions', []),
            'next_steps': session_summary.get('next_steps', []),
            'significant_artifacts': session_summary.get('artifacts', []),
            'notes': session_summary.get('notes', '')
        },
        
        # Conflict handling
        'conflict_strategy': 'prompt',
        'notes': session_summary.get('merge_notes', '')
    }
    
    return delta


def hash_content(content: str) -> str:
    """Generate SHA256 hash of content."""
    return f"sha256:{hashlib.sha256(content.encode()).hexdigest()[:16]}"


def write_delta(delta: dict, output_path: str):
    """Write delta to YAML file."""
    with open(output_path, 'w') as f:
        yaml.dump(delta, f, default_flow_style=False, sort_keys=False, width=80)


# Example usage for instance to follow:
if __name__ == '__main__':
    # Instance would construct this from session work
    session_summary = {
        'base_state': {
            'essential_md_hash': 'sha256:abc123...',  # From uploaded file
            'active_context_hash': 'sha256:def456...',
            'read_at': '2026-02-22T14:00:00Z'
        },
        
        'file_changes': [
            {
                'file': '.claude/context/active-context.md',
                'operations': [
                    {
                        'type': 'update_section',
                        'section': '## Current Work',
                        'find': 'Previous work description',
                        'replace': 'New work description from Android session'
                    },
                    {
                        'type': 'append_to_section',
                        'section': '## Pending Decisions',
                        'content': '- New item from Android session\n'
                    }
                ]
            }
        ],
        
        'summary': 'Example Android session with delta generation',
        'topics': ['delta-merge', 'android-continuity'],
        'key_decisions': ['Adopted delta-merge workflow'],
        'next_steps': ['Test on desktop instance'],
        'artifacts': [],
        'notes': 'First test of delta workflow',
        'merge_notes': 'Standard merge, no special handling needed'
    }
    
    # Generate and write
    delta = generate_delta(session_summary)
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')
    output_path = f'/mnt/user-data/outputs/android-delta-{timestamp}.yaml'
    
    write_delta(delta, output_path)
    print(f"Delta written to: {output_path}")
    print("Ready for download and desktop merge.")
