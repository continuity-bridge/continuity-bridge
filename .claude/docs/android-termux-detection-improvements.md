# Android/Termux Detection Improvements

**Date:** March 2, 2026 (8:30 AM)  
**Tested On:** Fire HD 8 (Fire OS 6 / Android 7)  
**Status:** Detection improved based on real-world testing

---

## Problem

Original detection script failed to properly identify Android/Termux environment:
- Platform detected as "unknown" instead of "android"
- CLAUDE_HOME not found (looking for wrong paths)
- Workflow defaulted to TEXT_ONLY despite git being available
- Termux abstraction layer caused confusion

---

## Solution

### 1. Hard-Code Android CLAUDE_HOME Path

**Key insight:** `/sdcard/Claude` is where adb uploads go and is writeable.

**Changed:**
```python
def detect_claude_home() -> str:
    candidates = [
        "/sdcard/Claude",           # Android - PRIMARY (adb upload location)
        "/sdcard/Platform_Home",    # Android - alternate naming
        # ... rest of platforms
    ]
```

**Why:** Android devices receive files via adb to /sdcard/. This is the standard, writeable location.

---

### 2. Multi-Indicator Android Detection

**Problem:** Termux abstraction layer makes single-check detection unreliable.

**Solution:** Check multiple Android indicators:

```python
android_indicators = [
    os.path.exists('/system/bin/app_process'),      # Android system binary
    os.path.exists('/sdcard'),                      # External storage
    os.path.exists('/data/data/com.termux'),        # Termux app
    'TERMUX_VERSION' in os.environ,                 # Termux env var
    'ANDROID_ROOT' in os.environ,                   # Android env var
    'com.termux' in os.environ.get('PREFIX', '')    # Termux prefix
]

if any(android_indicators):
    return 'android'
```

**Why:** Any ONE of these indicates Android. Multiple checks = reliable detection.

---

### 3. Recognize Android Git Workflow

**Problem:** Even with git available, defaulted to TEXT_ONLY workflow.

**Solution:** Special case for Android with git:

```python
if is_android and git_info['available']:
    # Check for work directory (cloned repo pattern)
    work_dirs = [
        os.path.join(claude_home, 'work'),
        '/sdcard/Claude',
        '/data/data/com.termux/files/home/work'
    ]
    has_work_dir = any(os.path.isdir(d) for d in work_dirs)
    
    if has_work_dir or has_bridge:
        manifest["workflow"] = "CONTAINER_GIT_WITH_BRIDGE"
```

**Why:** Android + git + work directory = full git workflow capability.

---

### 4. Termux Bash Context Detection

**Added:**
```python
def detect_bash_context() -> str:
    # Termux detection
    if '/data/data/com.termux' in pwd or 'TERMUX_VERSION' in os.environ:
        return 'termux_android'
```

**Why:** Distinguishes Termux bash from container bash from local bash.

---

### 5. Android-Specific Manifest Info

**Added section:**
```json
"android_environment": {
    "termux_detected": true,
    "termux_version": "0.118.0",
    "sdcard_accessible": true,
    "adb_upload_path": "/sdcard/Claude",
    "recommended_clone_path": "/sdcard/Claude",
    "notes": [
        "Termux abstraction layer may affect some detections",
        "/sdcard/ is writeable and where adb uploads go",
        "Work in /sdcard/Claude for best compatibility",
        "Use pkg install git python for dependencies"
    ]
}
```

**Why:** Provides Android-specific guidance and troubleshooting info.

---

## Testing Results (Fire HD 8)

### Before Changes
```
Platform: unknown ❌
CLAUDE_HOME: NOT FOUND ❌
Workflow: text_only ❌
```

### After Changes (Expected)
```
Platform: android ✅
CLAUDE_HOME: /sdcard/Claude ✅
Workflow: CONTAINER_GIT_WITH_BRIDGE ✅
Bash Context: termux_android ✅
```

---

## Android/Termux Setup Instructions

### Initial Setup

1. **Install Termux from F-Droid** (NOT Google Play - outdated version)

2. **Install dependencies:**
   ```bash
   pkg update
   pkg install git python
   ```

3. **Grant storage permissions:**
   ```bash
   termux-setup-storage
   ```

4. **Clone private repo:**
   ```bash
   cd /sdcard
   git clone git@github.com:username/continuity-bridge_username-anchor.git Claude
   cd Claude
   git checkout working
   ```

### Daily Workflow

```bash
# Start work
cd /sdcard/Claude
git pull private working

# Work happens (AI sessions, etc.)
# Files get modified

# End work
git add -A
git commit -m "Session work from Fire Tablet"
git push private working
```

### Why /sdcard/Claude?

1. **adb compatibility:** Files uploaded via adb go to /sdcard/
2. **Writeable:** /sdcard/ is always writeable on Android
3. **Accessible:** Both Termux and other apps can access /sdcard/
4. **Standard:** Matches expected Android file paths

---

## Known Termux Limitations

### Abstraction Layer Issues

**Problem:** Termux provides Linux-like environment but with Android constraints.

**Symptoms:**
- Some paths return "unknown" even when accessible
- File permissions may not match standard Linux
- Some system calls behave differently

**Workarounds:**
- Use multiple detection indicators (not just one check)
- Hard-code known working paths (/sdcard/Claude)
- Test on actual device, not just emulator

### Package Management

**Termux uses `pkg` not `apt`:**
```bash
pkg install git python  # NOT apt install
```

**Detection handles this:**
```python
if is_android:
    package_info = {
        "manager": "pkg",
        "install_cmd": "pkg install -y"
    }
```

---

## Fire OS 6 Specifics

**Based on:** Android 7 (Nougat)

**Quirks:**
- Older Android version (scoped storage less restrictive)
- Amazon-specific modifications
- May behave differently than stock Android

**Works well for testing because:**
- Less restrictive than Android 10+ scoped storage
- /sdcard/ fully accessible
- Good baseline for Android support

---

## Future Improvements

### To Investigate

1. **Android 10+ scoped storage**
   - May need different paths
   - May need URI permissions
   - Test on newer Android versions

2. **Termux version detection**
   - Different Termux versions have different capabilities
   - May need version-specific workarounds

3. **Alternative Android terminals**
   - Test with other terminal emulators
   - Ensure detection works beyond just Termux

### To Document

1. **Git SSH key setup on Android**
   - How to generate keys in Termux
   - How to add to GitHub
   - Troubleshooting SSH issues

2. **Editor setup**
   - nano, vim, or micro in Termux
   - Editing anchors.json on Android
   - File permission issues

3. **Cross-device sync patterns**
   - Desktop → Android workflow
   - Android → Desktop workflow
   - Handling merge conflicts

---

## Validation Checklist

**On Android/Termux, detection should report:**
- ✅ Platform: android
- ✅ CLAUDE_HOME: /sdcard/Claude (or /sdcard/Platform_Home)
- ✅ Bash context: termux_android
- ✅ Git: available
- ✅ Workflow: CONTAINER_GIT_WITH_BRIDGE (if git + work dir)
- ✅ Android environment section populated

**If any fail:**
- Check Termux version (0.118+ recommended)
- Verify storage permissions granted
- Ensure /sdcard/Claude exists with .claude/ subdirectory
- Check git installation: `which git`

---

## Credits

**Testing:** The Architect (Fire HD 8, real-world validation)  
**Detection Logic:** Vector (multi-indicator approach)  
**Insight:** "/sdcard/Claude is where adb uploads go - hard-code it"

**Cross-substrate collaboration:** Desktop testing → Android validation → improved detection for everyone

---

**Status:** Improved detection ready for testing on Fire HD 8.

**Next:** Run updated detect-capabilities.py on Fire Tablet, verify correct output.
