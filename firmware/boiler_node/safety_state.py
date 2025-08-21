import uasyncio as asyncio

class SafetyStateMachine:
	def __init__(self):
		self.state = "INIT"

	async def run(self):
		# Placeholder state machine loop
		while True:
			await asyncio.sleep(0.2)

