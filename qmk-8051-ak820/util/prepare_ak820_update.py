"""Offline durable-settings update plan. No USB and no flash session output.

FD01 v1 cannot establish RGB RAM cleanliness or an atomic live snapshot. This
module intentionally offers no live-ready mode and accepts no freshness flags.
"""
from __future__ import annotations

import json
from pathlib import Path

import ak820_diagnose as diagnostic
import ak820_tool as updater
import pack_ak820 as packer


def prepare_durable_update(ihx: Path, mapfile: Path, stock: bytes,
                           native_reference: bytes, original_backup: bytes,
                           source_payload: bytes, source_rom: bytes,
                           second_nvm_journal: bytes, status_reply: bytes,
                           policy: dict, out: Path) -> dict:
    """Transform caller-supplied evidence, without certifying its live origin.

    Policy is an explicit caller-controlled allowlist decision, never a proof
    of hardware freshness. Raw status and repeat bytes are validated locally.
    All validation precedes creation of the new output directory.
    """
    if any(type(value) is not bytes for value in (stock, native_reference, original_backup,
            source_payload, source_rom, second_nvm_journal, status_reply)):
        raise TypeError('Evidence must be immutable bytes, not status assertions')
    if type(policy) is not dict or policy.keys() != {'format', 'source_sha256', 'source_build_id', 'status_protocol', 'scope'}:
        raise ValueError('Unknown source policy fields')
    if (policy['format'] != 'ak820-durable-source-policy-1'
            or policy['scope'] != 'durable-snapshot-only'
            or policy['status_protocol'] != 'FD01-v1'):
        raise ValueError('Unsupported source policy/capability')
    source = packer.verify_payload(source_payload, allow_legacy=True)
    if source['trial']:
        raise ValueError('General permanent update requires a permanent source')
    if (policy['source_sha256'] != packer.digest(source_payload)
            or type(policy['source_build_id']) is not int
            or policy['source_build_id'] != source['build_id']):
        raise ValueError('Exact supported source identity differs')
    packer.validate_native(original_backup, stock, native_reference)
    updater.verify_live(source_rom, source_payload, 'permanent', stock)
    if source_rom[packer.NVM_START:packer.MANIFEST_START] != second_nvm_journal:
        raise ValueError('NVM/journal changed between supplied snapshots')
    status = diagnostic.decode_status(status_reply)
    if status['storage_failed'] or status['page_dirty'] or status['batch_depth']:
        raise ValueError('Source status reports dirty, batched or failed storage')
    if status['first_failure_stage']:
        raise ValueError('Source status retains a storage fault')
    nvm, migration = packer.migrate_vial_nvm(
        source_rom[packer.NVM_START:packer.NVM_END], source['build_id'])
    ihx_bytes, map_bytes = ihx.read_bytes(), mapfile.read_bytes()
    payload = packer.pack(packer.read_ihex(ihx), packer.read_symbols(mapfile), stock, nvm, False)
    if ihx.read_bytes() != ihx_bytes or mapfile.read_bytes() != map_bytes:
        raise ValueError('Target build inputs changed during preparation')
    target = packer.verify_payload(payload)
    # Embed bytes in a distinct plan format. Generic updater requires binary
    # image names, images.json and a native session; this output supplies none.
    result = {
        'format': 'ak820-durable-update-plan-1', 'scope': 'durable-snapshot-only',
        'flash_authorized': False, 'live_freshness_verified': False,
        'required_live_gate': {'capability': 'pending-save-visibility-and-snapshot-freeze',
                               'supported_version': None, 'implemented': False},
        'policy': dict(policy), 'source': source, 'target': target,
        'hashes': {name: packer.digest(value) for name, value in {
            'original_recovery_rom': original_backup, 'native_reference': native_reference,
            'stock_reference': stock, 'source_full_rom': source_rom,
            'second_nvm_journal': second_nvm_journal, 'source_status_reply': status_reply,
            'target_ihx': ihx_bytes, 'target_map': map_bytes, 'migrated_nvm': nvm,
            'target_payload': payload}.items()},
        'status': status, 'migration': migration, 'payload_hex': payload.hex(),
        'physical_operations': 0,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + '\n'
    out.mkdir(parents=True, exist_ok=False)
    (out / 'durable-update-plan.json').write_text(encoded, encoding='utf-8')
    return result
