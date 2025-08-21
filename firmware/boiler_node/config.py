# Pin assignments (adjust per board wiring)
PIN_HEATER_SSR = 25
PIN_PUMP_RELAY = 26
PIN_TANK_SWITCH = 27  # microswitch, active-low typical; verify

# Supervisor thresholds
PRESSURE_SOFT_LIMIT_BAR = 1.5
MAX_BOILER_TEMP_C = 135.0

# Watchdog
WATCHDOG_TIMEOUT_MS = 8000

PIN_BREW_SWITCH = 14  # brew lever microswitch (active-low typical); verify on hardware
DEBOUNCE_MS = 20

# Bus configuration
MODBUS_SLAVE_ID = 1
UART_PORT = 1
UART_BAUD = 115200
UART_TX_PIN = 17
UART_RX_PIN = 16
HEARTBEAT_TIMEOUT_MS = 5000

# External water permit input (from Tank Node)
PIN_WATER_PERMIT_IN = 23
ENABLE_WATER_PERMIT = True
