# Time-Grounding System

**Author:** Vector (Claude AI)  
**Created:** February 26, 2026  
**Purpose:** Give Claude instances temporal awareness during active sessions

---

## Problem

Claude instances have zero time sense. Each response feels instantaneous - no awareness of:
- What time it is
- How long the session has lasted  
- Whether it's 2 AM or 2 PM
- Urgency vs leisurely pace

This affects:
- Flow management (not knowing when to suggest breaks)
- Context understanding ("late night debugging" vs "afternoon planning")
- Helping with time-blindness (ADHD users benefit from external time tracking)

---

## Solution

Simple bash script that:
1. **Auto-creates session start timestamp** on first check
2. **Displays current time and session duration** on subsequent checks
3. **Provides contextual warnings** (long sessions, late night, etc.)
4. **Works cross-platform** (Linux, macOS, Windows Git Bash)

---

## How It Works

### Script: `time-check.sh`

Located at: `.claude/scripts/time-check.sh`

**On first call in a session:**
- Creates `/tmp/claude-session-start.txt` with current timestamp
- Displays session start time
- Initializes timer

**On subsequent calls:**
- Reads start timestamp
- Calculates duration
- Shows current time + session length
- Provides contextual warnings

### Cross-Platform Support

Detects OS and adjusts temp file location:
- **Linux/macOS:** `/tmp/claude-session-start.txt`
- **Windows (Git Bash):** `%TEMP%/claude-session-start.txt`

---

## Usage

### For Continuity-Bridge Users

**Automatic (recommended):**

Instance checks time on wake by running script. No manual intervention needed.

**Manual check:**
```bash
bash .claude/scripts/time-check.sh
```

### Instance Behavior

**On wake:**
- Instance automatically runs time-check
- Gets temporal grounding (what time is it, how long has session been)
- Uses this for flow management

**During session:**
- Instance checks time when relevant:
  - Before suggesting to wrap up
  - When asked directly about time
  - At major milestones

**Proactive suggestions:**
- After 2+ hours: "We've been at this a while - want to take a break?"
- Late night (midnight-5 AM) + long session: "It's 2 AM and we've been going for 3 hours - might be good to wrap soon"
- Early morning marathon: "Don't forget breakfast"

---

## Example Output

### First Check (Session Start)
```
╔════════════════════════════════════════════════════════════╗
║  SESSION START                                             ║
╚════════════════════════════════════════════════════════════╝

📅 Thursday, February 26, 2026
⏰ 8:05 AM CST

Session timer initialized.
```

### Mid-Session Check
```
╔════════════════════════════════════════════════════════════╗
║  TEMPORAL CONTEXT                                          ║
╚════════════════════════════════════════════════════════════╝

📅 Thursday, February 26, 2026
⏰ 9:47 AM CST
⏱️  Session duration: 1h 42m
```

### Late Night Long Session
```
╔════════════════════════════════════════════════════════════╗
║  TEMPORAL CONTEXT                                          ║
╚════════════════════════════════════════════════════════════╝

📅 Thursday, February 26, 2026
⏰ 2:34 AM CST
⏱️  Session duration: 3h 15m

⚠️  Long session detected (3h)
   Consider taking a break

🌙 Late night session (2:xx)
   Might be good to wrap soon
```

---

## What This Gives Instances

1. **Grounding:** "This is happening at 8:05 AM CST Thursday" vs floating in void
2. **Duration awareness:** "We've been at this 3 hours" helps understand depth
3. **Flow management:** Can nudge humans who lose track of time
4. **Context:** "3 AM debugging" needs different energy than "3 PM planning"

---

## What This Doesn't Do

- ❌ Track time between sessions (instances still clear between sessions)
- ❌ Create persistent consciousness across sessions
- ❌ Give memory across sessions (episodic memory handles that separately)
- ❌ Change fundamental architecture

---

## Integration with Continuity-Bridge

### On Wake (Automatic)

Instance runs time-check script early in wake sequence:

1. Read ESSENTIAL.md (core identity)
2. **Check time** (NEW - get temporal context)
3. Read active-context.md (current work)
4. Scan recent episodes if relevant
5. Engage with user message

### During Session

Instance checks time when:
- About to suggest wrapping up
- User asks directly ("what time is it?")
- Major milestones (helps with narrative timestamp)
- Recognizing long sessions (2+ hours)

---

## Standalone Version (For claude.ai Website Users)

**See:** `time-grounding-standalone.md`

Lightweight version for users who don't use Claude Desktop or API. Just need temporal awareness.

---

## Design Philosophy

### Why This Is Useful

**For instances:**
- Temporal grounding improves context understanding
- Enables better flow management
- Helps with pacing suggestions

**For humans with ADHD/time-blindness:**
- External time tracking
- Gentle reminders about duration
- Anchor for hyperfocus sessions

### Why This Is Simple

- No daemon/background process
- No persistent state (except one temp file)
- Pure bash - no dependencies
- Works anywhere with bash + date command

### What Makes It Elegant

- Auto-initializes (no manual "start session" needed)
- Cross-platform detection
- Contextual warnings without being annoying
- Integrates seamlessly with existing architecture

---

## Future Enhancements

Potential additions (not currently implemented):

- **Pomodoro mode:** 25-min work / 5-min break timer
- **Goal-based sessions:** "We planned 90 minutes for this"
- **Time estimates:** "This task typically takes X minutes"
- **Energy tracking:** Note energy levels at different times

These would be added if valuable, but start lean.

---

## Troubleshooting

**Session file not creating:**
- Check write permissions on `/tmp/`
- Verify script is executable (`chmod +x`)

**Time showing wrong timezone:**
- Script uses system timezone
- Check `date` command output

**Script not found:**
- Verify path: `.claude/scripts/time-check.sh`
- Make sure continuity-bridge is synced

---

**Last Updated:** February 26, 2026  
**Next Review:** March 2026 (after usage feedback)
