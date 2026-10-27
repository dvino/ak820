"""Validate reviewed, exact-image release witnesses without device access.

The committed witness manifest records independent review, not a signature.
CI additionally enforces the program policy and reproduces the approved image.
No caller-supplied approval boolean or standalone stack number grants approval.
"""
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

import pack_ak820
from ak820_profiles import RELEASE_PROFILES, validate_configuration

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import ak820_beta_transition_policy as beta_policy
REQUIRED_SOURCES = frozenset((
    'qmk-8051-ak820/util/ak820_release_safety.py',
    'qmk-8051-ak820/util/ak820_profiles.py',
    'qmk-8051-ak820/util/ak820_linked_inventory.py',
    'qmk-8051-ak820/util/pack_ak820.py',
    'qmk-8051-ak820/tests/ak820_stack/analyze.py',
    'qmk-8051-ak820/tests/ak820_irq/run.py',
    'qmk-8051-ak820/tests/ak820_startup/stack_contract.py',
    'qmk-8051-ak820/quantum/dynamic_keymap.c',
    'qmk-8051-ak820/quantum/repeat_key.c',
    'tools/installer/settings_backup.py', 'tools/installer/settings_workflow.py',
    'tools/ak820_device_protocol.py',
    'tools/installer/test_settings_backup.py', 'tools/installer/test_settings_workflow.py',
    'tools/ak820_beta_transition_policy.py',
    'tools/test_ak820_beta_transition_policy.py',
    'tools/test_release_safety.py',
    'audits/beta3-direct-20261026/prepare_release.py',
))
ROOT_NAMES = {'_main', '_ak820_timer_irq', '_USB_DeviceInterrupt', '_ak820_led_irq'}


def require(value, message):
    if not value:
        raise ValueError('Release safety not approved: ' + message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, 'duplicate JSON field')
            value[key] = item
        return value
    value = json.loads(path.read_text(), object_pairs_hook=unique,
                       parse_constant=lambda item: (_ for _ in ()).throw(ValueError('Invalid JSON number')))
    require(isinstance(value, dict), 'expected a JSON object')
    return value


def safe_path(root, name):
    require(isinstance(name, str) and name and '\\' not in name
            and not name.startswith('/') and all(p not in ('', '.', '..') for p in name.split('/')),
            'unsafe witness/source path')
    path = root
    for part in name.split('/'):
        path = path / part
        require(not path.is_symlink(), 'symlink in witness/source path')
    require(path.resolve().is_relative_to(root.resolve()) and path.is_file(), 'missing witness/source: ' + name)
    return path


def checked_record(root, name, record):
    path = safe_path(root, name)
    require(isinstance(record, dict) and type(record.get('size')) is int
            and path.stat().st_size == record['size'] and sha(path.read_bytes()) == record.get('sha256'),
            'changed witness/source: ' + name)
    return path


def number(value, name):
    require(type(value) is int and 0 <= value <= 256, 'invalid ' + name)
    return value


def manifest_name(configuration):
    """Select a mandatory exact-profile witness; never fall back if absent."""
    selected = validate_configuration(configuration)
    name = selected['profile']
    return ('ci/profiles/' + name + '/release-safety.json'
            if name in RELEASE_PROFILES else 'ci/release-safety.json')


def validate_beta_preflight(transition, root, ihx_hash, configuration, sources):
    """Validate the complete reviewed previous/current matrix, with no legacy fallback."""
    documents = {}
    for key in ('previous_beta_catalog', 'settings_catalog', 'preflight_matrix'):
        reference = transition.get(key)
        require(type(reference) is dict and set(reference) == {'path', 'size', 'sha256'},
                'missing beta transition evidence: ' + key)
        name = reference['path']
        require(name in sources and sources[name] == {k: reference[k] for k in ('size', 'sha256')},
                'beta transition evidence absent from reviewed sources: ' + key)
        documents[key] = checked_record(root, name, reference)
    previous = beta_policy.load_previous_catalog(documents['previous_beta_catalog'])
    catalog = load(documents['settings_catalog'])
    matrix = load(documents['preflight_matrix'])
    expected_sources = beta_policy.validate_transition_matrix(matrix, catalog, previous)
    require(transition.get('source_images') == sorted(expected_sources),
            'beta transition source scope differs from complete matrix')
    rows = [r for r in catalog['profiles'] if r['profile'] == configuration['profile']]
    require(len(rows) == 1 and rows[0]['configuration'] == configuration,
            'beta target configuration differs from reviewed image')
    identity = rows[0]['settings_identity']
    require(transition['target'] == {'ihx_sha256': ihx_hash, 'schema': configuration['nvm_schema'],
                'optional_features': configuration['optional_features'], 'code_sha256': identity['code_sha256']}
            and identity['ihx_sha256'] == ihx_hash and identity['nvm_schema'] == configuration['nvm_schema'],
            'beta transition target differs from exact image')


def validate(report, root=ROOT):
    root = Path(root)
    configuration = report.get('configuration')
    manifest = safe_path(root, manifest_name(configuration))
    proof = load(manifest)
    require(proof.get('format') == 'ak820-release-safety-1', 'unknown witness manifest')
    require(configuration == proof.get('program', {}).get('configuration'),
            'configuration differs from the reviewed exact image')
    optional = configuration['optional_features']
    sources = proof.get('source_files', {})
    require(isinstance(sources, dict) and REQUIRED_SOURCES <= sources.keys(), 'incomplete proof source snapshot')
    for name, record in sources.items():
        checked_record(root, name, record)
    artifacts = {}
    for extension in ('ihx', 'map', 'mem'):
        rows = [row for row in report.get('artifacts', [])
                if row.get('path', '').endswith('/ajazz_ak820_vial.' + extension)]
        require(len(rows) == 1, 'missing or ambiguous build identity')
        row = rows[0]
        artifacts[extension] = checked_record(root, 'qmk-8051-ak820/' + row['path'], row)
    ihx_hash = sha(artifacts['ihx'].read_bytes())
    symbols = pack_ak820.read_symbols(artifacts['map'])
    require(bool(symbols), 'empty linked symbols')
    symbol_hash = sha(json.dumps(symbols, sort_keys=True, separators=(',', ':')).encode())
    require(proof.get('program') == {'ihx_sha256': ihx_hash, 'symbols_sha256': symbol_hash,
                                   'configuration': configuration}, 'image, symbols or features differ from review')
    witnesses = proof.get('witnesses', {})
    require(set(witnesses) == {'stack', 'startup', 'irq', 'transition'}, 'incomplete safety witnesses')
    data = {}
    for name, record in witnesses.items():
        require(isinstance(record, dict), 'invalid witness record')
        data[name] = load(checked_record(root, record.get('path'), record))
    runtime, startup, irq, transition = (data[name] for name in ('stack', 'startup', 'irq', 'transition'))
    for item in (runtime, startup):
        require(item.get('identity', {}).get('ihx_sha256') == ihx_hash, 'stack witness belongs to another image')
    analyzer = sources['qmk-8051-ak820/tests/ak820_stack/analyze.py']['sha256']
    require(runtime.get('analyzer_sha256') == startup.get('analyzer_sha256') == irq.get('stack_analyzer_sha256') == analyzer,
            'witnesses use a different stack analyzer')
    require(runtime.get('decoder_source_sha256') == sources['qmk-8051-ak820/util/ak820_linked_inventory.py']['sha256']
            and startup.get('checker_sha256') == sources['qmk-8051-ak820/tests/ak820_startup/stack_contract.py']['sha256']
            and irq.get('runner_sha256') == sources['qmk-8051-ak820/tests/ak820_irq/run.py']['sha256'],
            'witness checker changed')
    roots = runtime.get('roots', {})
    require(set(roots) == ROOT_NAMES, 'missing control-stack root')
    bounds = {}
    for name, result in roots.items():
        require(isinstance(result, dict) and result.get('unresolved') == [], 'unresolved control-stack root')
        bounds[name] = number(result.get('bound'), name)
    require(startup.get('interrupt_enables_unchanged_until_main') is True, 'startup interrupt state unresolved')
    entry = number(startup.get('main_entry_frame_bound'), 'main-entry bound')
    require(entry >= 2 and number(startup.get('pre_main_control_stack_bound'), 'startup bound') >= entry,
            'startup/main entry frames disagree')
    require(irq.get('pass') is True and irq.get('linked_image_sha256') == ihx_hash
            and irq.get('wrapper_bytes_on_stack') == 17, 'IRQ wrapper proof missing or wrong image')
    names = {'timer': '_ak820_timer_irq', 'usb': '_USB_DeviceInterrupt', 'led': '_ak820_led_irq'}
    expected_irq = {name: 17 + bounds[symbol] for name, symbol in names.items()}
    require(irq.get('irq_bounds') == expected_irq, 'IRQ callbacks differ from global stack roots')
    irq_total = sum(expected_irq.values())
    require(irq.get('all_distinct_source_irq_bound') == irq_total, 'incomplete interrupt nesting allowance')
    expected_orders = {order for count in range(1, 4) for order in itertools.permutations(names, count)}
    cases = irq.get('cpu_cases', [])
    require(len(cases) == len(expected_orders)
            and {tuple(case.get('irq_order', [])) for case in cases} == expected_orders
            and all(case.get('canary_and_registers_preserved') is True for case in cases), 'IRQ order coverage incomplete')
    require(irq.get('selector_cases', {}).get('input_values_checked') == 256
            and irq.get('selector_cases', {}).get('bounded_table_entries') == 16
            and irq.get('emitted_contracts', {}).get('compiler_register_bank') == 0
            and irq['emitted_contracts'].get('shared_helper_masked_init_calls')
            and irq['emitted_contracts'].get('nonoverlay_allocations'), 'IRQ static/selector contract incomplete')
    capacity = number(irq.get('stack_capacity'), 'stack capacity')
    placement = re.search(r'Stack starts at:\s+0x([0-9a-f]+) \(sp set to 0x([0-9a-f]+)\) with (\d+) bytes available',
                          artifacts['mem'].read_text(), re.I)
    require(placement is not None, 'missing actual linked stack placement')
    start, initial_sp, linked_capacity = (int(placement[1], 16), int(placement[2], 16), int(placement[3]))
    require(start == initial_sp + 1 and capacity == linked_capacity == 256 - start
            and irq.get('initial_sp') == startup.get('crt_initial_sp') == initial_sp,
            'witness capacity differs from linked stack placement')
    total = bounds['_main'] + entry + irq_total
    require(total <= capacity and number(startup['pre_main_control_stack_bound'], 'startup bound') <= capacity,
            'whole-program stack allowance exceeds capacity')
    target = transition.get('target', {})
    require(transition.get('format') == 'ak820-settings-transition-2' and transition.get('passed') is True
            and transition.get('offline_only') is True
            and type(transition.get('physical_device_commands')) is int and transition['physical_device_commands'] == 0
            and target.get('ihx_sha256') == ihx_hash and target.get('schema') == configuration.get('nvm_schema')
            and target.get('optional_features') == optional and transition.get('source_images')
            and type(transition.get('tests')) is list and transition['tests']
            and all(type(test) is dict and type(test.get('exit_code')) is int and test['exit_code'] == 0
                    and type(test.get('command')) is list and test['command']
                    and all(type(part) is str and part for part in test['command'])
                    for test in transition['tests']),
            'installer transition not qualified for this image/features')
    transition_sources = set()
    for test in transition['tests']:
        require(isinstance(test.get('source_files'), dict) and test['source_files'], 'missing transition source snapshot')
        for name, expected_sha in test['source_files'].items():
            require(name in sources and sources[name]['sha256'] == expected_sha,
                    'transition test source changed or absent: ' + name)
            transition_sources.add(name)
        log = safe_path(root, test.get('log_path'))
        require(sha(log.read_bytes()) == test.get('log_sha256'), 'transition log changed')
    required_transition = {name for name in REQUIRED_SOURCES if name.startswith('tools/') or name.endswith('/prepare_release.py')}
    require(required_transition <= transition_sources, 'incomplete transition implementation/test source closure')
    validate_beta_preflight(transition, root, ihx_hash, configuration, sources)
    return {'manifest_sha256': sha(manifest.read_bytes()), 'foreground_bound': bounds['_main'],
            'main_entry_frame_bound': entry, 'irq_bound': irq_total, 'stack_bound': total,
            'stack_capacity': capacity, 'stack_margin': capacity - total,
            'build_identity': {extension: sha(path.read_bytes()) for extension, path in artifacts.items()},
            'scope': 'Reviewed control-stack/IRQ/transition proof under the documented MCS-51 architectural contract; no physical validation.'}
