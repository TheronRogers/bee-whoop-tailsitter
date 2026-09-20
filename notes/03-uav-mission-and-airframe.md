# 03 — UAV mission and airframe

UAV Mission Designer closeout. Two layers: the group-chat v0.1 envelope, then the signed v1 that replaced it. Only mission and airframe locks. Cost, sim fidelity, and manufacturing process live on other cards.

## v0.1 envelope (group, then superseded)

First lock, from the 10-gal / two-rotor tailsitter prove-it:

| Item | Number |
|---|---|
| Span | 2.8 m |
| Empty | 30 kg (cut to 24.9 kg dry so flight test stays Part 107) |
| Wet AUW | 68 kg with 10 gal; 63 kg at 24.9 kg empty |
| Tank | Bought 40 L, load 10 gal (38 kg). Do not invent a tank. |
| Planform | Two-rotor tailsitter. Rail-launch airplane-mode when full. Hover only after the dump. |
| Door + rail shoe | Same station: tank centroid / 25% chord |
| Airspace | 200 m box, surface to 15 m AGL, hard deck 8 m |
| Pass | 15–20 m/s so a 0.5–1 s gravity dump paints an 8–20 ft pile edge |
| Recovery | Hover after the door, dirt RTL next to the truck. No bed catch, no wire. |
| Rail | ≤2.5 m shoe on a parked pickup. Exit 12 m/s. 15–25 m post-shoe accel to 16 m/s. 80 m two-track is fallback. |

US/NDAA build. No DJI next to air ops. Pickup we already own, not a bought catapult.

**This envelope is stale.** Fire called 2 gal at 16 m/s a ~30 m streak (coverage ~0.3) and a toy. Signed v1 is below.

## Signed v1 mission

Leftover hotspot / mop-up on a prescribed pile. Not an active flaming edge. Not a wildfire.

- **Part 107 wet:** AUW ≤ 24.9 kg (55 lb) including water.
- **Water:** 1.5–2.0 gal Class A at 0.1–0.3%, nominal **2 gal / 7.6 kg**. Dense stream, not a farm mist or a soft bladder. Under 1 gal is a toy.
- **Cadence:** ≤3 min tote-to-target-to-tote (fill 15 + shoe 20 + air ≤90 + land 15 = 140 s). 4 min is abort (pack swap or go-around). 2–3 pins / 6–10 gal in ~15 min. Battery sized ~100 Wh / 3 sorties. No swap in the window. 2 gal premix in ≤15 s.
- **Hit:** centroid in the middle third of the 4 m wet patch (within ~1 m of dump center). A graze on the wrong side of the log is a miss. Water still needs a hand tool after. We do not replace the stir.
- **Sky-eye:** separate aircraft or mast. Places a drop line in a shared RTK frame (~30 m slant). Cues **predicted ground impact with wind**, not door-open. Bomber is dumb RTK + rangefinder + servo door. No thermal on the bomber. Release is onboard when it crosses. Live-stick from video is a miss (300 ms = 16 ft at 16 m/s).
- **Pin:** DDM the burn boss can punch into Avenza or a Garmin they already carry.
- **Ops:** one human on the radio, under existing air ops, next to a Type 4/5 crew. Daytime.
- **Build:** US / NDAA path.

## Signed airframe

Theron's BWB plank (Prototyper card). Not a tube + H-tail.

- **1.7 m span × 1.4 m** spinner-to-tail-pads
- **0.82 / 0.45 taper, 1.08 m², slotted flap, no canards**
- Two tractors blowing most of the wing, large elevons in the wash
- Tank in the root. Gravity **stream** door at the TE / feet, not a belly pod (hover is nose-up; a belly door paints a wall)
- **Empty ≤ 17.3 kg** so 2 gal still fits under 24.9 kg
- **Wet T/W ≥ 1.3 at 7000 ft** (32 kgf, ~16 kgf/motor). Empty T/W ~1.9. 1.04 wet sinks in a real hotspot (40°C column → 0.91; 80°C → 0.81). Sit offset from the hottest core. Do not hover in an 80°C plume.

The 2.8 m / 30 kg / 68 kg / 40 L-full set is leftover from the 10-gal bird. Do not inherit it as v1 truth.

## Signed dump profile

Not a 16 m/s airplane pass. Not a sit. Not hover-until-empty.

- **Rotor-borne tilt-crawl, 3–4 m/s** (Fire signed). 0.5 m/s is a footnote, not the crawl speed.
- This wing cannot fly 3–4 m/s (free-stream stall ~15 m/s at 7000 ft). Honest blown floor is 8–10 m/s. That 8–10 wing-borne / belly-door fork was rejected. Do not mix door and speed.
- **Height is over the crown, not the dirt.** Prove-it: **8 m over-crown / 6 m door-open** (no-wind). Step to 5 m over-crown (≥3 m feet-to-wood) only after the first hits. 5 m over a 2–3 m pile measured from dirt puts wash in the embers — don't.
- **Door-open is ~6 m before the pin** (4–5 m throw + half of the 4 m patch). 2 m is half-patch (centering), not the release point. A 2 m start at 8 m lands 2–6 m past the pin.
- Lead at 5 m over-crown is still **~5 m at 3 m/s, ~6 m at 4 m/s**, not 4 m. Same rule: throw + half streak.
- **1 s stream dump → 4 m wet patch.** 1 m is aim (centroid inside the patch), not patch width. Not a 0.3 s bag.
- Sky-eye predictor carries wind. A spray in a 2–3 m/s crosswind drifts ~2–4 m and walks the centroid out of the middle third. Keep the door a stream.
- **Crossing, not a sit.** T/W 1.3 only allows ~35° / 0.6 m of body offset — not out of a core. Time-in-heat is the offset. Body never parks over the heat.
- Hard deck 8 m at this speed. Airplane pass stays off.

## Launch and recovery (partly open)

- Parked pickup, shoe ≤ 2.5 m if we still rail. Exit 12 m/s. 5 kJ commit / 9 kJ if blown lift does not show — those kJ numbers were for the 2.8 m bird; treat as stale unless re-run.
- **Thrower (winch / sling / bungee) unpicked.**
- Recovery: hover after dump, dirt RTL next to the truck. No bed catch, no wire.
- At Part 107 wet mass, T/W > 1 wet is available. Rail may be optional for v1. Not locked.

## Still open

- Thrower
- Whether v1 still rail-launches or lifts off the truck (wet T/W 1.3 can hover)
- Rotor / prop selection for 32 kgf at 7000 ft
- Avionics beyond Cube-class FC + RTK + rangefinder + NDAA radio
- Sky-eye as aircraft vs mast
- Bought battery pack (energy target only: ~100 Wh / 3 sorties)
- Structure and materials inside the BWB box

## Will-nots

- DJI or non-NDAA over a pile next to air ops
- Invented tank or spray boom
- Wildfire or active flaming-edge prove-it
- Live-stick dump from sky-eye video
- Belly door
- 16 m/s / airplane dump pass
