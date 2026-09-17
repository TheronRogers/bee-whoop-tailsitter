# Bee Core v0.1 — Design brief

## Purpose

First custom PCB bring-up board for Bee flight hardware: prove RP2350A boot,
USB, SWD, then graft IMU → servo → single-channel brushless ESC on one board
suitable for JLCPCB PCBA (qty 5). Base = Raspberry Pi **RP2350A Minimal**
reference (`RPI-RP2350A-MINIMAL_R4-S1`), not a greenfield MCU island.

## Block diagram (text)

```
                    USB-C (VBUS)
                         |
                    +----+----+
                    |  3V3 LDO/buck |---- 3V3 rail ----+
                    +---------+-----+                  |
                         |                             |
                         v                             v
              +----------+-----------+        +--------+--------+
   BOOTSEL/   |   RP2350A (QFN-60)   |  SPI   | BMI270 /        |
   RUN btns --|   + W25Q32 QSPI      |------->| ICM-42688 IMU   |
   SWD hdr ---|                      |        +-----------------+
   Status LED-|                      |
              |  UART / I2C / SPI CS |-------> COMPANION 6-pin
              |  DShot GPIO          |-------> EFM8BB21 ESC
              |  Servo PWM GPIO      |-------> Servo header
              +----------+-----------+
                         |
                    USB DP/DM

   VBAT pad (optional, later) ----+
                                  |
                         +--------v--------+
                         | EFM8BB21 + 3φ   |
                         | FET bridge ESC  |---- Motor A/B/C
                         | (Bluejay)       |
                         +--------+--------+
                                  |
                               bulk C on VBAT

                         +--------+--------+
                         | small 5V BEC    |---- SERVO_5V
                         | (from VBAT/USB) |
                         +-----------------+
```

## Proof-order (bring-up sequence)

1. **USB** — enumerate / UF2 or picotool; confirm 3V3 rail and crystal.
2. **Blink / SWD** — status LED GPIO + SWD attach (BOOTSEL + RUN verified).
3. **IMU** — SPI read WHO_AM_I / sample rate; check noise vs motor ground.
4. **Servo** — PWM out + 5V rail load (no motor yet).
5. **DShot motor** — Bluejay ESC: DShot300/600 arm → spin → telemetry if wired.

Do not parallel-power VBAT motor path until steps 1–3 are green.

## Fab posture

| Item | Choice |
|------|--------|
| Fab / PCBA | JLCPCB, qty 5 |
| Layers | Prefer **4-layer** (ESC + IMU on same board → ground plane isolation) |
| Assembly | Prefer LCSC Basic where possible; Extended OK for MCU/IMU/USB-C |
| Base design | Official Minimal + LCSC mapping from funvill fork as part guide |
| Form factor | Bring-up friendly (not whoop 25.5 mm yet); leave copper pour room for ESC |

## In scope (v0.1)

- RP2350A QFN-60 (JLCPCB C42411118)
- External QSPI flash (W25Q32 class)
- USB-C, SWD header, BOOTSEL + RUN
- 3.3V from USB; optional battery pad footprint (DNP OK)
- IMU: BMI270 **or** ICM-42688 on SPI
- 1× integrated brushless ESC: EFM8BB21 + FET bridge (whoop-style single channel)
- 1× servo PWM + 5V servo rail (small BEC)
- Status LED, test points
- Unpopulated 6-pin **COMPANION** header: 3V3, GND, UART TX/RX, plus I2C or SPI CS

## Out of scope (v0.1)

- Multi-motor ESC / 4-in-1
- ExpressLRS / radio
- Analog/digital VTX
- Battery charger / fuel gauge (pad only)
- Full Betaflight target / AIO FC mechanical (25.5 mm)
- Gate-driver multi-S power stages unless explicitly promoted later
- Invented EFM8 pinouts without a chosen Bluejay layout letter

## Design anchors

- Official schematic/PCB: `vendor/rp2350-minimal/` and working `kicad/`
- LCSC part cheat-sheet: `vendor/RP2350A_Minimal_USBC/README.md`
- ESC topology: `ESC-NOTES.md`


## Implementation status (2026-09-15 MT)

- Working KiCad tree: `bee-core-v01/` (Minimal core + hierarchical IMU/SERVO/ESC/COMPANION).
- Bluejay **Layout A** locked as schematic default (EFM8 port roles cited from `A.inc`).
- PCB still upstream KiCad 10 format — fab/DRC pending KiCad 10 or format port.
- ESC discrete FET stage and servo BEC still GUI/finish work; see `NEXT-STEPS.md` and `bee-core-v01/SCHEMATIC-NOTES.md`.
