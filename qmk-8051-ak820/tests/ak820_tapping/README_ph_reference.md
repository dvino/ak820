# Permissive Hold reference fixture

Run from the repository root:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/ph_reference.py
```

Requires Python 3 and a host C compiler with UBSan (`CC`, default `cc`). This
is an offline host test. It does not build firmware, access a device or change
settings. Temporary executables are created beside the fixture and removed on
completion, avoiding hosts with a non-executable `/tmp`.

The runner compiles the actual retained `quantum/action_tapping.c`, removing
only its include directives. The adapter supplies its types and callbacks;
`action_code.h` and `action_tapping.h` remain actual reference headers. No compact
candidate implementation is included. Existing `oracle.py` tests are unchanged.

Both configurations enable `PERMISSIVE_HOLD`, disable hold-on-other-press and
its per-key override, and use `TAPPING_TERM=200`. Quick Tap is explicitly 0 in
one build and 200 in the other. The latter is equivalent to the reference
header's current default (`QUICK_TAP_TERM=TAPPING_TERM`). These are separate
observations, not a selection of the owner's intended Quick Tap behavior.
Retro Tapping, Retro Shift, per-key timing overrides and One Shot are disabled.
The retained queue has eight slots, seven usable; these traces do not overflow.

## Retained observations

`ph_reference_cases.json` contains every input and complete expected output for
both configurations. Expected outputs were captured from the retained engine
and inspected; they are fixed regression observations, not independent proof
that the reference is correct. The test never regenerates them. Three negative
controls must differ from their matching expectations: disabling PH, moving
the deadline one millisecond late, and removing queued-release scanning.

Input commands are `M position hex-keycode`, `E time position pressed`, and
`T time` (idle tick). Each case runs in a fresh process. Output columns are:

```text
original_event_time dispatch_time position pressed tap_count hex_code hex_mods hex_layers
```

Times are unsigned 16-bit values, including timer wrap. Dispatch time is the
incoming event/tick's time when the callback runs. It is not substituted for
the queued record's original time. Rows describe `process_record` callbacks,
not USB reports. Output order is dispatch order, not original-time order.

The 19 cases cover MT/LT nested and rolling sequences, queued MT/LT release
scanning, repeated taps, 199/200/201 ms deadlines, wrap, and older ordinary versus
modifier release. In the distinguishing older-release cases, another press is
already queued. The older ordinary release executes immediately at time 115;
the older modifier release waits until the MT settles at time 120. A FIFO that
only examines its head would miss this difference. Queued dual-role tests
exercise a release already waiting when that key becomes the tapping key.
The 200-ms Quick Tap configuration continues the second tap immediately;
the zero configuration permits the second press to become a hold at deadline.

## Adapter and pipeline limits

The adapter uses a fixed flat position map and a per-position press cache.
Classification reads the map; execution reads the cache. Inputs do not change
mapping during a lifecycle. Callback modifier/layer bookkeeping is an adapter,
not production ownership, decoding or HID logic. Overlapping modifier/layer
owners are not qualified by this fixture.

In particular, LT hold/tap scheduling is exercised, but **LT-dependent lookup is
not proved**: layer bits do not change the adapter's map. The fixture does not
execute `action_exec`, preprocessing, source-cache refresh, transparent layer
fallback, final quantum lookup, or actual release-identity handling. It cannot
settle when queued presses should be classified or re-resolved relative to an
LT decision, or qualify remapping and repeated lifecycles against that pipeline.
It must not be used to validate a proposed replay/cache policy.

Combo, Leader, Tap Dance, Auto Shift, macros, reentrant callbacks, encoders,
cancellation and safe post-overflow release suppression are outside this test.
The reference's overflow clear is not the owner's requested recovery contract.
No equivalence to a compact candidate, linked-image memory/stack/IRQ bounds,
physical timing, USB behavior or durable storage is claimed.

## Experimental layer-aware boundary fixture

Run separately:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/ph_layer_reference.py
```

This companion extracts retained non-board `action_exec`, preprocessing,
lookup/classification, source-layer caching and tapping functions. It uses a
separate two-layer map. It does not change the flat-map fixture above.
`P` rows show preprocessing; `F` rows show the instrumented final lookup:

```text
F original_time dispatch_time position pressed keycode action tap_count layer_state
```

Keycode, action and layer state are hexadecimal. The LT callback changes the
layer bit before printing `F`. Three host tests cover queued PH re-resolution,
release after layer deactivation and transparent fallback while the layer is
still active. The latter two assert complete final-boundary row sequences,
not only preprocessing or an arbitrary output difference.

The release trace holds LT past 200 ms, presses upper-layer `0005`, releases
LT, then releases the ordinary key. Its final keycode and action remain `0005`
with layer state zero. The release-cache mutant targets the `key` expression
in `store_or_get_action`, not the similar `event.key` expression in
`get_event_keycode`: the final action becomes `0004` while keycode stays `0005`.
The fallback trace releases base `0004` while layer state remains `2`; accepting
transparent layer 1 instead produces keycode/action `0001`. Each mutant must
compile under unchanged `-Werror` and UBSan flags, run successfully, contain
its specific wrong semantic row, and fail the baseline row assertion. Compiler
or process failures are test errors, not qualifying negative controls. PH and
refresh mutations remain separate controls on the queued trace.

The callback is still a stub for ordinary LT(1, KC_ESC) hold transitions.
Source inspection of retained `process_action` supports the momentary-layer
path for zero-tap ordinary LT, but dispatch equivalence is **unproven**: this
fixture does not extract or execute `process_action`, its opcode switch or
retained layer helpers. It also omits `process_record_quantum`,
`process_record_handler` and HID execution. These results qualify only the
retained lookup/tapping boundaries under that stub, not a full action pipeline,
production board code, firmware bounds, installed behavior or hardware timing.
