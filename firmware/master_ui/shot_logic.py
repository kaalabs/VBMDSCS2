# Shot logic consuming brew lever, optional flowmeter, and BLE scale inputs
# Provides weight-triggered start/stop, predictive stop suggestions, and ratio coach hooks.

class ShotLogic:
	def __init__(self):
		self.reset()

	def reset(self):
		self.running = False
		self.t_ms = 0
		self.weight_g = 0.0
		self.start_weight_g = None
		self.target_g = None
		self.ratio_target = None
		self.history = []  # (ms, weight)

	def start(self, start_weight_g: float = 0.0):
		self.running = True
		self.t_ms = 0
		self.start_weight_g = start_weight_g
		self.weight_g = start_weight_g
		self.history.clear()

	def stop(self):
		self.running = False

	def update(self, dt_ms: int, weight_g: float | None):
		if not self.running:
			return
		self.t_ms += dt_ms
		if weight_g is not None:
			self.weight_g = weight_g
			self.history.append((self.t_ms, weight_g))

	def yield_g(self) -> float:
		if self.start_weight_g is None:
			return 0.0
		return max(0.0, self.weight_g - self.start_weight_g)

	def predictive_stop_ms(self, target_yield_g: float) -> int | None:
		# Simple linear forecast based on last N samples of dW/dt
		if len(self.history) < 3:
			return None
		N = min(10, len(self.history)-1)
		ws = [self.history[-i-1][1] for i in range(N)]
		ts = [self.history[-i-1][0] for i in range(N)]
		dw = ws[0] - ws[-1]
		dt = (ts[0] - ts[-1]) / 1000.0
		if dt <= 0:
			return None
		rate = dw / dt  # g/s
		if rate <= 0.1:
			return None
		remaining = max(0.0, target_yield_g - self.yield_g())
		return int(remaining / rate * 1000)

	def ratio(self, dose_g: float | None) -> float | None:
		if dose_g is None:
			return None
		if self.start_weight_g is None:
			return None
		return self.yield_g() / dose_g if dose_g > 0 else None

