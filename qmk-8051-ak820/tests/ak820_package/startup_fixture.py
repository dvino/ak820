"""Tiny structurally valid linked startup fixture for updater-only tests.

These tests exercise package provenance, not CPU execution. The independent
tests/ak820_startup runner executes the real SDCC output against a copy oracle.
"""


def add_startup_fixture(data, symbols):
    symbols.update({'__mcs51_genXINIT': 0x3040, 's_GSINIT3': 0x3040,
                    'l_GSINIT3': 44, 's_XINIT': 0x30c0, 'l_XINIT': 1,
                    's_XISEG': 0x0a00, 'l_XISEG': 1,
                    's_XSEG': 0x0400, 'l_XSEG': 0x0600, 'l_PSEG': 0})
    code = bytes.fromhex('7901e9440060257a017bc07c307d007e0a'
                         '8b828c83e493ffa3ab82ac838d828e83eff0a3ad82ae83d9e7dae5')
    assert len(code) == 44
    data.update(enumerate(code, 0x3040))
    data[0x30c0] = 1
