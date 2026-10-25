# Getter wrapper bounds prototype

Status: external, unapplied, awaiting independent review. Source commit: `6c2cdc0452b664e37cd32a30b31e3e5f800c49cc` (pass 28). No repository edit, full firmware build, Git write, network request or device operation was performed.

`getter-bounds.patch` forwards the two location getters directly to the existing getters on AK820. Other boards retain the original guarded bodies. Public function names, parameter types, `bool` storage, return values, encoder enable guard and EEPROM layout stay unchanged.

The checks are redundant. Generic C getters reject the same layer/row/column or layer/encoder bounds before calculating an EEPROM address or reading it. The generic definitions are selected unless all four conditions hold: `AK820_KEYMAP_WORDS_ASM`, `AK820_BOARD`, `__SDCC_mcs51`, `__SDCC_MODEL_LARGE`. The assembly replacement is selected exactly when all four hold. Its geometry helper rejects layer >=6, row >=16, column >=8, and encoder index !=0, before either EEPROM call. Compile-time assertions pin 6/16/8, one encoder, key base 0x40, encoder base 0x640 and the large-model ABI. Unsupported ABI options already fail at preprocessing. Removing wrapper checks introduces no new configuration dependency.

The assembly encoder direction uses `jnz`, so every nonzero raw direction byte selects clockwise. The candidate SDCC listing copies the original byte unchanged into the getter argument slot, then tail-jumps. No conversion to a Boolean flag or new helper call is emitted. Generic C retains the existing conditional expression. Invalid coordinates return zero (`KC_NO`) without EEPROM reads; valid requests make the same two reads in the same order. Fault handling inside each EEPROM call is unchanged because no EEPROM operation or argument changes.

## Verification

`prepare.py` extracts both original wrapper bodies and all four generic address/getter bodies from current source. It generates the exact candidate patch and records source SHA256 in `sources.json`. The independent expected-value calculation in `harness.c` derives valid coordinates, addresses and returned bytes without calling either getter. Mock reads record their ordered addresses and reject a third read. Every comparison checks returned value, exact number of reads and both addresses.

Host checks exhaust all 256^3 key triples and all 256^3 layer/encoder/raw-direction triples for each of four cases: AK820 generic C, AK820 assembly instruction translation, unchanged non-AK820 C, and alternate generic geometry 2 layers/3 rows/5 columns/2 encoders. Total: 134,217,728 comparisons. Host direction uses an explicitly documented byte typedef to represent raw ABI values 2..255, which native C `_Bool` cannot represent. The assembly translation is generated instruction by instruction from the actual geometry and read bodies, preserves carry arithmetic and rejects any unknown opcode. It is a host model, not target execution.

`cpu.py` compiles an unchanged copy of the complete actual assembly kernel with SDCC 4.6.0 and the candidate wrappers, links a component fixture, and executes it in s51. It tests 1,536 matrix cases and 137,216 encoder cases. Matrix checks include every valid key and all byte values of each coordinate axis. Encoder checks include every layer/index pair for both canonical directions, plus 6,144 raw direction-byte injections spanning valid and invalid coordinates. Raw bytes enter the actual candidate wrapper through an assembly fixture, then pass through the actual getter and kernel. The mock EEPROM hook is compiled with the required register-preserving ABI. Return values and ordered read/no-read behavior pass. Writes are failure-marked. CPU marker: `a500000000000000`. These are bounded target CPU cases, not an exhaustive 256^3 target CPU run.

The raw assembly fixture is deliberately a separate translation unit: SDCC cannot infer naked assembly clobbers. An initial same-TU fixture failed because its hidden clobbers corrupted caller registers; separating it fixed the fixture. No production source change was required. Compilation warns about unused naked parameters and the mock's intentional generic-pointer-to-logical-address cast. The translation warns that unsigned byte <0 is always false; that is the correct carry result for `CJNE R2,#0`. Production-style `-Os` is ignored by this SDCC and emits a warning; `--opt-code-size` remains active.

`config.py` checks all 16 combinations of the actual C/ASM selection guards and compiles the encoder-disabled key wrapper for both AK820 and generic conditions. The exact patch leaves the outer `ENCODER_MAP_ENABLE` guard in place. Arbitrary alternate dimensions were not exhaustively compiled; generic bounds derive from the same macros in getter and old wrapper, so their equivalence does not depend on fixed dimensions.

Three deliberate mutations fail at the expected first counterexample: invert direction; admit generic layer 6; admit assembly layer 6. The latter two expose an otherwise-invalid EEPROM read after wrapper removal. Results and counterexamples are retained in `mutation-results.json` and `mutations/`.

## Standalone size result

With the retained compiler and component flags, wrapper CSEG is 99 -> 66 bytes: **33 fewer component CODE bytes**. XSEG is 6 -> 6 bytes, DSEG 0 -> 0, BSEG 0 -> 0. This does not establish a whole-image saving. The complete translation unit, linker placement, helpers, spill certificate, final RAM and stack/IRQ limits still require fresh exact-image measurement. The candidate contains no added call; the standalone listing ends both wrappers with `ljmp` to the existing getters.

## Reproduction and limits

From a host where this offline image and repository exist:

```sh
docker run --rm --user 898:898 --network none \
  -v /home/danil/ChatGPT/ak820-pass29-research-20261025/getter-bounds:/out \
  -v /home/danil/ChatGPT/ak820-pass26b-restored-20261025/ak820-max:/repo:ro \
  -w /out ak820-nkro-study-env:local sh run-all.sh
```

Container UID 898 matches this host's rootless Docker mapping; another host must use its matching writable mount UID. Image identity is `sha256:b41196ff4098d5b33786f23238a17ad1fb21b943a588076e085c4881e920d97d`. All output stays in `/out`; the repository mount is read-only. `run-all.sh`, `run-host.sh` and `cpu.py` retain exact compiler and simulator commands. Tool hashes and measured areas are in `results.json`. `SHA256SUMS` covers retained files.

The patch remains a candidate until fresh independent review and integration. No full QMK link, final-image stack/IRQ proof, final certificate regeneration, durable NVM fault injection or physical keyboard behavior is claimed. Invalid no-read behavior and identical valid read order are covered by host and CPU component mocks.
