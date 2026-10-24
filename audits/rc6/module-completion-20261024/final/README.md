# Final firmware module matrix

All 24 named profiles and 26 linked variants pass exact-image foreground,
startup and all enabled interrupt checks. The runtime proof precedes full
regression. Four images additionally pass 28 base suites and 276 unit tests
without skips each, plus 90 supplemental suites in total.

Firmware compiler inputs are frozen at `ac48c65`. The full regression uses
`147508e`, whose follow-up changes are confined to test fixtures and audit
records. The 22 runtime-only rows retain their original `ac48c65` source
identity. No previous-source result is substituted for a changed image.

| Variant | CODE bytes | XRAM bytes | Stack bound/capacity | Margin | Regression scope |
| --- | ---: | ---: | ---: | ---: | --- |
| `full` | 38447 | 2555 | 162/167 | 5 | 28 + 21 |
| `full-auto-shift` | 39055 | 2572 | 162/166 | 4 | runtime only |
| `full-auto-shift-dynamic-macro-short` | 39902 | 2658 | 162/165 | 3 | runtime only |
| `full-ctrl-gui` | 38745 | 2558 | 162/166 | 4 | runtime only |
| `full-dynamic-macro` | 39500 | 2641 | 162/165 | 3 | runtime only |
| `full-dynamic-macro-gui` | 39649 | 2644 | 162/165 | 3 | runtime only |
| `full-gui-lock` | 38602 | 2558 | 162/166 | 4 | runtime only |
| `full-key-overrides-short` | 40464 | 2734 | 162/162 | 0 | 28 + 23 |
| `full-leader` | 39117 | 2582 | 162/163 | 1 | runtime only |
| `full-mac-pc` | 38654 | 2558 | 162/166 | 4 | runtime only |
| `full-mac-pc-os-indicators` | 39091 | 2567 | 162/166 | 4 | runtime only |
| `full-mouse` | 39297 | 2585 | 162/167 | 5 | runtime only |
| `full-mouse-auto-shift` | 39905 | 2602 | 162/166 | 4 | runtime only |
| `full-mouse-auto-shift-gui-short` | 39818 | 2605 | 162/166 | 4 | runtime only |
| `full-mouse-auto-shift-short` | 39683 | 2602 | 162/166 | 4 | runtime only |
| `full-os-indicators` | 38899 | 2564 | 162/167 | 5 | runtime only |
| `full-qmk-settings-short` | 40075 | 2640 | 162/166 | 4 | 28 + 23 |
| `full-short` | 38220 | 2555 | 162/167 | 5 | runtime only |
| `full-tap-dance-short` | 40173 | 2795 | 166/166 | 0 | 28 + 23 |
| `nkro` | 37766 | 2542 | 156/163 | 7 | runtime only |
| `nkro-one-shot` | 38327 | 2552 | 162/163 | 1 | runtime only |
| `nkro-space-cadet` | 37878 | 2545 | 156/167 | 11 | runtime only |
| `one-shot` | 38188 | 2547 | 162/163 | 1 | runtime only |
| `one-shot-space-cadet` | 38308 | 2550 | 162/167 | 5 | runtime only |
| `space-cadet` | 37739 | 2540 | 156/167 | 11 | runtime only |
| `standard` | 37627 | 2537 | 156/163 | 7 | runtime only |

The two additional variants are `full-short` and
`full-mouse-auto-shift-short`. Required short-call builds also use a `-short`
suffix in this table. The minimum margin is zero for Tap Dance and Key
Overrides; any change requires a new exact-image proof.

Each row retains all runtime artifacts and component witnesses. The four
`full/` rows retain complete raw build trees, including prior failed fixture
or restricted-environment attempts when present. Only the final successful
reports qualify an image. All ordinary sanitizer options remain enabled.
`matrix.json` binds every row and archive by SHA256. The deterministic
`capability-catalog.json` contains only the four completely qualified images.
Each catalog fragment was generated and validated in its original source
checkout, then combined with duplicate CODE identities rejected.

Portable row verification:

```sh
python audits/rc6/module-completion-20261024/retain_evidence.py verify \
  --root . --source-commit SOURCE_COMMIT --final-dir ROW_DIRECTORY
```

Use the row's full `source_commit`. The verifier checks retained bytes and
frozen source bindings without requiring the original checkout paths or
repeating CPU suites; see [retention contract](../EVIDENCE.md).

No physical device command was sent. Hardware validation, release approval,
settings-write permission and flashing permission remain false. Physical USB
timing, durable writes, power-loss behavior and installer transition approval
are outside these offline results. Published and installed alpha.3 is unchanged.
