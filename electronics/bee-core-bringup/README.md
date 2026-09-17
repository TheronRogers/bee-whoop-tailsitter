# Bee Core — RP2350 bring-up board (v0.1)

Hardware foundation for grafting flight peripherals onto Raspberry Pi’s official
**RP2350A Minimal** KiCad design. Target: JLCPCB PCBA, qty 5, prefer 4-layer.

## Layout

| Path | Contents |
|------|----------|
| `DESIGN.md` | Purpose, block diagram, proof-order, fab posture, scope |
| `BOM-TARGETS.md` | Functional blocks + preferred LCSC candidates |
| `ESC-NOTES.md` | Single-channel whoop ESC topology (cited sources) |
| `NEXT-STEPS.md` | Immediate schematic graft plan |
| `vendor/rp2350-minimal/` | Untouched RPi Minimal KiCad zip extract |
| `vendor/RP2350A_Minimal_USBC/` | JLCPCB/LCSC-mapped fork (funvill) — reference only |
| `kicad/` | Pristine Minimal copy (reference; leave intact) |
| `bee-core-v01/` | **Working KiCad project** + graft sheets; see `SCHEMATIC-NOTES.md` |

## Sources

- Official Minimal: https://datasheets.raspberrypi.com/rp2350/Minimal-KiCAD.zip  
  → `RPI-RP2350A-MINIMAL_R4-S1` (RP2350A QFN-60)
- JLCPCB-mapped fork: https://github.com/funvill/RP2350A_Minimal_USBC
- Hardware design guide: https://datasheets.raspberrypi.com/rp2350/hardware-design-with-rp2350.pdf

## Tooling

| Tool | Version / method |
|------|------------------|
| KiCad | **9.0.2** (`sudo apt-get install -y kicad`, Debian package `9.0.2+dfsg-1`) |
| CLI | `kicad-cli` 9.0.2 (`kicad-cli version`) |
| GUI | `/usr/bin/kicad` (same package; needs display) |

Upstream Minimal sources are **KiCad 10**. Working schematic in `bee-core-v01/` was
downgraded to load in 9.0.2; PCB remains KiCad 10 until a newer KiCad is available.

## Locked v0.1 scope (summary)

RP2350A + QSPI flash + USB-C + SWD + BOOTSEL/RUN + 3V3 from USB; BMI270 or
ICM-42688 SPI IMU; 1× EFM8BB21 Bluejay ESC channel; 1× servo PWM + 5V BEC;
status LED; COMPANION 6-pin header (unpopulated).
