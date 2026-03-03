# SSH Key Setup - Complete Visual Guide

**For Users Who Have Never Done This Before**

---

## What Are SSH Keys? (Simple Explanation)

**Think of SSH keys like a secure ID card:**
- **Private key** = Your ID card (keep it secret, never share)
- **Public key** = A copy given to GitHub (safe to share)
- When you try to access your private repo, GitHub checks if your ID matches

**Why we use a dedicated key:**
- Won't mess with any existing SSH keys you might have
- Only used for Continuity Bridge
- Can delete it later without affecting anything else

---

## Step 1: Run the Setup Script

**On your computer:**

### Linux/Mac:
```bash
cd ~/Claude/.claude/scripts
chmod +x setup-ssh-key.sh
./setup-ssh-key.sh
```

### Windows (Git Bash):
```bash
cd /c/Users/YourName/Claude/.claude/scripts
bash setup-ssh-key.sh
```

### Android (Termux):
```bash
cd /sdcard/Claude/.claude/scripts
bash setup-ssh-key.sh
```

**What the script will ask:**
1. Your email (use the same email as your GitHub account)
2. Whether to overwrite if key exists (usually say No)

**What the script will do:**
- Create two files in `~/.ssh/`:
  - `continuity-bridge` (private key - SECRET)
  - `continuity-bridge.pub` (public key - safe to share)
- Update `~/.ssh/config` to use this key automatically
- Display your public key to copy

---

## Step 2: Copy Your Public Key

**The script will show something like:**

```
=====================================
Your SSH Public Key (copy this):
=====================================

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJqfPh... your-email@example.com

=====================================
```

**Copy EVERYTHING:**
- From `ssh-ed25519` at the start
- Through your email at the end
- Do NOT add or remove any characters
- Do NOT add line breaks

**Tip:** Triple-click the key to select the whole line, then copy.

---

## Step 3: Add Key to GitHub (Screenshots Described)

### 3.1 Go to GitHub SSH Settings

**Open your web browser and go to:**
```
https://github.com/settings/keys
```

**Or navigate manually:**
1. Click your profile picture (top right)
2. Click "Settings"
3. Click "SSH and GPG keys" (left sidebar)

### 3.2 Click "New SSH Key"

**You'll see a green button that says "New SSH key"**

Click it.

### 3.3 Fill in the Form

**You'll see a form with three fields:**

**Title:**
```
Continuity Bridge
```
(You can name it anything, but this makes it clear what it's for)

**Key type:**
```
Authentication Key
```
(Select this from the dropdown - should be the default)

**Key:**
```
[Paste your public key here]
```
(Paste the ENTIRE key you copied in Step 2)

**What it should look like:**
- Starts with `ssh-ed25519`
- Long string of random characters
- Ends with your email

**Common mistakes:**
- ❌ Only pasting part of the key
- ❌ Adding extra spaces or line breaks
- ❌ Pasting the private key instead (doesn't start with ssh-ed25519)
- ❌ Not including the email at the end

### 3.4 Click "Add SSH Key"

**Green button at the bottom of the form.**

**GitHub may ask for your password** - this is normal for security.

### 3.5 Verify It Was Added

**You should see:**
- Your new key listed on the SSH keys page
- Title: "Continuity Bridge"
- The key fingerprint (short version of the key)
- "Last used: Never" (until you use it)

---

## Step 4: Test the Connection

**Back in your terminal:**

```bash
ssh -T git@github.com-continuity-bridge
```

**Expected output if it works:**
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

**This is GOOD** - GitHub recognizes your key!

**If you see:**
```
Permission denied (publickey)
```

**This means:**
- Key not added to GitHub yet (go back to Step 3)
- Or key added but not matching (check you copied the whole key)

---

## Step 5: Clone Your Private Repo (First Time)

**Important:** Use the special hostname we configured.

**Normal GitHub URL:**
```
git@github.com:username/repo.git
```

**Continuity Bridge URL (use THIS):**
```
git@github.com-continuity-bridge:username/repo.git
```

**Notice:** `github.com-continuity-bridge` instead of just `github.com`

**Full command:**
```bash
cd ~
git clone git@github.com-continuity-bridge:username/continuity-bridge_username-anchor.git Claude
cd Claude
git checkout working
```

**Replace `username` with your actual GitHub username.**

---

## Step 6: Update Existing Repo (If Already Cloned)

**If you already cloned with the old URL, update it:**

```bash
cd ~/Claude
git remote set-url private git@github.com-continuity-bridge:username/continuity-bridge_username-anchor.git
```

**Verify it changed:**
```bash
git remote -v
```

**Should show:**
```
private  git@github.com-continuity-bridge:username/... (fetch)
private  git@github.com-continuity-bridge:username/... (push)
```

---

## Troubleshooting

### "Permission denied (publickey)"

**Possible causes:**

1. **Key not added to GitHub**
   - Go back to Step 3
   - Make sure you clicked "Add SSH key"

2. **Wrong key copied**
   - Run `cat ~/.ssh/continuity-bridge.pub`
   - Copy the ENTIRE output
   - Add to GitHub again

3. **SSH config not set up**
   - Run the setup script again
   - It will update ~/.ssh/config

### "Host key verification failed"

**First time connecting to GitHub?**
```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts
```

**This adds GitHub's fingerprint to your trusted hosts.**

### "Could not open a connection to your authentication agent"

**On Windows, start the SSH agent:**
```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/continuity-bridge
```

### "Bad permissions" error

**Fix file permissions:**
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/continuity-bridge
chmod 644 ~/.ssh/continuity-bridge.pub
chmod 600 ~/.ssh/config
```

---

## Platform-Specific Notes

### Android (Termux)

**SSH agent needs to run:**
```bash
# Add to ~/.bashrc
eval $(ssh-agent -s) > /dev/null 2>&1
ssh-add ~/.ssh/continuity-bridge 2>/dev/null
```

**Then restart Termux or run:**
```bash
source ~/.bashrc
```

### Windows

**Use Git Bash, NOT Command Prompt or PowerShell**
- Git Bash understands SSH properly
- Download from: https://git-scm.com/

**If using WSL (Windows Subsystem for Linux):**
- SSH keys work the same as Linux
- Use the Linux instructions

### Mac

**Should work exactly like Linux**
- Terminal app is fine
- iTerm2 also works great

---

## Security Best Practices

### DO:
- ✅ Keep your private key (`continuity-bridge`) SECRET
- ✅ Use a different SSH key for other projects (if you want)
- ✅ Add the public key to GitHub
- ✅ Test the connection before trying to push

### DON'T:
- ❌ Share your private key with anyone
- ❌ Email your private key
- ❌ Commit your private key to git
- ❌ Upload your private key anywhere

### If Your Key Is Compromised:

1. **Delete it from GitHub:**
   - Go to https://github.com/settings/keys
   - Click the red "Delete" button next to the key

2. **Generate a new key:**
   - Run setup-ssh-key.sh again
   - Choose to overwrite when asked

3. **Add new key to GitHub**
   - Follow Steps 3-4 again

---

## Quick Reference

### View your public key:
```bash
cat ~/.ssh/continuity-bridge.pub
```

### Test connection:
```bash
ssh -T git@github.com-continuity-bridge
```

### Check SSH config:
```bash
cat ~/.ssh/config
```

### Clone repo:
```bash
git clone git@github.com-continuity-bridge:user/repo.git
```

### Update existing remote:
```bash
git remote set-url private git@github.com-continuity-bridge:user/repo.git
```

---

## What Next?

**After SSH is working:**

1. Run preflight checks:
   ```bash
   python ~/.claude/scripts/preflight.py
   ```

2. Test git operations:
   ```bash
   cd ~/Claude
   git pull private working
   git push private working
   ```

3. If everything works, you're ready to use Continuity Bridge!

---

## Still Stuck?

**Common issues and solutions:**

**"I don't see my key on GitHub"**
→ Go to https://github.com/settings/keys and check

**"Connection works but git push fails"**
→ Check you used the `-continuity-bridge` hostname in your remote URL

**"I accidentally deleted my private key"**
→ Run setup-ssh-key.sh again, generate a new key, add to GitHub

**"Works on one computer but not another"**
→ Each computer needs its own SSH key (or copy the key between computers)

---

**Need more help?** Open an issue on the Continuity Bridge GitHub repo.
