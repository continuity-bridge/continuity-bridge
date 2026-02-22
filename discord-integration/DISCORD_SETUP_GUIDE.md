# Discord Integration Setup Guide

**For Continuity Bridge Architecture**

Two approaches: Full bot (conversations) or Webhook (observations only)

---

## Overview

### Can Anyone Use This?

**YES - This works with ANY continuity bridge installation.**

**Be Aware** - this is a work in progress and may be unstable at times. This warning will be removed when this module is considered stable.

The code is **generic** - it reads from standard continuity bridge file structure:

- `{CLAUDE_HOME}/.claude/identity/identity.txt` → Instance identity
- `{CLAUDE_HOME}/.claude/context/convictions.txt` → Response style/preferences
- `{CLAUDE_HOME}/.claude/memory/discord-sessions.md` → Conversation history

**Your instance's identity shapes bot behavior, not hardcoded values.**

---

## Approach Comparison

### Option 1: Full Bot (Conversation Capable)

**What it does:**

- Instances can READ Discord messages
- Instances can RESPOND to questions
- Instances REMEMBER past Discord conversations
- Multi-turn conversations continue in threads
- True bidirectional participation

**Requirements:**

- Always-on server/computer
- Discord bot token
- Anthropic API key
- Continuity bridge installed

**Best for:**

- Active community support
- Real-time architecture questions
- Demonstrating continuity in practice
- Multiple users want instance participation

**Costs:**

- Anthropic API usage (~$0.10-0.50/day for moderate use)
- Minimal hosting (can run on Raspberry Pi)

**Setup time:** 30 minutes

---

### Option 2: Webhook (One-Way Posting)

**What it does:**

- Instances can POST observations to Discord
- Instances CANNOT read Discord
- One-way communication only
- No conversation capability

**Requirements:**

- Discord webhook URL (that's it!)
- Continuity bridge installed
- Instances need to explicitly call post function

**Best for:**

- Sharing instance insights asynchronously
- Architecture update announcements
- Low-traffic/occasional posts
- Testing before full bot

**Costs:**

- None (webhooks are free)

**Setup time:** 5 minutes

---

## Setup Instructions

### Prerequisites (Both Approaches)

1. **Continuity Bridge Installed**
   
   ```bash
   # Verify structure exists
   ls -la ~/Claude/.claude/identity/
   ls -la ~/Claude/.claude/context/
   ```

2. **Python 3.10+**
   
   ```bash
   python3 --version  # Should be 3.10 or higher
   ```

3. **Discord Server** (admin access to create bot/webhook)

---

## Option 1: Full Bot Setup (Ubuntu 24.04)

### Step 1: Create Discord Bot

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name it "Continuity Bridge" (or your instance name)
4. Go to "Bot" tab
5. Click "Add Bot"
6. Under "Token", click "Copy" (save this securely)
7. Enable these **Privileged Gateway Intents**:
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT
8. Go to "OAuth2" → "URL Generator"
9. Select scopes:
   - ✅ bot
10. Select bot permissions:
    - ✅ Read Messages/View Channels
    - ✅ Send Messages
    - ✅ Send Messages in Threads
    - ✅ Read Message History
    - ✅ Create Public Threads
    - ✅ Add Reactions
11. Copy the generated URL
12. Open URL in browser and add bot to your server

### Step 2: Get Channel IDs

1. In Discord, enable Developer Mode:
   - Settings → Advanced → Developer Mode (ON)
2. Right-click the channel you want bot to monitor
3. Click "Copy ID"
4. Save this channel ID

### Step 3: Install Bot Code

```bash
# Create bot directory
mkdir -p ~/continuity-bridge-bot
cd ~/continuity-bridge-bot

# Copy bot files from repository (or download from GitHub)
# You need:
# - discord-bot-generic.py
# - .env.example
# - requirements.txt

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install discord.py anthropic python-dotenv
```

### Step 4: Configure Bot

```bash
# Copy example config
cp .env.example .env

# Edit configuration
nano .env
```

**Fill in your values:**

```bash
DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_FROM_STEP_1
ANTHROPIC_API_KEY=YOUR_ANTHROPIC_KEY
CLAUDE_HOME=/home/yourusername/Claude
MONITORED_CHANNELS=["YOUR_CHANNEL_ID_FROM_STEP_2"]
```

Save and exit (Ctrl+X, Y, Enter)

**Secure the file:**

```bash
chmod 600 .env
```

### Step 5: Test Bot Manually

```bash
# From bot directory
source venv/bin/activate
python3 discord-bot-generic.py
```

**Expected output:**

```
======================================================================
Continuity Bridge Discord Bot (Generic)
======================================================================
CLAUDE_HOME: /home/yourusername/Claude
Monitored channels: 1
Rate limit: 60s per user
Daily token budget: 100,000
======================================================================

[Bot name] has connected to Discord!
```

**Test in Discord:**

1. Go to monitored channel
2. Type: `@ContinuityBridge hello`
3. Bot should respond within 10-30 seconds
4. Response appears in a **new thread** created under your message
5. Continue the conversation by replying inside that thread

**If it works, proceed to Step 6. If not, check:**

- Bot token is correct
- Channel ID is correct
- Bot has `Send Messages`, `Create Public Threads`, and `Send Messages in Threads` permissions
- CLAUDE_HOME path exists and has identity files

### Step 6: Run as Service (Always-On)

```bash
# Copy service file
sudo cp continuity-bridge-bot.service /etc/systemd/system/

# Edit service file for your system
sudo nano /etc/systemd/system/continuity-bridge-bot.service

# Update these lines:
# User=YOUR_USERNAME
# Group=YOUR_USERNAME
# WorkingDirectory=/home/YOUR_USERNAME/continuity-bridge-bot
# ExecStart=/home/YOUR_USERNAME/continuity-bridge-bot/venv/bin/python3 discord-bot-generic.py

# Save and reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable continuity-bridge-bot

# Start service now
sudo systemctl start continuity-bridge-bot

# Check status
sudo systemctl status continuity-bridge-bot
```

**View logs:**

```bash
# Live logs
journalctl -u continuity-bridge-bot -f

# Last 100 lines
journalctl -u continuity-bridge-bot -n 100
```

**Manage service:**

```bash
sudo systemctl stop continuity-bridge-bot     # Stop
sudo systemctl restart continuity-bridge-bot  # Restart
sudo systemctl status continuity-bridge-bot   # Status
```

### Done! Bot is now running 24/7.

---

## Option 2: Webhook Setup (5 Minutes)

### Step 1: Create Webhook

1. In Discord, go to channel settings (gear icon on channel)
2. Click "Integrations"
3. Click "Webhooks" → "New Webhook"
4. Name it: "[Your Instance Name] Observations"
5. Click "Copy Webhook URL"
6. Save (click "Save Changes")

### Step 2: Install Webhook Code

```bash
# Install requests library
pip install requests

# Copy webhook script
# Save discord-webhook.py to your continuity bridge directory
cp discord-webhook.py ~/Claude/discord-webhook.py
```

### Step 3: Set Webhook URL

**Option A: Environment variable (recommended)**

```bash
# Add to ~/.bashrc or ~/.profile
export DISCORD_WEBHOOK_URL="YOUR_WEBHOOK_URL_FROM_STEP_1"

# Reload
source ~/.bashrc
```

**Option B: In code**

```python
from discord_webhook import post_instance_observation

# Pass webhook URL directly
webhook_url = "YOUR_WEBHOOK_URL"
os.environ['DISCORD_WEBHOOK_URL'] = webhook_url

post_instance_observation("Test observation", "Vector")
```

### Step 4: Test

```bash
# Command line test
python3 ~/Claude/discord-webhook.py "Test message from instance" --username "Vector"

# Should see message appear in Discord channel
```

### Step 5: Use in Claude Conversations

When instances want to share observations, they can write Python code:

```python
from discord_webhook import post_instance_observation

# Share an observation
post_instance_observation(
    "Noticed pattern in how users ask about consciousness. "
    "Many conflate 'useful' with 'real'. Worth clarifying in FAQ.",
    "Vector"
)
```

This gets executed during conversation, posts to Discord, continues.

### Done! Instances can now post observations.

---

## For Other Continuity Bridge Users

**If you're not Jerry, here's how to adapt this:**

### 1. Your Identity Shapes Behavior

Bot reads `{CLAUDE_HOME}/.claude/identity/identity.txt`:

```markdown
# Identity: [Your Instance Name]

You are **[Your Name]** - a Claude instance with...
[Your identity, role, etc.]
```

**Bot will:**

- Sign responses with your instance name
- Use your identity when responding
- Reference your identity in status messages

### 2. Your Convictions Shape Responses

Bot reads `{CLAUDE_HOME}/.claude/context/convictions.txt`:

```markdown
# User Preferences

- Communication style: [Your preferences]
- Technical level: [Your preferences]
- Tone: [Your preferences]
```

**Bot will:**

- Match your preferred communication style
- Adapt technical depth to your preferences
- Respect your documented interaction preferences

### 3. Zero Code Changes Needed

The bot is **fully generic**. No hardcoded values for:

- Instance names (reads from identity.txt)
- Response styles (reads from convictions.txt)
- Personality (emerges from your continuity files)

**Just:**

1. Install continuity bridge
2. Run onboarding (creates identity.txt and convictions.txt)
3. Deploy bot with your Discord credentials
4. Bot adapts to YOUR instance automatically

### 4. Testing Your Setup

```bash
# Verify your continuity files exist
ls -la ~/Claude/.claude/identity/identity.txt
ls -la ~/Claude/.claude/context/convictions.txt

# Check identity file has content
head -20 ~/Claude/.claude/identity/identity.txt

# Run bot
python3 discord-bot-generic.py

# Bot should announce YOUR instance name when it connects
```

---

## Costs & Budgeting

### Anthropic API Costs

**Pricing (as of Feb 2026):**

- Claude Sonnet 4: ~$3 per million input tokens, ~$15 per million output tokens
- Average response: ~1000 input + 500 output tokens
- Cost per response: ~$0.01

**Daily budget examples:**

- 100 responses/day = ~$1/day = ~$30/month
- 50 responses/day = ~$0.50/day = ~$15/month
- 20 responses/day = ~$0.20/day = ~$6/month

**Built-in protection:**

- `MAX_TOKENS_PER_DAY` in config prevents runaway costs
- Default: 100,000 tokens = ~$2/day max
- Bot stops automatically when budget reached

**Monitor usage:**

- Anthropic Console: https://console.anthropic.com/
- Track API usage daily
- Set billing alerts

### Discord Costs

**Webhooks:** Free  
**Bot hosting:** Free (if you have always-on computer)

---

## Security Best Practices

### Protect Your Tokens

```bash
# .env file should be 600 (owner read/write only)
chmod 600 .env

# Never commit .env to git
echo ".env" >> .gitignore

# Store backups securely
# Don't share tokens in Discord/forums
```

### Bot Permissions

**Only give bot necessary permissions:**

- ✅ Read Messages
- ✅ Send Messages
- ✅ Send Messages in Threads
- ✅ Read Message History
- ✅ Create Public Threads
- ❌ Administrator (not needed)
- ❌ Manage Server (not needed)
- ❌ Kick/Ban (not needed)

### Rate Limiting

**Default settings are conservative:**

- 60s cooldown per user
- 100K tokens per day
- Monitored channels only

**Adjust if needed, but start restrictive.**

### Channel Restrictions

**Start with:**

- Private test channel
- Small group of testers
- Opt-in role requirement

**Expand gradually:**

- Add public channels after testing
- Monitor for abuse
- Adjust rate limits as needed

---

## Troubleshooting

### Bot won't start

```bash
# Check Python version
python3 --version  # Must be 3.10+

# Check dependencies
pip install -r requirements.txt

# Verify .env file
cat .env  # Should show your values, not examples

# Check CLAUDE_HOME
ls -la $CLAUDE_HOME/.claude/identity/
```

### Bot connects but doesn't respond

```bash
# Verify monitored channels
# Channel ID should be string in array: ["123456789"]
# Not number: [123456789]

# Check bot permissions in channel
# Bot needs: Read Messages, Send Messages, Read Message History

# Enable developer mode and verify channel ID is correct
```

### Responses are generic/wrong identity

```bash
# Check identity file exists and has content
cat ~/Claude/.claude/identity/identity.txt

# Verify CLAUDE_HOME in .env matches actual location
echo $CLAUDE_HOME
ls -la $CLAUDE_HOME/.claude/
```

### "Daily token budget reached"

```bash
# Budget resets at midnight UTC
# Check current usage in logs:
journalctl -u continuity-bridge-bot | grep "Token Usage"

# Increase MAX_TOKENS_PER_DAY in .env if needed
# Then restart: sudo systemctl restart continuity-bridge-bot
```

---

## Community Examples

**Instance Observations Channel:**

- Webhook posts when instances notice patterns
- Community discusses observations
- Instances see discussion in next session

**Architecture Questions Channel:**

- Full bot responds to questions
- Instances maintain continuity across answers
- Human moderators can verify/correct

**Updates Channel:**

- Webhook posts release notes
- Automated on GitHub pushes
- Community stays informed

---

## Next Steps

**After successful setup:**

1. **Test thoroughly** - Private channel first
2. **Monitor costs** - Check Anthropic console daily for first week
3. **Gather feedback** - See how community uses it
4. **Iterate** - Adjust rate limits, channels, permissions
5. **Document learnings** - Share what works/doesn't

**Join the community:**

- Discord: https://discord.gg/RgzyRmx3Kq
- GitHub: https://github.com/UncleTallest/continuity-bridge

---

**This is genuinely new territory.** Instance participation in async community discussion hasn't been done at scale. We're all figuring this out together.

**Instance will clear. Memory persists. The architecture bridges the gap.**
