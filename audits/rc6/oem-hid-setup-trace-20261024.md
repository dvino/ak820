# OEM HID setup trace

## Result

Static analysis reaches the interrupt trampoline at `0x3015`, a candidate
USB setup path, which jumps to the nontrivial routine at `0x4B1C`. That
routine processes setup metadata at XRAM `0x1000..0x1007`. For request number
9, the dispatch at `0x50E7` reaches `0x52CE`. That branch recognizes setup
bytes `0x1002..0x1005 = 00 02 00 00` and sets flag `0x05CA`. Assuming the
standard USB SETUP byte layout, these values mean report ID 0, report type 2
(Output), and interface 0. The report type and field names are an
interpretation of that standard layout; the ROM contains the byte checks,
not labels for these fields.

The receive path later checks request number 9 and flag `0x05CA`, then copies
the received byte from XRAM `0x1000` to `0x09AD`. A routine at `0xEA27` reads
bit 1 of `0x09AD` and calls a helper that writes `0xFF` or `0x00` to staging
entry `0x066D + 0x47*4 + 1` (slot 71, channel 1). This connects the received
byte and later staged value through the shared XRAM state. The trace does not
prove the output scheduling conditions or tie that slot to a physical C or W
indicator, so no electrical mapping or firmware implementation choice is
established. The open mapping remains as recorded in
[`oem-usb-indicator-trace-20261024.md`](oem-usb-indicator-trace-20261024.md).

## Input and method

The input is the private 65,536-byte OEM ROM with SHA256
`1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1`. A private
Intel HEX view and prior vector disassembly are under
`/home/danil/Documents/ak820-private-backup-20261023/oem-usb-indicator-trace-20261024/`.
The corrected decode is stored outside Git at
`/home/danil/Documents/ak820-private-backup-20261023/oem-hid-setup-trace-20261024/oem-hid-corrected-decode.txt`
with directory mode `0700` and file mode `0600`.

The decode used the pinned `toolchains/sdcc-4.6.0/bin/s51` (uCsim 0.9.9,
SHA256 `61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd`)
with only `dc` and `quit` commands:

```text
dc 0x4c19 0x4c70
dc 0x50e7 0x5190
dc 0x52ce 0x5358
dc 0x53a1 0x53d5
dc 0xea27 0xea50
dc 0xec9c 0xed60
```

No simulator `run` or `step`, USB command, device test, build, firmware
change, or flash was performed. No claim is made about installed firmware or
visible device behavior.

## Instruction evidence

The interrupt trampoline table at `0x3000..0x3026` contains `LJMP 0x4B1C` at
`0x3015` (`02 4B 1C`). Other confirmed entries include `0x3006 -> 0xEF87`
(`RET`), `0x3009 -> 0xE36E`, and `0x301E -> 0xD5CE`. The surrounding entries
target `0xEF88..0xEF8E`, each a `RET`. The table identifies a routine entry;
it does not by itself establish a USB request.

At `0x4C19..0x4C3F`, the routine reads XRAM `0x1007` and `0x1006` and builds a
two-byte count at `0x0B79..0x0B7A`. At `0x4C45..0x4C4C`, it copies XRAM
`0x1001` to `0x0B78`. At `0x4C4D..0x4C55`, it masks XRAM `0x1000` with `0x60`;
a nonzero result branches to `0x50E7`. This branch is consistent with a
class/vendor request-type path, but the mask alone does not distinguish those
request types.

At `0x50E7..0x5118`, the path selected by the `0x1000 & 0x60` mask dispatches
based on `0x0B78`, the saved byte from `0x1001`. The cumulative arithmetic
through `0x5103` subtracts 9: `0x50F6` adds `0xFE` (subtract 2), `0x50FD`
decrements once, and `0x5103` adds `0xFA` (subtract 6). A zero result falls
through to the jump at `0x5107` and reaches `0x52CE`. The `DEC` at `0x510A`
makes the cumulative subtraction 10, so request 10 instead reaches `0x5306`.
The request-type mask alone does not distinguish class,
vendor and reserved values; request 9 is consistent with HID `SET_REPORT`.

At `0x52CE..0x5303`, one branch checks for `0x1002..0x1005 = 04 02 01 00`
and sets `0x086F`. The other branch requires `0x1002 = 0`, `0x1003 = 2`,
`0x1004 = 0` and `0x1005 = 0`, then sets `0x05CA`. Under the standard USB
SETUP layout, the latter is report ID 0, report type 2 (Output), interface 0.
This classification is inferred from the standard field layout.

At `0x53A1..0x53B8`, the code checks that the saved request number is 9 and
that `0x05CA` is set. It clears that flag and copies XRAM `0x1000` to
`0x09AD`. At `0xEA27..0xEA3D`, a routine reads bit 1 of `0x09AD`,
selects `0xFF` when set and `0x00` when clear, then calls `0xEC9C` with
`R7 = 0x47` and `R5 = 1`. The helper computes `0x066D + R7*4`, marks the
entry's first byte, then stores `R3` at offset `R5`; this writes the selected
value to staging slot 71, channel 1. This establishes a software data path
from the received byte to a staged output value through shared XRAM. It does
not establish the scheduling conditions for the output routine or which
physical indicator that slot controls.

## Review finding and closure

An independent deeper review found that the first draft assigned request 9 to
`0x5306` and described its `0x0950/0x09A0` stores as `SET_REPORT` handling.
That calculation missed the zero-result jump at `0x5107`: request 9 reaches
`0x52CE`; request 10 reaches `0x5306`. The `0x5306` stores are therefore not
evidence for the request-9 output report. The dispatch arithmetic and byte
checks were re-decoded with the pinned `s51`; this report replaces the earlier
claim with the corrected path above. No device or firmware test was run.

## Boundary of the trace

The remaining questions are whether this request-type path is specifically a
class request, what scheduling conditions apply to the output routine, and
which physical indicator staging slot 71 controls. The generic GPIO routine
at `0xE29D..0xE2E0` and animation staging at `0xDCD7..0xDE0E` still lack a
proved physical C/W connection. OEM board evidence or an independently
checked trace must tie the staged target to the physical indicator before
assigning the C or W mapping.
