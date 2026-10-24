# Foreground input outlining, 2026-10-24

The exact outliner admits the tapping and combo modules and five foreground board RGB functions. The opcode allowlist, direct-memory/SFR exclusions, ABI and refusal of nested helpers are unchanged. Board initialization, clock setup, matrix snapshots and all interrupt functions remain excluded.

The conservative retained-symbol graph from the fresh build has three interrupt roots and 13 reachable functions. None of the newly selected sites is reachable from those roots. The LED interrupt's numeric local call stays inside its excluded function. `irq-reachability.json` records the roots, closure, selected sites and input hash.

## Build result

The pinned SDCC 4.6.0 build uses the real main window 0x3027..0xc6ff and low window 0x28a0..0x2fff. The retained source savings patch is included for measurement and is excluded from the outliner patch.

| Build | Main bytes | Low bytes | Total bytes |
| --- | ---: | ---: | ---: |
| Existing default control | 38492 | 1821 | 40313 |
| Retained source savings, prior measurement | 38230 | 1804 | 40034 |
| Retained source savings plus new scope | 38010 | 1804 | 39814 |

The new scope saves 220 linked bytes beyond the retained source changes, or 499 bytes against the default control. The highest linked address is 0xc4a5. The manifest contains 155 helpers and 1608 replacement calls, with 2575 nominal saved bytes. Existing helper calls already require two extra live stack bytes; this scope change adds no further nesting.

On the original control's fresh pre-outline input, nominal selection changes from 2282 bytes to 2493 with tapping/combo, then 2513 when the foreground board functions and matrix snapshot are admitted. The shipped scope excludes the matrix snapshot. Nominal selection and linked image savings differ because selection order and code placement affect the result.

## Verification

The 12 focused outliner unit tests pass. Linked tapping tests pass all 65 cases; linked combo tests pass all 26 cases. Their peak exercised stack pointers are 135 and 128. The JSON results include image, tool and runner hashes.

The full helper differential suite passes all 155 helpers and 1608 replacement calls, with 16 CPU states per helper (2480 helper/state cases). `outline-results.json` records emitted-byte, relocation, replacement-call and CPU-effect verification.

These are static, build and CPU checks. They do not validate physical timing, interrupt latency, USB, flash or LED DMA behavior. No device was opened, reset or flashed.
