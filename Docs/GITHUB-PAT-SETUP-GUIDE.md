---
author: Jerry Jackson (Uncle Tallest)
copyright: © 2026 Jerry Jackson. All rights reserved.
version: v0.3.0
---
# GitHub Personal Access Token (PAT) Setup Guide

**For:** Container git workflow authentication  
**Difficulty:** Beginner-friendly  
**Time:** 5 minutes

---

## What is a Personal Access Token?

A PAT is like a password that gives specific permissions to one repository. Think of it like a house key that only opens one door, instead of a master key that opens everything.

**Why use a PAT instead of SSH keys?**
- ✅ Works in containers without persistent storage
- ✅ Easy to create and revoke
- ✅ Minimal permissions (only what you need)
- ✅ Simpler setup for beginners
- ✅ Can be saved in a file for reuse

---

## Step-by-Step Instructions

### Step 1: Go to GitHub Settings

**Option A: Direct link**
Visit: https://github.com/settings/tokens?type=beta

**Option B: Manual navigation**
1. Click your profile picture (top-right corner)
2. Click "Settings"
3. Scroll down to "Developer settings" (bottom of left sidebar)
4. Click "Personal access tokens"
5. Click "Fine-grained tokens"

---

### Step 2: Generate New Token

Click the green **"Generate new token"** button

You'll see a form with several fields:

---

### Step 3: Fill Out Token Details

**Token name:** (what you want to call this)
```
Continuity Bridge Container
```

**Description (optional):**
```
For container git workflow automation
```

**Expiration:**
- Choose: **90 days** (recommended for balance of security/convenience)
- Or: **Custom** if you want a different length
- Or: **No expiration** (less secure, but convenient)

**Resource owner:**
- Select your GitHub username (should be auto-selected)

---

### Step 4: Repository Access

**IMPORTANT:** Choose **"Only select repositories"**

Under the dropdown that appears:
- Search for and select: `continuity-bridge_tallest-anchor`
- (This limits the token to ONLY this one repo)

---

### Step 5: Permissions (CRITICAL - Get This Right)

Scroll down to **"Permissions"** section.

You need to set THREE permissions:

#### Repository Permissions

**1. Contents**
- Click the dropdown next to "Contents"
- Select: **"Read and write"**
- ✓ This appears as a green checkmark

**2. Pull requests**
- Click the dropdown next to "Pull requests"
- Select: **"Read and write"**
- ✓ This appears as a green checkmark

**3. Metadata**
- This should automatically be set to **"Read"**
- ✓ You don't need to change this

**THAT'S IT.** You should have exactly three permissions:
```
✓ Contents: Read and write
✓ Pull requests: Read and write
✓ Metadata: Read
```

**DO NOT select any other permissions.** More permissions = more security risk.

---

### Step 6: Generate the Token

1. Scroll to the bottom
2. Click the green **"Generate token"** button
3. You'll see your new token on the next page

**IMPORTANT:** The token will look like this:
```
github_pat_11AABBBCCCDDDEEEFFFF1234567890ABCDEFGHIJ
```
or sometimes:
```
ghp_1234567890abcdefghijklmnopqrstuvwxyz123456
```

**⚠️ CRITICAL:** Copy this token NOW. You won't be able to see it again!

Click the **📋 copy icon** to copy it to clipboard.

---

### Step 7: Save the Token Securely

**On your desktop/laptop (Persephone, Hecate, Geras, Ixion):**

```bash
# Navigate to Claude directory
cd ~/Claude  # or D:\Claude on Windows

# Save PAT to file
echo "github_pat_YOUR_TOKEN_HERE" > .github-pat

# Set restrictive permissions (Linux/Mac)
chmod 600 .github-pat

# Add to .gitignore (prevents accidentally committing)
echo ".github-pat" >> .gitignore
git add .gitignore
git commit -m "Add .github-pat to gitignore"
```

**Windows users:**
```powershell
cd D:\Claude
echo "github_pat_YOUR_TOKEN_HERE" > .github-pat
# Right-click file → Properties → Security → Edit → Remove all users except yourself
```

**On Android devices (Orpheus, Magheara):**

```bash
# In Termux or terminal
cd /sdcard/Claude  # or ~/Claude

# Save PAT
echo "github_pat_YOUR_TOKEN_HERE" > .github-pat
chmod 600 .github-pat
```

---

### Step 8: Test the Token

**Verify it works:**

```bash
# Replace YOUR_TOKEN_HERE with your actual token
TOKEN="github_pat_YOUR_TOKEN_HERE"

# Test authentication
curl -H "Authorization: token $TOKEN" https://api.github.com/user

# Should show your GitHub username and profile info
# If you see an error, the token might be wrong or expired
```

---

## Using the Token in Container Workflow

### Method 1: Automatic (Recommended)

The install script will look for `.github-pat` and use it automatically.

```bash
# Run installer
bash install-container-workflow.sh

# Choose option 1 (GitHub PAT)
# Script will find your .github-pat file
```

### Method 2: Manual Entry

If the file isn't found, the installer will prompt you to paste the token:

```bash
bash install-container-workflow.sh
# Choose option 1
# Paste your token when prompted
```

### Method 3: Container Upload

For ephemeral containers (claude.ai web):

1. Save `.github-pat` file on desktop
2. Upload to `/mnt/user-data/outputs/.github-pat`
3. Installer will detect and use it

---

## Security Best Practices

### DO:
- ✅ Keep token in `.github-pat` file (gitignored)
- ✅ Set file permissions to 600 (owner read/write only)
- ✅ Use 90-day expiration (renew when expired)
- ✅ Revoke old tokens after creating new ones
- ✅ Use fine-grained tokens (not classic)

### DON'T:
- ❌ Commit `.github-pat` to git
- ❌ Share token with anyone
- ❌ Post token publicly (Discord, GitHub issues, etc.)
- ❌ Use classic tokens (less secure)
- ❌ Grant more permissions than needed

---

## Troubleshooting

### "Authentication failed"

**Problem:** Token might be expired, revoked, or wrong

**Solution:**
1. Go to https://github.com/settings/tokens
2. Check if token is still active
3. If expired, generate a new one
4. Update `.github-pat` file with new token

### "Permission denied"

**Problem:** Token doesn't have right permissions

**Solution:**
1. Go to https://github.com/settings/tokens
2. Find your token
3. Click "Edit"
4. Verify permissions:
   - Contents: Read and write
   - Pull requests: Read and write
   - Metadata: Read
5. Save changes

### "Repository not found"

**Problem:** Token doesn't have access to the repo

**Solution:**
1. Edit your token
2. Check "Repository access" section
3. Make sure `continuity-bridge_tallest-anchor` is selected
4. Save changes

---

## Renewing Expired Tokens

Tokens expire based on the duration you set (e.g., 90 days).

**When your token expires:**

1. You'll get authentication errors
2. Generate a new token (follow steps above)
3. Update `.github-pat` file:
   ```bash
   echo "github_pat_NEW_TOKEN_HERE" > ~/.github-pat
   chmod 600 ~/.github-pat
   ```
4. Continue working normally

**Tip:** Set a calendar reminder for 7 days before expiration.

---

## Revoking Tokens

**If you think your token was compromised:**

1. Go to https://github.com/settings/tokens
2. Find the token
3. Click "Delete" or "Revoke"
4. Generate a new token immediately
5. Update `.github-pat` file

**Compromised = exposed publicly, shared accidentally, or found in git history**

---

## Visual Summary

```
GitHub Settings → Developer Settings → Personal Access Tokens → Fine-grained

Generate New Token:
  Name: Continuity Bridge Container
  Expiration: 90 days
  Repository: continuity-bridge_tallest-anchor only
  Permissions:
    ✓ Contents: Read and write
    ✓ Pull requests: Read and write  
    ✓ Metadata: Read

Copy Token → Save to .github-pat → Use in container workflow
```

---

## Comparison: PAT vs SSH

| Feature | GitHub PAT | SSH Key |
|---------|-----------|---------|
| Ease of setup | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐ Moderate |
| Works in containers | ✅ Yes, everywhere | ❌ Only with storage |
| Granular permissions | ✅ Yes | ❌ All or nothing |
| Revocation | ✅ Instant | ✅ Instant |
| Expiration | ✅ Optional | ❌ Never |
| Security | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| Novice-friendly | ✅ Yes | ❌ No |

**For container workflow, PAT is recommended.**

---

## FAQ

**Q: Can I use the same PAT on multiple devices?**  
A: Yes! Copy `.github-pat` to each device.

**Q: What if I lose my token?**  
A: Generate a new one. Old tokens can't be recovered.

**Q: Can I have multiple PATs?**  
A: Yes! You can create separate tokens for different purposes.

**Q: Does this work with two-factor authentication (2FA)?**  
A: Yes! PATs work regardless of 2FA settings.

**Q: Can I use this with GitHub Enterprise?**  
A: Yes, but the URL will be different (your company's GitHub domain).

**Q: Will this affect my other GitHub work?**  
A: No. This token ONLY affects the one repo you selected.

---

## Next Steps

After creating your PAT:

1. ✅ Save to `.github-pat` file
2. ✅ Run `bash install-container-workflow.sh`
3. ✅ Test with `start-session` / `close-session`
4. ✅ Set calendar reminder for token renewal

---

**You're ready to use container git workflow with secure, minimal-permission authentication!**
