# Qualified development matrix

All 18 named profiles and 20 build variants pass from clean frozen source
`d04290b799b1921a55f020ee3cfe041199fae244`. The two additional variants enable
`--short-calls` for `full` and `full-mouse-auto-shift`. The two larger named
profiles shown with that option require it. Compiler and simulator are the
pinned SDCC 4.6.0 tools; each record retains their exact hashes.

Every build first passes the exact linked foreground, CRT startup and all
three interrupt-source checks. It then passes 28 base suites and 273 unit
tests without skips, plus 16–26 supplemental suites. Tests retain
their normal sanitizer configuration, with no external sanitizer overrides.
Across 20 images this is 560 base-suite executions,
5,460 repeated base unit-test executions and 423 supplemental-suite executions;
these totals do not represent that many distinct test cases.

| Build | CODE bytes | Main / low trailing free | XRAM | Stack bound / capacity | Margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| [standard](standard/record.json) | 38,044 | 2,372 / 84 | 2,582 | 161 / 162 | 1 |
| [nkro](nkro/record.json) | 38,183 | 2,233 / 84 | 2,587 | 161 / 162 | 1 |
| [one-shot](one-shot/record.json) | 38,637 | 1,847 / 16 | 2,592 | 160 / 162 | 2 |
| [nkro-one-shot](nkro-one-shot/record.json) | 38,776 | 1,708 / 16 | 2,597 | 160 / 162 | 2 |
| [space-cadet](space-cadet/record.json) | 38,159 | 2,257 / 84 | 2,585 | 161 / 166 | 5 |
| [nkro-space-cadet](nkro-space-cadet/record.json) | 38,298 | 2,118 / 84 | 2,590 | 161 / 166 | 5 |
| [one-shot-space-cadet](one-shot-space-cadet/record.json) | 38,751 | 1,733 / 16 | 2,595 | 160 / 166 | 6 |
| [full](full/record.json) | 38,890 | 1,594 / 16 | 2,600 | 160 / 166 | 6 |
| [full-leader](full-leader/record.json) | 39,606 | 878 / 16 | 2,627 | 160 / 162 | 2 |
| [full-gui-lock](full-gui-lock/record.json) | 39,125 | 1,359 / 16 | 2,603 | 164 / 166 | 2 |
| [full-ctrl-gui](full-ctrl-gui/record.json) | 39,268 | 1,216 / 16 | 2,603 | 164 / 166 | 2 |
| [full-dynamic-macro-gui](full-dynamic-macro-gui/record.json) | 40,247 | 237 / 16 | 2,689 | 164 / 165 | 1 |
| [full-mouse-auto-shift-gui --short-calls](full-mouse-auto-shift-gui-short/record.json) | 40,359 | 125 / 16 | 2,650 | 164 / 166 | 2 |
| [full-auto-shift-dynamic-macro --short-calls](full-auto-shift-dynamic-macro-short/record.json) | 40,391 | 93 / 16 | 2,703 | 160 / 165 | 5 |
| [full-dynamic-macro](full-dynamic-macro/record.json) | 40,012 | 472 / 16 | 2,686 | 160 / 165 | 5 |
| [full-mouse](full-mouse/record.json) | 39,740 | 744 / 16 | 2,630 | 160 / 166 | 6 |
| [full-auto-shift](full-auto-shift/record.json) | 39,503 | 981 / 16 | 2,617 | 160 / 166 | 6 |
| [full-mouse-auto-shift](full-mouse-auto-shift/record.json) | 40,353 | 131 / 16 | 2,647 | 160 / 166 | 6 |
| [full --short-calls](full-short/record.json) | 38,643 | 1,841 / 16 | 2,600 | 160 / 166 | 6 |
| [full-mouse-auto-shift --short-calls](full-mouse-auto-shift-short/record.json) | 40,132 | 352 / 16 | 2,647 | 160 / 166 | 6 |

The minimum stack margin is 1 byte. Every total includes a two-byte
persistent CRT frame and 61 bytes for all distinct-source IRQ paths. Each
image passes all 15 interrupt orders, all 256 LED selector values and seven
delay-ABI CPU cases. `full-leader` additionally passes all 26 linked Leader
cases and the production-C host fixture.

Each row retains IHX/MAP/MEM, build/configuration reports, runtime proofs,
base and supplemental results, logs, and the complete build as
`raw-build.tar.xz`. [matrix.json](matrix.json) binds the row and raw-archive
hashes. The verifier checks those hashes, raw/loose equality, source blobs at
the frozen commit, the required suite plans, exact image identities and all
runtime contracts:

```sh
python3 audits/rc6/leader-next-20261024/verify_matrix.py
```

These are static and host/CPU-model results. They assume valid accesses,
bank-0 SDCC calls and MCS-51 in-service/RETI semantics, without a two-priority
assumption. They do not establish physical VS11 timing, flash behavior,
power-loss behavior or connected-device identity. No device command was sent.
No changed image is release-approved or installed by this work. See the
[change report](../README.md) and [runtime contract](../../../../docs/RUNTIME-STACK.md).
