# Beta.3 source and offline evidence

The source adds Caps Word (`0x7c73`) as a two-key Combo output and physical
macro Layer-Tap: codes `0x40F0`–`0x45FF` with low bytes `F0`–`FF` select layers
0–5 and persistent macros 0–15. Main adds Auto Shift. Its unchanged CRC leaf
is placed in the existing low CODE window. Main does not include GUI lock.

All ten local images passed exact startup, foreground and enabled-interrupt
checks before full regression. Each passed 28 base suites and 336 unit tests
without skips; supplemental suites total 337 across ten images (32–37 each).
Repeated suites are executions of the same tests, not distinct tests.
`local-build-inventory.json` records image hashes and retained report hashes.
`build-locations.json` locates the immutable original build roots.

Main uses 40,398 CODE bytes; IHX SHA256
`b6040e965dfa30a22049bec5591ff7ab074a89000d973f22f9f3b08736a33031`.
Its whole-program stack bound is 160/167 bytes and startup uses 2 bytes.
These figures apply only to that image.

Offline packing passed for all ten images. `transition-preflight.json` records
230 default-setting plans across 23 exact source images, 100 nondefault Caps
Word Combo plans and 100 macro Layer-Tap plans with exact macro bytes.
The frozen settings suite passed 180 tests. Prior beta.2 typed rows are kept
in `historical_profiles` as source-only contracts; new installation targets
declare `combo_actions` and `macro_layer_tap` explicitly.

The legacy f1c4347e source fixture comes from the validated saved postflash ROM.
The downloaded alpha.2 bundle has another IHX and cannot substitute for it.
Private ROMs, packed OEM-containing binaries and raw device captures stay
outside tracked evidence.

`measure_origin.py` invokes unchanged canonical measurement tools inside each
original source root. It compares build sources, runtime/test sources and the
entire copied build tree before and after measurement. Preserve those roots:
absolute generator and context paths prevent inspection of copied images as
if they had been built in the central root. No proof paths or gates are rewritten.

`prepare_release.py` generates catalogs, packing records, transition fixtures
and policy drafts. It does not generate independent approval. Program-policy
admission requires review of the final generated inputs before commit.
`beta3-final-source-admission-review.md` covers the source candidate only.

The next firmware work is current Direct-palette readback, atomic whole-frame
application and an attempt to fit the W pulse. It is listed in the Roadmap;
the detailed handoff is local and excluded from Git. None of these future
functions is claimed by this image.

Publication is on hold; the reviewed source may be pushed without a release.
Beta.2 remains unchanged. No keyboard writes, reset, loader transition or flash
were performed. Offline models and packing do not prove physical behavior.
