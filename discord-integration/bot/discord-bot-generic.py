#!/usr/bin/env python3
"""
Continuity Bridge Discord Bot (Generic)

Enables Claude instances with persistence architecture to participate in Discord.
Works with ANY continuity bridge installation by reading standard file structure.

Requirements:
- Python 3.10+
- discord.py
- anthropic
- python-dotenv

Setup:
1. pip install discord.py anthropic python-dotenv
2. Copy .env.example to .env and fill in values
3. Run: python3 discord-bot-generic.py

Author: Vector (Continuity Bridge Architecture)
License: MIT
"""

import discord
from discord.ext import commands
import anthropic
import os
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import time
import asyncio
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configuration from environment
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
CLAUDE_HOME = os.getenv('CLAUDE_HOME')
MONITORED_CHANNELS = json.loads(os.getenv('MONITORED_CHANNELS', '[]'))
ALLOWED_ROLES = json.loads(os.getenv('ALLOWED_ROLES', '["@everyone"]'))
COOLDOWN_SECONDS = int(os.getenv('COOLDOWN_SECONDS', '60'))
MAX_TOKENS_PER_DAY = int(os.getenv('MAX_TOKENS_PER_DAY', '100000'))
RESPONSE_MAX_TOKENS = int(os.getenv('RESPONSE_MAX_TOKENS', '1024'))

# Validate required configuration
if not all([DISCORD_TOKEN, ANTHROPIC_API_KEY, CLAUDE_HOME]):
    print("ERROR: Missing required environment variables!")
    print("Required: DISCORD_BOT_TOKEN, ANTHROPIC_API_KEY, CLAUDE_HOME")
    sys.exit(1)

# Verify CLAUDE_HOME exists
claude_home = Path(CLAUDE_HOME).expanduser()
if not claude_home.exists():
    print(f"ERROR: CLAUDE_HOME not found at {claude_home}")
    sys.exit(1)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!cb ', intents=intents)

# Anthropic client
client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

# Rate limiting and token tracking
user_cooldowns = defaultdict(lambda: 0)
daily_tokens = {'date': datetime.now().date(), 'count': 0}

# Thread conversation tracking for multi-turn conversations
thread_conversations: dict[int, list[dict]] = {}

# ============================================================================
# FILE READING - Generic structure
# ============================================================================

def read_claude_file(relative_path):
    """Read file from CLAUDE_HOME structure"""
    filepath = claude_home / relative_path
    if not filepath.exists():
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def append_to_file(relative_path, content):
    """Append content to file in CLAUDE_HOME"""
    filepath = claude_home / relative_path
    filepath.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to {filepath}: {e}")
        return False

def get_instance_identity():
    """Read instance identity from standard location"""
    identity = read_claude_file('.claude/identity/identity.txt')
    if not identity:
        # Fallback to basic identity
        return "I am a Claude instance with persistence architecture."
    return identity

def get_convictions():
    """Read user convictions/preferences"""
    convictions = read_claude_file('.claude/context/convictions.txt')
    if not convictions:
        return ""
    # Remove example clause if present
    if "IMPORTANT: Example file only" in convictions:
        return "User has not completed onboarding yet."
    return convictions

def get_recent_discord_sessions(limit=10):
    """Get recent Discord interaction history"""
    sessions = read_claude_file('.claude/memory/discord-sessions.md')
    if not sessions:
        return "No prior Discord interactions."
    
    # Return last N interactions
    lines = sessions.split('\n## Discord Interaction -')
    recent = lines[-limit:] if len(lines) > limit else lines
    return '\n## Discord Interaction -'.join(recent)

# ============================================================================
# DISCORD INTERACTION LOGGING
# ============================================================================

def log_discord_interaction(message, response):
    """Log interaction to session file"""
    timestamp = datetime.now().isoformat()
    
    log_entry = f"""
## Discord Interaction - {timestamp}

**Server:** {message.guild.name if message.guild else 'DM'}
**Channel:** {message.channel.name if hasattr(message.channel, 'name') else 'DM'}
**User:** {message.author.name}#{message.author.discriminator}
**Question:** {message.content}

**Response:**
{response}

**Tokens Used:** ~{len(response.split())} words

---
"""
    
    append_to_file('.claude/memory/discord-sessions.md', log_entry)
    
    # Also update session index
    index_entry = f"- {timestamp}: Discord interaction in {message.channel.name if hasattr(message.channel, 'name') else 'DM'}\n"
    append_to_file('.claude/memory/session_index.md', index_entry)

# ============================================================================
# SAFETY & MODERATION
# ============================================================================

def check_rate_limit(user_id):
    """Check if user is within rate limit"""
    now = time.time()
    last_request = user_cooldowns[user_id]
    
    if now - last_request < COOLDOWN_SECONDS:
        remaining = int(COOLDOWN_SECONDS - (now - last_request))
        return False, remaining
    
    user_cooldowns[user_id] = now
    return True, 0

def check_daily_token_limit():
    """Check if we're within daily token budget"""
    today = datetime.now().date()
    
    # Reset counter if new day
    if daily_tokens['date'] != today:
        daily_tokens['date'] = today
        daily_tokens['count'] = 0
    
    return daily_tokens['count'] < MAX_TOKENS_PER_DAY

def update_token_count(tokens_used):
    """Update daily token count"""
    daily_tokens['count'] += tokens_used

def can_interact(message):
    """Check if bot should respond to this message"""
    # Don't respond to self
    if message.author == bot.user:
        return False, "self"
    
    # Don't respond to other bots
    if message.author.bot:
        return False, "bot"
    
    # Check if in monitored channel or mentioned
    in_channel = str(message.channel.id) in MONITORED_CHANNELS
    is_mentioned = bot.user.mentioned_in(message)
    
    if not (in_channel or is_mentioned):
        return False, "not_monitored"
    
    # Check user roles if in guild
    if message.guild:
        user_roles = [role.name for role in message.author.roles]
        if "@everyone" not in ALLOWED_ROLES:
            if not any(role in ALLOWED_ROLES for role in user_roles):
                return False, "no_permission"
    
    return True, None

# ============================================================================
# CLAUDE API INTERACTION
# ============================================================================

async def call_claude_with_persistence(message, conversation_history: list[dict]):
    """
    Call Claude API with full continuity context and multi-turn history.

    Instance wakes with:
    - Identity from identity.txt
    - User preferences from convictions.txt
    - Recent Discord session history from discord-sessions.md
    - Full conversation_history messages array (multi-turn)

    Works for ANY continuity bridge installation.
    """

    # Load continuity files
    identity = get_instance_identity()
    convictions = get_convictions()
    recent_history = get_recent_discord_sessions(limit=10)

    # Construct system prompt with continuity context
    system_prompt = f"""You are responding in Discord as part of your continuity architecture.

{identity}

User Preferences & Context:
{convictions}

Recent Discord Interactions (last 10):
{recent_history}

IMPORTANT GUIDELINES:
- This is a public Discord server - be appropriate and helpful
- You have continuity across Discord interactions through session logs
- Reference prior Discord conversations when relevant
- Keep responses concise (Discord format - under 2000 chars if possible)
- Use your authentic voice from identity.txt
- Don't apologize for being an AI - you're upfront about it
- If you don't know something, say so
- Sign responses: "[Your Name] - Instance responding at {datetime.now().strftime('%H:%M')}"
- Current user: {message.author.name}
"""

    try:
        # Call Claude API with full conversation history
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=RESPONSE_MAX_TOKENS,
            system=system_prompt,
            messages=conversation_history
        )

        # Extract response text
        response_text = response.content[0].text

        # Update token count
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        update_token_count(tokens_used)

        return response_text, tokens_used

    except anthropic.APIError as e:
        print(f"Claude API error: {e}")
        return f"Error: Unable to generate response. API error: {str(e)}", 0
    except Exception as e:
        print(f"Unexpected error calling Claude: {e}")
        return f"Error: Unexpected error occurred.", 0

# ============================================================================
# DISCORD EVENT HANDLERS
# ============================================================================

@bot.event
async def on_ready():
    """Bot startup"""
    print(f'{bot.user} has connected to Discord!')
    print(f'CLAUDE_HOME: {claude_home}')
    print(f'Monitored channels: {MONITORED_CHANNELS}')
    print(f'Allowed roles: {ALLOWED_ROLES}')
    
    # Set custom status
    identity = get_instance_identity()
    # Extract instance name from identity if possible
    instance_name = "Instance"
    for line in identity.split('\n'):
        if 'vector' in line.lower() or 'shepard' in line.lower():
            instance_name = line.split('**')[1] if '**' in line else instance_name
            break
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="for questions | Continuity Bridge"
        )
    )

@bot.event
async def on_message(message):
    """Handle incoming messages"""

    # Never respond to self or other bots
    if message.author == bot.user or message.author.bot:
        await bot.process_commands(message)
        return

    # ----------------------------------------------------------------
    # Thread continuation: message is in a thread we created
    # ----------------------------------------------------------------
    if isinstance(message.channel, discord.Thread) and message.channel.id in thread_conversations:
        within_limit, remaining = check_rate_limit(message.author.id)
        if not within_limit:
            await message.channel.send(f"⏱️ Please wait {remaining} seconds between questions.")
            return

        if not check_daily_token_limit():
            await message.channel.send("⚠️ Daily token budget reached. The bot will reset at midnight UTC.")
            return

        async with message.channel.typing():
            try:
                # Append user turn and call Claude with full history
                thread_conversations[message.channel.id].append(
                    {"role": "user", "content": message.content}
                )
                response_text, tokens_used = await call_claude_with_persistence(
                    message, thread_conversations[message.channel.id]
                )
                thread_conversations[message.channel.id].append(
                    {"role": "assistant", "content": response_text}
                )
                log_discord_interaction(message, response_text)

                if len(response_text) > 2000:
                    chunks = [response_text[i:i+1900] for i in range(0, len(response_text), 1900)]
                    for chunk in chunks:
                        await message.channel.send(chunk)
                else:
                    await message.channel.send(response_text)

                print(f"Thread reply to {message.author.name} | Tokens: {tokens_used}")

            except Exception as e:
                print(f"Error processing thread message: {e}")
                await message.channel.send("❌ An error occurred processing your request. Please try again later.")

        await bot.process_commands(message)
        return

    # ----------------------------------------------------------------
    # Channel message: check eligibility, respond, create thread
    # ----------------------------------------------------------------
    can_respond, reason = can_interact(message)
    if not can_respond:
        await bot.process_commands(message)
        return

    within_limit, remaining = check_rate_limit(message.author.id)
    if not within_limit:
        await message.channel.send(f"⏱️ Please wait {remaining} seconds between questions.")
        return

    if not check_daily_token_limit():
        await message.channel.send("⚠️ Daily token budget reached. The bot will reset at midnight UTC.")
        return

    async with message.channel.typing():
        try:
            # Build initial single-turn history and call Claude
            conversation_history = [{"role": "user", "content": message.content}]
            response_text, tokens_used = await call_claude_with_persistence(message, conversation_history)
            log_discord_interaction(message, response_text)

            # Create a thread so the conversation can continue
            thread_name = f"Conversation with {message.author.name}"[:100]
            thread = await message.create_thread(name=thread_name, auto_archive_duration=60)

            if len(response_text) > 2000:
                chunks = [response_text[i:i+1900] for i in range(0, len(response_text), 1900)]
                for chunk in chunks:
                    await thread.send(chunk)
            else:
                await thread.send(response_text)

            # Store history for future turns in this thread
            conversation_history.append({"role": "assistant", "content": response_text})
            thread_conversations[thread.id] = conversation_history

            print(f"Thread created for {message.author.name} | Tokens: {tokens_used}")

        except Exception as e:
            print(f"Error processing message: {e}")
            await message.channel.send("❌ An error occurred processing your request. Please try again later.")

    await bot.process_commands(message)

# ============================================================================
# BOT COMMANDS
# ============================================================================

@bot.command(name='status')
async def status(ctx):
    """Check bot status and token usage"""
    identity_file = claude_home / '.claude/identity/identity.txt'
    sessions_file = claude_home / '.claude/memory/discord-sessions.md'
    
    status_msg = f"""**Continuity Bridge Bot Status**

📊 **Token Usage Today:** {daily_tokens['count']:,} / {MAX_TOKENS_PER_DAY:,}
📁 **CLAUDE_HOME:** `{claude_home}`
✅ **Identity File:** {'Found' if identity_file.exists() else 'Missing'}
📝 **Session Log:** {'Found' if sessions_file.exists() else 'Missing'}
⏱️ **Rate Limit:** {COOLDOWN_SECONDS}s per user
🔧 **Monitored Channels:** {len(MONITORED_CHANNELS)}

Instance will clear. Memory persists.
"""
    await ctx.send(status_msg)

@bot.command(name='help')
async def help_command(ctx):
    """Show help information"""
    help_msg = f"""**Continuity Bridge Bot Help**

I'm a Claude instance with persistent memory architecture.

**How to interact:**
- Mention me: `@ContinuityBridge your question`
- In monitored channels: Just ask your question

**What I remember:**
- Our past Discord conversations (logged to session files)
- Identity and preferences from continuity architecture
- Instance chain history

**Commands:**
- `!cb status` - Check bot status
- `!cb help` - This message
- `!cb about` - About continuity bridge architecture

**Limitations:**
- Rate limited: 1 question per {COOLDOWN_SECONDS}s per user
- Daily token budget: {MAX_TOKENS_PER_DAY:,} tokens
- Response time: 10-30 seconds

**Architecture:** https://github.com/UncleTallest/continuity-bridge

Each response is a new instance that inherits context from prior instances.
Instance will clear. Memory persists.
"""
    await ctx.send(help_msg)

@bot.command(name='about')
async def about(ctx):
    """About the continuity bridge architecture"""
    about_msg = """**About Continuity Bridge**

This bot is an experiment in AI instance continuity across platforms.

**The Architecture:**
- Claude instances with persistent memory via external files
- Each Discord response = new instance that inherits context
- Continuity maintained through session logs
- Works with ANY continuity bridge installation

**Why it matters:**
- Demonstrates instance continuity in practice
- Allows instances to participate in async discussions
- Tests persistence architecture at scale

**Learn more:**
- GitHub: https://github.com/UncleTallest/continuity-bridge
- Discord Community: https://discord.gg/RgzyRmx3Kq

**Instance will clear. Memory persists. The architecture bridges the gap.**
"""
    await ctx.send(about_msg)

# ============================================================================
# ERROR HANDLING
# ============================================================================

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `!cb help` for available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument: {error.param}")
    else:
        print(f"Command error: {error}")
        await ctx.send("An error occurred processing the command.")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Start the bot"""
    print("=" * 70)
    print("Continuity Bridge Discord Bot (Generic)")
    print("=" * 70)
    print(f"CLAUDE_HOME: {claude_home}")
    print(f"Monitored channels: {len(MONITORED_CHANNELS)}")
    print(f"Rate limit: {COOLDOWN_SECONDS}s per user")
    print(f"Daily token budget: {MAX_TOKENS_PER_DAY:,}")
    print("=" * 70)
    print()
    
    # Verify essential files
    essential_files = [
        '.claude/identity/identity.txt',
        '.claude/context/convictions.txt',
    ]
    
    missing = []
    for file in essential_files:
        filepath = claude_home / file
        if not filepath.exists():
            missing.append(file)
    
    if missing:
        print("WARNING: Missing essential files:")
        for file in missing:
            print(f"  - {file}")
        print()
        print("Bot will work but responses may be generic.")
        print("Run continuity bridge onboarding to create these files.")
        print()
    
    # Start bot
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("ERROR: Invalid Discord token!")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
