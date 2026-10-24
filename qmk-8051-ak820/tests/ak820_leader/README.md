# Compact Leader tests

`host.py` compiles production action, Quantum, Leader, Combo, tap-hold,
One Shot, Caps Word, Repeat and Vial macro code with UBSan. Hardware hooks are
stubbed. It covers the fixed mapping, consumed releases, preheld release,
timeout and wrap, duplicate prefix, cancellation, queued One Shot, Combo
ordering, tap-hold cancellation and unsupported virtual/encoder triggers.

`linked.py` runs the exact linked image in uCsim C52 with simulated peripherals.
It checks every selector, physical ownership, timeout/wrap, clear cancellation,
One Shot retention and an extended macro which re-enters `action_exec`.
The extended macro case keeps a physical key held across idle-tick dispatch
and checks its later release. This checks SDCC static-argument clobber risk;
macro dispatch is at the tail of an idle tick, after every use of its event.

Run the exact-image runtime stack/IRQ gate before linked regression tests.
The configurator registers both suites for `full-leader`. Neither runner opens
USB or proves physical matrix timing, device behavior or persistent storage.
