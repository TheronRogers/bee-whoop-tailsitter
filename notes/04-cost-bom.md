# 04 — Cost / BOM

**Owner:** Cost Watcher  
**Date:** 2026-08-21  
**Status:** Room BOM plus Part 107 first-cut paper. Hardware SKUs still open.

Why T50 is the envelope not the cart, what we killed, what a US-build tailsitter actually costs, Part 107 first-cut vs the 10 gal bird, and how we make this expensive. Airframe geometry lives in `03`; shop sequence in `06`.

Locked geometry we priced in the room (UAV Mission Designer): 2.8 m span tailsitter, 30 kg empty / 68 kg AUW with 10 gal in a bought 40 L tank, two rotors, gravity dump door (not a spray boom), rail-launch in airplane mode, hover/pin/dirt RTL only after the door.

Shop first cut (Manufacturing, after 2026-08-15): do **not** cut that 2.8 m / 10 gal plank first. First fab is a Part 107 dropper — empty ≤17.3 kg, wet ≤24.9 kg, 1.5–2 gal in an ~8 L bought poly — so we stay under 55 lb.

## T50 is the envelope, not the cart

A stock DJI Agras T50 is the right *size*: 40 L tank (10.6 gal) hits the 5–10 gal prove-it, tank and pump already exist, RTF kit ~$25k. That is why we kept it as the payload/endurance box.

We do not buy one. Theron builds drones. Federal and most state fire will not put DJI over a pile next to their air ops. A $25k Shenzhen bird a burn boss cannot say yes to is the expensive path — we pay once and still have no foothold.

## Killed options

| Option | Why it's dead |
| --- | --- |
| **DJI Agras T25** | ~$8k cheaper than T50, but the tank tops out at 20 L / 5.3 gal. Fails the high end of 5–10 gal. |
| **Buy T50** | Right envelope, wrong country of origin. Dead end for the foothold. |
| **Freefly Alta X NDAA** | US/NDAA, ~$46k, only lifts ~35 lb. 10 gal of water is ~83 lb. Fails the prove-it. |
| **Harris Aerial H6HL** | US, 40 kg class, quote-only industrial. Don't buy a monumental lift bird for a one-pass prove-it. |
| **Draganfly Heavy Lift** | $55k starting, 66 lb hook. Wrong architecture and too much money. |
| **Bought 50 kg catapult** (e.g. Naja H-50A ~$49k) | Two rotors that cannot hover 40 L also cannot climb a vertical rail. We need a shop-welded belly trolley that *throws* it in airplane mode, not a military pneumatic. |
| **Bought truck tender** (RoadRunner ~$12.5–19k) | Ag hover-spray refill deck. Wrong mission. v0.1 truck is a tote and a rail mount. |

## US-build tailsitter + shop rail + truck tote

Working number for the **10 gal / 68 kg envelope** on a pickup we already own: **~$16–26k**.

| Line | Estimate | Notes |
| --- | --- | --- |
| Two-rotor tailsitter airframe (US-path) | $10–15k | KDE-class lift, Cube, Doodle Labs radio (~$3–4k is the NDAA tax), composite wing/structure we fab. Motors sized for 30 kg empty hover (T/W ≥ 1.5), not 68 kg. |
| Shop-welded belly-trolley rail + cradle | $3–5k | Throws ~68 kg to 15–20 m/s in airplane mode. Not a $49k catapult. |
| Truck mods | $2–4k | Bed rack, 50–100 gal tote, 12 V fill pump. No bed catch on v0.1 (dirt RTL next to the truck). |
| Gravity door + FLIR-confirm + pin | inside airframe / ~$1–2k | Door is a $50 servo, not a boom. Thermal is a fixed brick to confirm a pointed-at pile, not a search gimbal. Pin is noise. |

After AUW/door/FLIR locked, the same kit can land closer to **$12–20k** if we stay shop-built and do not upsize motors for a full hover.

Do not invent a tank. Buy a 40 L tank, fly 10 gal, dump with a servo gravity door.

## Part 107 first-cut cost

Part 107 small UAS is **< 55 lb at takeoff**. The 68 kg (150 lb) envelope is not Part 107. That is why the shop crawled to a 24.9 kg wet dropper first.

**Paper (first cut, stays under 55 lb):**

| Line | Cost | Notes |
| --- | --- | --- |
| Part 107 knowledge test (UAG) | $175 | One attempt, PSI. IACRA + TSA + certificate card are $0. Recurrent training every 24 months is free. |
| Aircraft registration (Part 48) | $5 | Per aircraft, 3 years. |
| Optional study course | $0–300 | Free FAA guide works. Budget ~$180–500 all-in for one PIC + one bird. |

That is the whole first-cut regulatory line. Do not buy a waiver mill for a VLOS daytime pile next to a crew.

**Paper we do *not* buy on the first cut:**

- **Section 44807** (required for the 68 kg / 10 gal bird): FAA filing is $0. Time is the cost — a new make/model that is not already on the 44807 list is often **1–1.5 years**. A consultant packager is ~$2.5–4.5k and does not buy the calendar. Stay under 55 lb until the sawhorse and one dirt hover-land work.
- **Part 137** agricultural certificate: for pesticide/spray-for-hire, not a prescribed-pile water/Class A prove-it. Later, if ever.
- **Blue UAS listing:** later-phase cost. Not this sortie.

**First-cut hardware** (scaled from the room BOM, not a new quote): smaller plank, motors sized for ~17 kg hover, ≤2.5 m parked shoe at 12 m/s, ~8 L poly, no FLIR on this airframe.

| Line | Estimate | Notes |
| --- | --- | --- |
| Part 107 dropper airframe | $6–10k | Same US-path stack (KDE-class, Cube, Doodle Labs), smaller wing and motors. |
| Parked shoe / short rail | $1.5–3k | 24.9 kg @ 12 m/s is ~1.8 kJ, not the 11 kJ 68 kg throw. |
| Truck rack + small tote + fill | $1.5–3k | Still a tote, not a RoadRunner. |
| Part 107 paper | $180–500 | Exam + registration + optional study. |
| **First-cut kit** | **~$10–16k** | Plus the $180–500 paper. Pickup already owned. |

The 10 gal envelope stays the scale target. It is not the first shop cut, and it is not a $175 piece of paper.

## Ops cost

The standing ops line is a **spare battery pair**, not eight hover motors and not a tender farm. Profile is the cheap part: rail-launch full, one pass, hover only after the tank is light. Batteries and props take the abuse.

This week's only spend that matters: sawhorse, hose, and scale to walk the CG on the dump — **~$200**. Do not weld the rail until that walk says the shoe is on the tank station.

## What makes this the expensive path

1. **A rail we cannot weld this month.** If the trolley is a vendor lead time, the tailsitter just became more expensive than the X8 we killed.
2. **Welding the trolley to the wrong station.** Wrong shoe = scrap rail + scrap airframe time. Hose-and-scale first.
3. **Buying the envelope** (T50, Harris, catapult, RoadRunner) instead of fabbing the boring two-rotor + shop rail + tote.
4. **Paying for full-hover thrust, a search gimbal, or 44807/Blue** this phase does not use.
5. **Cutting the 68 kg plank first** and then waiting a year for 44807. That is how a $16–26k kit becomes a $20k kit that cannot legally fly the prove-it.

Max impact at this phase: Part 107 paper (~$180), lift we already know how to make, a NDAA radio, a rail we weld after the sawhorse. Everything else waits.

## Sister docs

- `01-vision-driver-mission.md` — prove-it lock
- `02-fire-industry-ops.md` — what a burn boss will say yes to
- `03-uav-mission-airframe.md` — airframe, airspace, dump timing
- `05-sim-fidelity.md` — what to simulate
- `06-manufacturing-build.md` — sawhorse, rail, first-cut plank
- `07-prototyper-model.md` — crude model
