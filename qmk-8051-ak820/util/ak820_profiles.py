"""Explicit AK820 build choices; feature costs must be measured after linking.

These are development profiles, not release approvals. The configurator owns
qualification. Keeping every Make switch explicit prevents an inherited
environment variable from silently selecting a different feature set.
"""
from __future__ import annotations

FORMAT = 'ak820-build-configuration-1'
SCHEMA = 0x082002
EXTENSION_SCHEMA = 0x082003
# Historical builders retained by the repository and published alpha.2. Their
# ordinary release checks still verify the actual builder, source and image.
LEGACY_BUILDERS = frozenset({
    '3f7a34aeb8666b0c98878d96ddc3335b4033515943af333449082bc733e93202',
    '166dff0bb41a7a029b8f3c1c8cd57976368e63714458ee26b8fabcf1eb6564a6',
    '4094ceba4c883b70355fb6fefa8a219cb18a0847bfbcb623c1e5833feaf276db',
})
SWITCHES = {
    'nkro': 'AK820_NKRO',
    'grave-escape': 'AK820_GRAVE_ESCAPE',
    'vialrgb-direct': 'AK820_VIALRGB_DIRECT',
    'tap-dance': 'AK820_COMPACT_TAP_DANCE',
    'key-overrides': 'AK820_COMPACT_KEY_OVERRIDE',
    'qmk-settings': 'AK820_QMK_SETTINGS',
    'mac-pc': 'AK820_MAC_PC',
    'os-indicators': 'AK820_OS_INDICATORS',
    'leader': 'AK820_COMPACT_LEADER',
    'nkro-control': 'AK820_NKRO_CONTROL',
    'one-shot': 'AK820_COMPACT_ONESHOT',
    'space-cadet': 'AK820_COMPACT_SPACE_CADET',
    'mouse-keys': 'AK820_COMPACT_MOUSEKEY',
    'auto-shift': 'AK820_COMPACT_AUTOSHIFT',
    'gui-lock': 'AK820_COMPACT_GUI_LOCK',
    'ctrl-gui-swap': 'AK820_COMPACT_CTRL_GUI_SWAP',
    'dynamic-macros': 'AK820_COMPACT_DYNAMIC_MACRO',
}
DEFAULT_PROFILE = 'main'
# The desktop and release builder offer these broad, finite feature packages.
# Historical names below remain usable to reproduce earlier development builds.
RELEASE_PROFILES = ('main', 'game', 'mmo', 'typing', 'code', 'pointer',
                    'onehand', 'creative', 'shortcuts', 'multios')

PROFILES = {
    # Development-only union used to measure whole-program compression.
    'maximal': tuple(SWITCHES),
    'work': ('nkro-control', 'one-shot', 'space-cadet', 'leader',
             'dynamic-macros', 'os-indicators'),
    'essential': ('nkro-control', 'one-shot', 'space-cadet', 'os-indicators'),
    'legacy-typing': ('nkro-control', 'one-shot', 'space-cadet', 'auto-shift', 'os-indicators'),
    'mouse': ('nkro-control', 'one-shot', 'space-cadet', 'mouse-keys', 'os-indicators'),
    'mouse-typing': ('nkro-control', 'one-shot', 'space-cadet', 'mouse-keys',
                     'auto-shift', 'gui-lock', 'os-indicators'),
    'system': ('nkro-control', 'one-shot', 'space-cadet', 'gui-lock',
               'ctrl-gui-swap', 'mac-pc', 'os-indicators'),
    'tap-dance': ('nkro-control', 'one-shot', 'space-cadet', 'tap-dance'),
    'key-overrides': ('nkro-control', 'one-shot', 'space-cadet', 'key-overrides'),
    'settings': ('nkro-control', 'one-shot', 'space-cadet', 'qmk-settings'),
    'full-tap-dance': ('nkro-control', 'one-shot', 'space-cadet', 'tap-dance'),
    'full-key-overrides': ('nkro-control', 'one-shot', 'space-cadet', 'key-overrides'),
    'full-qmk-settings': ('nkro-control', 'one-shot', 'space-cadet', 'qmk-settings'),
    'full-mac-pc': ('nkro-control', 'one-shot', 'space-cadet', 'mac-pc'),
    'full-mac-pc-os-indicators': ('nkro-control', 'one-shot', 'space-cadet', 'mac-pc', 'os-indicators'),
    'full-os-indicators': ('nkro-control', 'one-shot', 'space-cadet', 'os-indicators'),
    'full-leader': ('nkro-control', 'one-shot', 'space-cadet', 'leader'),
    'standard': (),
    'nkro': ('nkro-control',),
    'one-shot': ('one-shot',),
    'nkro-one-shot': ('nkro-control', 'one-shot'),
    'space-cadet': ('space-cadet',),
    'nkro-space-cadet': ('nkro-control', 'space-cadet'),
    'one-shot-space-cadet': ('one-shot', 'space-cadet'),
    'full': ('nkro-control', 'one-shot', 'space-cadet'),
    'full-gui-lock': ('nkro-control', 'one-shot', 'space-cadet', 'gui-lock'),
    'full-ctrl-gui': ('nkro-control', 'one-shot', 'space-cadet', 'gui-lock', 'ctrl-gui-swap'),
    'full-dynamic-macro-gui': ('nkro-control', 'one-shot', 'space-cadet', 'dynamic-macros', 'gui-lock'),
    'full-mouse-auto-shift-gui': ('nkro-control', 'one-shot', 'space-cadet', 'mouse-keys', 'auto-shift', 'gui-lock'),
    'full-auto-shift-dynamic-macro': ('nkro-control', 'one-shot', 'space-cadet', 'auto-shift', 'dynamic-macros'),
    'full-dynamic-macro': ('nkro-control', 'one-shot', 'space-cadet', 'dynamic-macros'),
    'full-mouse': ('nkro-control', 'one-shot', 'space-cadet', 'mouse-keys'),
    'full-auto-shift': ('nkro-control', 'one-shot', 'space-cadet', 'auto-shift'),
    'full-mouse-auto-shift': ('nkro-control', 'one-shot', 'space-cadet', 'mouse-keys', 'auto-shift'),
}
# Retain the historical feature sets under unambiguous names. The old
# firmware always included NKRO, Grave Escape and Direct.
PROFILES = {name: tuple(dict.fromkeys(tuple(features) + ('nkro', 'grave-escape', 'vialrgb-direct')))
            for name, features in PROFILES.items()}
_MAIN = ('one-shot', 'leader', 'dynamic-macros', 'os-indicators',
         'qmk-settings', 'key-overrides', 'vialrgb-direct')
def _variant(remove=(), add=()):
    return tuple(feature for feature in _MAIN if feature not in remove) + tuple(add)
PROFILES = {
    'main': _MAIN,
    'game': _variant(('leader',), ('nkro', 'nkro-control', 'gui-lock')),
    'mmo': _variant(('leader', 'key-overrides'), ('nkro', 'nkro-control', 'gui-lock', 'tap-dance')),
    'typing': _variant(('vialrgb-direct',), ('auto-shift', 'space-cadet')),
    'code': _variant(('vialrgb-direct',), ('space-cadet', 'grave-escape')),
    'pointer': _variant(('vialrgb-direct',), ('mouse-keys',)),
    'onehand': _variant(('vialrgb-direct', 'key-overrides'), ('mouse-keys', 'tap-dance')),
    'creative': _variant(('key-overrides',), ('tap-dance',)),
    'shortcuts': _variant(('vialrgb-direct', 'dynamic-macros'), ('tap-dance',)),
    'multios': _variant(('vialrgb-direct',), ('mac-pc', 'ctrl-gui-swap')),
    **PROFILES,
}
CONFLICTS = []
BASE_FEATURES = (
    'six-layers', 'sixteen-vial-macros', 'eight-two-key-combos',
    'compact-tap-hold', 'encoder-map', 'media-keys',
    'caps-word', 'repeat', 'alternate-repeat', 'tri-layer',
    'rgb-effects',
)
DEFERRED = {
    'magic': 'Additional swaps, Caps variants and persistent Magic settings are outside the bounded module contract; Ctrl/GUI and Alt/GUI swaps are session-only.',
}


def configuration(name: str) -> dict:
    if not isinstance(name, str) or name not in PROFILES:
        raise ValueError('Unknown profile: ' + str(name))
    enabled = PROFILES[name]
    return {
        'format': FORMAT, 'profile': name, 'optional_features': list(enabled),
        'base_features': list(BASE_FEATURES) + [label for feature, label in
            (('nkro', 'nkro-reports'), ('grave-escape', 'grave-escape'),
             ('vialrgb-direct', 'vialrgb-direct-ram')) if feature in enabled],
        'nvm_schema': EXTENSION_SCHEMA if any(f in enabled for f in ('tap-dance', 'key-overrides', 'qmk-settings')) else SCHEMA,
        'make_options': {switch: 'yes' if feature in enabled else 'no'
                         for feature, switch in SWITCHES.items()},
        'runtime_qmk_settings': ([1, 2, 4, 7, 18, 19] if 'auto-shift' in enabled else [1, 2, 7, 18, 19]) if 'qmk-settings' in enabled else [],
        'timing_ms': {'combo': 40, 'tap_hold': 200,
                      **({'os_indicator_lease': 3000, 'os_indicator_period': 4096}
                         if 'os-indicators' in enabled else {}),
                      **({'leader': 300} if 'leader' in enabled else {}),
                      **({'mouse_cursor': 20, 'mouse_wheel': 80} if 'mouse-keys' in enabled else {}),
                      **({'auto_shift': 175} if 'auto-shift' in enabled else {}),
                      **({'dynamic_macro_phase': 10} if 'dynamic-macros' in enabled else {})},
        'release_approved': False,
    }


def select(features: list[str]) -> str:
    if len(features) != len(set(features)):
        raise ValueError('Repeated feature selection')
    unknown = set(features) - SWITCHES.keys()
    if unknown:
        raise ValueError('Unsupported feature selection: ' + ', '.join(sorted(unknown)))
    for name, enabled in PROFILES.items():
        if set(features) == set(enabled):
            return name
    if not set(features) & {'nkro', 'grave-escape', 'vialrgb-direct'}:
        historical = set(features) | {'nkro', 'grave-escape', 'vialrgb-direct'}
        for name, enabled in PROFILES.items():
            if name not in RELEASE_PROFILES and historical == set(enabled):
                return name
    raise ValueError('This feature combination has no supported profile')


def legacy_configuration(name: str) -> dict:
    """Reconstruct beta.1 metadata for backup readers; never build or qualify it.

    New builds use configuration(), including legacy-typing when reproducing
    the historical Typing feature set. Historical metadata keeps its old name.
    """
    selected = 'legacy-typing' if name == 'typing' else name
    if selected in RELEASE_PROFILES or selected not in PROFILES:
        raise ValueError('Unknown historical profile: ' + str(name))
    value = configuration(selected)
    value['profile'] = name
    positive = {'nkro', 'grave-escape', 'vialrgb-direct'}
    value['optional_features'] = [feature for feature in value['optional_features'] if feature not in positive]
    value['make_options'] = {switch: setting for switch, setting in value['make_options'].items()
                             if switch not in {SWITCHES[feature] for feature in positive}}
    value['base_features'] = [
        'six-layers', 'sixteen-vial-macros', 'eight-two-key-combos',
        'compact-tap-hold', 'encoder-map', 'media-keys', 'nkro-reports',
        'caps-word', 'repeat', 'alternate-repeat', 'grave-escape', 'tri-layer',
        'rgb-effects', 'vialrgb-direct-ram',
    ]
    return value


def validate_legacy_configuration(value: dict) -> dict:
    """Validate frozen historical metadata without granting current approval."""
    if not isinstance(value, dict) or value != legacy_configuration(value.get('profile')):
        raise ValueError('Historical configuration differs from its original profile')
    return value


def validate_configuration(value: dict) -> dict:
    if not isinstance(value, dict) or value != configuration(value.get('profile')):
        raise ValueError('Build configuration differs from the selected profile')
    return value


def require_release_qualification(report: dict) -> None:
    """Keep new development profiles out of both existing release builders.

    Historical reports predate profile selection and retain their exact-image
    release policy. Configured images require the committed exact-image safety
    witnesses as well as the caller's existing build/review checks.
    """
    if 'configuration' in report:
        validate_configuration(report['configuration'])
        from ak820_release_safety import validate
        validate(report)
        return
    if report.get('builder_sha256') not in LEGACY_BUILDERS or any(
            row.get('origin') == 'source' and row.get('path', '').replace('\\', '/') == 'util/ak820_profiles.py'
            for row in report.get('sources', [])):
        raise ValueError('Missing configuration is not legacy provenance; development build is not approved')
