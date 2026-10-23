# Independent Combo candidate review

## Decision and scope

The reviewed source, normal application build and evidence package are approved
for the development commits and Git archive. No blocking code, format,
documentation or verification finding remains. This decision does not approve
installation, a complete flashable ROM, installer promotion or a release.
Physical acceptance and Combo backup migration remain open.

This review was independent of implementation. No firmware, test, compiler-tool
or product-documentation changes were authored by this review. The only authored
file is this report. No commit or hardware operation was performed.

The comparison starts at `4b83bb9` on `dev/compact-combos-20261024`. Review covered
the compact Combo engine, storage extension and Vial hooks; action and HID report
changes; typed EEPROM paths and parser copies; USB request dispatch and descriptor
pointers; RGB arithmetic; compiler pragmas and exact outlining; new and corrected
tests; and the English/Russian public documentation and technical evidence.

## Artifact binding

The normal build in `qmk-8051-ak820/.build/combos-candidate` was independently
hashed after qualification:

| Artifact | SHA256 |
| --- | --- |
| Application IHX | `a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f` |
| MAP | `a26c441c873cba85ca4c7c8a2ea659798b6d6d4eb87daa8840dc843e813307a9` |
| Build report | `b69cc6fe6813264f61b193d9fe4ebe41e9e34277007bfd5a2384c5f296c4a583` |
| Final qualification | `f0ac982d4176af3fc59fc11e6de0e40e6d434a7fcc7c30c996e9374bf7b6b275` |
| Exact-outline CPU results | `5cd8136f3751e317ff9927e30369e1cc03bc6c234343e6a3bc4f1890a43849ef` |

The build reports 40,313 occupied CODE bytes: 38,492 main and 1,821 low.
The highest main address is `0xc687`, leaving 120 trailing main bytes and
67 low bytes. XRAM is 2,621 bytes; initial SP is `0x5f`, with 160 allocated
stack bytes. Grave Escape, NKRO and all other earlier enabled features remain.
The image uses the original memory windows. The application IHX is not a
complete flashable ROM.

## Code and storage conclusions

The engine delays only eligible ordinary physical inputs. Matching uses the
saved resolved keycode, the 40 ms boundary is exclusive, and unsigned timer
subtraction handles wrap. First-member release drops the output once; the
remaining member stays suppressed. The admission hook still controls duplicate
presses, unmatched releases and blocked held sources after cancellation.
Generated Repeat, macro and dual-role records bypass Combo matching. Output
records pass through the existing ownership, Caps Word and Repeat pipeline.

The eight ten-byte entries occupy `0x0658..0x06a7`. Both markers and record
validation are required before an old gap record can become active. Getters
mask the stored markers on the wire. Each record fits one 64-byte page. Setters
validate before clearing input, retain the verified flush and latched fault
checks, and reload RAM only on success. The base schema remains `0x082002`.

The private XDATA views preserve public generic-pointer signatures. Retained
report callers pass the actual XDATA keyboard report; typed EEPROM callers
pass model-large locals or known globals. Generic EEPROM APIs remain available.
The scalar pressed snapshot retains the old snapshot semantics. Shared layer
mask calculation preserves separate default-layer and held-layer setters.
The parser has exactly the two copied meaningful byte fields.

The USB switch preserves request predicates and colliding standard/HID request
numbers. Descriptor lookup checks interface bounds before dereferencing the
CODE table. Cached SETUP predicates remain packet-local in the non-overlay IRQ
scope. RGB decay saturation is equivalent for byte ages; Direct mode skips only
values which were overwritten before use.

The expanded outliner admits only the stated foreground modules/functions.
USB interrupt/control paths, board IRQ, timer, IAP and delay remain outside the
added scope. The USB ISR and its transitive callees do not reach newly eligible
foreground functions. Helpers contain straight-line original instructions and
one return, with no nested helper or original C call. The maximum relative
stack increase is two bytes, including an interrupt overlapping a foreground
helper. This relative result is not a complete firmware stack bound.

## Evidence and corrections

The dedicated production Combo host fixtures were independently rerun and
passed. Final qualification was inspected: all 28 suites passed, with 258 unit
tests and no skips. Every recorded log SHA256 was independently verified.
IHX and MAP remained unchanged across the run.

The final evidence also records 26 linked Combo cases, 65 linked tapping
cases, 2,674 callee ABI cases and exact equivalence checks for 150 helper bodies
and 1,525 replacement sites with sixteen CPU states per helper. Results bind
the candidate IHX. The identical-record setter checks real Vial dispatch,
cache and reload without claiming changed-flash durability. The largest tested
foreground stack use is 61 bytes; tapping uses 40 and Combo uses 33. These are
observed paths, not exhaustive bounds.

Two fixture failures were resolved without changing firmware. The callee test
now compares returned SP with the actual post-CRT entry SP, retaining all
register, return and memory assertions. The macro cancellation fixture now
finds the unique function-scoped relocated `LCALL _register_code`, checks its
ASM/RST mapping and IHX bytes, and retains the full register-preserving clear
trampoline and output assertions. The obsolete caller-save byte pattern no
longer determines the call site. Initial failed results remain preserved;
corrected targeted and full runs pass.

Russian setter wording was corrected so it cannot be mistaken for the
installer. A preliminary review comment about the technical report's relative
Combo link was incorrect and is withdrawn: `../../docs/COMBOS.md` from
`audits/rc6` correctly resolves to the repository documentation.

Public documents distinguish source, built candidate, published alpha and
installed firmware. They describe the two-key/eight-entry/40 ms contract,
unsupported GUI choices, storage markers, fixed schema and installer boundary.
The pinned backup does not export Combos. A future package needs an explicit
backup extension and migration contract.

Generic C52 cost samples show additional instruction clocks of about 0.2% for
macro execution, 5.1% for matrix/Fn and 5.8% for RGB/Direct/suspend. No physical
scan, USB or interrupt latency claim follows. Host and CPU checks do not prove
electrical IAP behavior, durable changed settings, power-loss or cold-start
retention, GUI acceptance, physical unlock or arbitrary IRQ overlap. These
limits are stated in the reviewed documentation and remain outside approval.

The final lead check must bind the committed source manifest and packaged Git
archive to this unchanged application image and retained evidence. Changes to
firmware, compiler transforms or runtime contracts after this review require
renewed review and affected verification.
