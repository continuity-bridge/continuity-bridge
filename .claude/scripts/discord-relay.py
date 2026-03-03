#!/usr/bin/env python3
"""
discord-relay.py - Relay service for instance reports

Watches queue directory for report files and posts them to Discord.
Runs on host system (not in container) to bypass network restrictions.
"""

import json
import time
import requests
import os
from pathlib import Path
from datetime import datetime
import logging
import sys

# Configuration
QUEUE_DIR = Path.home() / "Claude" / ".claude" / "instance-reports-queue"
ARCHIVE_DIR = QUEUE_DIR / "archive"
WEBHOOK_FILE = Path.home() / "Claude" / ".credentials-local" / "discord-instance-reports-webhook.txt"
CHECK_INTERVAL = 2  # seconds
LOG_FILE = Path.home() / "Claude" / ".claude" / "logs" / "discord-relay.log"

# Setup logging
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def load_webhook_url():
    """Load webhook URL from credentials file."""
    if not WEBHOOK_FILE.exists():
        logger.error(f"Webhook URL file not found: {WEBHOOK_FILE}")
        return None
    
    with open(WEBHOOK_FILE) as f:
        url = f.read().strip()
    
    if not url:
        logger.error("Webhook URL is empty")
        return None
    
    return url


def post_to_discord(report_data, webhook_url):
    """Post report to Discord via webhook."""
    
    # Build instance identifier
    instance_id = report_data['instance']
    if report_data.get('platform') and report_data.get('hostname'):
        instance_id += f" ({report_data['platform']}/{report_data['hostname']})"
    
    # Build Discord embed
    title = f"{report_data['emoji']} {report_data['category'].title()} - {instance_id}"
    
    # Footer with salience and context
    footer_text = f"Salience: {report_data['salience']}"
    if report_data.get('context_updated'):
        footer_text += f" • Context: {report_data['context_updated']}"
    
    payload = {
        "embeds": [{
            "title": title,
            "description": report_data['message'],
            "color": report_data['color'],
            "footer": {"text": footer_text},
            "timestamp": report_data['timestamp']
        }]
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        logger.info(f"Posted report from {instance_id} (category: {report_data['category']})")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to post to Discord: {e}")
        return False


def process_report(report_file, webhook_url):
    """Process a single report file."""
    
    try:
        # Read report
        with open(report_file) as f:
            report_data = json.load(f)
        
        # Post to Discord
        if post_to_discord(report_data, webhook_url):
            # Archive successfully posted report
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            archive_path = ARCHIVE_DIR / report_file.name
            report_file.rename(archive_path)
            logger.info(f"Archived: {report_file.name}")
        else:
            logger.warning(f"Failed to post {report_file.name}, will retry later")
    
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {report_file.name}: {e}")
        # Move malformed files to error directory
        error_dir = QUEUE_DIR / "error"
        error_dir.mkdir(parents=True, exist_ok=True)
        report_file.rename(error_dir / report_file.name)
    
    except Exception as e:
        logger.error(f"Error processing {report_file.name}: {e}")


def watch_queue(webhook_url):
    """Watch queue directory and process reports."""
    
    logger.info("Discord relay service started")
    logger.info(f"Watching: {QUEUE_DIR}")
    logger.info(f"Check interval: {CHECK_INTERVAL}s")
    
    # Ensure queue directory exists
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        try:
            # Find all report files (not in subdirectories)
            report_files = sorted(QUEUE_DIR.glob("report-*.json"))
            
            if report_files:
                logger.info(f"Found {len(report_files)} pending report(s)")
                
                for report_file in report_files:
                    process_report(report_file, webhook_url)
            
            time.sleep(CHECK_INTERVAL)
        
        except KeyboardInterrupt:
            logger.info("Shutting down relay service")
            break
        
        except Exception as e:
            logger.error(f"Unexpected error in watch loop: {e}")
            time.sleep(CHECK_INTERVAL)


def main():
    """Main entry point."""
    
    # Load webhook URL
    webhook_url = load_webhook_url()
    if not webhook_url:
        logger.error("Cannot start without webhook URL")
        sys.exit(1)
    
    logger.info("Webhook URL loaded")
    
    # Start watching
    try:
        watch_queue(webhook_url)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

