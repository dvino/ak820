# Repeated VIA packet field probe

Date: 2026-10-23. This probe is complete. The control named by the lead is the stable
`feac6dae` IHX at 38,069 linked CODE bytes. The candidate build in
`qmk-8051-ak820/.build/protocol-be16-probe-20261023/build-report.json` linked
38,179 CODE bytes, a 110-byte regression. No USB or device operation was
performed. The source was restored after the candidate was rejected.

## Candidate

`quantum/via.c` decodes the same two-byte, high-byte-first offset in four
handlers: dynamic keymap bulk get/set and macro bulk get/set. The proposed
patch at `/tmp/ak820-protocol-optimization.patch` factors that decode into a
private helper taking a typed XDATA pointer. Its scope is only those four
offset fields. It does not touch packet length checks, size checks, storage
calls, reply bytes or transport ACK policy.

The candidate was built and rejected. It increased linked CODE by 110 bytes
(38,179 versus the 38,069-byte control). The helper call, argument setup and
return sequence outweighed the repeated decode. The speculative patch remains
outside the source tree at `/tmp/ak820-protocol-optimization.patch` for the
audit record only; production `via.c` retains the inline expressions. No
saving is claimed.

## Contracts to preserve

- The packet is exactly 32 bytes on AK820. `raw_hid_receive` rejects any other
  length before dispatch. The protocol packet and the transport-owned raw
  buffer are XDATA on the production path; the public VIA pointer ABI stays
  unchanged.
- The offset bytes are at `command_data[0..1]`, hence packet bytes 1 and 2,
  and are unsigned big-endian. The size is the next byte and must remain
  separately bounded to at most 28 before a bulk operation.
- Keymap and macro storage routines enforce their own configured capacities,
  end bounds and NVM failure behavior. The refactor must not reorder storage
  calls or make a failed write appear successful.
- `ak820_usb_raw_task` wraps command dispatch with NVM begin/end and only
  publishes the response when the persistence gate permits it. Malformed
  setter/no-response paths keep the endpoint NAK and must not receive a
  synthetic ACK. Read-only allowlisting after an NVM fault remains separate.

## Existing checks and gaps

- `qmk-8051-ak820/tests/ak820_keymap/harness.c` exercises production keymap
  bulk read/write at page boundaries, full 28-byte transfers, an unchanged
  write, last-byte reads, offsets 1535 and 65535, oversize 29-byte requests,
  rejected writes and macro committed-prefix reads. Its direct calls validate
  storage behavior but do not exercise all four VIA packet offset decoders.
- `qmk-8051-ak820/tests/ak820_usb/test_usb.c` exercises Raw32 ownership,
  malformed transfer length, transport ACK/NAK behavior, recovery reply policy,
  reset cancellation and persistence faults. The recovery whitelist is
  transport behavior and does not test the VIA bulk field decode.
- `tools/test_ak820_device_protocol.py` validates host request encodings,
  default read-only operation, malformed request rejection and storage-fault
  status. It uses a fake transport; it does not execute firmware decode or
  prove USB behavior.
- The new `tests/ak820_via_decode` host fixture extracts the four actual
  production switch cases. Its successful run covers 96 field combinations
  plus macro failure and malformed-size cases, checking decoded offsets,
  sizes, forwarded payload pointers and the no-response command marker.
  Its outer packet-length check is a fixture model; it does not prove the
  production entry point's short-packet rejection. Storage functions are
  stubs, so their capacities and journal behavior are covered separately.
- The rejected candidate was built, but no emitted-code or CPU differential
  execution compared its replies, storage effects or endpoint ACK/NAK with
  control. No such equivalence is claimed. The negative CODE result is
  sufficient to reject this optimization without broader runtime testing.

The candidate build and the focused host run were performed. No live protocol,
durable storage, physical keyboard behavior or installed firmware state is
established. Unique build evidence was also preserved outside Git under
`/home/danil/Documents/ak820-private-backup-20261023/optimization-probes/protocol-be16`.

Independent review, 2026-10-23: review_modtap_contract approved this report
and the extracted-case regression fixture. The contradictory initial
no-build wording was corrected; the modeled short-packet check is explicitly
separate from production entry-point coverage. No source optimization was
accepted and no runtime/device equivalence approval was granted.
