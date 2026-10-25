# Getter bounds regression

Run `python3 tests/ak820_getter_bounds/run.py` from the repository root. The check is offline. It needs Python 3 and a host `gcc` or `cc`, or Docker with the `ak820-nkro-study-env:local` image. The runner selects a host compiler first, then checks the local image and runs it with networking disabled. If neither compiler path works, the run fails.

The runner reads the current getter wrappers, generic getters, AK820 assembly kernel and board dimensions. Its reference wrappers come from Git commit `6c2cdc0452b664e37cd32a30b31e3e5f800c49cc`. It exhausts every byte value for each layer, row or encoder, column and raw direction byte across four configurations. Each case compares the returned keycode, EEPROM read count and ordered read addresses with an independent expectation. Three deliberate faults must fail. The AK820 assembly case runs an instruction-by-instruction host translation of the current geometry and read routines; it does not execute on an 8051.

The runner records source hashes and results as JSON Lines in `getter29-host-regression.jsonl` in the repository parent directory. These host results do not prove a firmware build, device behavior, or durable EEPROM fault handling.

## Linked CPU check

The installed `linked.py` is an exact copy of the retained CPU runner. It needs
the linked build artifacts and the bundled `s51` simulator. From the repository
root, a new single-process run can write to a separate output directory:

```sh
python3 tests/ak820_getter_bounds/linked.py \
  --repo "$PWD" \
  --build "$PWD/qmk-8051-ak820/.build/resume29-getter-bounds" \
  --output /tmp/ak820-getter-cpu
```

The recorded pass 29 proof ran eight disjoint shards. Its original runner,
`run.sh`, `inside.sh`, external `aggregate.py`, raw logs, per-shard reports and
SHA256 manifest remain at
`/home/danil/ChatGPT/ak820-pass29-research-20261025/linked-getters`.
That directory's README records the exact reproduction commands. The external
aggregate uses that directory's `final/shard-*` paths; it is not installed as a
portable repository command. The audit preserves the original container paths
in the evidence and checks their actual host counterparts.

The final CPU proof covers 2,431 cases: all 768 valid matrix locations, 15
invalid matrix boundaries, 1,536 valid encoder cases including every raw
direction byte, and 112 invalid encoder samples. It executes the actual linked
wrappers, getters, assembly address routines and EEPROM reader with one primed
cache page per call. Returns, ordered reads, cache bytes/flags, SP and canaries
are checked. The raw logs also prove generic-pointer B is zero at all 4,608
reader entries. All 44,601 occupied CODE bytes match the IHX before and after
each shard. Flash/write entry points have stopguards. Only empty trampoline
space at `0x2600..0x26ff` receives simulated CODE writes.

This is a C52 CPU model. It does not cover new read faults, dirty cross-page
cache transitions, durable storage, IRQs, peripherals or physical behavior.
CRT runs only to main entry; main, NVM initialization and ROM seeding do not run.
No device is opened. Whole-image stack/IRQ and hardware acceptance remain
separate gates. Earlier failed or interrupted attempts remain in the external
directory and do not qualify the image.
