# Tap and hold tests

Run from the repository root:

```sh
python3 qmk-8051-ak820/tests/ak820_tapping/run.py --negative-controls --output /tmp/ak820-tapping.json
```

This command runs offline. It does not open a keyboard or change settings.
It needs a host C compiler and Python 3.

The fixture compiles the production decoder, source cache, action pipeline,
compact decision engine, modifier and layer owners, Repeat and Tri Layer.
Hardware callbacks and user hooks use host substitutes. Includes are removed
from the combined C source; report-function parameter names are changed to
avoid the firmware's `keyboard_report` macro. Executable statements stay intact.
UBSan checks the host execution for undefined behavior.

The host fixture defines `NO_RESET`. Its EE_CLR trace checks the branch that
clears keyboard state and calls the substituted `eeconfig_init`. The production
image uses the other branch: it disables EEPROM, then resets through shutdown.
Host EE_CLR results do not prove that production reset path, NVM writes or
reset behavior. The public cancellation primitive needs separate linked tests.

The traces cover all 32 MT masks, six LT layers, accepted tap-byte classes,
199/200/201 ms, timer wrap, overlapping owners, live remapping, both encoder
directions, Repeat, persistent and default layers, explicit Adjust ownership,
clear paths, duplicate usages and boot/NKRO reports.
All 30 system/consumer usages share ownership between decoded actions, utility
calls, taps and Repeat. The tests check every same-namespace usage pair, both
release orders, winner restoration and namespace isolation. Duplicate owners
do not change activation order. Tri Layer tests change its targets while a
key is held and check that release still clears the original target. A boot report uses
ErrorRollOver above six distinct usages. Owners survive until release, and
leaving rollover restores all remaining usages. A completed seventh tap
cannot guarantee a typed character; it is not queued for later typing.

`oracle.py` compiles the retained QMK tapping engine with the selected timing
flags. The runner compares 156 eligible output traces. The older Shift-release
case deliberately differs: the compact engine accepts that release immediately.
Eleven mutations must fail: raw Grave Escape registration bypassing ownership,
a lost physical Grave Escape cache, Caps Word
consuming another weak owner, a stale
derived-layer mask, cancellation blocking an already released source, macro
counter wrap, a macro tap consuming a held macro state, an early deadline,
wrong right-hand modifiers, a lost release and a layer lookup before committing
the pending hold.

The fixture also runs the actual macro interpreter, byte grammar checker,
Vial keycode wrappers and ASCII sender. Full 8192-byte streams contain 2725
repeated basic DOWN commands or 2044 extended DOWN commands. Repeated streams,
unmatched UP, temporary TAP/ASCII actions, physical overlaps and cancellation
must preserve their owners. Macro DOWN/UP commands use one persistent state
per basic usage, modifier bit, layer and extra usage. Repeated DOWN is
idempotent; UP clears only that macro state. MT/LT inside these explicit macro
commands keeps its basic-byte action and does not start a physical 200 ms
decision.

Caps Word tests use its actual state machine and handler. Cleanup must remove
its temporary Shift while preserving encoded, Repeat and macro weak owners.
MT/LT taps pass through the normal Caps Word callback. Pure holds defer mode
bookkeeping: MT Shift and LT keep the mode active; after an MT Control hold,
the next ordinary key ends the mode and uses Control. This is a deliberate
compact-engine behavior, not full QMK feature-pipeline equivalence.

These results describe host C execution. Linked 8051 traces, memory and stack
bounds need separate checks. They do not prove physical timing, USB scheduling,
encoder hardware or durable storage. The QMK boundary adapter is a timing
reference, not a decoder or ownership reference.

Grave Escape uses the actual handler in this fixture. Physical, both encoder
and virtual releases after Shift-up must clear the originally resolved Grave.
A physical Escape and a repeated shifted Grave keep separate release actions.
Same-resolved basic/GESC overlaps retain both owners through either release
order. Separate cache and raw-owner mutations reproduce both previous faults.
