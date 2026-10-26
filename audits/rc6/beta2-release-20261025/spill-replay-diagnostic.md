# Spill replay diagnostic, 2026-10-26

The capture defect is confirmed. A pinned-compiler replay retained a warning inserted between `F` and `UNCTION` in the exact AST identity of `_ak820_extension_address`. Compiler ASM remained canonically identical to the frozen original; the source proof rejected only the corrupted AST identity. The correction keeps stdout and stderr separate. Fresh corrected-source qualification remains a separate requirement. Compact evidence: [capture-defect.json](spill-replay-diagnostic/capture-defect.json), [failed-header.txt](spill-replay-diagnostic/failed-header.txt).

The v3 preflight failed at the final inspector with `Spill source/type/opcode proof differs: selected`. The original differing record was not retained: the inspector removes its temporary replay directory when the exception exits. The traceback alone cannot establish the cause.

Six fresh compiler replay runs compared all nested values against the frozen spill report. All six matched `selected` (74 entries), `rejected`, input and output hashes, nominal saved bytes and extra stack bytes. The last five ran in one Python process. No ordering or temporary-path difference was observed.

The diagnostic used image `ak820-nkro-study-env:local`, UID 898, no network and read-only bind mounts. The multios clone was mounted at its original canonical checkout path. Original context provenance and the pinned toolchain were mounted read-only. All generated replay files were private container temporary files. Firmware source, compiler objects, proof reports and linked images were not changed. No USB command was sent.

The saved spill report SHA256 is `a3f1c01212b0167ba950c09983b1822cc101867d670442a1b62b68261d0c71e6`. The implementation SHA256 is `cfb43d3ccaf73ec27183c65eb142a6fc8263a1bf2df8694e0650fa822dd0c9f0`.

Two full inspectors also passed in one process, overlapping part of the repeated replay workload. Both retained IHX SHA256 `d8467f3cdd50bf6a4bca14ab1c4c05804f7bdd9a1d55a4ef589e4fdc51fa62c0` and MAP SHA256 `f333082e6f6679fc34a7a94625f8fffc7e54fa37295cb6e20b73ab118d140004`. A process-local diagnostic wrapper prints complete saved and replay values before the existing comparison if a mismatch occurs. Scripts: `/tmp/spill-diagnostic.py`, `/tmp/spill-repeat.py`, `/tmp/spill-inspect.py`; inspector log: `/tmp/spill-inspect-diagnostic.log`.

This evidence does not explain or erase the v3 failure. A recurrence needs the failed selected records and rejection reasons retained before temporary cleanup. No comparison gate was changed.

A third full inspector passed with a process-local temporary-directory meter. Immediately before cleanup its 536 files used 22,233,333 logical bytes and 22,538,240 allocated bytes. The container temporary filesystem reported 888,729,600 free bytes on the 120,746,736,640-byte root filesystem. Host `/mnt/storage` separately had 747,736,924,160 available bytes; Docker data root was `/var/lib/docker/103.65533`. The metered log is `/tmp/spill-inspect-metered.log`. This confirms that default container `/tmp` consumes the small root filesystem. The measured retained replay footprint alone does not establish that ten concurrent inspectors exhausted it; it is not a peak measurement of the original preflight workload. Disk pressure remains a hypothesis, with no retained ENOSPC message from the failed v3 run. Routing future temporary files to the large storage filesystem does not change proof comparisons or firmware.

## Recurrence during final qualification

The final multios worker stopped with the same selected-proof mismatch after all 28 base suites passed. Its temporary files were already redirected to `/mnt/storage`, so that capacity mitigation did not eliminate the failure. The stopped worker took 749.76 seconds. Its log is in the multios clone at `qmk-8051-ak820/.build/beta2-qualification-final/multios.log`. No divergent payload survived that attempt.

An external forensic wrapper now calls the unmodified inspector using the qualification interpreter `/tmp/buildenv/bin/python`, the same canonical source mount and the large scratch filesystem. It saves complete frozen and replay reports for every spill call and copies the temporary proof tree before comparison failure can remove it. Compiler-capture exceptions are printed and rethrown unchanged. Repository sources, proof gates and existing build evidence remain unchanged. The wrapper is `/tmp/spill-forensic-repeat.py`; its log is `/tmp/spill-forensic-repeat.log`; retained reports are under `/mnt/storage/Temp/ak820-beta2-20261025/scratch/multios/forensic/`.

A separate replacement entrypoint was prepared at `/tmp/ak820-beta2-forensic-qualify.py`. It forwards the original arguments through `runpy.run_path(..., run_name='__main__')`; it does not call qualification during preparation. Its trace returns the exact original replay object and rethrows original capture exceptions. Archive setup, formatting and recording errors are handled as best-effort observations so they cannot replace validator results. The corrected wrapper SHA256 is `0723d3e1e4f597e2b9fb810e6676d19a7afa4156cc55c25ca22f1dd9c4bc5f0d`.

The five-call forensic run completed successfully in one process. All five full inspectors passed, and every compared spill field matched the frozen proof. Complete expected/replay reports remain in `forensic/call-1-1` through `forensic/call-1-5`. The only traced capture exception was the existing `quantum/keymap_introspection.asm` generated-include rejection, identical to the frozen report's two rejected functions. A separate first exact-interpreter inspector also passed. No failed selected payload was reproduced in these read-only runs. A deterministic third-inspector mutation was not observed. The diagnostic containers have exited; actual qualification has not been launched by this diagnostic.

## Onehand recurrence

The onehand final worker later stopped with the same selected-proof mismatch during profile qualification after 2670 seconds. A separate direct spill-prepare loop was started against its stopped clone, mounted read-only at the source-bound `ak820-beta2-qualified-c-20261025` path. It runs up to 50 iterations or stops at the first divergence. Each iteration retains expected and replay reports; a divergence also retains the entire temporary metadata and rewritten-output tree. The loop uses the pinned compiler and `/tmp/buildenv/bin/python`; generated files stay under the large onehand scratch directory. No firmware build, source change or USB command is involved. Script: `/tmp/ak820-onehand-spill-loop.py`; log: `/tmp/ak820-onehand-spill-loop.log`; archive: `/mnt/storage/Temp/ak820-beta2-20261025/scratch/onehand/onehand-loop-a9c4ac9136a849eb8151e664c220783d`.

The direct onehand loop was stopped at the coordinator's request so the actual full lifecycle could run through the forensic entrypoint. Six complete replays matched every compared field. A seventh iteration was interrupted during source proof and remains unqualified. Its partial temporary tree was copied before interruption to `INTERRUPTED-onehand-replay-i52xm848` under the same archive, with an explicit `INTERRUPTED.json` marker. The diagnostic container exited with status 130 and no longer owns the clone. No divergent selected payload was observed in the six completed iterations; this does not close either earlier qualification failure.

## Captured MMO divergence

The held-file-descriptor observer retained a concrete MMO replay mismatch in `inotify-proof-observations/mmo/ak820-pass30-proof-6b3ycdn1`. Selection fell from 75 to 74 entries. The only missing entry was `quantum/dynamic_keymap.asm` / `_ak820_extension_address`; its new rejection was `Missing/ambiguous AST function identity`. The compiler-capture stage itself succeeded. Its AST file was removed before the observer could copy metadata.

A targeted read-only loop now captures only that translation unit and checks the missing candidate. Every AST, raw typed dump, preprocessed input and compiler ASM is retained under `scratch/mmo/mmo-ast-d1dc94960260481594362f69e3075318/call-N`. Existing merged AST captures contain warning text inside AST lines. In capture 2, a warning interrupts the `_ak820_extension_address` FUNCTION header after `args (... unsign`; the identity prefix survives, so that run still passes. Printed heap-pointer widths also vary between captures, changing AST byte offsets. A warning splitting the identity prefix remains a hypothesis until a failed header is retained.

A separate-stream experiment used the exact pinned compiler command and frozen preprocessed input. It returned zero, produced canonical ASM identical to the original, and passed source proof. AST stdout contained 139,845 bytes; warning stderr contained 2,926 bytes. Both streams and all compiler outputs are retained under `scratch/mmo/mmo-ast-843da26e065947af88f9d7d9c8baab1a/separate-streams`. No repository source, proof rule or firmware image was changed.

## Capture correction

The integration capture now writes compiler stdout unchanged to `.ast.log` and stderr separately to `.diagnostics.log`. Both files enter the existing hashed metadata file set. The AST identity check is retained. This removes the confirmed mixing of warnings and AST bytes without suppressing warnings or relaxing candidate admission. New build and qualification evidence is required for this changed generator; prior failed attempts remain failed.

The old MMO clone and its original proof remain unchanged for the targeted diagnostic. The separate-stream experiment confirms canonical ASM identity and successful source proof for the pinned compiler with separated outputs. The exact bytes of the originally rejected FUNCTION prefix were not recovered, so that individual old failure is not claimed to have a fully recovered AST explanation. The retained malformed successful FUNCTION header establishes a capture defect that warrants correction independently.

## Confirmed failed header

Targeted MMO capture 176 reproduced the exact rejected function and reason after 175 successful captures. The original merged AST contains, at lines 163–166:

```text
Fquantum/dynamic_keymap.c:291: warning 127: non-pointer type cast to generic pointer
from type 'unsigned-int fixed'
  to type 'const-void generic* fixed'
UNCTION (_ak820_extension_address=0x10460980) type (unsigned-int fixed) args (unsigned-char fixed, unsigned-char __xdata)
```

`capture()` completed its compiler, dependency and canonical-ASM checks. `source_proof()` returned `false, Missing/ambiguous AST function identity`. The raw typed dump and preprocessed input were retained. Removing only this exact warning block in memory restored source proof; the saved AST and validation gates were not edited. The separate-stream experiment used byte-identical preprocessed input and also retained canonical ASM identity. This establishes warning/AST stream mixing as the cause of the reproduced rejection. The original MMO observer recorded the same missing function and reason; its deleted original AST was not recovered.

The failed AST SHA256 is `2190bed042cd8bd0e59f7f41a2393bf5df5cb13ed874abe6a7713466010bf595`; the pinned compiler SHA256 is `3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891`. Other source, preprocessed, ASM and raw hashes are in `capture-defect.json`. Full failure 176 and the separate-stream experiment were copied to `/mnt/storage/Temp/ak820-beta2-20261025/failure-evidence/spill-capture-20261026`, sealed with `SHA256SUMS`, and made read-only. The loop exited with status 1 on its first reproduced rejection; the old MMO clone is released and unchanged.
