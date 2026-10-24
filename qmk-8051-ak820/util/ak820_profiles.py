"""Explicit AK820 build choices; feature costs must be measured after linking.

These are development profiles, not release approvals. The configurator owns
qualification. Keeping every Make switch explicit prevents an inherited
environment variable from silently selecting a different feature set.
"""
from __future__ import annotations

FORMAT = 'ak820-build-configuration-1'
SCHEMA = 0x082002
# Historical builders retained by the repository and published alpha.2. Their
# ordinary release checks still verify the actual builder, source and image.
LEGACY_BUILDERS = frozenset({
    '3f7a34aeb8666b0c98878d96ddc3335b4033515943af333449082bc733e93202',
    '166dff0bb41a7a029b8f3c1c8cd57976368e63714458ee26b8fabcf1eb6564a6',
    '4094ceba4c883b70355fb6fefa8a219cb18a0847bfbcb623c1e5833feaf276db',
})
SWITCHES = {
    'nkro-control': 'AK820_NKRO_CONTROL',
    'one-shot': 'AK820_COMPACT_ONESHOT',
    'space-cadet': 'AK820_COMPACT_SPACE_CADET',
    'mouse-keys': 'AK820_COMPACT_MOUSEKEY',
    'auto-shift': 'AK820_COMPACT_AUTOSHIFT',
    'gui-lock': 'AK820_COMPACT_GUI_LOCK',
    'ctrl-gui-swap': 'AK820_COMPACT_CTRL_GUI_SWAP',
    'dynamic-macros': 'AK820_COMPACT_DYNAMIC_MACRO',
}
PROFILES = {
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
CONFLICTS = []
BASE_FEATURES = (
    'six-layers', 'sixteen-vial-macros', 'eight-two-key-combos',
    'compact-tap-hold', 'encoder-map', 'media-keys', 'nkro-reports',
    'caps-word', 'repeat', 'alternate-repeat', 'grave-escape', 'tri-layer',
    'rgb-effects', 'vialrgb-direct-ram',
)
DEFERRED = {
    'qmk-settings': 'Requires a versioned saved extension and typed backup/restore; upstream layout moves Combos.',
    'tap-dance': 'Dynamic entries, input ownership and complete-image cost are not qualified.',
    'key-overrides': 'Modifier ownership, Repeat, Caps Word and macro interactions are not qualified.',
    'magic': 'Other modifier swaps and persistent Magic settings remain deferred; Ctrl/GUI swap is volatile and session-only.',
    'leader': 'Sequence length, timeout and supported output actions are not qualified.',
}


def configuration(name: str) -> dict:
    if not isinstance(name, str) or name not in PROFILES:
        raise ValueError('Unknown profile: ' + str(name))
    enabled = PROFILES[name]
    return {
        'format': FORMAT, 'profile': name, 'optional_features': list(enabled),
        'base_features': list(BASE_FEATURES), 'nvm_schema': SCHEMA,
        'make_options': {switch: 'yes' if feature in enabled else 'no'
                         for feature, switch in SWITCHES.items()},
        'runtime_qmk_settings': [],
        'timing_ms': {'combo': 40, 'tap_hold': 200,
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
    raise ValueError('This feature combination has no tested profile')


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
