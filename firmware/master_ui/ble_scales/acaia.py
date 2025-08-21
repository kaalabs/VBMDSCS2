# Acaia BLE scale driver skeleton (placeholder)
class AcaiaDriver:
	NAME_PATTERNS = ['Lunar', 'Acaia']
	NAME_PREFIX = "Acaia"
	def __init__(self, ble):
		self.ble = ble
		self.device = None
		self.weight_g = None
		self.rate_gs = None
		self.stable = False
		self.battery = None

	def matches(self, name: str) -> bool:
		# naive name prefix match; refine with UUIDs later Acaia
		return any(name.upper().startswith(p.upper()) for p in getattr(self, "NAME_PATTERNS", [self.NAME_PREFIX]))

	def connect(self, dev):
		self.device = dev
		# TODO: discover services/characteristics and subscribe

	def process(self):
		# TODO: parse notifications and update weight/time
		pass



	def on_connected(self, conn_handle):
		# TODO: discover and enable notifications on weight characteristic
		pass

	def on_notify(self, conn_handle, value_handle, data: bytes):
		# TODO: parse vendor format; return weight in grams if available
		return None


	# TODO: fill after GATT probe
	SERVICE_UUID = None
	WEIGHT_CHAR_UUID = None
