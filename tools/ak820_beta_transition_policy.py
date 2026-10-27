"""Exact previous-beta-only settings transition policy; no device operations."""
from copy import deepcopy
import hashlib
import json

PREVIOUS_BETA_TAG = 'v0.6.0-beta.3'
PREVIOUS_CATALOG_SHA256 = 'd07cbc6bb562e84193f6de121733d13e21aceb129b653e9ff97ae954da36920c'
# Published beta.3 profile identities, retained unchanged for source validation.
PREVIOUS_IDENTITIES = {'main': ('391d6dbca948b46cfc4be989b0055f310fbdfaf832bdc634c76ff2bf5e23b34e', 'd1a9421a865be4a46c6fef546a5bd7aa906eda21880debcec2dc8885e70ffa14'), 'game': ('5351cfafa6eb8bc55272c55e67f86d60ab0dac04809cbe3f25df14c2137f5005', '7e7ea48b2cc2eea8072fdb517f7a86bc241b0be7bb267ce73635a8ffde1151d9'), 'mmo': ('963aff70931a3ac4530fa8a8fd9f2dd4ad43125c3dce963ce1c8a7cce3009821', '91554fe0d9eaa32fa636a213973956d619e23f351d92e97d74ef2530aa04d923'), 'typing': ('57ec708eb400a885b6c1b803d934383709e9942688e619299259d0a0068fda14', '95d79868a22b01a120503e8015cc602a5486ee76906d820e53578229e758444f'), 'code': ('35803dda2c647d7b4b1c2208de2b7ce9a03405a6d87d05e0d3f5e91d5ff195fb', '7990de5224b91332592c423fd966ecfa5c2719eecdd406d2836754f79bf70d47'), 'pointer': ('6a97adeb76cc6333ee465b3b75dc000093843b884c08167e65a33f2ebba36946', 'baf75ef3479954ac6032a2f39bd6d28d0f51ffbe7ca7f6c92bbff6d00a991395'), 'onehand': ('f78f5f91f8382da4e8b60709a46b0e5cfb022f9a5cb925082434b04a3fb0fb8f', '1fe51dafd668feda3eaf25ed1ff9475e046e7d4c360dfbff6ba2cd0802a81374'), 'creative': ('476b1c667613712dfe302a4518f6bbd947bf994bc9e6fcb05323d5544b2b8c38', '8526e40cc1404a22d2aaf802ec4846c4dde8303167d101bf7114b5b9b906ca23'), 'shortcuts': ('3154808d2012f55b5c46098d52c96bc5a0056bcfb9a4c8e3ec991090aab45f64', 'ad24be0e1ffb3c184baa5ec382b19d183722f92fec5550961927282fe0703861'), 'multios': ('670b523bdc1a3e6eb28a3e874574bd3ba64eb7357d7040b40278a8ed37157a9f', '098c385abdf630eaf65553b252063f310d6bb76486143bac06c5bd4a4d2df4b8')}


def require(value, message):
    if not value:
        raise ValueError(message)


def _previous_rows(catalog):
    rows = catalog.get('profiles')
    require(type(rows) is list and [r.get('profile') for r in rows] == list(PREVIOUS_IDENTITIES),
            'Previous beta must contain the exact published ten profiles')
    for row in rows:
        identity = row.get('settings_identity', {})
        require((identity.get('ihx_sha256'), identity.get('code_sha256')) ==
                PREVIOUS_IDENTITIES[row['profile']], 'Previous beta image identity differs')
    return deepcopy(rows)


def load_previous_catalog(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PREVIOUS_CATALOG_SHA256,
            'Previous beta catalog differs from authenticated published beta.3')
    catalog = json.loads(raw)
    _previous_rows(catalog)
    return catalog


def previous_source_catalog(previous):
    result = deepcopy(previous)
    result['profiles'] = []
    result['historical_profiles'] = _previous_rows(previous)
    result['historical_sources'] = []
    result['settings_transitions'] = []
    return result


def compose_catalog(fresh, previous):
    """Keep previous published images as sources, never as restore targets."""
    result = deepcopy(fresh)
    current = result.get('profiles')
    require(type(current) is list and [r.get('profile') for r in current] == list(PREVIOUS_IDENTITIES),
            'New beta must contain the canonical ten profiles')
    current_by_id = {r['settings_identity']['ihx_sha256']: r for r in current}
    require(len(current_by_id) == len(current), 'Duplicate new beta image identity')
    retained = []
    for row in _previous_rows(previous):
        ihx = row['settings_identity']['ihx_sha256']
        if ihx in current_by_id:
            same = current_by_id[ihx]
            require(same['settings_identity'] == row['settings_identity'] and
                    same.get('configuration') == row.get('configuration'),
                    'Unchanged image has a conflicting settings contract')
        else:
            retained.append(row)
    result['historical_sources'] = []
    result['historical_profiles'] = retained
    sources = source_identities(result)
    result['settings_transitions'] = [
        {'source': source, 'target': row['settings_identity']['ihx_sha256']}
        for source in sorted(sources) for row in current]
    result['compatibility_scope'] = (
        'Settings sources are exact published beta.3 profiles and this beta profiles; '
        'restore targets are this beta only. Earlier releases are unsupported. '
        'Offline plans do not prove physical restore.')
    return result


def source_identities(catalog):
    require(catalog.get('historical_sources', []) == [], 'Legacy source admission is disabled')
    identities = {}
    for row in catalog['profiles'] + catalog.get('historical_profiles', []):
        image = row['settings_identity']
        pair = (image['ihx_sha256'], image['code_sha256'])
        require(all(type(h) is str and len(h) == 64 and all(c in '0123456789abcdef' for c in h)
                    for h in pair), 'Malformed settings image identity')
        require(pair[0] not in identities, 'Duplicate settings image identity')
        identities[pair[0]] = pair[1]
    return identities


def validate_backup_scope(backups, catalog):
    """Require complete exact previous/current coverage and reject older sources."""
    expected = set(source_identities(catalog).items())
    actual = {tuple(backup['source_identity']) for backup in backups.values()}
    require(len(actual) == len(backups), 'Duplicate backup image identity')
    require(actual == expected,
            'Backups must cover exactly previous beta.3 and current beta images')


def validate_catalog_scope(catalog, previous):
    """Reject transitive ancestry, rollback edges and altered previous contracts."""
    expected = compose_catalog({'profiles': catalog['profiles']}, previous)
    for key in ('historical_sources', 'historical_profiles', 'settings_transitions'):
        require(catalog.get(key) == expected[key], 'Previous/current catalog scope differs: ' + key)
    return source_identities(catalog)


def validate_transition_matrix(matrix, catalog, previous):
    """Bind a complete exact-image source/target matrix to the reviewed scope."""
    sources = validate_catalog_scope(catalog, previous)
    targets = {r['profile']: r['settings_identity'] for r in catalog['profiles']}
    require(matrix.get('format') == 'ak820-settings-transition-matrix-2'
            and matrix.get('offline_only') is True and matrix.get('hardware_validated') is False
            and type(matrix.get('physical_device_commands')) is int
            and matrix['physical_device_commands'] == 0
            and type(matrix.get('sources_per_target')) is int
            and matrix['sources_per_target'] == len(sources), 'Invalid beta transition matrix scope')
    cases = matrix.get('cases')
    require(type(cases) is list and len(cases) == len(sources) * len(targets),
            'Incomplete beta transition matrix')
    seen = set()
    labels = {}
    source_records = {}
    for case in cases:
        require(type(case) is dict, 'Invalid beta transition case')
        source, name = case.get('source'), case.get('target_profile')
        require(source in sources and name in targets, 'Out-of-scope beta transition source/target')
        target = targets[name]
        require(case.get('source_code_sha256') == sources[source]
                and case.get('target') == target['ihx_sha256']
                and case.get('target_code_sha256') == target['code_sha256'],
                'Beta transition exact image identity differs')
        pair = (source, name)
        require(pair not in seen, 'Duplicate beta transition case')
        seen.add(pair)
        label = case.get('source_case')
        require(type(label) is str and bool(label), 'Missing beta source label')
        require(source not in labels or labels[source] == label, 'Inconsistent beta source label')
        require(label not in labels.values() or labels.get(source) == label, 'Ambiguous beta source label')
        labels[source] = label
        require(case.get('passed') is True and case.get('offline_only') is True
                and type(case.get('physical_device_commands')) is int
                and case['physical_device_commands'] == 0
                and type(case.get('key_count')) is int and case['key_count'] == 498
                and type(case.get('encoder_count')) is int and case['encoder_count'] == 12
                and type(case.get('combo_count')) is int and case['combo_count'] == 8
                and type(case.get('source_scope')) is str and bool(case['source_scope'])
                and type(case.get('backup_manifest_sha256')) is str
                and len(case['backup_manifest_sha256']) == 64
                and all(c in '0123456789abcdef' for c in case['backup_manifest_sha256']),
                'Beta transition case not qualified')
        binding = (label, case['source_scope'], case['backup_manifest_sha256'])
        require(source not in source_records or source_records[source] == binding,
                'Beta transition source backup differs across targets')
        source_records[source] = binding
    require(seen == {(source, name) for source in sources for name in targets},
            'Incomplete beta transition source/target pairs')
    return sources
