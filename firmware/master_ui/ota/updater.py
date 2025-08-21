# MicroPython OTA updater skeleton (master UI)
# - Fetch bundle (manifest + files) over HTTPS or local file
# - Verify Ed25519 signature and file hashes
# - Stage under /storage/ota/bundle, swap atomically, reboot

import ujson as json
import uhashlib as hashlib
import os

from firmware.common import ed25519_verify

class OtaUpdater:
	def __init__(self, public_keys: dict):
		self.public_keys = public_keys  # key_id -> bytes

	def verify_manifest(self, manifest_bytes: bytes, signature: bytes) -> dict:
		m = json.loads(manifest_bytes)
		key_id = m.get('key_id')
		pk = self.public_keys.get(key_id)
		if not pk:
			raise ValueError('unknown key_id')
		if not ed25519_verify.verify(signature, manifest_bytes, pk):
			raise ValueError('signature verify failed')
		return m

	def verify_file(self, path: str, expected_sha256: str, expected_size: int) -> None:
		h = hashlib.sha256()
		sz = 0
		with open(path, 'rb') as f:
			while True:
				b = f.read(4096)
				if not b:
					break
				h.update(b)
				sz += len(b)
		if sz != expected_size:
			raise ValueError('size mismatch')
		digest = h.digest()
		if digest.hex() != expected_sha256.lower():
			raise ValueError('sha256 mismatch')

	def stage_bundle(self, manifest: dict, base_dir: str) -> None:
		# Verify each file
		for f in manifest.get('files', []):
			self.verify_file(os.path.join(base_dir, f['path']), f['sha256'], f['size'])
		# TODO: atomically swap current bundle pointer to new base_dir and request reboot

