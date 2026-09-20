# Open questions (resume)

Collected from CAD + electronics discussion at pause (~2026-09-19).

## Airframe / propulsion

1. Confirm span **120 mm** vs step-up to **200–300 mm** if 0802/1S thrust fails static test.
2. Real **0802 hole pattern** + exact prop diameter from the chosen motor kit.
3. Exact **AIO board outline** (replace 32×36×8 placeholder) after Bee Core → flyable 2-ESC AIO.
4. **Servo** brand / horn geometry + linkage (pushrod vs direct).
5. Weigh printed LW wing vs **foam mid-panel** if AUW creeps.
6. Re-enable **VibeCAD agent control** (`127.0.0.1:8766`) for live CAD iteration.

## Electronics / fab

1. Finish Bee Core PCB routing manually (or alternate tool) to fab-ready — or simplify v0.1 with **external ESC** pads.
2. Complete thin ESC sheet items (e.g. 10k BEMF mux vs tinyPEPPER).
3. First hover firmware: **custom RP2350** vs **STM32 + ArduPilot** escape hatch.
4. Motor lock: **0802** vs **1102** after thrust measurement at ~100 g AUW target.
5. Companion header pinout freeze when camera/swarm work resumes.
