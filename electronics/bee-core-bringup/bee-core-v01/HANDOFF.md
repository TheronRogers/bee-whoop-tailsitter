# Bee Core v0.1 — PCB layout handoff

**Status:** PCB layout **PAUSED** for Theron to continue manually or with another layout tool.
**Handoff date:** 2026-09-16 (MT / UTC-6)

## Verified working baseline

The working PCB is the restored pre-rip board:

```text
bee-core-v01/bee-core-v01-kicad9-bringup.kicad_pcb
```

It was verified byte-for-byte against:

```text
bee-core-v01/work/bee-core-v01-kicad9-bringup-pre-fcu-ripreroute.kicad_pcb
```

The working file and that snapshot both have SHA-256
`4b1771956bd26228d4c1e93bb610ed2b75a39c3be16262ae617d668ec21cc5cc`.
The matching copy `bee-core-v01-kicad9-bringup-stitched.kicad_pcb` is also present.

**Do not use the failed F.Cu rip/autoreroute as the baseline.** Its intermediate snapshot is:

```text
bee-core-v01/work/bee-core-v01-kicad9-bringup-ripped.kicad_pcb
```

The failed-pass scripts and DRC reports remain under `bee-core-v01/work/` for history only. The KiCad 10 source/rollback backup is separate and was not used as the working bring-up board.

## What to open

Open the KiCad 9 project, not an individual legacy/native board first:

```text
Project:    /workspace/bee-core-bringup/bee-core-v01/bee-core-v01-kicad9-bringup.kicad_pro
Schematic:  /workspace/bee-core-bringup/bee-core-v01/bee-core-v01-kicad9-bringup.kicad_sch
PCB:        /workspace/bee-core-bringup/bee-core-v01/bee-core-v01-kicad9-bringup.kicad_pcb
```

The box has **KiCad 9.0.2** installed. The KiCad 10 native PCB backup is named:

```text
bee-core-v01/bee-core-v01.kicad10-native-backup.kicad_pcb
```

Treat that KiCad 10 backup as rollback/reference material; do not overwrite it during the manual bring-up pass.

## Design and electrical status

- **Bring-up outline:** 80 × 60 mm.
- **Flight target:** 32 × 36 mm.
- **Rad CAD tray:** 32 × 36 mm; the 0802 motor/thrust assumption may be marginal, so validate thrust and packaging before locking the flight version.
- **Schematic ERC:** 0 errors / 35 warnings in KiCad 9.0.2. The warnings are documented in `ERC-REPORT.md` and are not a reason to alter schematic nets during this PCB handoff.
- **PCB post-stitch baseline:** approximately 0 unconnected, approximately 57 shorts, and approximately 82 track crossings. This is **not fab-ready**. Counts are the handoff baseline, not a fabrication sign-off.

### ESC topology lock

Keep the ESC topology unchanged while laying out:

- Bluejay/BLHeli_S **Layout O**.
- EFM8BB21 VDD powered from **VBAT** (1S); it is not powered from board +3V3.
- Complementary FET bridge using **IRLML2244** high-side P-FETs and **IRLML6244** low-side N-FETs.

Do not change schematic nets or substitute Layout A during this layout pass. Refer to `ESC-TOPOLOGY-DECISION.md` for the locked pin/polarity details.

## Suggested manual next steps

1. **U1 fanout:** manually clean the RP2350 0.4 mm-pitch escapes, alternating layers/vias only where there is a clear courtyard and preserving power/USB/QSPI/crystal intent.
2. **ESC corridor:** route the phase/gate/DShot paths through the east-side corridor with deliberate layer changes and clean return paths; keep the EFM8/VBAT/FET topology intact.
3. **F.Cu cleanup:** remove the remaining straight-pass mesh crossings and shorts rather than adding another blind autoroute pass. Keep In1 as the GND reference strategy unless the layout decision is deliberately revisited.
4. Refill zones, run PCB DRC, and resolve the actual shorts/crossings and any unconnected items before considering fabrication export.

This handoff intentionally stops at the restored pre-rip baseline. No further routing was performed here.
