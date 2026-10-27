"""Strict offline codec for schema 0x082003 compact module storage."""
import binascii
import json
import struct

SCHEMA = 0x082003
SETTINGS_ADDR = 0x6A8
FIELDS = {1: (5, 1, 0, 15, 0), 2: (6, 2, 1, 1000, 40),
          4: (14, 2, 1, 1000, 175), 7: (8, 2, 1, 1000, 200),
          18: (10, 2, 0, 100, 0), 19: (12, 2, 0, 100, 80)}

LEGACY_FIELDS = dict(FIELDS)
FIELDS.update({3: (16, 1, 0, 29, 1), 6: (18, 2, 0, 30000, 0), 22: (17, 1, 0, 1, 0)})

def require(ok, message):
    if not ok:
        raise ValueError(message)


def field_value(qsid, value):
    require(type(qsid) is int and qsid in FIELDS, 'Unknown settings ID')
    _, width, low, high, _ = FIELDS[qsid]
    require(type(value) is int and low <= value <= high and (qsid != 3 or not value & ~0x1d), 'Settings value out of range')
    return value.to_bytes(width, 'little')


def settings_record(values=None, *, version=2):
    require(type(version) is int and version in (1, 2), 'Unknown settings version')
    fields = LEGACY_FIELDS if version == 1 else FIELDS
    values = values if values is not None else {str(i): f[4] for i, f in fields.items()}
    require(isinstance(values, dict) and set(values) == {str(i) for i in fields}, 'Missing or unknown settings field')
    raw = bytearray((b'QS\x01\x0b\x3f' if version == 1 else b'QS\x02\x0f\x7f') + bytes(19))
    for qsid, (offset, width, _, _, _) in fields.items():
        raw[offset:offset+width] = field_value(qsid, values[str(qsid)])
    raw[22:] = binascii.crc_hqx(raw[:22], 0xFFFF).to_bytes(2, 'little')
    return bytes(raw)


def normalize_settings(values, *, version=2):
    require(type(values) is dict, 'Invalid settings fields')
    source = 1 if set(values) == {str(i) for i in LEGACY_FIELDS} else 2
    settings_record(values, version=source)
    require(type(version) is int and version in (1, 2) and source <= version, 'Settings record downgrade is forbidden')
    return {str(i): values.get(str(i), f[4]) for i, f in (LEGACY_FIELDS if version == 1 else FIELDS).items()}


def decode_settings(raw, *, version=None):
    require(type(raw) is bytes and len(raw) == 24, 'Settings record requires 24 bytes')
    if raw in (bytes(24), b'\xff'*24):
        raw = settings_record(version=version or 2)
    source = raw[2]
    require(source in (1, 2), 'Unknown settings record version')
    fields = LEGACY_FIELDS if source == 1 else FIELDS
    values = {str(i): int.from_bytes(raw[o:o+w], 'little') for i, (o,w,*_) in fields.items()}
    require(raw == settings_record(values, version=source), 'Invalid settings header, reserved bytes or CRC')
    return normalize_settings(values, version=version) if version is not None else values


def slot_offset(kind, index):
    require(kind in ('tap_dance', 'key_overrides'), 'Unknown extension kind')
    require(type(index) is int and 0 <= index < 8, 'Invalid extension index')
    return (0x6C0 if kind == 'tap_dance' else 0x740) + (index*10 if index < 6 else 64+(index-6)*10)


def output_valid(value, modifiers=True):
    return value == 0 or (0 <= value < 0x2000 and (4 <= (value & 255) <= 0xA4 or
                              (modifiers and 0xE0 <= (value & 255) <= 0xE7)))


def validate_entry(kind, raw):
    require(type(raw) is bytes and len(raw) == 10, 'Extension entry requires ten bytes')
    require(kind in ('tap_dance', 'key_overrides'), 'Unknown extension kind')
    if kind == 'tap_dance':
        *outputs, term = struct.unpack('<5H', raw)
        require(all(output_valid(v) for v in outputs) and term <= 32767, 'Invalid Tap Dance output or term')
    elif raw != bytes(10):
        trigger, replacement, layers, mods, negative, suppressed, options = struct.unpack('<HHHBBBB', raw)
        require(4 <= trigger <= 0xA4 and output_valid(replacement, False) and 1 <= layers <= 63
                and not options & 0x40 and options & 7, 'Invalid Key Override entry')
    return raw


def from_nvm(nvm, *, version=None):
    require(len(nvm) == 0x2800 and nvm[37:40] == SCHEMA.to_bytes(3, 'little'), 'Extension schema differs')
    result = {'version': 1, 'qmk_settings': decode_settings(bytes(nvm[SETTINGS_ADDR:SETTINGS_ADDR+24]), version=version)}
    for kind in ('tap_dance', 'key_overrides'):
        result[kind] = [validate_entry(kind, bytes(nvm[slot_offset(kind,i):slot_offset(kind,i)+10])).hex() for i in range(8)]
    return result


def validate_json(value):
    require(type(value) is dict and set(value) == {'version', 'qmk_settings', 'tap_dance', 'key_overrides'}
            and type(value['version']) is int and value['version'] == 1, 'Unknown extension JSON fields/version')
    require(type(value['qmk_settings']) is dict, 'Invalid settings fields')
    settings_record(value['qmk_settings'], version=1 if set(value['qmk_settings']) == {str(i) for i in LEGACY_FIELDS} else 2)
    for kind in ('tap_dance', 'key_overrides'):
        require(type(value[kind]) is list and len(value[kind]) == 8, 'Extension requires eight entries')
        for entry in value[kind]:
            require(type(entry) is str and len(entry) == 20, 'Invalid entry hex')
            require(validate_entry(kind, bytes.fromhex(entry)).hex() == entry, 'Noncanonical entry hex')
    return value


def loads(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON field')
            result[key] = value
        return result
    return validate_json(json.loads(raw, object_pairs_hook=pairs))
