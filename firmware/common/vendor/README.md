# Vendor crypto

Place a minimal Ed25519 implementation here (e.g., a MicroPython-compatible port of TweetNaCl) exposing:

```python
def verify(signature: bytes, message: bytes, public_key: bytes) -> None:
    # Raise on failure; return None on success
```

Then adjust `ed25519_verify.py` to import it as `ued25519`.
