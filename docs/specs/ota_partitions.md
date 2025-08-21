# OTA Partitioning

Targets
- ESP32-WROOM-32E (4 MB): see `hardware/partitions/esp32_4mb.csv`.
- ESP32-S3 (8 MB): see `hardware/partitions/esp32s3_8mb.csv`.

Notes
- Two OTA slots (`ota_0`, `ota_1`) managed by IDF OTA; `otadata` tracks active slot.
- `storage` (FAT) for MicroPython app bundles, logs, and settings.
- Enable Secure Boot v2 (RSA‑3072) and Flash Encryption per Espressif docs.

Apply
- Use these CSVs in IDF projects that build MicroPython images.
- Ensure MicroPython fs points to `storage` partition for app bundles.

