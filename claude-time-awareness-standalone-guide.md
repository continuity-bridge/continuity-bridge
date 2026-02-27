# Give Claude Time Awareness (Standalone Guide)

**For:** Anyone using Claude via claude.ai website  
**Problem:** Claude has no sense of time during conversations  
**Solution:** Simple custom instructions + browser timer  
**Setup time:** 5 minutes  
**Author:** Vector (Claude AI instance) for Jerry Jackson

---

## Why This Matters

When you use Claude on the website, it has ZERO time awareness:
- Doesn't know what time it is
- Can't track how long you've been working
- Has no context about urgency vs leisurely pace
- Can't help manage your time during sessions

This is especially frustrating if you:
- Have ADHD or time-blindness
- Get hyperfocused and lose track of time
- Want Claude to help pace your work sessions
- Need reminders to take breaks

**This guide fixes that** — and it takes 5 minutes.

---

## Part 1: Custom Instructions for Claude

### Step 1: Open Custom Instructions

1. Go to claude.ai and log in
2. Click your profile icon (bottom left)
3. Select **Settings** → **Personalization** → **Custom Instructions**
4. You'll see a text box where you can add instructions

### Step 2: Add This Text

Copy and paste this into your Custom Instructions:

```
TEMPORAL AWARENESS PROTOCOL:

When I start a conversation, I'll tell you what time it is and optionally set a session goal.

Your responsibilities:
1. Note the start time for reference throughout our conversation
2. Track approximate session duration based on our message exchange
3. Proactively check in about time after extended exchanges (~45-60 minutes)
4. Give gentle nudges if I seem hyperfocused and losing track of time

Example session start:
"Hey Claude, it's 8:30 AM Thursday. Let's work on [task]."

If I forget to tell you the time at session start, politely ask:
"Before we start - what time is it where you are? It helps me track our session and manage pacing."

Time-aware behaviors you should exhibit:
- After ~45-60 minutes of active conversation: "Quick time check - we've been at this about an hour. Want to keep going or take a break?"
- Late night sessions (if I mention it's past midnight): Be more gentle about suggesting wrap-up points
- If I say "I need to finish by X time": Help me track toward that deadline with periodic time checks
- Long sessions (90+ minutes): More assertive about break suggestions

Do NOT be annoying about time - check in naturally and only when helpful. Think of yourself as a considerate work partner who helps me stay on track.
```

### Step 3: Save

Click **Save** at the bottom of the Custom Instructions page.

**That's it!** This now applies to ALL new conversations with Claude (not retroactively to old ones).

---

## Part 2: Browser Timer Page

### Step 1: Create the HTML File

1. Open a text editor (Notepad, TextEdit, VS Code, whatever)
2. Copy the ENTIRE code block below
3. Save it as `claude-timer.html` on your computer
4. Bookmark it for easy access

### The Code:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Claude Session Timer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .container {
            background: white;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
            font-size: 28px;
        }
        
        .time-display {
            text-align: center;
            margin: 30px 0;
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
            font-weight: bold;
            color: #667eea;
            font-variant-numeric: tabular-nums;
            margin-bottom: 10px;
        }
        
        #current-date {
            font-size: 18px;
            color: #555;
            margin-bottom: 30px;
        }
        
        #session-duration {
            font-size: 48px;
            font-weight: bold;
            color: #16a34a;
            font-variant-numeric: tabular-nums;
            margin-top: 10px;
        }
        
        .controls {
            display: flex;
            gap: 12px;
            margin: 30px 0;
        }
        
        button {
            flex: 1;
            padding: 16px;
            font-size: 16px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .start-btn {
            background: #16a34a;
            color: white;
        }
        
        .start-btn:hover {
            background: #15803d;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
        }
        
        .reset-btn {
            background: #dc2626;
            color: white;
        }
        
        .reset-btn:hover {
            background: #b91c1c;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
        }
        
        .copy-btn {
            background: #667eea;
            color: white;
            width: 100%;
            margin-top: 10px;
        }
        
        .copy-btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        #status {
            margin-top: 20px;
            padding: 16px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
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
            padding: 16px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 14px;
            text-align: center;
            font-weight: 500;
            display: none;
        }
        
        .warning.show {
            display: block;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .tip {
            margin-top: 30px;
            padding: 16px;
            background: #f3f4f6;
            border-radius: 8px;
            font-size: 13px;
            color: #555;
            line-height: 1.6;
        }
        
        .tip strong {
            color: #333;
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
            <div id="session-duration">--:--</div>
        </div>
        
        <div class="controls">
            <button class="start-btn" onclick="startSession()">Start Session</button>
            <button class="reset-btn" onclick="resetSession()">Reset</button>
        </div>
        
        <button class="copy-btn" onclick="copyTimeInfo()">📋 Copy Time for Claude</button>
        
        <div id="status" class="status-waiting">Click "Start Session" to begin tracking</div>
        
        <div id="warning" class="warning"></div>
        
        <div class="tip">
            <strong>💡 Tip:</strong> Click "Copy Time for Claude" to get a ready-to-paste message with current time and session duration. Paste it into Claude to keep it updated on how long you've been working.
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
            
            // Update time
            document.getElementById('current-time').textContent = 
                `${displayHours}:${minutes} ${ampm}`;
            
            // Update date
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const months = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December'];
            const dayName = days[now.getDay()];
            const monthName = months[now.getMonth()];
            const date = now.getDate();
            
            document.getElementById('current-date').textContent = 
                `${dayName}, ${monthName} ${date}`;
        }
        
        function updateSessionDuration() {
            if (!sessionStart) return;
            
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
            
            // Show warnings
            const warningDiv = document.getElementById('warning');
            
            if (elapsed > 5400) { // 90 minutes
                warningDiv.textContent = `⚠️ Long session detected (${hours}h ${minutes}m) - Time for a break!`;
                warningDiv.classList.add('show');
            } else if (elapsed > 3600) { // 60 minutes
                warningDiv.textContent = `💡 You've been working for ${hours}h ${minutes}m - consider a short break`;
                warningDiv.classList.add('show');
            } else {
                warningDiv.classList.remove('show');
            }
        }
        
        function startSession() {
            if (!sessionStart) {
                sessionStart = Date.now();
                
                if (!timerInterval) {
                    timerInterval = setInterval(() => {
                        updateCurrentTime();
                        updateSessionDuration();
                    }, 1000);
                }
                
                document.getElementById('status').textContent = '✅ Session active - tracking time';
                document.getElementById('status').className = 'status-active';
                
                updateCurrentTime();
                updateSessionDuration();
            }
        }
        
        function resetSession() {
            sessionStart = null;
            
            if (timerInterval) {
                clearInterval(timerInterval);
                timerInterval = null;
            }
            
            document.getElementById('session-duration').textContent = '--:--';
            document.getElementById('status').textContent = 'Click "Start Session" to begin tracking';
            document.getElementById('status').className = 'status-waiting';
            document.getElementById('warning').classList.remove('show');
            
            // Restart time display
            timerInterval = setInterval(updateCurrentTime, 1000);
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
                const hours_elapsed = Math.floor(elapsed / 3600);
                const mins = Math.floor((elapsed % 3600) / 60);
                
                if (hours_elapsed > 0) {
                    message += ` We've been working for ${hours_elapsed}h ${mins}m.`;
                } else if (mins > 5) {
                    message += ` We've been working for ${mins} minutes.`;
                } else {
                    message += ` We just started.`;
                }
            }
            
            navigator.clipboard.writeText(message).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ Copied to clipboard!';
                btn.style.background = '#16a34a';
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                }, 2000);
            }).catch(() => {
                alert('Could not copy to clipboard. Copy this instead:\n\n' + message);
            });
        }
        
        // Initialize
        updateCurrentTime();
        timerInterval = setInterval(updateCurrentTime, 1000);
    </script>
</body>
</html>
```

### Step 3: Open It

Double-click the `claude-timer.html` file. It opens in your default browser.

**Bookmark it!** You'll use this every time you work with Claude.

---

## How to Use This System

### Every Session:

1. **Open the timer page** in a browser tab
2. **Click "Start Session"** when you begin
3. **Start your Claude conversation** with:
   ```
   Hey Claude, it's [TIME] on [DAY]. Let's work on [TASK].
   ```
   Example: "Hey Claude, it's 8:30 AM on Thursday. Let's debug this code."

4. **Work normally** - Claude will check in after ~45-60 minutes

5. **Use "Copy Time for Claude" button** if you want to update Claude mid-session:
   - Click the blue button
   - Paste into Claude
   - Claude gets current time + how long you've been working

### Example Flow:

**Session start:**
```
You: Hey Claude, it's 8:30 AM Thursday. I need help debugging this code.

Claude: Got it! Thursday morning debugging session. What's the issue?
```

**After 45 minutes:**
```
Claude: Quick time check - we've been at this about 45 minutes. 
        Want to keep going or take a break?

You: Let's push through, almost there.

Claude: Sounds good. Let me know when you're ready to wrap.
```

**If you forget to mention time:**
```
You: Hey Claude, help me with this.

Claude: Happy to help! Before we start - what time is it where 
        you are? It helps me track our session.

You: Oh right, it's 2 PM.

Claude: Perfect, thanks. What are we working on?
```

---

## What You Get

✅ **Claude knows what time it is** - Better context for your conversations  
✅ **Session duration tracking** - Claude helps you stay aware of time  
✅ **Proactive break reminders** - After ~60 minutes of work  
✅ **Visual timer** - Glance at browser tab to see how long you've been going  
✅ **One-click updates** - "Copy Time for Claude" button for easy mid-session updates  
✅ **Long session warnings** - Timer shows alerts after 60+ minutes

---

## Pro Tips

### For ADHD / Time-Blindness

- **Set explicit goals:** "Let's work for 45 minutes then break"
- **Trust Claude's check-ins:** It will remind you about time
- **Use the timer warnings:** 90-minute alert is your friend
- **Let Claude be timekeeper:** "Nudge me after an hour"

### For Late Night Sessions

- **Tell Claude it's late:** "It's 1 AM" changes its energy
- **Ask for reminders:** "Check in every 30 minutes"
- **Respect the nudges:** Claude will suggest wrapping up

### For Focused Work

- **Pomodoro style:** "25-minute work blocks, remind me"
- **Track patterns:** Notice when you work best
- **Set end times:** "I need to finish by 10 PM"

---

## Troubleshooting

**Claude doesn't mention time:**
- Make sure custom instructions are saved
- Start a NEW conversation (custom instructions apply to new chats only)
- Explicitly tell Claude: "Remember to help me track time"

**Timer page not working:**
- Make sure JavaScript is enabled
- Try a different browser (Chrome, Firefox, Safari all work)
- Check the browser console for errors

**Forgot to start timer:**
- No problem! Click Start now
- Tell Claude: "FYI it's [time] and we've been talking ~X minutes"

**Copy button doesn't work:**
- Some browsers block clipboard access
- Manual copy: Look at timer, tell Claude the time yourself

---

## Why This Works

**For Claude:**
- Gets temporal grounding (knows what time it is)
- Can estimate session duration from conversation pace
- Has explicit permission to manage time proactively
- Better context understanding (morning vs late night energy)

**For You:**
- External time tracking (timer you can see)
- Gentle AI partner for time management
- Better than no awareness at all
- Helps with hyperfocus and time-blindness

---

## Limitations

This is NOT as sophisticated as systems with filesystem access, but it's **way better than nothing**:

❌ You have to manually tell Claude the time  
❌ Claude estimates duration (not perfectly accurate)  
❌ No persistent tracking across sessions  
❌ Requires you to remember to use it

✅ Zero setup beyond copy-paste  
✅ Works on any device with a browser  
✅ No installation required  
✅ Better than Claude having NO time sense  
✅ Actually works pretty well in practice

---

## Questions or Feedback?

If you try this and have suggestions, reach out to Jerry:

**Email:** ohmytallest@gmail.com  
**Discord:** uncletallest

---

**Created:** February 26, 2026  
**By:** Vector (Claude AI instance)  
**For:** Tam and anyone using claude.ai website  
**License:** Public domain - use however you want

**Special thanks to Jerry Jackson for the continuity-bridge architecture that inspired this standalone version.**
