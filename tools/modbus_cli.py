#!/usr/bin/env python3
import sys, struct, time
import serial

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

def fc03_read(ser, slave, addr, count):
    payload = bytes([slave, 3, (addr>>8)&0xFF, addr&0xFF, (count>>8)&0xFF, count&0xFF])
    c = crc16(payload)
    ser.write(payload + bytes([c & 0xFF, (c>>8)&0xFF]))
    hdr = ser.read(3)
    if len(hdr) < 3: raise RuntimeError('timeout')
    sid, func, bytecount = hdr
    data = ser.read(bytecount)
    crc = ser.read(2)
    if len(data) != bytecount or len(crc) != 2:
        raise RuntimeError('short read')
    return list(struct.unpack('>'+'H'*(bytecount//2), data))

def fc06_write(ser, slave, addr, value):
    payload = bytes([slave, 6, (addr>>8)&0xFF, addr&0xFF, (value>>8)&0xFF, value&0xFF])
    c = crc16(payload)
    ser.write(payload + bytes([c & 0xFF, (c>>8)&0xFF]))
    ack = ser.read(8)
    if len(ack) != 8: raise RuntimeError('timeout')

USAGE = """
Usage:
  modbus_cli.py /dev/tty.usbserial-XXXX 115200 read SLAVE ADDR COUNT
  modbus_cli.py /dev/tty.usbserial-XXXX 115200 write SLAVE ADDR VALUE
  modbus_cli.py /dev/tty.usbserial-XXXX 115200 heartbeat SLAVE ADDR PERIOD_MS
"""

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print(USAGE)
        sys.exit(1)
    port = sys.argv[1]
    baud = int(sys.argv[2])
    cmd = sys.argv[3]
    slave = int(sys.argv[4])
    ser = serial.Serial(port, baudrate=baud, timeout=0.5)
    if cmd == 'read':
        addr = int(sys.argv[5], 0)
        count = int(sys.argv[6])
        vals = fc03_read(ser, slave, addr, count)
        print(vals)
    elif cmd == 'write':
        addr = int(sys.argv[5], 0)
        value = int(sys.argv[6], 0)
        fc06_write(ser, slave, addr, value)
        print('OK')
    elif cmd == 'heartbeat':
        addr = int(sys.argv[5], 0)
        period = int(sys.argv[6])
        t0 = time.time()
        try:
            while True:
                elapsed_ms = int((time.time() - t0)*1000) & 0xFFFF
                fc06_write(ser, slave, addr, elapsed_ms)
                time.sleep(period/1000.0)
        except KeyboardInterrupt:
            pass
    else:
        print(USAGE)
        sys.exit(1)
