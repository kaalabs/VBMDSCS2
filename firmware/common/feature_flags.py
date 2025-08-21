# Feature flags for node autonomy and optional features
# Defaults are conservative and local-only

default_flags = {
    # Core guards
    "ENABLE_BREW_INTERLOCK": True,         # Lever + low-water required for pump
    "ENABLE_COMMAND_TTL": True,            # Ignore expired master commands
    "ALLOW_REMOTE_CONTROL": False,         # Local-only by default
    # UX-only features
    "ENABLE_SHOT_TIMER": True,
    "ENABLE_TELEMETRY": True,
    "ENABLE_WARMUP_PROFILES": False,
    "ENABLE_HX_FLUSH_COACH": False,
    "ENABLE_ENERGY_MODES": False,
    # Sensors/hardware extensions
    "ENABLE_GROUPHEAD_TEMP": False,
    "ENABLE_FLOWMETER": False,
    "ENABLE_BREW_PRESSURE_SENSOR": False,
    "ENABLE_ULTRASONIC_TANK_SENSOR": False,

    "ENABLE_BLE_SCALES": False,
    "ENABLE_WEIGHT_TRIGGER_TIMER": False,
    "ENABLE_PREDICTIVE_STOP": False,
    "ENABLE_RATIO_COACH": False,
}

FLAG_ORDER = list(default_flags.keys())


def to_bitmask(flags: dict) -> int:
    mask = 0
    for i, name in enumerate(FLAG_ORDER):
        if flags.get(name, default_flags[name]):
            mask |= (1 << i)
    return mask


def from_bitmask(mask: int) -> dict:
    result = {}
    for i, name in enumerate(FLAG_ORDER):
        result[name] = bool((mask >> i) & 1)
    return result

