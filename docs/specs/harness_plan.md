# Harness Plan – Non-invasive Integration (No factory logic board)

Principles
- Zero permanent modifications; reversible to stock.
- Retain factory series wiring of pressurestat, thermal cutouts/fuses, and safety valve.

Heater control
- Interpose an SSR in series with the heater feed after the pressurestat output.
- SSR coil driven by ESP32 via opto/driver, with additional series hardware enable under MCU control.
- If SSR fails closed, pressurestat and thermal cutout still protect; if pressurestat fails, thermal cutout protects.

Pump control
- Interpose an AC-rated relay in series with the pump feed after the brew lever microswitch.
- Tap the brew lever microswitch signal using an opto-isolated high-impedance input to the ESP32; implement 10–20 ms debouncing.
- Relay coil driven by ESP32; default de-energized (pump off). Pump enable requires: lever active AND tank not-low AND no fault.

Low-water microswitch
- Tap the microswitch signal using an opto-isolated input to the ESP32; do not disturb factory series path that inhibits pump/heater.

Sensors
- Boiler pressure: add a 1/8" BSPT (or M) T-fitting on an available port; route to a 0–3 bar transducer.
- Boiler temperature: add PT1000/K-type probe to existing spare port or thermowell; avoid disturbing stock safety devices.

Grounding and EMC
- Single-point earth bonding of added metalwork; cable shields grounded at one end.
- RS‑485 cabling twisted/shielded; maintain separation from mains per creepage/clearance.

Connectorization
- Use inline adapters to interpose without cutting wires (e.g., spade-to-spade jumpers with insulated housings).



Water permit loop (fail-safe)
- Tank node asserts WATER_OK via open-collector or NC relay; default inhibit on power loss.
- Boiler and Brew nodes read permit via opto-isolated inputs; outputs require permit AND local checks.
- Factory microswitch remains in series as primary protection.
