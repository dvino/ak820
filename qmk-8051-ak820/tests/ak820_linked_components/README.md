# Bounded linked component checks

This runner calls the actual public RGB setter, Combo GET handler and NVM update
kernel, then checks all ordered distinct-source IRQ nests and LED selectors.
It uses the exact linked image and authenticated fixture source inputs. Each
section remains a component model, not a full configured regression suite.

The initializer runs CRT only to main entry and masks IE/IE_EX. It never calls
the ordinary emitted fixture's initializer, seeds NVM, or executes main.
All occupied CODE at or above 0xc700 is compared with the IHX after each
simulator session. Only the reserved test trampolines, public OEM wrapper
fixture and callback slots may be installed outside application windows.
This distinction is necessary for oversized diagnostic images.

Run from the repository root with the matching sources, retained build and
pinned toolchain in `toolchains/sdcc-4.6.0`:

```sh
python3 qmk-8051-ak820/tests/ak820_linked_components/run.py \
  --repo "$PWD" \
  --build "$PWD/qmk-8051-ak820/.build/resume26b-state-bytes" \
  --output /tmp/ak820-linked-components --sections rgb,combo,update,irq
```

Use `--source-root /path/to/exact-source-checkpoint` when inspecting an older
image whose relevant sources differ from the current tree. A missing or changed
manifest input is rejected. The runner derives foreground and CRT frame bounds
from the selected image; it never borrows another profile's main reservation.

The retained 26b result is in
[the current audit](../../../audits/maximal-continuation-20261025/linked-components.md).
The physical flash entry points have stop breakpoints. NVM tests prime the
existing cache and defer writes; dirty page crossings and durable flash failure
are excluded. The C tailwriter may clobber R0/R1. The C52 model and supplied OEM
wrapper/ACK fixtures do not establish real routing, non-reentry, timing, USB,
DMA or hardware behavior. Full configured regressions remain a separate gate.

The catalog-control IRQ-only runner is `work_irq.py`. It authenticates private
guard sources only for compiled guard symbols, so a profile without Tap Dance
requires no Tap Dance source witness. It additionally compares every occupied
CODE byte after every session and rejects fixture writes overlapping application
CODE. See the work command in the current audit.
