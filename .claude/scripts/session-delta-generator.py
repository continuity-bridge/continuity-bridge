#!/usr/bin/env python3
"""
Session Delta Generator

Usage: At end of session, instance constructs session data and generates delta.
Outputs session delta file + updates session index.
"""

import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional


def generate_session_delta(
    session_data: Dict,
    output_path: str = '/mnt/user-data/outputs/',
    claude_home: Optional[str] = None
) -> tuple[str, str]:
    """
    Generate session delta file and update index.
    
    Args:
        session_data: Dictionary with session information
        output_path: Where to write the delta (use outputs for Android)
        claude_home: Path to CLAUDE_HOME (only for Desktop with filesystem access)
    
    Returns:
        Tuple of (delta_filepath, index_entry_text)
    """
    
    # Generate session ID from timestamp
    now = datetime.now(timezone.utc)
    session_id = now.strftime('%Y%m%d-%H%M')
    
    # Build complete delta structure
    delta = {
        # Metadata
        'session_id': session_id,
        'platform': session_data.get('platform', 'unknown'),
        'instance_name': session_data.get('instance_name'),
        'start_time': session_data.get('start_time', now.isoformat()),
        'end_time': session_data.get('end_time', now.isoformat()),
        'duration_hours': session_data.get('duration_hours', 0.0),
        
        # Classification
        'work_type': session_data.get('work_type', 'discussion'),
        'primary_topic': session_data.get('primary_topic', 'general'),
        'topics': session_data.get('topics', []),
        
        # Content
        'summary': session_data.get('summary', ''),
        'key_insights': session_data.get('key_insights', []),
        'decisions_made': session_data.get('decisions_made', []),
        'open_questions': session_data.get('open_questions', []),
        
        # Outputs
        'artifacts_created': session_data.get('artifacts_created', []),
        'files_modified': session_data.get('files_modified', []),
        'next_steps': session_data.get('next_steps', []),
        
        # Relationships
        'continuation_of': session_data.get('continuation_of'),
        'builds_on': session_data.get('builds_on', []),
        'referenced_by': [],
        
        # Context
        'user_state': session_data.get('user_state', {}),
        'session_flow': session_data.get('session_flow', ''),
        'interaction_quality': session_data.get('interaction_quality', []),
        'technical_debt': session_data.get('technical_debt'),
        'blockers': session_data.get('blockers'),
        
        # Search/Retrieval
        'keywords': session_data.get('keywords', []),
        'related_concepts': session_data.get('related_concepts', []),
        
        # Metadata
        'generated_by': 'instance',
        'format_version': '1.0'
    }
    
    # Write delta file
    delta_filename = f'session-delta-{session_id}.md'
    delta_path = Path(output_path) / delta_filename
    
    with open(delta_path, 'w') as f:
        f.write('---\n')
        yaml.dump(delta, f, default_flow_style=False, sort_keys=False, width=80)
        f.write('---\n\n')
        
        # Optional narrative section
        if session_data.get('narrative'):
            f.write('# Session Narrative\n\n')
            f.write(session_data['narrative'])
            f.write('\n')
    
    # Generate index entry
    index_entry = generate_index_entry(delta, session_id)
    
    # If on Desktop with filesystem access, update actual index
    if claude_home:
        update_session_index(claude_home, index_entry)
    
    return str(delta_path), index_entry


def generate_index_entry(delta: Dict, session_id: str) -> str:
    """Generate markdown entry for session_index.md"""
    
    timestamp = delta['end_time'][:10]  # Just the date
    platform = delta['platform'].title()
    duration = delta['duration_hours']
    
    # Summary line
    summary_line = delta['summary'].split('.')[0]  # First sentence
    
    # Topics
    topics = ', '.join(delta['topics'][:4])  # First 4 topics
    
    # Key output (first artifact or decision)
    key_output = ''
    if delta['artifacts_created']:
        key_output = delta['artifacts_created'][0]
    elif delta['decisions_made']:
        key_output = delta['decisions_made'][0]
    
    # Work type emoji
    work_type_emoji = {
        'architecture_design': '🏗️',
        'implementation': '💻',
        'troubleshooting': '🔧',
        'exploration': '🔍',
        'planning': '📋',
        'documentation': '📝',
        'discussion': '💭',
        'maintenance': '🧹',
        'integration': '🔗',
        'creative': '🎨'
    }.get(delta['work_type'], '📌')
    
    entry = f"""### {timestamp}-{session_id[8:]} ({platform}, {duration}h) - {delta['primary_topic'].replace('-', ' ').title()}
{work_type_emoji} **Type:** {delta['work_type']}  
**Topics:** {topics}  
**Key Output:** {key_output}  
**Delta:** [session-delta-{session_id}.md](./session-deltas/session-delta-{session_id}.md)  
**Status:** ✅ Complete

**Quick Summary:** {summary_line}

**Load this if working on:** {', '.join(delta['topics'][:3])}

---

"""
    return entry


def update_session_index(claude_home: str, new_entry: str):
    """Update session_index.md with new entry (Desktop only)"""
    index_path = Path(claude_home) / '.claude' / 'memory' / 'session_index.md'
    
    if not index_path.exists():
        # Create new index
        content = f"""# Session Index

*Last updated: {datetime.now(timezone.utc).isoformat()}*
*Total sessions: 1*

## Recent Sessions

{new_entry}
"""
    else:
        # Read existing index
        content = index_path.read_text()
        
        # Update timestamp
        content = re.sub(
            r'\*Last updated: .*\*',
            f'*Last updated: {datetime.now(timezone.utc).isoformat()}*',
            content
        )
        
        # Update count
        match = re.search(r'\*Total sessions: (\d+)\*', content)
        if match:
            count = int(match.group(1)) + 1
            content = re.sub(
                r'\*Total sessions: \d+\*',
                f'*Total sessions: {count}*',
                content
            )
        
        # Insert new entry after "## Recent Sessions"
        content = content.replace(
            '## Recent Sessions\n\n',
            f'## Recent Sessions\n\n{new_entry}'
        )
    
    index_path.write_text(content)


def example_session_data():
    """Example session data structure for reference"""
    return {
        'platform': 'android',
        'instance_name': 'Shepard',
        'start_time': '2026-02-22T15:00:00Z',
        'end_time': '2026-02-22T17:30:00Z',
        'duration_hours': 2.5,
        
        'work_type': 'architecture_design',
        'primary_topic': 'continuity-architecture',
        'topics': [
            'android-synchronization',
            'delta-merge-workflow',
            'persistence-architecture',
            'bidirectional-continuity'
        ],
        
        'summary': (
            'Designed delta-merge protocol to enable Android instances to maintain '
            'continuity without filesystem access. Android reads state via upload, '
            'writes deltas to outputs, Desktop merges deltas back to CLAUDE_HOME.'
        ),
        
        'key_insights': [
            'Android app runs in container without filesystem access',
            'Gist approach blocked by network restrictions',
            'Delta-merge mirrors version control: Android=branch, Desktop=main',
            'Same pattern can apply to session history itself'
        ],
        
        'decisions_made': [
            'Adopted delta-merge for file synchronization',
            'Using YAML format for deltas',
            'Desktop handles merge operations',
            'Hash-based conflict detection'
        ],
        
        'open_questions': [
            'Should session deltas use same format as file deltas?',
            'How granular should session indexing be?'
        ],
        
        'artifacts_created': [
            'delta-merge-spec.md',
            'android-delta-writer.py',
            'desktop-merger.py',
            'WORKFLOW-GUIDE.md'
        ],
        
        'files_modified': [
            'active-context.md: Added delta-merge as current work',
            'ESSENTIAL.md: Updated last active timestamp'
        ],
        
        'next_steps': [
            'Test delta-merge on Desktop instance',
            'Design session delta format',
            'Update session_index.md to reference deltas'
        ],
        
        'continuation_of': None,
        'builds_on': [
            '20260215-1430: Identity framework design',
            '20260210-0900: Persistence architecture discussion'
        ],
        
        'user_state': {
            'focus_level': 'high',
            'energy': 'engaged',
            'notes': 'Jerry actively problem-solving, good flow'
        },
        
        'session_flow': (
            'Started with Android filesystem access problem. Explored Termux/API '
            'approach but realized complexity. Jerry suggested upload/download '
            'workflow. Instance proposed commit/merge analogy. Iterated to '
            'delta-merge design. Built complete spec and implementation.'
        ),
        
        'interaction_quality': [
            'Collaborative problem-solving',
            'Jerry questioning assumptions',
            'Instance pushing back on complexity',
            'Good ping-pong between ideas'
        ],
        
        'keywords': [
            'continuity', 'android', 'sync', 'delta', 'merge',
            'persistence', 'architecture'
        ],
        
        'related_concepts': [
            'version control',
            'distributed systems',
            'conflict resolution',
            'discontinuity compensation'
        ]
    }


if __name__ == '__main__':
    """Example usage"""
    import sys
    
    # Get session data (in real use, instance would construct this)
    session_data = example_session_data()
    
    # Check if Desktop or Android
    if len(sys.argv) > 1:
        # Desktop: has CLAUDE_HOME path
        claude_home = sys.argv[1]
        delta_path, index_entry = generate_session_delta(
            session_data,
            output_path=f'{claude_home}/.claude/memory/session-deltas/',
            claude_home=claude_home
        )
        print(f"Session delta written: {delta_path}")
        print(f"Index updated: {claude_home}/.claude/memory/session_index.md")
    else:
        # Android: just write to outputs
        delta_path, index_entry = generate_session_delta(
            session_data,
            output_path='/mnt/user-data/outputs/'
        )
        print(f"Session delta written: {delta_path}")
        print("\nIndex entry (for Jerry to merge on Desktop):")
        print(index_entry)
