# USB snapshot-loop size probe

Date: 2026-10-23. The candidate is rejected. It increases linked CODE by
62 bytes, so the source remains at the control version. No USB or device
operation was performed.

## Change measured

`ak820_usb_send` copies each report byte into the endpoint buffer. For reports
that also belong in `input_snapshot`, the original loop copies to both places;
for raw reports it copies only to the endpoint buffer. The candidate moved the
`offset == SNAPSHOT_SIZE` decision outside the loop and used separate loops.
The intent was to remove one condition from each copied byte. The code duplication
cost more than the repeated condition saved.

The candidate diff is preserved outside the source tree at
`/tmp/ak820-parallel-protocol-size-probe.patch`. The comparison used independent
build directories in an isolated worktree at `/tmp/ak820-protocol-parallel`,
branch `codex/protocol-size-probe`, from base commit
`d5b81fb6dfca2ca6b5f999911e3b14d6e814b04d`.

## Build evidence

Both builds used SDCC 4.6.0 #16555, compiler SHA256
`3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891`, and
assembler SHA256
`2ae1a62eb7454d80787352fc398ffe87847b1bb048988908f2241d1a4a37d877`.
They used the same pinned QMK CLI and LUFA tree. The build reports and complete
artifacts are under `qmk-8051-ak820/.build/parallel-protocol-control2-20261023`
and `qmk-8051-ak820/.build/parallel-protocol-candidate-20261023` in that
worktree.

| Build | Linked CODE | Main / low window | XRAM | Initial SP / stack capacity | IHX SHA256 |
| --- | ---: | ---: | ---: | ---: | --- |
| Control | 38,069 | 36,261 / 1,808 | 2,066 | 0x62 / 157 | `feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8` |
| Candidate | 38,131 | 36,323 / 1,808 | 2,066 | 0x61 / 158 | `8f5b28f65db801ae2803b51b827d7d80a2157392991c6e8837ca533358e00256` |

The candidate is +62 linked CODE bytes, all in the main window. Both images
fit the declared CODE windows. XRAM is unchanged. The one-byte shift in initial
SP and reported stack capacity comes from the linked image's internal RAM
allocation layout; it is not a measured peak-stack comparison. Control and
candidate source hashes for `usb_ak820.c` are respectively
`3cb107ad30956f61b9f248cc14b168f9a515bea60f6bc6d602eb97f350e4951f` and
`b93ddd6cb04c5a43437b2427b6904116015f0b134b06ca8002e0d84271336550`.

## Limits

The result is a size comparison from two successful firmware builds. No host
callback harness or linked CPU execution compared output buffers for raw,
keyboard and shared endpoint reports. No live USB behavior, endpoint ACK/NAK,
physical keyboard behavior or installed firmware state was tested. Since the
candidate loses CODE, it is rejected without claiming behavioral equivalence.
The production source contains no candidate change.
