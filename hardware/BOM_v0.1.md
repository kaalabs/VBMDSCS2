# BOM v0.1 (Draft) – VBM Domobar Classic/Standard Retrofit

Core electronics

- ESP32‑WROOM‑32E module (Boiler/Steam node)
- Optional ESP32‑S3 module (Master/UI)
- Isolated RS‑485 transceivers (e.g., ADM2483/ISO3082 class) or RS‑485 + digital isolators (ADuM series)

Power and protection

- Zero-cross SSR for heater (≥10 A @ 230 VAC), with snubber; DIN-rail or panel mount
- AC-rated relay for pump control (≥3 A @ 230 VAC) or SSR as appropriate
- Fast-blow or thermal fuses sized to heater current; inline fuseholder
- MOV + RC snubber for surge suppression on mains
- Proper earthing hardware; insulated stand-offs; enclosure with adequate creepage/clearance

Sensors and inputs

- Boiler pressure transducer, 0–3 bar, 5 V ratiometric, food-safe wetted materials
- Boiler temperature: PT1000 + MAX31865 (SPI) or K-type + MAX31856 (SPI), isolated where needed
- Tank low-water microswitch: opto-isolated digital input
- Brew lever microswitch: opto-isolated digital input (with debounce in firmware)
- Grouphead temperature clip: DS18B20 or NTC + ADC divider
- Brew-circuit pressure transducer: 0–16 bar, ratiometric
- Flowmeter (food-grade, low-restriction, e.g., Digmesa)
- Pump non-contact CT sensor for current logging
- DYP-A02YYUW ultrasonic level sensor (5 V) with level shifting/isolation as appropriate
- Optional simple TDS probe port (for diagnostics only)

Storage and connectivity

- microSD module (SPI) or FRAM for robust logging
- Wi‑Fi provisioning button/LED, buzzer for cues

Interfaces and passives

- Terminal blocks (mains-rated), ferrules, heat-resistant wiring (silicone/PTFE)
- Opto-isolators for digital inputs (≥2 channels for tank + brew; expand as needed)
- RC filters for ADC inputs; TVS diodes on signal lines; level shifters for 5 V sensors

Mechanical

- Mounting bracket/hardware to fit without drilling permanent holes (non-invasive)
- Harness adapters to interpose without cutting factory wiring

- Water permit loop hardware: NC safety relay or open-collector driver + pull-up; opto inputs on consumer nodes; harness connectors.

Notes

- Keep factory pressurestat, thermal cutouts, and safety valve fully operational.
- Ensure CE-relevant practices: creepage/clearance, conductor sizing, strain relief, earthing.

