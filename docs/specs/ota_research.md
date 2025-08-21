# OTA Update Research (ESP32 ESP-IDF/MicroPython)

Scope
- Evaluate OTA paths for ESP32-WROOM-32E and ESP32-S3 with MicroPython firmware and app code.

Candidate: ElegantOTA (reference)
- Summary: Popular Arduino/ESP OTA (web UI) library.
- Applicability: Arduino/C++ only; not directly compatible with MicroPython runtime.
- Potential use: Not recommended for this stack. Would require a C/ESP-IDF co-resident app managing OTA of MicroPython image, increasing complexity and risk.

Recommended OTA direction for this project
- Use ESP-IDF OTA partitioning and MicroPython firmware updates (.bin) with signed bundles and A/B rollback.
- Application layer (Python) updates:
  - Secure download over HTTPS (master/UI), verify signature, write to filesystem, swap symlink/current dir, and reboot.
  - Maintain feature flags/config separately; versioned schema.
- Transport options: Local web UI (AP mode), USB (mpremote), or optional MQTT-triggered fetch (never direct code via MQTT).

Security & safety
- Signed artifacts (ED25519/RSA) and manifest with version/compatibility.
- Watchdog and rollback on failure; never update core nodes simultaneously.
- Permit loop and mechanical safeties unaffected during updates.

Next actions
- Define partition table and A/B scheme.
- Prototype HTTPS fetch + signature verify in MicroPython on ESP32-S3.
- Document update UX and recovery.

