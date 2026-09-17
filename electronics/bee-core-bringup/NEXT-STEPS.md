# Bee Core v0.1 — next steps and PCB handoff

**Current status (2026-09-16, MT / UTC-6):** schematic ERC is clean for errors (**0 errors / 35 warnings** in KiCad 9.0.2). PCB layout is **PAUSED** for Theron to continue manually or with another layout tool. See [`bee-core-v01/HANDOFF.md`](bee-core-v01/HANDOFF.md) for the verified baseline and layout notes.

## Handoff

- Working PCB: `bee-core-v01/bee-core-v01-kicad9-bringup.kicad_pcb`.
- This is the restored pre-F.Cu-rip/autoreroute board; do not use the failed rip result as the routing baseline.
- Bring-up outline is **80 × 60 mm**; the flight target and Rad CAD tray are **32 × 36 mm**.
- PCB baseline is approximately **0 unconnected / 57 shorts / 82 crossings** after stitching. It is **not fab-ready**.
- ESC lock remains Layout O, EFM8 VDD on VBAT, with IRLML2244/IRLML6244.

## Completed

- Hierarchical IMU / SERVO / ESC / COMPANION sheets are present and connected.
- U2 duplicate regulator-output ERC conflict was resolved with a documented passive duplicate pin.
- Root +1V1/VREG_AVDD and ESC VBAT power-tree flags are connected.
- ESC U20 VDD is tied to VBAT and C24 decoupling is connected.
- Final ERC report: `bee-core-v01/ERC-REPORT.md` (0 errors / 35 warnings).
- KiCad 9 bring-up project and PCB were preserved separately from the KiCad 10 native backup.

## PCB layout — paused

Do not continue routing in this pass and do not change schematic nets. When Theron resumes, the suggested order is:

1. Clean the U1 fanout.
2. Route the ESC phase/gate/DShot corridor.
3. Clean the F.Cu mesh/crossings.
4. Refill zones and run PCB DRC.

The Rad CAD tray is 32 × 36 mm; 0802 thrust may be marginal and should be validated before the flight outline is locked.
