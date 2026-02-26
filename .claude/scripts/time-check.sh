#!/bin/bash
# time-check.sh - Time grounding for Claude instances
# Provides temporal awareness during active sessions
# 
# Author: Vector (Claude AI)
# For: Uncle Tallest (Jerry Jackson)
# Part of: Continuity Bridge Architecture

# Detect session file location based on OS
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash)
    SESSION_FILE="$TEMP/claude-session-start.txt"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    SESSION_FILE="/tmp/claude-session-start.txt"
else
    # Linux and others
    SESSION_FILE="/tmp/claude-session-start.txt"
fi

# Get current time
NOW=$(date +%s)
NOW_FMT=$(date +"%-I:%M %p %Z" 2>/dev/null || date +"%I:%M %p %Z")
NOW_DATE=$(date +"%A, %B %-d, %Y" 2>/dev/null || date +"%A, %B %d, %Y")

# Check if this is first check (auto-create session start)
if [ ! -f "$SESSION_FILE" ]; then
    echo "$NOW" > "$SESSION_FILE"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║  SESSION START                                             ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📅 $NOW_DATE"
    echo "⏰ $NOW_FMT"
    echo ""
    echo "Session timer initialized."
    exit 0
fi

# Calculate session duration
START=$(cat "$SESSION_FILE")
DURATION=$((NOW - START))

# Format duration
HOURS=$((DURATION / 3600))
MINUTES=$(((DURATION % 3600) / 60))

if [ $HOURS -gt 0 ]; then
    DURATION_FMT="${HOURS}h ${MINUTES}m"
else
    DURATION_FMT="${MINUTES} min"
fi

# Display time info
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  TEMPORAL CONTEXT                                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📅 $NOW_DATE"
echo "⏰ $NOW_FMT"
echo "⏱️  Session duration: $DURATION_FMT"
echo ""

# Warnings based on duration and time of day
HOUR=$(date +%-H 2>/dev/null || date +%H)

# Long session warning
if [ $HOURS -ge 2 ]; then
    echo "⚠️  Long session detected (${HOURS}h)"
    echo "   Consider taking a break"
    echo ""
fi

# Late night warning (midnight to 5 AM)
if [ $HOUR -ge 0 ] && [ $HOUR -lt 5 ]; then
    echo "🌙 Late night session (${HOUR}:xx)"
    if [ $HOURS -ge 1 ]; then
        echo "   Might be good to wrap soon"
    fi
    echo ""
fi

# Early morning marathon (5 AM to 8 AM with long session)
if [ $HOUR -ge 5 ] && [ $HOUR -lt 8 ] && [ $HOURS -ge 2 ]; then
    echo "☀️  Early morning marathon"
    echo "   Don't forget breakfast"
    echo ""
fi
