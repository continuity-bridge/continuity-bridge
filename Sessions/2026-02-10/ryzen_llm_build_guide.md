# Ryzen LLM Server Build Guide

**Date:** February 10, 2026, 4:15 PM
**System:** Ryzen 5 5600X LLM Server (Headless)
**User:** the Architect (the Architect)

---

## 📋 QUICK ANSWERS

### Which Ubuntu ISO?

**Ubuntu Server 24.04.1 LTS**

- Download: https://ubuntu.com/download/server
- File: `ubuntu-24.04.1-live-server-amd64.iso`
- Size: ~2.8GB
- Create bootable USB with Rufus (Windows) or `dd` (Linux)

### Which PSU?

**NZXT C650 80+ Gold (Fully Modular)** ✅ RECOMMENDED

- 650W is plenty (system draws ~290W peak)
- 80+ Gold = better efficiency (lower power bill for 24/7)
- Fully modular = cleanest cable management
- Quality: NZXT is solid, this is their good line

**Why not the others?**

- EVGA 850W Bronze: Overkill wattage, less efficient, partially modular = messy
- Thermaltake 650W: Non-modular = cable hell, lower quality

### Tailscale Note

Perfect - no need for port forwarding or static IP hassles. Access from anywhere!

---

## 🛠️ PARTS LIST

**What You Have:**

- ✅ Ryzen 5 5600X CPU
- ✅ Gigabyte Vision D AM4 motherboard
- ✅ 64GB DDR4-3956 RAM (4 sticks)
- ✅ GTX 1070 Ti 8GB GPU
- ✅ 500GB NVMe drive
- ✅ 4TB Enterprise HDD (optional backup)
- ✅ NZXT C650 PSU
- ⚠️ Case (assuming you have one?)

**What You Need:**

- Ubuntu Server 24.04.1 ISO
- USB drive (8GB+) for installer
- Keyboard + monitor (for initial setup only)
- Ethernet cable

---

## ⚡ BUILD STEPS

### Phase 1: Hardware Assembly (~30-60 min)

**Most is already installed, so this is mainly PSU + GPU:**

1. **Install PSU**
   
   - Mount in case (usually bottom, fan down if vents present)
   - Route cables: 24-pin ATX, 8-pin EPS (CPU), 8-pin PCIe (GPU)
   - Leave extras disconnected (fully modular advantage!)

2. **Install GPU**
   
   - Remove 2 PCIe slot covers
   - Insert GTX 1070 Ti into top PCIe x16 slot
   - Screw down bracket
   - Connect 8-pin PCIe power (might be 6+2 pin)

3. **Verify existing install**
   
   - CPU cooler secure? (Check retention)
   - RAM in correct slots? (A2/B2 for dual channel - consult mobo manual)
   - NVMe installed? (M.2 slot under heatsink probably)

4. **Cable check**
   
   - 24-pin ATX to motherboard ✓
   - 8-pin EPS to CPU power ✓
   - 8-pin PCIe to GPU ✓
   - SATA power to HDD (if using) ✓
   - Front panel connectors ✓

5. **First boot test (no OS yet)**
   
   - Connect monitor, keyboard, ethernet
   - Power on
   - Should POST and show BIOS/UEFI
   - Verify RAM shows 64GB
   - Verify NVMe detected
   - **Enable XMP/DOCP** in BIOS for RAM (gets you to 3956MHz)
   - **Save & Exit**

---

### Phase 2: Ubuntu Server Installation (~30 min)

**Create Bootable USB:**

**From Windows (Threadripper):**

- Download Rufus: https://rufus.ie/
- Insert USB drive
- Rufus settings:
  - Device: Your USB
  - Boot selection: Ubuntu Server ISO
  - Partition scheme: GPT
  - Target system: UEFI
  - Click START

**From Linux:**

```bash
# Find USB device
lsblk

# Write ISO (replace sdX with your USB - BE CAREFUL!)
sudo dd if=ubuntu-24.04.1-live-server-amd64.iso of=/dev/sdX bs=4M status=progress
sudo sync
```

**Boot from USB:**

1. Insert USB in Ryzen system
2. Power on, press F12/DEL for boot menu (varies by board)
3. Select USB drive
4. Ubuntu installer starts

---

### Phase 3: Headless Installation (~20 min)

**You'll use keyboard + monitor for install, then never again.**

**Installation Steps:**

1. **Language:** English

2. **Keyboard:** US (or your layout)

3. **Installation Type:** Ubuntu Server (not minimal)

4. **Network:**
   
   - Should auto-detect ethernet
   - Select DHCP (T-Mobile modem will assign IP)
   - **Note the IP address shown** - you'll need it!

5. **Proxy:** Leave blank (unless you have one)

6. **Mirror:** Default Ubuntu mirror (or pick closer one)

7. **Storage:**
   
   - ✅ **Use entire disk** (the 500GB NVMe)
   - ✅ **Set up this disk as an LVM group** (allows future flexibility)
   - Default layout is fine
   - **IMPORTANT:** This will erase the NVMe - make sure it's empty!

8. **Storage Summary:**
   
   - Should show ~500GB NVMe
   - One partition for /boot
   - Rest as LVM volume for /
   - Confirm and continue

9. **Profile Setup:**
   
   - Your name: the Architect (or whatever)
   - Server name: `llm-server` (or `ryzen-ai`, your choice)
   - Username: `the Architect` (lowercase, no spaces)
   - Password: [your secure password]
   - **Write these down!**

10. **SSH Setup:**
    
    - ✅ **Install OpenSSH server** ← CRITICAL! Check this box!
    - **Import SSH identity:** Skip (set up keys later)

11. **Featured Server Snaps:**
    
    - ❌ **Uncheck ALL** (you said no snaps!)
    - We'll install what we need via apt/docker

12. **Installation:**
    
    - Confirm and begin
    - Takes ~10 minutes
    - Remove USB when prompted
    - Reboot

---

### Phase 4: First Login & Updates (~15 min)

**After reboot:**

1. **Login at console:**
   
   ```bash
   llm-server login: the Architect
   Password: [your password]
   ```

2. **Check IP address:**
   
   ```bash
   ip addr show
   ```
   
   Look for `inet 192.168.X.X` under ethernet interface
   **Write this down!** You'll use it to SSH in.

3. **Update system:**
   
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```
   
   (Takes 5-10 min, installs security updates)

4. **Verify GPU detected:**
   
   ```bash
   lspci | grep -i nvidia
   ```
   
   Should show: `NVIDIA Corporation GP104 [GeForce GTX 1070 Ti]`

5. **Shutdown and disconnect monitor/keyboard:**
   
   ```bash
   sudo shutdown -h now
   ```

**From here on, everything is SSH!**

---

## 🔌 TAILSCALE SETUP

**On Ryzen LLM Server (via SSH from desktop):**

```bash
# SSH in from desktop
ssh the Architect@192.168.X.X  # Use the IP from earlier

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Connect to your Tailscale network
sudo tailscale up

# This will show a URL - open it in browser on desktop
# Authenticate with your Tailscale account
# Server will appear in your Tailscale admin panel

# Check Tailscale IP
tailscale ip -4
# Write this down - it's your permanent Tailscale IP!
```

**Now you can SSH via Tailscale from anywhere:**

```bash
ssh the Architect@100.x.x.x  # Your Tailscale IP
```

**Even from coffee shop wifi!** 🎉

---

## 🐳 DOCKER INSTALLATION

**Why Docker?** Open WebUI (the LLM frontend) runs in Docker - clean and isolated.

```bash
# Install Docker
sudo apt install -y docker.io docker-compose

# Add your user to docker group (avoid sudo)
sudo usermod -aG docker the Architect

# Enable Docker to start on boot
sudo systemctl enable docker
sudo systemctl start docker

# Logout and back in for group to take effect
exit
ssh the Architect@[tailscale-ip]

# Verify Docker works
docker run hello-world
```

---

## 🦙 OLLAMA INSTALLATION

```bash
# Official Ollama installer
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version

# Test with small model (optional)
ollama run llama3.2:1b
# (This downloads ~1GB model and runs chat)
# Type /bye to exit

# Check Ollama service
sudo systemctl status ollama
```

Ollama runs on `localhost:11434` by default.

---

## 🌐 OPEN WEBUI INSTALLATION

**This gives you ChatGPT-like interface for all your models.**

```bash
# Run Open WebUI container
docker run -d \
  --name open-webui \
  --network=host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://localhost:11434 \
  --restart always \
  ghcr.io/open-webui/open-webui:main

# Check it's running
docker ps

# View logs
docker logs open-webui
```

**Access Web UI:**

- Local: `http://localhost:3000`
- Tailscale: `http://[tailscale-ip]:3000`
- From desktop/laptop: `http://[tailscale-ip]:3000` in browser

**First time:**

- Create admin account
- You'll see "No models" - we'll add them next!

---

## 📦 DOWNLOAD MODELS

**Via CLI (SSH):**

```bash
# Small, fast model (4.7GB, great for daily use)
ollama pull llama3.1:8b

# Large, smart model (40GB, best quality)
ollama pull llama3.1:70b

# Coding specialist (7.4GB)
ollama pull codellama:13b

# Instruction-following (4.1GB)
ollama pull mistral:7b

# Check what you have
ollama list
```

**Via Web UI:**

- Go to http://[tailscale-ip]:3000
- Click "Models" in sidebar
- Click "Pull a model"
- Enter model name (e.g., `llama3.1:70b`)
- Watch download progress

---

## 🎛️ NVIDIA DRIVERS (For GPU Acceleration)

**Check if NVIDIA drivers needed:**

```bash
nvidia-smi
```

**If it says "command not found", install drivers:**

```bash
# Add NVIDIA repository
sudo apt install -y nvidia-driver-535

# Reboot to load drivers
sudo reboot

# SSH back in after reboot
ssh the Architect@[tailscale-ip]

# Verify GPU works
nvidia-smi
```

**Should show:**

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx.xx              Driver Version: 535.xx.xx    CUDA: 12.x  |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
|   0  NVIDIA GeForce GTX 1070 Ti  Off | 00000000:01:00.0  Off |  N/A             |
|...                                                                           |
+-----------------------------------------------------------------------------+
```

**Ollama will automatically use GPU when available!**

**Check GPU usage during inference:**

```bash
# In one terminal, watch GPU usage
watch -n 1 nvidia-smi

# In another, run a model
ollama run llama3.1:70b
```

You'll see GPU memory fill up and utilization spike! 🚀

---

## ⚙️ OPTIONAL: 4TB BACKUP DRIVE

**If you want to mount the 4TB HDD:**

```bash
# Find the drive
lsblk

# Create mount point
sudo mkdir -p /mnt/backup

# Format drive (ONE TIME ONLY - ERASES DRIVE!)
sudo mkfs.ext4 /dev/sdb  # Replace sdb with your drive!

# Get UUID
sudo blkid /dev/sdb

# Add to /etc/fstab for auto-mount
sudo nano /etc/fstab

# Add this line (replace UUID with yours):
UUID=your-uuid-here /mnt/backup ext4 defaults 0 2

# Save (Ctrl+O, Enter, Ctrl+X)

# Mount it
sudo mount -a

# Verify
df -h | grep backup
```

**Use for:**

- Model backups: `cp ~/.ollama/models/* /mnt/backup/models/`
- Data persistence
- Docker volume backups

---

## 🔧 SYSTEM OPTIMIZATION

**Automatic updates:**

```bash
# Install unattended-upgrades
sudo apt install -y unattended-upgrades

# Enable it
sudo dpkg-reconfigure -plow unattended-upgrades
# Select "Yes"
```

**Set static hostname for Tailscale:**

```bash
# Edit /etc/hosts
sudo nano /etc/hosts

# Add line:
100.x.x.x   llm-server  # Your Tailscale IP

# Save and exit
```

**Enable GPU persistence mode (keeps GPU ready):**

```bash
# Add to crontab
crontab -e

# Add this line:
@reboot sudo nvidia-smi -pm 1

# Save and exit
```

---

## 📊 MONITORING

**Check system resources:**

```bash
# CPU, RAM, disk
htop

# GPU usage
nvidia-smi

# Disk space
df -h

# Docker containers
docker ps
```

**Monitor Ollama:**

```bash
# Check running models
ollama ps

# View logs
sudo journalctl -u ollama -f
```

---

## 🚀 USAGE EXAMPLES

**CLI (SSH):**

```bash
# Chat with model
ollama run llama3.1:70b "Explain quantum computing"

# Use in scripts
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:70b",
  "prompt": "Write a Python function to calculate fibonacci"
}'
```

**Web UI:**

- Go to http://[tailscale-ip]:3000
- Select model from dropdown
- Chat like ChatGPT!
- Upload documents (PDFs, text files)
- Save conversations

**From Desktop (VS Code):**

- Install "Ollama" extension
- Configure: `http://[tailscale-ip]:11434`
- Use inline code suggestions!

---

## 🔒 SECURITY NOTES

**Firewall (UFW):**

```bash
# Enable firewall
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Ollama is only on localhost (safe)
# Open WebUI is only on Tailscale (safe)

# Check status
sudo ufw status
```

**SSH Keys (Better than passwords):**

```bash
# On your desktop, generate key (if you don't have one)
ssh-keygen -t ed25519

# Copy to server
ssh-copy-id the Architect@[tailscale-ip]

# Now you can SSH without password!
ssh the Architect@[tailscale-ip]
```

**Disable password SSH (optional, after keys work):**

```bash
sudo nano /etc/ssh/sshd_config

# Change this line:
PasswordAuthentication no

# Reload SSH
sudo systemctl reload sshd
```

---

## 🎯 COMPLETE CHECKLIST

**Hardware:**

- [ ] PSU installed and cables routed
- [ ] GPU installed with power connected
- [ ] RAM in correct slots (A2/B2)
- [ ] NVMe detected in BIOS
- [ ] XMP/DOCP enabled for RAM speed
- [ ] POST successful

**Software:**

- [ ] Ubuntu Server 24.04 installed
- [ ] System updated (`apt upgrade`)
- [ ] OpenSSH working
- [ ] Tailscale installed and connected
- [ ] Docker installed and user added to group
- [ ] NVIDIA drivers installed (`nvidia-smi` works)
- [ ] Ollama installed and running
- [ ] Open WebUI container running
- [ ] At least one model downloaded

**Access:**

- [ ] Can SSH via Tailscale IP
- [ ] Can access Web UI at http://[tailscale-ip]:3000
- [ ] GPU acceleration working (check `nvidia-smi` during inference)

**Optional:**

- [ ] 4TB backup drive mounted
- [ ] SSH keys configured
- [ ] Unattended upgrades enabled
- [ ] Monitoring tools installed (htop, etc.)

---

## 📞 HELP

**Common Issues:**

**"GPU not detected"**

- Check `lspci | grep -i nvidia` shows card
- Install/reinstall drivers: `sudo apt install nvidia-driver-535`
- Reboot after driver install

**"Ollama not using GPU"**

- Check `nvidia-smi` during inference
- Verify CUDA drivers: `nvidia-smi` should show CUDA version
- Check Ollama logs: `sudo journalctl -u ollama -f`

**"Can't access Web UI"**

- Check container running: `docker ps`
- Check logs: `docker logs open-webui`
- Verify Tailscale IP: `tailscale ip -4`
- Try `http://localhost:3000` from server itself

**"Model download fails"**

- Check disk space: `df -h`
- Check internet: `ping ollama.com`
- Try smaller model first: `ollama pull llama3.2:1b`

---

## ⏱️ ESTIMATED TIME

**Total time from parts to working LLM:**

- Hardware assembly: 30-60 min
- OS installation: 30 min
- Updates + drivers: 20 min
- Tailscale + Docker + Ollama: 20 min
- Open WebUI: 10 min
- Download first model: 15-60 min (depends on model size)

**TOTAL: ~2-4 hours** (including download time)

**Most of this can be hands-off while models download!**

---

## 🎉 SUCCESS LOOKS LIKE

You'll be able to:

- SSH to `the Architect@[tailscale-ip]` from anywhere
- Open `http://[tailscale-ip]:3000` in browser
- Chat with Llama 3.1 70B (or any model)
- See GPU working in `nvidia-smi`
- Run unlimited inference with no token limits
- Keep Threadripper desktop unchanged for gaming
- Access from work laptop via Tailscale

**No more message limits!** 🚀

---

**Let me know when you're ready to start and I'll be here for any questions!**
