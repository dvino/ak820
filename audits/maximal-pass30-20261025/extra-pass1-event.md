# Pass 1: record keycode reuse

Rejected at the component checkpoint. No repository source was edited, no full image was built, and no device or network operation was performed. Exactly one candidate was tried.

The candidate replaces the call to `process_record_quantum(record)` inside the actual `process_record` with a direct helper call. Its keycode argument rereads `record->keycode`; zero still calls `get_record_keycode(record, false)`. No new local retains a keycode across callbacks. Both One Shot post exits and the surrounding stage order remain intact. The normal wrapper remains available to other callers.

## Evidence

`run.py` extracts the actual three C functions from Git `bb91d89`, not the dirty working source. `source-action.c`, `source-quantum.c`, `candidate.patch`, source hashes in `results.json`, generated C, compiler listings and REL files preserve the inputs and outputs. The record layout follows the actual `action.h` and `keyboard.h`, including the event type and tap bit fields. The packed key-position argument is 16 bits, as in `keymap_common.h`.

Actual source contract: Dynamic Macro receives a value and cannot edit the record. One Shot also receives only values; its current body does not recurse into event processing. The One Shot boundary writes the resolved code into the record. A zero result is still a sentinel: the Quantum boundary must resolve again with `update_layer_cache=false`. A nonzero cached value is returned without resolver side effects. The candidate evaluates this choice at that same boundary. No modifier, layer, timer, or ownership cache is introduced.

The extracted C control chain passed 12,288 baseline/candidate cases with byte-identical ordered traces. Cases combine Dynamic Macro, One Shot and Quantum consumption; physical and synthetic positions; primitive/repeat flags; zero, transparent and ordinary codes; six starting layers; press/release; all five event types; times crossing the 16-bit wrap; nested helper/handler calls; record mutation; and clear/report effects. Traces include all record fields, stage calls, resolver arguments, modifier/layer/owner state and modeled reports. Three mutants were killed: missing zero fallback, wrong layer-update argument, and missing consumed-path One Shot post.

These are bounded leaf contracts. The oracle does not execute Combo, Tap Dance, Repeat or Macro implementation bodies, model all report types, capacities or storage, or emulate SDCC nonreentrant automatic allocation. Nested calls exercise the wrapper boundary only. The trace result cannot qualify all fourteen features, IRQ safety, device behavior or exact-image stack usage. Extending this into a whole-keyboard framework was stopped because the component already fails the size checkpoint.

## Component result

Pinned SDCC 4.6.0 compiled the actual extracted functions in model-large, with the board's speed flag followed by size optimization and the exact audited callee-saves list from `util/build_ak820.py`. Leaf declarations and manually selected active preprocessor branches replace the full translation-unit headers. This is a standalone component measurement, not the exact full preprocessed image context. No full-image outliner or short-call pass was run.

| Measurement | Baseline | Candidate |
|---|---:|---:|
| CSEG | 565 | 627 |
| process_record body | 404 | 466 |
| Quantum wrapper | 58 | 58 |
| getter | 103 | 103 |
| DSEG | 1 | 1 |
| BSEG bits | 1 | 1 |
| XSEG | 7 | 7 |
| Static push/pop instructions | 22/22 | 28/28 |

Raw growth is 62 CODE bytes. Even subtracting the entire 58-byte wrapper under the most favorable assumption that no other caller retains it leaves four bytes of growth. That subtraction is a component estimate, not a linker result. RAM is unchanged within this component; no full-image RAM claim follows.

On a cached nonzero code, the candidate skips the wrapper/getter call chain. A zero code still calls the getter. There are no new loops, waits, delays, ISR paths or persistent state. The generated caller nevertheless grows and has six additional static push/pop sites; static instruction counts are not runtime milliseconds. `component-shapes.json` records the emitted calls and function sizes. No full startup/IRQ/foreground stack bound is claimed, and this candidate must not be installed.

## Repeat

The host lacks GCC, so the existing local study image was used offline. The repository mount is read-only; only this external directory is writable. The numeric user is the local Docker namespace mapping for the directory owner.

```sh
docker run --rm --user 898 --network none -e EVENT_REPO=/repo \
  -v /home/danil/ChatGPT/ak820-pass26b-restored-20261025/ak820-max:/repo:ro \
  -v /home/danil/ChatGPT/ak820-bounded-final-passes-20261025/pass1-event:/work \
  ak820-nkro-study-env:local python3 /work/run.py
```

`run.log` and `results.json` contain results and compiler commands. The compiled chain is intentionally small. This rejected candidate has not received independent approval. No second variant or new research branch was started.
