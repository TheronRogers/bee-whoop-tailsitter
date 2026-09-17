# Bee Core v0.1 — next steps after schematic ERC cleanup

**Current status (2026-09-16, MT / UTC-6):** schematic ERC is clean for errors: **0 errors / 35 warnings** in KiCad 9.0.2. PCB layout is **PAUSED** for Theron manual/other-tool work. Read [`HANDOFF.md`](HANDOFF.md) before opening or editing the board.

## Working PCB handoff

- Open `bee-core-v01-kicad9-bringup.kicad_pro` in KiCad **9.0.2**.
- The editable schematic is `bee-core-v01-kicad9-bringup.kicad_sch` and the working PCB is `bee-core-v01-kicad9-bringup.kicad_pcb`.
- The working PCB is the restored pre-rip baseline, not the failed F.Cu rip/autoreroute result.
- KiCad 10 native rollback/reference: `bee-core-v01.kicad10-native-backup.kicad_pcb`.
- Bring-up outline: **80 × 60 mm**. Flight target / Rad CAD tray: **32 × 36 mm**.
- Post-stitch baseline: approximately **0 unconnected / 57 shorts / 82 crossings**. **Not fab-ready.**

## Completed

- Hierarchical IMU / SERVO / ESC / COMPANION sheets are present and connected.
- U2 duplicate regulator-output ERC conflict resolved with a documented passive duplicate pin.
- Root +1V1/VREG_AVDD and ESC VBAT power-tree flags are connected.
- ESC U20 VDD is tied to VBAT and C24 decoupling is connected.
- Final ERC report: `ERC-REPORT.md` (0 errors / 35 warnings).
- Final KiCad 9 ERC report: `work/erc-final-zero.rpt`.

## PCB layout — paused

Do not continue routing here and do not change schematic nets. Suggested manual/other-tool sequence when resumed:

1. U1 fanout cleanup.
2. ESC phase/gate/DShot corridor.
3. F.Cu cleanup.
4. Zone refill and PCB DRC.

The ESC topology is locked: **Layout O**, EFM8 VDD on **VBAT**, and **IRLML2244/IRLML6244** FETs. The 0802 thrust assumption may be marginal in the 32 × 36 mm Rad CAD tray; validate it before locking the flight layout.
