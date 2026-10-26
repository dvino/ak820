#!/usr/bin/env python3
"""Check linked VialRGB conversion and supported-mode replies in C52 simulation."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--build-dir', type=Path, required=True)
parser.add_argument('--s51', type=Path, required=True)
parser.add_argument('--output-dir', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('support', root / 'qmk-8051-ak820/tests/ak820_emitted/run.py')
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)
fw = support.Firmware(args.build_dir.resolve(), args.s51.resolve(), args.output_dir.resolve())
commands = fw.initialize()
observations = []
report = json.loads((args.build_dir / 'build-report.json').read_text())
configuration = report.get('configuration', {})
# The configuration is independently checked against defines by qualification.
no_direct = 'vialrgb-direct' not in configuration.get('optional_features', [])
vial_ids = [0, 2, 6, 13, 14, 31] if no_direct else [0, 2, 6, 13, 14, 1, 31]
expected_table = [0,0,2,1,6,2,13,3,14,4,31,5] if no_direct else [0,0,1,5,2,1,6,2,13,3,14,4,31,6]
assert [fw.code[fw.address('_supported_modes') + i] for i in range(len(expected_table))] == expected_table
for value in list(range(256)) + [256, 257, 511, 0xff00, 0xffff]:
    for symbol, expected in [('_qmk_id_to_vialrgb_id', vial_ids[value] if value < len(vial_ids) else 0),
                             ('_vialrgb_id_to_qmk_id', vial_ids.index(value) if value in vial_ids else 0)]:
        label = f'{symbol}_{value}_END'
        commands += fw.call(symbol, value) + fw.dump(label, 'sfr', 0x82, 2)
        observations.append((label, 'sfr', 0x82, [expected, 0]))
packet = fw.address('_raw_buffer')
for threshold in [0,1,2,5,6,12,13,14,30,31,32,255,256,257,65535]:
    for length in range(31):
        data = [threshold & 255, threshold >> 8] + [0xa5] * 30
        expected = data[:]
        expected[:length] = [255] * length
        at = 0
        for value in sorted(vial_ids):
            if value > threshold and length - at >= 2:
                expected[at:at+2] = [value, 0]
                at += 2
        label = f'supported_{threshold}_{length}_END'
        commands += [support.memory('xram', packet, data)]
        commands += fw.write('_get_supported_PARM_2', [length])
        commands += fw.call('_get_supported', packet) + fw.dump(label, 'xram', packet, 32)
        observations.append((label, 'xram', packet, expected))
log, stack = fw.execute('vialrgb-mode-boundaries', commands)
for label, space, address, expected in observations:
    actual = fw.extract(log, label, address, len(expected))
    assert actual == expected, (label, actual, expected)
report = {'pass': True, 'cases': len(observations), 'conversion_ids_per_direction': 261,
          'supported_requests': 15 * 31, 'linked_table_bytes': expected_table,
          'ihx_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(), **stack,
          'limits': 'Linked C52 CPU fixtures and simulated memory; no USB controller timing, interrupt nesting, physical device or whole-program stack proof.'}
(args.output_dir / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
