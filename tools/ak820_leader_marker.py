"""Strict linked Leader-default marker inspection; not release authorization.

The caller must independently authenticate the map, IHX, packed image and build.
"""
import re

SYMBOL = '_ak820_leader_default_marker'
PREFIX = b'AKL\x01'
WINDOWS = ((0x28a0, 0x3000), (0x3027, 0xc700))
APP_START = 0x2800
CODE_END = 0xc700


def _linked(map_text, code):
    if not isinstance(map_text, str) or type(code) is not dict:
        raise ValueError('Invalid Leader marker evidence')
    records = []
    symbols = []
    for line in map_text.splitlines():
        if re.search(r'(?<!\S)' + re.escape(SYMBOL) + r'(?!\S)', line):
            match = re.fullmatch(r'C:[ \t]+([0-9A-Fa-f]{8})[ \t]+' + re.escape(SYMBOL) + r'(?:[ \t]+\S+)?[ \t]*', line)
            if not match:
                raise ValueError('Malformed Leader marker symbol')
            records.append(int(match.group(1), 16))
        match = re.fullmatch(r'C:[ \t]+([0-9A-Fa-f]{8})[ \t]+(_\S+)(?:[ \t]+\S+)?[ \t]*', line)
        if match:
            symbols.append((int(match.group(1), 16), match.group(2)))
    if len(records) != 1:
        raise ValueError('Missing or duplicate Leader marker symbol')
    address = records[0]
    if not any(lo <= address and address + 6 <= hi for lo, hi in WINDOWS):
        raise ValueError('Leader marker outside linked CODE')
    if any(address <= pos < address + 6 and name != SYMBOL for pos, name in symbols):
        raise ValueError('Leader marker overlaps another CODE symbol')
    if any(type(pos) is not int or type(value) is not int or not 0 <= value <= 255 or
           not any(lo <= pos < hi for lo, hi in WINDOWS) for pos, value in code.items()):
        raise ValueError('Invalid linked CODE')
    try:
        marker = bytes(code[address + i] for i in range(6))
    except KeyError as error:
        raise ValueError('Incomplete Leader marker') from error
    if marker[:4] != PREFIX:
        raise ValueError('Invalid Leader marker format')
    value = int.from_bytes(marker[4:], 'little')
    if not 1 <= value <= 1000:
        raise ValueError('Invalid Leader marker value')
    occurrences = [pos for pos in code if all(code.get(pos + i) == byte for i, byte in enumerate(PREFIX))]
    if occurrences != [address]:
        raise ValueError('Missing or duplicate Leader marker discriminator')
    return address, marker, {'format': 'ak820-leader-default-1', 'milliseconds': value}


def extract_linked(map_text, code):
    """Inspect final linked CODE only; this is not packed-image authorization."""
    return _linked(map_text, code)[2]


def extract(map_text, code, packed_code):
    """Read the six-byte v1 marker from linked CODE and packed application CODE."""
    if type(packed_code) is not bytes or len(packed_code) != CODE_END - APP_START:
        raise ValueError('Invalid packed CODE length')
    address, marker, result = _linked(map_text, code)
    if packed_code[address - APP_START:address - APP_START + 6] != marker:
        raise ValueError('Packed Leader marker differs from linked CODE')
    return result
