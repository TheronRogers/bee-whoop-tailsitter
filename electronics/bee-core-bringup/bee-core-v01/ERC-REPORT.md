# ERC status summary — 2026-09-16

- **Final:** **0 errors / 35 warnings** (35 total), verified with KiCad 9.0.2 GUI ERC and `kicad-cli sch erc --severity-all`.
- **Previous checkpoint:** 4 errors / 31 warnings.
- **Detailed machine report:** `work/erc-final-zero.rpt`
- **GUI screenshot:** `work/ERC-final-panel.webp`

## Final fixes

- U2 regulator duplicate OUT pin conflict resolved by defining duplicate pin 4 as passive; pin 2 remains the power-output driver.
- Root +1V1 and VREG_AVDD power-tree flags retained.
- ESC U20 VDD/VBAT now has `#FLG03` on the exact VDD endpoint; C24 pin 1 is wired to the VBAT/VDD net.
- The KiCad 9 GUI ERC panel shows **Errors 0** and **Warnings 35**.

## Warnings accepted/documented

The 35 remaining warnings are non-blocking: legacy off-grid endpoints, four unavailable stock `Capacitor_SMD` footprint aliases, dangling/duplicate label naming, multiple net-name aliases in COMPANION, and one U2 embedded-symbol mismatch warning caused by the intentional pin-type cleanup. Resolve footprint aliases and tidy legacy geometry before fabrication export.

## PCB path

- Preserved KiCad 10 source/backup: `bee-core-v01.kicad_pcb` and `bee-core-v01.kicad10-native-backup.kicad_pcb`.
- Created editable KiCad 9 bring-up board: `bee-core-v01-kicad9-bringup.kicad_pcb`.
- Board has a 32 x 36 mm Edge.Cuts rectangle and 83 net names staged from `work/bee-core-v01.net`; footprint placement/routing remains the next PCB pass because the legacy netlist importer reports missing custom footprint aliases.
- KiCad 9 PCB DRC on the staged board: 0 violations / 0 unconnected items (`work/pcb9-drc.rpt`).
