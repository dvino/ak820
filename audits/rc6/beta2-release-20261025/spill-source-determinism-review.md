# Spill replay source review

Review, 2026-10-26. The retained call-176 AST now confirms diagnostic text splitting the target FUNCTION header; see the final section. Earlier sections record the narrowing before that payload was available. No build, inspector, compiler replay or USB operation was run for this review. Firmware, tools and tests were left unchanged.

The message `Spill source/type/opcode proof differs: selected` narrows the failure to admission of candidates, provided the frozen input files stayed unchanged. It does not itself identify a source/type or opcode defect.

- `inventory()` visits ASM files in sorted path order and instructions in file order (`ak820_parameter_spills.py:57`). Candidate state, references, entry bytes and replacement instructions come from frozen ASM/LST. Replacement register order is explicit. Iteration over the per-line symbol set cannot reorder references for any one symbol. No persistent module state is mutated between calls.
- `prepare()` captures modules in sorted order (`:484`). Its `selected` records contain candidate data and deterministic replacement data; captured temporary paths, raw dump hashes, compiler addresses and type strings are not inserted into those records. Ordering of the metadata `keep` set changes JSON manifest key order/hash, but that hash is not among the replay fields compared by `check_pass30()`. It cannot alone produce the selected mismatch.
- With those frozen files, `opcode_proof()`, `tail_private_access()` and replacement choice have no subprocess or random inputs. Fresh compiler output influences selection through capture success and the boolean result of `source_proof()`. A changed AST/raw/preprocessed text matters only if it changes one of the explicit admission predicates.

A concrete diagnostic weakness exists at `prepare():485-486`: every `ValueError` from `capture()` becomes a rejection for every otherwise eligible candidate in that module. In particular, a nonzero c1 compiler exit becomes `Typed SDCC capture failed`, while a missing dump or canonical ASM difference becomes `Typed compiler ASM identity mismatch`. Either can remove candidates and later surface only as the selected-list mismatch. This is fail closed; it is not evidence that either condition occurred in the reported failures.

Preprocessor failure uses `check=True` and raises `CalledProcessError`; subprocess timeouts raise `TimeoutExpired`. Neither is caught by that ValueError handler. Therefore ordinary preprocessor failure or a timeout would have a different direct traceback, rather than this mismatch. A nonzero c1 exit is different because it is explicitly translated into ValueError.

`canonical()` removes comments and whitespace outside double quoted literals. It retains labels, directives, areas, symbols, operands and literal contents. A compiler change confined to comments cannot fail canonical comparison. A semantic-looking output difference or missing output can fail capture even if the original C input is unchanged; its exact difference must be retained before assigning a cause.

The capture directories are fresh and module-relative, and modules are captured sequentially. No shared output filename between the reviewed capture calls was found. Preprocessing runs in the QMK root with the original flags, so generated include files in the original object directory remain inputs. Dependencies outside that object directory must match the initial snapshot. Object-directory dependencies are exempt from that initial comparison, but are hashed before and after capture; canonical ASM must still match the original. This exception is a bounded place to inspect if a failed payload reports input or include differences; it is not evidence of a concurrent writer. Reviewed host harnesses create their generated C/header files in private temporary directories; linked harnesses write their supplied output directories. No writer of the original compiler dependency tree was found in those paths.

`check_pass30()` compares `selected` before `rejected`, output hashes or byte totals (`configure_firmware.py:458-460`). Its TemporaryDirectory exits on the exception and removes the available compiler log, metadata manifest and replay JSON. This ordering hides the more specific rejection reason. `run_profile_tests()` calls the inspector before and after each suite (`:863`, `:870`), explaining the large number of compiler recaptures during qualification; the loop itself does not mutate spill state.

The existing independent instrumented replay is the appropriate next evidence. At the first mismatch, compare candidate keys `(module, function, object)` and the complete `rejected` list, then inspect `metadata/manifest.json` rejection reasons. A whole-module disappearance points first to capture failure; isolated candidate loss points to source-proof admission or changed frozen input. For a c1 failure retain its return code and AST log; for canonical mismatch retain original/captured ASM and a semantic line diff; for source-proof failure retain raw dump, AST and preprocessed input. Do not weaken equality, accept a retry as the missing qualification, or rebuild the frozen images to conceal this failure.

## Retained MMO failure and AST stream evidence

A later retained MMO replay narrows the actual failure further. Its expected and replay JSON files are under `/mnt/storage/Temp/ak820-beta2-20261025/inotify-proof-observations/mmo/ak820-pass30-proof-6b3ycdn1/`. Selection fell from 75 to 74; only `quantum/dynamic_keymap.asm / _ak820_extension_address` disappeared. Its new rejection is `Missing/ambiguous AST function identity`. The comparison file records differences in selected, rejected, output hashes and nominal saved bytes. Thus this occurrence passed module capture and failed the AST identity predicate. It did not follow the whole-module capture failure path described above.

The AST parser splits only at `^FUNCTION \(` and then requires a section starting exactly with `_ak820_extension_address=`. A warning inserted inside that prefix, or between the line start and FUNCTION, makes the actual function disappear from this parser. The typed compilation merges stderr into stdout (`capture():462`), so diagnostics and AST text share the saved stream.

This interleaving is directly visible in a retained successful onehand AST log:

`/mnt/storage/Temp/ak820-beta2-20261025/scratch/onehand/onehand-loop-a9c4ac9136a849eb8151e664c220783d/INTERRUPTED-onehand-replay-i52xm848/metadata/quantum/dynamic_keymap.ast.log`

- Lines 52–56 split `SYMBOL` into `S`, then warnings from `_pin_defs.h:41` and `dynamic_keymap.c:205`, then `YMBOL`.
- Lines 110–113 insert the `dynamic_keymap.c:230` warning between an ADD node's pointer and its type.
- Lines 161–164 insert the `dynamic_keymap.c:291` warning inside a CONSTANT node, just before the target function's intact header at line 166.

The first diagnostic occupies 107 bytes. The first AST-token interruption starts at byte offset 4203: exactly 107 + 4096. This is concrete evidence consistent with buffered AST stdout flushing in 4096-byte chunks while diagnostics enter the merged stream separately. The log also contains process pointer values in AST nodes, which are irrelevant to function identity but alter textual positions when their printed widths change. Buffer-boundary movement is a plausible explanation for intermittent corruption of a particular header. The failed MMO AST itself was not retained, so the exact corrupted header and the cause of any boundary movement remain unconfirmed.

The narrow corrective direction, if the targeted capture confirms this cause, is to preserve compiler stdout and stderr separately and apply the AST parser only to the AST stream. Compiler diagnostics should remain retained and compiler exit status must still be checked. Broadening the FUNCTION regex over a contaminated stream or weakening replay equality would obscure the cause. No such source change was made in this review.


## Confirmed cause from retained failing AST

The targeted MMO capture retained a failing AST at:

`/mnt/storage/Temp/ak820-beta2-20261025/scratch/mmo/mmo-ast-d1dc94960260481594362f69e3075318/call-176`

Independent reading confirms that AST lines 162–166 contain `F`, immediately followed by the three-line warning 127 diagnostic, then `UNCTION (_ak820_extension_address=0x10460980)`. There is no matching `^FUNCTION (_ak820_extension_address=` header in this file. Its SHA256 is `2190bed042cd8bd0e59f7f41a2393bf5df5cb13ed874abe6a7713466010bf595`, matching the retained capture record. `result.json` records the failed source proof; `diagnosis.json` records that removing only the inserted warning block in memory restores the source proof. That diagnostic operation did not replace any artifact or relax a qualification gate.

The original compiler ASM was independently compared with the captured ASM using the reviewed canonical function. The original comes from `/mnt/storage/Temp/ak820-beta2-20261025/failure-evidence-ast-streams-20261026/mmo/canonical-build/obj_ajazz_ak820_vial/quantum/dynamic_keymap.asm`. Its raw SHA256 is `62a0ec25bf36b6d970df50ccb51ea0399dfbf56588a7c3f1150b705529fe1837`, matching the capture record. Both original and captured ASM have canonical SHA256 `6dc304aa1407e8c2a21bc7eb84a2cee0e347e3931436fba6573b77a453c4b370`.

This confirms the mechanism: merged compiler diagnostics split the AST FUNCTION token, the exact AST identity parser rejects the otherwise captured candidate, and spill replay selection differs. The retained compiler code remains canonically identical. This evidence establishes the reproduced failure mechanism without assigning an unobserved exact byte boundary to the earlier cleaned-up qualification attempts. Separating retained compiler stdout and stderr addresses this mechanism; verification of the integrated correction belongs to its own review and qualification evidence.
