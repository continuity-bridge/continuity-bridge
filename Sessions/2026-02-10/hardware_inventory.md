# Hardware Inventory for LLM Setup

**Date:** February 10, 2026, 4:00 PM
**Purpose:** Planning local LLM infrastructure

---

## CURRENT DESKTOP SYSTEM (In Use)

**Motherboard:** Gigabyte Designaire Ex (TRX40 chipset)
**CPU:** AMD Threadripper 1900X (8 cores, 16 threads, Zen 1, 2017)
**RAM:** 128GB DDR4 (8 sticks, quad-channel) - Timetec (SK Hynix)
**GPU:** Asus GTX 1080 FE 8GB (1 of 2 available)
**Storage:**

- 3x ~500GB NVMe drives available
- 1x 8TB Archive HDD (current projects, Steam games)
- 5-6x 4TB Enterprise HDDs (ex-NAS)
- 1x 3TB HDD
- Several 2TB HDDs

**Requirements:**

1. Dual boot Windows 10+ and Linux
2. Gaming capability (some games barely run on GTX 1080)
3. Shared work folder accessible to both OSes
4. Syncthing for file sync with laptop
5. Playtesting various games (demanding)

---

## AVAILABLE RYZEN BUILD (Not Assembled)

**Motherboard:** Gigabyte Vision D AM4 (B550 chipset)
**CPU:** AMD Ryzen 5 5600X (6 cores, 12 threads, Zen 3, 2020)
**RAM:** 64GB DDR4-3956 (4 sticks, dual-channel) - Timetec (SK Hynix)
**Status:** Parts available, needs assembly

---

## MACPRO 3,1 (2008)

**CPU:** Dual Xeon (original, not upgraded) - likely 2x Xeon 5150 series
**RAM:** 16GB DDR2 (4 open slots, can expand to 32GB max)
**GPU Plan:** AMD R7 240 2GB or AMD RX570 8GB
**Status:** Functional but very dated (2008 hardware)

---

## WORK LAPTOP

**Model:** Lenovo Thinkpad P71
**OS:** Elementary OS 8.1
**Status:** Primary work machine

---

## AVAILABLE GPUs

### NVIDIA (CUDA-capable)

1. **Asus GTX 1080 FE** - 8GB VRAM (2 units, 1 in desktop)
   
   - Pascal architecture (2016)
   - CUDA Compute 6.1
   - Excellent for gaming AND LLM acceleration

2. **EVGA FTW3 GTX 1070 Ti** - 8GB VRAM
   
   - Pascal architecture (2017)
   - CUDA Compute 6.1
   - Great for LLM acceleration

3. **PNY XLR8 GTX 1660 Super** - 6GB VRAM
   
   - Turing architecture (2019)
   - CUDA Compute 7.5
   - Good for LLM, less VRAM

4. **Gigabyte GTX 1050 Ti** - 4GB VRAM
   
   - Pascal architecture (2016)
   - CUDA Compute 6.1
   - Limited VRAM for LLM

### AMD (ROCm-capable)

5. **AMD R7 240** - 2GB VRAM
   
   - GCN 1.0 (2013)
   - Low-end, planned for MacPro3,1
   - Not suitable for LLM acceleration

6. **AMD RX570** - 8GB VRAM
   
   - Polaris (2017)
   - ROCm support possible but tricky
   - Planned for MacPro3,1

---

## STORAGE SUMMARY

- **NVMe:** 3x ~500GB (high speed)
- **Enterprise HDD:** 5-6x 4TB (reliable, ex-NAS)
- **Archive HDD:** 1x 8TB (Steam + projects)
- **Standard HDD:** 1x 3TB, several 2TB

---

## NOTES

- User is open to reinstalling desktop if better specs result
- Gaming needs are real (one game barely runs on GTX 1080)
- Dual boot is non-negotiable for desktop
- Work laptop needs Syncthing integration
- Playtesting means variable game requirements
