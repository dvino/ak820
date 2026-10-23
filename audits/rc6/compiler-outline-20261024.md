# Exact outlining for the Combos budget

Date: 2026-10-24. Base: `4b83bb9`. This work changes only the offline
compiler pipeline and its tests. It does not change feature flags, six layers,
sixteen macros, shared macro storage, NVM addresses, the compiler or the loader
contract. No USB device was accessed.

## Current v3 proposal

The final source extends the v2 calibration below in two ways. It admits
positive-saving exact bodies as short as four bytes and two instructions,
and it adds an explicit set of foreground CSEG modules. The 200-helper cap,
one-byte minimum saving and forty-instruction maximum remain. Three-byte
bodies cannot pay for the LCALL/RET overhead and remain excluded.

The algorithm identifier is `exact-foreground-register-xdata-code-v3`.
The manifest records the instruction bounds, byte floor, and module/function
allowlist. Eleven focused unit tests pass. The new short-body case finds five
saved bytes from ten identical four-byte bodies; the private-symbol test
continues to require module ownership for every private reference while
allowing identical register-only suffixes to be shared.

The extra whole modules are `protocol/report.asm`, `protocol/host.asm`,
`keyboards/ajazz/ak820/ak820_rgb.asm`, `ak820_nvm.asm` and `eeprom_driver.asm`.
The USB module admits only `ak820_usb_raw_task`, `ak820_usb_raw_send`,
`raw_request_is_nonpersistent` and `ak820_usb_take_keyboard_reset`.
The USB ISR and every control/descriptor/raw-completion helper stay excluded.
Board/timer IRQ code, actual flash/IAP and delay modules stay excluded entirely.
All instruction, symbol, bank, area, label and no-nesting gates still apply.

The short-body-only frozen baseline probe passes all 113 helpers and 1,004
replacement sites with sixteen state cases per helper. It uses 39,791 CODE
bytes, saving 339
more than v2 and 686 against the original control. With the extra foreground
scope, it uses 39,096 bytes, saving 695 more than short bodies alone and 1,381
against the original control. These frozen probes do not include Combos.

The lead's integrated source includes Combos and separately measured C changes.
Its first control uses 41,194 CODE bytes. Short bodies alone reduce that to
40,926 and still overflow. The foreground extension reduces it to 40,452 and
fits. The next integrated control, after other C changes, uses 41,045 bytes.
The actual final v3 module reduces it to **40,313 bytes**: 38,492 main and
1,821 low, with 150 helpers and 1,525 replacement sites. This is a 732-byte
reduction against that same integrated control; it is not a sum of independent
savings. The final IHX SHA256 is
`a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f`.
The independent normal builder reproduces this exact IHX in
`.build/combos-candidate`. Its selected helper groups and every location also
match the frozen probe. Highest CODE is `0xc687`, leaving 120 trailing main
bytes and 67 trailing low bytes. XRAM is 2,621 bytes; stack starts at `0x60`
(initial SP `0x5f`) with 160 bytes of allocation. These final allocations
include the separately integrated Combos and C changes. They are identical to
that integrated control: v3 changes no static RAM allocation. Normalized source
manifests for integrated02 and the final normal build differ only in
`util/ak820_outline_audit.py`; all C, headers and other dependency hashes match.
Thus the 732-byte final reduction is an outliner-only controlled measurement.

More static replacement sites mean more opportunities to execute a helper.
Every executed site adds exactly two instructions, LCALL and RET, compared
with its inline body. The static site count is not an execution frequency;
no scan-latency or device clock-cycle result is inferred from it. A two-
instruction body can therefore execute four instructions after factoring.
Physical input, USB and rendering timing still need separate acceptance.

The stack increment remains at most two bytes on any foreground path: a
helper contains no call, so no foreground C callee can run while that helper's
return address remains live. Only one outlined helper can be active at a time.
Independent source inspection found no new eligible path from the USB ISR;
board and timer callbacks are outside the scope. Thus the IRQ stack delta is
zero, and a preempted foreground helper still adds at most two total bytes.
This relative bound does not establish a previously unknown global firmware
stack maximum. Existing conditional IRQ models and exercised-path peaks must
remain identified as such.

Final integrity/CPU differential checks **pass all 150 helpers and 1,525
replacements**, with sixteen cases per helper. Before the state comparisons,
the runner independently verifies every immediate relocation, linked helper
byte and LCALL site. The tested IHX is byte-identical to the normal builder's
final image; every selected group and location also matches. Results are in
`.build/compiler-integrated02-validation/outline-tests/results.json`, SHA256
`5cd8136f3751e317ff9927e30369e1cc03bc6c234343e6a3bc4f1890a43849ef`.
No callee-save extension is adopted. Independent review remains the acceptance
gate; no hardware or installed-image claim is made.

## Earlier v2 calibration

Expand the existing exact instruction outliner to consider three through forty
instructions, at least one nominal saved byte, and at most 200 helpers. Admit
`MOVC A,@A+DPTR`, whose CODE address depends on architectural registers. Keep
`MOVC A,@A+PC` excluded because moving it changes the address. Keep all existing
exclusions for branches, calls, stack, PSW, direct memory, SFRs, indirect IRAM,
non-Quantum modules and non-CSEG sections. Labels still end a candidate.

A fresh complete candidate saves **347 linked CODE bytes** against the fresh
control. It has 113 helpers and 373 replacement sites, compared with 30 and
187. The candidate has 369 trailing main-window bytes and one trailing low-window
byte. This does not provide a measured 1 KiB Combos allowance.

| Measurement | Control | Proposed candidate |
| --- | ---: | ---: |
| CODE bytes | 40,477 | 40,130 |
| Main-window actual bytes | 38,590 | 38,243 |
| Low-window actual bytes | 1,887 | 1,887 |
| Highest CODE address | `0xc6e9` | `0xc58e` |
| XRAM bytes | 2,512 | 2,512 |
| Linker stack allocation available | 157 | 157 |
| Extra live stack from exact outlining | 2 | 2 |

The stack allocation is capacity, not a measured worst-case stack depth. No
helper calls another helper, calls C, accesses SP, pushes registers or changes
register banks. Its sole extra live stack is its two-byte return address. A
longer block does not add nested stack depth. More replacement sites add call
and return execution overhead; no physical timing or interrupt-latency result
is claimed. Source safety and generic CPU evidence remain distinct from device
acceptance.

## Controlled builds and identity

The pinned SDCC 4.6.0 installation is
`/workspace/scratch/664bab7a0eb4/ak820/toolchains/sdcc-4.6.0`. The QMK executable is
`/workspace/scratch/664bab7a0eb4/ak820/qmk-8051-ak820/.venv/bin/qmk`.
The complete builds, manifests, logs, listings and maps are under
`qmk-8051-ak820/.build/compiler-control-stable` and
`qmk-8051-ak820/.build/compiler-outline-candidate` in the compiler worktree.
Both use the ordinary `0x3027..0xc700` and `0x28a0..0x3000` boundaries.

The IHX hashes are:

- Control: `45f28e80cd9e269cb507d6fff47b43cea2766b00967912599a98b036b638011d`.
- Candidate: `6e0cd41c8c637429b825c6e31262547264f2f3b5bc1eb8241ecc0aa9b1e03517`.

Each full build records 468 source/dependency records. After normalizing the
fresh output directory names, only `util/build_ak820.py` and
`util/ak820_outline_audit.py` differ between these records. Thus all C, headers,
compiler inputs and external dependencies match. The machine report records
both complete source digests and the common digest with these two changed
tools removed. The sweep uses the frozen control's assembled `dce-input` tree;
its cap-only variant reproduces the control IHX byte for byte. The final
candidate full build reproduces the MOVC sweep byte for byte.

The first build started before dependency preparation completed. Its input
manifest rejected the changed LUFA dependency, so it is not a control or a
successful qualification. The later fresh control passes that gate.

## Measured alternatives

All outlined sweep variants preserve actual low-window bytes and XRAM. The
results below are complete relinks, not assembler-size estimates.

| Experiment | CODE | Delta against control | Decision |
| --- | ---: | ---: | --- |
| Cap 100, minimum saving 12, old instruction bounds | 40,477 | 0 | Cap alone is ineffective: only 30 helpers meet the old threshold. |
| Cap 200, minimum saving 1, old instruction bounds | 40,184 | −293 | Positive; part of the proposal. |
| Three/four through 40 instructions, no MOVC | 40,156 | −321 | Positive; the sweep used minimum two, but two instructions cannot reach the eight-byte size floor. The full candidate uses three. |
| Absolute-DPTR MOVC, broader instruction bounds | 40,130 | −347 | Proposed; full rebuild agrees. |
| Proven DSEG/OSEG/BSEG symbol operands | 40,128 | −349 | Not adopted: only two more bytes for a new direct-memory placement contract. |
| Weighted conflict selection, same safe instruction set | 40,115 | −362 | Research only: fifteen more bytes; no new production selection algorithm. |
| Nine extra callee-save names | 40,536 | +59 | Rejected. |
| Only `ak820_macro_change` and `vial_fill_packet` callee-save | 40,451 | −26 | Not adopted without complete stack proof. |

No repeated eligible sequence longer than 28 instructions exists in the frozen
control, even when searching through 60 instructions. Raising the bound beyond
40 cannot save more in this input. The alternative selection score divides a
group's saving by its consumed inline bytes raised to 0.75; exponents 0, 0.25,
0.5, 0.75, 1, 1.25, 1.5 and 2 were compared. The best tested score gains only
fifteen bytes. None proves a globally optimal selection.

The direct-memory probe recognizes only symbols allocated in relocatable
DSEG/OSEG/BSEG, rejects every symbol also defined in another area, and excludes
absolute regions, SFRs and SP. Its additional two bytes are not a reason to
expand the production memory-access contract.

## Callee-save findings

The broad screen adds `timer_elapsed`, `ak820_macro_change`, `mulhi8`,
`vial_fill_packet`, `source_keycode_cache_slot`, `add_sat`, `sub_sat`,
`KEYCODE2CONSUMER` and `dynamic_keymap_key_to_eeprom_address`. All names are
supplied consistently to every translation unit. No C source is changed.
This screen widens only its isolated, nonflashable main end to `0xd700` so a
regression can be measured. It crosses the real `0xc700` boundary and must
never be packed for installation. Its 40,536-byte result is rejected.

The narrowed ordinary-boundary build saves 26 bytes. `ak820_macro_change` saves
r3 through r7 and returns its Boolean in DPL; it is a leaf. Its five calls are
in `action_util` and `action_layer`. Four ordinary callers formerly saved one
register; moving five saves into the callee adds four live stack bytes on
those paths. The remaining caller formerly saved six registers. The helper's
body also grows because its return paths join at the common epilogue.

`vial_fill_packet` is static, returns void and is a leaf. Its three LCALL sites
formerly saved two registers, while its tail-JMP site saved none. The callee
preserves four registers, so the tail path gains four live stack bytes and
ordinary call paths gain two. The public Vial boundary and its return remain
separate. No address-taking or external reference was found in frozen ASM.

The raw per-function deltas explain the complete link: macro-change callers
save 40 bytes and its body adds 22; Vial callers save 24 and its body adds 16.
The other seven names provide no net gain in this screen. The narrowed pair
has no complete whole-program stack/IRQ proof and is deliberately absent from
the production callee-save list. The linker stack-capacity number does not
supply that proof. No CPU or hardware claim is made for these rejected flags.

## Verification and remaining gate

Nine focused outliner unit tests pass, including PC-relative rejection,
absolute-DPTR acceptance, private-symbol ownership, bank aliases, labels,
nonoverlap, the small positive saving threshold, a twenty-instruction exact
helper and rejection of repeated transformation.

The outline-only full image passes the existing emitted-code differential
check for all 113 helpers and 373 replacements. It independently resolves immediate
relocations, compares linked helper bytes and LCALL sites, then compares inline
and outlined effects in uCsim across sixteen states, every register bank and
both carry inputs. Sixteen cases per helper pass. The image and manifest hashes are recorded in
the machine report.
Independent review is still required. Neither a source build nor these CPU
checks approve an image package or establish physical behavior.

Machine measurements: [compiler-outline-20261024.json](compiler-outline-20261024.json).


## Local compiler decisions

The pinned manual recommends local `#pragma noinvariant` when invariant lifting
hurts a function, rather than disabling the pass for the whole program
(`share/sdcc/doc/sdccman.html/node57.html` and `node120.html`). Five independent
whole-program screens used fresh directories and an isolated, nonflashable
`0xe700` main end so regressions could be measured. Low-window checks remained
active. These experiments change optimizer choices, not the compiler or ABI.

| Additional compiler flag | CODE | Actual main bytes | Low bytes | Result |
| --- | ---: | ---: | ---: | --- |
| `--noinvariant` | 39,903 | 38,009 | 1,894 | Main improves, but low exceeds its real end by six bytes; rejected globally. |
| `--noinduction` | 41,471 | 39,753 | 1,718 | Rejected; 1,341 bytes larger than outline-only candidate. |
| `--noloopreverse` | 40,130 | 38,243 | 1,887 | No benefit. |
| `--nogcse` | 43,194 | 41,472 | 1,722 | Rejected; 3,064 bytes larger. |
| `--no-peep-return` | 40,710 | 38,787 | 1,923 | Rejected; grows both windows and overruns the low end. |

The safe selective candidate puts an AK820 + SDCC guarded `#pragma noinvariant`
at the top of `quantum/dynamic_keymap.c`, `quantum/repeat_key.c`,
`quantum/keyboard.c` and `quantum/debounce/sym_defer_g.c`. Other targets retain
ordinary compilation. The low-window macro TU is untouched. No expression,
branch, loop bound or function signature changes.

A fresh full build with real ordinary boundaries uses **39,947 CODE bytes**:
38,060 main and 1,887 low. It saves 183 more bytes than outline-only, or **530
bytes against the original control**, and ends at `0xc4d7`. Its IHX SHA256 is
`9fbeb7f1314a65daf4ac9cc994a7a526fce267de2c5906dd7e038aa4f529bb34`.
There are 113 helpers and 381 replacement sites. The build and CPU evidence
are in `.build/compiler-outline-local-invariant`.

This selective candidate uses one more XRAM byte (2,513), and available stack
allocation falls from 157 to 154 bytes. The ASM explains the difference:
`matrix_task_row_changes` needs one XRAM byte and its old one-byte DSEG sloc
disappears. That DSEG byte occupied the separate `0x1f` hole, so freeing it
does not move the stack start. `dynamic_keymap_macro_send` gains a three-byte
DSEG sloc, moving the unchanged six-byte maximum OSEG and stack start three
bytes upward, from `0x63` to `0x66`. `find_alt_keycode` drops its three-byte
OSEG sloc, but another function still requires six bytes of OSEG. These are
compiler temporary allocations, not schema or persistent-layout changes.

The emitted CPU suite passes matrix/debounce/Fn release, extended macro/layer
and recursion guard, and RGB Direct/suspend/resume cases. The observed stack
peaks are 47, 52 and 25 bytes beyond initial SP; those exercised paths do not
include interrupt overlap. Feature and full outline differential checks of this selective image also
pass: 113 helpers, 381 sites and sixteen states per helper. The host optimization
suite passes exhaustive color/decoder and 196,019 macro traces, plus report and
debounce checks.

Per-function raw reductions from invariant control include macro playback
101 bytes, reset 22, set-buffer 11, alternate-repeat lookup 19, matrix task 15
and debounce six. Complete linked saving is 183 because outlining changes too.
The separate `compiler-noinvariant-main-proposal-20261024.patch` adds the same
guarded pragma to six main TUs: report, USB, board, NVM, RGB and EEPROM driver.
It is unapplied in the compiler worktree and was applied to the lead's later
integrated control. Its contribution is not estimated by adding raw TU
reductions; the integrated control and candidate measurements above are the
authoritative combined figures.

A separate safe straight-line DPTR-value tracking probe found zero redundant
immediate DPTR reloads in eligible Quantum blocks. Its complete relink is
byte-identical to the outline-only candidate. No peephole rule is proposed.


## Execution-cost sample for the final proposal

The same three emitted-code scenarios were run on integrated02 with v2 and
the independently rebuilt final v3 image. Both pass every functional check.
The following sums cover the same simulator run segments in each scenario.

| Scenario | Segments | v2 C52 ticks | v3 C52 ticks | Change |
| --- | ---: | ---: | ---: | ---: |
| Extended macro/action | 5 | 31,924,404 | 31,986,516 | +0.195% |
| Matrix/Fn | 14 | 2,068,272 | 2,172,912 | +5.059% |
| RGB Direct/suspend/resume | 50 | 4,939,428 | 5,223,444 | +5.750% |

These generic C52 instruction-execution samples quantify a cost on exercised
paths. They do not measure VS11K28A clocks, IRQ overlap, physical scan latency,
USB deadlines or worst-case runtime. Long macro delays dominate the macro sum;
its percentage must not be generalized to every key event. Complete logs,
segment counts and SHA256 values are recorded in the machine report.
