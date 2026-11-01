"""Authenticated previous beta.4.1/current settings transition policy; no device operations."""
from copy import deepcopy
import hashlib
import json

PREVIOUS_BETA_TAG = 'v0.6.0-beta.4.1'
# beta.4 and beta.4.1 published the same settings catalog, byte-for-byte.
PREVIOUS_CATALOG_SHA256 = '8bf90526a51e9879870a61d7de1c59b1df38e3489b77a67e67496503f0307658'
BETA4_IDENTITIES = {
    'main': ('05f49d16b380a8f40b55c3a38c0e863a25d884237d4fd8d6aaef51b6fd95c389', '70cf0f668b3839f67387f01e4cca600b68ceac27c38cb7230d0c4828c390e2de'),
    'game': ('aa7452fb3ebc68b01b4e675c5423b868806ecee6f79b5fe5786be6fd19d9d67a', '8cd041d28df837df230334f2f502b5540dbda7dec779d4d4a2c03d197874834e'),
    'mmo': ('ae5232a4d183d9cecf5b8f1cde917ea14961ed7d8db6b76ee93f85d348ddea54', 'd902e7e828b0cfea888c95e8d8138281e80e513cdf4e442303a637f5187db59f'),
    'typing': ('382e5e965740ce917b165ddc01d8a7078525173882016310a755bbb54a8b63a9', '7293446873b861d18087949547ab7c3ece7eba3c617b751bbed25f7867aa864f'),
    'code': ('fdfeb3cd0d793f54e58c26fa004c2f583db98098a7703a4dec7b0c72925336c3', '0cd0f22230eee4424af3e409670d16c17f9361cc07fda9347a64c82878e5b23a'),
    'pointer': ('c08d1bfefb705df10c17b545d90d156708f0482464de0e9e0aeb66afeb5ba19e', '0f1d088346d23ad50ae70efd27b333f5fc2bdf6c32b60938daa7eb6a4f0887fb'),
    'onehand': ('32bfa36b3b5a9d4b674b69d0b55b891045c43d575c716384aa77a6ebe6e6b99e', '8568924693c33bfb55dd2b8fac1895293dbdda81321059e2b51e6a496d5bd6cf'),
    'creative': ('05c61ebfea8c5d362b8a69e71ec689e26c284137c0a593d1b6501ea1713adbf7', '6be41cc2c497c64df4eaab97cddbed56f07bdff9215085014cb3c8bdb46d4180'),
    'shortcuts': ('1df6f4fc00eb36bca75b2fe8b3a46dbed63529ea00d9474f708dfee51dd1421d', 'b109452ff0dea42f2736a7436e518c5f2c287c0c8a95895308fe3b35ee426a5a'),
    'multios': ('871f9d60715a40261808a5433085cf4f829083c3dd0ae2e1230792dd46522998', '8456cf93ac153b3155b44b44e5bb430e46ffce4d7a5c92681dc28fe851cb3f81'),
}


def require(value, message):
    if not value:
        raise ValueError(message)


def _previous_rows(catalog):
    rows = catalog.get('profiles')
    require(type(rows) is list and [r.get('profile') for r in rows] == list(BETA4_IDENTITIES),
            'Previous beta must contain the exact published ten profiles')
    for row in rows:
        identity = row.get('settings_identity', {})
        require((identity.get('ihx_sha256'), identity.get('code_sha256')) ==
                BETA4_IDENTITIES[row['profile']], 'Previous beta image identity differs')
    require(catalog.get('historical_sources', []) == [], 'Legacy source admission is disabled')
    return deepcopy(rows)


def load_previous_catalog(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PREVIOUS_CATALOG_SHA256,
            'Previous beta catalog differs from authenticated published beta.4.1')
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
    require(type(current) is list and [r.get('profile') for r in current] == list(BETA4_IDENTITIES),
            'New beta must contain the canonical ten profiles')
    current_by_id = {r['settings_identity']['ihx_sha256']: r for r in current}
    require(len(current_by_id) == len(current), 'Duplicate new beta image identity')
    retained = []
    known = dict(current_by_id)
    for row in _previous_rows(previous):
        ihx = row['settings_identity']['ihx_sha256']
        if ihx in known:
            same = known[ihx]
            require(same['settings_identity'] == row['settings_identity'] and
                    same.get('configuration') == row.get('configuration'),
                    'Unchanged image has a conflicting settings contract')
        else:
            retained.append(row)
            known[ihx] = row
    result['historical_sources'] = []
    result['historical_profiles'] = retained
    sources = source_identities(result)
    result['settings_transitions'] = [
        {'source': source, 'target': row['settings_identity']['ihx_sha256']}
        for source in sorted(sources) for row in current]
    result['compatibility_scope'] = (
        'Settings sources are authenticated published beta.4.1 profiles and this beta profiles; '
        'restore targets are this beta only. Earlier releases are unsupported; byte-identical beta.4 identities cannot be distinguished. '
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
            'Backups must cover exactly previous beta.4.1 and current beta images')


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
    expected_pairs = {(source, target) for source in targets for target in targets}
    for field, payload, expected in (
        ('caps_word_combo_cases', 'combo_hex', '0400160000000000737c'),
        ('macro_layer_tap_cases', 'macro_data_sha256', hashlib.sha256(b'x' + bytes(16)).hexdigest()),
    ):
        actions = matrix.get(field)
        require(type(actions) is list and len(actions) == len(expected_pairs),
                'Incomplete action transition cases: ' + field)
        action_seen = set()
        for case in actions:
            require(type(case) is dict, 'Invalid action transition case')
            source, target = case.get('source_profile'), case.get('target_profile')
            require(type(source) is str and type(target) is str and
                    (source, target) in expected_pairs and (source, target) not in action_seen,
                    'Invalid or duplicate action transition pair')
            require(case.get('passed') is True and case.get(payload) == expected and
                    (field != 'macro_layer_tap_cases' or case.get('matrix_keycode') == '0x43f0'),
                    'Invalid action transition payload')
            for side, name in (('source', source), ('target', target)):
                require(all(case.get(side + '_' + key) == targets[name][key]
                            for key in ('ihx_sha256', 'code_sha256')),
                        'Action transition image identity differs')
            action_seen.add((source, target))
        require(action_seen == expected_pairs, 'Incomplete action transition pairs')
    return sources
