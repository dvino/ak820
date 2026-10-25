# Work-profile IRQ result

**PASS** for the exact final `.build/resume26-work` image. `work26-irq/results.json` is the canonical result; `foreground-stack.json` and the simulator logs retain the supporting observations.

| Identity | SHA256 |
| --- | --- |
| IHX | `a55253c26af1d82a3dd4173297cb9e6cb33209539b251c876f8e36bd4e079c35` |
| MAP | `dc2d68a8fc39a41533391571387a294336f72417f81d8dce554b304a40518e2f` |
| Build report | `26ae176f47c147f56c3c5473b646483ad56321e5948257f5ef4d501e66e56eda` |
| Scoped runner | `cd692d22a959108a12156b1162cd3af0daf826db74ef8c3f569b496cee7dff1f` |

The fresh main bound is **98 bytes with no unresolved paths**. Actual CRT execution reached main at SP 86, compared with initial SP 84. The unique CRT call at 0x3070, bytes `12967f`, confirms the two-byte entry frame. The IRQ CPU model reserved **100 bytes** for foreground and CRT.

All **15 ordered nests** of distinct Timer, USB and LED interrupts passed register/frame restoration and foreground canary checks. All **256 LED selector inputs** passed. Callback bounds are Timer 2, USB 5 and LED 2; the three 17-byte OEM wrappers give **60 IRQ bytes**. The total bound is **160 of 171 available stack bytes**, leaving **11 bytes**.

The two compiled private guards, in `quantum/dynamic_keymap.c` and `quantum/repeat_key.c`, matched this build's source manifest and passed the private source contract checks. The absent Tap Dance guard required no source authentication. Missing or mismatched source for a compiled guard is a hard failure. The selected guard sources, IHX, MAP and build report stayed unchanged during the run.

Every one of the **37,545 occupied CODE bytes** was compared with the exact linked image after each of **17 simulator sessions** and remained unchanged. This legal-window image contains no occupied CODE at or above 0xc700. The runner also rejected any fixture patch overlapping occupied application CODE.

This was one IRQ-only component run. CRT stopped at main entry; main, board, settings and NVM initialization did not run. Generic C52 execution models instructions; the pinned public OEM wrappers and explicit USB ACK side effect supply the interrupt model. Physical IRQ routing and timing, USB transport, LED DMA, storage and device behavior remain unqualified. No full configured regression, build, device operation or production source edit was performed by this task.

The frozen all-feature pass26b runner remains unchanged. This check uses the separate `work_irq.py` runner, frozen at the hash above.
