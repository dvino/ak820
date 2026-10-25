# Pass 27: USB classifier

The maximal image retains all 14 modules and all base functions. The linked
classifier change saves 48 CODE bytes against the byte-identical reproduced
26b: 44,747 → 44,699. Physical XRAM remains 3,007 bytes and stack capacity 167.
Main CODE still overflows by 4,346 bytes. This image is not installable.

The current-source work control saves 75 CODE bytes against the archived work
control: 37,545 → 37,470. It uses 2,554 physical XRAM bytes. Its conditional
stack bound is 160/171; maximal remains 165/167. These conditional bounds do
not close the complete OEM startup, bank, routing or non-reentry contracts.

## Reproduce the ledger

Run from the repository root; no build or device action is performed:

```sh
python3 audits/maximal-pass27-20261025/collect.py --output audits/maximal-pass27-20261025/measurements.json --current-output docs/maximal-current.json
```

The collector fails on missing or changed build artifacts, source/toolchain
inputs, image/map/listing identities, startup evidence and CPU support inputs.
For the historical 26b source difference, it verifies the original `cfd05a0`
Git blob; all matching inputs and generated files are checked in place.
The reproduced baseline IHX matches archived 26b SHA256
`47400365dfe8e7e56fd46a548938ca8c9024467ca13120f506cb7213e9f7ef10`.
Source and artifact verification are separate; historical sources are not
claimed to match the current tree.

## Retained checks

- `host-regression.jsonl`: all 16,777,216 three-byte prefixes match the switch
  oracle; both admission mutants are detected.
- `startup.json`, `work-startup.json`: fresh exact-image CRT checks; execution
  stops at main entry.
- `read-hook.json`: conditional reader preservation, 45 reachable instructions
  and seven rejected mutations. Read values and opaque writer are outside scope.
- `linked-checks.json`: 629 RGB, 576 Combo GET and 48 cache-only updater cases;
  15 distinct-source IRQ orders and 256 LED selectors. All 4,346 occupied high
  CODE bytes remain unchanged in 20 sessions. Flash entry is excluded.
- `work-irq.json`: 15 IRQ orders and 256 selectors, all 37,470 occupied CODE
  bytes unchanged in 17 sessions; conditional stack bound 160/171.
- `maximal-context.json`, `work-context.json`: exact newly generated and reviewed
  context certificates, preserved without edits. Their absolute paths and
  source/tool/ASM hashes record original provenance. After relocation, preserve
  these certificates as source locks; generate and independently review fresh
  contexts before a new build. Do not rewrite certificate paths to imply review.
- `baseline-context-review.md`, `source-context-review.md`,
  `work-context-review.md`: bounded source and context reviews. [Independent final
  integrated review](review.md) approves the bounded research source and evidence.
  It does not qualify firmware for installation, release or hardware use.

Large CPU logs remain outside this directory in retained sibling directories
`../classifier27-linked-checks/` and `../classifier27-work-irq/` relative to the
repository root. Compact JSON and JSONL evidence is copied byte for byte.
The previous `audits/maximal-continuation-20261025/` packet stays historical and
unchanged. Old context certificates are preserved; fresh certificates qualify
only their exact inputs.

The complete-feature objective remains open: legal maximal CODE placement,
complete OEM startup/IRQ and application-bank contracts, opaque-writer proof,
full configured functional regressions and physical validation are still
required. No device writes, reset, bootloader transition, flashing, packaging
or release changes were performed.
