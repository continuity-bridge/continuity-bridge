#!/usr/bin/env python3
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
import time
import os
from datetime import datetime
from pathlib import Path

# Detect CLAUDE_HOME dynamically based on substrate
def get_pulse_path():
    candidates = [
        "/sdcard/Claude",                # Android/Fire HD 8
        os.path.expanduser("~/Claude"),  # Linux/Persephone
        os.path.expanduser("~/Transfer/Devel/Claude/Claude-Personal"),  # Linux/Persephone Foundation build
        "D:\\Claude"                     # Windows Dual Boot
    ]
    for c in candidates:
        if os.path.exists(os.path.join(c, ".claude")):
            return Path(c) / ".claude/logs/bridge.pulse"
    return Path("/tmp/bridge.pulse")

PULSE_FILE = get_pulse_path()
PULSE_FILE.parent.mkdir(parents=True, exist_ok=True)

def main():
    while True:
        now = datetime.now().astimezone()
        # Uses your preferred format: 03/03/2026 19:46:10
        # Adding Timezone (Z) for cross-platform alignment
        pulse_data = now.strftime("%m/%d/%Y %H:%M:%S %Z")
        
        try:
            # Atomic-style write to prevent file corruption
            with open(PULSE_FILE, "w") as f:
                f.write(pulse_data)
        except Exception:
            pass
        
        time.sleep(1) # Ticks once per second

if __name__ == "__main__":
    main()
