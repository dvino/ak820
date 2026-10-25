# Word access ABI policy

Run the pure builder policy checks without a compiler or device:

```
python3 qmk-8051-ak820/tests/ak820_word_kernel/policy.py
```

The test loads the actual builder helper AST. It checks that both audited scalar
EEPROM hooks are required for the register-preservation assertion, that the four
word APIs remain caller-clobbered, and that incompatible ABI flags or a manual
assertion are rejected. These checks do not establish the actual hook machine
code or whole-image register/stack behavior.

The experimental kernel is selected explicitly with `--keymap-words-asm` in
`util/build_ak820.py`. The compile command records an explicit yes/no Make option
and the build report records the selection. The default is no. Pinning the
compiler/model, preserving the common audited ABI, a separate kernel translation
unit, component differential tests and exact linked-image checks remain required.
Current component and complete-image limits are recorded in
[optimization status](../../../docs/MAXIMUM-FUNCTIONALITY-STATUS.md).
