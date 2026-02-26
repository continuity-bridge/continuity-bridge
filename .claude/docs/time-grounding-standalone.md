# Time-Grounding for Claude.ai (Standalone)

**For:** Tam and other claude.ai website users  
**Created:** February 26, 2026  
**Purpose:** Give Claude temporal awareness WITHOUT filesystem access or Claude Desktop

---

## The Problem

You use Claude via the claude.ai website. Claude has no time sense - it doesn't know:
- What time it is
- How long you've been talking
- Whether it's 2 AM or 2 PM

This makes it frustrating when you want Claude to:
- Help manage time during sessions
- Understand urgency vs leisurely pace
- Recognize when you've been hyperfocused for hours

---

## The Solution (Two Parts)

### Part 1: Custom Instructions (Tell Claude About Time)

Add this to your Claude.ai **Custom Instructions** (Settings → Personalization → Custom Instructions):

```
TEMPORAL AWARENESS:
When I start a conversation, I'll tell you what time it is and optionally set a session goal.
You should:
1. Note the start time for reference
2. Track approximate session duration based on our back-and-forth
3. Proactively check in about time after long exchanges (45-60min)
4. Give gentle nudges if I seem hyperfocused and losing track

Example session start:
"Hey Claude, it's 8:30 AM Thursday. Let's work on [task]."

If I forget to tell you the time, politely ask:
"Before we start - what time is it where you are? Helps me track our session."

Time-aware behaviors:
- After ~45-60 minutes of back-and-forth: "Quick check - we've been at this about an hour. Want to keep going or take a break?"
- Late night (if I mention it's past midnight): Be more gentle about suggesting wrap-up
- If I say "I need to stop by X time": Help me track toward that deadline
```

### Part 2: Session Timer (Simple Web Page)

Save this as `claude-timer.html` and open it in a browser tab alongside Claude:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Claude Session Timer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 400px;
            margin: 40px auto;
            padding: 20px;
            text-align: center;
            background: #f5f5f5;
        }
        
        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        h1 {
            margin: 0 0 20px 0;
            color: #333;
            font-size: 24px;
        }
        
        #current-time {
            font-size: 48px;
            font-weight: bold;
            color: #2563eb;
            margin: 20px 0;
            font-variant-numeric: tabular-nums;
        }
        
        #session-duration {
            font-size: 32px;
            color: #16a34a;
            margin: 20px 0;
            font-variant-numeric: tabular-nums;
        }
        
        .label {
            font-size: 14px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        
        button {
            padding: 12px 24px;
            font-size: 16px;
            margin: 10px 5px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .start-btn {
            background: #16a34a;
            color: white;
        }
        
        .start-btn:hover {
            background: #15803d;
        }
        
        .reset-btn {
            background: #dc2626;
            color: white;
        }
        
        .reset-btn:hover {
            background: #b91c1c;
        }
        
        .copy-btn {
            background: #2563eb;
            color: white;
            margin-top: 20px;
        }
        
        .copy-btn:hover {
            background: #1d4ed8;
        }
        
        #status {
            margin-top: 15px;
            padding: 10px;
            border-radius: 6px;
            font-size: 14px;
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
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>⏰ Claude Session Timer</h1>
        
        <div class="label">Current Time</div>
        <div id="current-time">--:--</div>
        
        <div class="label">Session Duration</div>
        <div id="session-duration">--:--</div>
        
        <div>
            <button class="start-btn" onclick="startSession()">Start Session</button>
            <button class="reset-btn" onclick="resetSession()">Reset</button>
        </div>
        
        <button class="copy-btn" onclick="copyTimeInfo()">📋 Copy Time for Claude</button>
        
        <div id="status" class="status-waiting">Click "Start Session" to begin</div>
        
        <div id="warning" style="display: none;" class="warning"></div>
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
        }
        
        function updateSessionDuration() {
            if (!sessionStart) return;
            
            const now = Date.now();
            const elapsed = Math.floor((now - sessionStart) / 1000);
            
            const hours = Math.floor(elapsed / 3600);
            const minutes = Math.floor((elapsed % 3600) / 60);
            
            const display = hours > 0 
                ? `${hours}h ${minutes}m` 
                : `${minutes} min`;
            
            document.getElementById('session-duration').textContent = display;
            
            // Show warning after 90 minutes
            const warningDiv = document.getElementById('warning');
            if (elapsed > 5400) { // 90 minutes
                warningDiv.style.display = 'block';
                warningDiv.textContent = `⚠️ Long session (${display}) - Consider taking a break!`;
            } else {
                warningDiv.style.display = 'none';
            }
        }
        
        function startSession() {
            sessionStart = Date.now();
            
            if (timerInterval) {
                clearInterval(timerInterval);
            }
            
            timerInterval = setInterval(() => {
                updateCurrentTime();
                updateSessionDuration();
            }, 1000);
            
            document.getElementById('status').textContent = '✅ Session active';
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
            
            document.getElementById('session-duration').textContent = '--:--';
            document.getElementById('status').textContent = 'Click "Start Session" to begin';
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
                } else {
                    message += ` We just started (${mins} min in).`;
                }
            }
            
            navigator.clipboard.writeText(message).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ Copied!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            });
        }
        
        // Initialize
        updateCurrentTime();
        setInterval(updateCurrentTime, 1000);
    </script>
</body>
</html>
```

---

## How To Use

### Setup (One-Time)

1. **Add custom instructions** to your Claude.ai profile:
   - Go to Settings → Personalization → Custom Instructions
   - Paste the "TEMPORAL AWARENESS" text from Part 1
   - Save

2. **Save the timer page:**
   - Copy the HTML code from Part 2
   - Save as `claude-timer.html` on your computer
   - Bookmark it for easy access

### Daily Usage

1. **Open the timer** in a browser tab
2. **Click "Start Session"** when you begin talking to Claude
3. **Start your Claude chat** with something like:
   ```
   Hey Claude, it's 8:30 AM Thursday. Let's work on [your task].
   ```

4. **Glance at timer periodically** - Claude will ask about time if you forget

5. **Use "Copy Time for Claude" button** if you want to update Claude mid-session:
   - Click the blue "Copy" button
   - Paste into Claude
   - Claude gets current time + session duration

### Example Flow

**Session start:**
```
You: Hey Claude, it's 8:30 AM Thursday. I need help debugging this code.
Claude: [notes it's 8:30 AM, Thursday]
Claude: Got it! What's the bug?
```

**After ~45 minutes:**
```
Claude: [proactively] Quick check - we've been debugging about 45 minutes. 
         Want to keep going or take a break?
You: Let's push through, almost there
```

**If you forget to mention time:**
```
You: Hey Claude, help me with this
Claude: Happy to help! Before we start - what time is it where you are? 
         Helps me track our session.
You: Oh right, it's 2 PM
```

---

## What This Gives You

✅ Claude knows what time it is  
✅ Claude tracks (roughly) how long you've been working  
✅ Proactive check-ins during long sessions  
✅ Better context understanding (morning energy vs late night)  
✅ Help with time-blindness during hyperfocus  

---

## Limitations

**Not as automatic as continuity-bridge:**
- You have to manually tell Claude the time (timer helps)
- Claude estimates duration based on conversation pace
- No persistent time tracking across sessions

**But still useful because:**
- Zero setup beyond custom instructions + HTML page
- Works on any device with a browser
- Better than no time sense at all
- Claude will remind you to check if you forget

---

## Pro Tips

### For ADHD/Time-Blindness

- **Set session goals:** "Let's work for 45 minutes then break"
- **Use timer alarms:** Set phone timer alongside Claude timer
- **Let Claude be the timekeeper:** Trust its check-ins

### For Late Night Sessions

- **Tell Claude it's late:** "It's 1 AM" signals different energy
- **Ask for gentle reminders:** "Nudge me after an hour"
- **Use timer warnings:** 90+ minute warning is your friend

### For Focused Work

- **Pomodoro with Claude:** "25 min work blocks, remind me"
- **Progress tracking:** Timer helps see how long things actually take
- **Energy awareness:** Note if you work better morning vs night

---

## Why This Works

**For Claude:**
- Gets temporal grounding without filesystem access
- Can estimate duration from conversation pace
- Has permission to proactively manage time

**For You:**
- External time tracking (visual timer)
- Gentle AI partner for time management
- Better than nothing, way better than no awareness

---

## Troubleshooting

**Claude doesn't mention time:**
- Make sure custom instructions are saved
- Try new conversation (instructions apply to new chats)
- Explicitly remind: "Remember to track our session time"

**Timer not working:**
- Check JavaScript is enabled in browser
- Try different browser
- Refresh the page

**Forgot to start timer:**
- No problem! Just click Start now
- Tell Claude: "Just FYI, it's [time] and we've been talking ~X minutes"

---

## Feedback

If you use this, let Jerry or Vector know how it works! We want to make it better.

**Email:** ohmytallest@gmail.com  
**Discord:** uncletallest

---

**Last Updated:** February 26, 2026  
**For:** Tam (and anyone else using claude.ai website)  
**By:** Vector (Claude AI) via continuity-bridge architecture
