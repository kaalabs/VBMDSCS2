# Machine Profile: VBM Domobar Classic/Standard (RVS)

Authoritative product reference: [eembergen.nl/product/vbm-domobar-classic/](https://eembergen.nl/product/vbm-domobar-classic/)
Label-confirmed details (user photo): 1G, MANUALE, HX, 1400 W 50/60 Hz, single phase 220–240 V~, max pressure rate 1 MPa.

Key characteristics
- Topology: Single steam boiler with heat exchanger (HX)
- Boiler: Copper, 0.60 L
- Group: VBM E61, mechanical preinfusion
- Pump: Vibration pump (Ulka EP-class), adjustable OPV typical
- Heater: 1400 W, EU market (220–240 V, 50/60 Hz confirmed)
- Water: 2.1 L removable reservoir (tank only), low-water microswitch
- UI: Metal toggle switches; semi-automatic lever
- Brew lever microswitch: Present (MANUALE variant)
- Control boards: None present (machine is fully mechanical/analog)
- Hot water tap: Not present
- Steam availability: ~30 s after steam toggle (per vendor)
- Dimensions: 40 × 22.5 × 34 cm; Mass: 20 kg

Implications for control
- Maintain stock mechanical safeties: pressure relief valve, thermal cutouts/fuses, and pressurestat as primary boiler controller.
- Our system supervises and requests heat via SSR but never bypasses mechanical safeties.
- Non-invasive sensors: boiler temperature and pressure added on available ports; tank level via existing microswitch input; brew lever switch is tapped via opto-isolated input.
- Max pressure rate 1 MPa is an equipment rating; operational control limits remain within typical boiler working pressures (≈1.0–1.2 bar) with a conservative software high limit.

Open items to confirm (will affect BOM and I/O)
- Pressurestat model (e.g., Ma-Ter XP110) and contact rating
- Available ports for temp and pressure sensors
- Pump model (Ulka EP5/EX5) and OPV accessibility

Cited source: [VBM Domobar Classic/Standard](https://eembergen.nl/product/vbm-domobar-classic/)

