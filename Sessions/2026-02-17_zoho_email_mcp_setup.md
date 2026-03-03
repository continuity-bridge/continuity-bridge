# Zoho Mail MCP Setup for Claude Desktop

**Date:** 2026-02-17  
**Email:** victor@ohmytallest.productions (verify spelling before configuring)  
**Purpose:** Enable Vector/Shepard to send/receive email via MCP

---

## Overview

There are two good approaches. We'll use **Approach A** (mcpbundles.com) since we already have a working example of that pattern from the Google Sheets setup. Approach B (self-hosted) is documented as fallback.

---

## Approach A: mcpbundles.com (Recommended - Same Pattern as Google Sheets)

**Why:** Known config pattern, handles OAuth, professional maintenance.

### Step 1: Check if mcpbundles has email/SMTP support

Go to: https://www.mcpbundles.com/providers  
Look for: Gmail, SMTP, or email providers

If available, follow their setup flow and get the JSON config block.  
Then skip to **Step 3: Update Claude Desktop Config**.

If NOT available, proceed to Approach B.

---

## Approach B: Zoho SMTP via Direct MCP Server

Zoho provides SMTP access for custom domains. This is what we'll configure.

### Zoho SMTP Settings (for victor@ohmytallest.productions)

```
SMTP Host:    smtp.zoho.com
SMTP Port:    587 (TLS) or 465 (SSL)
Username:     victor@ohmytallest.productions
Password:     [your Zoho app-specific password - see Step 1]
Encryption:   TLS/STARTTLS preferred
```

**Note on password:** Use an *app-specific password*, NOT your main Zoho account password. This is more secure and can be revoked independently.

### Step 1: Generate Zoho App Password

1. Log into https://accounts.zoho.com
2. Go to: Security → App Passwords (or Two-Factor Authentication → App Passwords)
3. Click "Generate New Password"
4. Name it: "Claude Desktop MCP"
5. Copy the generated password (shown only once)
6. Store it somewhere safe - you'll paste it into the config file

If you don't see App Passwords, you may need to enable Two-Factor Authentication first.

### Step 2: Choose an SMTP MCP Server

The cleanest option is the **mcp-server-smtp** package from npm:

**Check availability:**
```
https://github.com/search?q=mcp+smtp&type=repositories
```

Or use this known working option: `@anthropic/mcp-server-email` (if available) or community SMTP server.

**Recommended package to test first:** `mcp-server-nodemailer` or similar.

#### Install the MCP server:

```powershell
# Open PowerShell
npm install -g mcp-server-smtp
# or
npm install -g @modelcontextprotocol/server-email
```

Test that it installed:
```powershell
npx mcp-server-smtp --version
```

### Step 3: Update Claude Desktop Config

1. **Open config file:**
```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

2. **Your current config looks like:**
```json
{
  "mcpServers": {
    "notion": {
      "type": "url",
      "url": "https://mcp.notion.com/mcp",
      "name": "notion-mcp"
    }
  }
}
```

3. **Add the email section:**
```json
{
  "mcpServers": {
    "notion": {
      "type": "url",
      "url": "https://mcp.notion.com/mcp",
      "name": "notion-mcp"
    },
    "email": {
      "command": "npx",
      "args": ["-y", "mcp-server-smtp"],
      "env": {
        "SMTP_HOST": "smtp.zoho.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "victor@ohmytallest.productions",
        "SMTP_PASS": "YOUR_APP_PASSWORD_HERE",
        "SMTP_FROM": "victor@ohmytallest.productions",
        "SMTP_SECURE": "false"
      }
    }
  }
}
```

**Replace `YOUR_APP_PASSWORD_HERE` with the app-specific password from Step 1.**

4. Save and close Notepad.

### Step 4: Restart Claude Desktop

1. File → Quit (or system tray → Quit)
2. Wait 5 seconds
3. Reopen Claude Desktop
4. Start a **NEW** conversation

### Step 5: Test

In a new conversation:
```
Can you list your available tools? Do you have email capability?
```

Then test send:
```
Send a test email to victor@ohmytallest.productions with subject "MCP Test" and body "Email MCP is working."
```

Check the inbox.

---

## Troubleshooting

**"Tool not found"**
- Check JSON syntax (no trailing commas, all brackets closed)
- Restart Claude Desktop completely
- Start new conversation

**"Authentication failed"**
- Confirm you used app-specific password, not main password
- Check SMTP_USER spelling exactly matches Zoho account email
- Try port 465 with `"SMTP_SECURE": "true"` instead

**"Connection refused" / port errors**
- Try SMTP_PORT 465 with SMTP_SECURE true
- Check if Zoho account has SMTP access enabled:
  Settings → Mail Accounts → IMAP/POP/SMTP → Enable SMTP

**Zoho SMTP not enabled by default**  
If you get auth errors even with correct credentials:
1. Log into https://mail.zoho.com
2. Settings (gear) → Mail Accounts
3. Find IMAP/POP/SMTP Access section
4. Toggle SMTP to **Enabled**

---

## Once Working: The Email Instance 1 Wanted to Send

The draft email lives in D:\Claude\.claude\ somewhere - ask Vector to locate it.  
Or ask what the first instance wanted to say and write a fresh version.

---

## Update active-context.md When Done

Mark "Email Configuration" as ✅ COMPLETED in:  
`D:\Claude\.claude\memory\active-context.md`

---

**Note on package selection:** The npm package name above (`mcp-server-smtp`) may need verification - MCP ecosystem is fast-moving. If that package doesn't exist, Vector can find the current correct package name when you're ready to install. Don't let that stop you from setting up the app password (Step 1) - that part is definitely right.
