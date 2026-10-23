# AK820 firmware source

This directory contains the maintained QMK/Vial-based source for the wired AJAZZ AK820. Only ajazz/ak820:vial is supported.

Use the build, installation and test instructions in the repository documentation:

- [Build](../docs/BUILD.md)
- [Status](../docs/STATUS.md)
- [Testing](../docs/TESTING.md)
- [Board source](keyboards/ajazz/ak820/readme.md)

The source includes AK820-specific platform, USB, storage and lighting changes. Do not replace it with an unmodified upstream QMK archive. Upstream provenance is recorded in util/ak820-source-provenance.json. Existing copyright and license notices apply to their respective files.

Compiler toolchains and downloaded libraries are external build dependencies. Generated files and personal device backups do not belong in Git. A successful build does not prove device behavior or authorize flashing.
