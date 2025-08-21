# Half Decent BLE scale driver skeleton (placeholder)
class HalfDecentDriver:
	NAME_PREFIX = "Half Decent"
	def __init__(self, ble):
		self.ble = ble
		self.device = None
		self.weight_g = None
		self.rate_gs = None
		self.stable = False
		self.battery = None

	def matches(self, adv):
		# TODO: parse adv to detect Half Decent
		return False

	def connect(self, dev):
		self.device = dev
		# TODO: discover services/characteristics and subscribe

	def process(self):
		# TODO: parse notifications and update weight/time
		pass

