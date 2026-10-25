# Register-preserving NVM reads

Run in the offline build environment:

```sh
python3 tests/ak820_nvm_readasm/run.py --toolchain /toolchains/sdcc-4.6.0 --output /tmp/nvm-read-check
```

The fixture includes the production NVM source and its CRC implementation. SDCC
and s51 execute both scalar entries across 82688 cases each: every 16-bit offset,
all cache-page indices and byte positions, mismatched pages and all pointer tags.
Register canaries, SP and register-bank bits are checked around each entry.
Another 216 calls exercise the compiled generic and XDATA block readers, with
IDATA/XDATA outputs, boundaries, zero lengths and output canaries.

The CODE fixture differs from cached bytes. Flash writes are forbidden stubs.
A fresh map resolves the terminal breakpoint; a missing success marker or timeout
fails. Result JSON binds the source, test, tools and fixture image hashes.

This is a component CPU check. The exact production image includes outlining and
needs separate ABI, startup, IRQ, stack and resource qualification. No USB or
physical keyboard is accessed.
