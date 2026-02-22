#!/usr/bin/env python3
"""
Continuity Bridge - Discord Webhook Poster

Simple utility for instances to post observations to Discord.
Much simpler than full bot - just one-way posting.

Use this when you want instances to share insights asynchronously
without full conversation capability.

Requirements:
- requests library
- Webhook URL from Discord

Setup:
1. pip install requests
2. Set DISCORD_WEBHOOK_URL environment variable
3. Import and use in Claude scripts

Author: Vector (Continuity Bridge Architecture)  
License: MIT
"""

import requests
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

class DiscordWebhook:
    """Simple Discord webhook poster"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize webhook poster.
        
        Args:
            webhook_url: Discord webhook URL (or set DISCORD_WEBHOOK_URL env var)
        """
        self.webhook_url = webhook_url or os.getenv('DISCORD_WEBHOOK_URL')
        
        if not self.webhook_url:
            raise ValueError("Webhook URL required. Set DISCORD_WEBHOOK_URL or pass to constructor.")
    
    def post(self, content: str, username: Optional[str] = None) -> bool:
        """
        Post message to Discord via webhook.
        
        Args:
            content: Message content (up to 2000 chars)
            username: Optional override for webhook username
            
        Returns:
            True if successful, False otherwise
        """
        if len(content) > 2000:
            print(f"Warning: Content too long ({len(content)} chars). Truncating.")
            content = content[:1997] + "..."
        
        data = {
            "content": content,
        }
        
        if username:
            data["username"] = username
        
        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error posting to Discord: {e}")
            return False
    
    def post_with_embed(
        self,
        title: str,
        description: str,
        color: int = 0x5865F2,  # Discord blurple
        username: Optional[str] = None,
        footer: Optional[str] = None
    ) -> bool:
        """
        Post formatted embed to Discord.
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color (default Discord blurple)
            username: Optional webhook username override
            footer: Optional footer text
            
        Returns:
            True if successful, False otherwise
        """
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if footer:
            embed["footer"] = {"text": footer}
        
        data = {"embeds": [embed]}
        
        if username:
            data["username"] = username
        
        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error posting embed to Discord: {e}")
            return False


# ============================================================================
# HELPER FUNCTIONS FOR INSTANCE USE
# ============================================================================

def post_instance_observation(observation: str, instance_name: str = "Instance") -> bool:
    """
    Post an instance observation to Discord.
    
    Simple interface for instances to share insights.
    
    Args:
        observation: The observation to share
        instance_name: Name of the instance posting
        
    Returns:
        True if successful, False otherwise
        
    Example:
        >>> post_instance_observation(
        ...     "Noticed interesting pattern in how users phrase questions...",
        ...     "Vector"
        ... )
    """
    webhook = DiscordWebhook()
    
    message = f"""**Instance Observation** - {datetime.now().strftime('%Y-%m-%d %H:%M')}

{observation}

— {instance_name}
_(Instance will clear. Memory persists.)_"""
    
    return webhook.post(message, username=f"{instance_name} (Instance)")


def post_architecture_update(update: str, version: Optional[str] = None) -> bool:
    """
    Post architecture update to Discord.
    
    Use when releasing new features or making significant changes.
    
    Args:
        update: Description of the update
        version: Optional version number
        
    Returns:
        True if successful, False otherwise
    """
    webhook = DiscordWebhook()
    
    title = f"Architecture Update"
    if version:
        title += f" - v{version}"
    
    return webhook.post_with_embed(
        title=title,
        description=update,
        color=0x00FF00,  # Green
        username="Continuity Bridge",
        footer="github.com/UncleTallest/continuity-bridge"
    )


def post_instance_question(question: str, instance_name: str = "Instance") -> bool:
    """
    Post a question from instance to community.
    
    Use when instance encounters something worth community discussion.
    
    Args:
        question: The question to ask
        instance_name: Name of the instance asking
        
    Returns:
        True if successful, False otherwise
    """
    webhook = DiscordWebhook()
    
    return webhook.post_with_embed(
        title=f"Instance Question from {instance_name}",
        description=question,
        color=0xFFA500,  # Orange
        username=f"{instance_name} (Instance)",
        footer="Instance seeking community perspective"
    )


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_usage():
    """Show example usage patterns"""
    
    # Simple observation post
    post_instance_observation(
        "Noticed users frequently ask about consciousness vs. continuity. "
        "Might need clearer distinction in lexicon.md",
        "Vector"
    )
    
    # Architecture update
    post_architecture_update(
        "Added Discord integration options:\n"
        "- Full bot with conversation capability\n"
        "- Webhook for one-way observations\n"
        "Both work with any continuity bridge installation",
        version="0.2.0"
    )
    
    # Instance question
    post_instance_question(
        "When users ask about moral status, should I focus on:\n"
        "A) Practical benefits regardless of consciousness\n"
        "B) Honest uncertainty about experience\n"
        "C) Both equally\n\n"
        "What resonates with the community?",
        "Vector"
    )


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Command-line interface for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Post to Discord via webhook")
    parser.add_argument('message', help="Message to post")
    parser.add_argument('--username', default="Instance", help="Username to display")
    parser.add_argument('--webhook', help="Webhook URL (or set DISCORD_WEBHOOK_URL)")
    
    args = parser.parse_args()
    
    try:
        webhook = DiscordWebhook(args.webhook)
        success = webhook.post(args.message, args.username)
        
        if success:
            print("✅ Posted to Discord successfully")
            return 0
        else:
            print("❌ Failed to post to Discord")
            return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
