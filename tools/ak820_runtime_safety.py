"""Combine exact-image foreground, CRT and interrupt evidence; no release approval."""
from __future__ import annotations

import itertools


ROOTS = {'timer': '_ak820_timer_irq', 'usb': '_USB_DeviceInterrupt', 'led': '_ak820_led_irq'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def count(value, name):
    require(type(value) is int and 0 <= value <= 255, 'Invalid stack count: ' + name)
    return value


def combine(runtime, startup, irq, identity, memory, sources):
    """Validate freshly generated reports against inspected image and source hashes.

    A failed capacity check is returned with its arithmetic for diagnosis. Missing,
    stale or inconsistent evidence raises instead of producing a qualified result.
    The caller runs the checkers; this function never treats supplied JSON as
    independent review, release approval, or hardware validation.
    """
    for report in (runtime, startup):
        require(all(report.get('identity', {}).get(key) == identity[key]
                    for key in ('ihx_sha256', 'map_sha256')), 'Stack evidence belongs to another image or MAP')
    analyzer = sources['qmk-8051-ak820/tests/ak820_stack/analyze.py']
    require(runtime.get('analyzer_sha256') == startup.get('analyzer_sha256') ==
            irq.get('stack_analyzer_sha256') == analyzer, 'Stack analyzer identity differs')
    require(runtime.get('decoder_source_sha256') == sources['qmk-8051-ak820/util/ak820_linked_inventory.py'] and
            startup.get('checker_sha256') == sources['qmk-8051-ak820/tests/ak820_startup/stack_contract.py'] and
            irq.get('runner_sha256') == sources['qmk-8051-ak820/tests/ak820_irq/run.py'],
            'Runtime checker identity differs')
    require(irq.get('pass') is True and irq.get('linked_image_sha256') == identity['ihx_sha256'] and
            irq.get('linked_map_sha256') == identity['map_sha256'], 'IRQ evidence failed or belongs to another image or MAP')
    wrapper = irq.get('wrapper_source', {})
    require(wrapper.get('kind') == 'public-pinned-wrapper-fixture' and
            wrapper.get('fixture_sha256') == sources['qmk-8051-ak820/tests/ak820_irq/oem-wrappers.json'] and
            wrapper.get('instruction_bytes') == 234, 'IRQ wrapper fixture identity differs')
    roots = runtime.get('roots', {})
    require(set(roots) == {'_main', *ROOTS.values()}, 'Runtime evidence omits a required root')
    bounds, unknown = {}, []
    for name, root in roots.items():
        if root.get('bound') is None:
            require(bool(root.get('unresolved')), 'Unknown root has no diagnostic')
            unknown.append(name)
        else:
            require(root.get('unresolved') == [], 'Bounded root still has unresolved paths')
            bounds[name] = count(root['bound'], name)
    require(all(symbol in bounds for symbol in ROOTS.values()), 'IRQ root remains unresolved')
    callbacks = irq.get('callback_static_reports', {})
    require(set(callbacks) == set(ROOTS) and all(callbacks[name].get('bound') == bounds[symbol] and
            callbacks[name].get('unresolved') == [] for name, symbol in ROOTS.items()),
            'IRQ callback bounds differ from foreground analysis')
    expected_irq = {name: 17 + bounds[symbol] for name, symbol in ROOTS.items()}
    irq_total = sum(expected_irq.values())
    require(irq.get('wrapper_bytes_on_stack') == 17 and irq.get('irq_bounds') == expected_irq and
            irq.get('all_distinct_source_irq_bound') == irq_total, 'Incomplete IRQ stack allowance')
    orders = {order for length in range(1, 4) for order in itertools.permutations(ROOTS, length)}
    cases = irq.get('cpu_cases', [])
    require(len(cases) == len(orders) and {tuple(case.get('irq_order', [])) for case in cases} == orders and
            all(case.get('canary_and_registers_preserved') is True and
                type(case.get('irq_stack_bytes')) is int and
                0 <= case['irq_stack_bytes'] <= sum(expected_irq[name] for name in case['irq_order'])
                for case in cases), 'Incomplete or failed IRQ CPU coverage')
    selector, contracts = irq.get('selector_cases', {}), irq.get('emitted_contracts', {})
    require(selector.get('input_values_checked') == 256 and selector.get('bounded_table_entries') == 16 and
            contracts.get('compiler_register_bank') == 0 and contracts.get('shared_helper_masked_init_calls') and
            contracts.get('nonoverlay_allocations'), 'Incomplete IRQ ABI, allocation or selector checks')
    require(startup.get('interrupt_enables_unchanged_until_main') is True, 'Startup interrupt state is unresolved')
    entry = count(startup.get('main_entry_frame_bound'), 'main entry')
    before_main = count(startup.get('pre_main_control_stack_bound'), 'pre-main')
    require(before_main >= entry >= 2, 'Startup omits the persistent main call frame')
    capacity, initial_sp = count(memory['stack_capacity'], 'capacity'), count(memory['initial_sp'], 'initial SP')
    require(capacity + initial_sp == 255 and irq.get('stack_capacity') == capacity and
            irq.get('initial_sp') == startup.get('crt_initial_sp') == initial_sp,
            'Runtime evidence differs from linked stack placement')
    total = max(before_main, bounds['_main'] + entry + irq_total) if not unknown else None
    passed = total is not None and total <= capacity
    return {'format': 'ak820-runtime-safety-1', 'passed': passed,
            'identity': identity, 'source_files': sources, 'root_bounds': {name: bounds.get(name) for name in roots},
            'unresolved_roots': unknown, 'foreground_bound': bounds.get('_main'),
            'main_entry_frame_bound': entry, 'pre_main_bound': before_main,
            'irq_bound': irq_total, 'stack_bound': total, 'stack_capacity': capacity,
            'stack_margin': capacity - total if total is not None else None,
            'whole_program_stack_qualified': passed, 'release_approved': False,
            'hardware_validated': False, 'physical_device_commands': 0,
            'limits': ['Control-stack bound from CRT entry with IE=IE_EX=0, valid memory accesses and the bank-0 SDCC ABI.',
                       'MCS-51 in-service/RETI semantics bound all three distinct interrupt sources; no priority-count assumption.',
                       'OEM wrapper instructions are a pinned public reference, not a connected-device identity check.',
                       'The packer supplies disabled IRQs at CRT entry; pre-CRT trial erase is checked separately.',
                       'No physical timing, flash, power-loss or device test; release and settings-transition approval are separate.']}
