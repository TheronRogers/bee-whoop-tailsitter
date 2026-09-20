# Manufacturing build

Shop notes only. How we cut and weld the US/NDAA tailsitter without inventing a tank.

## What we locked in the prove-it room (2026-08-14)

UAV Mission Designer locked the first envelope at **2.8 m span, 30 kg empty / 68 kg AUW** with 10 gal in a bought 40 L tank. Door and rail shoe share one station: **tank centroid / 25% chord**, so the CG walk stays inside two-rotor + elevon.

That is the manufacturing datum from the room. It is not what we cut first anymore (see Current first cut).

## Build sequence

1. **This week: sawhorse, hose, scale.** Fill the bought tank, open the gravity door, log scale + CG every few liters as it drains. Transient walk, not two static shots. If CG walks off 25% chord mid-dump, move the shoe pocket **before** anyone cuts foam or welds a trolley.
2. **Then weld the rail.** Belly-trolley (later TE/feet shoe if the door moved) on extrusion. Airplane-mode throw off the truck. No tailsitter tip-off.
3. **Then cut the plank.** Foam-core carbon-spar. Shoe pocket and door sit on the station the walk just proved.
4. **First hover-land is dirt next to the truck.** No bed catch on v0.1.

Do not weld a 68 kg trolley until the walk says the shoe is on the tank station. The way we blow the kit is a rail on the wrong station.

## What we do not fab

- **No tip-off.** Two rotors sized for empty hover cannot climb a vertical rail. The rail throws it in airplane mode.
- **No bed catch.** First recovery is dirt RTL next to the truck.
- **No spray boom.** A boom at pass speed paints a streak. Dump is a **servo gravity door on a bought tank**.
- **No invented tank.** Buy a poly can. Cut a door in it. Do not tool a custom bladder or a DJI spray kit.
- **No bought catapult.** Shop-welded extrusion + trolley. Pickup provides energy (roll) or a short parked shoe if Robotics signs the throw. Do not buy a $49k 50 kg pneumatic.

## Door and shoe

Same station: tank centroid / 25% chord.

- Door: $50-class servo, gravity dump, not a bung and not a boom. 10 gal will not leave a tank bung in one second.
- Shoe: belly trolley under that station so dump and launch load share the same hard point.
- Motors and gear are sized for **empty hover only** (30 kg class on the room bird). Full AUW does not hover; the rail takes takeoff.

If the door later moves to the trailing-edge / feet (Part 107 crawl), re-run the sawhorse walk and move the shoe with it. Do not weld the old belly station on a new door.

## How we fab US/NDAA without inventing a tank

We build the airframe and the rail. We buy the wet parts.

| Line | Source | Notes |
| --- | --- | --- |
| Wing / structure | We cut | Foam-core, carbon spar, no production composite tool |
| Rail + trolley + truck rack | We weld | Extrusion, belly (or TE) shoe, headache-rack mount |
| Tank | Buy | 40 L poly for the 10 gal envelope; ~8 L poly for the Part 107 dropper |
| Door | Buy + cut | Servo + gravity flap on the bought can |
| Motors | Buy US-path | KDE-class, sized for empty hover |
| Autopilot / radio | Buy NDAA | Cube + Doodle Labs (that is the NDAA tax) |
| Thermal / pin | Buy | Fixed FLIR brick if it is on this airframe; DDM pin is noise. Sky-eye is a different airplane on the later lock |

A bought T50 is a dead end: federal and most state fire will not put DJI next to air ops. Alta X NDAA fails the 5–10 gal lift. We do not buy a wildfire platform.

## Current first cut

After 2026-08-15 the shop moved. **Do not cut the 2.8 m / 10 gal plank first.**

First thing we fab is the **Part 107 dropper**:

- 1.7 m span × 1.4 m (spinner to tail pads), 0.82/0.45 taper, 1.08 m², slotted flap, no canards
- Theron’s BWB plank: two LE tractors blowing the wing, tank in the root
- Empty ≤17.3 kg, wet ≤24.9 kg, 1.5–2 gal Class A dense slug in an **~8 L bought poly**
- Door and shoe still share the tank station; door is now TE/feet stream, not a belly boom
- Rail: ≤2.5 m shoe on a **parked** pickup, 12 m/s exit (truck does not roll on this cut)
- Two LE tractors sized for ~17 kg hover
- No FLIR on this airframe; sky-eye is separate
- Same sequence: sawhorse walk (2 gal now), then weld shoe, then cut foam

The 2.8 m / 30/68 kg / 40 L bird is the old prove-it envelope, not the first shop cut. Same method, smaller can.

## Still open (shop)

- **Tank SKU.** Pick a real US poly can (~8 L first, 40 L only if we revive the big envelope). Do not invent one.
- **Thrower.** Winch vs sling vs bungee on the ≤2.5 m parked shoe is unpicked. Rolling-truck guide was the room fallback for 68 kg @ 20 m/s; that energy problem goes away on the 24.9 kg cut.
- **Sawhorse walk has not been run.** That is still this week’s only BOM line that matters.
- **Door station.** Belly (room) vs TE/feet (later crawl lock). Walk whichever door we cut; weld after.

## Production vs proto

v0.1 / first-cut is one-off foam and a shop rail on a pickup we already own. Do not tool production composites, a bed catch, or a Blue-listed airframe until the walk and one dirt hover-land work. Spare battery pair stays an ops line, not a structure line.
