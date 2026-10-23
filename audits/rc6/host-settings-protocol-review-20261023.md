# Host settings protocol review — 2026-10-23

## Scope and evidence

Independent read-only review covered the changes to
`tools/ak820_device_protocol.py` and the new
`tools/test_ak820_device_protocol.py`, compared with commit `c0c704e`.
The firmware VIA, Vial, macro upload and RGB implementations were checked
against the request formats. No USB device was opened and no hardware write
was attempted.

An isolated checkout of `c0c704e` with only the four reviewed protocol and
runner files overlaid passed all 28 offline tests (9 protocol, 19 runner):
`python -m unittest tools/test_ak820_device_protocol.py tools/test_ak820_device_tests.py`.
This avoided unrelated concurrent edits to release-bound installer files.
This proves the tested host request handling only; it does not prove USB
behavior, flash durability or physical keyboard behavior.

## Finding P1 — layout options can be silently truncated

The new typed `set_layout_options` accepts a 32-bit value. Its test sends
`0x12345678` and accepts an echoed request as success. The current AK820
firmware persists one byte: `quantum/via.c`, `via_set_layout_options`, casts
the value to `uint8_t`; `quantum/via.h` sets the field size to one. The stored
value would be `0x78` rather than the requested value.

Restrict this AK820 adapter's setter to 0..255 and require the three high
wire bytes to be zero at the exchange boundary. Add a regression proving
that 256 and larger values cause no transport call. Use a representable
value in the successful setter test. Status: closed. The setter and exchange boundary now reject values above 255; oversized and truthy non-boolean inputs are covered by negative tests.

## Integration check

The default read-only mode is appropriate. Existing explicit write callers
must opt in only after their existing authorization checks. The regression
runner now enables writes only from its existing consent flag, after checking
both authorization flags. Its explicit write fixtures opt in as well.

The allowlist rejects unsupported request families and malformed fixed
shapes before transport I/O. Macro uploads use the firmware's big-endian
offset and at most 28 data bytes. Save uses VIA command 9. Encoder getters
return CCW then CW, matching the firmware; durable NVM order is reversed.
Readback remains necessary because the firmware encoder firewall can echo
a protected write while replacing the requested keycode with zero.

## Exact source CODE identity

The packer copies 87 bytes from OEM ROM E650..E6A7 into the startup helper
at 2830. The linked IHX and deterministic wrappers do not independently
identify those helper bytes. The embedded manifest CODE checksum is
self-reported, so checking it against the same captured ROM is an integrity
check, not a trusted exact-image identity check.

No trusted checksum of the complete packed CODE range 2800..C700 was found
in the tracked release, documentation or audit files examined. Tracked
candidate reports contain a complete personal payload checksum, which also
covers variable NVM and cannot substitute for a CODE-only checksum.

The new settings implementation requires an approved OEM session and reconstructs
exact expected packed CODE. This closes that design question for its current
commands. A future standalone exact-identity backup without that session needs either a reviewed CODE/helper
checksum in approved release metadata or an approved OEM/session reference
from which to reconstruct the expected packed CODE. Without that input,
report the narrower linked-code verification or reject an operation whose
contract requires exact packed CODE. General update must independently
verify the complete expected source and target CODE before mutation.
