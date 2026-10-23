# Bounded optimization review

Independent precommit review, 2026-10-23: PASS for the private pointer change,
focused tests and retained build evidence. The reviewer did not author these
files. No firmware correctness or ABI blocker was found. This record does not
approve promotion into the installer, a Windows binary or a device operation.

## Source and emitted ABI

The only production firmware change is the private parameter of
`journal_header_valid`: `uint8_t *` becomes `uint8_t AK820_XDATA *`. Its single
caller passes a nine-byte local array in XDATA. The control locates it at
0x0529; the pointer build locates it at 0x0528. The candidate receives a two-byte
pointer through DPTR and reads through MOVX. Both return paths assign Boolean
0/1 to DPL, matching the caller and linked regression's observations.

The helper shrinks from 113 to 85 bytes. Removing the generic tag setup in its
caller supplies three further bytes: 31 CODE bytes saved in total. XRAM falls
from 2067 to 2066. Initial SP remains 0x62 and allocated stack capacity 157.
The journal format, CRC, write/replay sequence, flash operations and public ABI
are unchanged. The rejected delay expression is absent from production source.

## Independent checks

- The host runner passed all 65,025 legal delay pairs, 264,448 header cases and
  the sixteen-slot production macro/string guard cases under sanitizers.
- Direct linked execution passed all 2304 cases in both original control and
  pointer images. Peak SP was 0x68 and 0x66: six and four exercised stack bytes.
  This covers the helper only, without interrupt overlap.
- Controlled reports confirm CODE 38,100 / 38,069 / 38,103 for control, pointer
  and rejected delay. Both CODE windows, XRAM and stack figures agree with the
  listings and resource report.
- The host extraction and linked test are substantive. Exact padded observation
  labels avoid numeric-prefix ambiguity; missing observations fail. The oracle
  checks the private validator's header contract and does not replace recovery
  page-bound, CRC or replay checks.

Arbitrarily truncated encoded operands passed directly to playback exposed an
inherited read beyond the reported stream length. This bounded edit does not
fix that separate issue. The tests explicitly use the complete validated-stream
contract and do not claim complete parser or hardware coverage.

## Evidence retention finding — closed

The initial report referred only to transient probe paths. The retained
`bounded-evidence-20261023` package closes that finding:

- All 426 size-bearing manifest entries and three canonical reproduction files
  matched their recorded SHA256 values.
- All 76 artifact references in each of three build reports are present and
  match size and SHA256: 228 references total.
- Each retained build contains 64 relocated listings, including helper/caller.
- Recomputed compile warning counters match: 137 warnings in each build, with
  identical multisets. This does not declare inherited warnings harmless.
- Inventories were regenerated from all three retained roots.
- The linked helper was rerun from all three retained roots without the
  transient probes: 2304 passes each, stack six/four/six bytes respectively.

The [manifest](bounded-evidence-20261023/manifest.json) preserves paths, input
hashes and artifact identities. Dependencies must still be installed for a
source rebuild. Existing compiler/CPU and host evidence cannot establish
physical flash behavior, timing or Windows acceptance.
