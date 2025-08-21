# BLE Scale Manager (ESP32-S3 MicroPython placeholder)
# Central role: scan, connect, subscribe; vendor-specific drivers translate characteristics.

try:
	import bluetooth
except ImportError:
	bluetooth = None

class BleScaleManager:
	def __init__(self, ble=None):
		self.ble = ble or (bluetooth.BLE() if bluetooth else None)
		self.drivers = []  # instances of vendor drivers
		self.connected = {}

	def register_driver(self, driver_cls):
		self.drivers.append(driver_cls(self.ble))

	def start(self):
		if not self.ble:
			return
		# TODO: implement scan and connect orchestration

	def poll(self):
		# Placeholder for periodic processing
		pass

