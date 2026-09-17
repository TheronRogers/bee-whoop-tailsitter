# Bee Core v0.1 — PCB bring-up design notes

## Current bring-up state — 2026-09-16

The KiCad 9 bring-up PCB is editable and contains the imported schematic connectivity, 69 footprints, and an unrouted ratsnest. Legacy custom footprint aliases were remapped to stock KiCad footprints sufficiently for Update PCB from Schematic to complete.

### Board size decision

The 32 x 36 mm flight target is retained as the product target, but it is too tight for this first bring-up arrangement with USB, debug headers, ESC/power parts, and motor connectors. The bring-up outline is therefore **55 x 50 mm**. The PCB silkscreen explicitly marks the 32 x 36 mm flight target. Debug and connector consolidation should be revisited before shrinking toward flight size.

### Placement zones

- U1 (RP2350), U2/U3 flash, and J1 USB placeholder are grouped in the left/center logic area.
- U20 ESC controller and local decoupling are adjacent to the logic cluster.
- ESC FET/power groups and bulk capacitors are staged toward the right-hand motor/power edge.
- J2/J3 debug headers and J4/SW1/SW2 placeholders remain accessible around the perimeter.
- Mounting holes are staged along the left edge; the IMU and quiet-zone optimization still need a dedicated placement review.

### Open work

Replace the temporary header placeholders with verified production footprints, populate the defined 4-layer stackup with power/ground zones, route, and run PCB DRC. The KiCad 10 native backup remains untouched.
