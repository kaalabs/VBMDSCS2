# VBM Domobar Classic/Standard Control System

Safety-first, non-invasive control system retrofit for the Vibiemme Domobar Classic/Standard (RVS) single-boiler HX espresso machine.

Confirmed target characteristics
- 220–240 V~ / 50–60 Hz (single phase)
- Single boiler with heat exchanger (HX)
- Copper boiler 0.60 L
- Vibration pump
- Tank feed only, 2.1 L reservoir, microswitch low-water detection
- E61 group, semi-auto lever, metal toggle switches
- Heater 1400 W
- Max pressure rating (label): 1 MPa (equipment rating, not a control setpoint)

Label confirmation: 1G group, MANUALE, HX, 1400 W 50/60 Hz, single-phase 220–240 V~, max pressure rate 1 MPa.

Reference: [VBM Domobar Classic/Standard (RVS)](https://eembergen.nl/product/vbm-domobar-classic/)

Project principles (priority order)
1. Safety
2. Robustness
3. Maintainability
4. Modularity
5. Simplicity of use
6. Innovative features (opt-in)
7. Non-invasive (preserve original UX unless extended explicitly)

Architecture at a glance
- Boiler/Steam local node: ESP32‑WROOM‑32E (MicroPython). Enforces all local safeties and operates standalone.
- Tank/Water node: ESP32‑WROOM‑32E. Provides fail-safe WATER_OK permit and water telemetry; independent of master.
- Optional Master/UI node: ESP32‑S3 (MicroPython). Orchestrates, UI/telemetry. Failure cannot compromise safety.
- Fieldbus: Isolated RS‑485 (Modbus RTU) between nodes.
- Actuation: Heater via zero-cross SSR; pump via AC-rated relay. Factory pressurestat and thermal safeties remain in circuit.

Repository layout
- docs/: Specifications, safety, interfaces
- hardware/: BOM and hardware integration notes
- firmware/common/: Shared libraries (e.g., Modbus)
- firmware/boiler_node/: Local node firmware (ESP32‑WROOM‑32E)
- firmware/master_ui/: Master/UI firmware (ESP32‑S3)
- firmware/tank_node/: Tank/Water node firmware (ESP32‑WROOM‑32E)

Getting started
- See docs/specs/machine_profile.md, docs/specs/label_ocr.md, and docs/safety/safety_matrix.md
- firmware/boiler_node contains a MicroPython skeleton with a safety-state machine and placeholders for I/O mapping



## Features
See `docs/specs/features.md` for opt-in capabilities and dependencies.


## Integration Strategy
See `docs/specs/integration_strategy.md` for phased, decentralized integration (includes Water Level Monitor UX).


## Tools
- Host Modbus CLI: `tools/modbus_cli.py` (pyserial).
  - Example: `python3 tools/modbus_cli.py /dev/tty.usbserial-XXXX 115200 read 1 0x0010 4`
  - Heartbeat: `python3 tools/modbus_cli.py /dev/tty.usbserial-XXXX 115200 heartbeat 1 0x00F0 200`


### BLE scales
See `docs/specs/ble_scales.md`. Drivers: Acaia, Bookoo, Half Decent (skeletons under `firmware/master_ui/ble_scales/`).


See also: `docs/specs/harness_plan.md` for the fail-safe water permit loop.


## Dependencies & Roadmap
See `docs/specs/dependencies_roadmap.md` for feature dependencies and implementation order.
