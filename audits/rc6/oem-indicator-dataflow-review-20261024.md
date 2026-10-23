# OEM indicator data flow review

## Result

Static instruction checks confirm a path from a USB output-report byte to
staging slot 71, byte offset 1. The byte is either `0xFF` or zero according to
bit 1 of the stored report. This is a source-derived Caps indicator candidate.
The path does not prove that physical C uses that slot or that the installed
firmware implements this behavior.

A second path sends state `0x0A79` to slot 79, byte offset 1. This state toggles
through internal action 4 and suppresses mask `0x88` in the buffer at `0x087A`.
This is consistent with a Windows-key lock. The bounded trace does not connect
that buffer to a keyboard report or action 4 to a physical key combination.
Physical W and the Windows-key interpretation therefore remain unproved.

No source change, build, CPU execution, USB command, device test or flash was
performed. The result does not establish a physical mapping or authorize a live update.

## Input and method

The private 65,536-byte ROM has SHA256
`1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1`.
The hash was checked again. The pinned `toolchains/sdcc-4.6.0/bin/s51` decoded
selected instruction ranges using only `dc` and `quit`. No `run` or `step`
command was used. Raw results are outside Git in
`/home/danil/Documents/ak820-private-backup-20261023/oem-hid-setup-trace-20261024/independent-indicator-dataflow.txt`,
mode `0600`, inside the private backup directory. ROM byte searches were used
only to locate candidates; direct address patterns do not enumerate indirect
accesses.

## USB report path

At `0x4B1C`, the routine reads `0x223D`, checks bit 5, and dispatches the low
six bits of `0x220F` through helper `0x6F25`. The header
`qmk-8051-ak820/lib/ch555/ch555.h` identifies these registers as `USB_IF`
and `D0_STATUS`; bit 5 is the sub-device 0 transfer-completion interrupt.
The helper consumes three-byte table entries containing target high byte,
target low byte and selector. Table `0x4B3C` maps selector zero to `0x53A1`.
This is table data, not sequential instructions.

The request dispatch at `0x50F2..0x5113` subtracts 2, then 1, then 6 from the
saved request byte. Request **9 reaches `0x52CE`**. The next subtraction routes
request **10 to `0x5306`**. The first HID setup draft reversed this point. Its request-9 claim was
corrected after independent review; the current report records `0x52CE`.

At `0x52CE`, `R7` receives setup byte `0x1002`. The special branch for bytes
`04 02 01 00` at `0x1002..0x1005` sets flag `0x086F`. Otherwise
`0x52EC..0x5303` requires bytes `00 02 00 00` and sets flag `0x05CA` to one.
With the standard USB SETUP layout, those bytes mean report ID zero, output
report type 2 and interface zero. The request-type mask checks nonzero
`0x60` bits; it does not enforce an exact HID class request type.

At `0x53A1..0x53B8`, saved request `0x0B78` must equal 9 and flag `0x05CA`
must be nonzero. The routine clears the flag and copies `0x1000` to retained
byte `0x09AD`. Thus the output-data branch is distinct from the setup metadata
branch at `0x5306`. The bounded check proves the conditional instruction path;
it does not test transfer timing, malformed requests or data-stage length.

## Output path

At `0xEA27..0xEA3D`, bit 1 of `0x09AD` selects `R3=0xFF` or `R3=0`.
The routine sets `R5=1`, `R7=0x47` and calls `0xEC9C`.
That helper writes `0xFF` to `0x066D + 4*R7` and writes `R3` to that
address plus `R5`. Slot 71 therefore receives the selected byte at staging
address `0x078A`; its first byte at `0x0789` is `0xFF`.

At `0xEA40..0xEA50`, nonzero `0x0A79` similarly selects `0xFF`, otherwise
zero, for slot `0x4F` (79), offset 1: staging address `0x07AA`.
At `0xEA53..0xEA63`, state `0x0A84` controls the same slot at offset 3,
address `0x07AC`. The state meaning of `0x0A84` is not established here.

The copy loop at `0xDD75..0xDE05` copies all four bytes of each of 128 slots
unchanged from base `0x066D` to base `0x0200`. The candidate destination bytes
are therefore `0x031D` (slot 71, offset 1) and `0x033D` (slot 79, offset 1).
This proves the buffer arithmetic. Full scheduling, DMA configuration,
electrical polarity and the physical light connection remain outside this
bounded proof. In particular, `0xFF` is a buffer value, not proof of an active
high electrical output.

The inspected caller at `0xED4D..0xED72` reaches `0xEA27` only when
`0x05C6 == 1`, `0x0A5F >= 30` and `0x09A7 == 0`; an alternate branch reaches
`0xEC0A`. No claim is made that the indicator routine runs unconditionally.
The current `AK820_RGB_SLOT_MAP` in
`qmk-8051-ak820/keyboards/ajazz/ak820/config.h` excludes slots 71 and 79.
That exclusion agrees with dedicated candidates but is not independent proof
of their physical functions.

## State origin and remaining proof

The table at `0x6535` routes internal action 4 to `0x6577`. Instructions
`0x6577..0x6586` toggle `0x0A79` between zero and one. Both
`0x9EDC..0x9EE8` and `0xEC82..0xEC8E` read this state and, when nonzero,
clear bits `0x88` of `0x087A`. Under standard keyboard modifier-byte semantics,
these are the two GUI modifier bits. That report-byte role has not yet been
proved from its producer and transmitter, so the Windows-lock name remains
a candidate. Follow the producers and transmitter of `0x087A`, callers of
`0x9EC5` and `0xEC6E`, and the origin of action byte `0x0B1F` to close it.

Before claiming verified physical indicators, trace the scheduled buffer-copy/output path,
check alternate paths and initialization, and establish the board connection
for slots 71 and 79. A physical indication and key behavior test would still
be separate evidence, requiring the relevant explicit authorization.

## Independent integration check

A separate static check repeated the copy loop at `0xDD75`, action table at
`0x6535`, toggle at `0x6577`, caller gates at `0xED4D`, and mask clears at
`0x9EDC` and `0xEC82`. The decoded instructions agree with the bounded claims
above. The slot arithmetic was recalculated independently: staging `0x078A`
and `0x07AA` correspond to destination `0x031D` and `0x033D`. No simulator
execution or device command was used. The output scheduling, report-transmitter
and physical-connection limits remain open; this check does not approve an
indicator implementation.

Implementation follow-up: the owner explicitly requested enabling the outputs
as a development candidate. The source implementation uses the identified OEM
outputs with physical behavior still unverified; see
[oem-indicators-implementation-review-20261024.md](oem-indicators-implementation-review-20261024.md).
The earlier analysis alone was not an implementation approval. Device operations
still require their separate confirmation.
