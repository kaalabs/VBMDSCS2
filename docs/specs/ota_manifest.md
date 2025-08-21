# OTA Manifest (Application-layer bundle)

Format: JSON, detached signature with Ed25519 over the canonicalized manifest bytes.

Example
```json
{
  "manifest_version": 1,
  "bundle_version": "0.1.0",
  "device_type": "master_ui|boiler_node|tank_node",
  "min_fw_version": "0.1.0",
  "created_utc": "2025-01-01T12:00:00Z",
  "key_id": "ed25519-prod-2025",
  "sig_alg": "ed25519",
  "files": [
    { "path": "app/main.py", "sha256": "...", "size": 12345 },
    { "path": "app/lib/util.py", "sha256": "...", "size": 2345 }
  ]
}
```

Signature
- Detached; base64url-encoded in distribution metadata alongside manifest.
- Field name: `signature` (outside the signed object) or carried in a sidecar file `manifest.sig`.
- Verification: compute SHA-256 over raw manifest bytes (no whitespace changes), verify Ed25519 signature with trusted public key for `key_id`.

On-device verification
- Check `device_type` matches node role.
- Check running firmware version >= `min_fw_version`.
- Verify Ed25519 signature with known public key by `key_id`.
- Recompute SHA-256 for each file after download; sizes must match.
- Apply atomically (write to `/ota/bundle/` then swap symlink/config and reboot).

Rollback
- Store previous bundle path; if post-boot health checks fail, restore previous and relock.

