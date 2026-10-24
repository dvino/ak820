# Source size probes, 2026-10-24

The stable source changes save 279 occupied CODE bytes against `129c1c8`.
They retain six layers, sixteen macros, eight Combos and the existing report,
RGB and storage behavior. No keyboard was accessed. The complete builds use
pinned SDCC 4.6.0 and the normal outliner and callee-save configuration.

| Complete build under QMK `.build` | CODE | Main | Low | XRAM | Stack capacity |
| --- | ---: | ---: | ---: | ---: | ---: |
| `size-control2` | 40313 | 38492 | 1821 | 2621 | 160 |
| `size-bitflags` | 40195 | 38391 | 1804 | 2614 | 159 |
| `size-pagebyte` — stable | 40034 | 38230 | 1804 | 2612 | 160 |
| `size-protocol-bits` — optional | 40010 | 38206 | 1804 | 2610 | 159 |

[Measurements](size-source/measurements.json) bind each build to its IHX hash.
Stable main code ends at `0xc581`, leaving 382 trailing main bytes. Low code
uses 1804 bytes, leaving 84 bytes. Reserved HOME bytes remain excluded.
The application IHX is not a complete image approved for installation.

## Source changes and bounds

Seven private NVM, macro-upload and RGB boolean objects use SDCC bit storage;
host builds retain `bool`. No object's address is taken. Every assignment
already produces a boolean. Public parameters, return types and data formats
remain unchanged. The compiler emits bit instructions instead of XDATA loads
and stores. These modules do not add an interrupt caller or new helper call.

The private cached-page value, cache loader argument and erase counter use
one byte. Every cache caller checks the complete EEPROM request before page
selection. Valid pages are 0 through 159. A compile-time assertion requires
fewer than 256 pages, so the erase counter can reach the loop's terminating
value without wrapping. Journal page decoding remains 16-bit and is checked
before replay. Diagnostic and stored-header high bytes remain zero for valid
cache pages. The assertion was tightened from `<=256` in the measured stable
build to `<256` in source; the actual 160-page configuration is unchanged.

Two further private flags, Vial unlock-holding and macro playback's recursion
guard, save another 24 main bytes. This probe reduces stack capacity by one
byte through bit/overlay allocation and is not retained. The selected source
keeps the stable 279-byte saving and 160-byte stack allocation.

## Verification and rejected probes

The production VIA/NVM host suite passes. The NVM model passes 10944 power-cut
cases; added checks visit all 160 cache indices, erase through page 159 while
preserving protected regions, and reject journal page 160, 256 and 65535 before
writes. The macro model passes 25088 power cuts and grammar, retry, restart,
bounds and full-capacity checks. The production macro playback guard passes.
RGB host checks pass all 16777216 HSV cases and effects, Direct, suspend, timing
and wrap. LeakSanitizer could not enumerate `/proc`; rerunning with leak checks
disabled passes with address and undefined-behavior checks enabled.

The optional probe candidate passes all 2674 linked callee ABI cases, linked RGB,
breathing, diagnostics and layout checks. The adapted callee fixture also
passes the original control. Linked RGB observes 23 stack bytes; this is a
path measurement, not a whole-program or interrupt-overlap bound. Reports are
in [size-source](size-source/). Hardware timing and durable physical storage
remain untested.

The initial callee check assumed every private object occupied XRAM and wrote
two bytes to the cached-page object. It therefore failed after the valid
representation changes. The retained fixture now reads BSEG placement and
scalar allocation widths from relocated listings, uses simulator bit memory
for bit objects and writes cache scalars at their actual width. Assertions for
registers, SP, return values and memory effects remain. The initial failure is
retained alongside the successful control and candidate results.

Shared key/encoder EEPROM pair helpers saved only 8 bytes and added a call;
they were rejected. Scalar RGB and color copies together added 18 bytes.
Color-only scalar copies saved 4 bytes but were rejected to avoid needless
source churn. Neither change remains. The first baseline attempt failed from
an incorrectly copied LUFA dependency; `size-control2` used a local copy and
reproduced the existing exact control hash.
