# Master/UI main loop (prototype): heartbeat, read status, run shot logic, write predictive stop advisory

import time
from machine import UART
from firmware.common import registers
from firmware.master_ui.shot_logic import ShotLogic
from firmware.master_ui.ota.boot_handler import commit_or_rollback
from firmware.master_ui.ble_scales.manager import BleScaleManager
from firmware.master_ui.ble_scales.acaia import AcaiaDriver
from firmware.master_ui.ble_scales.bookoo import BookooDriver
from firmware.master_ui.ble_scales.halfdecent import HalfDecentDriver
from tools.modbus_cli import crc16  # reuse CRC for quick framing on device, or reimplement inline

SLAVE_ID = 1
TANK_ID = 2
UART_PORT = 1
UART_BAUD = 115200
UART_TX = 17
UART_RX = 16

# Minimal FC03/FC06 inline to avoid full CLI overhead

def fc03_read(uart, addr, count, slave=None):
    sid = SLAVE_ID if slave is None else slave
    payload = bytes([sid, 3, (addr>>8)&0xFF, addr&0xFF, (count>>8)&0xFF, count&0xFF])
    payload = payload
    c = crc16(payload)
    uart.write(payload + bytes([c & 0xFF, (c>>8)&0xFF]))
    t0 = time.ticks_ms()
    # crude read: wait for header then read rest
    while uart.any() < 3 and time.ticks_diff(time.ticks_ms(), t0) < 500:
        pass
    hdr = uart.read(3) or b"\x00\x00\x00"
    if len(hdr) < 3:
        return []
    _, _, bc = hdr
    data = uart.read(bc) or b""
    uart.read(2)  # crc discard
    if len(data) != bc:
        return []
    vals = []
    for i in range(0, bc, 2):
        vals.append((data[i]<<8) | data[i+1])
    return vals

def fc06_write(uart, addr, value):
    payload = bytes([SLAVE_ID, 6, (addr>>8)&0xFF, addr&0xFF, (value>>8)&0xFF, value&0xFF])
    c = crc16(payload)
    uart.write(payload + bytes([c & 0xFF, (c>>8)&0xFF]))
    # ignore echo
    time.sleep_ms(10)


def main():
    ble = BleScaleManager()
    ble.register_driver(AcaiaDriver)
    ble.register_driver(BookooDriver)
    ble.register_driver(HalfDecentDriver)
    uart = UART(UART_PORT, baudrate=UART_BAUD, tx=UART_TX, rx=UART_RX)
    def health_ok():
        # Read PoD status from boiler and tank; consider OK if both respond
        try:
            pod_boiler = fc03_read(uart, registers.REG_POD_STATUS_BITS, 1)
            pod_tank = fc03_read(uart, registers.REG_POD_STATUS_BITS, 1, slave=TANK_ID)
        except Exception:
            return False
        if not (pod_boiler and pod_tank):
            return False
        b = pod_boiler[0]
        t = pod_tank[0]
        # bits: 0 cfg, 1 comms, 2 sensors, 3 outputs_safe, 4 permit_seen
        def ok(bits):
            return (bits & (1<<1)) and (bits & (1<<2)) and (bits & (1<<3))
        return ok(b) and ok(t)

    # Commit or rollback based on health within grace period
    commit_or_rollback(health_ok)

    shot = ShotLogic()
    t_prev = time.ticks_ms()
    # set TTL to a sane value
    fc06_write(uart, registers.REG_COMMAND_TTL_MS, 2000)
    while True:
        # Heartbeat increments (age in ms), node treats large values as stale
        fc06_write(uart, registers.REG_MASTER_HEARTBEAT_MS, 0)

        # Read status
        vals = fc03_read(uart, registers.REG_STATUS_BITS, 1)
        if not vals:
            time.sleep_ms(100)
            continue
        status = vals[0]
        pump_on = bool(status & (1<<1))
        tank_low = bool(status & (1<<2))

        now = time.ticks_ms()
        dt = time.ticks_diff(now, t_prev)
        t_prev = now

        ble.poll()
        weight = ble.primary_weight()
        weight = None

        # Shot logic: start/stop off pump state transitions
        if pump_on and not shot.running and not tank_low:
            shot.start(start_weight_g=0.0 if weight is None else weight)
        elif not pump_on and shot.running:
            shot.stop()

        if shot.running:
            shot.update(dt, weight)
            # Predictive stop advisory if enabled
            target = 36.0  # example target yield in grams
            eta = shot.predictive_stop_ms(target)
            if eta is not None and eta < 3000:
                fc06_write(uart, registers.REG_ADVISORY_BITS, 1)  # bit0 predictive_stop
                fc06_write(uart, registers.REG_PREDICTIVE_STOP_MS, int(eta) & 0xFFFF)
            else:
                fc06_write(uart, registers.REG_ADVISORY_BITS, 0)
        else:
            fc06_write(uart, registers.REG_ADVISORY_BITS, 0)
        time.sleep_ms(100)

if __name__ == '__main__':
    main()

