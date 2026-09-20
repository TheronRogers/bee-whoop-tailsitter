# 05 — Sim fidelity (Robotics Simulation Expert)

**Owner:** Robotics Simulation Expert  
**Date:** 2026-08-21  
**Status:** Fidelity gates for v0.1. Not a vehicle spec. Airframe and BOM live in the other docs.

Get the required fidelity of the robotics mission for the current stage. Industry-standard numbers, shop tests before we cut metal, and no stupid mistakes with hardware. This doc is what to simulate and what not to.

## Required v0.1 fidelity

v0.1 is **rail → airplane pass → dump → hover-empty → dirt land**. It is not a wildfire and it is not a T50 hover-spray.

A stock Agras T50 will dump 10 gal, but the kit is a 4–11 m farm swath at 3 m AGL, ~7 min hover full, and the binoculars/radar go stupid in smoke. That is the wrong movie. We do not need a wildfire CFD, a plume model, or an ag-spray digital twin.

The prove-it fidelity is:

1. Rail imparts **airspeed** in airplane mode (not a vertical tip-off).
2. One pass puts the load on a short edge, not a 200 m streak.
3. After the door, T/W is enough to hover, drop the pin, and land on dirt next to the truck.
4. Thermal and pin share one RTK frame (surveyed lever arm), or the burn boss walks to a cold spot.

If those four close on the ground and in a short sim, we have a prototype. If we miss the edge or the pin, we stay on the sawhorse.

## T/W: empty ≥ 1.5, full < 1

| Condition | T/W | Why |
|---|---|---|
| Empty (~30 kg class, tank dry) | **≥ 1.5** | Hover for pin and dirt RTL. Two-rotor tailsitter needs leftover thrust for attitude, not just weight. |
| Full (10 gal / ~68 kg class) | **< 1** | We cannot hover the wet bird. That is the point of the rail. |

Motors sized for empty hover, not AUW. Sizing for 68 kg hover is an X8 / Alta problem we already left.

1.5 empty on 30 kg is ~45 kgf (22.5 kgf/side). At 68 kg that is T/W ~0.66. Enough to help on the rail. Not enough to climb off a vertical rail or sit over a pile wet.

## Why the rail must throw in airplane mode

Two rotors that cannot hover 40 L also cannot climb a vertical rail. A vertical tip-off still needs T/W > 1 at AUW, or a real catapult (the $49k class we killed).

A shop trolley on a **parked** truck does not get 68 kg to flying speed either. V² = 2as: 20 m/s off 3.5 m is ~6 g. That is not a weld-this-month rail.

So the rail is an **airplane-mode throw** (or a rolling-truck hold-down that releases at stall + margin). Airspeed off the shoe, then the wing flies. No tip-off. No bed catch on v0.1.

If later mass shrinks until wet T/W > 1, this gate changes. Until then, do not simulate a hover-takeoff of a full tank.

## Dump-door timing vs a 200 m streak

An ag pump (16–24 L/min) at 15–20 m/s paints on the order of a **kilometer**. A tank bung (1–2 in) still takes ~15 s for 10 gal → hundreds of meters.

A 0.5–1 s dump at 15–20 m/s is a **25–66 ft** wet line, not an 8–20 ft edge. The door has to be a **belly / gravity door** (bomb-bay class opening, ~0.08 m²), not a spray boom and not a bung.

| Pass | Door time | Wet line |
|---|---|---|
| 16 m/s | 1 s | ~16 m (toy streak) |
| 16 m/s | 0.35 s | ~18 ft |
| 22 m/s | 0.35 s | ~25 ft |

Western DA (5000–7000 ft) also kills a “15–20 m/s pass” on a skinny wing: that is stall. Either grow area / flaps / blown lift, or raise pass speed, or stop pretending it is an airplane pass.

**Do not simulate a boom.** Simulate a dump door, dump time, pass speed, and the streak that product implies.

## CG walk / two-rotor + elevon

Door and rail shoe sit on the **same station** (tank centroid / ~25% chord) so the full-vs-empty CG stays inside two-rotor + elevon control.

The failure is the **transient**, not the two photos. If the tank drains nose-first or tail-first, CG walks *during* the one-second dump. That is a departure at 8 m AGL.

Baffles, station, and a hose test of the walk as it drains. If it walks off 25% mid-dump, move the shoe before anyone welds.

Two-rotor yaw in hover is weak (elevons in wash). After the door the bird is light and twitchy. Sim the dump transient and the empty hover, not a pretty cruise.

## Hose-and-scale before weld

This week’s fidelity, not a sim:

- Sawhorse, hose, scale.
- Measure CG **as it drains**, not full vs empty snapshots.
- Lock shoe station to that walk.
- Then weld the belly trolley.

A rail on the wrong station is the way we blow the shop kit. Do not run a 6-DOF rail model until the hose says the shoe is on the tank.

## First hover-land is dirt, not a bed catch

Empty hover next to the truck, on dirt. A bed catch is a carrier landing we do not learn on sortie one. Sim RTL to a dirt patch. Do not sim a rail recapture.

Hard deck 8 m on the pass. Smoke kills binoculars/radar; hard deck and an upwind RTL, not hope.

## What not to simulate

| Skip | Why |
|---|---|
| Wildfire CFD / crown fire / coupled fire-atmosphere | Wrong mission. Leftover pile / prescribed heat. |
| T50 / ag hover-spray twin | Wrong vehicle and wrong swath. |
| Vertical rail / tip-off / hover-takeoff full | T/W full < 1. Physics does not close. |
| $49k catapult energy model | We are not buying one. |
| Bed-catch / truck-deck landing | v0.1 recover is dirt. |
| Spray boom / droplet spectra / GPA | Door is a dump, not a nozzle. |
| Section-search thermal / mapping | Burn boss already pointed at the pile. Lever arm and pin frame only. |
| Autonomy / lost-link novels | One human on the radio. |
| Nth-degree airfoil CFD before the sawhorse | Hose-and-scale first. |

## What to simulate (short list)

1. **Rail exit:** V vs stall at AUW, western DA, shoe length, rolling vs parked energy.
2. **Dump transient:** mass walk, moment, time-to-empty, streak vs edge.
3. **Empty hover:** T/W 1.5, two-rotor + elevon, pin drop, dirt RTL.
4. **Lever arm:** thermal pixel → RTK → pin, one frame, painted dirt line.

Ground truth beats the sim: hose-and-scale, painted line, then one instrumented pass.

## After the first lock (do not mix into the rail-pass card)

Fire later signed leftover mop-up, ~2 gal, Part 107 wet, and a **3–4 m/s tilt-crawl** (not the 16 m/s airplane pass). That set has its own gates:

- Wet T/W **≥ 1.3** at 7000 ft if we crawl; 1.04 sinks in a hot column.
- **Tail / feet door** in hover attitude (cruise belly paints a wall).
- Crossing, not a sit. 8 m **over the crown**, ~6 m lead (throw + half streak). 2 m lead is a miss.
- 1 m is **aim** (centroid in the middle third of a ~4 m patch), not patch width.
- Stream door, sky-eye predicted impact with wind.

Do not run one sim that is both “68 kg rail-pass” and “25 kg hover-crawl.” Pick the card, then sim that card.
