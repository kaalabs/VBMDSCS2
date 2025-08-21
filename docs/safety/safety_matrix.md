# Safety Matrix (IEC 60335 context, layered)

Principles
- Mechanical/hardwired protections remain primary.
- Our electronics add supervision, interlocks, logging, and controlled recovery.

Hazards and mitigations

| Hazard | Primary protection (factory) | Added electronic protection | Fail-safe behavior |
| --- | --- | --- | --- |
| Overpressure | Pressure relief valve; pressurestat limits | Software pressure limit; heater inhibit if pressure > 1.5 bar | Heater latched off until manual recovery |
| Overtemperature | Thermal cutout(s)/fuse on boiler | Independent watchdog and temperature check | Heater off; fault reported |
| Dry heating | Tank microswitch inhibits pump; user refills | Heater inhibit when tank low; pump inhibit | Latched fault until tank restored |
| Shorted SSR/relay | Pressurestat still in series; thermal cutout | Plausibility checks (pressure rise without command) | Power cycle required; alert |
| Sensor failure | N/A | Sensor plausibility checks; timeouts | Revert to mechanical-only; heater requests limited to safe window |
| Firmware lockup | N/A | HW watchdog; independent timeouts | Outputs off on watchdog reset |
| EMI/transients | N/A | Isolated RS‑485; input filtering; debouncing | Graceful degradation; retries |

Setpoints and limits (defaults)
- Boiler pressure working band: 1.0–1.2 bar (pressurestat); software high limit 1.5 bar
- Max boiler temp (supervision): 135 °C (HX steam boiler typical)
- Low-water: immediate inhibit; require manual acknowledgment after refill

