# Ten-profile local qualification (2026-10-28)

All ten physical-window images completed their own local offline qualification,
with SDCC and s51 required. Each passed the runtime stack proof and all relevant
host/CPU and linked-image profile tests. Each common qualification includes
356 unit tests with zero skipped; the number of profile suites varies with
enabled modules. Source, image identities and memory headroom are in
[measurements.md](measurements.md). Source commit was dirty, so these results
must not be represented as a clean build of that commit. These results do not
claim hardware validation or release approval.

| Profile | Common suites | Profile suites | Offline | Stack proof | Physical commands |
| --- | ---: | ---: | --- | --- | ---: |
| main | 36 | 36 | pass | pass | 0 |
| game | 36 | 36 | pass | pass | 0 |
| mmo | 36 | 36 | pass | pass | 0 |
| typing | 36 | 36 | pass | pass | 0 |
| code | 36 | 34 | pass | pass | 0 |
| pointer | 36 | 36 | pass | pass | 0 |
| onehand | 36 | 36 | pass | pass | 0 |
| creative | 36 | 34 | pass | pass | 0 |
| shortcuts | 36 | 34 | pass | pass | 0 |
| multios | 36 | 39 | pass | pass | 0 |

Each configuration report, qualification report and per-suite logs are in the
local build directory identified in the measurement record. Stack bounds are
conditional on the assumptions recorded in each report, including CRT entry with
interrupts disabled, valid memory accesses and the SDCC bank-0 ABI. OEM wrappers
are a pinned reference, not a connected-device identity check. No device was
flashed, reset or otherwise accessed. Successful offline checks are not a claim
that flashing is authorized or physical behavior validated.
