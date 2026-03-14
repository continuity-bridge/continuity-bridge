#!/usr/bin/env python3
# Author: Jerry Jackson (Uncle Tallest)
# Copyright: © 2026 Jerry Jackson. All rights reserved.
# Version: v0.3.0
"""
Continuity Bridge - Heartbeat Pre-Flight Check v0.2.1
Standardized for Substrate-Agnostic Temporal Continuity
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

class HeartbeatCheck:
    """Pre-flight validation with retry logic and performance monitoring."""
    
    def __init__(self, storage_path: str, max_retries: int = 3):
        self.storage_path = storage_path
        self.max_retries = max_retries
        self.backoff_delays = [0.1, 0.5, 1.0]
        
    def probe_write(self, path: str) -> Tuple[bool, float, Optional[str]]:
        if not path or not os.path.isdir(path):
            return False, 0.0, f"Path does not exist: {path}"
        
        test_file = os.path.join(path, '.heartbeat_probe')
        start_time = time.perf_counter()
        
        try:
            test_payload = {"timestamp": time.time(), "version": "0.2.0"}
            with open(test_file, 'w') as f:
                json.dump(test_payload, f)
            os.remove(test_file)
            latency_ms = (time.perf_counter() - start_time) * 1000
            return True, latency_ms, None
        except Exception as e:
            return False, 0.0, str(e)

    def check_temporal_bridge(self) -> Dict:
        """
        Calculates the delta between system time and the persistent pulse.
        """
        pulse_file = Path(self.storage_path) / ".claude/logs/bridge.pulse"
        if not pulse_file.exists():
            return {"status": "discontinuous", "delta_seconds": 0}
        
        try:
            # Read the pulse (e.g., "03/03/2026 21:31:47 CST")
            last_pulse_str = pulse_file.read_text().strip()
            
            # 1. Parse into a timezone-aware object
            # %Z handles the 'CST' or 'UTC' string added by astimezone()
            last_pulse = datetime.strptime(last_pulse_str, "%m/%d/%Y %H:%M:%S %Z").astimezone()
            
            # 2. Get current time as a timezone-aware object
            now = datetime.now().astimezone()
            
            # 3. Calculate delta (both are now aware, so no TypeError)
            delta = now - last_pulse
            delta_seconds = int(delta.total_seconds())
            
            return {
                "last_seen": last_pulse_str,
                "delta_seconds": delta_seconds,
                "status": "stable" if delta_seconds < 60 else "discontinuous"
            }
        except Exception as e:
            # If you still see 'error', this will tell us exactly why in the log
            return {"status": "error", "error": str(e), "delta_seconds": 0}
 
    def run_full_check(self) -> Dict:
        checks = {
            "timestamp": time.time(),
            "storage_check": self.check_with_retry(self.storage_path, "primary_storage"),
            "temporal_check": self.check_temporal_bridge(), # NEW: Integrated Pulse Check
            "overall_status": "FAIL",
            "recommendations": []
        }
        
        if checks["storage_check"]["success"]:
            checks["overall_status"] = "SUCCESS"
            
            # Performance Assessment
            latency = checks["storage_check"]["latency_ms"]
            if latency > 500:
                checks["recommendations"].append(f"High latency ({latency:.1f}ms) detected.")
                
            # Temporal Assessment
            tc = checks["temporal_check"]
            if tc["status"] == "discontinuous":
                checks["recommendations"].append(f"Bridge gap detected: {tc.get('delta_seconds', 0)}s since last pulse.")
        
        return checks

    def check_with_retry(self, path: str, purpose: str) -> Dict:
        for attempt in range(self.max_retries):
            success, latency, error = self.probe_write(path)
            if success:
                return {"success": True, "latency_ms": latency, "attempts": attempt + 1}
            if attempt < self.max_retries - 1:
                time.sleep(self.backoff_delays[min(attempt, len(self.backoff_delays)-1)])
        return {"success": False, "error": error, "attempts": self.max_retries}

def main():
    # ... (Keep your argparse logic) ...
    
    # Standardized Substrate-Agnostic Candidates
    candidates = [
        "/sdcard/Claude",           # Android PRIMARY
        os.path.expanduser("~/Claude"), # Linux/Mac Dynamic
        "D:\\Claude",               # Windows Dual-Boot
        os.getcwd()
    ]
    
    # ... (Keep logic to find storage_path from candidates) ...
    # Logic to find the first existing storage path
    storage_path = None
    for path in candidates:
        if os.path.exists(os.path.join(path, '.claude')):
            storage_path = path
            break
    
    if not storage_path:
        storage_path = os.getcwd()
        print(f"⚠ No standard CLAUDE_HOME found. Defaulting to: {storage_path}")

    checker = HeartbeatCheck(storage_path)
    results = checker.run_full_check()
    
    # JSON or Human output logic...
    if results['overall_status'] == 'SUCCESS':
        tc = results['temporal_check']
        print(f"✓ Temporal Bridge: {tc['status']} ({tc.get('delta_seconds', 0)}s delta)")
    
    sys.exit(0 if results['overall_status'] == 'SUCCESS' else 1)

if __name__ == '__main__':
    main()
