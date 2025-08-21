# Power-on Diagnostics (PoD)

Goals
- Verify core safety and readiness without energizing heater/pump.
- Catch wiring/sensor regressions early; never bypass mechanical safeties.
- Quick boot (<1–2 s) with optional extended service self-test.

Boot phases
- SAFE_INIT: outputs forced safe; watchdog/brownout enabled.
- SELF_TEST (quick): passive checks only; no AC actuation.
- ARMED: interlocks enforced; ready for control.
- EXTENDED_TEST (optional): user-invoked; controlled actuation allowed.

Quick self-tests (all nodes)
- Reset cause log; boot counter increment.
- Config/flags CRC check (when implemented).
- RS‑485 link/heartbeat sanity (where applicable).
- Sensors plausibility (passive only).

Tank/Water node
- Permit default inhibit at boot; debounced tank microswitch; latch on LOW.
- Optional ultrasonic single sample with outlier rejection.

Boiler/Steam node
- Read external WATER_OK permit (if enabled); parallel tank switch as backup.
- Boiler pressure near ambient on cold start; temp plausible.
- Outputs are safe (SSR/pump off).

Master/UI
- RS‑485 status read from nodes; basic storage R/W test; RTC check.

Extended diagnostics (service mode)
- Audible/visual device tests; ultrasonic multi-sample calibration.
- Logic-only SSR/pump pin toggles (no AC energize) and welded-SSR sentinel via pressure trend.

Fault handling
- Safety faults keep node in SAFE_INIT; outputs inhibited; latched fault with clear UX.
- Non-critical issues degrade features; continue safely.

Registers (summary)
- REG_POD_STATUS_BITS: bitset of PoD results per node (see register_map.md).
- REG_LAST_RESET_CAUSE: captures reset reason encoding.

