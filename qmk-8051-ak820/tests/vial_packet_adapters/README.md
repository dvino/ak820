# Compact Vial packet adapters

Run offline from the repository root:

```sh
docker run --rm -v "$PWD":/workspace -w /workspace/qmk-8051-ak820 \
  ak820-nkro-study-env:local python3 tests/vial_packet_adapters/run.py
```

The test extracts the production TD/KO parser cases, storage functions,
validators and KO cache reload. It compares them with the former adapters
that copied each ten-byte record through a local structure. It checks the
entire 32-byte reply, persisted bytes, NVM health and ordered read, write,
clear, flush and reload traces. TD-only, KO-only and combined configurations
cover all 256 indices, unknown commands, empty and malformed records, valid
stored records, an existing NVM fault and update/flush failures. Native C
compilation enables undefined-behavior checks. Each configuration runs twice:
516,096 cases with packed fixture record types and `__SDCC_mcs51` to model
the target's byte alignment, and 516,096 cases with native record alignment
and no target flag to exercise the local-copy fallback. The target model is
still GCC, not real SDCC adapter execution. Preprocessed production cases are
checked to require packet-to-record casts only in the target model; source
checks require each direct branch's target guard and type-alignment assertion. The clear callback is a trace
stub; transport ownership and the production clear path require source review.
This is a CPU/NVM model, not a device or linked firmware size result.

## Packet lifetime

`tmk_core/protocol/ch555/usb_ak820.c` publishes a complete packet as
`RAW_READY`. `ak820_usb_raw_task()` changes that state to `RAW_WORK` before
calling `raw_hid_receive()` synchronously. A new Raw request is admitted only
from `RAW_IDLE`; `control_out()` copies received bytes only in `RAW_RX`.
Cancellation preserves active ownership as `RAW_CANCELLED`, without clearing
the packet. Main releases that ownership after the command returns. Therefore
interrupts cannot replace the SET source while storage uses it.

`quantum/action.c` implements `clear_keyboard()` through modifier/key clears,
compact engine cancellation and report sending. These functions operate on
engine state and HID reports. `ak820_usb_send()` copies reports to endpoint
memory and input snapshots, without modifying the Raw packet. Compact TD
reload is a no-op. `ak820_key_override_reload()` cancels engine state and reads
records into its private `entries` array. Neither reload retains a packet
pointer or dispatches a packet callback. GET has no clear callback. These
properties permit direct packet slices for compact TD/KO only on
`__SDCC_mcs51`. Each direct GET and SET branch additionally requires the actual
record type's `_Alignof` to equal 1. Native and other targets use aligned local
structures and `memcpy`; compact validation semantics are preserved, while
noncompact branches retain their firewall behavior.

Compact validators inspect records as bytes; they never dereference the
GET slice as a multi-byte structure. Byte-only dereferencing alone does not
make an underaligned typed pointer conversion valid in ISO C; the target guard
and type-alignment assertion are required even when validators use bytes. GET saves its index
before clearing output bytes 1 through 10, preserving zero output for invalid
indices. SET preserves all request bytes except status byte 0. Combo retains
its separate firewall and storage format.

## Real compiler alignment check

```sh
docker run --rm --volumes-from ak820-nkro-measure \
  -v "$PWD":/workspace -w /workspace/qmk-8051-ak820 \
  ak820-nkro-study-env:local python3 tests/vial_packet_adapters/alignment.py \
  /toolchains/sdcc-4.6.0/bin/sdcc
```

`alignment.py` extracts the exact production record declarations and alignment
assertions and compiles them with real SDCC mcs51, large model. It proves those
types have alignment 1 and size 10 in that compiler configuration. This is a
standalone ABI check; it does not compile the production adapters or establish
firmware behavior, code size, device operation, or host acceptance.
