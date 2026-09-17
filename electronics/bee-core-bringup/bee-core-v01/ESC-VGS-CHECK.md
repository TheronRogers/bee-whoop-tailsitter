# Bee Core v0.1 ESC VGS check

**Research snapshot:** 2026-09-15 (MT)  
**Scope:** 1S LiPo, approximately 3.0–4.2 V VBAT, EFM8BB21 at approximately 3.3 V, Bluejay Layout A, complementary P/N whoop-style phase FETs.

## Executive recommendation

### **NO-GO — as currently described: Layout A + bare EFM8 GPIO directly on AO3401 P gates**

The GPIO can turn the AO3401 on, but it cannot guarantee that the P-FET is off at a charged 1S cell. With the P-FET source at VBAT and an EFM8 high output near 3.3 V, the high-side gate sees `VGS = 3.3 - VBAT`: 0.3 V at 3.0 V VBAT, 0 V at 3.3 V, and **-0.9 V at 4.2 V**. The AO3401 threshold is typically -0.9 V and can be as high as -1.3 V in the AOS datasheet; threshold is specified at only -250 uA and is not a fully-off or fully-on guarantee. At the EFM8BB21's guaranteed VOH minimum (`VDD - 0.7 V`, i.e. 2.6 V at 3.3 V under the specified source current), the worst-case charged-cell value is `VGS = -1.6 V`, clearly not an off condition.

**GO path:** retain a complementary P/N 1S stage, but do not call it Layout-A direct drive until the firmware/polarity and gate network are corrected and bench-proven. Either (a) use the 1S low-side-PWM/active-low-P-FET arrangement represented by legacy BLHeli O / an explicitly matched Bluejay layout, with source-referenced P-gate pull-ups and a safe open-drain/NMOS/NPN pull-down, or (b) keep Layout A only with a gate-driver/inverter topology that makes its high-side gate polarity and off-state unambiguous. An all-N high-side stage with bootstrap/charge-pump drive is a valid higher-voltage architecture, but is not the preferred minimal 1S bring-up solution.

## Electrical facts

### AO3401/AOS AO3401A (P-channel high side)

The official AOS AO3401 data sheet specifies:

- `VDS = -30 V`, `VGS = +/-12 V`.
- `VGS(th) = -0.5 V typ -0.9 V max -1.3 V`, measured at `VDS = VGS`, `ID = -250 uA`.
- `RDS(on) = 41 mOhm typ / 50 mOhm max` at `VGS = -10 V`, `ID = -4 A`.
- `RDS(on) = 47 mOhm typ / 60 mOhm max` at `VGS = -4.5 V`, `ID = -3.7 A`.
- `RDS(on) = 60 mOhm typ / 85 mOhm max` at `VGS = -2.5 V`, `ID = -2 A`.
- `Qg = 7 nC` at 4.5 V (14 nC at 10 V in the dynamic table).

The corresponding AOS LCSC listing is **C15127 (AO3401A)** and repeats the 30 V P-channel, SOT-23, 900 mV typical threshold and 85 mOhm maximum at -2.5 V. The “2.5 V operation” wording means characterized low-RDS operation with approximately 2.5 V *across gate and source*; it does not mean a 3.3 V gate-to-ground signal can turn off a source sitting at 4.2 V.

### AO3400A (N-channel low side)

The official AOS AO3400A data sheet specifies:

- `VDS = 30 V`, `VGS = +/-12 V`, nominal 5.7 A at 25 C under the data-sheet thermal conditions.
- `VGS(th) = 0.65 V typ to 1.45 V max`, measured at `ID = 250 uA`.
- `RDS(on) < 48 mOhm` at `VGS = 2.5 V`, `ID = 3 A`; `<32 mOhm` at 4.5 V.
- `Qg` approximately 7 nC at the 4.5 V test condition.

Therefore AO3400A is a reasonable 3.3 V-driven *low-side* candidate, subject to phase-current, copper, temperature, and pulse/SOA review. It does not solve the P-FET high-side off problem. The AOS LCSC listing is **C20917**.

### EFM8BB21 GPIO

Silicon Labs' EFM8BB2 data sheet covers the EFM8BB21F16G-C-QFN20 and specifies 2.2–3.6 V VDD. At `VDD >= 3.0 V`, high-drive GPIO `VOH >= VDD - 0.7 V` at `IOH = -7 mA` (low-drive is `VDD - 0.7 V` at -4.75 mA); the typical unloaded output will usually be closer to VDD. This is enough for the AO3400A gate at low-side `VGS` around 3.3 V, but it is not a source-referenced 4.2 V output for an AO3401 gate.

Do not use an EFM8 push-pull output with a gate pull-up to VBAT as a substitute for a level shifter: when VBAT exceeds VDD, the pull-up can force current into the MCU output/ESD structures. Use a source-to-gate pull-up and a correctly rated small NMOS/NPN pull-down/open-drain arrangement, with gate resistors and firmware polarity matched to the resulting logic.

## What “threshold” does and does not mean

`VGS(th)` is the point where a small test current starts to flow. It is not a guaranteed low-loss on-state and it is not a guaranteed off-state boundary at motor current. Use the data sheet's `RDS(on)` test points and gate-charge curves instead; this is especially important near 1–2 V, where resistance and device-to-device/temperature spread increase quickly.

For AO3401 with a direct GPIO gate, **ON** is the easy direction: GPIO low gives `VGS = -3.0 to -4.2 V`, enough to reach the -2.5 V characterized point. **OFF** is the failure direction at full charge: GPIO high near 3.3 V gives `VGS = -0.9 V` at 4.2 V, close to/inside the threshold range; it can conduct and can create shoot-through when the complementary N-FET is on. This must not be waved away as “threshold is only typical”; the maximum/temperature and GPIO VOH cases are precisely why it is not a production guarantee.

## Real 1S whoop precedent and what it proves

- The **HAKRC HK1S** teardown documents an EFM8BB1-controlled 1S board with three devices marked `SP1 645` and three marked `AKW 3FAB`, directly connected to battery, phase, and EFM8 pins. The author identifies `SP1 645` as probably Toshiba **SSM6J501NU** (P-channel) and the other marking as the complementary N-channel, but the N part is not confirmed. The board is marked 1S; the teardown notes that the EFM8 absolute maximum is 4.2 V and the advertised 2S capability is incorrect. This is useful evidence that direct-drive P/N 1S hardware exists, not proof that bare AO3401 GPIO drive is robust at every battery/temperature corner.
- Toshiba **SSM6J501NU** is a much stronger P-FET electrical match for small whoop currents than AO3401: 20 V, UDFN-6, 10 A class, with LCSC **C146326** listing maximum RDS(on) of 43 mOhm at -1.5 V, 26.5 mOhm at -1.8 V, 19 mOhm at -2.5 V and 15.3 mOhm at -4.5 V. LCSC currently lists it out of stock, so treat it as a reference/alternate rather than a locked BOM item.
- Commercial BetaFPV 1S AIO pages document BB21/BB51-based 5 A and 12 A ESCs and Bluejay targets, but do not publish their individual MOSFET part numbers or gate schematics. Do not infer that their FETs are AO3401/AO3400.
- OpenDrone's **OpenAIO-Whoop** README is a topology reference, not a production-board teardown: it explicitly targets 1S and says the board does not yet exist. It describes the intended direct-drive P+N approach and separately calls out the need to resolve the gate-drive/power-stage question. It should not be cited as proof that an AO3401 direct GPIO gate is safe.

## Layout A versus a 1S P/N stage

Bluejay `Layouts/A.inc` maps `P0.0..P0.3` to Vn/Am/Bm/Cm, P0.5 to RTX, and P1.0..P1.5 to Ap/Ac/Bp/Bc/Cp/Cc. It sets `PWM_ACTIVE_HIGH = 1`, `COM_ACTIVE_HIGH = 1`, and describes the PWM side as high. This is a firmware pin/polarity definition; it is not a universal declaration that `Ap` is a P-FET gate and `Ac` is an N-FET gate.

The legacy BLHeli **O** definition is the explicit 1S mixed-FET precedent: its source comment says “Com fets are active low ... Low side pwm,” and its macros make `Ap/Bp/Cp` active-high PWM outputs (normally N-FET low-side devices) and `Ac/Bc/Cc` active-low complementary outputs (normally P-FET high-side devices). That is the natural polarity for a direct P/N pair. Therefore the current Bee notes' blanket mapping “Ap/Bp/Cp -> P gates; Ac/Bc/Cc -> N gates” must not be accepted without rechecking the exact Bluejay source/build; it is inconsistent with the documented O-style direct P/N convention and likely inconsistent with Layout A's active-high high-side PWM semantics.

**Hardware lock condition:** before PCB placement, draw one complete phase showing source/drain, gate pull-up/pull-down, gate resistor, and the exact Bluejay signal/polarity. Then verify with a scope at VBAT = 3.0, 3.3, 4.2 V that every commanded-off P-FET has `VGS` near 0 V while the complementary N-FET is driven, and that dead time is present. Do not flash Layout A onto an O-style P/N stage merely because the port names look similar.

## Preferred LCSC candidates if the topology is corrected

| Role | Preferred part | LCSC | Relevant data / caveat |
|---|---|---:|---|
| P high side, SOT-23 | AOS AO3401A | **C15127** | -30 V; 85 mOhm max at -2.5 V; 900 mV typical threshold. Best documented/basic candidate, but only after source-referenced off drive and current/thermal review. |
| N low side, SOT-23 | AOS AO3400A | **C20917** | 30 V; 48 mOhm max at 2.5 V; good 3.3 V low-side candidate. |
| P high side, lower RDS / compact | Toshiba SSM6J501NU,LF | **C146326** | 20 V UDFN-6; 19 mOhm max at -2.5 V; currently listed out of stock; verify pinout/assembly availability. |
| P high side, SOT-23 alternate | NCE NCE3401AY | **C169815** | -30 V, 80 mOhm at -2.5 V, 4.4 A listing; verify manufacturer data sheet, thermal current, pinout, and stock. |

For a low-current Bee bring-up, C15127 + C20917 is a sensible **candidate pair**, not a proven factory pair. For 5–12 A whoop phases, SOT-23 package dissipation and copper—not the headline drain-current number—will likely dominate; the Toshiba-class low-RDS package is preferable if sourceable. Do not substitute the similarly named SI2301 blindly: the LCSC BORN C306861 listing is only a 20 V P-FET with 110 mOhm at 4.5 V and no favorable 2.5 V guarantee.

## Topology decision

1. **Current Layout A + direct P/N gates:** **NO-GO** until the physical gate polarity is proven; bare AO3401 GPIO high is not guaranteed off at 4.2 V.
2. **Correct 1S direct-drive P/N:** **CAUTION / conditional GO**. Use a firmware layout whose output polarity and PWM side match the P/N bridge (O-style low-side PWM is the documented precedent), source-referenced P-gate pull-ups, deliberate dead time, local VBAT bulk capacitance, and scope/thermal testing at a charged cell.
3. **All-N with bootstrap or a 3-phase gate driver:** technically valid and preferred for 2S+ or higher current, but more complex for this 1S bring-up. A driver must have a suitable low-voltage operating range and enough bootstrap/charge-pump headroom; it is not automatically safer merely because it uses N-FETs.

**Bring-up gate:** do not order the present ESC bridge as “validated.” First correct the Layout A/O-style mapping decision, add/define the P-gate off network (or explicitly accept a narrowly tested 1S-only direct gate), and capture gate/phase waveforms at 3.0/3.7/4.2 V before connecting a motor.

## Sources

1. Silicon Labs, **EFM8BB2 Data Sheet** (includes EFM8BB21F16G-C-QFN20; Port I/O table; absolute maximums): https://www.silabs.com/documents/public/data-sheets/efm8bb2-datasheet.pdf
2. AOS, **AO3401 30 V P-Channel MOSFET Data Sheet**, Rev. 6.1 (Feb. 2024): https://www.aosmd.com/sites/default/files/res/datasheets/AO3401.pdf
3. AOS, **AO3400A 30 V N-Channel MOSFET Data Sheet**, Rev. 3.1 (Jul. 2023): https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf
4. LCSC, **AOS AO3401A, C15127**: https://www.lcsc.com/product-detail/C15127.html
5. LCSC, **AOS AO3400A, C20917**: https://www.lcsc.com/product-detail/C20917.html
6. LCSC, **Toshiba SSM6J501NU,LF, C146326**: https://www.lcsc.com/product-detail/MOSFETs_TOSHIBA-SSM6J501NU-LF_C146326.html
7. LCSC, **NCE NCE3401AY, C169815**: https://www.lcsc.com/product-detail/C169815.html
8. Bluejay, **Layouts/A.inc**: https://raw.githubusercontent.com/mathiasvr/bluejay/main/Layouts/A.inc
9. BLHeli_S, **O.inc** (explicit low-side PWM / active-low complementary FET definition): https://raw.githubusercontent.com/bitdump/BLHeli/master/BLHeli_S%20SiLabs/O.inc
10. OpenDrone-hw, **OpenAIO-Whoop README** (1S direct-drive P+N design question; not a production board): https://raw.githubusercontent.com/OpenDrone-hw/OpenAIO-Whoop/main/README.md
11. Electronics Stack Exchange, **HAKRC HK1S ESC FET identification** (teardown and probable SSM6J501NU marking): https://electronics.stackexchange.com/questions/484001/hakrc-hk1s-esc-fet-identification
12. Nexperia, **Understanding power MOSFET data sheet parameters** (why VGS(th) is not full enhancement): https://assets.nexperia.com/documents/application-note/AN11158.pdf
13. TI, **Avoid Common Mistakes When Selecting and Designing With Power MOSFETs**: https://www.ti.com/lit/an/slpa021/slpa021.pdf
14. BetaFPV, **F4 1S 12A AIO** (BB51/Bluejay 1S ESC example; no FET schematic published): https://betafpv.com/products/f4-1s-12a-flight-controller
