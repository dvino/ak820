# Disclaimer and OEM trace review

Date: 2026-10-24. Independent review of the English and Russian README
disclaimers, the matching STATUS corrections and the OEM USB indicator trace.
The reviewed text was authored separately from this review.

## Documentation checks

The disclaimers cover source code, firmware and tools, use without warranties,
user risk, backups, compatibility, device damage and data loss. Both versions
place the notice before getting started and link to the existing GPLv3 LICENSE.
The liability qualification agrees with sections 15–17. The translations have
the same practical meaning. This checks the wording against the repository
license; it does not establish legal enforceability.

The STATUS corrections agree with the retained evidence: the corrected
26-suite qualification reports `passed: true`, 258 unit tests, zero skips and
unchanged build hashes. The earlier pointer-only IHX is labelled historical.
The actual SHA256 of `releases/rc6/installer-release.json` is
`234d7d7d267bc2b5dd61faa63d00543366b0db2208407631053c8b73f91055db`.
`python3 tools/check_docs.py` passed: 35 public documents, zero failures.

## OEM trace finding

Independent static decoding confirmed the recorded ROM and s51 hashes, reset
target and all ten listed vector targets. All ten selected wrappers save
registers, call `0x0DC4` and return with `RETI`. The first two wrappers write
the recorded three bytes to the recorded XRAM addresses.

The initial report incorrectly described `0x0DC4` as copying descriptor bytes
to `0x0175` and jumping through a table at `0x0DCA`. The instructions at
`0x0DC4` load DPTR from R2:R1, clear A and jump indirectly. The first two
wrappers therefore transfer control to `0x3006` and `0x3009`. The following
routine at `0x0DCA` stores R6, R7, R4, R5 and R3 to five XRAM bytes; it is not
the claimed three-byte descriptor copy.

Closure: the corrected report now describes the exact four instructions,
the register-derived `0x3006` and `0x3009` targets, and the separate five-byte
store at `0x0DCA`. It explicitly rejects the initial table interpretation.
The correction agrees with the independent decode. No finding remains open.

The trace correctly leaves HID `SET_REPORT`, host Caps state, Win-lock state,
GPIO/DMA assignment, electrical mapping and visible behavior unproved.
Earlier output-routine claims were checked for agreement with the cited prior
report, without redoing that earlier analysis.

## Scope

Only documentation and offline static bytes were checked. No new build, CPU
execution, USB access, settings write, reset, bootloader transition or flash
was performed. ROM bytes and disassembly remain outside Git in the external
private backup. The README, STATUS and corrected OEM trace pass this bounded
review. The final documentation check again passed with 35 public documents
and zero failures; `git diff --check` also passed.
