# Whole-image stack and interrupt matrix

All **21 named profiles and 23 build variants** pass from clean frozen source
`1187d4cedd439733bd0c7ceb5c41daac9089de5b`. The two additional variants use
short calls for `full` and `full-mouse-auto-shift`. The two larger named profiles
shown with short calls require that setting.

Each proof covers the whole linked foreground rooted at `_main`, C runtime
startup, the persistent CRT entry frame and all enabled USB, timer and LED
interrupt roots with their OEM wrappers. No required root is unresolved.
All 15 orders of distinct interrupt sources and 256 LED selector values pass
for every image. The combined IRQ allowance is 61 bytes; CRT contributes two.
Total use is the larger of pre-main use and foreground + CRT + all IRQs.

| Build | Foreground | CRT | IRQs | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| [full](full/record.json) | 97 | 2 | 61 | 160 / 166 | 6 |
| [full-auto-shift](full-auto-shift/record.json) | 97 | 2 | 61 | 160 / 166 | 6 |
| [full-auto-shift-dynamic-macro --short-calls](full-auto-shift-dynamic-macro-short/record.json) | 97 | 2 | 61 | 160 / 165 | 5 |
| [full-ctrl-gui](full-ctrl-gui/record.json) | 101 | 2 | 61 | 164 / 166 | 2 |
| [full-dynamic-macro](full-dynamic-macro/record.json) | 97 | 2 | 61 | 160 / 165 | 5 |
| [full-dynamic-macro-gui](full-dynamic-macro-gui/record.json) | 101 | 2 | 61 | 164 / 165 | 1 |
| [full-gui-lock](full-gui-lock/record.json) | 101 | 2 | 61 | 164 / 166 | 2 |
| [full-leader](full-leader/record.json) | 97 | 2 | 61 | 160 / 162 | 2 |
| [full-mac-pc](full-mac-pc/record.json) | 101 | 2 | 61 | 164 / 166 | 2 |
| [full-mac-pc-os-indicators](full-mac-pc-os-indicators/record.json) | 101 | 2 | 61 | 164 / 166 | 2 |
| [full-mouse](full-mouse/record.json) | 97 | 2 | 61 | 160 / 166 | 6 |
| [full-mouse-auto-shift](full-mouse-auto-shift/record.json) | 97 | 2 | 61 | 160 / 166 | 6 |
| [full-mouse-auto-shift-gui --short-calls](full-mouse-auto-shift-gui-short/record.json) | 101 | 2 | 61 | 164 / 166 | 2 |
| [full-mouse-auto-shift --short-calls](full-mouse-auto-shift-short/record.json) | 97 | 2 | 61 | 160 / 166 | 6 |
| [full-os-indicators](full-os-indicators/record.json) | 97 | 2 | 61 | 160 / 166 | 6 |
| [full --short-calls](full-short/record.json) | 97 | 2 | 61 | 160 / 166 | 6 |
| [nkro](nkro/record.json) | 98 | 2 | 61 | 161 / 162 | 1 |
| [nkro-one-shot](nkro-one-shot/record.json) | 97 | 2 | 61 | 160 / 162 | 2 |
| [nkro-space-cadet](nkro-space-cadet/record.json) | 98 | 2 | 61 | 161 / 166 | 5 |
| [one-shot](one-shot/record.json) | 97 | 2 | 61 | 160 / 162 | 2 |
| [one-shot-space-cadet](one-shot-space-cadet/record.json) | 97 | 2 | 61 | 160 / 166 | 6 |
| [space-cadet](space-cadet/record.json) | 98 | 2 | 61 | 161 / 166 | 5 |
| [standard](standard/record.json) | 98 | 2 | 61 | 161 / 162 | 1 |

The smallest margin is **one byte**, in `standard`, `nkro` and
`full-dynamic-macro-gui`. The combined Mac/PC + OS image has two bytes.
A changed image requires a new proof; these margins are not spare capacity
for an unmeasured feature. All twenty pre-existing variants reproduce the
accepted IHX bytes; see [comparison](../accepted-ihx-comparison.json).

## Evidence and scope

The [matrix](matrix.json) binds each row and its retained archive. Each archive
contains every reported compiler artifact, generated build source, relocated
listing and complete runtime CPU scripts/logs. Source files and checkers are
bound to Git blobs at the frozen commit. IHX, MAP and MEM also reconstruct CODE,
XRAM and stack placement. Proof components are recombined during verification.
The verifier requires the complete supported profile set, all roots, clean
source, tool pins, hashes, IRQ coverage and a nonnegative margin.

Four images (`full` and the three new module profiles) additionally pass the
[complete regression matrix](../final/README.md): 28 base suites and 273 unit
tests without skips per image, plus 92 supplemental suite executions in total.
The other 19 rows have fresh runtime proofs; their full regression suites were
not rerun in this work package. That distinction is recorded per row.

Run both retained-evidence checks from the repository root:

```sh
python3 audits/rc6/web-firmware-20261024/verify_matrix.py
python3 audits/rc6/web-firmware-20261024/runtime_matrix.py verify \
  --root . --final-dir audits/rc6/web-firmware-20261024/runtime-all
```

These checks need retained artifacts and Git history, not the original temporary
build paths. They check local consistency, not signatures or authentication.
Independent final review passed both retained-evidence verifiers and checked
all 23 rows against the English and Russian documentation.

The runtime premises remain valid accesses, bank-0 SDCC calls, disabled IRQs at
CRT entry and MCS-51 in-service/RETI behavior. All distinct interrupt-source
orders are considered, without assuming only two priority levels. Pre-CRT trial
erase, physical timing, power loss and actual device behavior are separate.
No physical device command was sent; no new image is installed or release-approved.
