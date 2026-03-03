# Ryzen-AI Server Security Hardening

## OBJECTIVE

Air-gap LLM server to ONLY allow access via Tailscale with HTTPS encryption

**Current State:**

- ✅ Server running: Ubuntu Server 24.04
- ✅ Open WebUI accessible: http://192.168.x.x:3000
- ✅ Tailscale installed: https://ryzen-ai.fell-pentatonic.ts.net
- ❌ HTTPS not configured yet
- ❌ Still accessible on local network (security risk)

**Goal State:**

- ✅ ONLY accessible via Tailscale (100.x.x.x network)
- ✅ HTTPS enabled (encrypted traffic)
- ✅ Certificate valid (Let's Encrypt or self-signed)
- ❌ Local network access BLOCKED (192.168.x.x)
- ✅ Mobile/laptop access works via Tailscale

---

## REFERENCE MATERIALS

**Primary Guide:**
https://henrynavarro.org/deploy-your-own-open-webui-interface-with-https-security-53a6ea2609d7

**Tailscale Docs:**

- Tailscale HTTPS: https://tailscale.com/kb/1153/enabling-https
- Tailscale Serve: https://tailscale.com/kb/1242/tailscale-serve

---

## IMPLEMENTATION STEPS

### Phase 1: Configure UFW Firewall (15 min)

**Goal:** Block all non-Tailscale access

```bash
# SSH into ryzen-ai server
ssh the Architect@ryzen-ai

# Install UFW if not present
sudo apt update
sudo apt install ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (critical - don't lock yourself out!)
sudo ufw allow 22/tcp

# Allow Tailscale interface ONLY
sudo ufw allow in on tailscale0

# Enable firewall
sudo ufw enable

# Verify rules
sudo ufw status verbose
```

**Test:**

- ✅ Can access via Tailscale: http://100.x.x.x:3000
- ❌ Cannot access via LAN: http://192.168.x.x:3000
- ✅ SSH still works

---

### Phase 2: Set Up HTTPS with Tailscale Serve (20 min)

**Option A: Tailscale HTTPS (Recommended - Easiest)**

Tailscale provides automatic HTTPS certificates for your tailnet!

```bash
# Enable Tailscale Serve with HTTPS
tailscale serve https / http://127.0.0.1:3000

# This automatically:
# - Gets HTTPS cert from Tailscale
# - Serves Open WebUI over HTTPS
# - Makes it available at: https://ryzen-ai.fell-pentatonic.ts.net
```

**Option B: Let's Encrypt (More Complex)**

If you want public-facing domain:

```bash
# Install Caddy (simpler than nginx for HTTPS)
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Configure Caddy
sudo nano /etc/caddy/Caddyfile
```

Add:

```
ryzen-ai.fell-pentatonic.ts.net {
    reverse_proxy localhost:3000
}
```

```bash
# Start Caddy
sudo systemctl restart caddy
sudo systemctl enable caddy
```

---

### Phase 3: Verify Security (10 min)

**Security Checklist:**

```bash
# 1. Check firewall status
sudo ufw status numbered

# 2. Check what's listening on ports
sudo netstat -tulpn | grep LISTEN

# 3. Verify Open WebUI only on localhost
sudo netstat -tulpn | grep 3000
# Should show: 127.0.0.1:3000 (NOT 0.0.0.0:3000)

# 4. Check Tailscale status
tailscale status
```

**From external device (laptop/phone):**

- ✅ https://ryzen-ai.fell-pentatonic.ts.net works
- ❌ http://192.168.x.x:3000 times out
- ✅ Certificate is valid (no browser warning)

---

### Phase 4: Update Open WebUI Config (5 min)

**Configure Open WebUI to only bind to localhost:**

```bash
# Edit docker-compose.yml or systemd service
cd ~/open-webui  # or wherever it's installed

# If using Docker:
nano docker-compose.yml
```

Change port binding from:

```yaml
ports:
  - "3000:8080"
```

To:

```yaml
ports:
  - "127.0.0.1:3000:8080"
```

```bash
# Restart Open WebUI
docker-compose down
docker-compose up -d

# Verify it's only listening on localhost
sudo netstat -tulpn | grep 3000
# Should show: 127.0.0.1:3000
```

---

## SECURITY BENEFITS

**Zero Trust Access:**

- ✅ Only Tailscale network can reach server
- ✅ Requires Tailscale authentication
- ✅ Can revoke access per-device

**Encrypted Traffic:**

- ✅ HTTPS for all connections
- ✅ Protects API keys, prompts, responses
- ✅ No plaintext over network

**Attack Surface Reduction:**

- ✅ Not exposed to local network
- ✅ Not port-forwarded to internet
- ✅ Firewall blocks unauthorized access

**Audit Trail:**

- ✅ Tailscale logs all connections
- ✅ Can see which devices accessed when
- ✅ Can force reauthentication

---

## TROUBLESHOOTING

**Problem: Locked out of server**

```bash
# If you can access physically:
# 1. Connect monitor/keyboard
# 2. Disable UFW: sudo ufw disable
# 3. Fix rules, re-enable
```

**Problem: Tailscale HTTPS not working**

```bash
# Check Tailscale Serve status
tailscale serve status

# Restart Tailscale
sudo systemctl restart tailscaled
```

**Problem: Open WebUI won't start**

```bash
# Check logs
docker logs open-webui

# Or if systemd:
sudo journalctl -u open-webui -f
```

---

## PRIORITY & TIMELINE

**Priority:** HIGH (security hardening)
**Estimated Time:** 1-2 hours total
**Complexity:** Moderate (firewall + reverse proxy)
**Risk:** Low (can rollback if issues)

**Best Time:** When you have 2 uninterrupted hours and can physically access server if needed

---

## ROLLBACK PLAN

If something goes wrong:

```bash
# Disable firewall
sudo ufw disable

# Stop Tailscale Serve
tailscale serve off

# Restart Open WebUI with original config
docker-compose down
# Restore original docker-compose.yml
docker-compose up -d
```

---

## NOTES

**From paranoid security nerd to paranoid security nerd:**

- This is solid defense-in-depth
- Tailscale's WireGuard is battle-tested
- HTTPS prevents MITM attacks
- Firewall prevents lateral movement
- You control the attack surface

**Bad actors ARE everywhere these days.** This setup makes you a hard target. 👍
