# Compact tapping source review

Date: 2026-10-23. This independent review covers the combined compact MT/LT
source, its recent size reductions, the English and Russian TAP-HOLD documents,
and host verification. No production source was edited. No primary firmware
build, USB command, reset or flash was started by this review.

No source correctness blocker was found in the reviewed supported profile.
Source approval is conditional on closing the documentation items below and
retaining final artifact, linked CPU and package checks as separate gates.
This report does not approve an image or establish installed firmware behavior.

## Checks and evidence

The ACTIVE admission XOR follows an equality rejection with no intervening
callback. It therefore sets ACTIVE on accepted presses and clears it on
accepted releases. Cancellation preserves BLOCKED, converts ACTIVE to BLOCKED,
and drops HELD. The static assertion pins the shift relationship; a released
HELD source is not blocked. The single pending decision is committed before a
new press obtains its layer mapping. Both encoder directions retain separate
source and cached-keycode slots.

The private hook declarations match their definitions. The current combined
build's `quantum/action.asm` places the caller's event parameter and local
record in XSEG. The modifier reference arrays, macro key/usage bitsets and
macro layer byte also reside in XSEG in the current generated assembly. The
reviewed private XDATA arguments originate in these objects. The four modifier
wrappers pass only modes 0–3; their strong/weak and add/remove selections match
the former separate arguments.

Tri Layer target variables remain private. Every accepted setter refreshes the
derived masks and effective layer state; invalid targets change neither.
Derived Adjust is ORed into explicit ownership. The supported profile's
`update_tri_layer` callers use the configured targets. Generic profiles retain
their former implementation. Mutable-target releases use their frozen target.

Macro DOWN/UP changes its retained bitset or modifier mask before changing
reference counts. TAP and ASCII use temporary contributions. Cancellation
clears the retained state and aborts later interpreter output. Caps Word removes
its raw temporary Shift without consuming owned weak modifiers. The AK820-only
send-character mask table is equivalent to the former packed-bit expression
for supported ASCII and retains the generic expression in other profiles.
The system-usage arithmetic preserves the three consecutive HID usages and
rejects values outside that range.

An independent offline rerun used:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/run.py --negative-controls --output /tmp/ak820-final-source-independent.json
```

It exited zero: `pass=true`, all nine mutations rejected, and all 156 eligible
retained-QMK traces matched. The report includes production-body ownership,
macro, Caps Word, accepted-byte, 6KRO/NKRO and mutable Tri Layer checks. A fresh
comparison of every saved source hash against the current tree found no
mismatch. Report SHA256:
`c03a126460f5ebc980338365430c624873c2983d7fe6fe6a3db1a9401a78d7f4`.
This rerun is Host C/UBSan evidence with substituted hardware/user callbacks.
It does not prove SDCC runtime ABI, worst-case stack, task latency, USB timing,
physical switches/encoder behavior or durable storage.

## Documentation closure

The EN/RU TAP-HOLD documents distinguish the supported firmware from the
candidate and describe immediate older releases, interruption policy, ownership,
macro behavior, Caps Word differences and physical-test limits consistently.
Two stale scope statements were sent for closure: the send-string probe's
claim that production integration had not occurred, and the contract's
“Current source” heading for the dated pre-candidate baseline. These are
record-maintenance items; they do not require a production code change.
Follow-up inspection confirms that the contract now labels the baseline
`453fa7c`, and both STATUS translations distinguish the valid measured candidate
from installed firmware and the older 23-suite evidence. The send-string audit
now records primary integration and separates 40,414 populated CODE bytes from
the 40,419-byte MEM span. Its earlier review paragraphs now carry an explicit pre-integration heading
and historical wording. Both documentation scope items are closed. Conditional
source approval therefore has no remaining source or documentation finding;
artifact, linked CPU, package and complete qualification gates remain separate. Final build addresses, memory, hashes, linked execution and package
contents require their own evidence record after the combined checks finish.

## Reset fixture limitation

A later linked-test diagnosis found a configuration difference that limits one
host assertion. The host runner explicitly defines `NO_RESET`; production does
not. The macro containing `QK_CLEAR_EEPROM` therefore exercises
`clear_keyboard(); eeconfig_init()` in the host fixture, with initialization
stubbed. Production instead calls `eeconfig_disable()` and
`soft_reset_keyboard()`. A CPU fixture that patches only `eeconfig_init()` does
not intercept that production path. A timeout at the NVM call is a failed CPU
case, not evidence of a macro ownership defect or a passing reset test.

Source inspection confirms that `soft_reset_keyboard()` calls
`shutdown_quantum()`, whose first operation is `clear_keyboard()`. The cleanup
primitive is present in the production reset path, after `eeconfig_disable()`.
Stopping before that NVM call proves neither successful cleanup nor successful
reset. No production change is justified merely to accommodate the old fixture.

A CPU case that injects `clear_keyboard()` from a report callback can test linked
cancellation during macro playback. It must be reported as a substituted hook
boundary, not as production `QK_CLEAR_EEPROM`, NVM or reset validation. The host
README and machine report should explicitly record the `NO_RESET` branch and
stubbed initialization so that their cancellation claim cannot imply production
reset coverage. This disclosure is an evidence correction required before final
qualification; the source correctness approval remains unchanged. No reset,
NVM write or hardware operation was performed by this review.
