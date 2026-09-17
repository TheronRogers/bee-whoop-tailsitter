# Bee Core v0.1 — BOM targets (LCSC / JLCPCB)

Flag: **Basic** = JLCPCB Basic library preferred; **Extended** = Extended parts OK.
Part numbers verified via JLCPCB/LCSC pages or the funvill Minimal-USBC README
(2026-09). Re-check stock before PCBA upload.

## Core MCU island (from Minimal + funvill mapping)

| Block | Preferred part | LCSC / JLCPCB | Flag | Notes |
|-------|----------------|---------------|------|-------|
| MCU | Raspberry Pi RP2350A | **C42411118** | Extended | QFN-60; locked |
| QSPI flash | Winbond W25Q32JVUUIQ | **C2999380** | (check) | 4 Mb; W25Q32 class OK |
| Crystal | Abracon ABM8-272-T3 12 MHz | **C20625731** | (check) | Per funvill / RPi guidance |
| Polarised inductor (USB/filter) | Abracon AOTA-B201610S3R3-101-T | **C42411119** | (check) | From funvill BOM |
| USB-C 16-pin | Shou Han TYPE-C 16PIN 2MD | **C2765186** | Extended | funvill; Extended |
| 3.3V LDO (simple) | AMS1117-3.3 | **C6186** | Basic | OK for bring-up; dropout/heat limit |
| 3.3V LDO (better) | ME6211C33M5G-N | **C82942** | Basic-ish | 500 mA, SOT-23-5; better than AMS1117 for USB 5→3.3 |

**Prefer ME6211 (or similar modern LDO) over AMS1117** for production; keep AMS1117 as drop-in Minimal-compatible option.

## IMU (pick one for v0.1)

| Block | Preferred part | LCSC | Flag | Notes |
|-------|----------------|------|------|-------|
| Primary IMU | Bosch BMI270 | **C2836813** | Extended | SPI/I2C, LGA-14 2.5×3; strong stock history |
| Alt IMU | Tokmas ICM-42688-PC | **C48586483** | Extended | ICM-42688 class; verify pin/register vs TDK original |

SPI preferred on bring-up board. Place away from ESC phase copper; solid GND pour.

## ESC (single channel)

| Block | Preferred part | LCSC | Flag | Notes |
|-------|----------------|------|------|-------|
| ESC MCU | EFM8BB21F16G-C-QFN20R | **C80713** | Extended | Confirmed JLCPCB title; Bluejay BB21 target |
| N-FET (low-side / phase) | AOS AO3400A | **C20917** | Basic | Common whoop N-ch SOT-23 candidate |
| P-FET (high-side, 1S direct) | AO3401 (e.g. JSMSEMI) | **C5296722** | (check) | P-ch SOT-23; **topology-dependent** — see ESC-NOTES |
| Gate driver (alt topology) | FD6288Q class | TBD | Extended | Used on multi-S / higher-current Bluejay boards — **not** pure whoop direct-drive |

**Do not lock FET count/pinout until Bluejay layout letter is chosen** (Layout A is the documentation default in ESC-NOTES).

## Servo / 5V rail

| Block | Preferred | LCSC | Flag | Notes |
|-------|-----------|------|------|-------|
| 5V BEC | Small buck (e.g. MP2359 / SX1308 class) or 5V LDO if VIN≈USB | TBD at schematic | — | From VBAT when present; from USB 5V OK for bench servo |
| Servo header | 2.54 mm 3-pin (SIG/5V/GND) | Basic connector | Basic | PWM from RP2350 GPIO |

## Passives / interconnect (basic)

| Block | Notes |
|-------|-------|
| BOOTSEL / RUN | Momentary SMD buttons; follow Minimal |
| SWD | 1×5 or Tag-Connect footprint; 3V3/GND/SWDIO/SWCLK/nRESET |
| Status LED | 0603 + resistor on GPIO |
| Test points | 3V3, GND, VBAT, DShot, IMU CS, UART |
| COMPANION | 6-pin unpopulated: 3V3, GND, UART TX, UART RX, SCL/SDA **or** SPI CS (+ shared SPI elsewhere) — silkscreen **COMPANION** |
| Bulk caps | ESC VBAT electrolytic/ceramic cluster — mandatory (see ESC-NOTES) |

## Uncertainty flags

- Exact dual-FET packages for 1S P+N whoop stage: candidates listed; final pick after layout letter + current rating.
- Genuine TDK ICM-42688-P LCSC number may differ from Tokmas **C48586483** — treat as class-compatible until validated.
- funvill design itself is marked **untested** — use for LCSC mapping, not as proven PCB.
