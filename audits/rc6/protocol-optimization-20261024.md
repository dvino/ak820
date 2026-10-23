# Protocol, EEPROM and RGB reduction

The isolated control is commit `4b83bb9`. The accepted source candidate saves
346 linked CODE bytes. Main CODE falls from 38,590 to 38,258 bytes; low CODE
falls from 1,887 to 1,873 bytes. XRAM falls from 2,512 to 2,509 bytes, and stack
capacity rises from 157 to 162 bytes. These are build and CPU-model results.
No keyboard was accessed and no image was selected for installation.

The complete control is `qmk-8051-ak820/.build/protocol-control2`; the complete
candidate is `.build/protocol-xdata-block` in the same source tree. Their input
manifests, relocated listings, IHX files and memory reports are retained.
The machine summary is `.build/protocol-verification/accepted-summary.json`.

## Changes

USB SETUP dispatch uses one request-byte switch. The recipient, direction,
configuration, value, interface and length checks remain in each branch.
USB and HID requests which share a byte remain grouped and separately checked.
Four private bit flags cache unchanged packet predicates. The descriptor selector
uses a CODE-only table of typed CODE pointers after the same interface bound.

Reactive RGB aging clamps the tick count to 255 only for byte-age arithmetic.
Every age fits in one byte, so any larger tick count produces the same zero.
The full tick count still advances the timer. Direct mode copies its three HSV
bytes before the other effect branches; the overwritten default assignments
are avoided. The rendering order, batch limit and HSV conversion remain.

The board implements the existing byte-read API through a shared offset-read
helper. Public generic EEPROM block functions remain in source with their
original signatures and pointer-space behavior. Separate, explicitly named
XDATA block APIs serve proved target buffers. The generic block bodies become
unreachable in this firmware and are removed by the existing DCE stage.
The private update function preserves the initial compare and full-block write:
unchanged data cannot trigger a cache load, flush or additional write.

## Buffer provenance

The following list covers every private block call in the accepted linked
image. EEPROM address arguments remain generic numeric EEPROM offsets; only
actual data buffers use typed XDATA pointers.

| Call group | Data-buffer origin and linked proof |
| --- | --- |
| Scalar word/dword reads | Address of the local return value in `eeprom_driver.c`. Final `eeprom_driver.rst` declares both return objects in `XSEG (XDATA)` at lines 84–92. |
| Scalar byte/word/dword writes | Address of the by-value argument. The same listing declares all three parameter objects in XSEG at lines 93–102. No caller-supplied data pointer is narrowed here. |
| RGB read/update | Global `rgb_matrix_config`, declared in XSEG at `ak820_rgb.rst:600–602`. |
| Default RGB EEPROM clear | Address of local eight-byte `dummy`, declared in XSEG at `quantum/eeconfig.rst:563–565`. The named private API is guarded by `AK820_BOARD`; other targets retain the generic call. |
| Macro length commit | Local three-byte `metadata`, declared in XSEG at `ak820_macro.rst:76–92`. |
| Macro data write | Existing private typed `data` view in `ak820_macro_write`; its sole firmware call chain is `ak820_usb_raw_task` → `raw_hid_receive` → `dynamic_keymap_macro_set_buffer` → `ak820_macro_write`. The first function passes static `raw_buffer`, explicitly declared `__xdata`. The existing public generic interfaces remain. |
| Dynamic keymap/macro read | Existing typed `target` in `ak820_dynamic_read_buffer`; both public callers forward the Raw HID packet payload. The sole retained transport producer is the same explicit-XDATA `raw_buffer`. |
| Dynamic keymap write | Existing typed `buffer` in `dynamic_keymap_set_buffer`; its only retained caller forwards the Raw HID payload. No new narrowing cast is introduced. |
| Private update-to-write | Forwards the same already typed source buffer after the first different byte. |

The accepted relocated listings contain no direct generic block API calls.
Combos is absent from this isolated measurement. Its separately implemented
get/set entry paths need explicit private-API redirection during integration.
The Combo implementation reports model-large local entry and stored-copy
buffers for those two paths; their final placement must be checked again in
the combined listings. This audit does not substitute for that integration proof.

## Measurements and rejected probes

All accepted rows below use complete, valid input manifests. The switches and
RGB aging were combined in the second successful candidate; their individual
contributions were not separately measured.

| Build directory below QMK `.build` | Total CODE | Main | Low | Decision |
| --- | ---: | ---: | ---: | --- |
| `protocol-control2` | 40,477 | 38,590 | 1,887 | Control |
| `protocol-usb-switch` | 40,461 | 38,574 | 1,887 | Retained |
| `protocol-usb-age` | 40,443 | 38,556 | 1,887 | Retained |
| `protocol-descriptor-table` | 40,384 | 38,497 | 1,887 | Retained |
| `protocol-predicates` | 40,365 | 38,478 | 1,887 | Replaced: ordinary bool locals cost four stack-capacity bytes |
| `protocol-rgb-direct` | 40,334 | 38,447 | 1,887 | Retained Direct-mode change |
| `protocol-bit-predicates` | 40,305 | 38,418 | 1,887 | Retained bit locals; one capacity byte before later EEPROM gains |
| `protocol-eeprom-byte-final` | 40,259 | 38,372 | 1,887 | Retained byte-read helper |
| `protocol-eeprom-writebyte` | 40,291 | 38,404 | 1,887 | Rejected: 32 bytes larger than read-byte candidate |
| `protocol-eeprom-word` | 40,276 | 38,389 | 1,887 | Rejected: 17 bytes larger than read-byte candidate |
| `protocol-xdata-block` | 40,131 | 38,258 | 1,873 | Accepted source candidate |
| `protocol-macro-fields` | 40,079 | 38,258 | 1,821 | Separate follow-up, not included in frozen accepted source |

A byte-algebra CRC replacement crossed the main-window end and was rejected:
it added 66 bytes to the first switch candidate. The original CRC is retained.
The first control attempt failed because LUFA was a directory symlink omitted
from the input snapshot; a fresh control used local dependency copies. One
intermediate switch build was invalidated by an RGB source edit before its
manifest check; no result from that build is used here.

The separate macro-field follow-up replaces two assignments of a two-byte
nonvolatile parser structure with assignments of its two byte fields. The
linked objects are separate two-byte XDATA objects, and no padding or aggregate
representation is consumed by the parser. It saves 52 low-window bytes; it is
not in the frozen accepted source. Its source, diff and complete build are
retained separately under `.build/protocol-verification` and the build named
above. Independent review and combined measurement are still required.

## Verification

- Production USB ASan/UBSan harness passed with and without mouse support.
- The deterministic production-source SETUP comparison matched two million
  cases in each image, including every request/type byte pair and malformed
  field boundaries. Both transcript hashes were `ab47fa10b13357b7`. It compares
  packet data, controller state, endpoint registers and setup lengths; it is a
  host model, not an SDCC/interrupt timing test.
- RGB decay matched for 1,048,576 pairs: every byte age and every tick count
  obtainable from a 16-bit elapsed timer shifted by four.
- The production RGB host suite passed effects, Direct, transitions, wrap and
  all 16,777,216 compact HSV cases. Its first run stopped in LeakSanitizer on
  unavailable `/proc` task enumeration. A repeat with `detect_leaks=0` passed;
  address and undefined-behavior checks remained enabled.
- The linked C52 RGB suite passed for control and accepted candidate. The
  candidate reached SP 116, or 23 bytes above its initialized SP. The tested
  stack consumption is the same as the control. This is not a global or IRQ
  stack bound.
- Scalar and private-block comparisons matched all 65,536 addresses for byte,
  word and dword reads in uncached, dirty-cache and flushed states. Additional
  block read/write/update boundary cases include offsets 65,535 and the NVM
  end. Ordered flash reads/programs/erases, diagnostics and the final full
  flash image matched; transcript hashes were `43d167fdc1acabd3`.
- Production VIA/NVM host regression passed locked boot filtering, six-layer
  reset, cross-page transfers, wear avoidance, overflow rejection, macro
  bounds and schema failure without writes.
- The NVM power-cut model passed 10,944 cases. The macro power-cut model passed
  25,088 cases across two erase orders, plus grammar, split, bounds, retry,
  restart and full-capacity checks. The separate macro-field follow-up passed
  the same macro model.

The private comparison programs and JSON results are retained in
`.build/protocol-verification`. The generic EEPROM APIs remain available for
other pointer spaces in source. No user settings, EEPROM layout, macro limits,
layer count, unlock rule, durable write ordering or failure stop was changed.
USB peripheral timing, electrical IAP behavior, RGB appearance, actual flash
retention and complete interrupt concurrency remain untested on hardware.

## Retained checks

The essential comparison programs and machine results are also retained in
`audits/rc6/protocol-optimization-20261024/`. The two Python comparisons accept
`--source-root` and `--output-dir`; their default source root is resolved from
the repository location, and the control is immutable commit `4b83bb9`.
Both scripts were rerun successfully after being moved to that directory.
From the repository root:

```sh
python3 audits/rc6/protocol-optimization-20261024/usb_differential.py
python3 audits/rc6/protocol-optimization-20261024/nvm_scalar.py
cc -std=c11 -Wall -Wextra -Werror -fsanitize=undefined \
  audits/rc6/protocol-optimization-20261024/rgb_age.c -o /tmp/ak820-rgb-age
/tmp/ak820-rgb-age
```

The isolated callee-save check first failed its stack expectation for every
function: initialization stopped at `main` after CRT's LCALL, so the live SP was
two bytes above the layout's initial SP. Registers and returns matched. A
separate fixture normalized SP after initialization and then passed all 2,674
ABI cases, including the moved byte reader. Both machine reports are retained.
The permanent regression should capture the SP after initialization and compare
against that value; it need not change simulated SP. The byte-reader listing
mapping also needs `ak820_nvm.asm` instead of `eeprom_driver.asm`.
