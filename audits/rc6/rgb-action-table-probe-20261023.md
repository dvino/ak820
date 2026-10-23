# RGB action table probe

This private probe replaces ten repeated RGB action calls with a table. It
changes no production source and does not open the keyboard. The candidate
saves 216 linked code bytes and four XRAM bytes against the frozen baseline.
It is awaiting independent review and is not approved for source integration.

The original `process_rgb.c` sets two function arguments for each action and
calls `handleKeycodeRGB` to choose one. The candidate stores the ten actions
in CODE memory in their keycode order. Shift selects the adjacent action by
flipping the low index bit. The table has ten two-byte function pointers.
SDCC emits two `MOVC` reads and calls `__sdcc_call_dptr`; it does not read a
generic data pointer. Dead-code removal retains all ten targets as table
roots and removes the former helper. The emitted assembly and roots are
recorded in `asm-evidence.json`.

This path applies only with `AK820_BOARD`, RGB Matrix keycodes enabled and
RGBLIGHT absent. Every other profile retains the original cases. The ten
keycodes are `RGB_MODE_FORWARD` through `RGB_SPD`, currently `0x7821` through
`0x782A`. A compile-time check covers every offset; SDCC also checks that a
function pointer occupies two bytes. `RGB_MOD` and `RGB_RMOD` are aliases of
the first two keycodes. Toggle and the legacy mode cases keep their existing
handling, including the consumed return value for unsupported modes.

The private files are in
`qmk-8051-ak820/.build/rc6-rgb-action-table-probe-20261023`.
`original.c` was captured before other source changes, with SHA256
`658aee04c8015977c79db28bbd4917778b595059c877c385e6472c0d4fdd6f1e`.
`probe.py` checks this against the canonical build manifest, writes
`candidate.c`, runs the host comparison, compiles both translation units
with the saved flags, and substitutes only this assembly unit into the
frozen baseline. It then repeats dead-code removal, outlining and linking.
It does not use a full build or require later unrelated source changes to
remain absent. `report.json` saves the compile commands and source hashes;
`linked-report.json` saves the link commands and measurements.

Before any SDCC compile, the host comparison passed 524,288 cases in each
of four profiles: board and generic, each with key-up and key-down triggers.
Each profile covers every 16-bit keycode, both pressed states, and no Shift,
left Shift, right Shift and both Shift keys. It compares the boolean return,
callback log, callback count, modifier value and `get_mods` call count.
The harness compiles the original and candidate source with stub dependency
headers; it uses the real keycode enumeration. These checks cover 2,097,152
events. They prove the dispatch contract in the host harness, not SDCC
pointer access or physical behavior.

The control reproduces the canonical IHX byte for byte:
`ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`.
The private candidate IHX is
`c85ab09532aaba4332fa3ee14e5c1b10ecbd48696dbd7a8d5aa2096e667a3c4a`.

| Linked measurement | Control | Candidate |
| --- | ---: | ---: |
| Code bytes | 39,432 | 39,216 |
| Main window bytes | 37,573 | 37,357 |
| Low window bytes | 1,859 | 1,859 |
| XRAM bytes | 2,071 | 2,067 |
| Reported stack capacity | 152 | 152 |
| Outlined helpers / sites | 32 / 221 | 32 / 221 |

Both links pass the configured code-window and memory limits. Reported
stack capacity is available space, not measured worst-case stack use.
The table path pushes two registers around the indirect call, adding two
stack bytes at that site compared with the former helper's tail call.
The CPU fixture checks the resulting tested high-water mark separately.

The linked C52 comparison also passes. `cpu_probe.py` runs 200 keycode,
edge and Shift combinations for each of five state seeds (0, 1, 127, 240,
255) in both images. The keycodes include `0x7820` through `0x7835`, zero,
`0x781F` and `0xFFFF`. It compares the boolean return, all eight RGB config
bytes, real modifiers, dirty persistence flag, change timestamp, rendering
flag and all 82 reactive LED ages. A separate 200-case run in each image
captures the exact selected callback and call count. Only that callback run
replaces action entry points with jumps to simulated ROM capture stubs;
the state runs execute the real linked RGB actions. The record uses the
production three-byte generic-pointer ABI, with an XDATA tag and the pressed
byte at offset five. `cpu-report.json` records the results and image hashes.

The real-action CPU runs reach stack pointer `0x7B` in the control and
`0x7D` in the candidate: 20 and 22 tested stack bytes above the initialized
stack pointer. This confirms the two-byte increase on these tested paths.
The capture-only callback run reaches `0x7B` in both. These are foreground
CPU observations; they do not establish a global maximum with interrupts.

An initial callback fixture placed an eleven-byte capture routine over each
action. The real wrappers are six bytes apart, so the fixture overwrote its
neighbors and failed on the control. The corrected fixture uses three-byte
jumps into separate unused simulator ROM slots. No firmware change was
needed. The corrected callback run and the expanded state run pass.

No live protocol, durable-storage, physical RGB, timing or interrupt behavior
is claimed. The dirty flag and timestamp checks cover the scheduling of a
future save, not a physical EEPROM write. No USB write, loader transition,
reset or flash operation was performed.
