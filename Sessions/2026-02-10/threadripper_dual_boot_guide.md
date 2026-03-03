# Threadripper Dual Boot - Add Linux Guide
**Date:** February 10, 2026
**System:** Threadripper 1900X Desktop
**Goal:** Add Ubuntu 24.04 alongside existing Windows install

---

## 🎯 GOAL

Add Linux dual boot to Threadripper desktop **without reinstalling Windows**.

---

## ⚠️ IMPORTANT PREREQUISITES

**BEFORE YOU START:**

1. **BACKUP EVERYTHING CRITICAL** (Windows files you can't lose)

2. **Verify you have free disk space:**
   - Ubuntu needs ~50GB minimum (100GB+ recommended for comfort)
   - Games/data on 8TB HDD = safe (separate drive)
   - Check Windows C: drive has space OR
   - Check if you have a spare NVMe/SSD for Linux

3. **Disable Fast Startup in Windows:**
   - Control Panel → Power Options → Choose what power buttons do
   - Uncheck "Turn on fast startup"
   - This prevents filesystem corruption between OSes

4. **Disable Secure Boot** (maybe - check first):
   - Reboot, enter BIOS (DEL key usually)
   - Find "Secure Boot" option
   - **Only disable if Ubuntu installer complains**
   - Modern Ubuntu usually works with Secure Boot on

---

## 🗺️ DISK LAYOUT STRATEGY

**Option A: Separate Drive** ⭐ RECOMMENDED
- Install Linux on one of the 500GB NVMes
- Windows stays on its current drive
- Zero risk to Windows
- Easy to remove later (just unplug drive)
- **This is what I'd do**

**Option B: Same Drive (Shrink Windows partition)**
- Shrink Windows partition to make space
- Install Linux in free space
- More complex, small risk
- Only if you MUST share one drive

**Which do you have? Multiple NVMe drives or just one?**

---

## 📦 DISK MANAGEMENT

**If using separate drive (Option A):**

No prep needed! Just make sure drive is empty.

**If shrinking Windows (Option B):**

1. **In Windows, run Disk Management:**
   - Win+X → Disk Management
   - Right-click C: drive
   - "Shrink Volume"
   - Shrink by ~100GB (100,000 MB)
   - Leave as unallocated space

---

## 💿 UBUNTU DESKTOP 24.04 LTS

**Download:**
- https://ubuntu.com/download/desktop
- File: `ubuntu-24.04.1-desktop-amd64.iso` (~5GB)
- Create bootable USB (same process as server)

**Why Desktop not Server?**
- You're gaming on this machine
- GUI is useful
- Can run Steam, Discord, Firefox, etc.
- Still has terminal for all the power

---

## 🔧 INSTALLATION STEPS

**Boot from USB:**
1. Insert USB
2. Reboot
3. Press F12/DEL for boot menu
4. Select USB
5. "Try or Install Ubuntu"

**Choose "Install Ubuntu"**

**Installation Wizard:**

1. **Language:** English

2. **Keyboard:** US

3. **Updates:** 
   - ✅ Download updates while installing
   - ✅ Install third-party software (GPU drivers, etc.)

4. **Installation Type:** ⚠️ **CRITICAL CHOICE**

   **If separate drive:**
   - Select "Something else" (manual partitioning)
   - Select your empty NVMe drive
   - Click "New Partition Table"
   - Create partitions:
     - 1GB EFI partition (if UEFI)
     - 8GB swap (or 16GB if you want hibernation)
     - Rest as ext4 mounted at `/`
   - **Set bootloader to Linux drive** (important!)

   **If same drive:**
   - Select "Install Ubuntu alongside Windows"
   - Ubuntu will use the free space you created
   - Drag slider to allocate space
   - **Easier but less control**

5. **Location:** Your timezone

6. **User:**
   - Name: the Architect
   - Computer name: threadripper-desktop
   - Username: the Architect
   - Password: [match your Windows or different, your call]

7. **Install:** 15-30 minutes

8. **Reboot:** Remove USB when prompted

---

## 🥾 BOOT MANAGEMENT

**After install, you'll see GRUB bootloader:**
```
Ubuntu
Advanced options for Ubuntu
Windows Boot Manager
```

**To choose OS:**
- Arrow keys to select
- Enter to boot
- Default: Ubuntu after 5 seconds

**To change default:**
```bash
# After booting Ubuntu
sudo nano /etc/default/grub

# Change this line:
GRUB_DEFAULT=2  # 2 = Windows (0-indexed, so 0=Ubuntu, 2=Windows usually)

# Or set timeout:
GRUB_TIMEOUT=10  # 10 seconds to choose

# Save and update
sudo update-grub
```

---

## 🎮 GAMING ON LINUX

**Steam:**
```bash
# Enable Proton for Windows games
# In Steam: Settings → Compatibility → Enable Steam Play for all titles
```

**NVIDIA Drivers:**
```bash
sudo apt install nvidia-driver-535
sudo reboot
```

**Verify:**
```bash
nvidia-smi  # Should show your GTX 1080
```

**Most Steam games "just work" now via Proton!**

Check compatibility: https://www.protondb.com/

---

## 📂 SHARED FOLDER BETWEEN OSes

**Create NTFS partition for shared data:**

**In Windows:**
1. Disk Management
2. Create new partition (or use existing data drive)
3. Format as NTFS
4. Label it "Shared" or "Data"

**In Ubuntu:**
```bash
# Install NTFS support
sudo apt install ntfs-3g

# Find the partition
sudo fdisk -l

# Create mount point
sudo mkdir /mnt/shared

# Mount it (one-time)
sudo mount -t ntfs-3g /dev/sdXN /mnt/shared

# Make permanent (auto-mount on boot)
sudo nano /etc/fstab

# Add line:
/dev/sdXN /mnt/shared ntfs-3g defaults 0 0

# Save and test
sudo mount -a
```

**Now `/mnt/shared` is accessible from both Windows and Linux!**

Put your projects, Tailscale configs, etc. there.

---

## 🔄 SYNCTHING ON UBUNTU

```bash
# Add Syncthing repository
sudo curl -o /usr/share/keyrings/syncthing-archive-keyring.gpg \
  https://syncthing.net/release-key.gpg

echo "deb [signed-by=/usr/share/keyrings/syncthing-archive-keyring.gpg] \
  https://apt.syncthing.net/ syncthing stable" | \
  sudo tee /etc/apt/sources.list.d/syncthing.list

# Install
sudo apt update
sudo apt install syncthing

# Enable for your user
systemctl --user enable syncthing
systemctl --user start syncthing

# Access Web UI
http://localhost:8384
```

**Configure sync folders to `/mnt/shared` so Windows can access too!**

---

## 🚫 NO SNAPS - USE FLATPAK

**Remove Snap (if you want):**
```bash
# List installed snaps
snap list

# Remove them
sudo snap remove --purge [package]

# Remove snapd
sudo apt remove --purge snapd

# Clean up
rm -rf ~/snap
sudo rm -rf /var/cache/snapd
```

**Install Flatpak:**
```bash
# Install Flatpak
sudo apt install flatpak

# Add Flathub repository
flatpak remote-add --if-not-exists flathub \
  https://flathub.org/repo/flathub.flatpakrepo

# Install GNOME Software with Flatpak support
sudo apt install gnome-software-plugin-flatpak

# Reboot
sudo reboot
```

**Now install apps via Flatpak:**
```bash
# Example: Discord
flatpak install flathub com.discordapp.Discord

# Run it
flatpak run com.discordapp.Discord
```

**Or use GNOME Software GUI (shows Flatpak apps)**

---

## 🎯 DESKTOP ENVIRONMENT CHOICE

**Ubuntu 24.04 comes with GNOME 46 by default.**

**If you want something lighter:**

**KDE Plasma:**
```bash
sudo apt install kubuntu-desktop
# Choose kdm at prompt
# Logout, select KDE from login screen
```

**XFCE (very light):**
```bash
sudo apt install xubuntu-desktop
```

**Stick with GNOME unless you have a reason to change!**

---

## 🛡️ ADDITIONAL SETUP

**Gaming optimizations:**
```bash
# Install GameMode (boosts performance)
sudo apt install gamemode

# Enable in Steam: Right-click game → Properties → Launch Options
# Add: gamemoderun %command%
```

**Development tools:**
```bash
sudo apt install build-essential git curl wget
```

**VS Code (via .deb, not snap):**
```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | \
  gpg --dearmor > packages.microsoft.gpg

sudo install -D -o root -g root -m 644 packages.microsoft.gpg \
  /etc/apt/keyrings/packages.microsoft.gpg

echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] \
  https://packages.microsoft.com/repos/code stable main" | \
  sudo tee /etc/apt/sources.list.d/vscode.list

sudo apt update
sudo apt install code
```

---

## ⏱️ TIME ESTIMATE

**Dual boot setup:**
- Disk prep (if shrinking): 10 min
- Create USB: 10 min
- Installation: 30 min
- Drivers + updates: 20 min
- Syncthing + Flatpak setup: 15 min
- Testing both OSes: 15 min

**TOTAL: ~1.5-2 hours**

**NOT including game installs or data migration**

---

## 🔍 VERIFICATION

**After setup, verify:**
- [ ] Can boot Windows (all games work)
- [ ] Can boot Ubuntu (GUI loads)
- [ ] NVIDIA drivers work in Ubuntu (`nvidia-smi`)
- [ ] Shared folder accessible from both OSes
- [ ] Syncthing running and syncing
- [ ] Steam runs in Ubuntu
- [ ] Test one game in Proton
- [ ] Flatpak working (no snaps)

---

## 🆘 TROUBLESHOOTING

**"Windows disappeared from GRUB menu!"**
```bash
sudo update-grub
# Scans for OSes and rebuilds menu
```

**"Shared folder read-only in Ubuntu"**
```bash
# Fix permissions
sudo chown -R the Architect:the Architect /mnt/shared
```

**"Game won't run in Linux"**
- Check ProtonDB for compatibility
- Try different Proton version in Steam
- Some games genuinely won't work (anti-cheat issues)
- Dual boot exists for this reason!

**"Can't access Linux files from Windows"**
- Normal! Windows can't read ext4
- Use shared NTFS partition instead
- Or access via network (Samba)

---

## 💭 MY RECOMMENDATION

**For your use case:**

1. **Install Ubuntu 24.04 Desktop on a separate NVMe** (if you have one)
2. **Keep Windows on its current drive**
3. **Use 8TB HDD as shared data drive** (format partition as NTFS)
4. **Set up Syncthing on both OSes** (sync to shared drive)
5. **Default boot to Windows** (gaming primary), select Ubuntu when coding

**This gives you:**
- ✅ Zero risk to Windows
- ✅ Easy removal if needed (just unplug drive)
- ✅ Full performance on both OSes
- ✅ Shared data via NTFS partition
- ✅ Syncthing keeps laptop in sync

**Does this work for you?**

Let me know if you want to proceed or have questions!
