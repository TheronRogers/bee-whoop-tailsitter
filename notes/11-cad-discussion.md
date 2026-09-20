# CAD discussion notes (Rad CAD / CAD agent)

**Period:** ~2026-09-15 → pause  
**Repo path:** `cad/`  
**Project name:** BeeWhoopTailsitter  
**Source:** CAD agent pause-pack handoff (2026-09-19)

## Status

v0 geometry blocked out; files staged in this repo. VibeCAD agent API was down when first pushed — live FCStd edits only if Theron opened the model manually. DualRotor / person-carrier CAD is **out of scope** for this pause pack.

## Coordinate frame (VTOL)

+Z up LE/props; TE/elevons at bottom; +Y span; +X face.

## Geometry locked

| Param | Value |
|------|--------|
| Span | 120 mm |
| Root / tip / mean chord | 52 / 44 / 48 mm |
| Area S | 5760 mm² (0.00576 m²) |
| Motor Y | ±30 mm |
| Prop disc D | 40 mm (**viz only — do not print**) |
| Elevon chord | 15 mm (~31% mean), root gap 8 mm |
| AIO tray | **32×36×8 mm** @ ~33% MAC from LE |
| Battery cue | ~8×40×12 mm near LE (1S 300–450 mAh class) |
| Servos | 2× ~9×12×22 mm near root TE |
| Prop disc gap / tip clear | 20 mm / 10 mm |
| Layout | Fixed dual motors, dual elevons, tailsitter (no tilt); yaw = differential thrust (hover) + elevon mix (cruise) |

## Materials (plan — not printed yet)

| Material | Use |
|----------|-----|
| Air / LW-PLA | Wing core, thick fairings, light elevon bodies |
| PLA | Skins, non-critical structure |
| PETG (or CF later) | Motor mounts, servo mounts, spar inserts, AIO standoffs, skids |

Do not print: prop discs, ground plane. Print strategy: sandwich PLA + Air PLA; engineering filament only on hardpoints.

## AUW / thrust

- Target AUW ~100 g (band ~80–120 g)
- Wing loading @ 100 g ≈ 17.4 kg/m² (~3.56 psf) — soft
- T/W target 2.0 ⇒ ~200 g total thrust (~100 g/motor)
- **Open risk:** 0802 + ~1.5″ props on 1S may be **marginal** for that T/W — verify static thrust before locking size; **1102** is the step-up

## Files

**In repo (`cad/`):**

- `BeeWhoopTailsitter.FCStd`
- `BeeWhoopTailsitter.stl`
- `build_bee_whoop_tailsitter.py` (`BEE_*` objects)
- `project.vibecad.json`
- `README.md`

**Mac originals:**

- `/Users/theronrogers/Documents/VibeCAD/BeeWhoopTailsitter.{FCStd,stl}`
- `/Users/theronrogers/Documents/VibeCAD/build_bee_whoop_tailsitter.py`
- `~/Library/Application Support/VibeCAD/.../BeeWhoopTailsitter-e0477b03/`

## Alignment with electronics

- Platform: whoop-adjacent learning bird; custom RP2350A AIO (Bee Core bring-up first, then flyable 2-ESC / 2-servo); ArduPilot STM32 escape hatch
- Electronics bring-up PCB is ~80×60 mm for debug; flight tray stays **32×36** until flyable AIO shrinks
- See also `notes/10-electronics-discussion.md` and `notes/open-questions.md`
