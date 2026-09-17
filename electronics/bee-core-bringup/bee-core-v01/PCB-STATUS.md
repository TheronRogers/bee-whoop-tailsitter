# Bee Core bring-up PCB routing status

## Current handoff status — 2026-09-16 (MT / UTC-6)

- **PCB layout: PAUSED** for Theron to continue manually or with another tool.
- Working board: `bee-core-v01-kicad9-bringup.kicad_pcb`. It is the restored pre-F.Cu-rip/autoreroute board, verified byte-for-byte against `work/bee-core-v01-kicad9-bringup-pre-fcu-ripreroute.kicad_pcb`.
- Handoff baseline: approximately **0 unconnected (post-stitch)**, **57 shorts**, and **82 track crossings**. **Not fab-ready.**
- Do **not** use `work/bee-core-v01-kicad9-bringup-ripped.kicad_pcb` or the later F.Cu rip/autoreroute outputs as the baseline; those are retained as failed-pass history only.
- See `HANDOFF.md` for the open-project paths, KiCad version, locked ESC topology, and suggested manual sequence.

## Historical failed F.Cu rip + net-group re-route (not current baseline)
- Attempted board: `bee-core-v01-kicad9-bringup.kicad_pcb` (F.Cu rip + net-group re-route 2026-09-16 ~05:54 MDT; subsequently restored).
- 4-layer stack: F.Cu / In1.Cu / In2.Cu / B.Cu. In1.Cu + B.Cu GND zones refilled. **No F.Cu GND pour.** In2.Cu carried experimental signal trunks.
- Attempted-pass DRC: **662 violations, 71 unconnected** (shorts 57→153; crossings 82→96).
- Fab: **No**.

## Routing
- QSPI flash to RP2350: QSPI_SCLK, QSPI_SD0, QSPI_SD1, QSPI_SD2, and QSPI_SD3 were routed on F.Cu. DRC still reports one unconnected-end warning on the QSPI_SCLK track, so this path needs cleanup/verification.
- USB D+/D-: not completed; series resistor/connector topology remains unrouted and has existing clearance/shorting violations around R8/J2.
- Crystal, IMU SPI, DShot/ESC gates, and VBAT/GND FET bridge: not completed.
- KiCad status after routing: 83 nets, 221 unconnected items reported by DRC. A reliable percentage-routed figure is not available from this pass.

## DRC
A DRC was run with zone refill enabled. Results before marker cleanup:
- Violations: 628+
- Errors: 509
- Warnings: 340+
- Unconnected items: 221
- Schematic parity: not run

The dominant blockers are existing dense-placement clearance/short violations, unrouted connections, and the QSPI_SCLK unconnected-end warning.

## JLCPCB/export blockers
Do not export for fabrication yet. Finish critical power and USB routing, complete the remaining SPI/clock/ESC nets, add/verify the B.Cu ground strategy, then rerun DRC and resolve the clearance/short violations.

## Screenshots
- Overview: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/ca4542acee9f4b07a139cd30061fc8ca103385b997669db2833e987f87a5135f.webp`
- MCU/flash area: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/5cd4f08d4cda67e923b7e255ab1ed1de3caa09c57a5f6929496ab9b0216a128f.webp`
- ESC power area: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/e76aace89648f5bf7090d52e8910e8a4580e3e5325d70e360c09b96f144a3965.webp`
- DRC results: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/c41d5551168bcaad5a09ac9782b95e5b20933c72f09b3a11b2d68e0833f13116.webp`

## Routing pass update (2026-09-16)
- Before/after DRC unconnected items: 221 -> 219. USB D+ and D- were routed through the series resistors; the USB reduction is verified in DRC.
- Crystal XIN/load-cap work was attempted but left blocked by dense placement/clearance; no dangling trial tracks were retained.
- IMU SPI (GPIO16-20), VBAT/GND FET bridge, B.Cu GND zone, and DShot remain open.
- Latest DRC: 621+ violations, 499 errors, 341 warnings, 219 unconnected items. Dominant theme remains dense-placement clearance/shorts plus unrouted connections.


## Final routing pass report (2026-09-16 03:20 UTC-6)
- DRC rerun after the routing pass: 619+ violations, 499 errors, 339+ warnings, and 219 unconnected items (before this pass: 221).
- USB: D+/D- series-resistor routing is present and the unconnected count dropped by 2, but DRC still flags one USB_D+ unconnected track end and dense shorts around the SW1/R8/J2 region.
- Crystal: XIN/load-cap routing remains blocked by dense placement; DRC still reports an XIN unconnected track end.
- IMU SPI GPIO16-20: not completed; trial routing was removed to avoid dangling tracks.
- VBAT/GND FET bridge and B.Cu GND zone: not completed. DShot GPIO14 via 220R to EFM8: not completed.
- Dominant DRC theme remains dense-placement shorts/clearance and unrouted connections.
- Screenshots from this pass:
  - Overview: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/87d450ca29ed5c4cbd7beeb930d70cdc5e2d553cc00b4d2dc7799e65c73f4d12.webp`
  - USB area: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/d0472d2ca8161e9baf3b050a41af26b4da8191d2f3186d39de965665c03a25e8.webp`
  - ESC power: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/c08c4398f1e37ae63a556a580486d0278193ffdd134dc2ace1d6d699c5877585.webp`
  - DRC: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/9cd4b25b8b1a593544416dac9d10da0e2c8ee5fef776c303aa5662a638353f4e.webp`


## Placement-first reset and final bring-up pass (2026-09-16 04:20 UTC-6)
- Target board was reset and saved; KiCad 10 backup was not modified.
- Board outline: 80 x 60 mm (10,10) to (90,70) mm. Silk note `flight target 32x36` retained.
- Existing signal tracks were removed and rebuilt as a clean 153-segment F.Cu connectivity pass. GND pours remain on In1.Cu and B.Cu; VBAT F.Cu pour remains confined to the ESC/right-side region.
- Unconnected baseline: 221 (prior recorded DRC); final live status/DRC: 38 (under 50).
- Critical connectivity: USB D+/D-, QSPI_SCLK/SD0-3/SS, XIN/XOUT, GPIO16-20 IMU/SPI, VBAT, and ESC phase/gate-related nets have explicit routes; final unconnected list begins with GND-only gaps.
- Final DRC with zone refill: 566+ violations, 463+ errors, 141 warnings, 38 unconnected items; schematic parity not run. Remaining violations are dominated by intentional straight-pass routing crossings/clearance and GND connectivity gaps; not fabrication-ready.
- Final overview screenshot: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/f7923da53a6b6d01059d8d01148c79205a1b5b459786b735d1bca0065fc7fd23.webp`
- Final DRC screenshot: `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/b133bb40bc48e38188aefa7070dfe58eac088b4ab8f302b6893cae4cd950c7dc.webp`


## Ground/DRC follow-up (2026-09-16 04:45 UTC-6)
- B.Cu GND zone is present in the target PCB and was refilled/saved; existing In1.Cu GND pours remain. No via-stitch array was added, and the attempted F.Cu GND-zone GUI operation was cancelled before completion.
- Live DRC after refill: 566+ violations, 463+ errors, 141 warnings, 38 unconnected items (unchanged from the placement-first baseline).
- Highest-severity remaining examples include F.Cu track crossings and shorts, including GPIO14 versus +3V3; these are not fabrication-ready.
- DShot documentation confirms the intended path `GPIO14 -- 220R -- EFM8 P0.5/RTX (pin 17)`. The PCB contains `/GPIO14` track/pad references, but the physical resistor-to-EFM8 continuity is not verified and the DRC still flags a GPIO14 short, so DShot is not signed off.
- Fab readiness: **No**.
- Screenshots: overview `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/a1c40dfbe89b6baa97353f7378f79606ed81b785906af8070eef72c84f603383.webp`; DRC `/home/box/agent-data/agents/841a3b31-c434-4ecf-b3ec-2cec458b2f0d/assets/a869cfa0d72c0234b1a0d52fe1a6a7e9b06216a91ed4a971d5e058478776afda.webp`.


## Scripted GND stitch / GPIO14 pass (2026-09-16 05:21 MDT)

Automated `pcbnew` Python + `kicad-cli pcb drc` on the kicad9 bring-up board. KiCad 10 backup was not touched.

### Root cause of the stalled 38 unconnected
The 38 DRC unconnected items were **all GND**, and they were never going to clear from a B.Cu zone refill in the GUI:

- The board had **0 vias** and **0 GND tracks** on F.Cu.
- GND copper existed only as filled In1.Cu and B.Cu zones (plus a VBAT F.Cu pour on the ESC side).
- Every SMT GND pad therefore sat on F.Cu with no layer transition onto the planes.
- Thermal-relief vs solid was not the blocker. Zones were switched to solid (`ZONE_CONNECTION_FULL`); unconnected only dropped after vias + short F.Cu stubs were added.
- A trial **F.Cu GND pour** did collapse unconnected to 0–1 but created dozens of new shorts against the existing F.Cu signal mesh. It was discarded.

### GPIO14 short — colliding geometry and fix
DRC before: GPIO14 shorted **+3V3**, **GPIO15**, and **/GPIO13**.

- U1 pad 18 (GPIO14) at `(43.00, 37.45)` is 0.40 mm pitch from pad 19 (GPIO15) and pad 20 (+3V3).
- The J2→U1 GPIO14 track `(52.10, 39.46) → (43.00, 37.45)` was a diagonal whose copper body overlapped pad 19/20 (centerline gap to the +3V3 pad-11→pad-20 diagonal: **0.173 mm**, less than the 0.20 mm trace width).
- The U20 pad 17 → J2 run `(78.75, 36.45) → (52.10, 39.46)` also ran past `/ESC/ESC_Ap` at U20 `(79.55, 37.75)`.

Fix: replace both diagonals with orthogonal 0.15 mm doglegs (U1 approach from y=41.0; U20 south to y=41.0 then west). Same treatment for GPIO15 and /GPIO13 fan-ins. **GPIO14 shorts after: none.**

### DRC before / after

| | Violations | Unconnected | Shorts | Track crossings |
|--|----------:|------------:|-------:|----------------:|
| Before | 566 | **38** | 55 | 85 |
| After | 606 | **0** | 51 | 122 |

Full category table: `DRC-CATEGORIES.md`. Reports: `work/drc-before.rpt`, `work/drc-final.rpt`.

Unconnected **38 → 0**. Shorts **55 → 51** (GPIO14 group gone). Total DRC **up 40** because the new doglegs and GND stubs add `tracks_crossing` / `clearance` on an F.Cu that was already a straight-pass mesh. Silk/courtyard/mask counts unchanged.

### What was written
- 28 through-hole GND vias, 0.6 mm / 0.3 mm, padstack size set on **all** copper layers (KiCad 9 `PADSTACK.SetSize`; `SetWidth` without a layer produced 0 mm copper and false `via_diameter`/`annular_width` hits).
- Short F.Cu GND stubs from SMT pads to those vias; a few adjacent-pad GND links (U10 6–7, U20 3–12, decoupling columns).
- In1.Cu / B.Cu GND zones refilled, solid pad connection, clearance tightened 0.50 → 0.25 mm.
- **No F.Cu GND zone** in the kept board.

### Files
- Working board replaced with the stitched result: `bee-core-v01-kicad9-bringup.kicad_pcb`
- Copy kept: `bee-core-v01-kicad9-bringup-stitched.kicad_pcb`
- Pre-pass snapshot: `work/bee-core-v01-kicad9-bringup-pre-stitch.kicad_pcb`
- Script: `work/stitch_final.py`
- `bee-core-v01.kicad10-native-backup.kicad_pcb` unchanged

### Fab readiness
**No.** 606 DRC violations remain. Dominant leftovers are solder-mask bridges (204), F.Cu track crossings (122), silk, and 51 real shorts (power vs signal, ESC phases, USB). GND ratsnest is cleared; the board is still a single-layer signal scramble.

### Recommended next human/GUI step
1. Open the stitched board, refill zones once in the GUI, and eyeball the 28 vias (MCU/ESC/IMU/decoupling). Confirm U1 pad 47 ↔ EP and U20 GND look sane.
2. Do **not** pour F.Cu GND until the F.Cu signal mesh is ripped up; a pour only shorts it.
3. Next real routing pass: move crossings onto In2.Cu (or a dedicated signal inner), starting with USB, crystal, and ESC phases. Leave In1 as GND.
4. Then add an F.Cu GND pour with ~0.25 mm clearance and a via stitch grid.
5. Only then chase the remaining 51 shorts / 122 crossings. Not fabrication-ready.

## Electrical cleanup pass (2026-09-16 05:37 MDT)

Goal: cut copper shorts/crossings using In2.Cu as signal while keeping In1.Cu GND; no F.Cu GND pour; unconnected stay 0.

### What was tried
1. **Bulk move long F.Cu trunks to In2** (134 segs, +220 vias): DRC blew up (935 viol / 7 unconn / 199 shorts) — vias landed on QFN pitch and both sides of crossings moved to In2 so they still crossed.
2. **Surgical In2 via-jogs** at geometric/DRC crossings: modest crossing help when loose, but new via annulars created more shorts than they cleared. Strict clearance allowed only ~12 jogs and crossings rose.
3. **Aggressive GND F.Cu stub/link rip-up**: crossings could drop a lot (e.g. ~60–67) but pad→via stubs had to come back for connectivity, reintroducing shorts in the dense mesh. SWIG/`GetTracks` also segfaults after large `Remove()` batches unless save+reload is used.

### What stuck (this board)
- Removed **6 redundant long F.Cu GND pad–pad links** that both shorted/crossed signals and were already plane-reachable via nearby stitch vias (decap column + U20 GND + C6/C5).
- Replaced one bad diagonal repair stub with a short **C3→(38.48,12) edge horizontal**.
- **No F.Cu GND pour.** In1.Cu + B.Cu GND zones refilled. In2.Cu left empty in the kept board (signal-via experiments discarded).
- KiCad 10 backup untouched. Snapshot: `work/bee-core-v01-kicad9-bringup-pre-in2-reroute.kicad_pcb`.

### DRC before / after

| | Violations | Unconnected | Shorts | Track crossings | Clearance |
|--|----------:|------------:|-------:|----------------:|----------:|
| Before (post-stitch) | 606 | **0** | 51 | 122 | 42 |
| After | 602 | **0** | **45** | 130 | 36 |

Full categories: `DRC-CATEGORIES.md`. Reports: `work/drc-final.rpt` (before), `work/drc-deliverable.rpt` / `work/drc-after-in2.rpt` (after).

### Fab readiness
**No.** Shorts **51→45** (material, copper-priority). Unconnected stays **0**. Crossings **122→130** (slightly worse — leftover F.Cu mesh + thin repair stubs). Still dominated by solder-mask bridges (204), silk, and ~45 real shorts (mostly placement pad–pad: J6/decap, U1 EP vs R16, USB/flash pitch).

### Recommended next step
1. Placement cleanup for remaining pad–pad shorts (J6 vs C1–C4, R16 vs U1 EP, U10 vs +3V3).
2. True In2 use: rip F.Cu signal mesh by **net groups**, place fanout vias in clear courtyards (not on QFN pads), route only one side of each crossing on In2.
3. Only then pour F.Cu GND.

## Placement collision fix (2026-09-16 ~05:50 MDT)

Goal: clear pad–pad shorts from overlapping footprints (J6/decap, R16↔U1 EP, U10/+3V3, USB/flash pitch). Prefer `pcbnew` Python; no F.Cu GND pour; keep In1/B.Cu GND via strategy; unconnected stay 0.

### Parts moved (16 footprints)
| Ref | From → To (mm) | Why |
|-----|----------------|-----|
| C1 | (34,12)→(28,18) | Clear J6 PTH row |
| C2 | (38,12)→(30,22) | Clear J6 |
| C3 | (42,12)→(43,21.5) | Crystal XIN load; clear J6 |
| C4 | (46,12)→(47.5,21.5) | Crystal XOUT load; clear J6 |
| C19 | (42,20)→(38,23) | Clear X1 |
| R14–R19 | y=33→y=48 (x unchanged) | Off U1 QFN/EP; south of J2 |
| R8 | (54,28)→(68,24) | Off U3 SOIC pads |
| R9 | (58,28)→(68,28) | Off U3 |
| U10 | (60,34)→(68,36) | Clear ESC R-row / +3V3 mesh |
| SW1 | (24,52)→(72,48) | Clear J3 PTH field |
| SW2 | (24,62)→(72,58) | Clear J4 PTH field |

Attached track/via endpoints on moved pads were translated with the footprints. Added GND via+stub where needed (C2, C3, U10; stub C1). Removed U10 +3V3 pad5–pad8 bridge that crossed its GND pads. Zones refilled. **No F.Cu GND pour. No In2 signal experiment.**

### DRC before / after

| | Violations | Unconnected | Shorts | Track crossings | Courtyards |
|--|----------:|------------:|-------:|----------------:|-----------:|
| Before (post electrical cleanup) | 602 | **0** | 45 | 130 | 33 |
| After placement | **529** | **0** | 57 | **82** | **20** |

Full categories: `DRC-CATEGORIES.md`. Reports: `work/drc-deliverable.rpt` (before), `work/drc-placement-deliverable.rpt` (after). Snapshot: `work/bee-core-v01-kicad9-bringup-pre-placement-fix.kicad_pcb`. Script notes: `work/placement_fix_final.py`.

### Placement themes — cleared
- **J6 vs C1–C4:** no remaining pad–pad shorts (caps relocated).
- **R16 vs U1 EP:** cleared (R14–R19 at y=48).
- **U10 vs +3V3 / R19:** cleared by moving U10 east + removing pad5–pad8 bridge.
- **USB/flash pitch (R8/R9 vs U3):** cleared.
- **SW1/J3, SW2/J4:** cleared.
- **Pad–pad different-footprint shorts: 0** (was 9+ plus PTH–pad placement pairs).

### Why shorts count rose (45→57) while placement shorts fell
Clearing overlaps stretches existing F.Cu diagonals across the 80×60 board. New shorts are almost all **track–track / track–via / pad–track from the pre-existing signal mesh**, not footprint copper sitting on other footprints. Only one remaining short names a moved pad (R8 pad2 vs `/ESC/PHASE_A` track). Corridor re-routes were tried and discarded — they increased crossings without net short reduction.

### Remaining short themes (57)
- F.Cu signal mesh crossings that DRC classifies as shorts (ESC phases, USB, GPIO fan-ins on U1 0.4 mm pitch).
- Power-rail tracks through remaining cap GND pads (C5/C6/C13–C15/C22/C23 on y=12/16/20 grid — not moved this pass).
- GND via annular vs nearby signal tracks (pre-existing stitch density).
- Connector PTH vs nearby tracks (J1/J2/J3/J7).

### Fab readiness
**No.** Unconnected **0**. Placement pad–pad collisions cleared. Shorts still **57** (above ≤15 target) — needs a real F.Cu rip-up / net-group re-route (optionally In2) before fab. Crossings improved **130→82**. Courtyards **33→20**.

### Recommended next step
1. Rip F.Cu signal mesh by net group; fan out with vias in clear courtyards; put one side of each crossing on In2.
2. Optionally nudge remaining rail-collision caps (C5/C6/C13–C15/C22/C23) off y=12/16/20.
3. Only then pour F.Cu GND.


## F.Cu rip + net-group re-route (2026-09-16 05:54 MDT)

Goal: rip scrambled F.Cu signal mesh (stretched after placement moves); re-route power/USB/crystal/QSPI/IMU on F.Cu+In2; leave ESC for next pass. Prefer pcbnew Python + kicad-cli. No F.Cu GND pour. In1 stays GND. KiCad 10 backup untouched.

### What was ripped
- **160 F.Cu signal tracks** removed (all non-GND).
- **Kept:** 32 F.Cu GND stubs, **31 GND stitch vias**, footprints, outline, In1.Cu + B.Cu GND zones, VBAT F.Cu zone, silk.
- Snapshot before rip: `work/bee-core-v01-kicad9-bringup-pre-fcu-ripreroute.kicad_pcb`
- Intermediate ripped-only: `work/bee-core-v01-kicad9-bringup-ripped.kicad_pcb`

### Nets re-routed (orthogonal F.Cu fanouts + In2 trunks)
| Group | Nets |
|-------|------|
| Power | +3V3, +1V1, VBAT, VBUS, /VREG_LX, /VREG_AVDD |
| USB | Net-(U1-USB_DP/DM), /USB_D+, /USB_D- |
| Crystal | /XIN, /XOUT, Net-(C4-Pad1) |
| QSPI | /QSPI_SCLK, SD0–SD3, /QSPI_SS, /FLASH_SS |
| IMU SPI | GPIO16–20 (U1↔U10 + J3 taps) |
| DShot stub | GPIO14 (U1↔J2↔U20); also /GPIO13, GPIO15 to J2 |

**Not routed (next pass):** all `/ESC/*` phase/gate/Vn nets, plus remaining header GPIOs (GPIO0–3, /GPIO4–12, /GPIO21–29, SWD, RUN, etc.).

Deliverable geometry: **283 track segs** (220 F.Cu + 63 In2.Cu), **116 vias** (31 GND + 85 signal). Script: `work/fcu_reroute_v3.py`.

### DRC before / after

| | Violations | Unconnected | Shorts | Track crossings |
|--|----------:|------------:|-------:|----------------:|
| Before (post-placement) | 529 | **0** | **57** | **82** |
| After rip+reroute | **662** | **71** | **153** | **96** |

Reports: `work/drc-placement-deliverable.rpt` (before), `work/drc-fcu-ripreroute-deliverable.rpt` (after). Categories: `DRC-CATEGORIES.md`.

Unconnected breakdown: **~58 ESC**, ~13 other open header/GPIO nets. **Power / USB / crystal / QSPI / IMU / GPIO14 show 0 unconnected** in DRC pad-net scan.

### Honest assessment — autoroute quality insufficient
Scripted orthogonal fanout + In2 trunks **does** clear the scrambled mesh and restores intentional connectivity for the priority net groups, but it **does not** meet the ≤20 shorts / lower-crossings success bar:

1. **U1 0.4 mm QFN pitch** cannot host parallel 0.15 mm escapes with 0.20 mm clearance on one layer; adjacent fanouts and power rings keep shorting.
2. **Via density** around decap / QSPI / IMU corridors adds annular shorts vs GND stitches and neighboring nets.
3. Moving vias without rewriting attached segments creates danglers — avoided in the kept board; residual 2 via_dangling / 1 track_dangling remain.

**Shorts 57→153 and crossings 82→96** — wrong direction vs target. Treat this board as a **structured intermediate** (mesh ripped, net groups on F.Cu+In2, ESC deliberately open), not a DRC win.

### Fab readiness
**No.** Not fabrication-ready. Prefer GUI or a DRC-aware router for U1 fanout/via placement before chasing the ≤20 short target.

### Recommended next step
1. Open deliverable; visually clean U1 north/south fanouts (alternate F.Cu vs In2 per pad, ≥0.55 mm stagger).
2. Route ESC phases/gates/DShot resistors on In2 east corridor with vias in clear sites (x≥60, y=40–50 grid).
3. Only then pour F.Cu GND.
4. KiCad 10 backup remains the rollback if this intermediate is discarded: `bee-core-v01.kicad10-native-backup.kicad_pcb`.
---
## 2026-09-16 restore
Restored working PCB from work/bee-core-v01-kicad9-bringup-pre-fcu-ripreroute.kicad_pcb after failed F.Cu rip/autoreroute (shorts 57→153). Failed attempt kept only as history via scripts in work/.
