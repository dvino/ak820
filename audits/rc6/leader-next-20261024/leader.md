# Compact Leader

The development profile `full-leader` adds a physical `QK_LEAD` prefix and one
selector within 300 ms. `1`–`9`, `0`, `A`–`F` select the 16 existing Vial macro
slots. Macro contents remain editable in Vial. The implementation does not
change the six-layer keymap, 8192-byte macro store, eight Combo slots, NVM
schema `0x082002`, loader or recovery path.

The [user guide](../../../docs/COMPACT-LEADER.md) describes selection,
cancellation and unsupported inputs. This report records implementation and
verification. No device command or physical test was performed; the published
and installed alpha.3 image remains unchanged.

## Event ownership

A bounded bitmap owns releases for consumed physical presses. Releases of
previously held keys continue to their normal owner, including after a layer
change. Tapping admission rejects duplicate presses and blocks held sources
after shared cancellation. Encoder, virtual, Repeat and Combo outputs cannot
start a sequence. Unknown ordinary nonmodifier keys cancel and are consumed;
modifiers and other controls cancel and act normally.

Only one macro can wait for dispatch. Its slot is cleared before the existing
interpreter is called. Dispatch occurs at the tail of an idle `action_exec`
tick, after its event and record are no longer used. This placement also
avoids recursion through interpreter-generated key events. No stack-analyzer
whitelist or proof assumption was added for Leader.

## Review findings and corrections

1. Dispatch at the beginning of `action_exec` could let an extended Vial macro
   overwrite SDCC's static by-value argument and record before the outer
   physical event was processed. The linked allocation confirmed the risk.
   Dispatch moved to the idle-tick tail. A linked regression holds a physical
   key across a macro containing virtual `QK_LEAD` events and checks its final
   release and the absence of recursive selection.
2. A buffered Combo could otherwise flush after macro selection, reorder
   earlier input and consume a queued One Shot modifier. Prefix admission now
   settles buffered Combo input first. An active Combo keeps its owner. The
   production-C host case checks the ordering.
3. Several prefixes before the next idle tick could overwrite an already
   selected macro. A prefix received while a macro is pending is consumed
   without rearming selection. Host and linked cases check distinct physical
   prefix positions and retention of the first slot.

Independent review also checked source-index bounds, suppression through
mapping changes, shared clear/NKRO/unlock cancellation, timer wrap, unsupported
inputs and queued One Shot ownership. The integrated source and bilingual
guides have no remaining correctness finding. The integrated evidence is
listed below.

## Integrated image

The image combines Leader with the accepted [report pointer optimization](optimization.md).
The exact-image runtime gate ran before the regression suites:

| Measurement | Bytes |
| --- | ---: |
| CODE | 39,606 |
| Main CODE trailing space | 878 |
| XRAM | 2,627 |
| Foreground control stack | 97 |
| CRT main-entry frame | 2 |
| All distinct-source IRQ paths | 61 |
| Combined stack bound | 160 |
| Allocated stack | 162 |
| Remaining stack | 2 |

The integrated image passes all 28 base suites and 273 unit tests without
skips, all 22 supplemental suites, and all 26 linked Leader cases. Tests use
their normal sanitizer configuration with no external overrides. The existing
bounded fixture retains its own leak-check exception. The exact IHX SHA256 is:

`c9764ed8044836270c467a56d5d36162d4d810e864b67ebd7ab7abd4b3c39471`

The complete build, machine reports and command log are retained in
`probes/integrated-leader/`; hashes and resource measurements are in
[probes.json](probes.json). This pre-freeze candidate records its modified
source honestly. The [final matrix](final/README.md) subsequently rebuilt all
20 variants from one clean source commit and supersedes this candidate.

Independent evidence review verified all 131 integrated files and five
isolated-candidate files against the manifest, opened the complete raw build
archive and checked the image, runtime and suite results. The source,
bilingual documentation and pre-freeze evidence are approved for the feature
commit. No finding remains open in this package. Final matrix review is
recorded in the [change report](README.md).

The earlier isolated Leader candidate used 39,640 CODE bytes and the same
160/162 stack bound. It passed all 22 supplemental suites and 26 linked Leader
cases. Its base run reported a missing Russian guide/language link. Adding
the translated guide and reciprocal links closed that documentation failure;
the check then passed for all 53 public documents. The integrated run repeated
all base suites with those files present. The initial documentation failure
and isolated reports are retained in `probes/leader-isolated/`.

The linked Leader cases cover all 16 selectors, expiry at 300 ms, timer wrap,
preheld releases, clear while held, pending-slot protection, unsupported
encoder input and Escape cancellation. A nonempty slot-0 macro sends shifted
`KC_Z` through the actual interpreter and HID trace, while the queued One Shot
remains available for the following physical key. Host tests use production C
with UBSan; linked tests run the exact SDCC image on the pinned CPU simulator.

## Limits

The stack result assumes valid accesses, the bank-0 SDCC ABI and MCS-51
in-service/RETI semantics. It includes all three enabled interrupt sources;
it does not assume only two priority levels. The public wrapper fixture does
not establish physical VS11 timing or a connected device's identity.

Longer Leader sequences, a configurable sequence dictionary, encoder entry
and additional Leader feature combinations are not implemented. Release
approval, installer transition and physical behavior remain separate work.
