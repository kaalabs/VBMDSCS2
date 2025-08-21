# Simple heartbeat writer stub for bench testing (to run on another MCU or host with UART bridge)
# This module assumes access to the same Modbus RTU server. It periodically writes REG_MASTER_HEARTBEAT_MS.

import time

def write_register(uart_write_fn, slave_id: int, addr: int, value: int):
    # Build Modbus FC06 frame
    def crc16(data):
        POLY = 0xA001
        crc = 0xFFFF
        for b in data:
            crc ^= b
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ POLY
                else:
                    crc >>= 1
        return crc & 0xFFFF
    payload = bytes([slave_id & 0xFF, 6, (addr>>8)&0xFF, addr&0xFF, (value>>8)&0xFF, value&0xFF])
    c = crc16(payload)
    frame = payload + bytes([c & 0xFF, (c>>8)&0xFF])
    uart_write_fn(frame)

# Example usage (pseudocode):
# from machine import UART
# import registers
# uart = UART(1, baudrate=115200, tx=17, rx=16)
# while True:
#     write_register(uart.write, 1, registers.REG_MASTER_HEARTBEAT_MS, 0)
#     time.sleep_ms(200)
#     # Master increments this value to indicate elapsed ms since last reset
#     # Node treats value > HEARTBEAT_TIMEOUT_MS as stale
