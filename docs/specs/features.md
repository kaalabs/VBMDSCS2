# Feature Specification (Opt-in Nerd Features)

Scope and defaults
- Default behavior preserves stock UX. All advanced features are opt-in, with physical interlocks.
- Safety layers remain primary: mechanical safeties and firmware watchdogs supersede features.

Software/UX-only (non-invasive)
- Shot timer and counters (lever microswitch-based); per-day and lifetime stats.
- Maintenance telemetry: heater cycles, pump runtime, steam time; backflush/descale reminders.
- Smart warm-up profiles; steam-boost mode within safe limits.
- HX flush coach: estimate brew water temp via boiler pressure + thermosyphon model; recommend flush time/volume.
- Energy modes: idle sleep, scheduled wake, auto-standby.
- Audible/visual cues: steam ready, brew target time reached, low tank (latched).
- Local-first connectivity: Wi‑Fi AP + WPA2 provisioning; optional MQTT/Home Assistant; signed OTA; offline-first logging.

Low-additional-hardware (non-invasive)
- Grouphead temperature clip (thermistor/DS18B20) for accurate HX guidance and learning.
- Shot logging enhancement: non-contact CT pump current sensing.
- Water quality tracking: optional simple TDS probe port for diagnostics.
- Water level tracking: DYP-A02YYUW ultrasonic sensor (5 V), UART/analog; provides tank percentage, trend, and shots-remaining estimate; diagnostic by default, never overrides mechanical interlock.

Medium hardware extensions (preserve stock UX)
- Volumetric shot assist (flowmeter). Auto-stop at target volume when enabled.
- Brew/boiler pressure telemetry: transducers on brew path and boiler for curves; no control changes by default.
- Adaptive preinfusion timer: timed soft-start pump gating; opt-in and conservative.

Diagnostics and service
- Service mode: pump priming, boiler refill, OPV set-check, leak detection via pressure decay.
- Fault analytics: SSR welded detection; trend drift of pressurestat/OPV.

Privacy/safety
- Local-only by default; remote requires explicit enable and presence interlocks.
- Signed OTA with rollback; latched faults override features.

Dependencies matrix (abridged)
- Flowmeter → volumetric assist; brew pressure transducer → brew curves; grouphead temp clip → HX coach accuracy; ultrasonic tank → water analytics; CT sensor → shot detection refinement.



UX specifics
- Water level UX: Local LED/buzzer cues; UI tank state/percent; latched low-water alarm with manual recovery.
