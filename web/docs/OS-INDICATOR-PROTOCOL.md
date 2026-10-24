Русский перевод: [Протокол индикатора OS](ru/OS-INDICATOR-PROTOCOL.md).

# OS indicator protocol

This development contract implements the firmware part of AKW-063.
`AK820_OS_INDICATORS` overrides only **OS**; C and W keep their existing roles.
Optional `AK820_MAC_PC` supplies normal OS state. Without it, normal is off.

The desktop helper and platform layout detectors are separate planned work.
A client must identify the exact image before sending FD02; VID/PID or an
arbitrary reply does not prove support. The [development catalog](CAPABILITY-CATALOG.md)
prepares identity data, without release or write authorization.

## Transport and request

Use the existing 32-byte Raw HID exchange. FD00, FD01 and USB descriptors are
unchanged. There is no new Feature Report or GETFEATURES. Other report lengths
are rejected by the existing USB handler.

FD02 bypasses NVM transactions and flushing, including malformed requests
and replies after an existing NVM fault. It neither unlocks Vial nor clears a
storage error or acknowledges another saved setter.

| Byte | Request value |
| --- | --- |
| 0–1 | `FD 02` |
| 2 | Version `01` |
| 3 | Action: `00` query, `01` set/refresh |
| 4 | Mode: `00` normal/release, `01` off, `02` on, `03` breathing |
| 5–31 | Zero |

Query requires mode zero and never refreshes the lease. Undefined versions,
actions, modes and nonzero reserved bytes are malformed: they do not change
or refresh the override. Expiry/unlock cancellation still applies independently.

## Reply

| Byte | Reply value |
| --- | --- |
| 0–1 | `FD 02` |
| 2 | Version `01` |
| 3 | Status: `00` accepted, `01` malformed, `02` unavailable |
| 4 | Effective override mode after expiry/cancellation |
| 5 | Marker `A8` |
| 6–7 | Lease, little endian: `B8 0B` = 3000 ms |
| 8–9 | Breathing period, little endian: `00 10` = 4096 ms |
| 10–31 | Zero |

Normal mode describes policy, not brightness: Mac mode may keep OS on.
A set requires ownership of the same Raw HID request, configured/awake USB
and no Vial unlock in progress. Check, timestamp and mode publication use a
saved/restored interrupt mask. A cancelled request cannot revive an override.

A disconnected or sleeping transport may not deliver a reply. Timeout is
failure; the client does not retry blindly. It validates version, marker,
zero status, expected mode, durations and reserved bytes. A scheduled heartbeat
follows a successful previous exchange; errors stop it until connection and
image identity are checked again. Future versions need a supported parser.

## Lifetime

Refresh every 1000 ms or sooner, with no parallel requests. Every accepted set
starts a 3000-ms lease; query does not. The 32-bit millisecond clock and latched
expiry avoid revival after a 16-bit wrap or long macro. Unsigned elapsed time
assumes the foreground is serviced within one full 32-bit wrap (about 49.7 days).

Breathing is a 4096-ms triangle with 16-ms steps and component values 0–254;
continuous on uses 255. Heartbeats do not restart its phase. These are nominal
firmware intervals, not measured physical timing.

Priority is USB dark state, live helper override, then Mac/PC state.
Reset, configuration changes, suspend/resume, expiry or Vial unlock cancel the
helper mode. Unknown layout, helper disable and orderly exit send normal;
sudden loss expires automatically. Mac/PC survives USB/suspend key cleanup
and supplies the fallback until firmware restart.

The host pauses the helper while configuration, update or rollback owns the
device (AKW-064). Firmware cancellation does not replace exclusive ownership
or confirmation for those operations.

## Channels and evidence

OEM OS state reaches slot 79 component 3, DMA index `0x13F`.
W uses component 1 at `0x13D`; their shared intensity is `0x13C`.
Intensity is full when either is active, with independent component values.
Component 2 is untouched. C uses slot 71.

The [work report](../../audits/rc6/web-firmware-20261024/README.md) records
the OEM dataflow and exact-image checks. They do not prove the physical
light connection, brightness, timing or helper behavior on a real OS.
Each advertised profile requires its own memory, foreground-stack and IRQ
proof before its regression gates.
