# Bee Core v0.1 — Schematic notes (working tree)

**Working project:** `/workspace/bee-core-bringup/bee-core-v01/`  
**Do not edit:** `vendor/` (untouched). Original Minimal also remains in `kicad/` as a pristine copy.

## KiCad compatibility

| Item | Notes |
|------|-------|
| Installed on box | **KiCad 9.0.2** (`apt`, package `kicad 9.0.2+dfsg-1`) |
| Upstream Minimal | Generated with **KiCad 10** (`generator_version 10.0`, sch `20260306`, pcb `20260206`) |
| Working `.kicad_sch` | Downgraded for KiCad 9 (see `bee-core-v01.kicad_sch.kicad10-bak` for native) |
| Working `.kicad_pcb` | Still KiCad 10 native — **will not load** in 9.0.2 until upgraded KiCad or PCB downgrade |
| CLI | `kicad-cli` 9.0.2 — sch ERC/PDF export works on downgraded tree |

Downgrade transforms applied to schematic: strip `do_not_autoplace` / `show_name` / `in_pos_files` / `body_style`; `(power global)` → `(power)`; move property-level `(hide …)` into `(effects …)`.

## Hierarchy

| Sheet | File | Contents |
|-------|------|----------|
| Root (page 1) | `bee-core-v01.kicad_sch` | RP2350A Minimal MCU island + sheet boxes |
| IMU (page 2) | `sheets/imu.kicad_sch` | **U10 BMI270** + SPI/INT globals |
| SERVO (page 3) | `sheets/servo.kicad_sch` | PWM/5V net plan + labels |
| ESC (page 4) | `sheets/esc.kicad_sch` | **U20 EFM8BB21** Layout A port nets |
| COMPANION (page 5) | `sheets/companion.kicad_sch` | 6-pin header net plan |

Custom symbols: `bee-core.kicad_sym` (BMI270 from BMI160 pin-compatible LGA-14; EFM8BB21F16G-C-QFN20 per EFM8BB2 DS §6.3).

## GPIO assignment (v0.1)

| Function | RP2350 net | Notes |
|----------|------------|-------|
| UART0 TX (companion) | GPIO0 | |
| UART0 RX (companion) | GPIO1 | |
| I2C1 SDA (companion) | GPIO2 | |
| I2C1 SCL (companion) | GPIO3 | |
| DShot → ESC RTX | GPIO14 | Add **100–330 Ω** series to EFM8 P0.5 in GUI |
| Servo PWM | GPIO15 | |
| IMU SPI0 MISO | GPIO16 | BMI270 SDO |
| IMU CS | GPIO17 | BMI270 CSB |
| IMU SPI0 SCK | GPIO18 | BMI270 SCx |
| IMU SPI0 MOSI | GPIO19 | BMI270 SDx |
| IMU INT1 | GPIO20 | |

These GPIOs were promoted from local → **global_label** on the root sheet so hierarchical sheets connect.

## ESC — Bluejay Layout A (cited)

Source: [Bluejay `Layouts/A.inc`](https://raw.githubusercontent.com/mathiasvr/bluejay/main/Layouts/A.inc) — `PWM_ACTIVE_HIGH`, `COM_ACTIVE_HIGH`; PWM side high.

| Port | Role | QFN20 pin (BB2 DS) | Net on sheet |
|------|------|--------------------|--------------|
| P0.0 | Vn | 2 | ESC_Vn |
| P0.1 | Am | 1 | ESC_Am |
| P0.2 | Bm | 20 | ESC_Bm |
| P0.3 | Cm | 19 | ESC_Cm |
| P0.5 | RTX | 17 | GPIO14 (DShot) |
| P1.0 | Ap | 14 | ESC_Ap |
| P1.1 | Ac | 13 | ESC_Ac |
| P1.2 | Bp | 11 | ESC_Bp |
| P1.3 | Bc | 10 | ESC_Bc |
| P1.4 | Cp | 9 | ESC_Cp |
| P1.5 | Cc | 8 | ESC_Cc |

FET plan (not yet placed as components): 3× AO3401A (P, LCSC C5296722) high-side + 3× AO3400A (N, C20917) low-side; Ap/Bp/Cp → P gates; Ac/Bc/Cc → N gates.

**FLAG:** 3.3 V GPIO cannot strongly enhance a P-FET on a 1S VBAT rail (Vgs too small). Re-validate against OpenAIO-Whoop / known BLHeli hardware before PCB — may need VBAT-referenced gate drive or alternate FETs. Prefer correct nets over a fake-complete power stage.

Silk: `BLUEJAY LAYOUT A` and `VBAT MAX 1S`.


## Wiring honesty flag

`U10` (BMI270) and `U20` (EFM8BB21) are **placed** with correct footprints/LCSC fields.
An attempted CLI auto-wire attached global labels to the **wrong pins** (coordinate bug);
those wires were **removed**. Intended nets remain as unconnected global labels + text
pin maps. **GUI must wire pins per the tables above** before trusting the netlist.

## Remaining GUI pass (exact)

1. Open `bee-core-v01.kicad_pro` in KiCad **9.0.2+** (schematic). Prefer KiCad **10+** if editing the PCB or restoring `.kicad10-bak`.
2. **IMU:** add 100 nF on VDD and VDDIO to GND; NC markers on aux/OIS pins 2,3,9,10,11; test points on CS/INT1; fix any off-grid wire ends.
3. **SERVO:** place `Conn_01x03` (SIG/SERVO_5V/GND); choose BEC (or VBUS polyfuse path); bulk C on SERVO_5V.
4. **ESC:** place 3×AO3401A + 3×AO3400A + gate resistors; BEMF sense dividers Am/Bm/Cm/Vn; VBAT pad + polyfuse; bulk electrolytic+ceramics at FET cluster; motor 3-pad; **Rseries on DShot**; C2 debug optional.
5. **COMPANION:** place `Conn_01x06` DNP, silkscreen `COMPANION`.
6. Power: consider ME6211 (C82942) vs Minimal AMS1117-class LDO when touching power island.
7. Assign footprints / LCSC fields; run ERC clean; then PCB 4-layer zones (GND under IMU; fat VBAT/phase).
8. JLCPCB: BOM+CPL export; mark Basic vs Extended.

## Progress estimate

| Block | ~% | State |
|-------|----|-------|
| Minimal MCU island | 100% kept | Renamed/title; KiCad9 sch loadable |
| IMU | ~65% | Symbol+SPI nets; caps/TP GUI |
| SERVO | ~35% | Nets documented; connector/BEC GUI |
| ESC | ~45% | MCU+Layout A nets; FET bridge GUI + Vgs review |
| COMPANION | ~40% | Pinout+GPIOs; header footprint GUI |
| **Overall first pass** | **~45–50%** | |
