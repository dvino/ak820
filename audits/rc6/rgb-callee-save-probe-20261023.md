# RGB helper register preservation probe

This private probe tests whether adding `handleKeycodeRGB` to SDCC's
`--callee-saves` list saves linked code. It changes no production source and
does not access the keyboard.

The helper is defined in `quantum/process_keycode/process_rgb.c`, not
`quantum.c`. It is a static function that returns no value. All ten linked
calls come from `process_rgb` in the same translation unit. The frozen raw
assembly has no reference to this helper in any other translation unit, and
the C source does not take its address. The existing discovery report agrees
with this inventory. Adding its name only when compiling `process_rgb.c`
therefore covers both its definition and every caller; other units cannot
depend on this private calling convention.

The initial saving hypothesis does not hold. The control assembly already
has no register pushes or pops in `process_rgb`, including at all ten calls.
The candidate removes no caller spills. Instead, each helper branch pushes
registers r7 through r0, calls the selected RGB action through
`__sdcc_call_dptr`, restores r0 through r7 and returns. Both control branches
tail-jump to that indirect-call trampoline. The helper returns void, so it
does not have a return-register conflict. The public boolean return from
`process_rgb` remains a separate function contract.

The candidate needs eight register-save bytes plus an additional two-byte
return address while an action runs, compared with the control tail call.
The build's reported stack capacity is free space, not proof of worst-case
stack use. The pinned application wrappers use register bank 0; no wrapper,
interrupt handler or register-bank option changes in this probe. The helper
is reached through the existing foreground RGB processing path.

The private folder is
`qmk-8051-ak820/.build/rc6-rgb-callee-probe-20261023`.
`probe.py` compiles the saved-source control and the candidate with the exact
saved flags, differing only by the extra callee-save name. It replaces this
one unit in frozen assembly, runs the existing dead-code removal and
outlining passes, and links both configured code windows. The control must
reproduce the canonical IHX byte for byte before the candidate link is
accepted. `report.json`, `asm-evidence.json` and `linked-report.json` retain
the commands and results.

The control reproduced canonical IHX
`ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`
byte for byte. The candidate IHX is
`0ffd59e9ed4b18fa4b786f62114bb3d91047a71c4196bec73b9010a5fd1747e3`.

| Linked measurement | Control | Candidate |
| --- | ---: | ---: |
| Code bytes | 39,432 | 39,498 |
| Main window bytes | 37,573 | 37,639 |
| Low window bytes | 1,859 | 1,859 |
| XRAM bytes | 2,071 | 2,071 |
| Reported stack capacity | 152 | 152 |
| Outlined helpers / sites | 32 / 221 | 32 / 221 |

Reject this candidate. It adds 66 linked code bytes and increases stack use
along the helper path, with no caller saving. Both links passed the code
window and memory checks. CPU regression tests were skipped because this
candidate will not be integrated. The static calling-convention inspection
does not prove interrupt behavior, physical RGB output or timing on hardware.
No CPU or hardware result is claimed.
