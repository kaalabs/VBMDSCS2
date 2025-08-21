# Tank/Water Node – provides fail-safe WATER_OK permit and telemetry

import uasyncio as asyncio
from machine import Pin, UART, WDT
import time

import config
from firmware.common import registers
from firmware.common.modbus_rtu import ModbusServer

class TankNode:
	def __init__(self):
		self.wdt = WDT(timeout=config.HEARTBEAT_TIMEOUT_MS)
		self.tank_sw = Pin(config.PIN_TANK_SWITCH, Pin.IN, Pin.PULL_UP)
		self.permit = Pin(config.PIN_WATER_PERMIT_OC, Pin.OUT, value=0)  # 0=permit asserted (pull-down), 1=hi-Z via external driver
		self.led = Pin(config.PIN_LED, Pin.OUT, value=0)
		self.buzzer = Pin(config.PIN_BUZZER, Pin.OUT, value=0)
		self.uart = UART(config.UART_PORT, baudrate=config.UART_BAUD, tx=config.UART_TX_PIN, rx=config.UART_RX_PIN)
		self.reg = registers.RegisterMap()
        # Initialize PoD status: config_ok (bit0) assumed true at boot until checks fail
        self.reg.holding[registers.REG_POD_STATUS_BITS] = 1
		self.mb = ModbusServer(self.uart, config.MODBUS_SLAVE_ID, self.reg)
		self.low_latched = False

	def is_tank_low(self) -> bool:
		return self.tank_sw.value() == 0

	def set_permit(self, ok: bool):
		# Fail-safe: permit asserted only when ok=True; default inhibit on boot/fault
		self.permit.value(0 if ok else 1)
		self.led.value(1 if not ok else 0)

	async def modbus_task(self):
		while True:
			self.mb.poll()
			await asyncio.sleep_ms(5)

	async def watchdog_task(self):
		while True:
			self.wdt.feed()
			await asyncio.sleep(1)

	async def supervisor(self):
		last_state = None
		last_change = time.ticks_ms()
		while True:
			raw = self.is_tank_low()
			now = time.ticks_ms()
			if raw != last_state:
				last_state = raw
				last_change = now
			stable_low = raw and time.ticks_diff(now, last_change) >= config.DEBOUNCE_MS
			if stable_low:
				self.low_latched = True
				self.set_permit(False)
			else:
				# Only clear latch if explicit write clears fault or after long stable OK (policy can evolve)
				if not self.low_latched:
					self.set_permit(True)
			# Update status register
			status = 0
			if self.permit.value() == 0: status |= 1<<0  # bit0 permit_on
			if raw: status |= 1<<1                    # bit1 tank_low_raw
			if self.low_latched: status |= 1<<2      # bit2 low_latched
			self.reg.holding[registers.REG_STATUS_BITS] = status
			await asyncio.sleep_ms(50)

	async def main(self):
		# Start in safe inhibit until first stable OK
		self.set_permit(False)
		asyncio.create_task(self.watchdog_task())
		asyncio.create_task(self.modbus_task())
		await self.supervisor()

async def main():
	node = TankNode()
	await node.main()

try:
	asyncio.run(main())
finally:
	asyncio.new_event_loop()

