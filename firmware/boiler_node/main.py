# MicroPython firmware skeleton – Boiler/Steam Node (ESP32‑WROOM‑32E)
# Safety-first design: mechanical protections remain primary. This node supervises and actuates within safe bounds.

import uasyncio as asyncio
from machine import Pin, WDT

import config
from safety_state import SafetyStateMachine
from machine import UART
from firmware.common.modbus_rtu import ModbusServer
try:
    from firmware.common import feature_flags, registers
    from firmware.common.modbus_rtu import ModbusServer
except ImportError:
    import sys
    sys.path.append("/firmware/common")
    import feature_flags, registers

class BoilerController:
    def __init__(self):
        self.wdt = WDT(timeout=config.WATCHDOG_TIMEOUT_MS)
        self.heater = Pin(config.PIN_HEATER_SSR, Pin.OUT, value=0)
        self.pump = Pin(config.PIN_PUMP_RELAY, Pin.OUT, value=0)
        self.tank_low = Pin(config.PIN_TANK_SWITCH, Pin.IN, Pin.PULL_UP)
        self.water_permit = Pin(config.PIN_WATER_PERMIT_IN, Pin.IN, Pin.PULL_UP)
        self.state_machine = SafetyStateMachine()
        self.reg = registers.RegisterMap()
        # Initialize PoD status: config_ok (bit0) assumed true at boot until checks fail
        self.reg.holding[registers.REG_POD_STATUS_BITS] = 1
        self.flags = feature_flags.default_flags.copy()
        self.uart = UART(config.UART_PORT, baudrate=config.UART_BAUD, tx=config.UART_TX_PIN, rx=config.UART_RX_PIN)
        self.mb = ModbusServer(self.uart, config.MODBUS_SLAVE_ID, self.reg)

    async def watchdog_task(self):
        while True:
            self.wdt.feed()
            await asyncio.sleep(1)

    def set_heater(self, on: bool) -> None:
        self.heater.value(1 if on else 0)

    def set_pump(self, on: bool) -> None:
        self.pump.value(1 if on else 0)

    def is_tank_low(self) -> bool:
        return self.tank_low.value() == 0

    def is_water_permit_ok(self) -> bool:
        # Active-low permit input typical; verify wiring.
        return self.water_permit.value() == 0
        # Microswitch wiring is often active-low; verify on hardware.
        return self.tank_low.value() == 0

    async def safety_supervisor(self):
        # Update status/telemetry registers
        # Minimal supervisor placeholder: inhibit outputs on low water
        while True:
            inhibit = self.is_tank_low() or (config.ENABLE_WATER_PERMIT and not self.is_water_permit_ok())
            if inhibit:
                self.set_heater(False)
                self.set_pump(False)
                        # Update status bits
            status = 0
            if self.heater.value(): status |= 1<<0
            if self.pump.value():   status |= 1<<1
            if self.is_tank_low():  status |= 1<<2
            if config.ENABLE_WATER_PERMIT and self.is_water_permit_ok(): status |= 1<<3
            self.reg.holding[registers.REG_STATUS_BITS] = status
            await asyncio.sleep_ms(100)

    
    async def modbus_task(self):
        while True:
            self.mb.poll()
            await asyncio.sleep_ms(5)

    async def ttl_supervisor(self):
        # Enforce TTL and heartbeat: ignore/clear remote commands when TTL=0 or heartbeat stale
        while True:
            ttl = self.reg.read(registers.REG_COMMAND_TTL_MS)
            hb = self.reg.read(registers.REG_MASTER_HEARTBEAT_MS)
            if ttl <= 0 or hb > config.HEARTBEAT_TIMEOUT_MS:
                # Disable remote command bits if TTL disabled or heartbeat stale
                self.reg.holding[registers.REG_COMMAND_BITS] = 0
            await asyncio.sleep_ms(200)
    async def main_loop(self):
        asyncio.create_task(self.watchdog_task())
        asyncio.create_task(self.safety_supervisor())
        asyncio.create_task(self.modbus_task())
        asyncio.create_task(self.ttl_supervisor())
        await self.state_machine.run()

async def main():
    ctrl = BoilerController()
    await ctrl.main_loop()

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

