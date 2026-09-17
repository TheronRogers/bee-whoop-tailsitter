# DRC categories — Bee Core kicad9 bring-up

Board: `bee-core-v01-kicad9-bringup.kicad_pcb`  
Tool: KiCad 9.0.2 `kicad-cli pcb drc --severity-all`  
Pass: 2026-09-16 ~05:54 MDT (F.Cu rip + net-group re-route)  
Prior: 05:50 MDT placement collision fix; 05:37 electrical cleanup; 05:21 stitch

`kicad-cli` reports DRC violations and unconnected items as two totals.
Category counts below include both (`[code]:` headers in the report).

## After F.Cu rip + re-route (deliverable)

Source: `work/drc-fcu-ripreroute-deliverable.rpt`

| Count | Δ vs placement | Code |
|------:|---------------:|------|
| 162 | −42? / mask churn | solder_mask_bridge |
| 153 | +96 | shorting_items |
| 96 | +14 | tracks_crossing |
| 73 | +? | clearance |
| 71 | +71 (was 0) | unconnected_items (≈58 ESC + open GPIOs) |
| 58 | | silk_overlap |
| 39 | | silk_over_copper |
| 24 | | hole_clearance |
| 20 | 0 | courtyards_overlap |
| 16 | | hole_to_hole |
| 9 | 0 | drill_out_of_range |
| 5 | | holes_co_located |
| 3 | | silk_edge_clearance |
| 2 | | via_dangling |
| 1 | | track_dangling |
| 1 | | copper_edge_clearance |

**CLI totals:** 662 DRC violations, **71 unconnected**.

Critical routed nets (power/USB/crystal/QSPI/IMU/GPIO14): **0 unconnected**. ESC intentionally open.

## Before this pass (placement collision fix)

Source: `work/drc-placement-deliverable.rpt`

| Count | Code |
|------:|------|
| ~204→145 mask varies | solder_mask_bridge |
| 57 | shorting_items |
| 82 | tracks_crossing |
| 0 | unconnected_items |

**CLI totals:** 529 DRC violations, **0 unconnected**.

---


## Historical sections (prior passes)

# DRC categories — Bee Core kicad9 bring-up

Board: `bee-core-v01-kicad9-bringup.kicad_pcb`  
Tool: KiCad 9.0.2 `kicad-cli pcb drc --severity-all`  
Pass: 2026-09-16 ~05:50 MDT (placement collision fix)
Prior: 05:37 MDT electrical cleanup; 05:21 MDT stitch
Prior stitch baseline: 05:21 MDT in sections below

`kicad-cli` reports DRC violations and unconnected items as two totals.
Category counts below include both (`[code]:` headers in the report).

## Before (GUI-stalled board, B.Cu GND zone present, 0 vias)

Source: `work/drc-before.rpt`

| Count | Code | Notes |
|------:|------|-------|
| 204 | solder_mask_bridge | unchanged; dense 0402/QFN mask |
| 85 | tracks_crossing | F.Cu spaghetti from the straight-pass routing |
| 78 | silk_overlap | warning |
| 55 | shorting_items | includes GPIO14 vs +3V3 / GPIO15 / GPIO13 |
| 54 | silk_over_copper | warning |
| 38 | unconnected_items | **all GND** — SMT pads isolated on F.Cu |
| 35 | clearance | netclass 0.20 mm |
| 33 | courtyards_overlap | placement |
| 9 | drill_out_of_range | U1 EP 0.20 mm thermal vias vs min drill |
| 6 | silk_edge_clearance | warning |
| 4 | copper_edge_clearance | |
| 3 | hole_to_hole | |

**CLI totals:** 566 DRC violations, **38 unconnected**.

## After (scripted stitch)

Source: `work/drc-final.rpt`  
Board files: `bee-core-v01-kicad9-bringup-stitched.kicad_pcb` (also copied over the working `.kicad_pcb`)

| Count | Δ | Code |
|------:|--:|------|
| 204 | 0 | solder_mask_bridge |
| 122 | +37 | tracks_crossing |
| 78 | 0 | silk_overlap |
| 54 | 0 | silk_over_copper |
| 51 | −4 | shorting_items |
| 42 | +7 | clearance |
| 33 | 0 | courtyards_overlap |
| 9 | 0 | drill_out_of_range |
| 6 | 0 | silk_edge_clearance |
| 4 | 0 | copper_edge_clearance |
| 3 | 0 | hole_to_hole |
| 0 | −38 | unconnected_items |

**CLI totals:** 606 DRC violations, **0 unconnected**.

Via-related codes (`via_diameter`, `annular_width`) are **0** after setting KiCad 9 padstack size 0.6 / 0.3 mm on all copper layers.

## What the 38 unconnected actually were

Every ratsnest pair was GND–GND. Typical examples from the before report:

- U10 pads 6–7, U20 pads 3–12, U1 pad 47 vs EP PTH 61
- Crystal X1 GND pads vs nearby decoupling
- Capacitor GND pads in the decoupling grid (C1–C24)
- FET source pads Q1–Q3
- J4 / J7 connector GND

None of those pads had an F.Cu path onto the In1.Cu / B.Cu GND pours because **the board had zero vias**.

## GPIO14 shorts (before)

Three `shorting_items` involved GPIO14:

1. **GPIO14 ↔ +3V3** at U1 south-east corner  
   Track `(52.10, 39.46) → (43.00, 37.45)` (J2 pad 32 → U1 pad 18).  
   Centerline miss to the +3V3 pad-20 / pad-11 diagonal was **0.173 mm**; with 0.20 mm trace width that is a copper-body short (need ≥ 0.20 mm). The same diagonal also overlapped U1 pad 20 (+3V3, 0.2×0.8 mm) and pad 19 (GPIO15).
2. **GPIO14 ↔ GPIO15** — same fan-in vs U1 pad 19 track.
3. **GPIO14 ↔ /GPIO13** — same fan-in vs U1 pad 17 track.

A related U20–J2 GPIO14 run `(78.75, 36.45) → (52.10, 39.46)` passed within shorting distance of `/ESC/ESC_Ap` at `(79.55, 37.75)` (U20). That geometry was rerouted south-then-west in the same pass.

**After:** no `shorting_items` mention GPIO14.

## Root causes (not a GUI refill bug)

1. **No layer transition.** 0 vias anywhere. In1.Cu and B.Cu GND zones were assigned to net GND and were filled; F.Cu SMT GND pads still could not reach them.
2. **No F.Cu GND copper.** 0 GND tracks before the script. A trial F.Cu GND zone *did* drive unconnected toward 0–1 but added many new shorts against the dense F.Cu signal mesh; it was **not** kept.
3. **Thermal relief was secondary.** Zones were switched to solid pad connection (`ZONE_CONNECTION_FULL`) on In1/B.Cu. That alone did not clear the 38 unconnected; vias did.
4. **GPIO14 was QFN-pitch fan-in**, not a zone-net assignment error and not a netlist mismatch.
5. Duplicate In1.Cu GND zone `(1,1)–(54,49)` plus board-sized `(11,11)–(89,69)` is harmless leftover geometry, not the stall.

## Files

- `work/drc-before.rpt` — baseline
- `work/drc-final.rpt` — after stitch
- `work/stitch_final.py` — padstack-aware via + dogleg script
- `work/bee-core-v01-kicad9-bringup-pre-stitch.kicad_pcb` — working file immediately before this pass
- KiCad 10 backup **not** modified

## After electrical cleanup (2026-09-16 05:37 MDT)

Source: `work/drc-deliverable.rpt` (also `work/drc-after-in2.rpt`)  
Board: `bee-core-v01-kicad9-bringup.kicad_pcb` (stitched copy updated)

Compared to post-stitch baseline (`work/drc-final.rpt`).

| Count | Δ | Code |
|------:|--:|------|
| 204 | 0 | solder_mask_bridge |
| 130 | +8 | tracks_crossing |
| 78 | 0 | silk_overlap |
| 54 | 0 | silk_over_copper |
| 45 | −6 | shorting_items |
| 36 | −6 | clearance |
| 33 | 0 | courtyards_overlap |
| 9 | 0 | drill_out_of_range |
| 6 | 0 | silk_edge_clearance |
| 4 | 0 | copper_edge_clearance |
| 3 | 0 | hole_to_hole |
| 0 | 0 | unconnected_items |

**CLI totals:** 602 DRC violations, **0 unconnected**.

### Strategy notes
- Kept In1.Cu as GND; no F.Cu GND pour.
- In2.Cu signal experiments (bulk move / via-jog) were **not** kept — they increased shorts and hole-clearance noise.
- Net win this pass: remove redundant long F.Cu GND links that were shorting the signal mesh while pads remained via-stitched to In1/B.Cu.
- Crossings ticked up slightly from remaining spaghetti + a few thin repair stubs; not fab-ready.

### Files
- `work/bee-core-v01-kicad9-bringup-pre-in2-reroute.kicad_pcb` — snapshot before this pass
- `work/pass1_gnd_links.py` — GND link removal script
- `work/drc-deliverable.rpt` — after
- KiCad 10 backup **not** modified

## After placement collision fix (2026-09-16 ~05:50 MDT)

Source: `work/drc-placement-deliverable.rpt`  
Board: `bee-core-v01-kicad9-bringup.kicad_pcb` (stitched copy updated)

Compared to post-electrical-cleanup baseline (`work/drc-deliverable.rpt`).

| Count | Δ | Code |
|------:|--:|------|
| 203 | −1 | solder_mask_bridge |
| 82 | −48 | tracks_crossing |
| 58 | −20 | silk_overlap |
| 57 | +12 | shorting_items |
| 55 | +19 | clearance |
| 39 | −15 | silk_over_copper |
| 20 | −13 | courtyards_overlap |
| 9 | 0 | drill_out_of_range |
| 3 | −3 | silk_edge_clearance |
| 1 | −3 | copper_edge_clearance |
| 1 | +1 | hole_clearance |
| 1 | +1 | copper_sliver |
| 0 | 0 | unconnected_items |
| 0 | −3 | hole_to_hole |

**CLI totals:** 529 DRC violations, **0 unconnected**.

### Placement outcome
- Pad–pad shorts between different footprints: **0** (themes J6/C1–C4, R16/U1 EP, U10/+3V3, R8–R9/U3, SW1/J3, SW2/J4 cleared).
- Short count rose because stretched F.Cu diagonals create new track/via shorts; not because footprints still overlap.
- Crossings and courtyards improved materially.

### Files
- `work/bee-core-v01-kicad9-bringup-pre-placement-fix.kicad_pcb` — snapshot before this pass
- `work/drc-placement-deliverable.rpt` — after
- `work/placement_fix_final.py` — notes/script
- KiCad 10 backup **not** modified
