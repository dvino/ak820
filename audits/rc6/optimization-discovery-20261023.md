# RC6 optimization search

Date: 2026-10-23. This is an offline discovery pass, an isolated compiler probe
and a controlled full link. It did not access USB, modify production source or
commit changes. It follows the owner's supplied plain-language rules;
no retrieved writing sample was used.

## Baseline and source check

The baseline is `qmk-8051-ak820/.build/rc6-candidate-erase-20261023/`.
Its IHX SHA256 was checked directly:
`d2d48dcd67f5fa6b5d49388c5737860fae44aa213be745ef6aa2ab5a39774dce`.
The saved build report records SDCC 4.4.0 #14620, CODE 39,347 bytes,
XRAM 2,071 bytes and stack capacity 152 bytes. Stack capacity is available
space, not a measured worst-case stack depth.

| Placement range, end excluded | Used | Capacity | Free |
| --- | ---: | ---: | ---: |
| Main `0x3027..0xC700` | 37,488 | 38,617 | 1,129 |
| Low `0x28A0..0x3000` | 1,859 | 1,888 | 29 |
| Both | 39,347 | 40,505 | 1,158 |

At the start of this pass, all 443 manifest files accessible relative to the source tree matched their
recorded SHA256. The other 22 entries have `toolchain` origin and do not live
under the source tree; this pass did not independently rehash all of them.
The compiler used for the isolated probe does match the baseline compiler
SHA256 `9b8d26bc440dea99004cd56a37f88eb5964ceb092a7e4b65fc7f16a3f732570b`.
These checks support correspondence to the saved baseline. They do not turn a
later source change into a built or installed result.

## Fresh linked ranking

The companion JSON contains every counted function, direct call/jump site,
generic-pointer site and repeated return suffix. It counts encoded instruction
bytes in final relocated `dce/**/*.rst`, grouped by underscore function labels.
It excludes data directives and library bodies without RST files. It is a size
ranking, not an execution profile. Indirect callbacks and address-taken roots
must also be read from `dce/reachability.json` and the source.

| Function | Linked start | Instruction bytes |
| --- | --- | ---: |
| `control_setup` | `0x5728` | 2,065 |
| `raw_hid_receive` | `0xA619` | 1,583 |
| `dynamic_keymap_macro_send` | `0x84D5` | 902 |
| `ak820_macro_write` | `0x2B06` | 899 |
| `process_action` | `0x6F53` | 863 |
| `vial_handle_cmd` | `0xAEA6` | 857 |
| `rgb_matrix_task` | `0x4AD2` | 792 |
| `matrix_task` | `0x8E03` | 598 |
| `ak820_usb_raw_task` | `0x6540` | 506 |
| `dynamic_keymap_set_buffer` | `0x81D4` | 466 |

The older inventory used IHX `12260272...`, not this candidate. Most top
functions retain its byte counts, but `vial_handle_cmd` is now 857 rather than
833. The fresh inventory counts 1,319 direct call/jump sites and 57 calls to
generic-pointer helpers. The 1,319 count is not an ACALL/AJMP eligibility count.
No fresh relocation-aware short-transfer opportunity total was computed here.

The DCE report records 574 functions, 398 retained and 176 removed across 64
modules. It retains startup, USB, timer and LED roots. No retained hook was
classified as removable merely because its ordinary direct-call count is zero.

## Candidates and bounded probes

| Candidate and exact evidence | Expected effect | Next probe and acceptance condition |
| --- | --- | --- |
| Private typed host driver: `tmk_core/protocol/host.c:43`; active constructor in `protocol/ch555/ch555_ak820.c:74,94`. The linked driver object is XDATA `0x0BA3`. Host keyboard/LED/system/consumer functions contain 11 of the 57 generic-helper sites. | CODE and one private XRAM byte; no intended NVM or wire change. | First choice. Preserve generic public set/get and report-pointer ABI, qualify only private driver pointee under AK820. The isolated result below justifies a complete controlled relink and callback/null-state regressions. |
| Local journal header pointer: `keyboards/ajazz/ak820/ak820_nvm.c:58,67`; `journal_header_valid` has three generic-helper calls and its sole caller supplies a local nine-byte header. | Possible CODE reduction, no intended storage-format change. | Prove header placement and helper ABI from emitted code, then change only the private helper. Exercise every header byte/complement mismatch, committed/incomplete journal and failed replay. Stop on any altered fault/recovery behavior. |
| Grave Escape event accesses: `quantum/process_keycode/process_grave_esc.c`; five generic-helper sites. | Possible CODE decrease; may add wrapper CODE or stack. | Trace all record origins, including repeat-generated events, before a private typed view. Preserve press/release ownership, weak modifiers and overlapping physical/repeat cases. Do not cast arbitrary public callers without provenance. |
| Shared protocol result handling: `quantum/via.c:264..525`; 1,583 instruction bytes in `raw_hid_receive`, versus 857 in `vial_handle_cmd`. | Possible CODE reduction; timing/stack can move. | Compare one repeated packet-field or failure tail, with existing response/ACK rules written down first. Preserve length bounds, unlock gates, no-ACK failures and send-before-boot ordering. Do not extract the already shared final `raw_hid_send` again. |
| USB setup/descriptor dispatch: `protocol/ch555/usb_ak820.c:139,188`; 2,065 + 452 instruction bytes. | Possible CODE and dispatch-cycle reduction; high protocol sensitivity. | Separate one descriptor-selection alternative from setup-state handling. Exhaustively compare request fields, interface bounds, stalls and transfer lengths; keep USB ISR/EP0 ownership unchanged. Existing private-copy work must not be credited again. |
| Cross-module callback and usage tails: `host_system_send` and `host_consumer_send` have two generic-helper sites each and parallel report construction. | Possible CODE reduction after typed driver; helper overhead may erase it. | Only after the typed-driver link result, try one shared extra-report tail. Keep distinct last-usage state, suppression order and callback signatures. Measure the combined image, not additive TU estimates. |

No expected byte saving is assigned to an unbuilt candidate. Macro decoding,
`process_action`, RGB processing and matrix scanning remain inspection targets
because of their emitted size; this pass found no new bounded algorithm change
there with enough proof to recommend ahead of the candidates above. A runtime
profile is still missing, so size does not establish interrupt/USB timing value.

## Common-tail search and prior results

The baseline already outlines 32 helpers across 221 sites. Its report gives
1,234 nominal bytes removed and two extra stack bytes; this is an existing
baseline transformation, not a saving made by this search.

The root's fresh existing-tool audit is
`host/runs/20261023-optimization-outlining-inventory.json`: 1,519 safe blocks,
267 exact groups and 2,254 normalized families, with zero selected groups at
the default minimum saving of 12. Existing outlined helpers cannot be nested.
Changing normalization or the threshold therefore requires a new proof and
controlled link, rather than applying the current pass again.

The companion suffix inventory independently finds repeated return sequences.
For example, `movx a,@dptr; mov dpl,a; ret` appears in 21 functions, and
`pop ar6; pop ar7; ret` in nine. These tiny suffixes are poor first probes:
a long tail jump already costs three bytes, while call-based factoring adds a
return address and changes stack requirements. Identical local-label spellings
in longer suffixes do not prove identical branch targets. These are rejected
as automatic rewrites, not counted as saved bytes.

Keep the existing negative results from `docs/ROADMAP.md` and
`docs/SPACE-OPTIONS.md`: four layers save zero CODE/XRAM; compact CIE's measured
216 bytes are already included; Direct HSV packing targets RAM and adds CODE;
flag-only One Shot is incomplete and exceeds its old limit; SDCC 4.5 did not
produce a valid image; macro capacity does not free CODE without a new layout.
The historical 531 short-transfer candidates need a new post-placement proof.
The 11 audited callee-save names and prior arithmetic/decoder improvements are
already build inputs, not new proposals. No broad peephole rule is recommended.

## Isolated host-driver compiler result

Private files: `qmk-8051-ak820/.build/rc6-host-driver-probe-20261023/`.
`probe.py` copies only `host.c`, reads the saved `cflags.txt`, and runs the pinned
compiler for a control and candidate. It does not invoke the firmware builder.
The candidate changes the private driver to `host_driver_t __xdata *` under
`AK820_BOARD` and explicitly casts the generic setter argument. Other targets
keep the original declaration and assignment. Public signatures and report
pointers stay unchanged.

| Translation-unit result, before DCE/outlining/link | Control | Candidate |
| --- | ---: | ---: |
| Raw CSEG | 725 | 663 |
| Generic-helper calls, including dead functions | 13 | 3 |
| Private driver allocation | 3 | 2 |

Both compiles succeeded. After removing comments, control ASM exactly matches
the saved pre-DCE `protocol/host.asm`; the saved control REL also has CSEG
`0x2D5`. The raw TU difference is **62 CODE bytes and one XRAM byte**. It is
not a complete linked saving: DCE, outlining, placement and retained functions
can change it. The candidate getter rebuilds the generic XDATA pointer tag
as `B=0`; callbacks still use `__sdcc_call_dptr`, and source null checks remain.
This is emitted-code inspection, not callback execution or full ABI validation.

## Controlled full link

`link_probe.py` copies the 64 original raw ASM modules from the frozen baseline,
runs the existing DCE with all four saved external roots, assembles, runs the
existing outliner with maximum 40 helpers and minimum saving 12, assembles again
and links with the original windows, flags and object order. The control must
reproduce the exact baseline IHX file before the candidate runs. The candidate
changes only the copied raw host ASM; later production edits are excluded.

The control reproduced the exact IHX file bytes and all resource figures.
The candidate IHX SHA256 is
`319824985e75b636c0f4dc433d7fa4602f2d86f24ea76166b3c1c273ae057871`.

| Complete linked result | Control | Candidate | Difference |
| --- | ---: | ---: | ---: |
| CODE | 39,347 | 39,298 | -49 |
| Main CODE | 37,488 | 37,439 | -49 |
| Low CODE | 1,859 | 1,859 | 0 |
| XRAM | 2,071 | 2,070 | -1 |
| Stack capacity | 152 | 152 | 0 |

Both links retain 398 of 574 functions and remove 176. Both select 32 outlined
helpers, 221 sites and 1,234 nominal bytes. All linked bytes remain in the two
allowed windows. Candidate headroom is 1,178 main bytes and 29 low bytes,
1,207 total. This is a measured offline linked saving. It is not installed
firmware, peripheral timing evidence or a complete pointer/ABI execution proof.
The existing emitted ABI suite passed all three cases, and the feature suite
passed all 33 cases against the host-only linked candidate. A focused linked
host fixture passed 18 observations: null-driver suppression and LED return,
usage state before the null guard, restoring a driver, callback return values,
generic report pointer DPTR/B and payload, duplicate-usage suppression, release
and restoring the original driver. Its exercised stack use is eight bytes.
`host_get_driver` is removed by DCE, so its generic return has TU emitted-code
evidence only, not execution evidence from this linked image.

The first focused fixture used incorrect expected report IDs. The actual
`report.h` enum gives system 3 and consumer 4. The initial failing expectations
remain in `cpu-host/results.json`; the corrected new run is
`cpu-host-corrected/results.json`. A separate mistyped input path stopped one
invocation before simulator execution. No firmware recovery or blind retry was
used. The test fixture, rather than firmware, was corrected from source evidence.
No production integration or hardware update follows automatically from it.
The companion JSON embeds compiler/link commands, hashes and source provenance;
the private build folder also retains logs, ASM, REL, MAP, MEM and IHX.

## Combined research image

At the root lead's request, `combined_probe.py` added the root's current
Breathing change to the host-driver experiment. It snapshots `ak820_rgb.c`,
compiles it with the saved baseline flags, and substitutes only that raw ASM
and the host candidate ASM before the same frozen DCE/outline/link pipeline.
Its source-manifest check found only `ak820_rgb.c` changed from baseline among
the 443 accessible inputs. RGB snapshot SHA256:
`2d9a4e6541c9b49a76c3f2f1785401c06126c69d47c045421a58abb904fe3aee`.
All other raw modules remain the saved baseline. This is a controlled research
reconstruction, not a run of the complete production source builder or packer.

Combined IHX SHA256:
`ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837`.
CODE is 39,432 bytes: 37,573 main and 1,859 low. XRAM is 2,071 bytes;
stack capacity is 152 bytes. Main headroom is 1,044 bytes and low headroom
29 bytes, 1,073 total. Compared with the original baseline this costs 85 CODE
bytes and zero XRAM bytes. Compared with host-only it costs 134 CODE bytes
and one XRAM byte. The combined image retains 399 of 575 functions and removes
176; outlining remains 32 helpers, 221 sites and 1,234 nominal bytes.

The three existing emitted ABI cases and the 18 focused host observations pass
against the combined image. Its focused host peak remains eight tested stack
bytes. RGB visual smoothness, peripheral timing and physical behavior were not
tested by this pass. Alt Repeat, persistence, cold start, restart, power-loss
and recovery device checks remain deferred; offline feature regressions above
are a separate evidence level.
