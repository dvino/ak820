Русский перевод: [Direct](ru/DIRECT.md).

# Direct palette

Direct uses 82 HSV8 entries: hue, saturation and value are bytes. LED indices
follow ordinary Vial LED metadata (`GET 0x44`), not the 83 physical key positions.
Value is clamped to 160. The palette lives in RAM and is lost on power loss.
Reading while RGB is off returns stored colors, not visible darkness.

Support requires an exact image with the validated Direct v1 contract and runtime
negotiation. Older images and profiles without Direct have no palette getter.
Global RGB color cannot reconstruct the palette. Legacy fastset updates up to nine
LEDs immediately; a sequence of fastset packets is not an atomic frame.

## Host calls

`DeviceAPI.direct_snapshot()` negotiates support and reads a coherent palette.
It returns `None` when the extension is unavailable. A generation change restarts
the read, with at most three attempts. Failed or malformed replies stop the call.
The snapshot includes the flags observed in the final status read. These describe
visibility at that moment; changes to enabled, selected or suspended state do not
advance the palette generation. Stored HSV colors stay available while dark.
No read selects a mode, enables lighting, unlocks Vial or writes EEPROM.

`set_direct_frame(hsv, frame_id=…, expected_generation=…)` requires an instance
created with `allow_writes=True`. Supply 246 bytes, a nonzero 16-bit frame ID and
the generation from a fresh snapshot. The host clamps each LED's V byte to 160
before upload, matching the negotiated firmware limit while leaving the input
bytes unchanged. The call uploads sequential chunks of at most eight LEDs and
commits once. Failure stops without automatic abort, retry or restore.
`direct_status()` reads progress; `direct_abort(frame_id)` explicitly
cancels a matching unfinished upload. Neither call provides write authorization.

A successful commit changes the logical RAM palette and advances its generation.
When Direct is visible, conversion and scan-boundary publication may still be
pending. Status states are 0 idle, 1 upload, 2 conversion, 3 queued, 4 publication,
5 done and 6 cancelled. A frame accepted for publication finishes at the bounded
scan boundary before normal rendering honors later mode or enable changes.
Suspend and USB keyboard reset cancel pending work. Actual physical LED and DMA
behavior requires hardware validation; host tests do not establish it.

## Wire format

All packets are 32 bytes. Byte 0 is VIA GET `8` or SET `7`; byte 1 is the
subcommand. The table uses offsets relative to byte 2. Integers are little-endian.
Unused request bytes are zero.

| Operation | Subcommand | Arguments or response |
| --- | --- | --- |
| Capabilities GET | `0x45` | Response: `AD`, version 1, flags 3, count 82, format 1 (HSV8), mapping 1 (Vial LED index), maximum 160, read limit 7, upload limit 8, timeout uint16 1000 ms |
| Palette GET | `0x46` | Request: generation uint32 at 0, first at 4, count at 5. Response: result at 0, first at 1, count at 2, flags at 3, generation at 4, HSV triples at 8 |
| Status GET | `0x47` | State at 0, sequential coverage at 1, frame ID uint16 at 2, generation uint32 at 4, flags at 8 |
| Begin SET | `0x43` | Version 1 at 0, count 82 at 1, frame ID uint16 at 2, expected generation uint32 at 4 |
| Chunk SET | `0x44` | Frame ID uint16 at 0, first at 2, count at 3, HSV triples at 4 |
| Commit SET | `0x45` | Frame ID uint16 at 0 |
| Abort SET | `0x46` | Frame ID uint16 at 0 |

SET replies replace argument byte 0 with a result and echo the remaining bytes,
except that a CHUNK reply contains V bytes clamped to 160 after its LED range
has been validated. HSV components occupy one wire byte each. Exact duplicate chunks compare
the normalized colors, so a duplicate above 160 is accepted only when it
normalizes to the already stored value.
Results: 0 success, 1 invalid, 2 busy, 3 stale generation, 4 incomplete, 5 wrong ID.
Runtime flags: bit 0 RGB enabled, bit 1 Direct selected, bit 2 suspended.
Generation arithmetic wraps at 32 bits.

Chunks must extend sequential coverage. Exact duplicates of already covered
colors are accepted after brightness clamping. Gaps, invalid ranges, conflicting
duplicates and incomplete commit cancel the matching upload without replacing
the active palette. A wrong ID leaves another transaction intact. An upload
expires after 1000 ms without an accepted chunk. A new begin replaces an
unfinished upload; conversion or publication is busy. Legacy fastset cancels an
unfinished upload and advances generation. Duplicate commit of an accepted frame
is idempotent. Abort is available during upload, not after commit acceptance.

## Backup

ROM and NVM backups contain no Direct palette. Settings export adds a separate
`direct-ram.json` only for an exact image marked `direct_protocol: 1` and after
runtime negotiation. Its typed format binds count, HSV encoding, LED mapping and
brightness to the captured palette. This sidecar does not change old backup
formats or claim that all RAM and NVM were frozen together.

Durable settings restore keeps its existing behavior. The separate
`restore_direct_palette` call requires explicit writes, an exact supported live
CODE image, matching runtime capabilities and a valid sidecar. It reads a fresh
generation, commits the frame and checks palette readback. It does not save the
palette to EEPROM or select Direct. Old backups have no recoverable RAM palette.
