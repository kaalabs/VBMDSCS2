# Keys and Security (OTA)

Boot/firmware
- Secure Boot v2 (ESP-IDF) with RSA‑3072 signing; Flash Encryption enabled.
- Keys stored offline; use Espressif tooling; never on device.

App bundle (MicroPython)
- Ed25519 signing (detached signature of manifest); public keys embedded read-only on device.
- Key rotation via `key_id`; maintain allowlist of active keys.
- Build pipeline: generate manifest → compute file hashes → sign with `ed25519` → publish bundle + manifest + signature.

Device verification
- Verify signature → validate hashes/sizes → apply to staging → reboot and health-check → commit or rollback.
- Health checks: watchdog, PoD pass, permit loop unaffected.

Operational practices
- Separate dev/staging/prod keys; minimal blast radius.
- Time-based revocation window; require manual physical presence to re-enable OTA after a rollback.

