# Minimal Modbus RTU (subset) for MicroPython: FC03 Read Holding, FC06 Write Single
# CRC16 implementation and a simple state machine for a single UART.
# NOTE: For prototype/testing; production should harden framing and timing.

import struct

POLY = 0xA001

def crc16(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLY
            else:
                crc >>= 1
    return crc & 0xFFFF

class ModbusServer:
    def __init__(self, uart, slave_id: int, regmap):
        self.uart = uart
        self.slave_id = slave_id & 0xFF
        self.regmap = regmap
        self.buf = bytearray()

    def _read_registers(self, addr, count):
        values = []
        for i in range(count):
            values.append(self.regmap.read(addr + i) & 0xFFFF)
        return values

    def _write_register(self, addr, value):
        # For write, the caller should provide seq/now in regmap.write if needed.
        return self.regmap.write(addr, value)

    def poll(self):
        # Non-blocking poll; read available bytes and parse frames
        n = self.uart.any()
        if not n:
            return
        self.buf.extend(self.uart.read(n) or b"")
        # Try to parse complete frames
        while len(self.buf) >= 8:
            # Find our slave id
            if self.buf[0] != self.slave_id:
                self.buf.pop(0)
                continue
            if len(self.buf) < 8:
                break
            slave, func = self.buf[0], self.buf[1]
            if func == 3 and len(self.buf) >= 8:
                addr, count = struct.unpack('>HH', self.buf[2:6])
                frame = self.buf[:6]
                recv_crc = self.buf[6] | (self.buf[7] << 8)
                calc = crc16(frame)
                if recv_crc != calc:
                    self.buf.pop(0)
                    continue
                # Build response
                vals = self._read_registers(addr, count)
                payload = bytes([self.slave_id, 3, len(vals)*2]) + struct.pack('>'+'H'*len(vals), *vals)
                c = crc16(payload)
                resp = payload + bytes([c & 0xFF, (c >> 8) & 0xFF])
                self.uart.write(resp)
                del self.buf[:8]
            elif func == 6 and len(self.buf) >= 8:
                addr, value = struct.unpack('>HH', self.buf[2:6])
                frame = self.buf[:6]
                recv_crc = self.buf[6] | (self.buf[7] << 8)
                calc = crc16(frame)
                if recv_crc != calc:
                    self.buf.pop(0)
                    continue
                ok = self._write_register(addr, value)
                # Echo write on success
                payload = bytes([self.slave_id, 6]) + self.buf[2:6]
                c = crc16(payload)
                resp = payload + bytes([c & 0xFF, (c >> 8) & 0xFF])
                self.uart.write(resp)
                del self.buf[:8]
            else:
                # Unsupported function; drop one byte
                self.buf.pop(0)

