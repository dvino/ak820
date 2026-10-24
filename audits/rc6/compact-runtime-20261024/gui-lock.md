# Volatile GUI controls

The `gui-lock` implementation filters only the two GUI bits at the final
keyboard-report composition. It leaves raw, weak and reference-counted owners
unchanged, including during off/on transitions. The control handler accepts
only `GU_ON`, `GU_OFF` and `GU_TOGG`, consumes both edges, changes state only
on press and immediately recomposes the report. The state is a zero-initialized
SDCC bit; it is not stored in NVM. Other Magic actions remain disabled.

The isolated `full-gui-lock --short-calls` build uses 39,139 CODE bytes,
232 more than the archive's 38,907-byte `full --short-calls` control. This is
an isolated cost; combined-image costs must be measured again.

The host test extracts the production control and report functions. Under
UBSan it checks all 65,536 keycodes, both edges and both states, then all 256
modifier masks from each of four owner classes. Mixed owners, idempotent
commands and immediate report updates are checked separately.

Eleven linked C52 scenarios cover left/right GUI, held off/on transitions,
encoded Control+GUI ownership, toggles, clear and late releases, preserved
queued/held One Shot state, ordinary One Shot consumption, Repeat history,
NKRO switching, actual busy-endpoint FIFO retry and resume cleanup.

Independent review found that GUI controls initially consumed queued One Shot
state before reaching the report handler. The final implementation exempts
exactly these three controls in the One Shot consumer. New linked cases cover
both queued and held OSM across each control, then prove ordinary consumption. The maximum observed stack use in this suite
is a scenario measurement, not a whole-program bound. The exact result and
image hash are in [gui-lock/linked.json](gui-lock/linked.json); the host result
is in [gui-lock/host.txt](gui-lock/host.txt).

The control names follow the [QMK Magic keycodes](https://docs.qmk.fm/keycodes_magic).
The session-only output-mask behavior above is the AK820 implementation;
upstream persistence and swaps are not implied.

No USB device was opened. Physical timing, endpoint behavior, IRQ overlap and
release qualification are not established by these tests. Independent review
and final integrated build evidence are recorded separately.
