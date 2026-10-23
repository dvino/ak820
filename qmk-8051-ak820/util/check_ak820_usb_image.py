#!/usr/bin/env python3
"""Check AK820 USB descriptors in a linked SDCC IHX/map, without USB access.

This checks emitted bytes, independently of host C packing/wchar_t behavior.
It does not validate SIE timing, interrupt execution, or physical enumeration.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_ihex(path):
    image, base, ended = {}, 0, False
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        require(not ended and line.startswith(':'), f'IHX line {line_number}: invalid record position')
        record = bytes.fromhex(line[1:])
        require(len(record) >= 5 and len(record) == record[0] + 5 and sum(record) % 256 == 0,
                f'IHX line {line_number}: invalid size/checksum')
        address = int.from_bytes(record[1:3], 'big')
        kind, data = record[3], record[4:-1]
        if kind == 0:
            for offset, value in enumerate(data):
                location = base + address + offset
                require(location <= 0xffff and location not in image,
                        f'IHX line {line_number}: duplicate/out-of-range code byte')
                image[location] = value
        elif kind == 1:
            require(not data and address == 0, 'invalid IHX EOF')
            ended = True
        elif kind in (2, 4):
            require(len(data) == 2 and address == 0, 'invalid IHX extended address')
            base = int.from_bytes(data, 'big') << (4 if kind == 2 else 16)
        elif kind in (3, 5):
            require(len(data) == 4 and address == 0, 'invalid IHX start address')
        else:
            raise ValueError(f'unsupported IHX record type {kind}')
    require(ended, 'IHX EOF missing')
    return image


def read_symbols(path):
    symbols = {}
    for match in re.finditer(r'^C:\s+([0-9A-Fa-f]+)\s+_(\w+)\s+usb_descriptor\s*$',
                             path.read_text(), re.MULTILINE):
        require(match[2] not in symbols, f'duplicate map symbol {match[2]}')
        symbols[match[2]] = int(match[1], 16)
    require(symbols, 'no USB descriptor CODE symbols in SDCC map')
    return symbols


def hid_bits(data):
    """Accumulate main-item bits per report ID, including constant padding."""
    size = count = report_id = depth = position = 0
    stack, result = [], defaultdict(int)
    while position < len(data):
        prefix = data[position]
        position += 1
        require(prefix != 0xfe, 'unexpected long HID item')
        length = (0, 1, 2, 4)[prefix & 3]
        require(position + length <= len(data), 'truncated HID item')
        value = int.from_bytes(data[position:position + length], 'little')
        position += length
        kind, tag = (prefix >> 2) & 3, prefix >> 4
        if kind == 1:
            if tag == 7:
                size = value
            elif tag == 8:
                require(0 < value <= 255, 'invalid HID report ID')
                report_id = value
            elif tag == 9:
                count = value
            elif tag == 10:
                stack.append((size, count, report_id))
            elif tag == 11:
                require(stack, 'HID global stack underflow')
                size, count, report_id = stack.pop()
        elif kind == 0:
            if tag in (8, 9, 11):
                require(size and count and depth, 'HID data item without size/count/collection')
                result[(tag, report_id)] += size * count
            elif tag == 10:
                depth += 1
            elif tag == 12:
                require(depth, 'HID collection underflow')
                depth -= 1
    require(not stack and not depth, 'unbalanced HID descriptor')
    return dict(result)


def validate(ihx, map_path, info, serial, with_mouse=False):
    image, symbols = read_ihex(ihx), read_symbols(map_path)

    def read(address, length):
        require(length > 0 and all(address + i in image for i in range(length)),
                f'missing emitted code bytes at 0x{address:04x}, length {length}')
        return bytes(image[address + i] for i in range(length))

    def address(name):
        require(name in symbols, f'missing map symbol {name}')
        return symbols[name]

    def obj(name, length):
        return read(address(name), length)

    def le16(data, offset):
        return int.from_bytes(data[offset:offset + 2], 'little')

    device = obj('DeviceDescriptor', 18)
    require(device[:8] == bytes.fromhex('12 01 00 02 00 00 00 40'), 'invalid USB device header/EP0 size')
    require(le16(device, 8) == int(info['usb']['vid'], 0) and
            le16(device, 10) == int(info['usb']['pid'], 0), 'USB VID/PID differs from board info')
    require(device[12:] == bytes.fromhex('00 01 01 02 03 01'), 'invalid device revision/string indexes/configuration count')

    config_header = obj('ConfigurationDescriptor', 9)
    require(config_header == bytes.fromhex('09 02 54 00 03 01 00 a0 fa'), 'invalid AK820 configuration header')
    configuration = obj('ConfigurationDescriptor', le16(config_header, 2))
    interfaces, hid_lengths, endpoints = {}, {}, {}
    current, offset = None, 9
    while offset < len(configuration):
        length, kind = configuration[offset:offset + 2]
        require(length >= 2 and offset + length <= len(configuration), 'invalid nested descriptor length')
        data = configuration[offset:offset + length]
        if kind == 4:
            require(length == 9 and data[2] not in interfaces, 'invalid/duplicate interface')
            current = data[2]
            interfaces[current] = data
        elif kind == 0x21:
            require(current is not None and current not in hid_lengths and
                    length == 9 and data[:7] == bytes.fromhex('09 21 11 01 00 01 22'), 'invalid HID descriptor')
            hid_lengths[current] = le16(data, 7)
        elif kind == 5:
            require(current is not None and current not in endpoints and length == 7, 'invalid/duplicate endpoint')
            endpoints[current] = data
        else:
            raise ValueError(f'unexpected configuration descriptor type {kind}')
        offset += length
    require(set(interfaces) == set(hid_lengths) == set(endpoints) == {0, 1, 2}, 'interface/HID/endpoint mismatch')
    reports = {}
    expected_bits = {
        'Keyboard': {(8, 0): 64, (9, 0): 8},
        'Raw': {(8, 0): 256, (9, 0): 256, (11, 0): 64},
        'Shared': {(8, 3): 16, (8, 4): 16, (8, 6): 248, (9, 6): 8},
    }
    if with_mouse:
        expected_bits['Shared'][(8, 2)] = 40
    for interface, name, ep, packet_size in ((0, 'Keyboard', 0x81, 8), (1, 'Raw', 0x83, 32), (2, 'Shared', 0x82, 32)):
        boot = 1 if interface == 0 else 0
        require(interfaces[interface] == bytes((9, 4, interface, 0, 1, 3, boot, boot, 0)),
                f'{name}: invalid interface fields')
        require(endpoints[interface] == bytes((7, 5, ep, 3, packet_size, 0, 1)),
                f'{name}: invalid endpoint address/size/attributes')
        length = obj(name + 'Report_size', 1)[0]
        require(length == hid_lengths[interface], f'{name}: HID length differs from emitted report size')
        require(address(name + 'Report_size') == address(name + 'Report') + length,
                f'{name}: emitted report extent differs from declared size')
        bits = hid_bits(obj(name + 'Report', length))
        require(bits == expected_bits[name], f'{name}: report IDs/bit lengths differ: {bits}')
        require(all((bit_count + 7) // 8 + bool(report_id) <= packet_size
                    for (_, report_id), bit_count in bits.items()), f'{name}: report exceeds endpoint size')
        reports[name] = {'length': length, 'endpoint': hex(ep), 'packet_size': packet_size,
                         'bits': {f'{tag}:{report_id}': count for (tag, report_id), count in bits.items()}}

    require(obj('LanguageString', 4) == bytes.fromhex('04 03 09 04'), 'invalid language descriptor')
    strings, errors = {}, []
    for name, text in (('Manufacturer', info['manufacturer']), ('Product', info['keyboard_name']), ('SerialNumber', serial)):
        length, kind = obj(name + 'String', 2)
        require(kind == 3 and length >= 2 and length % 2 == 0, f'{name}: invalid USB string header')
        data = obj(name + 'String', length)
        actual = data[2:].decode('utf-16le')
        expected = text.encode('utf-16le')
        strings[name] = {'length': length, 'text': actual}
        if data != bytes((2 + len(expected), 3)) + expected:
            errors.append(f'{name}: got length {length}, text {actual!r}; expected length {2 + len(expected)}, text {text!r}')
    require(not errors, '; '.join(errors))
    return {'status': 'PASS', 'image_sha256': hashlib.sha256(ihx.read_bytes()).hexdigest(),
            'device_length': len(device), 'configuration_length': len(configuration),
            'reports': reports, 'strings': strings,
            'scope': 'emitted SDCC descriptor bytes only; no SIE/device validation'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ihx', type=Path)
    parser.add_argument('map', type=Path)
    parser.add_argument('--info', type=Path, default=Path(__file__).resolve().parents[1] / 'keyboards/ajazz/ak820/info.json')
    parser.add_argument('--serial', default='vial:f64c2b3c')
    parser.add_argument('--with-mouse', action='store_true')
    args = parser.parse_args()
    try:
        result = validate(args.ihx, args.map, json.loads(args.info.read_text()), args.serial, args.with_mouse)
    except (OSError, ValueError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
