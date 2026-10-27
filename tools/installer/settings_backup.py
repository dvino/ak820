"""Local settings export and typed Vial restore for exact-image contracts.

No HID is imported and no firmware writes are implemented here. The caller
supplies DeviceAPI, an approved firmware profile and physical unlock consent.
Backups contain private data and must stay local. A backup is not an OEM
recovery image, an atomic snapshot or a copy of every live RAM field.
"""
from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
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
import ak820_extension_settings as extensions
import ak820_profiles

FORMAT = 'ak820-settings-backup-1'
FORMAT_V2 = 'ak820-settings-backup-2'
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
FULL_IHX = 'd505d4f420f745dbd5e98a0e3638c8f3ae6d7719c8729dad274595b71b641f18'
SUPPORTED_IMAGES += ((FULL_IHX, '01f0f7a979d8cfa8217b3bba333758ae3509cf7f3f8e35fbffb1ed034b808e5d'),)
WORK_IHX = '652ee9b583a285cea779d3937b8bcd84035e391d823d71d8ea1d34db2fdef880'
SUPPORTED_IMAGES += ((WORK_IHX, 'a7ad972f47acff20f3492ed846f5c6ca0825d43de263f26cc9328069a27cdd10'),)
WORK_FEATURES = frozenset(('nkro-control', 'one-shot', 'space-cadet', 'leader',
                           'dynamic-macros', 'os-indicators'))
MODULE_FEATURES = frozenset(ak820_profiles.SWITCHES)
FULL_FEATURES = frozenset(('nkro-control', 'one-shot', 'space-cadet'))
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


def load_profile(bundle, native_backup, *, trusted_catalog=None):
    """Reconstruct exact packed CODE from approved inputs and valid OEM bytes.

    The installer must separately validate release approval. The optional
    trusted matrix supplies development settings contracts for offline/desktop
    work; it does not approve installation. Each contract binds field semantics
    to exact IHX, packed CODE, definition and schema, never a profile name alone.
    """
    bundle = Path(bundle)
    ihx, mapfile = bundle / 'firmware/application.ihx', bundle / 'firmware/application.map'
    ihx_sha256 = pack.digest(ihx.read_bytes())
    images = _legacy_images()
    if trusted_catalog is not None:
        current = _catalog_images(trusted_catalog)
        for digest, image in current.items():
            require(digest not in images or images[digest]['code_sha256'] == image['code_sha256'],
                    'Catalog redefines a pinned historical image')
        images.update(current)
    require(ihx_sha256 in images,
            'Unsupported firmware build for settings preservation')
    native_backup = bytes(native_backup)
    pack.validate_native(native_backup)
    code = diagnostic.diagnostic_build(ihx, mapfile, bundle / 'reports/build-report.json')
    symbols = pack.read_symbols(mapfile)
    nvm, _ = pack.migrate(native_backup, code, symbols)
    schema = images[ihx_sha256]['build_id']
    if schema != pack.BUILD_ID:
        nvm, _ = pack.migrate_vial_nvm(nvm, pack.BUILD_ID, target_build_id=schema)
    payload = pack.pack(code, symbols, native_backup, nvm, False, target_build_id=schema)
    definition = _json((bundle / 'reference/vial.json').read_bytes())
    code_sha256 = pack.digest(payload[:pack.CODE_END-pack.APP_START])
    require(images[ihx_sha256]['code_sha256'] == code_sha256,
            'Firmware CODE does not match a reviewed settings profile')
    require(images[ihx_sha256].get('definition_sha256', pack.digest(canonical(definition))) ==
            pack.digest(canonical(definition)), 'Settings definition differs from the exact catalog image')
    return {'payload': payload, 'backup': native_backup, 'native_backup': native_backup,
            'definition': definition, 'code': code,
            'definition_sha256': pack.digest(canonical(definition)), 'schema': schema,
            'ihx_sha256': ihx_sha256, 'code_sha256': code_sha256,
            'compatible_images': images,
            **({'settings_transitions': trusted_catalog['settings_transitions']} if trusted_catalog is not None else {})}


def _legacy_images():
    return {ihx: {'ihx_sha256': ihx, 'code_sha256': code, 'build_id': pack.BUILD_ID,
                  'combos_version': 1 if ihx in (CANDIDATE_IHX, FULL_IHX, WORK_IHX) else None,
                  'features': (sorted(WORK_FEATURES) if ihx == WORK_IHX else
                               sorted(FULL_FEATURES) if ihx == FULL_IHX else []) + ['nkro', 'grave-escape', 'vialrgb-direct']}
            for ihx, code in SUPPORTED_IMAGES}


def _sha(value):
    return (type(value) is str and len(value) == 64 and
            all(c in '0123456789abcdef' for c in value))


@lru_cache(maxsize=64)
def _supported_keycodes(features, macro_layer_tap, compact_controls_version=1):
    return tuple(code for code in range(65536) if keycode_supported(code, features=features, compact_controls_version=compact_controls_version)
                 and (macro_layer_tap or not macro_layer_tap_keycode(code)))


def catalog_settings_identity(configuration, ihx_sha256, code_sha256, definition_sha256, *, combo_actions=('caps-word-toggle',), macro_layer_tap=True, direct_protocol=None):
    """Describe a measured packed image; this grants no release/write approval.

    CODE is SHA256 of permanent packed bytes [APP_START:CODE_END], including
    entry, vectors and OEM erase helper. A linked-window hash is not equivalent.
    The caller must obtain the catalog from a separately trusted source.
    """
    config = ak820_profiles.validate_configuration(configuration)
    return _settings_identity(config, ihx_sha256, code_sha256, definition_sha256,
                              combo_actions=combo_actions, macro_layer_tap=macro_layer_tap, direct_protocol=direct_protocol)


def _settings_identity(config, ihx_sha256, code_sha256, definition_sha256, *, combo_actions, macro_layer_tap, direct_protocol=None):
    require(all(_sha(v) for v in (ihx_sha256, code_sha256, definition_sha256)),
            'Invalid settings image digest')
    require(type(combo_actions) in (list, tuple) and list(combo_actions) in ([], ['caps-word-toggle']),
            'Unknown Combo action capability')
    require(type(macro_layer_tap) is bool, 'Invalid macro layer tap capability')
    features = config['optional_features']
    require(direct_protocol is None or (type(direct_protocol) is int and direct_protocol == 1 and 'vialrgb-direct' in features), 'Invalid Direct exact-image capability')
    return {'ihx_sha256': ihx_sha256, 'code_sha256': code_sha256,
            'definition_sha256': definition_sha256, 'nvm_schema': config['nvm_schema'],
            'profile': config['profile'], 'features': sorted(features),
            'supported_keycodes': list(_supported_keycodes(tuple(sorted(features)), macro_layer_tap, config.get('compact_controls_version', 1))),
            'macro_layer_tap': macro_layer_tap,
            **({'compact_controls_version': 2, 'settings_record_version': 2, 'combo_media': True} if config.get('compact_controls_version') == 2 else {}),
            **({'direct_protocol': 1} if direct_protocol == 1 else {}),
            'combo_actions': list(combo_actions), 'combos_version': 1, 'extensions_version': 1 if config['nvm_schema'] == extensions.SCHEMA else None}


def _catalog_images(catalog):
    """Consume the typed section of an explicitly trusted firmware matrix.

    Matrix measurements describe candidates, not release/install approval.
    Unknown contract fields fail closed so future semantics need a new reader.
    """
    require(type(catalog) is dict and catalog.get('format') == 'ak820-firmware-matrix-1' and
            type(catalog.get('profiles')) is list and type(catalog.get('settings_transitions')) is list,
            'Invalid trusted settings catalog')
    images = {}
    historical_profiles = catalog.get('historical_profiles', [])
    require(type(historical_profiles) is list and all(type(row) is dict and
            type(row.get('settings_identity')) is dict for row in historical_profiles),
            'Invalid historical settings profiles')
    for historical_row, row in ([(False, r) for r in catalog['profiles']] +
                                [(True, r) for r in historical_profiles]):
        require(type(row) is dict, 'Invalid settings catalog row')
        value = row.get('settings_identity')
        if value is None:
            continue
        require(type(value) is dict, 'Invalid settings identity')
        validator = ak820_profiles.validate_source_configuration
        config = validator(row.get('configuration'))
        expected = _settings_identity(config, value.get('ihx_sha256'),
                                             value.get('code_sha256'), value.get('definition_sha256'),
                                             combo_actions=value.get('combo_actions', []), macro_layer_tap=value.get('macro_layer_tap', False), direct_protocol=value.get('direct_protocol'))
        compared = {'combo_actions': [], 'macro_layer_tap': False, **value}
        require(canonical(compared) == canonical(expected), 'Settings identity fields/features/keycodes differ from configuration')
        require(row.get('profile') == config['profile'] and row.get('identity', {}).get('ihx_sha256') == value['ihx_sha256']
                and row['identity'].get('nvm_schema') == value['nvm_schema'],
                'Settings identity differs from measured image')
        require(value['ihx_sha256'] not in images and
                value['code_sha256'] not in {i['code_sha256'] for i in images.values()},
                'Duplicate or ambiguous settings image')
        images[value['ihx_sha256']] = {**expected, 'build_id': value['nvm_schema'], '_configuration': config}
    current_images = {row['settings_identity']['ihx_sha256'] for row in catalog['profiles']
                      if row.get('settings_identity') is not None}
    historical = catalog.get('historical_sources', [])
    require(type(historical) is list, 'Invalid historical settings sources')
    for source in historical:
        require(type(source) is dict and set(source) == {'ihx_sha256', 'code_sha256'},
                'Unknown historical settings source fields')
        ihx = source['ihx_sha256']
        pinned = _legacy_images().get(ihx) if type(ihx) is str else None
        require(pinned is not None and source['code_sha256'] == pinned['code_sha256'] and
                ihx not in images, 'Unknown or duplicate historical settings source')
        images[ihx] = pinned
    for transition in catalog['settings_transitions']:
        require(type(transition) is dict and set(transition) == {'source', 'target'} and
                transition['source'] in images and transition['target'] in current_images,
                'Unknown settings transition image/fields')
    return images


def _image_configuration(image):
    config = image.get('_configuration')
    if config is None:
        return ak820_profiles._configuration(image.get('profile'), ak820_profiles.PROFILES[image.get('profile')])
    config = ak820_profiles.validate_source_configuration(config)
    require(config['profile'] == image.get('profile'), 'Image configuration profile differs')
    return config


def _profile_images(profile):
    images = profile.get('compatible_images')
    if images is None:
        # Synthetic in-memory profiles used by the isolated model tests.
        return {profile['ihx_sha256']: {'ihx_sha256': profile['ihx_sha256'],
                                        'code_sha256': profile['code_sha256'],
                                        'build_id': pack.BUILD_ID}}
    for key, image in images.items():
        require(image.get('ihx_sha256') == key, 'Settings image index differs')
        if 'supported_keycodes' in image:
            config = _image_configuration(image)
            expected = _settings_identity(config, image.get('ihx_sha256'), image.get('code_sha256'),
                                                 image.get('definition_sha256'), combo_actions=image.get('combo_actions', []), macro_layer_tap=image.get('macro_layer_tap', False), direct_protocol=image.get('direct_protocol'))
            compared = {'combo_actions': [], 'macro_layer_tap': False,
                        **{k: v for k, v in image.items() if k != '_configuration'}}
            require(canonical(compared) == canonical({**expected, 'build_id': expected['nvm_schema']}),
                    'Settings image metadata differs from exact capability contract')
        if image.get('build_id') == extensions.SCHEMA:
            config = _image_configuration(image)
            require(image.get('extensions_version') == 1 and image.get('combos_version') == 1
                    and config['nvm_schema'] == extensions.SCHEMA
                    and set(image.get('features', ())) == set(config['optional_features'])
                    and len(image.get('features', ())) == len(config['optional_features']),
                    'Schema03 requires reviewed typed module metadata matching configuration')
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
    return pack.validate_nvm(rom[pack.NVM_START:pack.NVM_END], image['build_id'])


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


def rgb_modes(image=None):
    # Historical images and old synthetic fixtures used the Direct enum.
    direct = image is None or 'supported_keycodes' not in image or 'vialrgb-direct' in image.get('features', ())
    return RGB_MODES if direct else {1: 2, 2: 6, 3: 13, 4: 14, 5: 31}


def rgb_wire(raw, *, selected=False, image=None):
    require(len(raw) == 8, 'RGB config requires eight saved bytes')
    mode, enabled = raw[0] >> 2, raw[0] & 3
    modes = rgb_modes(image)
    require(enabled in (0, 1) and mode in modes, 'Saved RGB enable/mode is unsupported')
    require(raw[3] <= BRIGHTNESS, 'Saved RGB brightness exceeds the target limit')
    wire = modes[mode] if enabled or selected else 0
    return wire.to_bytes(2, 'little') + bytes((raw[4], raw[1], raw[2], raw[3]))


def translated_rgb_config(raw, source_image, target_image):
    """Preserve the wire effect while encoding the target's exact saved enum."""
    selected = rgb_wire(raw, selected=True, image=source_image)
    effect = int.from_bytes(selected[:2], 'little')
    inverse = {value: key for key, value in rgb_modes(target_image).items()}
    require(effect in inverse, 'Saved RGB effect is unsupported by the selected target image')
    target = bytearray(raw)
    target[0] = inverse[effect] * 4 + (raw[0] & 3)
    return bytes(target)


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


def _validate_combo_actions(combos, image):
    for entry in combos['entries_hex']:
        output = int.from_bytes(bytes.fromhex(entry)[8:10], 'little')
        require(not 0xA8 <= output <= 0xC2 or image.get('combo_media') is True, 'Media Combo is unsupported by the exact image')
        require(output != 0x7C73 or 'caps-word-toggle' in image.get('combo_actions', []),
                'Caps Word Combo is unsupported by the exact image')


def _combo_capable(profile, identity=None):
    image = _profile_images(profile)[identity or profile['ihx_sha256']]
    version = image.get('combos_version')
    require(version in (None, 1), 'Unknown Combo profile version')
    return version == 1


def settings_from_nvm(nvm, rgb_mode, *, combos=False, direct_capable=False, settings_version=None):
    schema = int.from_bytes(nvm[37:40], 'little')
    metadata = pack.validate_nvm(nvm, schema)
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
            'limitations': ([
                'Direct HSV palette is RAM-only; a separate direct-ram.json sidecar is required to recover it.',
                'Current RGB flags are sampled separately from NVM and the palette generation.',
                *LIMITATIONS[2:]] if direct_capable else LIMITATIONS)}
    if schema == extensions.SCHEMA:
        result['extensions'] = extensions.from_nvm(nvm, version=settings_version)
    if combos:
        result['combos'] = combo_settings(nvm)
    return result


def _check_getters(api, settings, image=None):
    if 'extensions' in settings:
        require(image is not None, 'Missing typed image metadata')
        config = _image_configuration(image)
        features = config['optional_features']
        data = settings['extensions']
        ids = api.settings_query()
        require(ids == config['runtime_qmk_settings'], 'Settings capabilities differ')
        for qsid in ids:
            require(api.get_setting(qsid) == data['qmk_settings'][str(qsid)], 'Settings getter differs')
        counts = api.dynamic_entry_counts()
        require(counts == (8 if 'tap-dance' in features else 0, 8,
                           8 if 'key-overrides' in features else 0), 'Dynamic capabilities differ')
        for kind, feature in (('tap_dance','tap-dance'), ('key_overrides','key-overrides')):
            if feature in features:
                for index, raw in enumerate(data[kind]):
                    require(api.get_extension(kind, index).hex() == raw, 'Extension getter differs')
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
    image = _rom_identity(rom, profile)
    require(rgb['effects'] == sorted(rgb_modes(image).values()) and rgb['info_hex'] == '0100a0',
            'RGB capabilities differ from the supported image')
    current = bytes.fromhex(rgb['mode_hex'])
    require(current == rgb_wire(nvm[24:32], image=image),
            'RGB RAM and saved NVM differ; save the intended settings explicitly before export')
    settings = settings_from_nvm(nvm, current, combos=_combo_capable(profile, _rom_identity(rom, profile)['ihx_sha256']), direct_capable=image.get('direct_protocol') == 1, settings_version=image.get('settings_record_version', 1))
    if 'combos' in settings:
        _validate_combo_actions(settings['combos'], image)
    _check_getters(api, settings, _rom_identity(rom, profile))
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
        if source_image.get('direct_protocol') == 1:
            palette = api.direct_snapshot()
            require(palette is not None, 'Exact image Direct capability unavailable at runtime')
            files['direct-ram.json'] = canonical(validate_direct_palette(palette))
            api.trace.flush()
            with Path(api.trace.name).open('rb') as trace:
                trace.seek(trace_start)
                files['read-log.jsonl'] = trace.read()
        manifest = {'format': FORMAT_V2 if source_image['build_id'] == extensions.SCHEMA else FORMAT, 'created_utc': datetime.now(timezone.utc).isoformat(),
                    'device': DEVICE, 'definition_sha256': profile['definition_sha256'],
                    'nvm_schema': source_image['build_id'], 'source_build_id': source_image['build_id'],
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
    require(isinstance(manifest, dict) and manifest.get('format') in (FORMAT, FORMAT_V2), 'Unknown backup format')
    require(set(manifest) <= {'format', 'created_utc', 'device', 'definition_sha256', 'nvm_schema',
                            'source_build_id', 'source_ihx_sha256', 'code_sha256', 'counts', 'scope', 'files'},
            'Unknown backup manifest field')
    require(canonical(manifest.get('device')) == canonical(DEVICE), 'Backup device identity differs')
    source_ihx = manifest.get('source_ihx_sha256')
    source_code = manifest.get('code_sha256')
    image = _profile_images(profile).get(source_ihx)
    require(image is not None and image['code_sha256'] == source_code and
            manifest.get('definition_sha256') == profile['definition_sha256'] and
            type(manifest.get('nvm_schema')) is int and manifest['nvm_schema'] == image['build_id'] and
            type(manifest.get('source_build_id')) is int and manifest['source_build_id'] == image['build_id'],
            'Unsupported backup firmware/definition/schema')
    require(manifest['format'] == (FORMAT_V2 if image['build_id'] == extensions.SCHEMA else FORMAT), 'Backup format/schema mismatch')
    require(manifest.get('counts') == {'layers': 6, 'physical_keys': 83, 'assignments': 498,
                                     'encoder_assignments': 12, 'macros': 16, 'macro_capacity': 8192},
            'Backup dimensions differ')
    require(isinstance(manifest.get('files'), dict) and set(manifest['files']) in (set(FILES), set(FILES) | {'direct-ram.json'}),
            'Unexpected backup files')
    limits = dict(FILES)
    if 'direct-ram.json' in manifest['files']:
        require(image.get('direct_protocol') == 1, 'RAM palette requires exact-image Direct capability')
        limits['direct-ram.json'] = 4096
    files = {name: _read_file(path, name, limit) for name, limit in limits.items()}
    for name, data in files.items():
        require(manifest['files'][name] == _record(data), 'Backup hash/size mismatch: ' + name)
    require(_read_file(path, 'manifest.json', 65536) == raw, 'Backup manifest changed during read')
    require(files['.gitignore'] == b'*\n', 'Backup Git exclusion is missing')
    rom, nvm = files['before-full-rom.bin'], files['saved-nvm.bin']
    validate_rom(rom, profile, (source_ihx, source_code))
    require(nvm == rom[pack.NVM_START:pack.NVM_END], 'Saved NVM differs from the full ROM')
    settings = _json(files['settings.json'])
    expected = settings_from_nvm(nvm, rgb_wire(nvm[24:32], image=image), combos=_combo_capable(profile, source_ihx), direct_capable=image.get('direct_protocol') == 1, settings_version=image.get('settings_record_version', 1))
    for item in expected['keys'] + expected['encoders']:
        if macro_layer_tap_keycode(item['keycode']):
            require(image_keycode_supported(item['keycode'], image,
                    context='encoder' if 'direction' in item else 'matrix'),
                    'Unsupported macro layer tap keycode in backup source')
    for commands in expected['macros']['commands']:
        for command in commands:
            if command.get('command') in ('tap16', 'down16', 'up16'):
                value = int.from_bytes(bytes.fromhex(command['operands_hex']), 'little')
                require(not macro_layer_tap_keycode(value),
                        'Unsupported macro layer tap keycode in backup source macro')
    if 'combos' in expected:
        _validate_combo_actions(expected['combos'], image)
    require(canonical(settings) == canonical(expected), 'Settings JSON differs from validated NVM or RGB contract')
    return {'path': path, 'identity': identity, 'manifest': manifest, 'settings': expected,
            'rom': rom, 'nvm': nvm, 'source_identity': (source_ihx, source_code),
            **({'direct_ram': validate_direct_palette(_json(files['direct-ram.json']))}
               if 'direct-ram.json' in files else {})}


def macro_layer_tap_keycode(code):
    return type(code) is int and 0x40 <= code >> 8 <= 0x45 and 0xF0 <= (code & 255) <= 0xFF


def keycode_supported(code, *, features=(), compact_controls_version=2):
    """Conservative current-build allowlist, including documented tap fallbacks.

    quantum/keymap_common.c, quantum.c, process_rgb.c and enabled key processors
    define this list. Unknown feature namespaces are never silently restored.
    """
    if type(code) is not int or not 0 <= code <= 65535:
        return False
    require(set(features) <= MODULE_FEATURES and len(features) == len(set(features)), 'Unknown settings feature profile')
    if compact_controls_version == 2 and (0x7C50 <= code <= 0x7C52 or 0x7E00 <= code <= 0x7E02):
        return True
    optional = {
        'nkro-control': (0x7011, 0x7012, 0x7013),
        'space-cadet': (0x7C1A, 0x7C1B, 0x7C1E),
        'gui-lock': (0x7009, 0x700A, 0x700B),
        'ctrl-gui-swap': (0x701B, 0x701C, 0x701D),
        'mac-pc': (0x7014, 0x7015, 0x7016),
        'auto-shift': (0x7C13, 0x7C14, 0x7C15),
        'dynamic-macros': tuple(range(0x7C53, 0x7C58)),
        'leader': (0x7C58,),
        'grave-escape': (0x7C16,),
    }
    if any(feature in features and code in values for feature, values in optional.items()):
        return True
    if 'mouse-keys' in features and (0xCD <= code <= 0xD5 or 0xD9 <= code <= 0xDC):
        return True
    if 'tap-dance' in features and 0x5700 <= code <= 0x5707:
        return True
    if 'key-overrides' in features and code in (0x7C5D, 0x7C5E, 0x7C5F):
        return True
    basic = lambda value: (value in (0, 1) or 4 <= value <= 0xC2 or 0xE0 <= value <= 0xE7 or
                           ('mouse-keys' in features and (0xCD <= value <= 0xD5 or 0xD9 <= value <= 0xDC)))
    if code < 256:
        return basic(code)
    if code < 0x4000:  # modifiers; mod-tap retains its existing tap-only fallback
        return basic(code & 255)
    if code < 0x5000:  # layer-tap retains tap-only fallback, known layers only
        return macro_layer_tap_keycode(code) or ((code >> 8) & 15 < 6 and basic(code & 255))
    if code < 0x5200:
        return ((code - 0x5000) >> 5) < 6
    if (code & 0xFFE0) in (0x5200, 0x5220, 0x5240, 0x5260, 0x52C0):
        return (code & 31) < 6
    if 0x52A0 <= code <= 0x52BF:  # existing held-mod OSM fallback, not one-shot
        return True
    return (0x7700 <= code <= 0x770F or 0x7820 <= code <= 0x782A or
            code in (0x7C00, 0x7C01, 0x7C02, 0x7C03, 0x7C73,
                     0x7C77, 0x7C78, 0x7C79, 0x7C7A))


def image_keycode_supported(code, image, *, context='matrix'):
    require(context in ('matrix', 'encoder', 'macro', 'macro-tap', 'macro-down', 'macro-up'), 'Unknown keycode source')
    if macro_layer_tap_keycode(code) and (context != 'matrix' or image.get('macro_layer_tap') is not True):
        return False
    if not keycode_supported(code, features=image.get('features', ()), compact_controls_version=image.get('compact_controls_version', 1)):
        return False
    if 'supported_keycodes' in image and code not in image['supported_keycodes']:
        return False
    # These compact processors admit physical matrix positions only.
    if context != 'matrix' and (0x5700 <= code <= 0x5707 or 0x7C53 <= code <= 0x7C58 or
                                0x7C13 <= code <= 0x7C15 or 0x7C50 <= code <= 0x7C52 or
                                0x7E00 <= code <= 0x7E02):
        return False
    if context.startswith('macro') and 0x7C5D <= code <= 0x7C5F and context != 'macro-tap':
        return False
    if context.startswith('macro') and code in (0x7C1A, 0x7C1B, 0x7C1E):
        return False
    return True


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
    target_schema = int.from_bytes(target_nvm[37:40], 'little')
    pack.validate_nvm(target_nvm, target_schema)
    require(not ('extensions' in backup['settings'] and target_schema != extensions.SCHEMA), 'Schema03 backup downgrade is forbidden')
    require(target_schema == _profile_images(profile)[profile['ihx_sha256']]['build_id'],
            'Target NVM schema differs from exact image')
    settings, nvm = backup['settings'], backup['nvm']
    target_identity = (profile['ihx_sha256'], profile['code_sha256'])
    images = list(_profile_images(profile).values())
    target_image = _profile_images(profile)[profile['ihx_sha256']]
    target_features = target_image.get('features', ())
    require(set(target_features) <= MODULE_FEATURES, 'Unknown settings feature profile')
    source_rank = next(i for i, image in enumerate(images)
                       if (image['ihx_sha256'], image['code_sha256']) == backup['source_identity'])
    target_rank = next(i for i, image in enumerate(images)
                       if (image['ihx_sha256'], image['code_sha256']) == target_identity)
    if 'settings_transitions' in profile:
        require(backup['source_identity'] == target_identity or
                {'source': backup['source_identity'][0], 'target': target_identity[0]} in profile['settings_transitions'],
                'Settings transition is not explicitly reviewed for these exact images')
    else:
        require(source_rank <= target_rank,
                'Settings restore would downgrade firmware; only same-image or approved forward transitions are allowed')
    extension_data = backup['settings'].get('extensions')
    if target_schema == extensions.SCHEMA and extension_data is None:
        extension_data = extensions.from_nvm(target_nvm, version=target_image.get('settings_record_version', 1))
        require(extension_data['qmk_settings'] == extensions.decode_settings(extensions.settings_record(version=target_image.get('settings_record_version', 1))) and
                all(v == bytes(10).hex() for kind in ('tap_dance','key_overrides') for v in extension_data[kind]),
                'Legacy backup cannot overwrite nondefault target extensions')
    if extension_data is not None:
        extension_data = {**extension_data, 'qmk_settings': extensions.normalize_settings(extension_data['qmk_settings'], version=target_image.get('settings_record_version', 1))}
        target_extensions = extensions.from_nvm(target_nvm, version=target_image.get('settings_record_version', 1))
        for kind, feature in (('tap_dance','tap-dance'), ('key_overrides','key-overrides')):
            require(feature in target_features or extension_data[kind] == target_extensions[kind],
                    'Inactive module data differs: ' + kind)
        writable_ids = _image_configuration(target_image)['runtime_qmk_settings']
        for qsid in map(int, extension_data['qmk_settings']):
            require(qsid in writable_ids or extension_data['qmk_settings'][str(qsid)] ==
                    target_extensions['qmk_settings'][str(qsid)], 'Inactive QMK setting differs')
    blockers = []
    combo_entries = None
    if _combo_capable(profile):
        target_combos = combo_settings(target_nvm)
        if 'combos' in settings:
            _validate_combo_actions(settings['combos'], target_image)
            combo_entries = settings['combos']['entries_hex']
        else:
            require(all(data == bytes(10).hex() for data in target_combos['entries_hex']),
                    'Legacy backup has no Combos; existing target Combos must not be cleared')
    else:
        require('combos' not in settings, 'Target firmware does not support Combos')
    for item in settings['keys'] + settings['encoders']:
        context = 'encoder' if 'direction' in item else 'matrix'
        if not image_keycode_supported(item['keycode'], target_image, context=context):
            blockers.append('Unsupported keycode ' + hex(item['keycode']) + ': ' + str(item))
    raw = nvm[24:32]
    source_image = _profile_images(profile)[backup['source_identity'][0]]
    selected_rgb = rgb_wire(raw, selected=True, image=source_image)
    if int.from_bytes(selected_rgb[:2], 'little') not in rgb_modes(target_image).values():
        blockers.append('Saved RGB effect is unsupported by the selected target image')
    if int.from_bytes(selected_rgb[:2], 'little') == 1:
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
                if not image_keycode_supported(value, target_image, context='macro-' + name.removesuffix('16')):
                    blockers.append(f'Unsupported keycode in macro {number}: {value:#06x}')
    require(not blockers, 'Settings cannot be restored before any erase/write:\n' + '\n'.join(blockers))
    return {'extension_features': target_features, 'extension_data': extension_data, 'combo_entries': combo_entries, 'key_count': 498, 'encoder_count': 12, 'macro_chunks': chunks,
            'rgb_saved_mode': selected_rgb, 'rgb_effective_mode': rgb_wire(raw, image=source_image),
            'rgb_saved_config': translated_rgb_config(raw, source_image, target_image),
            'limitations': list(settings['limitations']) + (['Runtime NKRO mode and pending One Shot modifiers are volatile; not restored.']
                if target_features else []), 'requires_physical_unlock': True}


def recheck_source(api, backup, profile):
    backup = validate_backup(backup['path'], profile, backup['identity'])
    rom = api.read_code(0, 65536)
    validate_rom(rom, profile, backup['source_identity'])
    require(rom == backup['rom'], 'Source ROM/settings changed after backup; start a new operation')
    _check_getters(api, backup['settings'], _rom_identity(rom, profile))
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
    expected_settings['limitations'] = actual['limitations']
    if 'extensions' in expected_settings and 'extensions' in actual:
        expected_settings['extensions'] = {**expected_settings['extensions'], 'qmk_settings': extensions.normalize_settings(expected_settings['extensions']['qmk_settings'], version=2 if '22' in actual['extensions']['qmk_settings'] else 1)}
    images = _profile_images(profile)
    rgb = translated_rgb_config(backup['nvm'][24:32], images[backup['source_identity'][0]],
                                images[profile['ihx_sha256']])
    expected_settings['rgb'] = {**expected_settings['rgb'], 'saved_config_hex': rgb.hex()}
    if _combo_capable(profile) and 'combos' not in expected_settings:
        require(all(data == bytes(10).hex() for data in actual['combos']['entries_hex']),
                'Legacy restore target Combos are not empty')
        expected_settings['combos'] = actual['combos']
    if 'extensions' in actual and 'extensions' not in expected_settings:
        expected_settings['extensions'] = actual['extensions']
        require(actual['extensions']['qmk_settings'] == extensions.decode_settings(extensions.settings_record(version=2 if '22' in actual['extensions']['qmk_settings'] else 1)) and all(v == bytes(10).hex() for kind in ('tap_dance','key_overrides') for v in actual['extensions'][kind]), 'Legacy restore target extensions differ')
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
    rgb = plan['rgb_saved_config']
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
    if plan['extension_data'] is not None:
        values = plan['extension_data']
        ids = api.settings_query()
        for qsid in ids:
            value = values['qmk_settings'][str(qsid)]
            if api.get_setting(qsid) != value or qsid in (3, 22):
                write('setting:' + str(qsid), lambda: api.set_setting(qsid, value))
                current = extensions.decode_settings(bytes(expected[0x6A8:0x6C0]), version=2 if '22' in values['qmk_settings'] else 1)
                if current[str(qsid)] != value:
                    current[str(qsid)] = value
                    expected[0x6A8:0x6C0] = extensions.settings_record(current, version=2 if '22' in current else 1)
                durable('setting')
        require(extensions.decode_settings(bytes(expected[0x6A8:0x6C0]), version=2 if '22' in values['qmk_settings'] else 1) == values['qmk_settings'], 'Unexposed settings differ')
        for kind, feature in (('tap_dance','tap-dance'), ('key_overrides','key-overrides')):
            if feature not in plan['extension_features']:
                continue
            for index, raw in enumerate(values[kind]):
                offset = extensions.slot_offset(kind, index)
                data = bytes.fromhex(raw)
                if expected[offset:offset+10] != data:
                    write(kind + ':' + str(index), lambda: api.set_extension(kind, index, data))
                    expected[offset:offset+10] = data
                    durable(kind)
    durable('final settings')
    result = verify_restore(api, backup, profile)
    result.update(writes=writes, target_backup=str(target_backup['path']))
    return result


def validate_direct_palette(value):
    """Validate a separate volatile palette; ROM bytes cannot reconstruct it."""
    require(type(value) is dict and set(value) == {'format','capability','generation','flags','hsv_hex'}
            and value['format'] == 'ak820-direct-ram-1', 'Invalid Direct RAM backup')
    require(type(value['flags']) is int and 0 <= value['flags'] <= 7, 'Invalid Direct RAM flags')
    expected = {'version': 1, 'capabilities': 3, 'count': 82, 'encoding': 'HSV8',
                'mapping': 1, 'maximum_brightness': 160, 'read_chunk': 7,
                'upload_chunk': 8, 'timeout_ms': 1000}
    require(canonical(value['capability']) == canonical(expected), 'Direct RAM capability mismatch')
    require(type(value['generation']) is int and 0 <= value['generation'] <= 0xffffffff,
            'Invalid Direct RAM generation')
    require(type(value['hsv_hex']) is str and len(value['hsv_hex']) == 492,
            'Invalid Direct RAM colors')
    raw = bytes.fromhex(value['hsv_hex'])
    require(raw.hex() == value['hsv_hex'] and all(v <= 160 for v in raw[2::3]), 'Invalid Direct RAM HSV')
    return value


def restore_direct_palette(api, backup, profile, *, frame_id):
    """Explicit separate RAM restore; no mode selection, EEPROM save or retry."""
    require(api.allow_writes, 'Writes are disabled for this DeviceAPI instance')
    backup = validate_backup(backup['path'], profile, backup['identity'])
    palette = validate_direct_palette(backup.get('direct_ram'))
    image = _profile_images(profile)[profile['ihx_sha256']]
    require(image.get('direct_protocol') == 1, 'Target exact image lacks Direct RAM contract')
    # Validate live CODE before issuing any write, using the existing exact-image check.
    rom = api.read_code(0,65536)
    validate_rom(rom, profile, (profile['ihx_sha256'], profile['code_sha256']))
    require(api.direct_info() == palette['capability'], 'Target Direct runtime capability mismatch')
    current = api.direct_snapshot()
    require(current is not None, 'Target Direct palette unavailable')
    result = api.set_direct_frame(bytes.fromhex(palette['hsv_hex']), frame_id=frame_id,
                                  expected_generation=current['generation'])
    actual = api.direct_snapshot()
    require(actual is not None and actual['hsv_hex'] == palette['hsv_hex'], 'Direct RAM restore readback differs')
    return result
