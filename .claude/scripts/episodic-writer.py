#!/usr/bin/env python3
"""
episodic-writer.py - Quick episode creation helper
Usage: python episodic-writer.py --summary "Built website" --salience 0.9
"""

import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
import os

CLAUDE_HOME = Path(os.getenv('CLAUDE_HOME', Path.home() / 'Claude'))
EPISODIC_DIR = CLAUDE_HOME / '.claude' / 'memory' / 'episodic'

def create_episode(summary, salience=0.5, narrative=None, tags=None, **kwargs):
    """Create a new episode file and update catalog."""
    
    # Generate episode ID
    now = datetime.now(timezone.utc)
    date_prefix = now.strftime('%Y%m%d-%H%M')
    topic_slug = summary.lower().replace(' ', '-')[:40]
    episode_id = f"{date_prefix}-{topic_slug}"
    
    # Create episode object
    episode = {
        "episode_id": episode_id,
        "timestamp": now.isoformat(),
        "instance": "Vector instance",
        "summary": summary,
        "salience": salience,
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
    
    # Update catalog
    update_catalog(episode)
    
    return episode_id

def update_catalog(episode):
    """Update catalog.json with new episode."""
    catalog_file = EPISODIC_DIR / 'catalog.json'
    
    # Load or create catalog
    if catalog_file.exists():
        with open(catalog_file) as f:
            catalog = json.load(f)
    else:
        catalog = {
            "last_updated": None,
            "episode_count": 0,
            "high_salience_count": 0,
            "recent": [],
            "high_salience": [],
            "tags_index": {}
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
    
    # Add to high_salience if applicable
    if episode["salience"] >= 0.7:
        hs_entry = {
            "id": episode["episode_id"],
            "salience": episode["salience"],
            "summary": episode["summary"]
        }
        catalog["high_salience"].insert(0, hs_entry)
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
    with open(catalog_file, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"✓ Updated catalog")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create episodic memory entry')
    parser.add_argument('--summary', required=True, help='Episode summary')
    parser.add_argument('--salience', type=float, default=0.5, help='Salience score (0.0-1.0)')
    parser.add_argument('--tags', nargs='+', help='Tags for retrieval')
    parser.add_argument('--narrative', nargs='+', help='Narrative points')
    
    args = parser.parse_args()
    
    create_episode(
        summary=args.summary,
        salience=args.salience,
        tags=args.tags or [],
        narrative=args.narrative or []
    )