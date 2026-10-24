# FULL alpha3 control stack

The exploratory FULL image in `.build/alpha3-full-guards` has a proved
93-byte foreground control-stack bound. Timer, USB and LED callback bounds
are two, six and two bytes. No analyzed root has an unresolved path.
These bounds exclude each root's entry return address.

The IHX SHA256 is
`d505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18`.
The [machine report](guards-runtime-stack.json) records the image, MAP,
relocated listings, analyzer, decoder and private guard source hashes.
[Analyzer test output](guards-tests.log) records 30 passing tests.
The [host transport report](transport-host/results.json) records the ASan/UBSan
checks of startup gating, direct dispatch, 136 transport guards, retry ownership
and reset/suspend cleanup. It is a host model, not a device result.

```sh
python3 qmk-8051-ak820/tests/ak820_stack/analyze.py \
  --build-dir qmk-8051-ak820/.build/alpha3-full-guards \
  --output audits/rc6/alpha3-stack-20261024/guards-runtime-stack.json
python3 -m unittest discover -s qmk-8051-ak820/tests/ak820_stack -v
```

The source keeps every supported feature. AK820 host report dispatch now calls
its fixed CH555 transport directly. The original transport bodies, report
readiness, retry handling, suspend handling and null-driver startup checks
remain. Mutable RAM callback pointers no longer select these calls. A private
bool protects Repeat delivery while its original repeat count remains available
to the event pipeline. The LED selector mask bounds all input byte values.

The analyzer carries the Macro and Repeat ownership flags across function
calls. It proves their complete early-return instruction sequences and their
constant nonzero setters. The source check accepts only the private declaration,
early return, true setter and false reset, once each. All other identifier uses,
including parenthesized address taking and macro arguments, fail closed. Unknown
instruction references discard ownership facts. A callee
that clears an incoming owned state fails the proof. Recursive calls are
analyzed in their actual ownership context; none is replaced by a fixed-depth
allowance or an assumed leaf. Combo source is unchanged: its paths close with
these contexts.

The RGB action callback proof covers the full 16-bit range guard, normalized
index, shifted-key XOR, spill/reload, pointer arithmetic, ROM getter and call
helper. Every selected table entry is read from the checked IHX. The callback
bound includes its call frame and both saved registers. Other const RGB
callbacks use the separate ROM pointer-thunk proof. Tests change guards,
registers, offsets, XOR, spill addresses, setters and helper targets and require
the affected proof to fail closed.

The guard proof assumes valid C memory accesses, private bool objects whose
addresses do not escape, the normal SDCC object layout and bank-0 ABI. It does
not prove safety against arbitrary RAM aliasing or corruption. These are the
same valid-memory and ABI limits as the underlying control-stack analysis.
Startup, interrupt wrappers, nesting and physical behavior need their separate
checks. See [startup review](startup-review.md) and the
[IRQ evidence](../alpha3-irq-20261024/). The machine report deliberately keeps
`whole_program_qualified` false because application control flow alone does not
qualify the whole firmware.

Earlier machine reports `runtime-stack.json` and `mask-runtime-stack.json`
record the earlier source images and their unresolved paths. They do not
represent the current source or the guards image. No firmware was installed
and no USB device was opened for this analysis. Independent proof review is complete: all findings are closed, and the final
`alpha3-release` image reproduces the bounds. Integrated evidence and final
program review are recorded in the [release qualification](../alpha3-release-20261024/review.md).
