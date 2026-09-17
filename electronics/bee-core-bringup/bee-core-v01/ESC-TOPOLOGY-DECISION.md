# Bee Core v0.1 — ESC topology decision (single motor channel)

**Research / decision date:** 2026-09-15 (MT)  
**Supersedes for schematic work:** Layout-A + bare AO3401 from 3V3 GPIO (`ESC-VGS-CHECK.md` = **NO-GO**)  
**Goal:** one locked, fab-safe 1S learning ESC on the bring-up board (JLCPCB qty 5).

---

## DECISION — **GO**

**Topology:** Complementary **P high-side + N low-side**, **direct GPIO gate drive**, **Bluejay / BLHeli_S layout letter O**, with **EFM8BB21 VDD tied to VBAT (1S only)** — the proven tinyPEPPER / whoop pattern.

**Do not** keep Layout A with Ap→P / Ac→N driven from board 3V3. That is the Vgs failure already documented.

**Fallback (only if discrete ESC is deferred):** solder-pad / footprint for a proven commercial 1S single ESC module (signal / GND / VBAT / A/B/C). Prefer the integrated path above for learning; it is clearly safe when the powering rule is obeyed.

---

## Why this path (rationale)

1. **Vgs math is closed without new invention.** At 1S, P-FET source sits at VBAT. Turning the P-FET *off* requires gate ≈ VBAT (`VGS ≈ 0`). tinyPEPPER does that by powering the EFM8 from the same VBAT rail so GPIO-high ≈ VBAT. Fishpepper explicitly stated that a regulated 3.3 V EFM8 **cannot** drive the P-channel correctly on that design ([tinyPEPPER project comments](https://fishpepper.de/projects/tinypepper/)).
2. **Open, flight-proven schematic exists.** [fishpepper/tinyPEPPER](https://github.com/fishpepper/tinyPEPPER) `single_esc.sch` (v0.5 = EFM8BB21): IRLML2244 (P) + IRLML6244 (N), no gate-driver IC, firmware **`O_L_05` / Layout O**.
3. **Firmware polarity matches the FETs.** Bluejay `Layouts/O.inc`: *“Low side pwm and 1S flag set”*, `PWM_ACTIVE_HIGH = 1`, `COM_ACTIVE_HIGH = 0`, `P1_INIT` holds COM pins high (P-FET off). PWM pins drive **N** (low side); COM pins drive **P** (high side, active-low).
4. **FD6288 / bootstrap all-N is the wrong first fab for 1S.** FD6288 VCC is specified ~5–20 V (≈4.8 V min on vendor summaries) — UVLO under a 1S pack. Keep gate-driver ESCs for ≥2S later.
5. **Layout A is the wrong letter for this bridge.** Layout A is high-side PWM / COM active-high — do not flash A onto an O-style P/N stage.

---

## Schematic block (one phase shown; replicate ×3)

```
 VBAT (1S LiPo, 3.0–4.2 V) ─────────────────┬─────────────── EFM8 VDD
        │                                    │
        │                              +3V3 board rail is NOT EFM8 VDD
        │
        ├──── bulk C (47–100 µF) + 100 nF ───┤
        │                                    │
        │         ┌──── IRLML2244 (P) ────┐  │
        └─────────┤ S                  D ├──── PHASE_x ──── motor
                  │ G                    │
                  └───[0–47 Ω]───────────┘
                         ▲
                         │  EFM8 Ac/Bc/Cc  (COM, active LOW = P ON)
                         │
                  ┌──── IRLML6244 (N) ────┐
   PHASE_x ───────┤ D                  S ├──── GND
                  │ G                    │
                  └───[0–47 Ω]───────────┘
                         ▲
                         │  EFM8 Ap/Bp/Cp  (PWM, active HIGH = N ON)

 BEMF (copy tinyPEPPER):
   PHASE_A/B/C ── 1 kΩ ──► star ──► Vn (Layout O: P0.3)
   PHASE_A/B/C ── 10 kΩ ─► Am / Bm / Cm (Layout O mux: see pin table)
   (Replicate `single_esc.sch` sense wiring; do not invent a new divider.)

 DShot:
   RP2350 GPIO14 ── 220 Ω ──► EFM8 P0.5 (RTX)
   Optional Schottky anode@signal / cathode@EFM8_VDD clamp if VBAT can sit < ~3.1 V
   while FC is on USB 3V3.
```

**No bootstrap capacitors. No gate-driver IC. No P-gate pull-up to VBAT into a 3V3 push-pull pin.**

---

## Bluejay / BLHeli lock

| Item | Value |
|------|--------|
| Layout letter | **O** (silk: `BLUEJAY LAYOUT O` / `VBAT MAX 1S`) |
| MCU class | BB21 → Bluejay **`O_H_*`** (H = 48 MHz BB21/BB2) |
| Recommended first hex | **`O_H_05`** (dead-time step 5; same family as tinyPEPPER’s `O_L_05` on BB10) |
| PWM side | **Low-side** (N-FETs on Ap/Bp/Cp) |
| COM polarity | **Active low** (P-FETs on Ac/Bc/Cc) |
| Dead time | Use **non-zero** firmware dead-time (5–15). Do not ship `*_00` until scoped. |

### Layout O port map (BB21 QFN-20) — replace Layout A nets

| Port | Layout O role | QFN-20 (BB2 DS) | Net |
|------|---------------|-----------------|-----|
| P0.0 | Bm | 2 | ESC_Bm |
| P0.1 | Cm | 1 | ESC_Cm |
| P0.2 | Am | 20 | ESC_Am |
| P0.3 | Vn | 19 | ESC_Vn |
| P0.5 | RTX | 17 | DShot (GPIO14 via 220 Ω) |
| P1.0 | Ap (PWM → **N**) | 14 | ESC_Ap |
| P1.1 | Ac (COM → **P**) | 13 | ESC_Ac |
| P1.2 | Bp → **N** | 11 | ESC_Bp |
| P1.3 | Bc → **P** | 10 | ESC_Bc |
| P1.4 | Cp → **N** | 9 | ESC_Cp |
| P1.5 | Cc → **P** | 8 | ESC_Cc |

Sources: [Bluejay `Layouts/O.inc`](https://raw.githubusercontent.com/mathiasvr/bluejay/main/Layouts/O.inc), [BLHeli_S `O.inc`](https://raw.githubusercontent.com/bitdump/BLHeli/master/BLHeli_S%20SiLabs/O.inc).

---

## BOM lines (single channel)

| Ref / qty | Part | LCSC (preferred) | Role / notes |
|-----------|------|------------------|--------------|
| U20 ×1 | EFM8BB21F16G-C-QFN20 | **C80713** | Bluejay target; **VDD = VBAT only** |
| Q_P ×3 | Infineon **IRLML2244TRPBF** | **C169763** | P high-side; Rdson ≤95 mΩ @ −2.5 V |
| Q_N ×3 | Infineon **IRLML6244TRPBF** | **C143946** | N low-side; tinyPEPPER twin |
| Alt P | AO3401A | C15127 | Only if Infineon P unavailable; still needs VBAT-rail MCU |
| Alt N | AO3400A | C20917 | Same caveat |
| Rg ×6 | 0 Ω or **47 Ω** 0402 | Basic | tinyPEPPER = direct (0 Ω). Prefer **47 Ω** on bring-up for ringing control; do not use >100 Ω without re-check |
| Rsense ×3 | **1 kΩ** 0402 | Basic | Phase → Vn star |
| Rsense ×3 | **10 kΩ** 0402 | Basic | Per tinyPEPPER mux/GND network |
| Rdshot ×1 | **220 Ω** 0402 | Basic | RP2350 → EFM8 RTX |
| Cbulk ×1+ | **47–100 µF** ≥6.3 V (0805 ceramic OK as on tinyPEPPER, or electrolytic) | — | At FET cluster VBAT–GND |
| Cdec ×1+ | **100 nF** | Basic | Next to EFM8 VDD and at bridge |
| — | Schottky SOD-323 (optional) | Basic | DShot clamp to EFM8 VDD |
| — | VBAT pad + polyfuse (DNP OK) | — | Motor power only when ready |

**Gate / level-shift / bootstrap parts:** none for this topology.

Avoid clone “IRLML*” listings when Infineon C143946 / C169763 are in stock (fishpepper: counterfeit FETs had bad Rdson).

---

## Powering rules (non-negotiable)

1. **EFM8 VDD = VBAT (1S).** Never power EFM8 from the board 3V3 LDO while P-FET sources sit on VBAT.
2. **1S only.** No 2S, no HV LiPo charged above **4.2 V**. EFM8 absolute max is 4.2 V (same caveat tinyPEPPER documents). Prefer charge-to-4.2 storage discipline.
3. **USB bring-up without battery:** ESC MCU is unpowered; that is OK. Motor tests only after VBAT is present and scoped.
4. **RP2350 stays on 3V3.** DShot is the only intentional cross-rail signal — series R mandatory.

---

## What NOT to do

| Don’t | Why |
|-------|-----|
| Layout **A** + Ap→P / Ac→N from **3V3** GPIO | `VGS ≈ 3.3 − 4.2 = −0.9 V` — not a guaranteed P off (`ESC-VGS-CHECK.md`) |
| EFM8 on 3V3 + P-FET gates direct to GPIO | Same failure; fishpepper confirmed |
| Pull-up P gates to VBAT into push-pull 3V3 pins | Injects current into MCU ESD |
| FD6288 / MP1907 on 1S without a ≥5 V driver rail | Driver UVLO / wrong class for this board |
| Flash `A_H_*` onto this pinout | Shoot-through / wrong polarity |
| Skip VBAT bulk at the bridge | Known FET death mode on discrete ESCs |
| 2S “just to try” | Destroys EFM8 and breaks P-FET off |

---

## Pragmatic module fallback (if discrete deferred)

Add a **DNP** footprint / solder-pad island:

- Pads: `ESC_SIG`, `GND`, `VBAT`, `MOT_A`, `MOT_B`, `MOT_C`
- Keep RP2350 DShot + series R to `ESC_SIG`
- Mount a known-good 1S BLHeli_S/Bluejay brick (donor whoop ESC channel or tiny 1S ESC)

Use only if schedule forces shipping without the discrete bridge; the tinyPEPPER-derived path above is preferred and safe.

---

## Bring-up gate (before motor)

1. Silk and firmware both say **LAYOUT O**.
2. Scope Ac gate vs VBAT at **3.0 / 3.7 / 4.2 V**: commanded-off P has `VGS ≈ 0`; commanded-on has `|VGS| ≥ ~2.5 V`.
3. Confirm dead time between N and P on one phase.
4. Then connect a small whoop motor; watch FET and EFM8 temperature.

---

## Sources

1. fishpepper, **tinyPEPPER** (1S, EFM8BB21 v0.5, IRLML2244/6244, Layout O): https://fishpepper.de/projects/tinypepper/ — https://github.com/fishpepper/tinyPEPPER — `single_esc.sch`
2. fishpepper comment: regulated 3.3 V EFM8 cannot drive the P-FET on that design: https://fishpepper.de/projects/tinypepper/
3. Bluejay **Layouts/O.inc** (low-side PWM, COM active low, 1S): https://raw.githubusercontent.com/mathiasvr/bluejay/main/Layouts/O.inc
4. BLHeli_S **O.inc** (historical low-side PWM / active-low COM): https://raw.githubusercontent.com/bitdump/BLHeli/master/BLHeli_S%20SiLabs/O.inc
5. Infineon **IRLML2244** DS (Rdson 95 mΩ max @ −2.5 V): https://www.infineon.com/dgdl/irlml2244pbf.pdf?fileId=5546d462533600a401535668e1d52685
6. LCSC **C169763** IRLML2244TRPBF / **C143946** IRLML6244TRPBF
7. Fortior **FD6288** (VCC ~5–20 V — not for naked 1S): https://www.fortiortech.com/en/product/hvic/hvic/fd6288
8. Bee Core prior NO-GO: `bee-core-v01/ESC-VGS-CHECK.md`
9. OpenAIO-Whoop (topology intent only; board not built): https://github.com/OpenDrone-hw/OpenAIO-Whoop
10. HAKRC HK1S teardown (1S P/N direct drive precedent): https://electronics.stackexchange.com/questions/484001/hakrc-hk1s-esc-fet-identification
