# Electronics discussion notes (Bee / Tailsitter agent)

**Period:** 2026-09-09 → 2026-09-16 (paused)  
**Repo path:** `electronics/bee-core-bringup/`  
**Goal Theron stated:** break into hardware with an affordable tailsitter; see how cheaply a fully custom PCB can be made; unlock later directions (camera, autonomy, swarm).

## Locked decisions

| Topic | Lock |
|-------|------|
| Airframe control | Two fixed rotors + two elevons; no tilt, swashplate, or collective |
| Board scope | Full AIO from day one (FC + ESCs + servo drivers), not commodity FC first |
| Motors for v0 | Brushless whoop-class (switched from brushed after cost compare; ~+$10–35/bird vs brushed but matches later path) |
| Bring-up first | RP2350 “Bee Core” board before flyable 2-ESC AIO — learn PCB + showable progress |
| MCU lean | RP2350A (UK, dual M33 or Hazard3 RISC-V, PIO); custom/Zephyr firmware. STM32F4 + ArduPilot = escape hatch for stock VTOL |
| Liberty / RT | Prefer liberty-aligned sourcing + real-time learning; don’t pick FC MCU primarily for future vision |
| Growth model | Split: RT AIO now, companion (cam/CV/swarm) later via UART/SPI/I2C header |
| ESC (bring-up) | One on-board EFM8BB21 + FET channel |
| ESC topology | **Bluejay Layout O**, complementary P/N (tinyPEPPER pattern); **EFM8 VDD = VBAT (1S only)**; N: IRLML6244; P: IRLML2244; flash `O_H_05` |
| ESC NO-GO | Layout A + bare 3.3 V GPIO → AO3401 P-gates (VGS ≈ −0.9 V at 4.2 V VBAT) |
| IMU | BMI270 (or ICM-42688) on SPI |
| Fab | JLCPCB PCBA qty ~5; prefer 4-layer when ESC+IMU share board |

## Bee Core bring-up board (v0.1)

**On board:** RP2350A, QSPI flash, USB-C, SWD, BOOTSEL/RUN, BMI270, 1× Layout O ESC, 1× servo PWM + 5 V path, COMPANION 6-pin (DNP OK), status LED.

**Proof order:** USB → blink/SWD → IMU ≥1 kHz → servo → DShot motor.

**GPIO map (locked in schematic notes):**

| Function | GPIO |
|----------|------|
| Companion UART TX/RX | 0 / 1 |
| Companion I2C SDA/SCL | 2 / 3 |
| DShot → ESC | 14 |
| Servo PWM | 15 |
| IMU SPI MISO/CS/SCK/MOSI | 16 / 17 / 18 / 19 |
| IMU INT1 | 20 |

## KiCad status at pause

- Project: `electronics/bee-core-bringup/bee-core-v01/`
- Schematic: hierarchical IMU / SERVO / ESC / COMPANION; **ERC 0 errors**
- Working PCB: `bee-core-v01-kicad9-bringup.kicad_pcb`
- Bring-up outline grew **80×60 mm** for debug; **flight AIO target 32×36 mm** (Rad CAD tray) kept in silk/docs
- Placement/routing: useful progress then stalled; failed F.Cu rip/autoreroute **reverted**; baseline ~0 unconnected after GND vias, shorts/crossings still high — **not fab-ready**
- Theron: continue PCB manually or with another tool later — see `bee-core-v01/HANDOFF.md`

## Open / revisit on resume

1. Manual PCB routing / DRC to fab-ready, or simplify first fab (external ESC pads).
2. Flyable AIO: second ESC + second servo; shrink toward 32×36.
3. Firmware: custom VTOL on RP2350 vs ArduPilot on STM32 for first hover video.
4. Motor class: 0802 vs 1102 given ~100 g AUW / T/W~2 flag from CAD.
5. 10k BEMF mux resistors on ESC sheet still thin vs tinyPEPPER reference.

## Key docs in tree

- `DESIGN.md`, `BOM-TARGETS.md`, `ESC-TOPOLOGY-DECISION.md`, `ESC-VGS-CHECK.md`
- `SCHEMATIC-NOTES.md`, `PCB-STATUS.md`, `HANDOFF.md`, `DRC-CATEGORIES.md`
