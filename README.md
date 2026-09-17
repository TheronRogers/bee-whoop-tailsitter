# Bee Whoop Tailsitter

Affordable dual-motor, dual-elevon tailsitter platform (Bee). Prototype path: learn custom PCB + printable airframe, then flyable AIO.

## Layout

- `cad/` — Rad CAD / VibeCAD airframe (BeeWhoopTailsitter)
- `electronics/` — Bee Core bring-up board (RP2350 KiCad design)

## Airframe (v0)

| Spec | Value |
|------|--------|
| Span | 120 mm |
| Mean chord | 48 mm (root 52 / tip 44) |
| Area | ~5760 mm² |
| Motors | Y ±30 mm, 40 mm prop discs |
| Elevons | 15 mm chord, 8 mm root gap |
| AIO tray | 32×36×8 mm @ ~33% MAC |
| Battery cue | 1S near LE |
| Servos | 2× micro ~9×12×22 |
| Materials | PLA + Air/LW-PLA; PETG/CF hardpoints |
| AUW / T/W | ~100 g / target 2.0 — verify 0802/1S thrust |

No tilt rotor, swashplate, or collective. Fixed motors + elevons + differential thrust.

## Electronics (Bee Core bring-up)

- RP2350A + QSPI flash + USB-C + SWD
- BMI270 IMU (SPI)
- 1× EFM8BB21 ESC channel, Bluejay **Layout O**, EFM8 on VBAT (1S)
- 1× servo PWM + companion header
- KiCad 9 project under `electronics/bee-core-bringup/bee-core-v01/`
- Schematic ERC clean; **PCB layout not fab-ready** (routing paused for manual finish)
- Bring-up board outline ~80×60 mm; flight target 32×36 mm

See `electronics/bee-core-bringup/` docs (`DESIGN.md`, `ESC-TOPOLOGY-DECISION.md`, `PCB-STATUS.md`).

## Status

Active hardware learning path. PCB routing handed back for manual / alternate tooling.
