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
supported_requests = 0
for threshold in [0,1,2,5,6,12,13,14,30,31,32,255,256,257,65535]:
    # Exercise the public fixed-packet handler, including malformed lengths.
    # The generic helper's arbitrary-length behavior remains covered by host.py.
    for length in [*range(33), 33, 255]:
        data = [8, 0x42, threshold & 255, threshold >> 8] + [0xa5] * 28
        expected = data[:]
        if length == 32:
            expected[2:] = [255] * 30
            at = 2
            for value in sorted(vial_ids):
                if value > threshold:
                    expected[at:at+2] = [value, 0]
                    at += 2
        label = f'supported_{threshold}_{length}_END'
        commands += [support.memory('xram', packet, data)]
        commands += fw.write('_vialrgb_get_value_PARM_2', [length])
        commands += fw.call('_vialrgb_get_value', packet) + fw.dump(label, 'xram', packet, 32)
        observations.append((label, 'xram', packet, expected))
        supported_requests += 1
foreign = 0x3f00
data = [8, 0x42, 0, 0] + [0xa5] * 28
commands += [support.memory('xram', foreign, data)]
commands += fw.write('_vialrgb_get_value_PARM_2', [32]) + fw.call('_vialrgb_get_value', foreign)
commands += fw.dump('supported_foreign_END', 'xram', foreign, 32)
observations.append(('supported_foreign_END', 'xram', foreign, data))
log, stack = fw.execute('vialrgb-mode-boundaries', commands)
for label, space, address, expected in observations:
    actual = fw.extract(log, label, address, len(expected))
    assert actual == expected, (label, actual, expected)
direct_spec = importlib.util.spec_from_file_location('direct_cpu', Path(__file__).with_name('direct.py'))
direct_cpu = importlib.util.module_from_spec(direct_spec)
direct_spec.loader.exec_module(direct_cpu)
direct_report = direct_cpu.run(fw, support)
assert direct_report['available'] == (not no_direct), 'Direct feature/entry-point mismatch'
report = {'direct_v1': direct_report, 'pass': direct_report['pass'], 'cases': len(observations), 'conversion_ids_per_direction': 261,
          'supported_requests': supported_requests, 'foreign_buffer_rejected': True, 'linked_table_bytes': expected_table,
          'ihx_sha256': hashlib.sha256(fw.image.read_bytes()).hexdigest(), **stack,
          'limits': 'Linked C52 CPU fixtures and simulated memory; no USB controller timing, interrupt nesting, physical device or whole-program stack proof.'}
(args.output_dir / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
