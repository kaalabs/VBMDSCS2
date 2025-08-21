# BLE Scale Integration (Master/UI)

Target compatibility
- Acaia
- Bookoo
- Half Decent

Approach
- Master/UI (ESP32‑S3) hosts BLE Central, scans/pairs with supported scales.
- Drivers per vendor implement discovery, subscription to weight/time streams, and tare/zero commands where available.
- Data model: weight (g), rate (g/s), time (ms), stability flag, battery.
- Privacy: pairing requires user action; no Internet; data stays local unless MQTT is explicitly enabled.

Nerd features enabled by BLE scales
- Weight-triggered shot timer: start when puck wet mass increases; stop at target yield.
- Brew ratio coach: display live ratio (yield/dose) and target window cues.
- Predictive stop: combine flowmeter (if present) + weight derivative to stop near target yield.
- Bloom/preinfusion assist: hold pump until weight increase threshold then ramp; opt-in and respect lever semantics.
- RDT/flow monitoring: detect chokes or channeling via weight rate anomalies; log for diagnostics.
- Smart purge and backflush dosing by weight.
- Calibration assistant: verify scale linearity with reference mass prompts.

Failure/robustness
- If BLE drops mid-shot, system falls back to time/flow-only logic; never compromises safety.
- Scales are optional; nodes remain autonomous; BLE lives entirely on master/UI.

