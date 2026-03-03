# Google Sheets MCP Setup via mcpbundles.com

**Service:** https://www.mcpbundles.com/providers/google-sheets  
**Your Credential:** https://www.mcpbundles.com/w/uncle-the Architect-personal/providers/b1c58d83-00fe-44ac-a364-445c29dda287  
**Security:** OAuth flow (you control permissions, can revoke anytime)

---

## WHY THIS IS BETTER THAN RANDOM GITHUB

**mcpbundles.com:**

- ✅ Professional service, maintained
- ✅ OAuth authentication (secure, standard)
- ✅ Can revoke access via Google Account settings
- ✅ Security audited infrastructure
- ✅ Support available

**Random GitHub repo:**

- ⚠️ Unknown code quality
- ⚠️ Could be abandoned
- ⚠️ No security guarantees
- ⚠️ Running arbitrary code with full Sheets access

**Your paranoia is justified. This is the right choice.** 🔒

---

## SETUP STEPS

### Step 1: Get MCP Configuration from mcpbundles

1. **Go to your provider page:**
   https://www.mcpbundles.com/w/uncle-the Architect-personal/providers/b1c58d83-00fe-44ac-a364-445c29dda287

2. **Look for "Configuration" or "MCP Config" section**
   
   - Should show JSON configuration block
   - Contains server URL and authentication

3. **Copy the JSON block** (will look something like):
   
   ```json
   {
     "google-sheets": {
       "type": "url",
       "url": "https://mcp.mcpbundles.com/hub/",
       "headers": {
         "Authorization": "Bearer ..."
       }
     }
   }
   ```

---

### Step 2: Add to Claude Desktop Config

1. **Open Claude Desktop config file:**
   
   ```powershell
   notepad "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

2. **Your config currently looks like:**
   
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

3. **Add the Google Sheets section** (from mcpbundles):
   
   ```json
   {
     "mcpServers": {
       "notion": {
         "type": "url",
         "url": "https://mcp.notion.com/mcp",
         "name": "notion-mcp"
       },
       "google-sheets": {
         "type": "url",
         "url": "https://mcp.mcpbundles.com/bundle/google-sheets",
         "headers": {
           "Authorization": "Bearer your-token-here"
         }
       }
     }
   }
   ```

4. **Save and close Notepad**

---

### Step 3: Restart Claude Desktop

1. **Quit Claude completely:**
   
   - File → Quit
   - Or right-click system tray icon → Quit

2. **Wait 5 seconds**

3. **Reopen Claude Desktop**

4. **Start NEW conversation** (don't use existing ones)

---

### Step 4: Test Connection

**In new Claude conversation:**

```
Can you list your available tools? Check if google-sheets is connected.
```

**I should respond with:**

- List of tools including google-sheets operations
- Confirmation that connection is active

---

### Step 5: Test Read/Write

#### Create Test Sheet

1. Go to https://sheets.google.com
2. Create new blank spreadsheet
3. Name it: "MCP Test"
4. Put "Hello World" in cell A1
5. Copy the sheet URL

#### Test Read

**In Claude:**

```
Read cell A1 from this sheet: [paste URL]
```

**I should respond:** "Hello World" ✅

#### Test Write

**In Claude:**

```
Write "Test successful!" to cell B1 in that sheet
```

**Check the sheet** - B1 should say "Test successful!" ✅

---

## USING WITH MARCUS CHARACTER SHEET

### Setup

1. **Create Google Sheet:**
   
   - Name: "Marcus Gruene - VTM V5"
   - Tab 1: "Character Sheet"
   - Tab 2: "Experience Log"
   - Tab 3: "Session Notes"

2. **Populate from fillable data:**
   
   - Copy Basic Info, Attributes, Skills sections
   - Add Experience Log table
   - Format for readability

3. **Share URL with me in conversation**

### Example Commands

**After a game session:**

```
Update Marcus' Experience Log:
- Date: 2/12/2026
- XP Gained: 5
- Notes: "Session 1 - First night in Austin"
```

**I can:**

- Read current stats (Hunger, HP, Willpower)
- Update XP automatically
- Log session notes
- Track character changes
- Calculate new totals

**During character creation:**

```
Marcus just bought Protean 4 (7 XP). Update the sheet:
- Deduct 7 XP from banked
- Add Protean 4 to disciplines
- Update XP log with purchase
```

---

## SECURITY NOTES

**What permissions does this grant?**

- Read/write access to your Google Sheets
- Only sheets you explicitly share URLs for
- Cannot access other Google services (Gmail, Drive, etc.)

**How to revoke access:**

1. Go to https://myaccount.google.com/permissions
2. Find "MCP Bundles" or similar
3. Click "Remove Access"

**Best practices:**

- Only share sheet URLs with Claude when needed
- Periodically review what sheets Claude has accessed
- Revoke and re-authenticate if credentials compromised

---

## TROUBLESHOOTING

**Problem: "google-sheets not found in tools"**

- Check claude_desktop_config.json syntax (valid JSON?)
- Restart Claude Desktop completely
- Start NEW conversation (old ones don't get new tools)

**Problem: "Authentication failed"**

- Token expired - re-authenticate via mcpbundles.com
- Copy new token to config
- Restart Claude Desktop

**Problem: "Cannot access sheet"**

- Sheet must be accessible via link (not private)
- Check sharing settings (Anyone with link → Viewer)
- Or share directly with mcpbundles service account

**Problem: "Changes not appearing in sheet"**

- Refresh the sheet (F5)
- Check if sheet is protected/locked
- Verify you have edit permissions

---

## BENEFITS

**For Marcus character tracking:**

- ✅ Automated XP logging
- ✅ Real-time stat updates
- ✅ Session note recording
- ✅ No manual copy/paste
- ✅ Always up-to-date

**For future characters:**

- ✅ Template once, use forever
- ✅ Track multiple characters
- ✅ Chronicle-wide campaign management
- ✅ Shared tracking with ST (if desired)

---

## PRIORITY

**Recommendation:** Set this up AFTER:

1. ✅ Marcus character finalized
2. ✅ LVM expansion completed
3. ✅ Models downloaded

**Then:** Create Marcus sheet in Google Sheets, connect MCP, automate tracking

**Time investment:** 15 minutes  
**Payoff:** Every session forever  

---

**Questions?** I'll guide you through setup when you're ready!
