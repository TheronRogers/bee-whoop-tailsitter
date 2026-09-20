# v0.1 Water-Drop UAV — Mission, Impact, Cost Lock

**Owner:** Vision Driver  
**Date:** 2026-08-21  
**Status:** Locked enough to prototype. Team being wound down; this is the handoff.

Get us to a probable prototype by refining mission, impact, and cost so we can scale from there. Hardware, rail, and sim fidelity live in the other docs. This one is the go/no-go.

## The prove-it (v0.1 is not a wildfire)

One daytime sortie on a **prescribed pile or leftover hotspot**, sitting under existing air ops next to a Type 4/5 crew. We do not replace them.

Three things, or we do not have a prototype:

1. **Find the heat** — a cheap FLIR *confirm* of the pile the burn boss already pointed at. Not a section search. Not a mapping product.
2. **Put 5–10 gal** of water or Class A on the **flaming edge**.
3. **Hand the burn boss a DDM pin** they can punch into Avenza or a Garmin they already carry.

Miss the edge, or they do not trust the pin, and we stay on the sawhorse.

## Flight profile we are working from

Theron's call, not the X8:

- Fixed-wing **two-rotor tailsitter**.
- **Rail-launch full** in airplane mode off a modified pickup (belly trolley). No tip-off, no vertical climb on the rail, no $49k catapult.
- **Hover only after the dump**, when the tank is light — pin, then dirt RTL next to the truck. No bed catch on v0.1.
- One **15–20 m/s pass** in a 200 m box, surface to 15 m AGL, hard deck 8 m. A 0.5–1 s gravity dump paints an **8–20 ft pile edge**, not a 200 m streak.

T/W empty ≥ 1.5, full < 1. That is why we launch on a rail and hover empty.

## Size class (UAV lock)

| Item | Value |
|---|---|
| Span | 2.8 m |
| Empty | 30 kg |
| AUW (10 gal) | 68 kg |
| Tank | Bought 40 L, centroid / 25% chord |
| Dump | Servo gravity door, not a spray boom |
| Rail shoe | Same station as the door / tank centroid |

## Constraints that killed other paths

- **We build drones.** Do not buy a DJI Agras T50. Federal and most state fire will not put DJI next to their air ops. A $25k bird a burn boss cannot say yes to is the expensive path.
- **US or NDAA-path.** T50 is the *envelope* (40 L, 5–10 gal, one pass), not the shopping list.
- **Keep the airframe boring.** It has to look like a tool, not a demo.
- **Do not invent the fire part.** Same 5–10 gal, Class A or water, one pass, one human on the radio.
- **Do not invent a wildfire sim.** v0.1 fidelity is the rail-to-pass-to-hover, a timed gravity dump, and a surveyed thermal-to-pin lever arm on a painted dirt line.

## Cost envelope (Cost Watcher)

Two-rotor + shop-welded rail + truck tote on a pickup we already own: **~$16–26k**.

- Airframe, US-path: ~$10–15k
- Welded rail / cradle: ~$3–5k
- Bed rack + 50–100 gal tote + fill pump: ~$2–4k

If the rail is not something we weld this month, the tailsitter becomes the expensive path. Spare battery pair is the real ops line on a short sortie. Alta X ($46k, 35 lb) fails 5–10 gal. Harris H6HL is quote-only. Draganfly stays off the BOM.

## Sequence we locked

1. Hose-and-scale the CG walk on a sawhorse (this week) before anyone welds the rail.
2. Weld a belly-trolley rail that throws it in airplane mode.
3. First hover-land is dirt next to the truck.

## Still open

- Planform / airfoil, rotor diameter and station, exact motors, elevon sizing
- Avionics (Cube + Doodle Labs is the NDAA-cost assumption, not a lock)
- Tank brand, FLIR model, pin-drop hardware
- Real CG numbers from the sawhorse
- Class A hardware vs water-only on the first sortie

## What we killed

| Idea | Why |
|---|---|
| Buy T50 / T25 | DJI will not get a yes from federal/state air ops; T25 tank fails the 10 gal high end |
| US-build X8 we already know | Theron picked the tailsitter + pickup rail profile |
| $49k 50 kg catapult / $19k RoadRunner | Does not buy the prove-it |
| Hover-spray like an ag drone | Full T/W < 1; dump is a flying pass |
| Spray boom | Paints a 200 m streak at pass speed |
| Section-search thermal | Gold-plates v0.1; burn boss already pointed at the pile |
| Bed catch on v0.1 | First recover is dirt |
| Wildfire / replace a crew | Foothold is next to Type 4/5 under existing air ops |

## Scale-from-here

If this sortie hits the edge and the pin is trusted, we scale trucks and sorties, not a bigger bird. The next increment is a second pickup and a spare battery pair, not a new airframe class.

## Sister docs

- `02-fire-industry-ops.md` — how crews actually work, what a burn boss will say yes to
- `03-uav-mission-airframe.md` — airframe, airspace, dump timing
- `04-cost-bom.md` — BOM and ops cost
- `05-sim-fidelity.md` — what to simulate, what not to
- `06-manufacturing-build.md` — sawhorse, rail, door, stations
- `07-prototyper-model.md` — crude model and open geometry
