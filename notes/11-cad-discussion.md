# CAD discussion notes (Rad CAD / CAD agent)

**Period:** ~2026-09-15 → pause  
**Repo path:** `cad/`  
**Project name:** BeeWhoopTailsitter

## Geometry lock (v0 block-out)

From Rad CAD handoff / VibeCAD block-out (provisional where noted):

| Spec | Value |
|------|--------|
| Span | ~120 mm |
| Mean chord | 48 mm (root 52 / tip 44) |
| Area | ~5760 mm² |
| Motors | Y ±30 mm |
| Prop discs | 40 mm (viz only — do not print as flight props) |
| Elevons | 15 mm chord, 8 mm root gap |
| AIO tray | **32×36×8 mm** @ ~33% MAC |
| Battery cue | 1S near LE |
| Servos | 2× micro ~9×12×22 |
| Materials | Dual-extruder PLA + Air/LW-PLA; PETG/CF only for hardpoints |
| AUW / T/W | ~100 g / target ~2.0 |

## Architecture (shared with electronics)

- Dual fixed motor, dual elevon tailsitter
- No tilt rotor / swashplate / collective
- Printable / makeable first bird for learning + talent/funding demo

## Files in repo

- `cad/BeeWhoopTailsitter.FCStd` — main FreeCAD / VibeCAD model
- `cad/BeeWhoopTailsitter.stl` — mesh export
- `cad/build_bee_whoop_tailsitter.py` — rebuild script (`BEE_*` objects)
- `cad/project.vibecad.json` — VibeCAD project metadata
- `cad/README.md` — short geometry summary

Mac source paths (originals):

- `/Users/theronrogers/Documents/VibeCAD/BeeWhoopTailsitter.{FCStd,stl}`
- `/Users/theronrogers/Documents/VibeCAD/build_bee_whoop_tailsitter.py`
- `~/Library/Application Support/VibeCAD/v26-3/VibeCAD/projects/BeeWhoopTailsitter-e0477b03/`

## Flags / open questions

1. **Thrust margin:** 0802/1S may be marginal at ~100 g AUW (T/W ~2). Revisit 1102 or lighten structure before locking motors.
2. Board outline: electronics bring-up is 80×60 for debug; flight tray stays **32×36** — shrink AIO after Bee Core proves out.
3. Optional sibling CAD (not in this repo unless asked): DualRotorTailsitter / Person iterations under the same VibeCAD folder.

## Alignment with electronics

AIO tray size drove silk/docs on the Bee Core PCB (“flight target 32×36”). Companion/cam/swarm are later; leave mechanical room for a companion board when the airframe grows I/O.
