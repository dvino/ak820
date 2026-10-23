# Send-string lookup probe

Date: 2026-10-23. Base: `d5b81fb6dfca2ca6b5f999911e3b14d6e814b04d`. The probe changes only the private flag lookup inside `send_char` and its eight-byte mask table. It does not change the public API, the weak ASCII tables, the string parser, macro storage or any device operation.

The three packed flag lookups previously shifted a table byte by a variable number of places for every character. The candidate looks up the one-bit mask for `ascii_index & 7`, then tests that mask in each of the three existing flag tables at `ascii_index >> 3`. Casting the character to `uint8_t` before indexing preserves the existing unsigned 0–255 interpretation. The ordinary supported ASCII range remains 0–127. Shift, Right Alt, dead-key space tap, key tap and delay calls retain their existing order.

## Paired builds

Both full builds used SDCC 4.6.0 #16555, the same builder and flags, and separate fresh output directories. The pinned LUFA tree was copied into this worktree for the builds. The control IHX exactly matches the stable pinned image, which confirms the control source and build inputs reproduce the reference.

| Image | CODE total | Main CODE window | Low CODE window | XRAM | Stack capacity | IHX SHA256 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Control at base commit | 38,069 | 36,261 | 1,808 | 2,066 | 157 | `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8` |
| Mask lookup candidate | 38,059 | 36,251 | 1,808 | 2,066 | 156 | `d41d579063441236d18bf712c0529035b084494e464e2cad1e9fbef2f6d61226` |

The candidate saves 10 linked CODE bytes overall and in the main window; the low window and XRAM are unchanged. The added mask table occupies eight CODE bytes. In SDCC's relocated listing, the `send_char` body shrinks from 169 to 151 bytes, saving 18 bytes before accounting for that table. The stack allocation begins one byte later in the candidate, leaving one fewer byte of linker-reported stack capacity. This is allocation evidence only; it does not establish worst-case runtime stack use.

The compiler SHA256 is `3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891`; the assembler SHA256 is `2ae1a62eb7454d80787352fc398ffe87847b1bb048988908f2241d1a4a37d877`. Build reports, MAP, MEM, IHX and relocated listings are under the ignored `qmk-8051-ak820/.build/parallel-send-control-copy/` and `qmk-8051-ak820/.build/parallel-send-candidate/` directories in the probe worktree.

## Behavior comparison

A host C comparison compiled the actual `send_char` and `send_string_with_delay` bodies and actual weak ASCII tables from the base commit and candidate. Stubbed tap, register, unregister and wait functions recorded ordered event traces. All 128 individual ASCII values produced identical traces, including the Shift and Right Alt events, keycodes and dead-key space taps. Delay commands for 0, 1 and 255 milliseconds, and inter-character intervals 0, 1 and 255 milliseconds, also produced identical traces. The complete comparison recorded 734 events per version with byte-identical traces.

This is a host C comparison plus a pinned full firmware build. It is not an 8051 runtime test, USB protocol test, device test or evidence about physical typing. No hardware was accessed. No setting or firmware was written. The stack-capacity change still needs review before integration.

## Isolated review state (before primary integration)

This is an uncommitted probe. Independent review and the guarded isolated build
were complete. At that stage, integration against the concurrent caller changes
remained pending; the later combined measurement is recorded below.

Independent review reproduced the 734-event host comparison and checked both
IHX hashes. No supported-ASCII correctness blocker was found. The reviewer
requested a target guard and preservation of the comparison script. The script
is preserved externally at
`/home/danil/Documents/ak820-private-backup-20261023/optimization-probes/send-string/compare.py`;
the original command was `python3 /tmp/sendchar_probe.py`. The isolated worktree
now guards the optimization with `AK820_BOARD`; the generic path retains its
original expressions. The guarded build completed as recorded below;
combined-source validation remains required. No primary production source change had been applied at that isolated-review
stage; the later integration measurement follows below.

The guarded isolated build completed in
`qmk-8051-ak820/.build/parallel-send-guarded/`. Its IHX SHA256 remains
`d41d579063441236d18bf712c0529035b084494e464e2cad1e9fbef2f6d61226`
and CODE remains 38,059 bytes, so the target guard does not change this AK820
artifact. The preserved comparison script was adapted to accept a firmware
root argument and to extract the guarded table; its rerun again matched all
734 ordered events. Combined compact-tapping validation is still pending.

The current preserved-script invocation is:

```sh
python3 /home/danil/Documents/ak820-private-backup-20261023/optimization-probes/send-string/compare.py /tmp/ak820-send-string-parallel/qmk-8051-ak820
```

A second independent review accepted the guarded isolated candidate and
reproduced the 734-event comparison and guarded IHX hash. The review requested
removal of stale pending-review and pending-build statements; those statements
have been replaced above. At that stage, combined-source validation remained pending; its later
measurement follows below.

## Combined primary measurement

The guarded candidate was integrated after the reviewed system mapping.
Fresh build `.build/compact-modtap-send-mask-20261023` succeeded. Its last
byte is `0xc6f6`, leaving nine bytes before the exclusive `0xc700` boundary.
The builder counts 40,414 populated CODE bytes (38,603 main and 1,811 low).
MEM reports a 40,419-byte occupied span including holes, XRAM 2,512 and stack
allocation capacity 154. These two CODE measures are distinct. IHX SHA256:
`24e97578ee469e5343d6949976fef96898d87c0e38ec6148374af1b1611a1655`.
The preceding mapping-only MEM span was 40,429 bytes and ended at `0xc700`.

The preserved send-string comparison matched 734 events on this primary source.
The production tap-hold host suite passed all nine negative controls and 156
eligible QMK comparisons. Existing optimization suites also passed. Linked CPU
execution and final artifact review remain pending; the image is not installed
or approved for an update.
