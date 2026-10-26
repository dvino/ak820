#!/usr/bin/env python3
"""Create a new trial session entirely from local files; never opens USB.

The original native recovery session is read-only. No permanent image is
created. For an existing trial, require its exact image and a complete CODE
readback with a clean journal before preserving its current NVM.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pack_ak820 as packer
import ak820_tool as updater


def write_trial(ihx: Path, mapfile: Path, stockpath: Path, nativepath: Path,
                backup: bytes, out: Path, *, current_rom: bytes | None = None,
                current_trial: bytes | None = None,
                target_build_id: int = packer.BUILD_ID,
                source_build_id: int = packer.BUILD_ID) -> dict:
    stock, native = stockpath.read_bytes(), nativepath.read_bytes()
    packer.validate_native(backup, stock, native)
    data, symbols = packer.read_ihex(ihx), packer.read_symbols(mapfile)
    if (current_rom is None) != (current_trial is None):
        raise ValueError("Existing trial migration requires both readback and exact current trial image")
    if current_rom is None:
        nvm, migration = packer.migrate(backup, data, symbols)
        if target_build_id != packer.BUILD_ID:
            nvm, schema_migration = packer.migrate_vial_nvm(
                nvm, packer.BUILD_ID, target_build_id=target_build_id)
            migration = {'native_migration': migration, 'schema_migration': schema_migration}
        provenance = {"mode": "native_backup", "source_sha256": packer.digest(backup)}
    else:
        old = packer.verify_payload(current_trial, allow_legacy=True, target_build_id=source_build_id)
        if not old['trial']:
            raise ValueError("Expected the exact previously installed trial image")
        # This preserves the existing protected-loader/tail, full code/entry,
        # manifest, marker, journal and incomplete-macro checks.
        updater.verify_live(current_rom, current_trial, 'trial', stock, target_build_id=source_build_id)
        nvm, migration = packer.migrate_vial_nvm(
            current_rom[packer.NVM_START:packer.NVM_END], old['build_id'],
            target_build_id=target_build_id)
        provenance = {'mode': 'verified_trial_readback',
                      'source_sha256': packer.digest(current_rom),
                      'prior_trial_sha256': packer.digest(current_trial),
                      'journal_header_verified_empty': True,
                      'note': 'Offline snapshot validation does not establish that the live device has not changed since capture.'}
    trial = packer.pack(data, symbols, stock, nvm, True, target_build_id=target_build_id)
    info = packer.verify_payload(trial, target_build_id=target_build_id)
    recovery = backup[packer.APP_START:packer.APP_END]
    metadata = {'format': 'ak820-vial-release-1',
                'hardware': 'AJAZZ AK820 wired / VS11K28A / 320F:505B',
                'address': packer.APP_START, 'length': len(trial),
                'preserved': [[0, packer.APP_START], [packer.APP_END, 65536]],
                'backup_sha256': packer.digest(backup),
                'ihx_sha256': packer.digest(ihx.read_bytes()),
                'map_sha256': packer.digest(mapfile.read_bytes()),
                'images': {updater.IMAGES['trial']: info,
                           updater.IMAGES['restore']: {'size': len(recovery), 'sha256': packer.digest(recovery),
                               'restores': 'native application/settings from the original recovery backup'}},
                'migration': migration, 'nvm_provenance': provenance,
                'trial_only': True, 'hardware_validated': False,
                'trial_recovery': 'After successful early marker erase, the next reset enters the OEM loader.',
                'physical_operations': 0}
    # All validation completes before making any output. Never modify or reuse
    # the source recovery directory. The existing updater checks this manifest.
    out.mkdir(parents=True, exist_ok=False)
    (out / updater.IMAGES['trial']).write_bytes(trial)
    (out / updater.IMAGES['restore']).write_bytes(recovery)
    (out / 'before-full-rom.bin').write_bytes(backup)
    (out / 'images.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    updater.plan(out, 'trial', target_build_id=target_build_id)
    updater.plan(out, 'restore')
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ihx', type=Path, required=True)
    parser.add_argument('--map', dest='mapfile', type=Path, required=True)
    parser.add_argument('--stock-rom', type=Path, required=True)
    parser.add_argument('--native-reference', type=Path, required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--native-rom', type=Path, help='Validated full native backup; import its original settings')
    source.add_argument('--recovery-session', type=Path, help='Read the original personal native restore session')
    parser.add_argument('--current-rom', type=Path, help='Complete FD00 readback of the existing trial')
    parser.add_argument('--current-trial', type=Path, help='Exact image used to install that trial')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.recovery_session:
        if args.current_rom is None or args.current_trial is None:
            parser.error('--recovery-session requires --current-rom and --current-trial')
        _, _, backup = updater.session_image(args.recovery_session, 'restore')
    else:
        if args.current_rom is not None or args.current_trial is not None:
            parser.error('Use --recovery-session when preserving existing trial NVM')
        backup = args.native_rom.read_bytes()
    metadata = write_trial(args.ihx, args.mapfile, args.stock_rom, args.native_reference,
                           backup, args.out,
                           current_rom=args.current_rom.read_bytes() if args.current_rom else None,
                           current_trial=args.current_trial.read_bytes() if args.current_trial else None)
    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
