# Offline keymap buffer regression

From the repository root:

```sh
python3 tests/ak820_keymap_firewall/run.py
python3 tests/ak820_keymap_firewall/linked.py --help
```

The host runner reads current source and headers, builds a temporary harness,
and compares the extracted function with the saved Git source oracle. It uses
the local compiler with ASan/UBSan when supported, and without sanitizers
otherwise. If no local compiler is available, it uses the offline
`ak820-nkro-study-env:local` image. The retained pass 28 run uses ASan/UBSan. It checks 6,849,504 cases, three mutants and
QK_BOOT alias drift. It does not connect to a keyboard. The EEPROM is a host
mock: a scheduled read fault returns `0xff` and sets a sticky flag. Write
failures and durable storage behavior are outside this test.

## Exact linked CPU check

`linked.py` is the reviewed runner retained byte for byte from the external
pass 28 proof. It uses the repository's pinned SDCC 4.6.0 `s51` in generic C52
mode. Retained build outputs are required; no firmware build or device access
is performed. Reproduce the 600-case check from the repository root using the
same offline container image:

```sh
mkdir -p /tmp/ak820-pass28-linked
docker run --rm --network none --userns=host --user "$(id -u):$(id -g)" \
  -v "$PWD/..:$PWD/..:ro" \
  -v /tmp/ak820-pass28-linked:/tmp/ak820-pass28-linked:rw \
  sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d \
  python3 "$PWD/tests/ak820_keymap_firewall/linked.py" \
  --repo "$PWD" \
  --build "$PWD/qmk-8051-ak820/.build/resume28-keymap-firewall" \
  --output /tmp/ak820-pass28-linked
```

The parent mount is read-only and only the output directory is writable.
`results.json` records input hashes, per-case results and CODE snapshots;
`cpu.log` retains simulator output. A reproduced result identifies the local
`linked.py` path; the original proof identifies its external `runner.py` path.
The [pass 28 collector](../../audits/maximal-pass28-20261025/README.md) verifies
that both runner files have identical bytes.

The runner checks unique matching build-source entries, parameter widths and
the QK_BOOT alias. It executes the actual linked setter with partial keycode
pairs, unchanged writes, lock/cache flag combinations and 88 early rejections.
It checks input guards, all 64 cache bytes, flags, returned SP and stack canaries,
and requires every occupied CODE byte to match before and after execution.
Flash entry stopguards fail the check if reached. Only the trampoline may be
written to an empty simulated ROM range.

CRT runs only to main entry. Main, board and NVM initialization do not run;
IRQs are disabled. Accepted requests fit one primed cache page with batch depth
one. Only pre-existing sticky failures are tested: actual new read faults,
dirty cross-page transitions, flash effects, durable storage, interrupts and
physical keyboard behavior are not qualified. The oversized maximal image
remains diagnostic and cannot be installed.
