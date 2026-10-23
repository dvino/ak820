# RC6 breathing arithmetic probe — 2026-10-23

## Result

The compact breathing interpolation can use an 8-bit product without changing any of its 256 possible outputs. For the table values in this build, adjacent deltas are 1 to 36 and the fraction is 0 to 7, so the largest product is 252. The cast to `uint8_t` therefore loses no bits.

In a frozen link, the candidate reduced CODE by 42 bytes. uCsim C52 also reported fewer virtual clocks in the direct helper and rendered-frame probes. These results support the arithmetic change as an optimization candidate. They do not change the production source or establish physical keyboard timing.

## Proof and build evidence

The source table has a 32-entry compact form used by `breathing_cie`; it was checked at all 31 interpolated intervals. The candidate computes the same result as the existing 16-bit expression for every input from 0 through 255, including the index-31 early return. There were no mismatches. The 256-entry curve was used only as a separate oracle; it is not the table this compact function interpolates.

The machine report records the production source SHA256 as `2d9a4e6541c9b49a76c3f2f1785401c06126c69d47c045421a58abb904fe3aee`. The private candidate source copy has SHA256 `810ac091fb9f0206ab6e6db86e6ab2f51a8003f647c64f35ebb8602db6d23415`. The candidate IHX has SHA256 `6b94dcab471db542d236747babfe553ec984299294ff8428b594cfd1ab9444b5`; the CPU result file records the same linked-image SHA256. This ties the tested image to the candidate build while keeping the production source identity separate.

The existing SDCC 4.4.0 control translation unit reproduced the canonical `ak820_rgb.asm` byte for byte before linking. The candidate compiled from a private source copy. Its CSEG fell from `0xA71` to `0xA47`, saving 42 bytes in the RGB translation unit.

The control's frozen reconstruction reproduced canonical IHX `ae8aff55e799b89ac22dee7aef5d82805359b4ab8bf7b223a95b4c33d5174837` byte for byte. Replacing only the RGB assembly object produced candidate IHX `6b94dcab471db542d236747babfe553ec984299294ff8428b594cfd1ab9444b5`.

| Measure | Frozen control | Arithmetic candidate | Change |
| --- | ---: | ---: | ---: |
| CODE, both windows | 39,432 | 39,390 | -42 bytes |
| Main CODE window | 37,573 | 37,531 | -42 bytes |
| Low CODE window | 1,859 | 1,859 | 0 bytes |
| XRAM | 2,071 | 2,071 | 0 bytes |
| Linker stack capacity | 152 bytes | 152 bytes | 0 bytes |

The compiler emitted `MUL AB` for the candidate product. The existing control calls `__mulint` and shifts the 16-bit result. In the same uCsim C52 helper run, 161 direct calls for inputs 0–160 used 63,181 virtual clocks in the control and 42,895 in the candidate, a reduction of 20,286 virtual clocks. The 50-frame renderer run used 10,013,062 and 10,006,762 virtual clocks respectively, a reduction of 6,300. These counters include the same simulator setup and call machinery in each run; they describe the C52 model only.

The candidate's emitted helper returned the expected sparse-table result for all supported frame values 0–160, with maximum error 1 against the 256-entry curve oracle. Separately, `quantized_curve_error_max` in `compile-report.json` is 17: it measures the difference between each full-curve value and the compact table value at `value >> 3`. It describes the compact table's quantization against the full curve; it is not the interpolation error or a candidate-versus-control difference. All 50 simulated frames passed across ten phases and five hue/saturation combinations. The renderer filled all 82 LED records in batches of at most eight. The runner reported a 152-byte linker stack capacity; that is a linker limit, not a measured physical stack margin.

## Scope and limitations

This is a finite-domain C proof, isolated translation-unit compile, frozen assembly reconstruction, and uCsim C52 CPU model. It does not establish VS11K28A peripheral behavior, DMA transfer, physical timing or smoothness, USB behavior, EEPROM behavior, on-keyboard visuals, or battery impact. No full production builder or packed image was produced, no hardware was accessed, and the installed implementation remains unverified by this probe.

The probe source, variant objects, frozen links, logs, and machine reports are under `qmk-8051-ak820/.build/rc6-breathing-arithmetic-probe-20261023/`. The scripts are `probe.py` and `link_probe.py`. The candidate source was created only inside that private build folder; production `keyboards/ajazz/ak820/ak820_rgb.c` was not edited. The existing build artifacts are preserved. The field names in `compile-report.json` were corrected after the run; no compiler, linker, or CPU tests were rerun for that metadata-only edit.

## Reproduction

The completed run used the output directory recorded above. It already contains artifacts, so the scripts refuse to overwrite it by default. To repeat the run, choose a new output directory and pass it to both scripts. For example, from the repository's Windows PowerShell prompt:

```powershell
rtk proxy wsl.exe -d Ubuntu -- python3 /mnt/c/Users/vinok/git/AK820-git/qmk-8051-ak820/.build/rc6-breathing-arithmetic-probe-20261023/probe.py --out /mnt/c/Users/vinok/git/AK820-git/qmk-8051-ak820/.build/rc6-breathing-arithmetic-probe-20261023-rerun-1
rtk proxy wsl.exe -d Ubuntu -- python3 /mnt/c/Users/vinok/git/AK820-git/qmk-8051-ak820/.build/rc6-breathing-arithmetic-probe-20261023/link_probe.py --out /mnt/c/Users/vinok/git/AK820-git/qmk-8051-ak820/.build/rc6-breathing-arithmetic-probe-20261023-rerun-1 --control-asm-dir /mnt/c/Users/vinok/git/AK820-git/qmk-8051-ak820/.build/rc6-optimized-breathing-20261023/obj_ajazz_ak820_vial --candidate-asm /mnt/c/Users/vinok/git/AK820-git/qmk-8051-ak820/.build/rc6-breathing-arithmetic-probe-20261023-rerun-1/candidate/ak820_rgb.asm
```

The link script also invokes the existing `tests/ak820_breathing/run.py` against the candidate IHX with the bundled uCsim C52 simulator.
