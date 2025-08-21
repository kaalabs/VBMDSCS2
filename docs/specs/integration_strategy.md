# Integration Strategy – Decentralized Autonomous Nodes with Optional Orchestration

Principles
- Core nodes operate safely and autonomously; master/UI only augments non-core functions.
- Factory hardwired safeties remain in series; our control never bypasses them.
- All advanced features are opt-in; physical interlocks and watchdogs always apply.

Phased integration (reversible)
- Phase 0: Read-only validation
  - Tap tank microswitch, brew lever, boiler pressure/temp (read-only).
  - Water level UX: show "Tank OK/Low" status and latched "Low tank" alarm; add buzzer/LED cue mapping.
  - Optional: bring-up of DYP‑A02YYUW ultrasonic sensor on bench; calibrate empty/full; no control action yet.
- Phase 1: Boiler/Steam node install (autonomous)
  - Insert heater SSR after pressurestat; enable low-water inhibit and safety watchdog.
  - Water level UX: real-time status on local indicator and master UI; alarm latch with manual acknowledgement after refill.
  - Optional DYP: display % estimate and basic shot-remaining estimate using recent flow averages.
- Phase 1.5: Pump relay after brew lever + shot timing
  - Gate pump by lever + low-water interlock; implement shot timer/counters.
  - Water level UX: pre-brew check blocks shot when low; present clear recovery guidance.
- Phase 2: UX features (master optional)
  - Warm-up/eco modes, HX flush coach, telemetry, OTA, MQTT (opt-in).
  - Water level UX: If DYP present, show tank percentage trend and estimated refills; log low-water events.
- Phase 3: Medium hardware features
  - Volumetric assist (flowmeter), brew pressure telemetry, adaptive preinfusion.
  - Water level UX: Use flowmeter stats to refine "shots remaining" when DYP is absent (heuristic based on average shot volume + steam usage).
- Phase 4: Advanced/experimental (gated)
  - Pressure profiling via certified AC driver; additional interlocks; not required for water UX.

Implementation notes for water level monitoring
- Source signals: tank microswitch (primary interlock) and optional DYP‑A02YYUW (UART/analog).
- Debounce and hysteresis: software debounce ≥20 ms for switches; percentage smoothing for ultrasonic; time gating to avoid chatter during movement.
- Latching behavior: "Low tank" latches outputs-inhibited until refill is detected and user acknowledges at UI (or power cycle), matching safety matrix.
- UI/alerts: icon/state on master UI, local LED/buzzer patterns (distinct from other faults), MQTT state if enabled.
- Privacy/safety: No remote start allowed when low-water is latched; remote clear requires physical presence action.



Permit architecture updates
- Introduce Tank/Water node providing fail-safe WATER_OK permit and telemetry.
- Boiler/Brew nodes require permit AND local checks; bus advisories do not affect safety.
- Loss of permit (or node power) immediately inhibits heater/pump; factory microswitch remains primary.
