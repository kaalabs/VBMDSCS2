# Tank/Water Node configuration
# Inputs
PIN_TANK_SWITCH = 4      # factory microswitch (active-low typical)
PIN_ULTRASONIC_TX = 5    # if using UART-based DYP, TX
PIN_ULTRASONIC_RX = 18   # if using UART-based DYP, RX

# Outputs (fail-safe permit)
PIN_WATER_PERMIT_OC = 19 # open-collector/low=permit; high-Z= inhibit (use external pull-up)
PIN_BUZZER = 21
PIN_LED = 22

# Bus configuration
MODBUS_SLAVE_ID = 2
UART_PORT = 1
UART_BAUD = 115200
UART_TX_PIN = 17
UART_RX_PIN = 16

# Time constants
DEBOUNCE_MS = 20
PERMIT_RELEASE_MS = 100   # time to release permit after low water detected
HEARTBEAT_TIMEOUT_MS = 5000
