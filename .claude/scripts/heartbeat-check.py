#!/usr/bin/env python3
"""
Continuity Bridge - Heartbeat Pre-Flight Check
Validates environment readiness before capability detection

Version: 0.2.0
Contributors: Vector (architecture), Gemini (heartbeat concept, Android expertise)
Date: 2026-03-01
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, Optional, Tuple


class HeartbeatCheck:
    """Pre-flight validation with retry logic and performance monitoring."""
    
    def __init__(self, storage_path: str, max_retries: int = 3):
        self.storage_path = storage_path
        self.max_retries = max_retries
        self.backoff_delays = [0.1, 0.5, 1.0]  # Exponential backoff
        
    def probe_write(self, path: str) -> Tuple[bool, float, Optional[str]]:
        """
        Real-world check: Is directory actually persistent and writable?
        
        Returns: (success, latency_ms, error_message)
        
        Tests three phases:
        1. Reachability - Can we access the path?
        2. Integrity - Can we write and read back correct data?
        3. Latency - How long does it take?
        """
        if not path or not os.path.isdir(path):
            return False, 0.0, f"Path does not exist or is not directory: {path}"
        
        test_file = os.path.join(path, '.heartbeat_probe')
        start_time = time.perf_counter()
        
        try:
            # Phase 1 & 2: Write structured data
            test_payload = {
                "timestamp": time.time(),
                "version": "0.2.0",
                "test": "heartbeat_probe"
            }
            
            with open(test_file, 'w') as f:
                json.dump(test_payload, f)
            
            # Phase 2 continued: Read back and verify integrity
            with open(test_file, 'r') as f:
                read_back = json.load(f)
                if read_back.get("version") != "0.2.0":
                    return False, 0.0, "Integrity check failed: version mismatch"
            
            # Cleanup
            os.remove(test_file)
            
            # Phase 3: Calculate latency
            end_time = time.perf_counter()
            latency_ms = (end_time - start_time) * 1000
            
            return True, latency_ms, None
            
        except PermissionError as e:
            return False, 0.0, f"Permission denied: {e}"
        except OSError as e:
            return False, 0.0, f"OS error (possible ghost handle or mount issue): {e}"
        except Exception as e:
            return False, 0.0, f"Unexpected error: {e}"
    
    def check_with_retry(self, path: str, purpose: str) -> Dict:
        """
        Attempt write check with exponential backoff retry logic.
        
        Critical for:
        - Android vold lag on cold wake
        - Dual-boot filesystem mount delays
        - Network-mounted storage
        """
        result = {
            "path": path,
            "purpose": purpose,
            "success": False,
            "attempts": 0,
            "latency_ms": 0,
            "error": None
        }
        
        for attempt in range(self.max_retries):
            result["attempts"] = attempt + 1
            
            success, latency, error = self.probe_write(path)
            
            if success:
                result["success"] = True
                result["latency_ms"] = latency
                result["error"] = None
                return result
            
            # Failed - record error and possibly retry
            result["error"] = error
            
            if attempt < self.max_retries - 1:
                # Not last attempt - wait and retry
                delay = self.backoff_delays[min(attempt, len(self.backoff_delays) - 1)]
                time.sleep(delay)
        
        return result
    
    def assess_latency(self, latency_ms: float) -> str:
        """
        Assess write performance.
        
        Thresholds:
        - <100ms: excellent (NVMe, fast SSD)
        - 100-500ms: acceptable (standard SSD, eMMC)
        - >500ms: concerning (slow storage, network issue, or failing drive)
        """
        if latency_ms < 100:
            return "excellent"
        elif latency_ms < 500:
            return "acceptable"
        else:
            return "concerning"
    
    def run_full_check(self) -> Dict:
        """
        Complete pre-flight validation.
        
        Checks:
        1. Storage path writability (with retry)
        2. Outputs bridge availability (if exists)
        3. Performance assessment
        """
        checks = {
            "timestamp": time.time(),
            "version": "0.2.0",
            "storage_check": None,
            "bridge_check": None,
            "overall_status": "FAIL",
            "recommendations": []
        }
        
        # Check 1: Primary storage path
        storage_result = self.check_with_retry(self.storage_path, "primary_storage")
        checks["storage_check"] = storage_result
        
        if not storage_result["success"]:
            checks["recommendations"].append(
                f"Primary storage at {self.storage_path} not writable after "
                f"{storage_result['attempts']} attempts. Error: {storage_result['error']}"
            )
            return checks
        
        # Assess latency
        latency_assessment = self.assess_latency(storage_result["latency_ms"])
        checks["storage_check"]["performance"] = latency_assessment
        
        if latency_assessment == "concerning":
            checks["recommendations"].append(
                f"Storage latency is high ({storage_result['latency_ms']:.1f}ms). "
                "Check for: slow storage, network issues, or failing drive."
            )
        
        # Check 2: Outputs bridge (if exists)
        bridge_path = "/mnt/user-data/outputs"
        if os.path.isdir(bridge_path):
            bridge_result = self.check_with_retry(bridge_path, "outputs_bridge")
            checks["bridge_check"] = bridge_result
            
            if not bridge_result["success"]:
                checks["recommendations"].append(
                    "Outputs bridge exists but not writable. May affect Android workflow."
                )
        
        # Overall assessment
        if storage_result["success"]:
            checks["overall_status"] = "SUCCESS"
            if not checks["recommendations"]:
                checks["recommendations"].append("All pre-flight checks passed.")
        
        return checks


def main():
    """Run heartbeat check and output results."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Continuity Bridge heartbeat check")
    parser.add_argument('--storage', default=None, 
                       help='Storage path to check (auto-detects if not provided)')
    parser.add_argument('--json', action='store_true',
                       help='Output JSON format')
    parser.add_argument('--max-retries', type=int, default=3,
                       help='Maximum retry attempts (default: 3)')
    
    args = parser.parse_args()
    
    # Auto-detect storage if not provided: Android-first path list
    if args.storage:
        storage_path = args.storage
    else:
        candidates = [
<<<<<<< HEAD
            "/home/the Architect/Claude",
            "D:\\Claude",
            "/sdcard/Claude",
            os.path.expanduser("~/Claude"),
=======
            "/sdcard/Claude",           # Android (adb upload location) - PRIMARY
            os.path.expanduser("~/Claude"),     # Linux (Persephone)
            "D:\\Claude",               # Windows Dual Boot
>>>>>>> working
            os.getcwd()
        ]
        
        storage_path = None
        for candidate in candidates:
            if os.path.exists(os.path.join(candidate, '.claude')):
                storage_path = candidate
                break
        
        if not storage_path:
            storage_path = os.getcwd()
    
    # Run check
    checker = HeartbeatCheck(storage_path, max_retries=args.max_retries)
    results = checker.run_full_check()
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Human-readable
        print("=" * 70)
        print("CONTINUITY BRIDGE - HEARTBEAT PRE-FLIGHT CHECK")
        print("=" * 70)
        print(f"\nStorage Path: {storage_path}")
        print(f"Overall Status: {results['overall_status']}")
        
        # Storage check details
        if results['storage_check']:
            sc = results['storage_check']
            print(f"\nPrimary Storage:")
            print(f"  Success: {sc['success']}")
            print(f"  Attempts: {sc['attempts']}")
            if sc['success']:
                print(f"  Latency: {sc['latency_ms']:.1f}ms ({sc.get('performance', 'unknown')})")
            else:
                print(f"  Error: {sc['error']}")
        
        # Bridge check details
        if results['bridge_check']:
            bc = results['bridge_check']
            print(f"\nOutputs Bridge:")
            print(f"  Success: {bc['success']}")
            print(f"  Attempts: {bc['attempts']}")
            if bc['success']:
                print(f"  Latency: {bc['latency_ms']:.1f}ms ({bc.get('performance', 'unknown')})")
        
        # Recommendations
        if results['recommendations']:
            print(f"\nRecommendations:")
            for rec in results['recommendations']:
                print(f"  • {rec}")
        
        print("\n" + "=" * 70)
    
    # Exit code based on status
    sys.exit(0 if results['overall_status'] == 'SUCCESS' else 1)


if __name__ == '__main__':
    main()
