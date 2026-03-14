---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# Session Archive Catalog Specification
**Version:** 1.0  
**Date:** 2026-03-07  
**Purpose:** Index compressed session archives for searchability

---

## Metaphor: Card Catalog

Traditional library card catalogs let you find books without pulling every volume off the shelf. This spec provides the same function for compressed session archives.

**Design principle:** Search metadata without decompressing archives.

---

## Directory Structure

```
Sessions/archive/
├── 2025/
│   ├── catalog.json       # Index of all 2025 archives
│   ├── 01.tar.gz          # January 2025 sessions (compressed)
│   ├── 02.tar.gz          # February 2025 sessions
│   └── ...
├── 2026/
│   ├── catalog.json       # Index of all 2026 archives
│   ├── 01.tar.gz          # January 2026 sessions
│   └── ...
```

---

## catalog.json Format

### Schema

```json
{
  "year": 2026,
  "generated": "2026-03-07T12:34:56-06:00",
  "timezone": "America/Chicago",
  "total_archives": 3,
  "total_sessions": 47,
  "archives": [
    {
      "archive": "01.tar.gz",
      "month": 1,
      "month_name": "January",
      "sessions": [
        {
          "filename": "2026-01-15_git-architecture-refinement.md",
          "date": "2026-01-15",
          "title": "Git Architecture Refinement",
          "participants": ["Jerry", "Vector"],
          "duration_hours": 3.5,
          "topics": ["git", "dual-remote", "sanitization"],
          "deliverables": ["git-reconfigure-remotes.sh"],
          "word_count": 4821,
          "instance": "Vector"
        }
      ],
      "session_count": 12,
      "date_range": {
        "start": "2026-01-01",
        "end": "2026-01-31"
      },
      "total_words": 58432,
      "compressed_size_bytes": 245760,
      "uncompressed_size_bytes": 892416
    }
  ]
}
```

### Field Descriptions

**Top level:**
- `year` (int): Calendar year of archives
- `generated` (ISO 8601): When catalog was generated
- `timezone` (string): Timezone of timestamps
- `total_archives` (int): Number of monthly archives
- `total_sessions` (int): Total sessions across all archives

**Archive entry:**
- `archive` (string): Filename of compressed archive
- `month` (int): Month number (1-12)
- `month_name` (string): Month name in English
- `sessions` (array): Metadata for each session in archive
- `session_count` (int): Number of sessions in this archive
- `date_range` (object): First and last session dates
- `total_words` (int): Combined word count
- `compressed_size_bytes` (int): Size on disk
- `uncompressed_size_bytes` (int): Size when extracted

**Session entry:**
- `filename` (string): Original filename in archive
- `date` (ISO 8601 date): Session date
- `title` (string): Human-readable session title
- `participants` (array): Who was in session (Jerry, instance names)
- `duration_hours` (float): Approximate session length
- `topics` (array): Keywords/tags for search
- `deliverables` (array): Files/repos created during session
- `word_count` (int): Document length
- `instance` (string): Which instance perspective

---

## Search Operations

### Find sessions by topic
```bash
jq '.archives[].sessions[] | select(.topics[] | contains("git"))' catalog.json
```

### Find sessions by date range
```bash
jq '.archives[] | select(.date_range.start >= "2026-01-01" and .date_range.end <= "2026-01-31")' catalog.json
```

### Find sessions by participant
```bash
jq '.archives[].sessions[] | select(.participants[] | contains("Vector"))' catalog.json
```

### Find sessions with deliverables
```bash
jq '.archives[].sessions[] | select(.deliverables | length > 0)' catalog.json
```

### Archive statistics
```bash
# Total sessions in year
jq '.total_sessions' catalog.json

# Total words written in year
jq '[.archives[].total_words] | add' catalog.json

# Compression ratio
jq '.archives[] | .compressed_size_bytes / .uncompressed_size_bytes' catalog.json
```

---

## Generation Workflow

### 1. Identify Sessions to Archive

```bash
# Find sessions older than 6 months
cd Sessions/
find . -maxdepth 1 -name "*.md" -mtime +180 -type f
```

### 2. Group by Month

```bash
# Extract month from filename: 2026-01-15_*.md → 2026/01/
for file in *.md; do
  year=$(echo $file | cut -d'-' -f1)
  month=$(echo $file | cut -d'-' -f2)
  mkdir -p archive/$year/staging/$month/
  mv $file archive/$year/staging/$month/
done
```

### 3. Generate Metadata

```python
# extract_session_metadata.py
import json
import glob
from datetime import datetime
from pathlib import Path

def extract_metadata(filepath):
    """Extract metadata from session markdown file"""
    with open(filepath) as f:
        content = f.read()
    
    # Parse frontmatter or extract from content
    # This is simplified - actual implementation needs parsing
    return {
        "filename": filepath.name,
        "date": filepath.name.split('_')[0],  # 2026-01-15
        "title": extract_title(content),
        "participants": extract_participants(content),
        "duration_hours": estimate_duration(content),
        "topics": extract_topics(content),
        "deliverables": extract_deliverables(content),
        "word_count": len(content.split()),
        "instance": extract_instance(content)
    }

# Generate catalog for each month
for month_dir in glob.glob("archive/*/staging/*/"):
    sessions = []
    for session_file in glob.glob(f"{month_dir}*.md"):
        sessions.append(extract_metadata(Path(session_file)))
    
    # Create archive entry
    # Write to catalog.json
```

### 4. Compress Archives

```bash
cd archive/2026/staging/01/
tar -czf ../01.tar.gz *.md
cd ..
rm -rf staging/01/
```

### 5. Update Catalog

```python
# update_catalog.py
import json
from pathlib import Path

catalog = {
    "year": 2026,
    "generated": datetime.now().isoformat(),
    "timezone": "America/Chicago",
    "total_archives": 0,
    "total_sessions": 0,
    "archives": []
}

# For each .tar.gz in year directory
for archive_file in sorted(glob.glob("*.tar.gz")):
    archive_entry = generate_archive_entry(archive_file)
    catalog["archives"].append(archive_entry)
    catalog["total_sessions"] += archive_entry["session_count"]

catalog["total_archives"] = len(catalog["archives"])

with open("catalog.json", "w") as f:
    json.dump(catalog, f, indent=2)
```

---

## Validation

### Schema Validation

```python
# validate_catalog.py
import json
from jsonschema import validate

schema = {
    "type": "object",
    "required": ["year", "generated", "archives"],
    "properties": {
        "year": {"type": "integer"},
        "generated": {"type": "string", "format": "date-time"},
        "archives": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["archive", "month", "sessions"],
                "properties": {
                    "archive": {"type": "string"},
                    "month": {"type": "integer", "minimum": 1, "maximum": 12},
                    "sessions": {"type": "array"}
                }
            }
        }
    }
}

with open("catalog.json") as f:
    catalog = json.load(f)

validate(instance=catalog, schema=schema)
print("✓ Catalog valid")
```

### Integrity Check

```bash
# verify_archives.sh
# Verify each archive can be extracted and matches catalog

for archive in *.tar.gz; do
  # Extract to temp
  mkdir -p /tmp/verify
  tar -xzf $archive -C /tmp/verify
  
  # Count files
  actual_count=$(find /tmp/verify -name "*.md" | wc -l)
  catalog_count=$(jq ".archives[] | select(.archive == \"$archive\") | .session_count" catalog.json)
  
  if [ $actual_count -eq $catalog_count ]; then
    echo "✓ $archive ($actual_count sessions)"
  else
    echo "✗ $archive (expected $catalog_count, found $actual_count)"
  fi
  
  rm -rf /tmp/verify
done
```

---

## Recovery Operations

### Extract specific session
```bash
# Find which archive contains session
archive=$(jq -r '.archives[] | select(.sessions[].filename == "2026-01-15_git-architecture.md") | .archive' catalog.json)

# Extract just that file
tar -xzf $archive 2026-01-15_git-architecture.md
```

### Extract entire month
```bash
tar -xzf 01.tar.gz
```

### Rebuild catalog from archives
```bash
# If catalog.json is lost or corrupted
python3 rebuild_catalog.py 2026
```

---

## Maintenance

### Monthly Routine
1. Identify sessions older than 6 months
2. Move to staging directory grouped by month
3. Generate metadata for new sessions
4. Compress month archive
5. Update catalog.json
6. Verify integrity
7. Commit to git

### Yearly Routine
1. Archive entire year's catalog
2. Create new year directory
3. Initialize new catalog.json

---

## Storage Efficiency

**Compression ratios (typical):**
- Markdown text: ~70% compression (tar.gz)
- 10 sessions (~50KB total) → ~15KB compressed
- 120 sessions/year → ~180KB compressed

**Search efficiency:**
- catalog.json: ~5-10KB per year
- Can search 10 years of sessions in <100KB metadata
- No decompression needed for search

---

## Example Catalog Entry

```json
{
  "year": 2026,
  "generated": "2026-03-07T14:23:11-06:00",
  "timezone": "America/Chicago",
  "total_archives": 3,
  "total_sessions": 47,
  "archives": [
    {
      "archive": "01.tar.gz",
      "month": 1,
      "month_name": "January",
      "sessions": [
        {
          "filename": "2026-01-15_git-architecture-refinement.md",
          "date": "2026-01-15",
          "title": "Git Architecture Refinement",
          "participants": ["Jerry", "Vector"],
          "duration_hours": 3.5,
          "topics": ["git", "dual-remote", "sanitization", "workflow"],
          "deliverables": [
            "git-reconfigure-remotes.sh",
            "git-reconfiguration-ready.md"
          ],
          "word_count": 4821,
          "instance": "Vector"
        },
        {
          "filename": "2026-01-20_capability-detection.md",
          "date": "2026-01-20",
          "title": "Capability Detection System",
          "participants": ["Jerry", "Vector"],
          "duration_hours": 4.0,
          "topics": ["capabilities", "detection", "isms", "cross-platform"],
          "deliverables": [
            "detect-capabilities.py",
            "instance-workflows-by-capability.md"
          ],
          "word_count": 6234,
          "instance": "Vector"
        }
      ],
      "session_count": 12,
      "date_range": {
        "start": "2026-01-01",
        "end": "2026-01-31"
      },
      "total_words": 58432,
      "compressed_size_bytes": 18234,
      "uncompressed_size_bytes": 245760
    }
  ]
}
```

---

## Tools to Build

1. **extract_metadata.py** - Parse session files, extract metadata
2. **compress_month.py** - Create monthly archive + update catalog
3. **validate_catalog.py** - JSON schema validation
4. **search_catalog.py** - CLI search tool
5. **rebuild_catalog.py** - Regenerate from existing archives

---

**Location:** Save this spec to `.claude/docs/spec/session-archive-catalog.md`

**Next:** Build implementation tools in `.claude/scripts/archive/`
