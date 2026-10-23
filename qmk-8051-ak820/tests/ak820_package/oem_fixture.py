"""Generated OEM-shaped ROMs for offline package tests.

The bytes are synthetic and carry no vendor code. Tests patch the expected
span digests to these fixtures so production validation logic still runs.
"""
from __future__ import annotations

import pack_ak820 as packer
from unittest.mock import patch


def make_synthetic_oem():
    rom = bytearray((offset * 37 + 19) & 0xFF for offset in range(65536))
    rom[0x27C0:0x27C4] = bytes.fromhex("aa5533cc")
    rom[0xA040] = 0
    rom = bytes(rom)
    application = rom[packer.APP_START:packer.APP_END]
    protected_sha = packer.digest(rom[:0x27C0] + rom[packer.APP_END:])
    factory_sha = packer.digest(rom[packer.APP_START:0xA000] + rom[0xD200:packer.APP_END])
    return rom, application, protected_sha, factory_sha


def patch_synthetic_oem(stack, updater, rom):
    application = rom[packer.APP_START:packer.APP_END]
    protected_sha = packer.digest(rom[:0x27C0] + rom[packer.APP_END:])
    factory_sha = packer.digest(rom[packer.APP_START:0xA000] + rom[0xD200:packer.APP_END])
    patches = (
        (packer, "STOCK_SHA", packer.digest(rom)),
        (updater, "STOCK_SHA", packer.digest(rom)),
        (packer, "NATIVE_SHA", packer.digest(application)),
        (packer, "PROTECTED_SHA", protected_sha),
        (packer, "FACTORY_CODE_SHA", factory_sha),
        (packer, "PATCHED_CODE_SHA", packer.digest(b"unreachable synthetic alternate")),
    )
    for module, name, value in patches:
        stack.enter_context(patch.object(module, name, value))
    return application
