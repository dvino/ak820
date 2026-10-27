# Exact HSV conversion kernel

`cpu.py` compiles the production color source and the immutable RC4 portable
reference with SDCC, then compares their results in the generic 8051 simulator.
The reference uses a typed output pointer to avoid an SDCC aggregate-return
issue in the BGR layout; its HSV arithmetic is unchanged. CIE correction uses
the production table before the reference conversion. The command requires
absolute compiler, simulator and output paths:

```sh
python3 tests/ak820_color_kernel/cpu.py \
  --sdcc /absolute/path/to/sdcc \
  --simulator /absolute/path/to/s51 \
  --output /absolute/path/to/new-output-directory
```

Both compact and full CIE curves use the production GRB byte order. Each mode
covers all 256 hue and saturation values at eleven value boundaries, then all
hue and value combinations with saturation zero and 255, with CIE enabled and
disabled. The final pass checks every hue with output beginning one byte before, at,
or one byte after the input. RGB and BGR layouts have
smaller representative passes. A mismatch stops at a dedicated CPU breakpoint;
the runner requires the success marker and retains the simulator log and image
hashes. These are component CPU checks, without hardware access. They do not
qualify firmware startup, interrupt handling or the linked stack bound.

The kernel reads the complete input before writing any output. It uses the
large-model typed XDATA ABI, caller-saved registers and native unsigned MUL.
The region calculation preserves hue 255 as region six. Only the ramp needed
by the selected region is calculated; its products and byte truncations are
identical to the portable algorithm. The portable implementation remains the
fallback for other targets.

## Breathing waveform

`waveform.py` uses the same command arguments. It extracts the production
native leaf and portable fallback, compiles both, and compares every phase in
s51 and against an independent integer calculation. The eight coefficients
remain in the CODE section after RET. The first MOVC index is 0, 2, 4 or 6;
the second index adds one. No execution path falls through into the table.
The test preserves the CPU log, all 256 results and exact source/image hashes.

## Slot writer

`slots.py` uses the same command arguments. It compiles the production slot
writer with the native DMA base and interrupt-bit addresses, then checks 8,192
cases in s51: every slot byte, both LED interrupt states, the other IE_EX bits
clear and set, and eight black/component/edge colors. Each case verifies all
512 DMA bytes and the adjacent guard bytes. Slots 128–255 must leave the entire
buffer unchanged. Valid slots use intensity zero for black and 255 otherwise,
followed by red, green and blue. The complete IE_EX byte must be preserved.
The test also checks that the masked write interval contains no instruction
that changes carry. This does not simulate interrupt preemption or establish
peripheral timing on a device.
