# CI host CRC link fix

## Change

`ak820_nvm.c` calls `ak820_crc16`, whose implementation is in `ak820_crc.c`. The two shared host-model link commands in `.github/workflows/windows-installer.yml` listed `ak820_nvm.c` but omitted `ak820_crc.c`. Both commands now include that source file. No C, Python or test source, compiler option, sanitizer, CI policy, tag or release setting changed.

Workflow SHA-256 after the change: `303487a6fd0441643cfefd67aef07592f5ee476fcffb68106500b3bf0acde57a`.

## Previous CI run

GitHub Actions run `40255129448`, shared-host job `121355226331`, passed the 261 host tool tests, 3 compiler tests and 18 compiler-capture tests before failing while linking the NVM power-loss model. The linker reported undefined reference to `ak820_crc16` from `ak820_nvm.c:48`. The failed run remains unchanged in CI history.

## Local host-model check

Both models were compiled and run from the checked-out source in `ak820-nkro-study-env:local` (image ID `sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d`, Debian 12, GCC 12.2.0). The repository was mounted read-only, networking was disabled, and output plus `TMPDIR` were placed under `/mnt/storage/Temp/ak820-beta2-20261025/ci-host-crc-models`. Compile and run exit codes were all zero.

NVM model: 10,944 power-cut cases passed, along with persistence, batching, retry, bounds and cross-page checks.

Macro model: Vial6 grammar, split, bounds, retry, restart and full-capacity checks passed; 25,088 upload power cuts passed across two erase orders.

The full executed commands and model output are in `ci-host-crc-link-fix.log`. This validates host CPU models only; it does not exercise USB or a physical keyboard.

## Source hashes

- `ak820_crc.c`: `0874e2964d63a4e6b2306187759cdf343d4fbc73ee92497e43ae7368bb918b59`
- `ak820_nvm.c`: `ebe940c2354c7d8c015847519e422bb54770216fafdcdd39e5a107fe8631a789`
- `ak820_macro.c`: `8f4fe5f5cf8ee3b87a2b095f4ba4a372d3ab6daefadc6cf1699d3338c898aaa2`
- `nvm_powercut.c`: `9a808a7dcc09e43611b111379780465566d64914b7beba605652d6f39d5433db`
- `macro_powercut.c`: `c3a5f662535a1282fd39974188546566bf99bfb17fd69bc0b2966a695fae0018`
