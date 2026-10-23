# Remaining local optimization probes

Date: 2026-10-23. This is static analysis of the combined local build. No
firmware source, compiler output, USB state or installed firmware was changed.
The report follows the owner's supplied plain-language instructions; no
retrieved writing sample was used.

The reference is `.build/rc6-optimization-batch-20261023` inside QMK. Its IHX
SHA256 is `4b68ae92d95538e4c0af1d445c723645b1d7f570b3ea206002d7521b45fe7ce3`.
Its recorded CODE is 39,144 bytes, XRAM 2,067 bytes and stack capacity 152 bytes.
The typed host driver, shared report tail, Breathing arithmetic and RGB action
table are already included. Their earlier savings are not new opportunities.
Six layers, sixteen macros and supported behavior remain acceptance conditions.

## What was counted

The companion JSON records the hashes of all 64 final relocated `dce/**/*.rst`
files, the instruction ranking, direct transfer sites, generic-pointer sites
and compiler helper sites. The script is
`qmk-8051-ak820/.build/rc6-deep-local-20261023/inventory.py`.
Run it with `rtk proxy python` from the repository root. It does not build.

Only encoded instruction rows with cycle brackets count. Every counted byte
was compared with its linked IHX address: zero mismatches. Data directives do
not count. There are 36,359 instruction bytes in 436 nonempty underscore-label
groups, including startup and generated outline helpers. These are not 436
independent C functions. The total is not the CODE size: tables, padding and
library bodies without RST files are outside this count.

There are 1,302 direct LCALL/ACALL/LJMP/AJMP sites, including local labels.
There are 49 generic-pointer helper sites: 34 `__gptrget`, 13 `__gptrput` and
two `___gptr_cmp`. The older discovery's 57 sites referred to the earlier IHX.
The inventory finds 45 `___memcpy`, seven `__mulint` and five
`__sdcc_call_dptr` sites. The JSON also lists two startup helper transfers.
Counts are emitted sites, not execution frequencies. Indirect callbacks,
address-taken roots and library-internal edges need separate analysis. This is
neither a complete call graph nor a runtime profile. No short-call saving is
claimed from the direct-edge count.

| Function | Address | Instruction bytes |
| --- | --- | ---: |
| control_setup | 0x5784 | 2,065 |
| raw_hid_receive | 0xA53A | 1,583 |
| dynamic_keymap_macro_send | 0x84E2 | 902 |
| ak820_macro_write | 0x2B06 | 899 |
| process_action | 0x6F60 | 863 |
| vial_handle_cmd | 0xADC7 | 857 |
| rgb_matrix_task | 0x4B0F | 823 |
| matrix_task | 0x8E10 | 598 |
| ak820_usb_raw_task | 0x659C | 506 |
| dynamic_keymap_set_buffer | 0x81E1 | 466 |

## Probes in order

No probe below has been compiled in this pass. None has a claimed byte saving.
Each should change one bounded expression or private interface, followed by a
controlled full link. Accept only a measured net improvement in the relevant
CODE window with unchanged tests, formats and error behavior.

1. **Private journal header pointer.** In
   `keyboards/ajazz/ak820/ak820_nvm.c:58`, `journal_header_valid` still accepts a
   generic pointer. Its sole call at line 74 supplies `recover_journal`'s local
   nine-byte header. Final `ak820_nvm.rst:669..671` loads that header's XDATA
   address `0x0529` and a zero memory-space tag. The callee saves three pointer
   bytes (`:546..557`) and calls `__gptrget` at `:571,593,613`. Probe a private
   XDATA pointee qualifier only. Check all header bytes, complement mismatches,
   incomplete prepare/cleanup, invalid page, bad CRC, failed replay and valid
   replay with existing NVM host/CPU fault models. Stop if journal bytes,
   ordering, fault propagation or any recovery result changes. Host/CPU tests
   cannot establish flash durability.

2. **Macro delay multiply.** In `quantum/dynamic_keymap.c:673`, the delay uses
   `(uint16_t)(d0 - 1) + (uint16_t)(d1 - 1) * 255u`. Final
   `quantum/dynamic_keymap.rst:2816..2834` prepares `__mulint_PARM_2`, pushes five
   registers and calls `__mulint` at `0x87E7`. Probe a bounded unsigned
   shift/subtract expression with explicitly preserved width. Compare every
   legal nonzero byte pair (65,025 inputs), then complete macro traces for all
   16 macro IDs, zero/maximum delay, truncation, busy state, nested playback
   rejection and exit release. Stop on changed delay, signed overflow,
   wraparound or parser acceptance. Other modules still call `__mulint`, so
   eliminating this call does not imply removing the linked helper body.

3. **Grave Escape event access.** `quantum/process_keycode/process_grave_esc.c:30`
   has a generic public `keyrecord_t *`. Its final RST contains get sites
   `:657,682,685` and put sites `:693,696`. Physical records originate in
   `quantum/action.c:102`; repeat also creates/copies records in
   `quantum/repeat_key.c:21,32,49,96`, and quantum dispatch calls GESC at
   `quantum/quantum.c:437`. A private typed view is only a candidate after every
   retained caller and record placement is proved, including repeat and Vial
   synthetic events. Preserve the public ABI. Compare press/release traces,
   all modifier/override combinations, weak modifiers, physical/repeat overlap,
   cached resolved keycodes and layer changes. Stop on an unproved pointer
   origin, added unsafe cast, altered ownership or stuck key.

4. **One protocol packet-field or response tail.** `quantum/via.c:264..525`
   remains the 1,583-byte receiver; `quantum/vial.c` dispatch remains 857 bytes.
   Final `quantum/via.rst:1000` and `quantum/vial.rst:1110` identify the entry
   groups. Compare one repeated two-byte field decode or failure branch at a
   time. First record existing request/response traces. Exercise every command,
   malformed lengths/offsets, lock gates, no-ACK errors, storage errors and
   send-before-boot ordering using offline protocol models. Stop on any wire
   difference or extra write. The final raw-HID send is already shared; do not
   count extracting it again. Avoid combining EP0, unlock and storage changes.

5. **Other helper sites after provenance/range proof.** The seven multiply
   sites are in `sine8`, two in `rgb_matrix_task`, `hsv_to_rgb_into`, the macro
   delay and two in `fast_set_leds` (exact addresses and RST lines in JSON).
   Inspect the two `fast_set_leds` packet-index calculations before attempting
   a cast or strength reduction; retain offset overflow and partial-packet
   rejection tests, all LED bounds and exact Direct-mode bytes. RGB already has
   bounded arithmetic changes and exhaustive host/CPU evidence; a new rewrite
   must rerun those same domains, not reuse their PASS. Generic EEPROM/report
   APIs and memcpy sites are not safe global cast targets. Stop where an
   external caller, address space, aliasing or legal range remains unproved.

USB setup/descriptor dispatch is large but remains a lower-priority structural
probe. `protocol/ch555/usb_ak820.rst:1368` and `:1027` identify the 2,065-byte
setup and 452-byte descriptor groups. Any probe must compare all request fields,
interface bounds, stalls, transfer lengths and ISR/EP0 state ownership. Size
alone does not justify changing this path. Existing EP0 private-copy work is
not a fresh saving.

For every accepted experiment, check source/artifact manifests, IHX hash, both
CODE windows, XRAM, stack capacity and focused CPU stack use. Then run the
offline regression suite and independent code/document/evidence review. A
capacity figure is not a global stack bound. Physical timing, USB interaction,
LED appearance, persistent writes and power-loss behavior remain untested
without separate authorized device work. No live update follows from this report.
