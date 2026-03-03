# Adding Anthropic Claude to Open WebUI

**Source:** https://openwebui.com/posts/anthropic_2e8d9af5

## WHY DO THIS

**Hybrid Strategy:**

- Local Ollama models: Unlimited, free, fast (development)
- Claude API: Limited tokens, premium quality (production)
- Same interface: Switch between models seamlessly

**Your Free Tier Limits:**

- 100k AI tokens/month (~50 long conversations)
- 20 tool executions/month (save for production testing)

---

## STEP-BY-STEP SETUP

### Step 1: Get Your Anthropic API Key

1. **Go to:** https://console.anthropic.com/
2. **Login** with your account
3. **Navigate to:** API Keys section
4. **Copy** your API key (starts with `sk-ant-`)

**IMPORTANT:** Save this somewhere secure! You can't view it again.

---

### Step 2: Add to Open WebUI

#### SSH to Your Server

```bash
ssh the Architect@ryzen-ai
```

#### Access Open WebUI Admin

1. **Open browser to:** http://100.x.x.x:3000 (your Tailscale IP)
   
   - Or http://192.168.x.x:3000 (local network)

2. **Login** as admin

3. **Go to:** Settings (gear icon) → Admin Settings → Connections

#### Add Anthropic Connection

**Look for "External Connections" or "API Keys" section:**

```
Provider: Anthropic
API Key: sk-ant-api03-[your-key-here]
Base URL: https://api.anthropic.com/v1
```

**Or via Docker environment variables:**

```bash
# Edit docker-compose.yml
cd ~/open-webui  # or wherever you installed it
nano docker-compose.yml
```

**Add environment variables:**

```yaml
environment:
  - ANTHROPIC_API_KEY=sk-ant-api03-[your-key-here]
  - ANTHROPIC_API_BASE_URL=https://api.anthropic.com/v1
```

**Restart Open WebUI:**

```bash
docker-compose down
docker-compose up -d
```

---

### Step 3: Enable Claude Models

**In Open WebUI:**

1. **Go to:** Settings → Models
2. **Look for:** "External Models" or "Anthropic"
3. **Enable:**
   - ✅ claude-sonnet-4-5-20250514 (Sonnet 4.5 - your current version!)
   - ✅ claude-opus-4-5-20251101 (Opus 4.5 - most capable)
   - ✅ claude-haiku-4-5-20251001 (Haiku 4.5 - fastest/cheapest)

**Model Selection Tips:**

```
Development/Testing: Haiku 4.5 (cheap tokens, fast)
Production/Quality: Sonnet 4.5 (balanced)
Premium Features: Opus 4.5 (most capable, expensive)
```

---

### Step 4: Test It Works

**Start new chat in Open WebUI:**

1. **Click model selector dropdown** (top of chat)

2. **Should see:**
   
   - Local: llama3.1:8b, qwen2.5:14b, etc.
   - Remote: claude-sonnet-4.5, claude-opus-4.5, claude-haiku-4.5

3. **Select:** claude-sonnet-4.5

4. **Test prompt:**
   
   ```
   Generate a VTM V5 Gangrel character concept in exactly 50 words, 
   focusing on an unusual combination of Nature and Civilization.
   ```

5. **Verify:**
   
   - Response quality is HIGH (Claude-level)
   - Token counter shows usage
   - Model badge shows "claude-sonnet-4.5"

---

## TOKEN BUDGET STRATEGY

**Your Free Tier: 100k tokens/month**

**Token Usage (approximate):**

```
Short prompt + response: ~500 tokens
Medium conversation: ~2,000 tokens
Long character generation: ~5,000 tokens
Full session: ~10,000 tokens

100k tokens = ~50 full sessions or 200 short tasks
```

**Smart Usage Plan:**

### Phase 1: Development (Use Local Models)

```
Daily testing: Qwen 2.5 14B (local)
Code generation: Qwen 2.5 Coder 7B (local)
Quick iterations: Llama 3.1 8B (local)

Cost: $0, unlimited
```

### Phase 2: Quality Check (Use Claude Sparingly)

```
Final character polish: Claude Sonnet 4.5
User-facing backstories: Claude Sonnet 4.5
Demo content: Claude Sonnet 4.5

Cost: ~5k tokens per character = 20 characters/month
```

### Phase 3: Production (Post-Monetization)

```
Free tier users: Local models (your server)
Paid subscribers: Claude API (their subscription covers it)

Cost: Subscribers fund API usage!
```

---

## MODEL SELECTION CHEAT SHEET

**Use LOCAL models for:**

- ✅ Testing/iteration
- ✅ Development
- ✅ Code generation
- ✅ Rough drafts
- ✅ Learning/experimentation
- ✅ High volume tasks

**Use CLAUDE API for:**

- ✅ Final character generation (user-facing)
- ✅ Nuanced backstories
- ✅ Demo content for GitHub
- ✅ Marketing materials
- ✅ Complex rule interpretation
- ✅ "Make this perfect" tasks

**Performance Comparison:**

| Task    | Local (Qwen 14B) | Claude Sonnet 4.5   | Winner |
| ------- | ---------------- | ------------------- | ------ |
| Speed   | 15-20 tok/s ⚡    | 40-60 tok/s ⚡⚡      | Claude |
| Quality | Good ⭐⭐⭐         | Excellent ⭐⭐⭐⭐⭐     | Claude |
| Cost    | $0 (unlimited)   | Limited tokens      | Local  |
| Latency | 0ms (LAN)        | 50-100ms (internet) | Local  |
| Offline | ✅ Works          | ❌ Needs internet    | Local  |

---

## BANDWIDTH CONSIDERATIONS

**Adding Claude API to your setup:**

**Token traffic:**

```
Request: ~1-5KB (prompt)
Response: ~5-20KB (generated text)
Per conversation: <100KB total

Still minimal! Less than loading a webpage.
```

**T-Mobile Home Internet: Still totally fine!** ✅

**Optimization:**

```bash
# Monitor API usage in Open WebUI
# Settings → Usage → API Statistics

# Set limits per model
# Settings → Models → [model] → Rate Limits
Max tokens per request: 4096 (prevent runaway)
Max requests per minute: 5 (stay under limits)
```

---

## TROUBLESHOOTING

### Problem: "Anthropic models not showing up"

**Check:**

```bash
# Verify API key is set
docker logs open-webui | grep -i anthropic

# Should see: "Anthropic API configured"
# Should NOT see: "Invalid API key"
```

**Fix:**

```bash
# Re-add environment variable
cd ~/open-webui
nano docker-compose.yml

# Add/verify:
environment:
  - ANTHROPIC_API_KEY=sk-ant-api03-...

# Restart
docker-compose restart
```

### Problem: "API key invalid"

**Your API key format:**

```
✅ CORRECT: sk-ant-api03-[long-string]
❌ WRONG: ant-[short-string]
❌ WRONG: Just the org ID
```

**Get new key:**

- https://console.anthropic.com/settings/keys
- Delete old key, create new one
- Update Open WebUI config

### Problem: "Rate limit exceeded"

**You hit your 100k token limit!**

**Check usage:**

- https://console.anthropic.com/settings/usage
- Shows current month's consumption

**Solutions:**

1. Wait for next month (limit resets)
2. Upgrade to paid tier ($5/mo for 200k extra)
3. Use local models until reset

---

## HYBRID WORKFLOW EXAMPLE

**Sanguihedral Character Generation:**

### Step 1: Rapid Prototyping (Local)

```
Model: Qwen 2.5 14B (local, unlimited)

Prompt: "Generate 10 different Gangrel character concepts"

Result: 10 concepts in 30 seconds, cost: $0
Pick best 3 for refinement
```

### Step 2: Refinement (Local)

```
Model: Qwen 2.5 14B (local, unlimited)

Prompt: "Expand concept #3 with full stats and backstory"

Result: Complete character draft, cost: $0
Iterate 5-10 times until mechanics work
```

### Step 3: Polish (Claude API)

```
Model: Claude Sonnet 4.5 (API, premium quality)

Prompt: "Polish this character's backstory for dramatic irony 
and chronicle integration. Make it publication-ready."

Result: Professional-quality final character
Cost: ~5k tokens (5% of monthly budget)
```

### Step 4: User-Facing (Hybrid)

```
Free users: Qwen 2.5 14B (your server, unlimited)
Paid users: Claude Sonnet 4.5 (API, their subscription)

Result: Sustainable business model!
```

---

## MONITORING & LIMITS

**Track your usage:**

```bash
# In Open WebUI
Settings → Admin → Statistics → API Usage

# Shows:
- Tokens used per model
- Cost (if paid tier)
- Requests per day
- Popular models
```

**Set alerts:**

```
Settings → Admin → Limits
- Max tokens per user/day: 10k
- Max tokens per model: 4096
- Rate limits: 5 req/min
```

**Monthly budget planning:**

```
100k free tokens/month
÷ 5k tokens per character
= 20 premium characters/month

Enough for:
- Development testing: 10 characters
- Demo content: 5 characters
- User beta testing: 5 characters
```

---

## WHEN TO UPGRADE (Post-Monetization)

**Free Tier ($0/month):**

- 100k tokens ≈ 20 characters
- Good for: Personal use, testing, demos

**Tier 1 ($5/month):**

- +200k tokens = 300k total
- +20 tool calls
- Good for: Small user base (10-20 active)

**Tier 2 ($25/month):**

- +1M tokens = 1.1M total
- +200 tool calls  
- Good for: Growing user base (50-100 active)

**Break-even calculation:**

```
If 10 users × $5/month = $50 revenue
- $25 API costs = $25 profit

Sustainable at 5 paid subscribers!
```

---

## RECOMMENDED SETTINGS

**For Development:**

```yaml
Default Model: qwen2.5:14b (local, fast)
Temperature: 0.7 (balanced creativity)
Max Tokens: 4096 (reasonable length)
Top-P: 0.9 (good variety)
```

**For Production (User-Facing):**

```yaml
Free Tier: qwen2.5:14b (your server)
Paid Tier: claude-sonnet-4.5 (API)
Temperature: 0.8 (more creative)
Max Tokens: 8192 (complete characters)
Top-P: 0.95 (high quality)
```

---

## NEXT STEPS

**Today:**

- [ ] Add Anthropic API key to Open WebUI
- [ ] Test Claude Sonnet 4.5 vs Qwen 2.5 14B
- [ ] Compare quality/speed for character generation
- [ ] Document which model for which task

**This Week:**

- [ ] Build XP calculator (no AI needed)
- [ ] Test character generation with both models
- [ ] Decide: Local for dev, Claude for polish?
- [ ] Monitor token usage

**Long Term:**

- [ ] Launch with free tier (local models)
- [ ] Add paid tier (Claude API)
- [ ] Subscribers fund API costs
- [ ] Profitable! 🎉

---

**BOTTOM LINE:** You now have the BEST of both worlds - unlimited local testing + premium Claude quality when you need it! 🚀
