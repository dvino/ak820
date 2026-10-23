# OEM USB indicator trace

## Result

The host Caps state, Win-lock state and physical indicator mapping remain
unproved. The trace reached a set of interrupt entry points and a shared
indirect call helper, but did not identify which entry handles HID `SET_REPORT`
or follow a host Caps bit to the indicator output. No C or W pin, DMA slot or
active level is approved by this analysis. This does not change the earlier
finding that animation slot 7 is not evidence for either indicator.

This was offline static analysis of the OEM ROM. No USB command, CPU
execution, device test, firmware change, build or flash was performed. No
claim is made about installed firmware or visible indicator behavior.

## Input and bounded method

The private 65,536-byte ROM
`/home/danil/Documents/ak820-private-backup-20261023/captures/evidence/oem-backup/before-full-rom.bin`
has SHA256
`1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1`.
The bytes remained outside Git. A temporary Intel HEX view was generated in
`/tmp` and loaded by the pinned `toolchains/sdcc-4.6.0/bin/s51`, version
0.9.9, SHA256
`61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd`.
The `dc` command decoded the reset/vector area and selected vector targets.
No simulation `run`/`step` command was issued. A linear decode was treated
only as a search aid; embedded tables and data can resemble instructions.

## Findings

At ROM address `0x0000`, reset jumps to `0x1421`. The vector area contains
these jump entries:

| Vector address | Entry target |
| --- | --- |
| `0x0013` | `0x18F0` |
| `0x001B` | `0x193C` |
| `0x0023` | `0x1988` |
| `0x002B` | `0x19D4` |
| `0x0033` | `0x1A20` |
| `0x003B` | `0x1A6C` |
| `0x004B` | `0x1AB8` |
| `0x0053` | `0x1B04` |
| `0x005B` | `0x1B50` |
| `0x0063` | `0x1B9C` |

The selected targets share a repeated interrupt wrapper. For example,
`0x18F0` saves CPU registers, writes `00 30 06` to XRAM `0x00A5..0x00A7`,
calls `0x0DC4`, restores registers and returns with `RETI`. The next selected
entry at `0x193C` writes `00 30 09` to `0x004A..0x004C` before calling the
same routine. The other inspected entries also store three-byte values and call
`0x0DC4`. The register values and store layout must be interpreted separately.

At `0x0DC4`, the instructions are `MOV DPH,R2`, `MOV DPL,R1`, `CLR A`
and `JMP @A+DPTR`. This helper jumps to the address held in `R2:R1`;
it does not dispatch through a table at `0x0DCA`. In the first two inspected
wrappers the target registers select `0x3006` and `0x3009`. The separate
routine at `0x0DCA` stores `R6,R7,R4,R5,R3` to XRAM `0x0175..0x0179`;
those stores are not a copy of the wrappers' three-byte values.

This establishes indirect call targets for the inspected wrappers, without
identifying the peripheral, endpoint, USB request or payload semantics.
No identified `SET_REPORT` handler or stored host Caps bit was established.
The initial descriptor-table interpretation was rejected during independent
review and replaced by this instruction-level description.

The earlier confirmed local output routines remain as recorded in
[`oem-indicator-mapping-20261023.md`](oem-indicator-mapping-20261023.md):
`E29D..E2E0` is generic selector-driven GPIO logic, and `DCD7..DE0E` includes
animation staging and copying. No caller chain from these routines to a host
Caps or Win-lock state was established here.

## Proof still required

To map C, identify the USB setup/endpoint path for HID `SET_REPORT`, follow
its report byte into stored host Caps state, and trace every branch from that
state to an output value. To map W, identify the Win-lock key action and
follow its state to its output value. For either output, the evidence must
show the concrete GPIO or DMA target, zero/one output values, and relevant
mode or output-enable setup. OEM board documentation or an independently
checked trace must then connect that target to the physical C or W light.

The interrupt vectors and indirect call targets are leads for further offline
analysis, not proof of the request type. Do not infer the HID handler from
isolated byte patterns, infer a light from an unused DMA slot, or assign a
spare slot based on animation behavior. If the ROM does not establish the
board connection, the electrical mapping remains blocked on OEM evidence.
