#!/usr/bin/env python3
"""Source-derived canonical pass30 compiler inputs; not a release approval gate."""
import json
from pathlib import Path

from ak820_build_inputs import dependency_paths, digest
from ak820_capture_compile import validate_default_keymap, validate_manifest
from ak820_pointer_compile_environment import validate_pointer_environment
from ak820_pointer_compile_policy import expected_flags as pointer_flags, expected_units as pointer_units, validate_pointer_arguments
from ak820_profiles import configuration

POLICY = 'ak820-canonical-pass30-inputs-1'
# Feature lists and Make options are frozen independently of the profile registry.
FEATURES = {
    'main': 'one-shot leader dynamic-macros os-indicators qmk-settings key-overrides vialrgb-direct auto-shift',
    'game': 'one-shot dynamic-macros os-indicators qmk-settings key-overrides vialrgb-direct nkro nkro-control gui-lock',
    'mmo': 'one-shot dynamic-macros os-indicators qmk-settings vialrgb-direct nkro nkro-control gui-lock tap-dance',
    'typing': 'one-shot leader dynamic-macros os-indicators qmk-settings key-overrides auto-shift space-cadet tap-dance',
    'code': 'one-shot leader dynamic-macros os-indicators qmk-settings key-overrides space-cadet grave-escape tap-dance',
    'pointer': 'one-shot leader dynamic-macros os-indicators qmk-settings key-overrides mouse-keys tap-dance',
    'onehand': 'one-shot leader dynamic-macros os-indicators qmk-settings mouse-keys tap-dance',
    'creative': 'one-shot leader dynamic-macros os-indicators qmk-settings vialrgb-direct tap-dance nkro nkro-control',
    'shortcuts': 'one-shot leader dynamic-macros os-indicators qmk-settings key-overrides tap-dance nkro nkro-control',
    'multios': 'one-shot leader dynamic-macros os-indicators qmk-settings key-overrides mac-pc ctrl-gui-swap tap-dance',
}

SWITCHES = dict(pair.split('=') for pair in '''
nkro=AK820_NKRO grave-escape=AK820_GRAVE_ESCAPE vialrgb-direct=AK820_VIALRGB_DIRECT
 tap-dance=AK820_COMPACT_TAP_DANCE key-overrides=AK820_COMPACT_KEY_OVERRIDE
 qmk-settings=AK820_QMK_SETTINGS mac-pc=AK820_MAC_PC os-indicators=AK820_OS_INDICATORS
 leader=AK820_COMPACT_LEADER nkro-control=AK820_NKRO_CONTROL one-shot=AK820_COMPACT_ONESHOT
 space-cadet=AK820_COMPACT_SPACE_CADET mouse-keys=AK820_COMPACT_MOUSEKEY
 auto-shift=AK820_COMPACT_AUTOSHIFT gui-lock=AK820_COMPACT_GUI_LOCK
 ctrl-gui-swap=AK820_COMPACT_CTRL_GUI_SWAP dynamic-macros=AK820_COMPACT_DYNAMIC_MACRO
'''.split())


def canonical(value):
    if not isinstance(value, dict) or not isinstance(value.get('profile'), str) or value['profile'] not in FEATURES:
        raise ValueError('Unknown canonical profile')
    name = value['profile']
    expected = configuration(name)
    # JSON comparison also distinguishes booleans from integers.
    features = FEATURES[name].split()
    options = {switch: 'yes' if feature in features else 'no' for feature, switch in SWITCHES.items()}
    if (expected['optional_features'] != features or expected['make_options'] != options or
            json.dumps(value, sort_keys=True) != json.dumps(expected, sort_keys=True)):
        raise ValueError('Noncanonical profile configuration')
    return name


def expected_units(name, obj):
    if name not in FEATURES:
        raise ValueError('Unknown canonical profile')
    units = pointer_units(obj)
    enabled = set(FEATURES[name].split())
    for feature, path in [('mouse-keys', 'keyboards/ajazz/ak820/ak820_mousekey'),
                          ('leader', 'ak820_leader'), ('tap-dance', 'ak820_tap_dance'),
                          ('key-overrides', 'ak820_key_override')]:
        if feature not in enabled:
            del units[obj + '/' + path + '.o']
    if 'auto-shift' in enabled:
        units[obj + '/ak820_autoshift.o'] = 'keyboards/ajazz/ak820/ak820_autoshift.c'
    if 'grave-escape' in enabled:
        path = 'quantum/process_keycode/process_grave_esc'
        units[obj + '/' + path + '.o'] = path + '.c'
    return units


def expected_flags(name, obj):
    if name not in FEATURES:
        raise ValueError('Unknown canonical profile')
    enabled = set(FEATURES[name].split())
    flags = pointer_flags(obj)
    start, end = flags.index('-DVIALRGB_NO_DIRECT'), flags.index('-DAK820_QMK_SETTINGS')
    board = []
    for feature, token in [
        ('nkro', '-DAK820_NKRO'), ('grave-escape', '-DAK820_GRAVE_ESCAPE'),
        ('auto-shift', '-DAK820_COMPACT_AUTOSHIFT'),
        ('vialrgb-direct', '-DAK820_VIALRGB_DIRECT'), ('nkro-control', '-DAK820_NKRO_CONTROL'),
        ('one-shot', '-DAK820_COMPACT_ONESHOT'), ('space-cadet', '-DAK820_COMPACT_SPACE_CADET'),
        ('mouse-keys', '-DAK820_COMPACT_MOUSEKEY'), ('mouse-keys', '-DAK820_MOUSE_CURSOR_STEP=8'),
        ('mouse-keys', '-DAK820_MOUSE_CURSOR_PERIOD=20'), ('mouse-keys', '-DAK820_MOUSE_WHEEL_STEP=1'),
        ('mouse-keys', '-DAK820_MOUSE_WHEEL_PERIOD=80'), ('dynamic-macros', '-DAK820_COMPACT_DYNAMIC_MACRO'),
        ('gui-lock', '-DAK820_COMPACT_GUI_LOCK'), ('ctrl-gui-swap', '-DAK820_COMPACT_CTRL_GUI_SWAP'),
        ('leader', '-DAK820_COMPACT_LEADER'), ('os-indicators', '-DAK820_OS_INDICATORS'),
        ('mac-pc', '-DAK820_MAC_PC'), ('tap-dance', '-DAK820_COMPACT_TAP_DANCE'),
        ('key-overrides', '-DAK820_COMPACT_KEY_OVERRIDE')]:
        if feature == 'vialrgb-direct' and feature not in enabled:
            board.append('-DVIALRGB_NO_DIRECT')
        elif feature in enabled:
            board.append(token)
    flags[start:end] = board
    if 'mouse-keys' not in enabled:
        for token in ('-DMOUSEKEY_ENABLE', '-DMOUSE_ENABLE', '-DMOUSE_SHARED_EP'):
            flags.remove(token)
    if 'grave-escape' in enabled:
        flags.insert(flags.index('-DREPEAT_KEY_ENABLE'), '-DGRAVE_ESC_ENABLE')
    if 'nkro' in enabled:
        flags.insert(flags.index('-DSHARED_EP_ENABLE'), '-DNKRO_ENABLE')
    return flags


def validate_commands(root, build, objects, toolchain, qmk_bin, selected):
    name = canonical(selected)
    root, build = Path(root).resolve(), Path(build).resolve()
    obj = (build / 'obj_ajazz_ak820_vial').relative_to(root).as_posix()
    units = expected_units(name, obj)
    expected = {path[:-2] + '.rel' for path in units}
    if len(objects) != len(expected) or set(objects) != expected:
        raise ValueError('Canonical object membership differs from policy')
    captures = validate_manifest(root, build, objects, build / 'obj_ajazz_ak820_vial')
    flags = expected_flags(name, obj)
    sources, wrappers = set(), 0
    for path in captures:
        data = json.loads(path.read_text(encoding='utf-8'))
        validate_pointer_environment(data.get('environment'), root, build, toolchain, qmk_bin)
        output = path.relative_to(root).as_posix()[:-len('.compile.json')]
        dep = output[:-2] + '.d'
        source = units.get(output)
        if source is None or source in sources or not output.startswith(obj + '/'):
            raise ValueError('Canonical object/source mapping differs from policy')
        wrappers += validate_pointer_arguments(data['argv'], flags, dep, source, output) == 'wrapper'
        paths = dependency_paths(root / dep, root, target=Path(output).name, primary=source)
        if data.get('generated_inputs') != {str(p): digest(p) for p in paths if p.is_relative_to(build)}:
            raise ValueError('Generated compiler input evidence differs: ' + output)
        sources.add(source)
    if wrappers != 1:
        raise ValueError('Expected one compressed default-keymap invocation')
    validate_default_keymap(captures, build)
    return POLICY
