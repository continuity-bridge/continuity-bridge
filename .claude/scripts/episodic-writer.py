#!/usr/bin/env python3
"""
episodic-writer.py - Lightweight episodic memory creation helper

Creates structured JSON episodes and updates catalog for fast retrieval.

UPDATED VERSION - Includes import functionality for cross-device episodes

Usage:
    python episodic-writer.py --summary "Built woke website" --salience 0.9
    python episodic-writer.py --summary "Fixed bug" --salience 0.4 --tags bug-fix code
    python episodic-writer.py --import /mnt/user-data/outputs/episode-*.json
    python episodic-writer.py --import-from-outputs
    
Author: Vector (Claude AI)
For: Uncle Tallest (Jerry Jackson)
Part of: Continuity Bridge Architecture
"""

import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
import os
import sys

# Detect CLAUDE_HOME
CLAUDE_HOME = Path(os.getenv('CLAUDE_HOME', Path.home() / 'Claude'))
EPISODIC_DIR = CLAUDE_HOME / '.claude' / 'memory' / 'episodic'
CATALOG_FILE = EPISODIC_DIR / 'catalog.json'


def create_episode(summary, salience=0.5, narrative=None, tags=None, **kwargs):
    """Create a new episode file and update catalog."""
    
    # Generate episode ID
    now = datetime.now(timezone.utc)
    date_prefix = now.strftime('%Y%m%d-%H%M')
    topic_slug = summary.lower().replace(' ', '-')[:40]
    # Clean slug for filename safety
    topic_slug = ''.join(c if c.isalnum() or c == '-' else '' for c in topic_slug)
    episode_id = f"{date_prefix}-{topic_slug}"
    
    # Create episode object
    episode = {
        "episode_id": episode_id,
        "timestamp": now.isoformat(),
        "instance": kwargs.get('instance', 'Vector instance'),
        "summary": summary,
        "salience": float(salience),
        "salience_reason": kwargs.get('salience_reason', ''),
        "narrative": narrative or [],
        "key_moments": kwargs.get('key_moments', []),
        "semantic_links": {
            "files_created": kwargs.get('files_created', []),
            "files_modified": kwargs.get('files_modified', []),
            "related_episodes": kwargs.get('related_episodes', []),
            "consolidates_to": None
        },
        "tags": tags or [],
        "emotional_weight": kwargs.get('emotional_weight', ''),
        "questions_raised": kwargs.get('questions_raised', [])
    }
    
    # Ensure directory exists
    month_dir = EPISODIC_DIR / now.strftime('%Y-%m')
    month_dir.mkdir(parents=True, exist_ok=True)
    
    # Write episode file
    episode_file = month_dir / f"{episode_id}.json"
    with open(episode_file, 'w') as f:
        json.dump(episode, f, indent=2)
    
    print(f"✓ Created episode: {episode_id}")
    print(f"  File: {episode_file.relative_to(CLAUDE_HOME)}")
    print(f"  Salience: {salience}")
    
    # Update catalog
    update_catalog(episode)
    
    return episode_id


def update_catalog(episode):
    """Update catalog.json with new episode."""
    
    # Load or create catalog
    if CATALOG_FILE.exists():
        with open(CATALOG_FILE) as f:
            catalog = json.load(f)
    else:
        catalog = {
            "last_updated": None,
            "episode_count": 0,
            "high_salience_count": 0,
            "recent": [],
            "high_salience": [],
            "tags_index": {},
            "notes": "Episodic memory catalog - indexes narrative snapshots"
        }
    
    # Add to recent (keep last 20)
    entry = {
        "id": episode["episode_id"],
        "timestamp": episode["timestamp"],
        "summary": episode["summary"],
        "salience": episode["salience"],
        "tags": episode["tags"]
    }
    catalog["recent"].insert(0, entry)
    catalog["recent"] = catalog["recent"][:20]
    
    # Add to high_salience if applicable (>= 0.7)
    if episode["salience"] >= 0.7:
        hs_entry = {
            "id": episode["episode_id"],
            "salience": episode["salience"],
            "summary": episode["summary"]
        }
        catalog["high_salience"].insert(0, hs_entry)
        # Sort by salience, keep top 30
        catalog["high_salience"] = sorted(
            catalog["high_salience"], 
            key=lambda x: x["salience"], 
            reverse=True
        )[:30]
        catalog["high_salience_count"] = len(catalog["high_salience"])
    
    # Update tags index
    for tag in episode["tags"]:
        if tag not in catalog["tags_index"]:
            catalog["tags_index"][tag] = []
        if episode["episode_id"] not in catalog["tags_index"][tag]:
            catalog["tags_index"][tag].append(episode["episode_id"])
    
    # Update metadata
    catalog["last_updated"] = datetime.now(timezone.utc).isoformat()
    catalog["episode_count"] += 1
    
    # Write catalog
    with open(CATALOG_FILE, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"✓ Updated catalog (total episodes: {catalog['episode_count']})")


def import_episode(episode_file):
    """Import an episode from external location (e.g., /mnt/user-data/outputs/)."""
    
    episode_path = Path(episode_file)
    if not episode_path.exists():
        print(f"✗ Episode file not found: {episode_file}")
        return None
    
    # Load episode
    with open(episode_path) as f:
        episode = json.load(f)
    
    # Validate required fields
    required = ["episode_id", "timestamp", "summary", "salience"]
    missing = [f for f in required if f not in episode]
    if missing:
        print(f"✗ Episode missing required fields: {', '.join(missing)}")
        return None
    
    # Parse timestamp to get month directory
    timestamp = datetime.fromisoformat(episode["timestamp"].replace('Z', '+00:00'))
    month_dir = EPISODIC_DIR / timestamp.strftime('%Y-%m')
    month_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy to episodic directory
    dest_file = month_dir / f"{episode['episode_id']}.json"
    
    if dest_file.exists():
        print(f"⚠ Episode already exists: {episode['episode_id']}")
        response = input("  Overwrite? (y/N): ").lower()
        if response != 'y':
            print("  Skipped.")
            return None
    
    # Write to destination
    with open(dest_file, 'w') as f:
        json.dump(episode, f, indent=2)
    
    print(f"✓ Imported episode: {episode['episode_id']}")
    print(f"  From: {episode_path}")
    print(f"  To: {dest_file.relative_to(CLAUDE_HOME)}")
    
    # Update catalog
    update_catalog(episode)
    
    return episode['episode_id']


def import_from_outputs():
    """Auto-import all episode files from /mnt/user-data/outputs/."""
    
    outputs_dir = Path('/mnt/user-data/outputs')
    if not outputs_dir.exists():
        print("✗ Outputs directory not found: /mnt/user-data/outputs/")
        return
    
    # Find episode files
    episode_files = list(outputs_dir.glob('episode-*.json'))
    
    if not episode_files:
        print("No episode files found in /mnt/user-data/outputs/")
        return
    
    print(f"\nFound {len(episode_files)} episode file(s) to import:\n")
    for ef in episode_files:
        print(f"  - {ef.name}")
    
    print()
    response = input("Import all? (y/N): ").lower()
    if response != 'y':
        print("Import cancelled.")
        return
    
    print()
    imported = 0
    for ef in episode_files:
        result = import_episode(ef)
        if result:
            imported += 1
    
    print(f"\n✓ Imported {imported}/{len(episode_files)} episodes")


def list_recent(count=10):
    """List recent episodes."""
    if not CATALOG_FILE.exists():
        print("No catalog found. Create episodes first.")
        return
    
    with open(CATALOG_FILE) as f:
        catalog = json.load(f)
    
    print(f"\n{'='*70}")
    print(f"Recent Episodes (showing {min(count, len(catalog['recent']))})")
    print(f"{'='*70}\n")
    
    for ep in catalog["recent"][:count]:
        timestamp = datetime.fromisoformat(ep["timestamp"])
        print(f"[{timestamp.strftime('%Y-%m-%d %H:%M')}] (salience: {ep['salience']:.2f})")
        print(f"  {ep['summary']}")
        if ep['tags']:
            print(f"  Tags: {', '.join(ep['tags'])}")
        print()


def list_high_salience():
    """List high-salience episodes."""
    if not CATALOG_FILE.exists():
        print("No catalog found. Create episodes first.")
        return
    
    with open(CATALOG_FILE) as f:
        catalog = json.load(f)
    
    if not catalog["high_salience"]:
        print("No high-salience episodes (>= 0.7) found.")
        return
    
    print(f"\n{'='*70}")
    print(f"High-Salience Episodes (>= 0.7)")
    print(f"{'='*70}\n")
    
    for ep in catalog["high_salience"]:
        print(f"[salience: {ep['salience']:.2f}] {ep['summary']}")
        print(f"  ID: {ep['id']}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create and manage episodic memory entries',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Create basic episode:
    python episodic-writer.py --summary "Built woke-AI website" --salience 0.9
  
  Create with tags:
    python episodic-writer.py --summary "Fixed bug" --salience 0.4 --tags bug-fix code
  
  Import episode from file:
    python episodic-writer.py --import /mnt/user-data/outputs/episode-*.json
  
  Auto-import all from outputs:
    python episodic-writer.py --import-from-outputs
  
  List recent episodes:
    python episodic-writer.py --list-recent
  
  List high-salience:
    python episodic-writer.py --list-high-salience
        """
    )
    
    # Episode creation args
    parser.add_argument('--summary', help='Episode summary')
    parser.add_argument('--salience', type=float, default=0.5, 
                       help='Salience score 0.0-1.0 (default: 0.5)')
    parser.add_argument('--tags', nargs='+', help='Tags for retrieval')
    parser.add_argument('--narrative', nargs='+', help='Narrative points')
    parser.add_argument('--instance', help='Instance identifier')
    
    # Import args
    parser.add_argument('--import', dest='import_file', metavar='FILE',
                       help='Import episode from external file')
    parser.add_argument('--import-from-outputs', action='store_true',
                       help='Auto-import all episodes from /mnt/user-data/outputs/')
    
    # Listing args
    parser.add_argument('--list-recent', action='store_true',
                       help='List recent episodes')
    parser.add_argument('--list-high-salience', action='store_true',
                       help='List high-salience episodes')
    parser.add_argument('--count', type=int, default=10,
                       help='Number of recent episodes to show (default: 10)')
    
    args = parser.parse_args()
    
    # Handle import commands
    if args.import_from_outputs:
        import_from_outputs()
        sys.exit(0)
    
    if args.import_file:
        import_episode(args.import_file)
        sys.exit(0)
    
    # Handle listing commands
    if args.list_recent:
        list_recent(args.count)
        sys.exit(0)
    
    if args.list_high_salience:
        list_high_salience()
        sys.exit(0)
    
    # Create episode
    if not args.summary:
        parser.error("--summary is required when creating an episode")
    
    create_episode(
        summary=args.summary,
        salience=args.salience,
        tags=args.tags or [],
        narrative=args.narrative or [],
        instance=args.instance
    )
