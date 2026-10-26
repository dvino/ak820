Русский перевод: [Профили сборки](ru/BUILD-PROFILES.md).

# Build profiles

The default profile is `main`. See the [profile catalog](profiles/README.md) and [module matrix](MODULE-MATRIX.md) for the ten current compositions. Older compositions remain for development reproduction; historical `typing` is available as `legacy-typing`.

Run commands from the repository root. Each image requires a fresh build directory, pinned SDCC 4.6.0 and a source/IRQ context certificate. Generate the certificate from a fresh seed build and complete IRQ analysis; a certificate from a different composition is rejected when protected modules differ.

```sh
python tools/configure_firmware.py list
python tools/configure_firmware.py build --profile main \
  --build-dir qmk-8051-ak820/.build/main \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python \
  --parameter-spills-context /path/to/reviewed-context.json
```

Current profiles automatically use compressed default keymaps, short calls, ASM NVM read/update and keymap-word kernels, proven parameter/register save removal, tail sharing and outlining. Inspection binds the complete chain to exact sources, tools and image.

Startup, stack bounds and every enabled IRQ of the exact image are checked before full regression suites. Unknown paths or memory overflow block qualification. Offline checks do not prove physical keyboard behavior. See [runtime stack checks](https://github.com/dvino/ak820/blob/v0.6.0-beta.2/docs/RUNTIME-STACK.md) and [Status](STATUS.md).
