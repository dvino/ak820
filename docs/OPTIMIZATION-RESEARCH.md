Русский перевод: [Исследования оптимизации](ru/OPTIMIZATION-RESEARCH.md).

# Optimization research

Primary sources checked online on 2026-10-25. Ideas are separated from measured
firmware savings; the current result remains in [Status](MAXIMUM-FUNCTIONALITY-STATUS.md).

| Direction | Source and applicability | Next action or result |
| --- | --- | --- |
| Address spaces and memory model | [SDCC manual, sections 3.5, 3.15](https://sdcc.sourceforge.net/doc/sdccman.pdf): large-model locals and parameters use XDATA; named address spaces can reduce access cost. Mixing independently compiled memory models is unsupported. | Existing typed XDATA interfaces stay. A small/medium-model migration needs a coherent ABI and allocation design; it is not a safe per-file flag change. |
| Register allocation tuning | The same manual says `--max-allocs-per-node` does not affect MCS51. | Excluded as a size experiment for this target. |
| Return and frame optimization | The same manual documents `--peep-return` and `--fomit-frame-pointer`. Return optimization defaults depend on debug mode; frame omission concerns eligible frames. | Inspect effective emitted code before counting any saving. The current build already requests code-size optimization. |
| Global register knowledge | [Keil REGFILE](https://www.keil.com/support/man/docs/c51/c51_regfile.asp) provides program-wide knowledge of registers used by external functions. | Prototype exact clobber analysis on immutable SDCC assembly. Remove saves only after proving the callee preserves that register on all paths; indirect calls, aliases and register-bank changes must fail closed. This is a proposed pass, not an SDCC option already enabled. |
| Common exits and blocks | [Keil optimizer description](https://www.keil.com/product/brochures/c51_v6.pdf) describes common tails and block packing. | Exact module-local return-tail sharing is implemented experimentally. Current full-image gain is 207 bytes after linking and short-call placement. |
| QMK size guidance | [QMK AVR size guide](https://docs.qmk.fm/squeezing_avr) recommends LTO, narrower layer state and feature removal. | Eight-bit layer state is already present. AVR/GCC LTO cannot be assumed to work in this SDCC port; feature removal does not satisfy this task. |
| 8051-port dead-code tools | [Original QMK8051 port](https://github.com/vuhuycan/qmk-8051) points to assembly-level dead-code removal and notes the XDATA/stack costs. | This build already removes unreachable functions and outlines shared sequences. Published size claims from another keyboard are not estimates for this image. |
| Alternative compiler | [SDCC developer's historical comparison](https://sourceforge.net/p/sdcc/mailman/message/36359114/) found different sizes for SDCC, Keil and Raisonance on one Dhrystone configuration in 2018. [Keil evaluation limits](https://www2.keil.com/limits) cap C51 at 2 KiB. | A compiler comparison remains a possible separate porting experiment. The historical benchmark does not predict this firmware's gain; the evaluation tool cannot link this image. |

Register-preservation and bytecode experiments must include their adapters,
interpreter or helper costs. No percentage from a vendor example is counted as
saved firmware bytes. No device operations or compiler purchase are implied.

## New compiler check

The [MCS51 peephole discussion](https://sourceforge.net/p/sdcc/patches/466/?page=4)
records register-tracking changes after the pinned release. The official
[2026-10-21 snapshot](https://sourceforge.net/projects/sdcc/files/snapshot_builds/amd64-unknown-linux2.5/)
was downloaded separately: SDCC 4.6.4, revision 17055; archive SHA256
`406fd1ed7261e9e026fbd3fe21d9c6cebcc456ebd0ec250f967bb530d3871697`.

Eight actual translation units were compiled with identical board flags under
4.6.0 and the snapshot. Their combined raw CSEG shrank by only 36 bytes: USB 2,
action 7, dynamic keymap 2, VIA 16, NVM 4, tapping 5; Vial and settings unchanged.
This precedes dead-code removal and outlining, so it is not a complete-image gain.
The pinned production toolchain remains unchanged. New register-bank aliases
and runtime helpers would require fresh optimizer, ABI and stack qualification
before a whole-image toolchain migration.

Raising the exact outliner helper cap from 200 to 400 or 1000 was also screened
on the immutable current input. Both select 210 helpers with 3344 nominal saved
bytes, versus 3327 at 200. A fresh complete image with cap 400 saved 34 CODE bytes against the same
register-trimmed source at cap 200 (experiments 12/13). The 17-byte screening
figure is a different object-level metric and is not added to that linked delta.

## Paged-memory screen

The same eight translation units were separately screened under SDCC medium
model. USB and settings compiled, saving 61 and 13 raw CODE bytes while
allocating 35 and 18 PSEG bytes. Six units failed on implicit PDATA objects
passed to explicitly typed XDATA APIs. The NVM shift-width warnings also occur
in the large-model control: they concern the byte-sized cache index and are not
evidence of a new pointer-width defect.
This is evidence against a flag-only conversion, not proof that a coherent
medium-model design cannot work. No mixed-model image was linked or accepted.
The official manual requires the same model for all project files and linking.
A coherent redesign must also qualify the 256-byte PDATA page, hardware page
register, all parameter consumers and the existing assembly ABIs.

A bounded coherent medium-model copy was then made to compile all eight units
with explicit XDATA annotations for escaped objects and aggregate parameters.
Raw CSEG fell by 1080 bytes; including 36 extra GSINIT bytes gives 1044. Mapping
current retained function names gives an estimated 819 CSEG-byte reduction,
not a linked-image result. Raw PSEG is 404/256; the current-retention estimate
is 377 bytes, still 121 over the page before other files. PSEG is non-overlay.
The board writes P2=0xff and its custom CRT deliberately avoids unverified
short-MOVX paging. Hardware paging and deliberate page placement therefore
remain prerequisites. The experiment is retained externally as
`ak820-medium-feasibility`; the production large-model ABI remains unchanged.

## Optimizer-switch screen

Twelve current production units were compiled separately with the same maximal
flags under pinned SDCC 4.6.0. Controls were compared with `--nogcse`,
`--noinduction`, `--noloopreverse` and all three together. No variant reduced
raw CODE/CONST/XINIT totals in any unit. Loop reversal made no size difference;
disabling common-subexpression or induction optimization usually added code.
For example USB CSEG grew by 766 or 278 bytes respectively. The existing
per-file `noinvariant` pragmas were retained in this screen. No switch was
adopted, and no linked-image saving is claimed. Commands, source/object hashes
and all 60 object results are retained externally in `ak820-optimizer-screen`.
This screen follows the optimizer option semantics in the
[official SDCC manual](https://sdcc.sourceforge.net/doc/sdccman.pdf).

## Allocator and return-peephole screen on image 20

Twelve retained translation units were selected from image 20 by original ASM
size. All baseline compilations reproduced their original ASM hashes from the
same frozen preprocessed inputs. With pinned SDCC 4.6.0,
`--max-allocs-per-node 10000`, `--max-allocs-per-node 100000` and explicit
`--peep-return` produced identical noncomment ASM in all 36 runs. Assembled
CSEG, DSEG, XSEG and PSEG sizes did not change. No option was adopted and no
linked saving is claimed. Exact inputs, tool hashes, timings and section sizes
are retained externally in `ak820-allocator-sweep20/REPORT.md` and
`ak820-allocator-sweep20/results/results.json`. The screen does not establish
results for the unmeasured units.

## Compiler metadata capture

The spill proof reads SDCC's syntax tree (AST) from stdout. Diagnostics from
stderr are retained in a separate file. Both logs are included in the capture
hashes. Merging the streams can insert a warning inside an AST function header
and cause a missing-function rejection. Source, type, compiler ASM and postlink
checks remain mandatory. A changed capture tool requires fresh builds and
exact-image qualification.
