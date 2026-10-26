# Optional feature fixture review

Result: bounded static PASS. No actionable defect found in the reviewed changes to `ak820_emitted/run.py` and `ak820_transport_retry/run.py`. This review does not qualify the release or prove CPU regression or hardware behavior. No tests, builds or USB operations were run.

Reviewed source SHA256:

- `ak820_emitted/run.py`: `3ec8a5f5faaeb451d0e2ba2b51c0af8dc320896215eaacc912815d0648a19c03`
- `ak820_transport_retry/run.py`: `9afd924b0de448e2ad80540165108bebbc97170c246a55e47a905a22d3a8eb6c`

The enabled Direct color, suspend/resume and NKRO retry expectations remain unchanged. Disabled features select explicit negative assertions: omitted Direct maps to zero, command 0x42 preserves configuration and DMA, solid rendering survives; a stale NKRO setting retains boot report retry and leaves the shared endpoint untouched. Configuration selection checks the report against both actual IHX and MAP hashes and rejects a mismatch with the observed allocation. Existing linked listings remain required inputs to fixture symbol discovery.

Static inspection used the certified images under `ak820-beta2-qualified-a-20261025/qmk-8051-ak820/.build/next-{main,game}-release2-certified` and `ak820-beta2-qualified-b-20261025/qmk-8051-ak820/.build/next-typing-release2-certified`. Each IHX/MAP digest matched its build report. Main and typing allocate an 8-byte keyboard report; game allocates 32 bytes. Main/game retain the 246-byte Direct buffer; typing omits it. These footprints agree with optional_features.

The typing relocated listing receives the public `vialrgb_set_value` pointer in DPL/DPH/B, stores its three bytes, and reads the one-byte XRAM `_vialrgb_set_value_PARM_2` before the 32-byte length check. The fixture supplies that ABI with the XRAM pointer tag zero, length 32, and command byte 0x42 at offset 1. The compiled typing switch accepts only 0x41. The static ID conversion takes and returns a 16-bit value in DPTR, matching the fixture call and SFR readback. The shared factory_keymaps decoder preserves the legacy table behavior and rejects incomplete or ambiguous compressed defaults.

Certified IHX SHA256:

- main: `4544d1fe4bb8e9baf262feef8bab0db60a9e98ca2d547266e6d5ecbc10fb4843`
- typing: `131d3fb8d53d7f374fd1edfb85f72237ce6976b28c78269f7405a833407de692`
- game: `8963ce6e5e09f32e2cb4ef8c243f03baf90cc90cedd86c4773076239690025bc`

A fresh complete configured regression remains required. This review does not extend existing stack qualification or establish a final source freeze.
