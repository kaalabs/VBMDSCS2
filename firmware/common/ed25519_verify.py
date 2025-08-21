# Minimal Ed25519 verifier adapter for MicroPython
# Tries available micro-libs; fails closed if none present.
# API: verify(signature: bytes, message: bytes, public_key: bytes) -> bool

# Preferred: integrate a minimal Ed25519 impl (e.g., TweetNaCl port) and adapt here.

_def_backend = None

import sys
# Try known module names in MicroPython variants
try:
    sys.path.append("/firmware/common/vendor")
except Exception:
    pass
try:
    # Example placeholder; replace with actual module when vendored
    from ued25519 import verify as _mp_verify  # type: ignore
    _def_backend = 'ued25519'
    def verify(signature: bytes, message: bytes, public_key: bytes) -> bool:
        try:
            _mp_verify(signature, message, public_key)
            return True
        except Exception:
            return False
except Exception:
    pass

if _def_backend is None:
    try:
        # CPython/dev fallback if running on host with pure-python ed25519 module installed
        import ed25519  # type: ignore
        _def_backend = 'ed25519'
        def verify(signature: bytes, message: bytes, public_key: bytes) -> bool:
            try:
                vk = ed25519.VerifyingKey(public_key)
                vk.verify(signature, message)
                return True
            except Exception:
                return False
    except Exception:
        _def_backend = None

if _def_backend is None:
    def verify(signature: bytes, message: bytes, public_key: bytes) -> bool:
        # Fail closed: without a verifier, reject updates
        return False
