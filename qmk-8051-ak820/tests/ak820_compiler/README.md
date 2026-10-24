# Check SDCC Boolean stores

These tests run offline. They never open USB or change the keyboard.
`run.py` builds a small program with the selected compiler, runs it in the
uCsim C52 CPU model, and checks both false and true stores. It covers typed
near and XDATA pointers, generic pointers to both spaces, a comparison return,
the current key-record field order, a Boolean parameter and a bitfield with
neighbouring bits. The current key record has no tap field; its configuration
defines `NO_ACTION_TAPPING`. The separate tap bitfield is a compiler test.

From the repository root in Ubuntu:

```sh
python3 qmk-8051-ak820/tests/ak820_compiler/run.py \
  --sdcc toolchains/sdcc-4.4.0/bin/sdcc \
  --s51 toolchains/sdcc-4.4.0/bin/s51 \
  --output qmk-8051-ak820/.build/compiler-check-new
```

The output directory must be new. `--extra-flag=VALUE` appends one compiler
argument; repeat it for a flag and its value. The fixed base flags are
`-mmcs51 --std-sdcc11 --model-large --opt-code-size`. The report records the
command, compiler version and hash, fixture hash and every result. A compiler
failure, CPU timeout, missing completion marker or wrong byte fails the run.
The runner deliberately fails when the selected compiler has bug 3845.

`linked.py` tests an existing linked AK820 image without building it:

```sh
python3 qmk-8051-ak820/tests/ak820_compiler/linked.py \
  --build qmk-8051-ak820/.build/rc6-sdcc46-full-experiment-20261023 \
  --s51 toolchains/sdcc-4.4.0/bin/s51 \
  --output qmk-8051-ak820/.build/compiler-linked-check-new
```

It executes the retained matrix path for press and release, then checks the
event object and the action record. It also executes both encoder mapping
directions and stops at the shared action wrapper for each press and release.
The single encoder event buffer is checked before each call. A later simulated
clock value between calls checks that release reads a fresh timestamp. Static
symbols come from relocated listings; missing or ambiguous buffers fail.
This runner imports the existing `ak820_emitted` CPU harness and uses its
simulated matrix, USB and NVM setup. Its report identifies the exact IHX hash.
The CPU model does not prove physical keys, encoder wiring, USB timing,
durable flash storage or installed firmware. These are narrow checks of the
executed code, not a compiler-wide or firmware-wide correctness certificate.
