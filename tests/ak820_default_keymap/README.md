Run `python tests/ak820_default_keymap/test_generator.py` for strict extraction, codec boundaries, reserved extraction-phase arguments and exact final table checks.

`compile_tu.py --flags PATH --compiler PATH --output FRESH_DIRECTORY` uses an existing configured build's `cflags.txt` to compile only introspection. It checks current bootstrap bytes, final removal of the original allocation, unchanged encoder/LED bytes, option-off defaults and replacement of a stale generated include. It also rejects an indirectly forced extraction phase and a final-only header changed after dependency discovery. Run inside the cached offline build environment.

The wrapper discovers and freezes bootstrap and final include closures separately. It checks both after compilation, including generated QMK headers, and parses final assembly to require the exact compressed arrays and absence of bootstrap allocations. `generation.json` retains bootstrap provenance and records final dependencies, their hashes, the final discovery command, phase-only dependencies and the intentionally generated include.

`check_decoder.py BOOTSTRAP_ASM` compiles the integrated getter body with host AddressSanitizer/UndefinedBehaviorSanitizer and checks all 16,777,216 uint8 coordinate triples against the compiler-resolved original table. This requires a host C compiler. These checks do not qualify the linked image, stack, reset timing or hardware.


`linked.py` executes the exact linked raw default getter and its option-off
control in the generic C52 simulator. From the repository root, run each shard
with a distinct output directory:

```sh
python3 tests/ak820_default_keymap/linked.py \
  --repo "$PWD" \
  --build "$PWD/qmk-8051-ak820/.build/resume30-default-keymap" \
  --control "$PWD/qmk-8051-ak820/.build/resume30-default-keymap-control" \
  --output /tmp/ak820-default-linked-shard-0 \
  --shard-count 4 --shard-index 0
```

Repeat with shard indices 1–3 and separate output paths. Use the recorded offline
build environment for its simulator dependencies. The accepted four-shard proof
remains at `/home/danil/ChatGPT/ak820-pass26b-restored-20261025/default30-linked-decoder`.
Its `SHA256SUMS`, reports and raw logs bind the exact runner and two images.
The installed runner has identical bytes to that executed external `run.py`.
The [pass 30 audit](../../audits/maximal-pass30-20261025/README.md) validates the
original files without moving or rewriting their paths.

The 275 cases per image include all 256 valid defaults and 19 invalid locations.
Full occupied CODE, return values, stack and canaries are checked. Raw layer
count is established by bootstrap metadata and linked bounds: DCE removed its
function, so no CPU call to that entry is claimed. Cost differences measure
only reset/default lookup instructions and generic C52 ticks. They do not
measure complete reset, real milliseconds or ordinary keypress latency.
No device, network, durable-storage or physical acceptance is involved.
