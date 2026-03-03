# LVM Expansion Quick Guide
## Problem: 3.6TB drive, only 100GB allocated to LVM

**Visual:**
```
Physical Disk (sda3): [========================================] 3.6TB
LVM Volume:           [====]                                     100GB
Used:                 [==]                                        54GB
Free to grab:              [================================]    3.5TB
```

---

## ONE-LINER FIX (If You're Feeling Lucky)

```bash
sudo pvresize /dev/sda3 && \
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv && \
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv && \
df -h /
```

**What this does:**
1. Tell LVM the partition is bigger
2. Extend logical volume to use ALL free space
3. Resize ext4 filesystem to match
4. Show you the glorious result

---

## SAFE STEP-BY-STEP (Recommended)

### Step 1: Check Current State
```bash
# See physical volumes (like zpool status)
sudo pvs

# See volume groups (like zpool list)
sudo vgs

# See logical volumes (like zfs list)
sudo lvs

# See current disk usage
df -h /
```

**Expected output:**
```
PV         VG        ...  PSize   
/dev/sda3  ubuntu-vg      100.00g  ← Should be 3.6T!

VG        #PV  ...  VSize   VFree
ubuntu-vg   1       100.00g  40.00g  ← Free space in VG

LV        VG        ...  LSize  
ubuntu-lv ubuntu-vg       100.00g
```

---

### Step 2: Extend Physical Volume

**Tell LVM to use the full partition:**
```bash
sudo pvresize /dev/sda3
```

**Verify:**
```bash
sudo pvs
# PSize should now show 3.6T
```

**ZFS equivalent:** `zpool online -e tank sda3`

---

### Step 3: Extend Logical Volume

**Use ALL available space in volume group:**
```bash
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
```

**Or specify exact size:**
```bash
sudo lvextend -L +3.4T /dev/ubuntu-vg/ubuntu-lv
```

**Verify:**
```bash
sudo lvs
# LSize should now show ~3.6T
```

**ZFS equivalent:** `zfs set quota=none tank/dataset`

---

### Step 4: Resize Filesystem

**Make ext4 filesystem use the new space:**
```bash
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
```

**This takes 10-30 seconds** for large volumes.

**ZFS equivalent:** Automatic! (ZFS does this for you)

---

### Step 5: Verify Success

```bash
df -h /
```

**Should show:**
```
Filesystem                         Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv  3.5T   54G  3.3T   2% /
```

**SUCCESS!** 🎉

---

## TROUBLESHOOTING

### Problem: "No free space in volume group"

```bash
# Check VG free space
sudo vgdisplay ubuntu-vg | grep "Free"

# If zero, check if PV expanded
sudo pvdisplay /dev/sda3 | grep "PV Size"

# If still 100GB, run pvresize again
sudo pvresize /dev/sda3
```

### Problem: "PV not using full partition"

```bash
# Check partition size
sudo fdisk -l /dev/sda3

# Manually set PV size (use value from fdisk)
sudo pvresize --setphysicalvolumesize 3.6T /dev/sda3
```

### Problem: "Filesystem didn't resize"

```bash
# Check LV size
sudo lvs

# If LV is big but filesystem isn't:
df -h /

# Run resize2fs again
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv

# Check progress (for large volumes)
sudo resize2fs -P /dev/ubuntu-vg/ubuntu-lv
```

---

## SAFETY NOTES

**These commands are NON-DESTRUCTIVE:**
- ✅ They only GROW things (never shrink)
- ✅ Your data stays intact
- ✅ No formatting, no data loss
- ✅ Can be run multiple times safely

**Worst case scenario:**
- Commands fail → Nothing changes, data safe
- Try again with different flags
- Reboot and retry

**Cannot happen:**
- ❌ Data loss (unless you type wrong device!)
- ❌ Partition corruption
- ❌ System break

---

## AFTER EXPANSION - GET YOUR MODELS!

```bash
# Now you have room for ALL the models!

# The big boy (40GB)
ollama pull llama3.3:70b

# Coding specialist (7.4GB)
ollama pull qwen2.5-coder:7b

# Daily driver (4.7GB)
ollama pull llama3.1:8b

# Pattern recognition beast (8.5GB)
ollama pull qwen2.5:14b

# Novel thinking (9.3GB)
ollama pull deepseek-v3:16b

# Still have 3.2TB free! 🎉
```

---

## ZFS USER NOTES

**What you're used to in ZFS:**
```bash
# ZFS would be:
zpool online -e tank sda3     # Expand pool
zfs set quota=none tank/data  # Remove quota
# Done! Filesystem auto-resizes
```

**LVM requires 3 steps:**
```bash
pvresize /dev/sda3                              # Expand pool
lvextend -l +100%FREE /dev/vg/lv                # Remove quota
resize2fs /dev/vg/lv                            # Resize fs manually
```

**Why LVM is more annoying:**
- ZFS integrates volume manager + filesystem
- LVM separates them (need manual resize2fs)
- But LVM is more widely supported on Ubuntu

**Why you miss ZFS:**
- Automatic filesystem resizing
- Snapshots that actually work
- Data integrity checking
- Better compression
- ... but this server doesn't have ZFS kernel modules 😢

---

## RECOMMENDED COMMAND SEQUENCE

```bash
# Copy-paste this whole block:

echo "=== BEFORE ==="
df -h / && sudo pvs && sudo vgs && sudo lvs

echo -e "\n=== EXPANDING ==="
sudo pvresize /dev/sda3
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv

echo -e "\n=== AFTER ==="
df -h / && sudo pvs && sudo vgs && sudo lvs

echo -e "\n=== DOWNLOAD MODELS ==="
ollama pull llama3.3:70b
```

---

**Estimated time:** 5 minutes  
**Risk level:** Very low  
**Reward:** 3.5TB of model storage! 🚀
