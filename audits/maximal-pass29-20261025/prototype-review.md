# Independent getter-bounds prototype review

Result: CLEAN for integration of this exact prototype. No blocking correctness finding. This does not approve the resulting firmware image or complete the implementation packet.

Reviewed source HEAD: `6c2cdc0452b664e37cd32a30b31e3e5f800c49cc`. Repository was clean at review entry. No repository mutation, full build, network or device operation was performed. The review was performed independently of prototype authorship.

Frozen evidence directory: `getter-bounds/`. SHA256SUMS SHA256: `744c53b0384bb02c3e4171a72d8f17cdfdc921bde3c90cf6d9aa8a4ac56e79fc`. Every manifest member and all four source hashes were verified. Patch SHA256: `3021ebd7582cf9dff4c9d478f4aa66c1a207dfbf2f094eb0af2d5aa341726a5f`. CPU image SHA256: `cf083dbead1a4e87395740d7e084f43c3b71e670f44fe6a4c2754a1983d67e73`.

## Contract and code

The patch changes only `keycode_at_keymap_location` and `keycode_at_encodermap_location` in `quantum/dynamic_keymap.c`. Non-AK820 bodies remain byte-for-byte original inside the new alternate branches. The outer encoder-enable guard remains intact.

Generic getters already test identical coordinate macros before address computation or EEPROM access and return KC_NO for invalid inputs. The source selection guard and the assembly kernel guard are logical complements over the four required macros; all other configurations retain the generic definitions. The assembly kernel pins geometry and rejects unsupported calling conventions at preprocessing. Its matrix path rejects layer >=6, row >=16 and column >=8; encoder rejects layer >=6 and every nonzero encoder index. The read routine returns DPTR zero on rejection before either EEPROM hook. Valid paths retain exactly two reads at the same big-endian word addresses. The patch reaches no writer and changes no NVM fault handler.

Raw direction bytes remain unchanged through the compiled wrapper parameter copies. Assembly uses zero versus nonzero and generic C uses the existing conditional expression. The native host fixture intentionally replaces bool with uint8_t, which permits byte values 2..255 but is not itself target ABI proof. The separate SDCC assembly injection fixture closes that gap for its tested cases.

The complete source kernel was compared to its repository counterpart. The host oracle independently calculates validity, addresses, byte values and read count; it does not call the implementation to calculate expected values. The generated instruction translation is a model of actual source instructions, not target CPU execution. Its carry arithmetic, register byte truncation, branch conditions and read ordering match the exercised instruction set. This review does not generalize that translator beyond these frozen instructions.

## Independently repeated evidence

All four host configurations were rebuilt and executed in an offline container using scratch copies: AK820 generic, AK820 translated assembly, non-AK820 generic and alternate generic geometry. All 134,217,728 comparisons passed. Actual SDCC/s51 CPU compilation and execution were independently repeated from scratch with the repository mounted read-only: 1,536 matrix and 137,216 encoder checks, including 6,144 raw direction-byte cases, passed. This uses the actual compiled kernel and wrappers with mock EEPROM hooks; it does not execute the complete firmware or hardware. The three retained mutation counterexamples were inspected and detect direction inversion and admitted invalid layer reads in generic and translated assembly paths.

Standalone REL areas independently inspected: baseline CSEG 0x63 (99), candidate CSEG 0x42 (66); XSEG 6 in both, DSEG/BSEG zero. Both baseline valid paths and candidate paths tail-jump to the same getter. Neither wrapper listing contains a new call, push or pop. Public parameter storage is unchanged. Invalid inputs now enter the getter, so scratch-register/parameter-slot activity and instruction count differ, although no EEPROM read occurs. This is compatible with the existing caller-clobbered ABI; it must not be described as identical invalid-path execution.

## Qualifications and next gate

The component command includes --opt-code-speed and ignored -Os; the qualified production build checks a different exact flag string and full audited callee-saves list. The CPU fixture lists only eeprom_read_byte as callee-saved. Neither public getter nor either wrapper belongs to the production callee-saves list, so the forwarding contract is consistent, but these components cannot prove linked-image size, clobbers or stack qualification. The 33-byte reduction is component evidence only.

The configuration check preprocesses the actual selection guard expressions, while its encoder-disabled compile uses a sliced key-wrapper fixture. Encoder-disabled preservation is established here by inspection of the exact unchanged outer guard, not a complete disabled-encoder firmware build.

After integration, obtain exact full-image CODE/RAM measurements, spill/context certificate, startup/foreground/IRQ stack bounds and regression results, update current documentation, and obtain fresh independent review of that exact tree and evidence. No durable-storage fault injection or physical behavior was proven by this prototype.
