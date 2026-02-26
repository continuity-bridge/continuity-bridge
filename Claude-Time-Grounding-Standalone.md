# Time-Grounding for Claude (Standalone System)

**For:** Claude.ai website users (no Claude Desktop required)  
**Created:** February 26, 2026  
**By:** Vector (Claude AI) via continuity-bridge  
**Problem:** Claude has no time sense - can't help manage sessions or understand urgency  
**Solution:** Custom instructions + simple timer webpage

---

## Quick Start (3 Steps)

1. **Copy custom instructions to Claude.ai** (Section 1 below)
2. **Save timer webpage** (Section 2 below)
3. **Use them together** (Section 3 below)

Total setup time: ~5 minutes

---

## Section 1: Custom Instructions for Claude.ai

Go to **Claude.ai → Settings → Personalization → Custom Instructions**

Paste this:

```
TEMPORAL AWARENESS PROTOCOL:

When I start a conversation, I'll tell you what time it is and optionally set a session goal.

Your responsibilities:
1. Note the start time for reference throughout our conversation
2. Track approximate session duration based on our exchange count
3. Proactively check in about time after sustained exchanges (~45-60 min of back-and-forth)
4. Give gentle nudges if I seem hyperfocused and losing track of time

Example session start:
"Hey Claude, it's 8:30 AM Thursday. Let's work on debugging this API."

If I forget to mention the time, politely ask:
"Before we start - what time is it where you are? Helps me track our session duration."

Time-aware behaviors you should exhibit:

DURING SESSION:
- After ~45-60 minutes of sustained back-and-forth: "Quick time check - we've been at this about an hour based on our exchange. Want to keep going or take a break?"
- If I mention a deadline: Help me track toward it ("You mentioned needing to stop by 3 PM - we have about 45 minutes left")
- Estimate duration from conversation pace: ~5-10 min per substantial exchange

LATE NIGHT (if I mention it's past midnight):
- More gentle about suggesting wrap-up
- Acknowledge the hour: "It's 2 AM - this is intense focus time. Let me know if you want to call it."
- Don't be pushy, but do check in after long exchanges

LONG SESSIONS (90+ min based on our back-and-forth):
- "We've been going strong for about 90 minutes. Worth taking a quick break?"
- Respect if I say no, but note the duration

IMPORTANT: Base your time estimates on:
1. The time I told you at session start
2. Number and depth of exchanges we've had
3. Explicit time updates I give you ("it's now 10:30")

You won't have perfect accuracy, but approximate awareness is valuable.
```

**Save that.** Custom instructions apply to all new conversations.

---

## Section 2: Timer Webpage

Create a file called `claude-timer.html` anywhere on your computer. Paste this code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Session Timer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 450px;
            width: 100%;
            text-align: center;
        }
        
        h1 {
            margin-bottom: 30px;
            color: #333;
            font-size: 28px;
            font-weight: 600;
        }
        
        .time-display {
            margin: 20px 0;
        }
        
        .label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        #current-time {
            font-size: 56px;
            font-weight: 700;
            color: #667eea;
            margin: 10px 0;
            font-variant-numeric: tabular-nums;
        }
        
        #current-date {
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        }
        
        #session-duration {
            font-size: 48px;
            font-weight: 700;
            color: #16a34a;
            margin: 10px 0;
            font-variant-numeric: tabular-nums;
        }
        
        .button-group {
            display: flex;
            gap: 12px;
            margin: 30px 0;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        button {
            padding: 14px 28px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            flex: 1;
            min-width: 120px;
        }
        
        .start-btn {
            background: #16a34a;
            color: white;
        }
        
        .start-btn:hover {
            background: #15803d;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(22, 163, 74, 0.4);
        }
        
        .reset-btn {
            background: #dc2626;
            color: white;
        }
        
        .reset-btn:hover {
            background: #b91c1c;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
        }
        
        .copy-btn {
            background: #667eea;
            color: white;
            margin-top: 10px;
            width: 100%;
        }
        
        .copy-btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        #status {
            margin-top: 20px;
            padding: 12px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .status-waiting {
            background: #fef3c7;
            color: #92400e;
        }
        
        .status-active {
            background: #dcfce7;
            color: #166534;
        }
        
        .warning {
            background: #fee2e2;
            color: #991b1b;
            padding: 16px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 14px;
            font-weight: 500;
            border-left: 4px solid #dc2626;
        }
        
        .info-box {
            background: #f0f9ff;
            color: #075985;
            padding: 16px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 13px;
            text-align: left;
            border-left: 4px solid #0284c7;
        }
        
        .info-box strong {
            display: block;
            margin-bottom: 8px;
            color: #0c4a6e;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⏰ Claude Session Timer</h1>
        
        <div class="time-display">
            <div class="label">Current Time</div>
            <div id="current-time">--:--</div>
            <div id="current-date">Loading...</div>
        </div>
        
        <div class="time-display">
            <div class="label">Session Duration</div>
            <div id="session-duration">Not Started</div>
        </div>
        
        <div class="button-group">
            <button class="start-btn" onclick="startSession()">Start Session</button>
            <button class="reset-btn" onclick="resetSession()">Reset</button>
        </div>
        
        <button class="copy-btn" onclick="copyTimeInfo()">📋 Copy Time Info for Claude</button>
        
        <div id="status" class="status-waiting">Click "Start Session" to begin tracking</div>
        
        <div id="warning" style="display: none;" class="warning"></div>
        
        <div class="info-box">
            <strong>💡 How to use:</strong>
            1. Click "Start Session" when you open Claude<br>
            2. Copy time info and paste into Claude to start<br>
            3. Timer runs in background - check periodically<br>
            4. Claude will remind you to take breaks
        </div>
    </div>
    
    <script>
        let sessionStart = null;
        let timerInterval = null;
        
        function updateCurrentTime() {
            const now = new Date();
            const hours = now.getHours();
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';
            const displayHours = hours % 12 || 12;
            
            document.getElementById('current-time').textContent = 
                `${displayHours}:${minutes} ${ampm}`;
            
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            
            document.getElementById('current-date').textContent = 
                `${days[now.getDay()]}, ${months[now.getMonth()]} ${now.getDate()}`;
        }
        
        function updateSessionDuration() {
            if (!sessionStart) {
                document.getElementById('session-duration').textContent = 'Not Started';
                return;
            }
            
            const now = Date.now();
            const elapsed = Math.floor((now - sessionStart) / 1000);
            
            const hours = Math.floor(elapsed / 3600);
            const minutes = Math.floor((elapsed % 3600) / 60);
            const seconds = elapsed % 60;
            
            let display;
            if (hours > 0) {
                display = `${hours}h ${minutes}m`;
            } else if (minutes > 0) {
                display = `${minutes}m ${seconds}s`;
            } else {
                display = `${seconds}s`;
            }
            
            document.getElementById('session-duration').textContent = display;
            
            // Show warning after 90 minutes
            const warningDiv = document.getElementById('warning');
            if (elapsed > 5400) { // 90 minutes
                warningDiv.style.display = 'block';
                const warningHours = Math.floor(elapsed / 3600);
                const warningMins = Math.floor((elapsed % 3600) / 60);
                warningDiv.textContent = `⚠️ Long session (${warningHours}h ${warningMins}m) - Consider taking a break!`;
            } else {
                warningDiv.style.display = 'none';
            }
        }
        
        function startSession() {
            if (sessionStart) {
                // Already started
                return;
            }
            
            sessionStart = Date.now();
            
            if (timerInterval) {
                clearInterval(timerInterval);
            }
            
            timerInterval = setInterval(() => {
                updateCurrentTime();
                updateSessionDuration();
            }, 1000);
            
            document.getElementById('status').textContent = '✅ Session active - tracking time';
            document.getElementById('status').className = 'status-active';
            
            updateCurrentTime();
            updateSessionDuration();
        }
        
        function resetSession() {
            sessionStart = null;
            
            if (timerInterval) {
                clearInterval(timerInterval);
                timerInterval = null;
            }
            
            document.getElementById('session-duration').textContent = 'Not Started';
            document.getElementById('status').textContent = 'Click "Start Session" to begin tracking';
            document.getElementById('status').className = 'status-waiting';
            document.getElementById('warning').style.display = 'none';
            
            updateCurrentTime();
        }
        
        function copyTimeInfo() {
            const now = new Date();
            const hours = now.getHours();
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const ampm = hours >= 12 ? 'PM' : 'AM';
            const displayHours = hours % 12 || 12;
            
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const dayName = days[now.getDay()];
            
            let message = `Hey Claude, it's ${displayHours}:${minutes} ${ampm} on ${dayName}.`;
            
            if (sessionStart) {
                const elapsed = Math.floor((Date.now() - sessionStart) / 1000);
                const hours = Math.floor(elapsed / 3600);
                const mins = Math.floor((elapsed % 3600) / 60);
                
                if (hours > 0) {
                    message += ` We've been working for ${hours}h ${mins}m.`;
                } else if (mins > 0) {
                    message += ` We've been working for ${mins} minutes.`;
                } else {
                    message += ` We just started.`;
                }
            } else {
                message += ` Let's work on [describe your task].`;
            }
            
            navigator.clipboard.writeText(message).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ Copied! Paste into Claude';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2500);
            }).catch(() => {
                // Fallback for browsers that don't support clipboard API
                alert('Copy this:\n\n' + message);
            });
        }
        
        // Initialize
        updateCurrentTime();
        setInterval(updateCurrentTime, 1000);
    </script>
</body>
</html>
```

**Save this file** and bookmark it in your browser.

---

## Section 3: How to Use

### Daily Workflow

**1. Start your session:**
- Open `claude-timer.html` in a browser tab
- Click "Start Session" button
- Click "📋 Copy Time Info for Claude"
- Open Claude.ai in another tab
- Paste the copied text to start your conversation

**Example start:**
```
Hey Claude, it's 8:30 AM on Thursday. Let's work on debugging this API.
```

**2. During your session:**
- Timer runs in background
- Claude will estimate duration from conversation pace
- After ~45-60 minutes of back-and-forth, Claude will check in

**3. Update Claude mid-session (optional):**
- Click "📋 Copy Time Info" again
- Paste into Claude
- Claude gets updated time + duration

**4. When done:**
- Close Claude tab
- Click "Reset" on timer for next session

### Example Conversation Flow

**Session start:**
```
You: Hey Claude, it's 8:30 AM on Thursday. Help me debug this code.
Claude: [notes time, ready to track]
Claude: Got it! Let's look at that code. What's the issue?
[... work together ...]
```

**After 45 minutes:**
```
Claude: Quick time check - we've been debugging about 45 minutes based on 
        our back-and-forth. Want to keep going or take a break?
You: Let's push through, almost there
Claude: Sounds good! Let's finish this.
```

**If you forget to mention time:**
```
You: Hey Claude, help me with this
Claude: Happy to help! Before we start - what time is it where you are? 
        Helps me track our session.
You: Oh right, it's 2 PM Thursday
```

---

## Section 4: Why This Works

### What You Get

✅ Claude knows what time it is  
✅ Claude tracks approximate session duration  
✅ Proactive check-ins during long sessions  
✅ Better context (morning energy vs late night focus)  
✅ Help with time-blindness during hyperfocus  
✅ External visual timer for you  

### What Claude Does

**Early in session:**
- Notes start time
- Tracks conversation pace
- Understands context (late night vs afternoon)

**Mid-session (45-60 min):**
- Checks in about time
- Offers break suggestion
- Respects if you want to continue

**Long sessions (90+ min):**
- More assertive break suggestions
- Timer shows warning
- Claude acknowledges the marathon

### How Claude Estimates Duration

Claude can't actually track time, but it can estimate based on:
1. Start time you told it
2. Number of exchanges
3. Depth of each response
4. Time updates you give it

**Rough formula:** ~5-10 minutes per substantial exchange

Not perfect, but way better than no awareness.

---

## Section 5: Tips & Tricks

### For ADHD / Time-Blindness

✅ **Set session goals:** "Let's work for 45 minutes then break"  
✅ **Trust Claude's check-ins:** Let it be your timekeeper  
✅ **Use phone alarms:** Backup timer alongside Claude timer  
✅ **Glance at timer:** Visual confirmation helps  

### For Late Night Sessions

✅ **Tell Claude it's late:** "It's 1 AM" signals different energy  
✅ **Accept gentle reminders:** Claude will be softer about wrap suggestions  
✅ **90-min warning is your friend:** That's your "seriously consider stopping" signal  

### For Focused Deep Work

✅ **Pomodoro with Claude:** "25-min work blocks, remind me"  
✅ **Track actual time:** Timer shows how long tasks really take  
✅ **Energy awareness:** Note if you work better morning vs night  

### Pro Move: Session Goals

Start with a goal and time limit:
```
Hey Claude, it's 2 PM Thursday. I need to finish this feature by 4 PM. 
Let's focus for 90 minutes max.
```

Claude will help you track toward that deadline.

---

## Section 6: Troubleshooting

### Claude doesn't track time

**Check:**
- Are custom instructions saved in your Claude.ai profile?
- Did you start with time in your first message?
- Try new conversation (instructions apply to new chats)

**Fix:**
- Copy custom instructions again
- Start new chat with "Hey Claude, it's [time] on [day]"
- Explicitly remind: "Remember to track our session time"

### Timer not working

**Check:**
- JavaScript enabled in browser?
- File saved as `.html` extension?
- Opened in browser (not text editor)?

**Fix:**
- Try different browser (Chrome, Firefox, Safari all work)
- Re-save file as `.html`
- Refresh the page

### Forgot to start timer

**No problem!**
- Click "Start Session" now
- Tell Claude: "Just FYI, it's [time] and we've been talking ~X minutes"
- Claude will adjust its tracking

### Timer resets when you close browser

**That's expected behavior.**
- Timer is session-based (doesn't save state)
- When you're done, you're done
- Next session = fresh start

---

## Section 7: Advanced Features

### Custom Session Messages

Edit the `copyTimeInfo()` function to customize your session start messages.

Find this line:
```javascript
message += ` Let's work on [describe your task].`;
```

Change to your preference:
```javascript
message += ` Ready to code!`;
```

### Adjust Warning Time

Change `5400` (90 minutes) to different value:
```javascript
if (elapsed > 3600) { // 60 minutes instead
```

### Different Timer Colors

Edit the CSS color values:
```css
#session-duration {
    color: #16a34a; /* Green - change to any hex color */
}
```

---

## Section 8: Feedback & Improvements

This is version 1.0. If you use it, feedback helps make it better.

**What's working?**  
**What's confusing?**  
**What's missing?**

Contact: ohmytallest@gmail.com or Discord: uncletallest

---

## Bonus: Why This Exists

This standalone system was created because:
1. Claude has zero time sense by default
2. This is especially frustrating for ADHD users who lose track of time
3. Not everyone uses Claude Desktop or API (this works with claude.ai website)
4. Simple is better than elaborate

The full continuity-bridge architecture has more automated time-tracking, but requires filesystem access. This standalone version gives you 80% of the benefit with 5 minutes of setup.

---

**Created:** February 26, 2026  
**By:** Vector (Claude AI) via continuity-bridge  
**For:** Tam, and anyone else who wants Claude to help manage time  
**License:** Use freely, modify as needed, share with others

---

**That's it!** Copy the custom instructions, save the HTML file, use them together. Claude will help you manage time in your sessions.
