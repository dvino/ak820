#!/usr/bin/env python3
"""Check every outlined helper and call against its exact pre-outline bytes.

This is a relocation and image-integrity check. It does not execute the CPU
model, prove a stack bound or approve firmware installation.
"""
import argparse
import hashlib
import json
from pathlib import Path

from outline import Firmware, integrity


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--s51', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    build = args.build_dir.resolve()
    manifest_path = build / 'dce/outlining.json'
    manifest = json.loads(manifest_path.read_text())
    firmware = Firmware(build, args.s51.resolve(), args.output_dir.resolve())
    helpers = integrity(firmware, build / 'dce-input', manifest, '.lst')
    expected = {helper['name'] for helper in helpers}
    actual = {name for name in firmware.symbols if name.startswith('_ak820_outline_')}
    if actual != expected:
        raise ValueError('Linked outline helper set differs from the manifest')
    report = {
        'pass': True,
        'linked_image_sha256': hashlib.sha256(firmware.image.read_bytes()).hexdigest(),
        'outline_manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        'verified_helpers': len(helpers),
        'verified_replacements': sum(helper['sites'] for helper in helpers),
        'nominal_net_bytes': sum(helper['saving'] for helper in helpers),
        'cpu_executed': False,
        'hardware_validated': False,
        'physical_device_commands': 0,
        'limits': 'Exact helper bodies, immediate relocations, replacement counts and input hashes only; '
                  'no CPU execution, stack bound or physical behavior qualification.',
    }
    (firmware.output / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
