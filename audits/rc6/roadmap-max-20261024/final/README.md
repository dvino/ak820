# Development profile evidence

All eight profiles pass the linked memory and configuration checks on 2026-10-24.
Full offline regression qualification of the frozen source revision is the next
gate; this initial table records builds only. No profile is approved for release
or installation. No device was opened.

## Exact linked resource use

| Profile | CODE | Main trailing free | Low trailing free | XRAM | Static IRAM | Allocated stack |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `standard` | 39,115 | 1,301 | 84 | 2,612 | 96 | 160 |
| `nkro` | 39,259 | 1,157 | 84 | 2,617 | 97 | 159 |
| `one-shot` | 39,765 | 719 | 16 | 2,622 | 96 | 160 |
| `nkro-one-shot` | 39,909 | 575 | 16 | 2,627 | 97 | 159 |
| `space-cadet` | 39,225 | 1,191 | 84 | 2,615 | 93 | 163 |
| `nkro-space-cadet` | 39,369 | 1,047 | 84 | 2,620 | 94 | 162 |
| `one-shot-space-cadet` | 39,874 | 610 | 16 | 2,625 | 93 | 163 |
| `full` | 40,018 | 466 | 16 | 2,630 | 94 | 162 |

All sizes are bytes. The CODE windows remain `0x28a0..0x2fff` and
`0x3027..0xc6ff`. Trailing free space is measured separately in each window;
alignment holes are not reported as trailing space. Ordinary XRAM remains
`0x0400..0x0fff`, with the fixed LED DMA reservation at `0x0200..0x03ff`.

Allocated stack capacity describes placement, not maximum runtime usage.
No profile has a qualified whole-program bound, exact-image interrupt/nesting
proof or approved installer transition. Same NVM schema is insufficient to
make a different image compatible with release settings restoration.

The standard profile uses 699 fewer CODE bytes than the starting `48ce5fa`
development image (39,814), and 1,198 fewer than published alpha.2 (40,313).
The full profile includes all three new optional features and remains 295
CODE bytes smaller than alpha.2. Its low window has only 16 trailing bytes.
These are complete-image comparisons; individual optimization costs are
nonadditive.

Build identities and source manifests are recorded in
[profile-builds.json](../profile-builds.json). Those are preliminary build
records; final regression records will be bound to their own exact image,
MAP, build report and test source hashes.

## Scope and related evidence

- [Packing change and 3,104 CPU state comparisons](../packing.md).
- [Protocol representation and request comparisons](../protocol-size.md).
- [Compact Space Cadet behavior and interaction tests](../space-cadet.md).
- [Exact-image stack analysis and unresolved roots](../../runtime-stack-20261024/report.md).
- [Deferred feature build probes](../feature-probes.md).
- [QMK Settings storage and migration proposal](../qmk-settings-plan.md).

The published and installed firmware remains v0.6.0-alpha.2. This work neither
publishes nor installs a new release.
