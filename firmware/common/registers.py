# Minimal in-memory register map for Modbus-style access
# Addresses are placeholders; actual bus implementation added later

# Device info
REG_DEVICE_TYPE = 0x0000  # 1 = boiler node
REG_FW_VERSION  = 0x0001  # integer x.y.z encoded

# Status and measurements (RO)
REG_STATUS_BITS         = 0x0010  # bit0:heater_on, bit1:pump_on, bit2:tank_low, bit3:fault
REG_BOILER_PRESSURE_MBAR= 0x0011
REG_BOILER_TEMP_C10     = 0x0012  # temp * 10
REG_TANK_PERCENT_0_1000 = 0x0013  # 0..1000

# Counters (RO)
REG_HEATER_CYCLES = 0x0020
REG_PUMP_SECONDS  = 0x0021

# Heartbeat (RW)
REG_MASTER_HEARTBEAT_MS = 0x00F0

# Advisory (RW)
REG_ADVISORY_BITS      = 0x0200  # bit0 predictive_stop_request
REG_PREDICTIVE_STOP_MS = 0x0201  # ETA until stop in ms (advisory)

# Commands (RW)
REG_FEATURE_FLAGS = 0x0100  # bitmask per feature_flags.FLAG_ORDER
REG_COMMAND_BITS  = 0x0101  # bit0:request_heat_enable (node may clamp)
REG_COMMAND_TTL_MS= 0x0102  # commands valid window
REG_COMMAND_SEQ   = 0x0103  # last accepted seq (RO)

class RegisterMap:
    def __init__(self):
        self.holding = {}
        self.seq = 0
        # defaults
        self.holding[REG_DEVICE_TYPE] = 1
        self.holding[REG_FW_VERSION] = 0x000100  # 0.1.0
        self.holding[REG_COMMAND_TTL_MS] = 2000
        self.holding[REG_MASTER_HEARTBEAT_MS] = 0
        self.holding[REG_ADVISORY_BITS] = 0
        self.holding[REG_PREDICTIVE_STOP_MS] = 0
        self.holding[REG_FEATURE_FLAGS] = 0
        self.holding[REG_COMMAND_BITS] = 0

    def read(self, addr: int) -> int:
        return int(self.holding.get(addr, 0))

    def write(self, addr: int, value: int, seq: int = None, now_ms: int = None) -> bool:
        # In-node guard: only allow safe writes
        if addr in (REG_DEVICE_TYPE, REG_FW_VERSION, REG_STATUS_BITS, REG_HEATER_CYCLES, REG_PUMP_SECONDS,
                    REG_BOILER_PRESSURE_MBAR, REG_BOILER_TEMP_C10, REG_TANK_PERCENT_0_1000, REG_COMMAND_SEQ):
            return False
        if addr == REG_COMMAND_BITS and seq is not None and now_ms is not None:
            ttl = self.read(REG_COMMAND_TTL_MS)
            if ttl <= 0:
                return False
            # store last accepted sequence
            self.holding[REG_COMMAND_BITS] = value & 0xFFFF
            self.holding[REG_COMMAND_SEQ] = seq & 0xFFFF
            return True
        self.holding[addr] = value & 0xFFFF
        return True

