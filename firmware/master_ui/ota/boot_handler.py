# OTA boot handler: commit or rollback app-layer bundle after reboot
# Strategy:
# - On boot, read /storage/current_bundle.txt (target)
# - Run basic health checks (PoD pass, heartbeat up, minimal tasks start)
# - If ok within grace period, write /storage/last_good_bundle.txt and continue.
# - If not, restore last_good pointer and reset.

import os, time

POINTER = "/storage/current_bundle.txt"
LAST_GOOD = "/storage/last_good_bundle.txt"
GRACE_MS = 10000


def _read(path):
	try:
		with open(path, 'r') as f:
			return f.read().strip()
	except Exception:
		return None


def _write(path, val):
	with open(path + ".new", 'w') as f:
		f.write(val)
	os.rename(path + ".new", path)


def commit_or_rollback(health_ok_fn):
	target = _read(POINTER)
	if not target:
		return
	# Wait for health_ok
	t0 = time.ticks_ms()
	while time.ticks_diff(time.ticks_ms(), t0) < GRACE_MS:
		if health_ok_fn():
			# Commit
			_write(LAST_GOOD, target)
			return
		time.sleep_ms(200)
	# Rollback
	last = _read(LAST_GOOD)
	if last:
		_write(POINTER, last)
		import machine
		machine.reset()

