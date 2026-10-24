"""Local settings export and typed Vial restore for the reviewed RC6 image.

No HID is imported and no firmware writes are implemented here. The caller
supplies DeviceAPI, an approved firmware profile and physical unlock consent.
Backups contain private data and must stay local. A backup is not an OEM
recovery image, an atomic snapshot or a copy of every live RAM field.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'qmk-8051-ak820/util'))
from ak820_device_protocol import DeviceAPI
import ak820_diagnose as diagnostic
import pack_ak820 as pack

FORMAT = 'ak820-settings-backup-1'
SUPPORTED_IHX = 'f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e'
SUPPORTED_IMAGES = (
    (SUPPORTED_IHX, '6ff7b1653925da7dc12bdb6f7ef5fc1dc4319c5b931def50c68b9cf45c4054d7'),
    ('feac6dae864e801b6177fb8c57a23a65c59b850c5dd3ce84dfb2abb853058cc8',
     '119c907421d45154b0e6c16fb176ec2c1a51c1fec9627e341599d5b0cc8dca52'),
    ('d5842186152b0a612289775c89cc8564167cb8f0bb0b2cc34858a37dda7b8fd3',
     '7e6b90f51a99ac335c0cb910fffc85f1d1705e7159a12de46f8e492807c36d40'),
    ('45f28e80cd9e269cb507d6fff47b43cea2766b00967912599a98b036b638011d',
     'cc5af6cc86724103fbc3e2c1815bf7a2235edc0ed85a932fd3e993cd6b4f7931'),
)
CANDIDATE_IHX = 'a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f'
SUPPORTED_IMAGES += ((CANDIDATE_IHX, 'd787703f62f96d7204bf25c566eac39f66b8c8c3f711ce152d7ff1eded9716da'),)
UID = '0470ff9001b915d3'
DEVICE = {'vid': 0x320F, 'pid': 0x505B, 'vial_uid': UID}
# Pinned enum in rgb_matrix.h / vialrgb_effects.inc for this exact image.
RGB_MODES = {1: 2, 2: 6, 3: 13, 4: 14, 5: 1, 6: 31}
BRIGHTNESS = 160
PHYSICAL = tuple((slot // 8, slot % 8) for slot in pack.PHYSICAL)
FILES = {'settings.json': 512 * 1024, 'before-full-rom.bin': 65536,
         'saved-nvm.bin': pack.NVM_END - pack.NVM_START,
         'read-log.jsonl': 8 * 1024 * 1024, '.gitignore': 2}
LIMITATIONS = [
    'Direct HSV palette: no getter; not exported or restored.',
    'Hidden current RGB mode while off and current RGB flags: no getter; only saved NVM values are preserved.',
    'Unused matrix slots and reserved NVM bytes: captured as evidence, not imported.',
    'Animation phase, reactive ages, held keys and macro execution position: not exported.',
    'No firmware freeze: repeated stable reads do not guarantee an atomic snapshot.',
    'Vial UID identifies a model, not a unique physical keyboard; connect only one supported device.',
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def _json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON field: ' + key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Invalid JSON number')))


def load_profile(bundle, native_backup):
    """Reconstruct exact packed CODE from approved inputs and valid OEM bytes.

    The installer validates its release approval before this function. This
    additional pin binds protocol/field semantics to the reviewed image; a new
    build needs an explicitly reviewed profile, not just the same schema ID.
    """
    bundle = Path(bundle)
    ihx, mapfile = bundle / 'firmware/application.ihx', bundle / 'firmware/application.map'
    ihx_sha256 = pack.digest(ihx.read_bytes())
    require(ihx_sha256 in {image[0] for image in SUPPORTED_IMAGES},
            'Unsupported firmware build for settings preservation')
    native_backup = bytes(native_backup)
    pack.validate_native(native_backup)
    code = diagnostic.diagnostic_build(ihx, mapfile, bundle / 'reports/build-report.json')
    symbols = pack.read_symbols(mapfile)
    nvm, _ = pack.migrate(native_backup, code, symbols)
    payload = pack.pack(code, symbols, native_backup, nvm, False)
    definition = _json((bundle / 'reference/vial.json').read_bytes())
    code_sha256 = pack.digest(payload[:pack.CODE_END-pack.APP_START])
    require((ihx_sha256, code_sha256) in SUPPORTED_IMAGES,
            'Firmware CODE does not match a reviewed settings profile')
    images = {ihx: {'ihx_sha256': ihx, 'code_sha256': code, 'build_id': pack.BUILD_ID,
                    'combos_version': 1 if ihx == CANDIDATE_IHX else None}
              for ihx, code in SUPPORTED_IMAGES}
    return {'payload': payload, 'backup': native_backup, 'native_backup': native_backup,
            'definition': definition, 'code': code,
            'definition_sha256': pack.digest(canonical(definition)), 'schema': pack.BUILD_ID,
            'ihx_sha256': ihx_sha256, 'code_sha256': code_sha256,
            'compatible_images': images}


def _profile_images(profile):
    images = profile.get('compatible_images')
    if images is None:
        # Synthetic in-memory profiles used by the isolated model tests.
        return {profile['ihx_sha256']: {'ihx_sha256': profile['ihx_sha256'],
                                        'code_sha256': profile['code_sha256'],
                                        'build_id': pack.BUILD_ID}}
    return images


def _rom_identity(rom, profile):
    code_sha256 = pack.digest(rom[pack.APP_START:pack.CODE_END])
    matches = [image for image in _profile_images(profile).values()
               if image['code_sha256'] == code_sha256]
    require(len(matches) == 1, 'Running CODE is not an exact reviewed settings image')
    image = matches[0]
    at = pack.MANIFEST_START
    expected = (pack.MAGIC + b'\1\0\0\0' + int(image['build_id']).to_bytes(4, 'little') +
                bytes.fromhex(image['code_sha256']))
    require(rom[at:at+48] == expected, 'Application manifest/build identity differs')
    return image


def validate_rom(rom, profile, expected_identity=None):
    require(len(rom) == 65536, 'Incomplete full ROM')
    native, payload = profile['backup'], profile['payload']
    require(rom[:0x27C0] == native[:0x27C0] and rom[pack.APP_END:] == native[pack.APP_END:],
            'Protected loader/tail differs from the OEM recovery session')
    require(rom[0x27C0:0x27C4] == bytes.fromhex('aa5533cc'), 'Permanent boot marker is missing')
    image = _rom_identity(rom, profile)
    if expected_identity is not None:
        require((image['ihx_sha256'], image['code_sha256']) == tuple(expected_identity),
                'ROM CODE differs from the recorded source image')
    elif not profile.get('compatible_images'):
        require(rom[pack.APP_START:pack.CODE_END] == payload[:pack.CODE_END-pack.APP_START],
                'Running CODE differs from the exact supported image')
    # The last16 manifest bytes describe the original installation's NVM,
    # which may differ from a fresh migration of the OEM recovery snapshot.
    require(not any(rom[pack.NVM_END+64:pack.MANIFEST_START]), 'Journal header is not empty')
    return pack.validate_nvm(rom[pack.NVM_START:pack.NVM_END], profile['schema'])


def macro_commands(stream):
    """Describe already validated bytecode; operands are binary, not text."""
    logical = pack.macro_stream_length(stream)
    result, commands, text, offset = [], [], bytearray(), 0
    names = {1: 'tap', 2: 'down', 3: 'up', 4: 'delay', 5: 'tap16', 6: 'down16', 7: 'up16'}
    def flush():
        if text:
            commands.append({'text_hex': bytes(text).hex()})
            text.clear()
    while offset < logical:
        value = stream[offset]
        offset += 1
        if value == 0:
            flush()
            result.append(commands)
            commands = []
        elif value == 1:
            flush()
            opcode = stream[offset]
            count = 1 if opcode <= 3 else 2
            operands = stream[offset+1:offset+1+count]
            commands.append({'command': names[opcode], 'operands_hex': operands.hex()})
            offset += 1 + count
        else:
            text.append(value)
    return result


def rgb_wire(raw, *, selected=False):
    require(len(raw) == 8, 'RGB config requires eight saved bytes')
    mode, enabled = raw[0] >> 2, raw[0] & 3
    require(enabled in (0, 1) and mode in RGB_MODES, 'Saved RGB enable/mode is unsupported')
    require(raw[3] <= BRIGHTNESS, 'Saved RGB brightness exceeds the target limit')
    wire = RGB_MODES[mode] if enabled or selected else 0
    return wire.to_bytes(2, 'little') + bytes((raw[4], raw[1], raw[2], raw[3]))


def combo_settings(nvm):
    entries = []
    for index in range(8):
        offset = DeviceAPI.COMBO_OFFSET + index*10
        raw = nvm[offset:offset+10]
        # Freshly migrated images have an unused all-zero extension.
        if raw == bytes(10):
            data = raw
        else:
            require(raw[4:8] == DeviceAPI.COMBO_MARKER, 'Unknown Combo marker/version')
            data = raw[:4] + bytes(4) + raw[8:]
        entries.append(DeviceAPI.validate_combo(data).hex())
    return {'version': 1, 'entries_hex': entries}


def _combo_capable(profile, identity=None):
    image = _profile_images(profile)[identity or profile['ihx_sha256']]
    version = image.get('combos_version')
    require(version in (None, 1), 'Unknown Combo profile version')
    return version == 1


def settings_from_nvm(nvm, rgb_mode, *, combos=False):
    metadata = pack.validate_nvm(nvm)
    length = metadata['published_macro_length']
    stream = nvm[pack.MACRO_ADDR:pack.MACRO_ADDR+length]
    keys = [{'layer': layer, 'row': row, 'column': col,
             'keycode': int.from_bytes(nvm[DeviceAPI.key_offset(layer, (row, col)):
                                           DeviceAPI.key_offset(layer, (row, col))+2], 'big')}
            for layer in range(6) for row, col in PHYSICAL]
    encoders = [{'layer': layer, 'direction': direction,
                 'keycode': int.from_bytes(nvm[DeviceAPI.encoder_offset(layer, direction):
                                               DeviceAPI.encoder_offset(layer, direction)+2], 'big')}
                for layer in range(6) for direction in (0, 1)]
    result = {'keys': keys, 'encoders': encoders, 'layout_options': nvm[40],
            'macros': {'count': 16, 'capacity': 8192, 'published_length': length,
                       'logical_length': metadata['logical_macro_length'],
                       'data_hex': stream.hex(), 'commands': macro_commands(stream)},
            'rgb': {'saved_config_hex': nvm[24:32].hex(), 'current_mode_hex': rgb_mode.hex(),
                    'saved_source': 'NVM[24:32]', 'current_source': 'VialRGB 0x08/0x41'},
            'limitations': LIMITATIONS}
    if combos:
        result['combos'] = combo_settings(nvm)
    return result


def _check_getters(api, settings):
    if 'combos' in settings:
        require(api.combo_count() == 8, 'Combo count differs')
        for index, data in enumerate(settings['combos']['entries_hex']):
            require(api.get_combo(index) == bytes.fromhex(data), 'Combo getter differs from saved NVM')
    for item in settings['keys']:
        require(api.get_key(item['layer'], (item['row'], item['column'])) == item['keycode'],
                'Key getter differs from saved NVM: ' + str(item))
    for item in settings['encoders']:
        require(api.get_encoder(item['layer'], item['direction']) == item['keycode'],
                'Encoder getter differs from saved NVM: ' + str(item))
    require(api.get_layout_options() == settings['layout_options'], 'Layout getter differs from saved NVM')
    stream = bytes.fromhex(settings['macros']['data_hex'])
    require(api.macros() == stream + bytes(8192-len(stream)), 'Macro getter differs from published NVM')
    require(api.rgb_mode().hex() == settings['rgb']['current_mode_hex'], 'RGB RAM differs from saved settings')


def capture_settings(api, profile):
    api.status()
    require(set(api.definition()) == set(PHYSICAL), 'Physical definition coordinates differ')
    rom = api.read_code(0, 65536)
    validate_rom(rom, profile)
    nvm = rom[pack.NVM_START:pack.NVM_END]
    require(api.read_nvm() == nvm, 'NVM changed during export')
    rgb = api.rgb()
    require(rgb['effects'] == sorted(RGB_MODES.values()) and rgb['info_hex'] == '0100a0',
            'RGB capabilities differ from the supported image')
    current = bytes.fromhex(rgb['mode_hex'])
    require(current == rgb_wire(nvm[24:32]),
            'RGB RAM and saved NVM differ; save the intended settings explicitly before export')
    settings = settings_from_nvm(nvm, current, combos=_combo_capable(profile, _rom_identity(rom, profile)['ihx_sha256']))
    _check_getters(api, settings)
    require(api.read_nvm() == nvm, 'NVM changed during getters; export is not a firmware freeze')
    require(api.rgb_mode() == current, 'RGB changed during export')
    api.status()
    return rom, nvm, settings


def _record(data):
    return {'size': len(data), 'sha256': pack.digest(data)}


def export_settings(api, output, profile):
    """Publish a new local backup only after rereading and validating all files."""
    output = Path(output).absolute()
    require(not output.exists() and not output.is_symlink(), 'Backup output already exists; choose a new directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix='.' + output.name + '-pending-', dir=output.parent))
    try:
        api.trace.flush()
        trace_start = Path(api.trace.name).stat().st_size
        api.boot_liveness()
        rom, nvm, settings = capture_settings(api, profile)
        api.trace.flush()
        with Path(api.trace.name).open('rb') as trace:
            trace.seek(trace_start)
            read_log = trace.read()
        files = {'settings.json': canonical(settings), 'before-full-rom.bin': rom,
                 'saved-nvm.bin': nvm, 'read-log.jsonl': read_log, '.gitignore': b'*\n'}
        source_image = _rom_identity(rom, profile)
        manifest = {'format': FORMAT, 'created_utc': datetime.now(timezone.utc).isoformat(),
                    'device': DEVICE, 'definition_sha256': profile['definition_sha256'],
                    'nvm_schema': pack.BUILD_ID, 'source_build_id': pack.BUILD_ID,
                    'source_ihx_sha256': source_image['ihx_sha256'],
                    'code_sha256': source_image['code_sha256'],
                    'counts': {'layers': 6, 'physical_keys': 83, 'assignments': 498,
                               'encoder_assignments': 12, 'macros': 16, 'macro_capacity': 8192},
                    'scope': 'saved supported settings and exposed RGB values; not all current RAM',
                    'files': {name: _record(data) for name, data in files.items()}}
        for name, data in {**files, 'manifest.json': canonical(manifest)}.items():
            with (temp / name).open('xb') as target:
                target.write(data)
                target.flush()
                os.fsync(target.fileno())
        validate_backup(temp, profile)
        require(not output.exists() and not output.is_symlink(), 'Backup output appeared during export')
        # A completed destination is nonempty and cannot be replaced by rename.
        # Windows also rejects any existing destination. No ready backup is overwritten.
        temp.rename(output)
        return validate_backup(output, profile)
    finally:
        if temp.exists():
            shutil.rmtree(temp)


def _read_file(folder, name, maximum):
    path = folder / name
    require(not path.is_symlink() and path.is_file(), 'Missing or linked backup file: ' + name)
    require(path.stat().st_size <= maximum, 'Oversized backup file: ' + name)
    with path.open('rb') as source:
        data = source.read(maximum+1)
    require(len(data) <= maximum, 'Backup file grew during read: ' + name)
    return data


def validate_backup(path, profile, expected_identity=None):
    """Read immutable bytes, verify hashes and derive values from saved NVM.

    JSON supplies no writable addresses or USB packets. Even a self-consistent
    edited settings.json must agree with the exact supported ROM and NVM.
    """
    path = Path(path).absolute()
    require(path.is_dir() and not path.is_symlink(), 'Backup must be a real directory')
    raw = _read_file(path, 'manifest.json', 65536)
    identity = pack.digest(raw)
    require(expected_identity is None or identity == expected_identity, 'Backup manifest changed after validation')
    manifest = _json(raw)
    require(isinstance(manifest, dict) and manifest.get('format') == FORMAT, 'Unknown backup format')
    require(canonical(manifest.get('device')) == canonical(DEVICE), 'Backup device identity differs')
    source_ihx = manifest.get('source_ihx_sha256')
    source_code = manifest.get('code_sha256')
    image = _profile_images(profile).get(source_ihx)
    require(image is not None and image['code_sha256'] == source_code and
            manifest.get('definition_sha256') == profile['definition_sha256'] and
            type(manifest.get('nvm_schema')) is int and manifest['nvm_schema'] == pack.BUILD_ID and
            type(manifest.get('source_build_id')) is int and manifest['source_build_id'] == pack.BUILD_ID,
            'Unsupported backup firmware/definition/schema')
    require(manifest.get('counts') == {'layers': 6, 'physical_keys': 83, 'assignments': 498,
                                     'encoder_assignments': 12, 'macros': 16, 'macro_capacity': 8192},
            'Backup dimensions differ')
    require(isinstance(manifest.get('files'), dict) and set(manifest['files']) == set(FILES),
            'Unexpected backup files')
    files = {name: _read_file(path, name, limit) for name, limit in FILES.items()}
    for name, data in files.items():
        require(manifest['files'][name] == _record(data), 'Backup hash/size mismatch: ' + name)
    require(_read_file(path, 'manifest.json', 65536) == raw, 'Backup manifest changed during read')
    require(files['.gitignore'] == b'*\n', 'Backup Git exclusion is missing')
    rom, nvm = files['before-full-rom.bin'], files['saved-nvm.bin']
    validate_rom(rom, profile, (source_ihx, source_code))
    require(nvm == rom[pack.NVM_START:pack.NVM_END], 'Saved NVM differs from the full ROM')
    settings = _json(files['settings.json'])
    expected = settings_from_nvm(nvm, rgb_wire(nvm[24:32]), combos=_combo_capable(profile, source_ihx))
    require(canonical(settings) == canonical(expected), 'Settings JSON differs from validated NVM or RGB contract')
    return {'path': path, 'identity': identity, 'manifest': manifest, 'settings': expected,
            'rom': rom, 'nvm': nvm, 'source_identity': (source_ihx, source_code)}


def keycode_supported(code):
    """Conservative current-build allowlist, including documented tap fallbacks.

    quantum/keymap_common.c, quantum.c, process_rgb.c and enabled key processors
    define this list. Unknown feature namespaces are never silently restored.
    """
    if type(code) is not int or not 0 <= code <= 65535:
        return False
    basic = lambda value: value in (0, 1) or 4 <= value <= 0xC2 or 0xE0 <= value <= 0xE7
    if code < 256:
        return basic(code)
    if code < 0x4000:  # modifiers; mod-tap retains its existing tap-only fallback
        return basic(code & 255)
    if code < 0x5000:  # layer-tap retains tap-only fallback, known layers only
        return (code >> 8) & 15 < 6 and basic(code & 255)
    if code < 0x5200:
        return ((code - 0x5000) >> 5) < 6
    if (code & 0xFFE0) in (0x5200, 0x5220, 0x5240, 0x5260, 0x52C0):
        return (code & 31) < 6
    if 0x52A0 <= code <= 0x52BF:  # existing held-mod OSM fallback, not one-shot
        return True
    return (0x7700 <= code <= 0x770F or 0x7820 <= code <= 0x782A or
            code in (0x7C00, 0x7C01, 0x7C02, 0x7C03, 0x7C16, 0x7C73,
                     0x7C77, 0x7C78, 0x7C79, 0x7C7A))


def macro_chunks(stream):
    logical = pack.macro_stream_length(stream)
    require(16 <= len(stream) <= 8192, 'Macro stream size is unsupported')
    # Publish at exactly the saved length. Earlier chunks must not contain the
    # sixteenth terminator, otherwise firmware publishes early and ignores tail.
    final_start = max(0, len(stream)-28)
    require(final_start < logical, 'Published macro padding cannot be reproduced (more than27 bytes)')
    chunks, offset = [], 0
    while offset < final_start:
        count = min(28, final_start-offset)
        chunks.append((offset, stream[offset:offset+count]))
        offset += count
    chunks.append((offset, stream[offset:]))
    return chunks


def plan_restore(backup, profile, target_nvm=None):
    backup = validate_backup(backup['path'], profile, backup['identity'])
    target_nvm = bytes(target_nvm if target_nvm is not None else
                       profile['payload'][pack.NVM_START-pack.APP_START:pack.NVM_END-pack.APP_START])
    pack.validate_nvm(target_nvm)
    settings, nvm = backup['settings'], backup['nvm']
    target_identity = (profile['ihx_sha256'], profile['code_sha256'])
    images = list(_profile_images(profile).values())
    source_rank = next(i for i, image in enumerate(images)
                       if (image['ihx_sha256'], image['code_sha256']) == backup['source_identity'])
    target_rank = next(i for i, image in enumerate(images)
                       if (image['ihx_sha256'], image['code_sha256']) == target_identity)
    require(source_rank <= target_rank,
            'Settings restore would downgrade firmware; only same-image or approved forward transitions are allowed')
    blockers = []
    combo_entries = None
    if _combo_capable(profile):
        target_combos = combo_settings(target_nvm)
        if 'combos' in settings:
            combo_entries = settings['combos']['entries_hex']
        else:
            require(all(data == bytes(10).hex() for data in target_combos['entries_hex']),
                    'Legacy backup has no Combos; existing target Combos must not be cleared')
    else:
        require('combos' not in settings, 'Target firmware does not support Combos')
    for item in settings['keys'] + settings['encoders']:
        if not keycode_supported(item['keycode']):
            blockers.append('Unsupported keycode ' + hex(item['keycode']) + ': ' + str(item))
    raw = nvm[24:32]
    if RGB_MODES[raw[0] >> 2] == 1:
        blockers.append('Direct Control palette has no getter; selected Direct mode cannot be preserved')
    if raw[5:8] != target_nvm[29:32] or raw[6:8] != bytes(2):
        blockers.append('Saved RGB flags/padding have no setter or differ from the target')
    # Core configuration outside RGB is not writable through the selected API.
    # Do not silently discard e.g. a saved default layer or NKRO setting.
    for start, end in ((2, 24), (32, 37)):
        if nvm[start:end] != target_nvm[start:end]:
            blockers.append(f'Core NVM configuration {start}..{end-1} has no restore setter')
    stream = bytes.fromhex(settings['macros']['data_hex'])
    try:
        chunks = macro_chunks(stream)
    except ValueError as error:
        blockers.append(str(error))
        chunks = []
    # Validate key-bearing macro commands as well as matrix/encoder values.
    for number, commands in enumerate(settings['macros']['commands']):
        for command in commands:
            name = command.get('command', '')
            if name in ('tap', 'down', 'up', 'tap16', 'down16', 'up16'):
                operands = bytes.fromhex(command['operands_hex'])
                value = int.from_bytes(operands, 'little')
                if len(operands) == 2 and value > 0xFF00:
                    value = (value & 255) << 8  # firmware's encoded low-zero keycode
                if not keycode_supported(value):
                    blockers.append(f'Unsupported keycode in macro {number}: {value:#06x}')
    require(not blockers, 'Settings cannot be restored before any erase/write:\n' + '\n'.join(blockers))
    return {'combo_entries': combo_entries, 'key_count': 498, 'encoder_count': 12, 'macro_chunks': chunks,
            'rgb_saved_mode': rgb_wire(raw, selected=True), 'rgb_effective_mode': rgb_wire(raw),
            'limitations': list(LIMITATIONS), 'requires_physical_unlock': True}


def recheck_source(api, backup, profile):
    backup = validate_backup(backup['path'], profile, backup['identity'])
    rom = api.read_code(0, 65536)
    validate_rom(rom, profile, backup['source_identity'])
    require(rom == backup['rom'], 'Source ROM/settings changed after backup; start a new operation')
    _check_getters(api, backup['settings'])
    require(api.read_nvm() == backup['nvm'], 'Source NVM changed after backup')
    api.status()


def require_target_backup(backup, profile):
    """Require a captured target snapshot to contain the selected image."""
    backup = validate_backup(backup['path'], profile, backup['identity'])
    expected = (profile['ihx_sha256'], profile['code_sha256'])
    require(backup['source_identity'] == expected,
            'Target firmware differs from the selected image; settings cannot be restored')
    return backup


def verify_restore(api, backup, profile):
    backup = validate_backup(backup['path'], profile, backup['identity'])
    rom, nvm, actual = capture_settings(api, profile)
    expected_target = (profile['ihx_sha256'], profile['code_sha256'])
    require(_rom_identity(rom, profile)['ihx_sha256'] == expected_target[0] and
            _rom_identity(rom, profile)['code_sha256'] == expected_target[1],
            'Final running firmware differs from the selected target image')
    expected_settings = dict(backup['settings'])
    if _combo_capable(profile) and 'combos' not in expected_settings:
        require(all(data == bytes(10).hex() for data in actual['combos']['entries_hex']),
                'Legacy restore target Combos are not empty')
        expected_settings['combos'] = actual['combos']
    require(canonical(actual) == canonical(expected_settings), 'Final restored settings differ from the backup')
    # User values are compared, not journal data, unused slots, stale macro tail
    # or the new firmware's initial-config manifest digest.
    return {'verified': True, 'rom_sha256': pack.digest(rom), 'nvm_sha256': pack.digest(nvm),
            'keys': 498, 'encoders': 12, 'macros': 16, 'rgb_saved_bytes': 8,
            'physical_behavior': 'not tested', 'power_loss_persistence': 'not tested'}


def restore_settings(api, backup, profile, before_write=None, *, target_backup=None):
    """Restore through existing commands; any failure leaves evidence and stops.

    The installer has to request fresh physical unlock. The target snapshot is
    created here unless the same workflow already exported it before unlock.
    No rollback, reset, retry or command replay occurs on an exception.
    """
    require(api.allow_writes, 'Settings restore requires explicit write mode')
    backup = validate_backup(backup['path'], profile, backup['identity'])
    if target_backup is None:
        target_backup = export_settings(api, api.output / ('before-restore-' +
                                       datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')), profile)
    target_backup = require_target_backup(target_backup, profile)
    plan = plan_restore(backup, profile, target_backup['nvm'])
    recheck_source(api, target_backup, profile)
    require(api.status()['vial_unlocked'], 'A fresh physical Vial unlock is required before restore')
    expected = bytearray(target_backup['nvm'])
    settings = backup['settings']
    writes = 0

    def write(stage, operation):
        nonlocal writes
        if before_write:
            before_write(stage)
        validate_backup(backup['path'], profile, backup['identity'])
        require(api.status()['vial_unlocked'], 'Vial locked during restore; stopped without retry')
        require(operation() is True, 'Restore ACK mismatch at ' + stage)
        writes += 1
        api.status()

    def durable(stage):
        require(api.read_nvm() == bytes(expected), 'Durable settings or neighboring bytes differ after ' + stage)

    for layer in range(6):
        for item in settings['keys'][layer*83:(layer+1)*83]:
            key, value = (item['row'], item['column']), item['keycode']
            offset = DeviceAPI.key_offset(layer, key)
            data = value.to_bytes(2, 'big')
            if expected[offset:offset+2] != data:
                write(f'key:{layer}:{key[0]}:{key[1]}', lambda: api.set_key(layer, key, value))
                expected[offset:offset+2] = data
                require(api.get_key(layer, key) == value, 'Key readback differs')
        durable('key layer ' + str(layer))
    for item in settings['encoders']:
        layer, direction, value = item['layer'], item['direction'], item['keycode']
        offset = DeviceAPI.encoder_offset(layer, direction)
        data = value.to_bytes(2, 'big')
        if expected[offset:offset+2] != data:
            write(f'encoder:{layer}:{direction}', lambda: api.set_encoder(layer, direction, value))
            expected[offset:offset+2] = data
            require(api.get_encoder(layer, direction) == value, 'Encoder readback differs')
    durable('encoders')
    if expected[40] != settings['layout_options']:
        write('layout', lambda: api.set_layout_options(settings['layout_options']))
        expected[40] = settings['layout_options']
        require(api.get_layout_options() == expected[40], 'Layout readback differs')
        durable('layout')
    stream = bytes.fromhex(settings['macros']['data_hex'])
    meta = pack.MACRO_BUSY_ADDR
    if (expected[pack.MACRO_ADDR:pack.MACRO_ADDR+len(stream)] != stream or
            int.from_bytes(expected[meta+1:meta+3], 'little') != len(stream)):
        for offset, data in plan['macro_chunks']:
            write('macro:' + str(offset), lambda: api.upload_macro_chunk(offset, data))
            require(api.read_code(pack.NVM_START+pack.MACRO_ADDR+offset, len(data)) == data,
                    'Macro chunk durable readback differs')
        expected[pack.MACRO_ADDR:pack.MACRO_ADDR+len(stream)] = stream
        expected[meta:meta+3] = b'\0' + len(stream).to_bytes(2, 'little')
        require(api.macros() == stream + bytes(8192-len(stream)), 'Published macro readback differs')
        durable('macros')
    rgb = backup['nvm'][24:32]
    if expected[24:32] != rgb:
        write('rgb:selected', lambda: api.set_rgb_mode(plan['rgb_saved_mode']))
        require(api.rgb_mode() == plan['rgb_saved_mode'], 'Selected RGB mode readback differs')
        if not rgb[0] & 3:
            write('rgb:off', lambda: api.set_rgb_mode(plan['rgb_effective_mode']))
        require(api.rgb_mode() == plan['rgb_effective_mode'], 'RGB readback differs')
        write('rgb:save', api.save_rgb)
        expected[24:32] = rgb
        durable('RGB save')
    if plan['combo_entries'] is not None:
        require(api.combo_count() == 8, 'Combo count differs before restore')
        for index, value in enumerate(plan['combo_entries']):
            data = bytes.fromhex(value)
            offset = DeviceAPI.COMBO_OFFSET + index*10
            stored = DeviceAPI.stored_combo(data)
            if expected[offset:offset+10] != stored:
                write('combo:' + str(index), lambda: api.set_combo(index, data))
                expected[offset:offset+10] = stored
                require(api.get_combo(index) == data, 'Combo readback differs')
                durable('Combo ' + str(index))
    durable('final settings')
    result = verify_restore(api, backup, profile)
    result.update(writes=writes, target_backup=str(target_backup['path']))
    return result
