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



Capture procedure (per model)
1. Use nRF Connect (or similar) to scan and connect to the scale.
2. Record advertised name/manufacturer data.
3. Record all GATT services and characteristics (UUIDs), and identify the weight notify characteristic and CCCD.
4. Note CCCD write value to enable notifications.
5. Save logs and paste UUIDs into driver placeholders (SERVICE_UUID, WEIGHT_CHAR_UUID).

Models to capture (priority)
- Acaia Lunar
- BOOKOO Themis mini
- Half Decent scale

Known limitations
- CCCD index may differ (not always value_handle+1).
- Name prefix matching is a fallback; prefer UUIDs.
- Vendor payload formats may need parsing/byte-order fixes.
