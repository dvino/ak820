# System usage mapping size probe

Date: 2026-10-23. A target-only system usage mapping candidate saves 72 bytes
of linked CODE in the frozen source snapshot. The candidate still links past
the allowed CODE end at `0xc700`, so it is not an approved image and needs a
fresh combined build if selected for integration. No device operation was
performed.

## Change measured

The actual helper is `KEYCODE2SYSTEM` in
`qmk-8051-ak820/tmk_core/protocol/report.h` (there is no such helper in
`quantum.c`). For `AK820_BOARD`, the candidate replaces its three-case switch
with a range check and an offset from `SYSTEM_POWER_DOWN`. The target keycodes
are consecutive (`KC_SYSTEM_POWER` through `KC_SYSTEM_WAKE`, `0xa5` through
`0xa7`), as are the corresponding usages (`SYSTEM_POWER_DOWN` through
`SYSTEM_WAKE_UP`, `0x81` through `0x83`). Other keycodes still return zero.
The non-AK820 implementation remains the existing switch.

The isolated checkout is `/tmp/ak820-parallel-usage`, detached at
`d5b81fb6dfca2ca6b5f999911e3b14d6e814b04d`. The frozen primary snapshot was
captured at `2026-10-23T23:20:11+03:00`: tracked primary differences were
copied as a binary patch, `ak820_tapping.c` and `ak820_tapping.h` were copied
from their then-current untracked state, and the pinned LUFA directory was
copied. The two tapping files were included to reproduce the primary build
inputs; they were not edited here. The frozen `report.h` SHA256 was
`cdb85da5e6e27eba8065a238d191cad543d7760bf28b40185ac3593c3ff35526`.

## Paired build evidence

Both builds used the same isolated source snapshot, SDCC 4.6.0, builder, QMK
CLI, compiler and assembler. Each used a separate fresh build directory. The
builder rejected both linked images because their code extends into the
reserved region at `0xc700`; their actual MAP and MEM outputs were retained
and measured despite that rejection.

| Build | ROM/EPROM/FLASH occupied | Last address | XRAM | Stack capacity | IHX SHA256 |
| --- | ---: | ---: | ---: | ---: | --- |
| Control | 40,520 bytes | `0xc75b` | 2,512 | 155 | `3d55f78d56f210698c68131c4bcee2d7c1ace688b0d6f69bafd56967602d2e9d` |
| Candidate | 40,448 bytes | `0xc713` | 2,512 | 155 | `5eef397a0e5eaaffcfeded6d86734bea6d6d37a7d30990a13d2f66897dc0ae1e` |

The candidate saves 72 linked bytes. Its final byte is still at `0xc713`, 20
bytes beyond the allowed exclusive boundary `0xc700`. XRAM and linker-reported
stack capacity did not change. The stack number is allocation evidence, not a
measurement of worst-case runtime stack use. The IHX remains an unapproved
application image and was not packaged or installed.

Compiler SHA256: `3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891`.
Assembler SHA256: `2ae1a62eb7454d80787352fc398ffe87847b1bb048988908f2241d1a4a37d877`.
Builder SHA256: `3f7a34aeb8666b0c98878d96ddc3335b4033515943af333449082bc733e93202`.
Control and candidate MAP SHA256 values are respectively
`756a76f43f6c7c89cf4ce324de366d01c1328a28281be92c44cc5263b305d8aa` and
`dc45afbcd780666486eb9cb9f145124a468a620bd6dbad3c9f293482167f8a6d`.
Control and candidate MEM SHA256 values are respectively
`372188f5249652ad5a4beb1e8abe8321a78d799d65326f957b22697405ab74bb` and
`086791b633c28a5ffea747fd221d34ab1d23e20ecc249e06a276727df1abc799`.
Build artifacts are under
`qmk-8051-ak820/.build/usage-control-20261023/` and
`qmk-8051-ak820/.build/usage-candidate-20261023/` in the isolated checkout.

## Limits and review

An independent reviewer compiled the actual old and new helpers with
`cc -std=c11 -Wall -Wextra -Werror -O2`. All 65,536 uint16 inputs produced
identical results after the unchanged uint8 parameter conversion. An additional
256 postincrement argument cases verified single evaluation. The helper is an
inline function, not a macro. All production callers retain their conversions.
The reviewer independently checked both IHX, MAP and MEM hashes and approved
the isolated mapping change for a fresh combined build, not image approval.
The harness and result are preserved outside Git under
`/home/danil/Documents/ak820-private-backup-20261023/optimization-probes/system-usage/`.

This is paired link-size evidence plus host equivalence and source review.
No 8051 execution, live protocol, durable-storage, physical keyboard behavior
or installed firmware state was tested. The candidate is not retained in the
primary source. Its isolated source patch is `/tmp/ak820-parallel-usage.patch`.
A fresh combined-source build and artifact validation remain required.

## First primary integration measurement

The reviewed mapping was applied without changes after the admission-XOR
control. Fresh build `.build/compact-modtap-system-range-20261023` was correctly
rejected: its final byte is exactly `0xc700`, one byte beyond the allowed
exclusive boundary. MEM reports 40,429 occupied CODE bytes, XRAM 2,512 and
stack allocation capacity 155. The preceding control ended at `0xc748`, so
the 72-byte saving composes in this source snapshot. This remains a rejected
application image, not an approved or installed update.
