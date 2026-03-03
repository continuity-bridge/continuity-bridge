# SPEEDRUN TO FIRST LLM PROMPT

**COPY-PASTE READY - NO FLUFF**

---

## 1️⃣ AFTER UBUNTU INSTALL - GET IP & SSH

**On server console:**

```bash
# Login with your credentials
# Then get IP:
ip addr show
```

**Note the IP:** `192.168.X.X`

**From your desktop, SSH in:**

```bash
ssh the Architect@192.168.X.X
# Type 'yes' to accept fingerprint
# Enter your password
```

---

## 2️⃣ UPDATE SYSTEM

```bash
sudo apt update && sudo apt upgrade -y
```

**Wait ~10 minutes.** Get coffee. ☕

---

## 3️⃣ INSTALL NVIDIA DRIVERS

```bash
sudo apt install -y nvidia-driver-535
```

**After install completes:**

```bash
sudo reboot
```

**IMPORTANT:** SSH will disconnect. Wait 30 seconds, then SSH back in:

```bash
ssh the Architect@192.168.X.X
```

**Verify GPU works:**

```bash
nvidia-smi
```

**Should show:** GeForce GTX 1070 Ti with CUDA 12.2 ✅

---

## 4️⃣ INSTALL TAILSCALE (Access from anywhere!)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

**Opens URL in output** - copy it, paste in desktop browser, authenticate

**Get your Tailscale IP:**

```bash
tailscale ip -4
```

**Note this IP!** Something like `100.x.x.x` - you can use this from coffee shop!

---

## 5️⃣ INSTALL DOCKER

```bash
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker the Architect
sudo systemctl enable docker
sudo systemctl start docker
```

**MUST logout and back in for docker group:**

```bash
exit
```

**SSH back in:**

```bash
ssh the Architect@192.168.X.X
# OR use Tailscale IP: ssh the Architect@100.x.x.x
```

**Verify Docker works:**

```bash
docker run hello-world
```

Should say "Hello from Docker!"

---

## 6️⃣ INSTALL OLLAMA

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Verify:**

```bash
ollama --version
```

**Check it's running:**

```bash
sudo systemctl status ollama
```

Should say "active (running)"

---

## 7️⃣ INSTALL OPEN WEBUI (ChatGPT-like interface)

```bash
docker run -d \
  --name open-webui \
  --network=host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://localhost:11434 \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

**Check it's running:**

```bash
docker ps
```

Should show `open-webui` container running

**Access in browser on your desktop:**

- Local network: `http://192.168.X.X:3000`
- Tailscale: `http://100.x.x.x:3000`

**First time:** Create admin account (any email, any password - it's local only)

---

## 8️⃣ DOWNLOAD YOUR FIRST MODEL

**Small & fast (recommended first):**

```bash
ollama pull llama3.1:8b
```

**Takes ~15 minutes.** Shows progress bar.

**Other good models to add:**

```bash
# Large & smart (40GB, takes ~40 min)
ollama pull llama3.1:70b

# Coding specialist (7GB)
ollama pull codellama:13b

# Fast instruction-following (4GB)
ollama pull mistral:7b
```

**Check what you have:**

```bash
ollama list
```

---

## 9️⃣ YOUR FIRST PROMPT! 🎉

**Method 1: Command line (quick test)**

```bash
ollama run llama3.1:8b
```

**Type your prompt, press Enter. Magic happens!**

**To exit:** Type `/bye`

---

**Method 2: Web UI (better for real use)**

1. Open browser: `http://192.168.X.X:3000`
2. Login with your admin account
3. Select model from dropdown (top)
4. Type in chat box
5. **UNLIMITED PROMPTS, NO TOKEN LIMITS!** 🚀

---

## 🎯 VERIFY GPU ACCELERATION WORKING

**While running a prompt, open second SSH session:**

```bash
nvidia-smi
```

**Should show:**

- GPU Memory usage climbing (hundreds of MB to GBs)
- GPU-Util at 50-100%
- Power usage at 100W+

**This means GPU is accelerating inference!** 🔥

---

## 🔧 USEFUL COMMANDS

**List running models:**

```bash
ollama ps
```

**Stop a model:**

```bash
ollama stop llama3.1:8b
```

**View Ollama logs:**

```bash
sudo journalctl -u ollama -f
```

**Restart Open WebUI:**

```bash
docker restart open-webui
```

**View Open WebUI logs:**

```bash
docker logs open-webui
```

---

## 🎨 CUSTOMIZE OPEN WEBUI

**In web interface:**

- Settings → Interface → Dark/Light theme
- Settings → Models → Set default model
- Upload documents (PDFs, text) for context
- Save conversations
- Create custom system prompts

---

## 📱 ACCESS FROM ANYWHERE (Tailscale)

**On your laptop/phone:**

1. Install Tailscale app
2. Login with same account
3. Open browser: `http://100.x.x.x:3000`
4. **Works from coffee shop, airport, anywhere!**

---

## ⚡ COMPLETE COMMAND SEQUENCE (COPY ALL AT ONCE)

**After first SSH login:**

```bash
# Updates
sudo apt update && sudo apt upgrade -y

# NVIDIA Drivers
sudo apt install -y nvidia-driver-535
sudo reboot

# [SSH back in after reboot]

# Verify GPU
nvidia-smi

# Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# [Authenticate in browser]

# Docker
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker the Architect
sudo systemctl enable docker
sudo systemctl start docker
exit

# [SSH back in]

# Verify Docker
docker run hello-world

# Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama --version

# Open WebUI
docker run -d \
  --name open-webui \
  --network=host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://localhost:11434 \
  --restart always \
  ghcr.io/open-webui/open-webui:main

# First Model
ollama pull llama3.1:8b

# RUN IT!
ollama run llama3.1:8b
```

---

## 🎉 SUCCESS =

**You can:**

- ✅ Type prompts in terminal
- ✅ Access web UI at http://192.168.X.X:3000
- ✅ See GPU accelerating in `nvidia-smi`
- ✅ Get instant responses with no token limits
- ✅ Access from anywhere via Tailscale

---

## 🆘 TROUBLESHOOTING

**"ollama: command not found"**

```bash
# Check if installed:
which ollama

# If not found, reinstall:
curl -fsSL https://ollama.com/install.sh | sh
```

**"Can't access web UI"**

```bash
# Check container running:
docker ps

# Check logs:
docker logs open-webui

# Restart if needed:
docker restart open-webui
```

**"GPU not being used"**

```bash
# Check drivers:
nvidia-smi

# Should show driver version and GPU
# If "command not found", reboot or reinstall drivers
```

**"Model download fails"**

```bash
# Check disk space:
df -h

# Check internet:
ping ollama.com

# Try smaller model first:
ollama pull llama3.2:1b
```

---

## 🚀 YOU'RE DONE WHEN...

You can open a browser, go to `http://192.168.X.X:3000`, type "Tell me a joke about programmers" and get a response in under 10 seconds.

**THAT'S IT. YOU WIN.** 🎉

**Saved to:** `D:/Docs/Claude/Sessions/2026-02-10/SPEEDRUN_TO_FIRST_PROMPT.md`

Reference anytime!
