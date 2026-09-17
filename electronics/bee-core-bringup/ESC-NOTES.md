# ESC notes — single-channel whoop-style (EFM8BB21)

> **LOCKED decision (2026-09-15 MT):** see `bee-core-v01/ESC-TOPOLOGY-DECISION.md` — **GO = Bluejay Layout O + IRLML2244/6244 P/N, EFM8 VDD=VBAT (1S)**; Layout A + 3V3→AO3401 is NO-GO.

**Do not invent pinouts.** Pin maps below are cited from Bluejay layout sources.
Choose one Bluejay **layout letter** before committing schematic nets to the EFM8.

## Goal for Bee Core v0.1

One brushless channel on the same PCB as RP2350A:

- MCU: **EFM8BB21** (LCSC **C80713**, QFN-20) running **Bluejay** (BLHeli_S successor)
- Input: **DShot** from RP2350 GPIO
- Output: 3-phase motor (A/B/C)
- Power: **VBAT** + **GND** with local bulk capacitance
- Style: whoop-class **direct GPIO → FET bridge** (no gate-driver IC) for 1S/low voltage

## Topology overview

### A) Whoop 1S/2S direct-drive (preferred reference for “whoop-style”)

Source: [OpenDrone-hw/OpenAIO-Whoop](https://github.com/OpenDrone-hw/OpenAIO-Whoop) README —

> ESC runs Bluejay on EFM8BB51 with **GPIO direct drive: no gate-driver IC**,
> so the power stage is a **complementary P+N pair per phase**.

Per motor channel (here: **one** channel):

| Item | Role |
|------|------|
| 3 × high-side P-FET | Phase A/B/C to VBAT |
| 3 × low-side N-FET | Phase A/B/C to GND |
| EFM8 GPIO | Drive FET gates (layout-defined active levels) |
| Comparator inputs | Sense BEMF on phases + virtual neutral |
| DShot RX pin | Single-wire command (+ optional bidirectional telemetry) |
| Bulk caps | Across VBAT–GND at FET cluster |

**Key nets (logical):**

```
RP2350 DShot GPIO  ---->  EFM8 RTX / RX (signal)
VBAT  ----+----  bulk C  ----+----  P-FET drains (phases via FETs)
GND   ----+----  bulk C  ----+----  N-FET sources
Phase A / B / C  ---->  motor connector
EFM8 3V3 (from board 3V3 or onboard LDO) + GND
```

OpenAIO-Whoop notes 2S may need **level shift** so P-FETs turn fully off — for Bee Core
start with **1S / USB-bench VBAT ≤ ~4.2 V** unless level-shift is designed in.

### B) Higher-voltage / module ESC (alternate, not default)

Source: OSHWHub [EFM8-ESC](https://oshwhub.com/tomiaaa/EFM8-ESC) (EFM8BB21F16G + **FD6288Q**
three-phase half-bridge driver) and commercial AIO (e.g. iFlight BLITZ Whoop F7 AIO:
BB21 + FD6288). Uses gate-driver IC between MCU and FETs. Better for multi-S;
**not** the pure whoop direct-drive topology. Author warns: **add bus filter caps
or FETs fail.**

## Bluejay / firmware constraints (cited)

Sources:

- [bird-sanctuary/bluejay](https://github.com/bird-sanctuary/bluejay)
- Layout A: [Layouts/A.inc](https://raw.githubusercontent.com/mathiasvr/bluejay/main/Layouts/A.inc)
- Analysis: [BLUEJAY_ESC_ANALYSIS.md](https://github.com/tcmichals/rt-fc-offloader/blob/main/docs/BLUEJAY_ESC_ANALYSIS.md)

- Targets: EFM8 **BB21** / **BB51**
- Input: **DShot only** (300/600); bidirectional DShot / EDT optional
- Bootloader: BLHeli serial on the **same signal wire** (hold line high ~150 ms at power-up)
- Many **layout letters** (A–Z…); each remaps ports — **pick one and stick to it**

### Layout A pin roles (BB21) — documentation default only

From Bluejay `Layouts/A.inc` and analysis summary:

| Port bit | Symbol | Role |
|----------|--------|------|
| P0.0 | Vn / V_Mux | Comparator virtual neutral |
| P0.1 | Am / A_Mux | Phase A BEMF sense |
| P0.2 | Bm / B_Mux | Phase B BEMF sense |
| P0.3 | Cm / C_Mux | Phase C BEMF sense |
| P0.5 | RTX / RX | DShot signal |
| P1.0 | Ap / A_Pwm | Phase A PWM FET gate |
| P1.1 | Ac / A_Com | Phase A complementary FET gate |
| P1.2 | Bp / B_Pwm | Phase B PWM FET gate |
| P1.3 | Bc / B_Com | Phase B complementary FET gate |
| P1.4 | Cp / C_Pwm | Phase C PWM FET gate |
| P1.5 | Cc / C_Com | Phase C complementary FET gate |

Layout A flags (from source): PWM active high, COM active high, PWM side **high**, 0 LEDs.

**Warning:** Other commercial whoops may use Layout G/H/Q/etc. Flashing the wrong
layout letter will short phases. Silk the layout letter next to the EFM8.

## Capacitors / grounding (mandatory practice)

- Local **bulk** on VBAT at the FET bridge (electrolytic + ceramics). OSHWHub EFM8-ESC
  explicitly: missing bus caps → destroyed FETs.
- Star/return GND: ESC power GND vs RP2350 digital GND with careful join (single point
  or ferrite) so IMU SPI is not sitting on motor return current.
- 4-layer recommended: inner GND plane; keep phase pours short and fat.

## Integration with RP2350

| Net | Connection |
|-----|------------|
| DShot | RP2350 GPIO → series resistor (~100–330 Ω typical practice) → EFM8 RX |
| ESC 3V3 | Share board 3V3 **or** power from VBAT via EFM8 internal path per datasheet — do not float |
| Flash | Via BLHeli passthrough from FC GPIO or dedicated USB–serial jig on signal wire |
| Motor | 3 pads/connector; no shared connector with servo 5V |

## Candidate discrete FETs (not a proven Bee schematic)

| Role | Example LCSC | Notes |
|------|--------------|-------|
| N-ch | AO3400A **C20917** | Common SOT-23 N |
| P-ch | AO3401 **C5296722** | Common SOT-23 P; verify Vgs for 1S gate drive from 3.3 V MCU |

Final FET choice needs Rdson / current / package thermal review for the intended motor.

## Recommended next hardware decisions

1. Lock **1S direct-drive** vs **FD6288** path.
2. Lock Bluejay **layout letter** (start with **A** only if we draw to A.inc).
3. Place ESC copper + caps before IMU; keep IMU on quiet corner.
4. Add silkscreen: `BLUEJAY LAYOUT _` and `VBAT MAX _S`.
