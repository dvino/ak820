# Pass26b linked component result

**PASS** for `.build/resume26b-state-bytes`. This is bounded CPU and static evidence for an oversized diagnostic image. It does not qualify a device update.

| Identity | SHA256 |
| --- | --- |
| IHX | `47400365dfe8e7e56fd46a548938ca8c9024467ca13120f506cb7213e9f7ef10` |
| MAP | `6674f5031e0d2fcf1ad7e9f8a68ea5eac1f2fb8dd6a7676ea0642dbd6177f5d2` |
| Frozen runner | `2a233abda1e08798d0f9bcc9614c40a463788017724c9861e9ac2cc2f2ed4c3e` |
| s51 | `61b7a6a84d3f5702c7e45df5b019cf0610d13f9d74046e69820291290d1e5cdd` |

`pass26b-final/results.json` contains the complete result, support-runner hashes and the eight relevant source/config/guard files authenticated against this build's source manifest. Those files, the image, map and build report stayed unchanged during execution. This verifies selected inputs and image identity; it is not a separate reproduction of the complete build.

## Coverage

| Check | Cases | Result |
| --- | ---: | --- |
| Public VialRGB setter | 629 | All 256 packet lengths; nine first-index boundaries; counts 0–11 and 255; 256 value inputs across four edge positions; full 82-entry HSV array, original packet, adjacent guards and return SP. Actual compiled brightness clamp: 160. |
| Public Combo GET | 576 | All 256 indices in both lock states; valid, corrupt marker, corrupt version, duplicate and empty records for every valid index; complete 32-byte reply, guards, unchanged cache/read state and return SP. |
| NVM update and real writer | 48 | Dirty/failed state combinations; empty, equal, first/last mismatch, upper cache edge, equal page crossing, out-of-range zero reads, and 65535 wrap into cache zero; unchanged source and guards; original three-byte address/tag and 16-bit length on mismatch. |
| OEM IRQ nesting | 15 | Every ordered distinct-source nest; register/frame restoration, return SP and foreground canary. |
| LED selector | 256 | Every selector byte. |

The real flash erase, byte-program, page-program and NVM page-writer entries had stop breakpoints. None was reached. Empty/equal stack-kernel paths preserved R0/R1; the real C tailwriter retains its normal caller-scratch ABI. Generic address tags 0, 0x80 and 0xff were retained on mismatch. The earlier baseline image also passed the same 48 NVM output/cache oracles; caller-scratch registers are not compared across C and assembly implementations.

All eight valid Combo slots at base 0x658, with ten bytes per slot, fit wholly within a 64-byte cache page. Their five row forms in both lock states give 80 wholly cached record checks. No valid split record occurs in this layout. Split-layout indices outside the supported eight entries are rejected before a record read. A future valid cross-page record layout is not qualified by this fixture.

## Fresh stack bound and code integrity

The fresh `_main` analysis returned **103 bytes with no unresolved paths**. The linked CRT contains one call to main at 0x3070, bytes `12afa0`. Actual CRT execution stopped at main with SP 90, compared with initial SP 88, confirming its two-byte entry frame. The IRQ CPU model therefore reserved **105 bytes**, derived for this image.

Timer, USB and LED callbacks have static bounds 2, 5 and 2. Each unchanged public OEM wrapper adds 17 bytes. The distinct-source IRQ bound is **60 bytes**. Foreground, CRT and all distinct-source interrupts total **165 of 167 available stack bytes**. `foreground-stack.json` retains the fresh main analysis and private guard source identities.

CRT ran only to main entry. Main, settings initialization and NVM initialization did not run. IE and IE_EX were explicitly masked. No ROM byte at or above 0xc700 was written. All **4,394 occupied CODE bytes at or above 0xc700** were read back and matched the exact IHX in **all 20 simulator sessions**. Only the call trampolines, pinned public OEM wrapper/helper fixture and callback slots were added outside application windows.

## Limits and replay

Generic C52 execution models instructions. OEM wrapper invocation supplies hardware return frames, and the fixture supplies the USB ACK side effect. Real interrupt timing, peripheral routing, USB transport, LED DMA, physical flash and device behavior remain untested. Dirty cross-page transitions that require flash are excluded. The equal NVM crossing case uses immutable linked CODE as its physical-read fixture, without pretending that it represents saved settings. This bounded suite does not replace full configured regressions or hardware checks.

Replay from the repository root with the matching build artifacts and sources:

```sh
python /path/to/run.py --repo "$PWD" \
  --build "$PWD/qmk-8051-ak820/.build/resume26b-state-bytes" \
  --source-root /path/to/exact-pass26b-source-checkpoint \
  --output /path/to/new-results --sections rgb,combo,update,irq
```

The runner is frozen at the hash above. `run.py` and the matching `runner-2a233abda1e08798d0f9bcc9614c40a463788017724c9861e9ac2cc2f2ed4c3e.py` snapshot are identical. Production source files were not edited by these checks. No build, physical device access or commit was performed by this test task.
