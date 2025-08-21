# BLE Scale Manager (ESP32-S3 MicroPython)
# Central role: scan, connect, subscribe; vendor-specific drivers translate characteristics.

import time
try:
	from micropython import const
except Exception:
	def const(x):
		return x

try:
	import bluetooth
except ImportError:
	bluetooth = None

_DEFN_COMPLETE_LOCAL_NAME = const(0x09)
PROP_NOTIFY = const(0x10)


def _adv_name(adv_data: bytes) -> str | None:
	i = 0
	while i + 1 < len(adv_data):
		length = adv_data[i]
		if length == 0:
			break
		t = adv_data[i + 1]
		if t == _DEFN_COMPLETE_LOCAL_NAME:
			name = adv_data[i + 2 : i + 1 + length]
			try:
				return name.decode()
			except Exception:
				return None
		i += 1 + length
	return None


class BleScaleManager:
	def __init__(self, ble=None, scan_interval_ms=30000):
		self.ble = ble or (bluetooth.BLE() if bluetooth else None)
		self.scan_interval_ms = scan_interval_ms
		self.last_scan = 0
		self.connected = {}   # addr(bytes) -> {'conn':int, 'driver':obj, 'weight':float|None, 'last':ms, 'ranges':list}
		self.candidates = {}  # addr(bytes) -> driver
		self.drivers = []
		self.primary_addr = None
		if self.ble:
			self.ble.active(True)
			self.ble.irq(self._irq)

	def register_driver(self, driver_cls):
		if not self.ble:
			return
		self.drivers.append(driver_cls(self.ble))

	def _irq(self, event, data):
		if event == bluetooth._IRQ_SCAN_RESULT:
			addr_type, addr, adv_type, rssi, adv_data = data
			name = _adv_name(adv_data) or ""
			for d in self.drivers:
				if hasattr(d, "matches") and d.matches(name):
					self.candidates[bytes(addr)] = d
		elif event == bluetooth._IRQ_SCAN_DONE:
			# Connect to the first candidate not already connected
			for addr, d in list(self.candidates.items()):
				if addr not in self.connected:
					try:
						self.ble.gap_connect(0, addr)
						break
					except Exception:
						pass
		elif event == bluetooth._IRQ_PERIPHERAL_CONNECT:
			conn_handle, addr_type, addr = data
			key = bytes(addr)
			drv = self.candidates.get(key)
			if drv:
				self.connected[key] = {"conn": conn_handle, "driver": drv, "weight": None, "last": time.ticks_ms(), "ranges": []}
				try:
					drv.on_connected(conn_handle)
				except Exception:
					pass
				if self.primary_addr is None:
					self.primary_addr = key
				# Discover services then characteristics
				try:
					self.ble.gattc_discover_services(conn_handle)
				except Exception:
					pass
		elif event == bluetooth._IRQ_PERIPHERAL_DISCONNECT:
			conn_handle, addr_type, addr = data
			key = bytes(addr)
			if key in self.connected:
				del self.connected[key]
			if self.primary_addr == key:
				self.primary_addr = None
		elif event == bluetooth._IRQ_GATTC_SERVICE_RESULT:
			conn_handle, start_handle, end_handle, uuid = data
			# Record ranges for later characteristic discovery
			for info in self.connected.values():
				if info["conn"] == conn_handle:
					info["ranges"].append((start_handle, end_handle))
					break
		elif event == bluetooth._IRQ_GATTC_SERVICE_DONE:
			conn_handle, status = data
			# Discover characteristics in recorded ranges; fallback to full range
			ranges = None
			for info in self.connected.values():
				if info["conn"] == conn_handle:
					ranges = info.get("ranges") or []
					break
			try:
				if ranges:
					for (start, end) in ranges:
						self.ble.gattc_discover_characteristics(conn_handle, start, end)
				else:
					self.ble.gattc_discover_characteristics(conn_handle, 1, 0xFFFF)
			except Exception:
				pass
		elif event == bluetooth._IRQ_GATTC_CHARACTERISTIC_RESULT:
			conn_handle, def_handle, value_handle, properties, uuid = data
			# Enable notify if available; CCCD is usually value_handle + 1
			if properties & PROP_NOTIFY:
				try:
					self.ble.gattc_write(conn_handle, value_handle + 1, b"\x01\x00", 1)
				except Exception:
					pass
		elif event == bluetooth._IRQ_GATTC_CHARACTERISTIC_DONE:
			# nothing to do; wait for notifications
			pass
		elif event == bluetooth._IRQ_GATTC_NOTIFY:
			conn_handle, value_handle, notify_data = data
			# Route to driver; fallback to heuristic parsing
			for key, info in self.connected.items():
				if info["conn"] == conn_handle:
					try:
						w = info["driver"].on_notify(conn_handle, value_handle, notify_data)
						if w is None:
							w = self._parse_weight_guess(notify_data)
						if w is not None:
							info["weight"] = w
							info["last"] = time.ticks_ms()
					except Exception:
						pass
					break

	def _parse_weight_guess(self, data: bytes):
		# Try int16 little (g*10), then float32 little
		try:
			if len(data) >= 2:
				v = int.from_bytes(data[:2], "little", signed=True)
				if -20000 < v < 20000:
					return v / 10.0 if abs(v) > 100 else float(v)
		except Exception:
			pass
		try:
			if len(data) >= 4:
				import struct
				f = struct.unpack("<f", data[:4])[0]
				if -5000.0 < f < 5000.0:
					return float(f)
		except Exception:
			pass
		return None

	def start(self):
		if not self.ble:
			return
		now = time.ticks_ms()
		if time.ticks_diff(now, self.last_scan) > self.scan_interval_ms:
			self.last_scan = now
			try:
				self.ble.gap_scan(3000, 30000, 30000)
			except Exception:
				pass

	def poll(self):
		# Trigger scans periodically
		self.start()

	def primary_weight(self) -> float | None:
		if self.primary_addr and self.primary_addr in self.connected:
			return self.connected[self.primary_addr]["weight"]
		# else return any recent weight
		best = None
		best_ts = 0
		for info in self.connected.values():
			if info["weight"] is not None and time.ticks_diff(time.ticks_ms(), info["last"]) < 5000:
				if info["last"] > best_ts:
					best = info["weight"]
					best_ts = info["last"]
		return best

