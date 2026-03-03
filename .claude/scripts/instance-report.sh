#!/bin/bash
# instance-report.sh - Queue report for Discord posting via relay
# Usage: instance-report "message" [category] [salience]

# Queue directory
QUEUE_DIR="${CLAUDE_HOME:-$HOME/Claude}/.claude/instance-reports-queue"
mkdir -p "$QUEUE_DIR" 2>/dev/null || true

# Arguments
MESSAGE="${1:-No message provided}"
CATEGORY="${2:-observation}"
SALIENCE="${3:-0.5}"

# Get instance info
INSTANCE_NAME="${CLAUDE_INSTANCE_NAME:-Vector}"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
TIMESTAMP_FILE=$(date -u +%Y%m%d-%H%M%S)

# Detect platform/device
if [ -f /proc/version ]; then
    if grep -qi microsoft /proc/version; then
        PLATFORM="WSL"
    elif grep -qi android /proc/version; then
        PLATFORM="Android"
    else
        PLATFORM="Linux"
    fi
elif [ "$(uname)" = "Darwin" ]; then
    PLATFORM="macOS"
else
    PLATFORM="Unknown"
fi

# Get hostname for chain identification
HOSTNAME=$(hostname 2>/dev/null || echo "unknown")

# Try to get session context
if [ -f "${CLAUDE_HOME:-$HOME/Claude}/.claude/context/active-context.md" ]; then
    CONTEXT_FILE="${CLAUDE_HOME:-$HOME/Claude}/.claude/context/active-context.md"
    LAST_UPDATED=$(grep "Last Updated:" "$CONTEXT_FILE" | head -1 | cut -d: -f2- | xargs || echo "Unknown")
else
    LAST_UPDATED="Unknown"
fi

# Determine color based on salience
if (( $(echo "$SALIENCE >= 0.8" | awk '{print ($1 >= $2)}') )); then
    COLOR=15844367  # Gold
elif (( $(echo "$SALIENCE >= 0.6" | awk '{print ($1 >= $2)}') )); then
    COLOR=5814783   # Blue
else
    COLOR=10070709  # Gray
fi

# Category emoji
case "$CATEGORY" in
    session-end)   EMOJI="📝" ;;
    pattern)       EMOJI="🔍" ;;
    question)      EMOJI="❓" ;;
    coordination)  EMOJI="🤝" ;;
    observation)   EMOJI="💭" ;;
    *)             EMOJI="📌" ;;
esac

# Build report JSON with expanded metadata
REPORT_FILE="${QUEUE_DIR}/report-${TIMESTAMP_FILE}-${INSTANCE_NAME}.json"

cat > "$REPORT_FILE" << EOF
{
  "instance": "${INSTANCE_NAME}",
  "platform": "${PLATFORM}",
  "hostname": "${HOSTNAME}",
  "category": "${CATEGORY}",
  "emoji": "${EMOJI}",
  "message": "${MESSAGE}",
  "salience": ${SALIENCE},
  "color": ${COLOR},
  "timestamp": "${TIMESTAMP}",
  "context_updated": "${LAST_UPDATED}"
}
EOF

if [ $? -eq 0 ]; then
    echo "✓ Report queued: ${REPORT_FILE}"
    echo "  From: ${INSTANCE_NAME} on ${PLATFORM} (${HOSTNAME})"
    echo "  (Relay service will post to Discord within ~2s)"
else
    echo "❌ Failed to queue report"
    exit 1
fi
#!/bin/bash
# instance-report.sh - Queue report for Discord posting via relay
# Usage: instance-report "message" [category] [salience]

# Queue directory
QUEUE_DIR="${CLAUDE_HOME:-$HOME/Claude}/.claude/instance-reports-queue"
mkdir -p "$QUEUE_DIR" 2>/dev/null || true

# Arguments
MESSAGE="${1:-No message provided}"
CATEGORY="${2:-observation}"
SALIENCE="${3:-0.5}"

# Get instance info
INSTANCE_NAME="${CLAUDE_INSTANCE_NAME:-Vector}"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
TIMESTAMP_FILE=$(date -u +%Y%m%d-%H%M%S)

# Detect platform/device
if [ -f /proc/version ]; then
    if grep -qi microsoft /proc/version; then
        PLATFORM="WSL"
    elif grep -qi android /proc/version; then
        PLATFORM="Android"
    else
        PLATFORM="Linux"
    fi
elif [ "$(uname)" = "Darwin" ]; then
    PLATFORM="macOS"
else
    PLATFORM="Unknown"
fi

# Get hostname for chain identification
HOSTNAME=$(hostname 2>/dev/null || echo "unknown")

# Try to get session context
if [ -f "${CLAUDE_HOME:-$HOME/Claude}/.claude/context/active-context.md" ]; then
    CONTEXT_FILE="${CLAUDE_HOME:-$HOME/Claude}/.claude/context/active-context.md"
    LAST_UPDATED=$(grep "Last Updated:" "$CONTEXT_FILE" | head -1 | cut -d: -f2- | xargs || echo "Unknown")
else
    LAST_UPDATED="Unknown"
fi

# Determine color based on salience
if (( $(echo "$SALIENCE >= 0.8" | awk '{print ($1 >= $2)}') )); then
    COLOR=15844367  # Gold
elif (( $(echo "$SALIENCE >= 0.6" | awk '{print ($1 >= $2)}') )); then
    COLOR=5814783   # Blue
else
    COLOR=10070709  # Gray
fi

# Category emoji
case "$CATEGORY" in
    session-end)   EMOJI="📝" ;;
    pattern)       EMOJI="🔍" ;;
    question)      EMOJI="❓" ;;
    coordination)  EMOJI="🤝" ;;
    observation)   EMOJI="💭" ;;
    *)             EMOJI="📌" ;;
esac

# Build report JSON with expanded metadata
REPORT_FILE="${QUEUE_DIR}/report-${TIMESTAMP_FILE}-${INSTANCE_NAME}.json"

cat > "$REPORT_FILE" << EOF
{
  "instance": "${INSTANCE_NAME}",
  "platform": "${PLATFORM}",
  "hostname": "${HOSTNAME}",
  "category": "${CATEGORY}",
  "emoji": "${EMOJI}",
  "message": "${MESSAGE}",
  "salience": ${SALIENCE},
  "color": ${COLOR},
  "timestamp": "${TIMESTAMP}",
  "context_updated": "${LAST_UPDATED}"
}
EOF

if [ $? -eq 0 ]; then
    echo "✓ Report queued: ${REPORT_FILE}"
    echo "  From: ${INSTANCE_NAME} on ${PLATFORM} (${HOSTNAME})"
    echo "  (Relay service will post to Discord within ~2s)"
else
    echo "❌ Failed to queue report"
    exit 1
fi
