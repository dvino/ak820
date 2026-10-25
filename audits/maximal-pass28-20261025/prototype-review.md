# Keymap firewall independent review

Decision: PASS for source/prototype integration and subsequent diagnostic builds. No blocking functional finding was identified. This is not linked-image, stack/IRQ, CPU or hardware acceptance.

Reviewed clean repository HEAD eb3c23045a4fdd18ca2001c7a7f085eb7ca3939e and the frozen external keymap-firewall prototype. AGENTS.md and MAXIMUM-FUNCTIONALITY-PLAN.md were read. No repository edits, full builds, commits or device actions occurred. Review outputs and executables were written outside the repository.

## Source and ABI

The complete baseline.inc equals the current complete dynamic_keymap_set_buffer function byte-for-byte. All three recorded source hashes and both API header hashes match current files. The prototype commit field names its earlier extraction baseline cfd05a0; it is historical provenance, not the reviewed current HEAD. The actual function/header identities remain unchanged across those commits.

The patch changes only the locked AK820 branch. Non-AK820 code is preserved under the added else. VIAL_ENABLE, VIAL_INSECURE and unlocked gates retain their behavior. Public offset and size remain uint16_t and data remains generic. The real byte-reader declaration is generic; the real writer accepts an XDATA buffer, generic EEPROM destination and size_t length. Component declarations match those interfaces. EEPROM addresses are numeric offsets: the target reader ignores the generic tag and tail-dispatches to read_offset. The sole writer and its original-buffer pointer, destination expression and full size argument remain unchanged. No writer or backend implementation changes are included.

Zero and size >28 return before count narrowing or buffer dereference. With Vial enabled, bounds checks establish offset <1536 and size <=1536-offset before either read. Thus accepted address arithmetic is bounded, count fits uint8_t, and offset+size cannot overflow a target 16-bit int. Invalid 16-bit offsets and oversized requests cannot reach the firewall or writer. The existing no-Vial bounds behavior is unchanged.

Let a=offset&1 and b=(offset+size)&1. The candidate starts its interior cursor at buffer+a and processes size-a-b bytes. This is nonnegative and even for all positive sizes, including size=1 at either parity. It is exactly the original loop range [a,size-b), so remaining cannot underflow and both bytes of each iteration are present. Boundary and interior replacements agree for QK_BOOT=0x7c00. Both boundary reads occur unconditionally when their boundary exists, prior boundary first, following boundary second, before interior filtering. Neither read is eliminated by a packet-byte short circuit. The first mutation precedes the second read exactly as before; there is no shared first/last byte when both boundaries exist. Reader-return-dependent mutations and writer invocation therefore agree for arbitrary returned byte values and persistent reader side effects that do not asynchronously mutate the input packet.

## Independent host checks and limits

The frozen harness was rebuilt and executed in ak820-nkro-study-env:local with networking disabled, prototype mounted read-only and only /tmp writable. ASan/UBSan: PASS 6,849,504 differential cases. The independently calculated count is 3*1536*30*2*6*3 + 65536*12*2 + 300000. All three separately recompiled mutants failed at their reported first mismatches: skipped read (1,1), reversed reads (1,2), missing interior filtering (0,2).

The main sweep exhausts accepted offsets, lengths 0..29, lock states, packet patterns and two read-fault positions over three EEPROM patterns. Additional sweeps cover every uint16_t offset with representative extreme lengths and random requests. Pattern coverage is not exhaustive enumeration of every packet or EEPROM byte. The fault stub returns 0xff and records a sticky flag; it does not emulate backend journal, flash faults or durable writes. Buffer canaries, read count/order/addresses, fault state and writer identity/count/arguments are compared. The writer stub does not perform storage.

Host unsigned arithmetic and int width differ from SDCC. Native tests cannot validate address-space tags, 16-bit promotions, static parameter storage or instruction clobbers. Integer-derived EEPROM pointers and their arithmetic are a target address convention; sanitizer success does not make them a portable ISO C model. Existing baseline high-byte shifts depend on target integer semantics; the candidate byte comparisons avoid that dependency. For accepted Vial requests, the new count arithmetic and pointer increments are bounded as proved above. Target listings and exact-image checks remain necessary.

The retained relocatable areas independently show CSEG 0x1c6 ->0x17a (454 ->378, -76), DSEG 5 ->5, XSEG 10 ->10 and CONST 0. This confirms component accounting only; component compilation was not repeated. The retained candidate assembly has both EEPROM reader calls and the unchanged writer parameter slots. No whole-image saving is inferred.

## Private-formal context admission

validate_context was independently run against both actual pass27 classifier bootstrap object trees and DCE trees, current pinned toolchain and current map sources. Maximal passed all 84 provenance paths and three complete protected modules; WORK passed all 79 provenance paths and three complete protected modules. Protection includes whole board, timer and USB compiler ASM. Both remain application_irq_only, without whole-image or hardware qualification.

These checks admit those unchanged research contexts only. A new pass28 build must validate its own actual protected compiler ASM/modules against the selected profile certificate, together with tools, map and provenance. Changed protected ASM requires a fresh certificate. A component object does not establish that identity for a future whole build. Fresh exact-image placement, parameter/clobber, startup, foreground, all enabled IRQ/wrapper/nesting and stack-capacity checks are required before that image's full regressions. Existing pass27 bounds cannot accept the changed target.
