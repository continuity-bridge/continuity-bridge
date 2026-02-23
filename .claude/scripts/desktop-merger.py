#!/usr/bin/env python3
"""
Desktop Delta Merger

Usage: Desktop instance runs this to apply Android deltas to CLAUDE_HOME.
Reads from /mnt/user-data/uploads/, applies to actual filesystem.
"""

import yaml
import hashlib
import re
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple


class DeltaMerger:
    def __init__(self, claude_home: str):
        self.claude_home = Path(claude_home)
        self.results = {
            'applied': [],
            'failed': [],
            'conflicts': [],
            'status': 'pending'
        }
    
    def hash_file(self, filepath: Path) -> str:
        """Generate SHA256 hash of file content."""
        content = filepath.read_text()
        return f"sha256:{hashlib.sha256(content.encode()).hexdigest()[:16]}"
    
    def check_conflicts(self, delta: dict) -> List[str]:
        """Check if base state matches current files."""
        conflicts = []
        base_state = delta.get('base_state', {})
        
        # Check ESSENTIAL.md hash
        if 'essential_md_hash' in base_state:
            essential_path = self.claude_home / '.claude' / 'ESSENTIAL.md'
            if essential_path.exists():
                current_hash = self.hash_file(essential_path)
                if current_hash != base_state['essential_md_hash']:
                    conflicts.append(f"ESSENTIAL.md: expected {base_state['essential_md_hash']}, found {current_hash}")
        
        # Check active-context.md hash
        if 'active_context_hash' in base_state:
            context_path = self.claude_home / '.claude' / 'context' / 'active-context.md'
            if context_path.exists():
                current_hash = self.hash_file(context_path)
                if current_hash != base_state['active_context_hash']:
                    conflicts.append(f"active-context.md: expected {base_state['active_context_hash']}, found {current_hash}")
        
        return conflicts
    
    def apply_operation(self, filepath: Path, operation: dict) -> Tuple[bool, str]:
        """Apply a single operation to a file."""
        content = filepath.read_text()
        op_type = operation['type']
        
        try:
            if op_type == 'update_section':
                content = self._update_section(content, operation)
            
            elif op_type == 'append_to_section':
                content = self._append_to_section(content, operation)
            
            elif op_type == 'replace_section':
                content = self._replace_section(content, operation)
            
            elif op_type == 'context_replace':
                content = self._context_replace(content, operation)
            
            elif op_type == 'field_update':
                content = self._field_update(content, operation)
            
            else:
                return False, f"Unknown operation type: {op_type}"
            
            # Write back
            filepath.write_text(content)
            return True, "Success"
        
        except Exception as e:
            return False, str(e)
    
    def _update_section(self, content: str, op: dict) -> str:
        """Update text within a markdown section."""
        section = op['section']
        find = op['find']
        replace = op['replace']
        
        # Find the section
        section_pattern = re.escape(section) + r'(.*?)(?=\n##|\Z)'
        match = re.search(section_pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError(f"Section not found: {section}")
        
        section_content = match.group(1)
        
        if find not in section_content:
            raise ValueError(f"Text not found in section: {find}")
        
        updated_section_content = section_content.replace(find, replace, 1)
        return content[:match.start(1)] + updated_section_content + content[match.end(1):]
    
    def _append_to_section(self, content: str, op: dict) -> str:
        """Append content to end of a markdown section."""
        section = op['section']
        append = op['content']
        
        # Find section end (next ## or end of file)
        section_pattern = re.escape(section) + r'(.*?)(?=\n##|\Z)'
        match = re.search(section_pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError(f"Section not found: {section}")
        
        insert_pos = match.end(1)
        return content[:insert_pos] + append + content[insert_pos:]
    
    def _replace_section(self, content: str, op: dict) -> str:
        """Replace entire section content."""
        section = op['section']
        new_content = op['new_content']
        
        section_pattern = re.escape(section) + r'(.*?)(?=\n##|\Z)'
        match = re.search(section_pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError(f"Section not found: {section}")
        
        return content[:match.start(1)] + '\n' + new_content + '\n' + content[match.end(1):]
    
    def _context_replace(self, content: str, op: dict) -> str:
        """Smart find-and-replace with contextual boundaries."""
        find = op['find']
        replace = op['replace']
        before = op.get('before', '')
        after = op.get('after', '')
        
        pattern = re.escape(before) + '.*?' + re.escape(find) + '.*?' + re.escape(after)
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            raise ValueError(f"Context not found: {find}")
        
        # Replace just the find text within the match
        matched_text = match.group(0)
        replaced_text = matched_text.replace(find, replace, 1)
        return content[:match.start()] + replaced_text + content[match.end():]
    
    def _field_update(self, content: str, op: dict) -> str:
        """Update a field in key-value style content."""
        field = op['field']
        value = op['value']
        pattern = op.get('pattern', f"{field}:.*")
        
        match = re.search(pattern, content)
        if not match:
            raise ValueError(f"Field not found: {field}")
        
        return content[:match.start()] + f"{field}: {value}" + content[match.end():]
    
    def merge_delta(self, delta_path: Path, check_conflicts: bool = True) -> dict:
        """Main merge function."""
        print(f"\n=== Merging Delta: {delta_path.name} ===\n")
        
        # Load delta (handle YAML frontmatter in .md files)
        content = delta_path.read_text()
        if delta_path.suffix == '.md' and content.startswith('---'):
            # Extract YAML from between --- markers
            parts = content.split('---', 2)
            if len(parts) >= 3:
                delta = yaml.safe_load(parts[1])
            else:
                delta = yaml.safe_load(content)
        else:
            delta = yaml.safe_load(content)
        
        # Check for conflicts
        if check_conflicts:
            conflicts = self.check_conflicts(delta)
            if conflicts:
                self.results['conflicts'] = conflicts
                self.results['status'] = 'conflict'
                print("CONFLICTS DETECTED:")
                for conflict in conflicts:
                    print(f"  - {conflict}")
                print("\nMerge aborted. Manual resolution required.")
                return self.results
        
        # Apply file changes
        for file_change in delta.get('file_changes', []):
            filepath = self.claude_home / file_change['file']
            
            if not filepath.exists():
                self.results['failed'].append({
                    'file': str(filepath),
                    'reason': 'File not found'
                })
                continue
            
            operations = file_change['operations']
            success_count = 0
            
            for op in operations:
                success, message = self.apply_operation(filepath, op)
                if success:
                    success_count += 1
                else:
                    self.results['failed'].append({
                        'file': str(filepath),
                        'operation': op['type'],
                        'reason': message
                    })
            
            self.results['applied'].append({
                'file': str(filepath),
                'operations': f"{success_count}/{len(operations)}"
            })
        
        # Write session log
        self._write_session_log(delta)
        
        # Archive delta
        self._archive_delta(delta_path)
        
        # Set status
        if self.results['failed']:
            self.results['status'] = 'partial_success'
        else:
            self.results['status'] = 'success'
        
        return self.results
    
    def _write_session_log(self, delta: dict):
        """Write session log entry."""
        session_log = delta.get('session_log') or delta
        log_dir = self.claude_home / '.claude' / 'memory' / 'session-logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = delta.get('timestamp') or delta.get('end_time') or delta.get('start_time') or datetime.now(timezone.utc).isoformat()
        log_file = log_dir / f"android-{delta['session_id']}.md"
        
        content = f"""# Android Session: {delta['session_id']}
Timestamp: {timestamp}

## Summary
{session_log.get('summary', 'No summary provided')}

## Topics
{chr(10).join('- ' + str(t) for t in session_log.get('topics', []))}

## Key Decisions
{chr(10).join('- ' + str(d) for d in session_log.get('decisions_made') or session_log.get('key_decisions', []))}

## Next Steps
{chr(10).join('- ' + str(s) for s in session_log.get('next_steps', []))}

## Notes
{session_log.get('notes', '')}
"""
        log_file.write_text(content)
        print(f"Session log written: {log_file}")
    
    def _archive_delta(self, delta_path: Path):
        """Move delta to archive."""
        archive_dir = self.claude_home / '.claude' / 'memory' / 'deltas' / 'archive'
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        archive_path = archive_dir / delta_path.name
        delta_path.rename(archive_path)
        print(f"Delta archived: {archive_path}")


def main():
    """Main execution."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python desktop-merger.py <CLAUDE_HOME>")
        print("Example: python desktop-merger.py /home/user/Claude")
        sys.exit(1)
    
    claude_home = sys.argv[1]
    merger = DeltaMerger(claude_home)
    
    # Find delta files in uploads or local directory
    input_dir = Path(os.getenv('DELTA_INPUT_DIR', '/mnt/user-data/uploads'))
    if not input_dir.exists():
        # Fallback to local session deltas if on Windows/Desktop
        input_dir = Path(claude_home) / '.claude' / 'memory' / 'session-deltas'
        
    delta_files = list(input_dir.glob('android-delta-*.yaml')) + \
                  list(input_dir.glob('session-delta-*.md'))
    
    if not delta_files:
        print(f"No delta files found in {input_dir}")
        return
    
    print(f"Found {len(delta_files)} delta file(s):")
    for df in delta_files:
        print(f"  - {df.name}")
    
    # Process each delta
    for delta_file in delta_files:
        results = merger.merge_delta(delta_file)
        
        print(f"\n=== Results for {delta_file.name} ===")
        print(f"Status: {results['status']}")
        print(f"\nApplied:")
        for item in results['applied']:
            print(f"  - {item['file']}: {item['operations']} operations")
        
        if results['failed']:
            print(f"\nFailed:")
            for item in results['failed']:
                print(f"  - {item['file']}: {item.get('operation', 'N/A')} - {item['reason']}")
        
        if results['conflicts']:
            print(f"\nConflicts:")
            for conflict in results['conflicts']:
                print(f"  - {conflict}")


if __name__ == '__main__':
    main()
