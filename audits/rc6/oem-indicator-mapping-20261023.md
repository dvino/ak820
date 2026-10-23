# OEM C and W indicator mapping

## Result

The electrical mapping of C and W remains unproved. No pin, DMA slot or active
level is approved for implementation from this analysis. In particular, slot 7
must not be assigned to either indicator from the animation code below.

This is static ROM analysis. No USB command, device test, firmware change,
build or flash was performed. It makes no claim about installed firmware or
visible indicator behavior.

## Input and method

The private 65,536-byte original ROM was checked against SHA256
`1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1`.
The bytes stayed outside Git. A private temporary Intel HEX representation was
loaded into the pinned `toolchains/sdcc-4.6.0/bin/s51` (uCsim 0.9.9). The `dc`
command decoded the address ranges listed below. No CPU execution was used.

An unrestricted linear decode is only a search aid: data and jump tables can
decode as plausible instructions. The observations below use local instruction
sequences with consistent control flow. They do not establish a complete
control-flow graph or a host-report dataflow trace.

## Confirmed local behavior

| ROM range | Observation | Limit |
| --- | --- | --- |
| `DCD7..DD74` | A timer-like value at XRAM `0AF7` is compared with `A0`; the early path returns. The other path clears it, selects color-table data or values from `0A7F..0A81`, and writes `FF` plus three components to `0689..068C`. | `0689 = 066D + 7*4` identifies staging slot 7. There is no host Caps bit or identified Win-lock state in this local sequence. |
| `DD75..DE0E` | Four bytes per slot are copied unchanged from `066D + slot*4` to `0200 + slot*4`, for slots `0..127`. The function then writes direct RAM `08=02`, `09=00`. | The transfer has no inversion, but cannot establish which physical light a slot drives or whether a nonzero value lights it. |
| `E29D..E2B0` | Direct SFR `A6` selects a generic output path. `JBC ACC.4` takes the GPIO branch after clearing the selector bit. That branch multiplies the remaining accumulator by three and jumps into `E2B1`. Otherwise, `((A & 1)+1)` is complemented and decremented before masking SFR `F1`. | This is selector-driven output logic, without an identified C/W caller or board connection. |
| `E2B1..E2E0` | Sixteen three-byte entries clear `P0.0..P0.7`, then `P3.0..P3.7`, and return. | A pin-clear operation does not by itself prove an active-low indicator. The same path can serve other board functions. |

## Evidence still needed

The missing proof is the complete chain for each indicator:

1. Identify the OEM HID output-report handler and the stored host Caps bit.
2. Follow that bit to the output write, including intermediate state and all
   relevant mode branches. Separately identify the OEM Win-lock state from its
   key-action path and follow its output write.
3. Record the output target and the values produced for state zero and state
   one. For GPIO, include output-enable/mode setup and both set/clear paths.
   For DMA, include the slot and every relevant component.
4. Establish that the target is the physical C or W light. This needs an OEM
   board connection or an independently checked trace tying the OEM state to
   that light. An unused slot, color animation or generic GPIO helper is not
   sufficient.

A useful next offline step is to recover instruction boundaries from the USB
interrupt vectors and their call targets, identify the HID SET_REPORT receive
path, then build cross-references for its state storage. Searching isolated
`ANL #02` or bit-test byte patterns alone is insufficient because jump targets
and data also contain those bytes. If ROM analysis cannot establish the final
board connection, leave the implementation blocked on that evidence rather
than selecting spare DMA slots.

The requested replacement behavior remains defined in
`input-indicators-contract-20261023.md`: C follows host Caps Lock and W follows
additional-layer activity. That behavior does not supply the electrical map.
