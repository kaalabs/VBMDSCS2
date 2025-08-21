# ESP-IDF Secure Boot v2 and Flash Encryption Setup

Prereqs
- ESP-IDF v5.x recommended (adjust symbols for v4.x if needed).
- Offline key generation on a secure host; keys are never checked in.

Steps (summary)
1. Generate Secure Boot signing key (RSA‑3072) and Flash Encryption key as per Espressif docs.
2. Place signing key path in `hardware/idf/sdkconfig.secure.defaults` (host path only).
3. Select the appropriate partition CSV in IDF project config.
4. Build bootloader and app; sign binaries; flash in DEVELOPMENT mode for bring-up.
5. Validate OTA A/B swaps, watchdog/rollback, and power-loss during OTA.
6. Switch to RELEASE flash encryption mode; lock JTAG/UART boot as required.

Operational notes
- Keep separate keys for dev/staging/prod; rotate on schedule.
- Record efuse burns and keep a device ledger.
- Combine with our app-layer Ed25519 bundle sign/verify.

References
- Espressif Secure Boot v2 and Flash Encryption guides (IDF docs).

