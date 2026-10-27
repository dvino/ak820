Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

## v0.6.0-beta.3 firmware qualification, 2026-10-26

All ten unchanged profile configurations have completed exact-image firmware
qualification. Each profile passed 28 base qualification suites with 351 unit tests and
zero skips. The separate profile regression runs passed 32 to 37 supplementary
suites. Stack bounds cover startup, foreground code and every enabled
interrupt source; all are within the reported capacity.

| Profile | CODE bytes | XRAM bytes / 3008 | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: |
| main | 40,466 | 2,858 / 3,008 | 160 / 182 | 22 |
| game | 40,462 | 2,932 / 3,008 | 160 / 177 | 17 |
| mmo | 40,343 | 2,935 / 3,008 | 164 / 180 | 16 |
| typing | 38,720 | 2,351 / 3,008 | 160 / 184 | 24 |
| code | 38,467 | 2,342 / 3,008 | 160 / 184 | 24 |
| pointer | 38,902 | 2,361 / 3,008 | 160 / 184 | 24 |
| onehand | 38,806 | 2,388 / 3,008 | 164 / 185 | 21 |
| creative | 39,903 | 2,869 / 3,008 | 164 / 183 | 19 |
| shortcuts | 38,796 | 2,405 / 3,008 | 164 / 185 | 21 |
| multios | 38,415 | 2,335 / 3,008 | 160 / 184 | 24 |

Direct v1 is present in `main`, `game`, `mmo` and `creative`. It supports RAM-only
readback of the 82-color HSV palette and atomic full-frame uploads. In `game`
and `mmo`, GUI lock is off by default. When enabled, it pulses W through a
2000 ms brightness cycle; an active or default layer above zero takes
steady-light priority.

The release uses Python installation packages for Windows and Linux x86_64.
The GUI installer is excluded; the companion application is separate. Firmware
qualification, package assembly and independent approval have separate
records for each exact image. Source evidence is indexed in
`audits/beta3-direct-20261026/README.md`.
Release acceptance on 2026-10-27 passed 303 host tests, 186 installer/settings
tests, four catalog-edge regression tests and checks of 79 public documents.
Independent firmware and host reviews are retained alongside the source evidence.
Publication requires successful CI for the final merged `main` commit and its
release tag. No hardware or device writes were performed during acceptance.
Physical USB, LED and DMA timing, and power-loss or durable-storage behavior
remain unverified.

The last historical installation was alpha.3 on 2026-10-24, image SHA256
`d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`. This is
a historical device record and does not establish beta.3 device behavior.
