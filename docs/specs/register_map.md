# Node Register Map (Boiler/Steam Node v0.1)

Access model
- Transport: RS‑485 (Modbus RTU planned); this map defines logical 16‑bit holding registers.
- Endianness: 16‑bit values; multi‑word types not used yet.
- Permissions: RO (read‑only), RW (read/write). Nodes may clamp or reject unsafe writes.
- Safety: Commands honor a TTL window and immutable safety envelopes; core autonomy is preserved on comms loss.

Device information (RO)

| Address | Name           | Type | Units | Description |
| ---: | --- | --- | --- | --- |
| 0x0000 | REG_DEVICE_TYPE | RO   | –     | 1 = Boiler/Steam node |
| 0x0001 | REG_FW_VERSION  | RO   | –     | Version encoded as (major<<8)|(minor<<4)|patch, e.g. 0x010 for 0.1.0 |

Status and measurements (RO)

| Address | Name                    | Type | Units  | Description |
| ---: | --- | --- | --- | --- |
| 0x0010 | REG_STATUS_BITS          | RO   | bitset | bit0 heater_on; bit1 pump_on; bit2 tank_low; bit3 fault |
| 0x0011 | REG_BOILER_PRESSURE_MBAR | RO   | mbar   | Boiler pressure; 0..3000 mbar typical |
| 0x0012 | REG_BOILER_TEMP_C10      | RO   | 0.1 °C | Boiler temp ×10 |
| 0x0013 | REG_TANK_PERCENT_0_1000  | RO   | 0.1 %  | Tank level; 0..1000 (optional, requires ultrasonic sensor) |

Counters (RO)

| Address | Name             | Type | Units | Description |
| ---: | --- | --- | --- | --- |
| 0x0020 | REG_HEATER_CYCLES | RO   | count | Cumulative heater on→off transitions |
| 0x0021 | REG_PUMP_SECONDS  | RO   | s     | Cumulative pump on‑time |

Commands and configuration (RW unless noted)

| Address | Name             | Type | Units | Description |
| ---: | --- | --- | --- | --- |
| 0x0100 | REG_FEATURE_FLAGS | RW   | bitset | Feature bitmask per `feature_flags.FLAG_ORDER`. Unsupported features are ignored. |
| 0x0101 | REG_COMMAND_BITS  | RW   | bitset | bit0 request_heat_enable (node may clamp). Writes require valid TTL; acceptance updates `REG_COMMAND_SEQ`. |
| 0x0102 | REG_COMMAND_TTL_MS| RW   | ms    | TTL for command validity (default 2000 ms). If 0, remote commands are disabled. |
| 0x0103 | REG_COMMAND_SEQ   | RO   | –     | Last accepted command sequence (monotonic, 16‑bit wrap). |

Guardrails and semantics
- Nodes ignore writes to RO addresses; invalid writes return an error at protocol level when implemented.
- TTL enforcement: Commands applied only when received within `REG_COMMAND_TTL_MS` of issuance; expired commands are ignored.
- Safety envelopes: Firmware ignores or clamps commands that would exceed internal limits (e.g., boiler pressure/temperature bounds, low‑water interlock). Mechanical safeties remain primary.
- Autonomy on comms loss: If master bus is lost (no heartbeats), node continues in safe autonomous control; setpoints revert to local defaults.

Forward allocation (reserved)
- 0x0200–0x02FF: Volumetric assist, flowmeter, brew pressure telemetry.
- 0x0300–0x03FF: Diagnostics/service, fault codes, trend data.



Advisories (RW)

| Address | Name | Type | Units | Description |
| ---: | --- | --- | --- | --- |
| 0x0200 | REG_ADVISORY_BITS | RW | bitset | bit0 predictive_stop_request |
| 0x0201 | REG_PREDICTIVE_STOP_MS | RW | ms | ETA until stop suggested by master (advisory only) |


Tank/Water node (concept)
- Follows the same register semantics for status/counters and heartbeat.
- Status bits for: permit_on, tank_low_raw, low_latched.
- Master may read percentage if ultrasonic sensor is present; still advisory only.


## Tank/Water Node Register Map (v0.1)

Device information (RO)

| Address | Name           | Type | Units | Description |
| ---: | --- | --- | --- | --- |
| 0x0000 | REG_DEVICE_TYPE | RO   | –     | 2 = Tank/Water node |
| 0x0001 | REG_FW_VERSION  | RO   | –     | Version encoded as (major<<8)|(minor<<4)|patch |

Status and measurements (RO)

| Address | Name                     | Type | Units  | Description |
| ---: | --- | --- | --- | --- |
| 0x0010 | REG_STATUS_BITS           | RO   | bitset | bit0 permit_on; bit1 tank_low_raw; bit2 low_latched |
| 0x0013 | REG_TANK_PERCENT_0_1000   | RO   | 0.1 %  | Tank level; 0..1000 (requires ultrasonic) |

Counters (RO)

| Address | Name                 | Type | Units | Description |
| ---: | --- | --- | --- | --- |
| 0x0022 | REG_LOW_EVENTS        | RO   | count | Number of low-water latch events |
| 0x0023 | REG_PERMIT_SECONDS    | RO   | s     | Cumulative seconds with permit asserted |

Commands and configuration (RW unless noted)

| Address | Name              | Type | Units | Description |
| ---: | --- | --- | --- | --- |
| 0x0100 | REG_FEATURE_FLAGS  | RW   | bitset | e.g., enable ultrasonic sensor (if present) |
| 0x0102 | REG_COMMAND_TTL_MS | RW   | ms    | TTL for write validity; 0 disables remote writes |
| 0x00F0 | REG_MASTER_HEARTBEAT_MS | RW | ms | Master heartbeat age (written by master periodically) |

Guardrails and semantics
- Permit is hardware-enforced; registers are advisory/telemetry only.
- Latching: `low_latched` requires explicit service action (or policy-defined clear) before permit can assert again.


Power-on Diagnostics registers (per node)

| Address | Name                | Type | Units | Description |
| ---: | --- | --- | --- | --- |
| 0x0040 | REG_POD_STATUS_BITS  | RO   | bitset | bit0 config_ok; bit1 comms_ok; bit2 sensors_ok; bit3 outputs_safe; bit4 permit_seen (where applicable) |
| 0x0041 | REG_LAST_RESET_CAUSE | RO   | –     | Encoded last reset cause |
