#!/usr/bin/env python3
"""Cross-platform AK820 installer; default action only enumerates HID.

USB mutation requires an independently reviewed, hash-bound release and explicit
operator consent. Permanent is the install default; --trial is explicit.
The loader transport lives in util/ak820_tool.py; this file orchestrates it.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import time
import traceback
import venv
import zipfile

FROZEN = bool(getattr(sys, 'frozen', False))
ROOT = Path(sys._MEIPASS) if FROZEN else Path(__file__).resolve().parents[2]
UTIL = ROOT / 'qmk-8051-ak820' / 'util'
sys.path.insert(0, str(UTIL))

import ak820_tool as transport
import ak820_diagnose as diagnostic
import pack_ak820 as packer
from prepare_ak820_trial import write_trial
from ak820_ci_authorization import CI_EXTRA_FILES, validate_bundle_authorization
from ak820_release_manifest import MANIFEST_FORMAT, RELEASE, validate_host_manifest, read_review_record

BUNDLE = ROOT / 'releases' / RELEASE
APPROVAL = ROOT / 'tools' / 'installer' / 'approved-release.json'
ORIGINAL = ROOT / 'evidence' / 'oem-backup'
RECOVERY_REFERENCE = None  # User-owned local inputs, never distributed.
RUNS = ((Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local')) / 'AK820' / 'runs')
        if FROZEN else ROOT / 'host' / 'runs')
VENV = ROOT / '.venv-ak820-installer'
PROMPT = None
PROGRESS = None
CANCEL_EVENT = None


def read_input(message):
    return (PROMPT or input)(message)
APP_ID = (0x320F, 0x505B)
LOADER_ID = (0x0C45, 0x7687)
HARDWARE = 'AJAZZ AK820 wired / VS11K28A / 320F:505B'
EXPECTED_OEM = '1dc3e2f79bd03d0bdc4e7a0fc43241e6e89445799948990725ee644ec45c09d1'
EXPECTED_RESTORE = 'd7152819712470cf37a0c29d69b756edc4a51aca1d20c13e1fcf4b96f9638535'
BAD_IHX = {'42447e53fa5b7e70154c5c4bb92973f9c3fbe75ab3c0fd27d8d5abadc1216e91'}
REQUIRED_FILES = frozenset((
    'firmware/application.ihx', 'firmware/application.map', 'firmware/application.mem',
    'reports/build-report.json', 'reports/packing-validation.json',
    'reviews/independent-review.md',
    'reference/info.json', 'reference/vial.json',
))
REPRODUCTION_BUILDER = 'reproduction/build_ak820.py'


class Cancelled(Exception):
    """Operator declined before any destructive operation."""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


class Log:
    def __init__(self, mode):
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        self.folder = RUNS / (stamp + '-' + mode)
        self.folder.mkdir(parents=True, exist_ok=False)
        self.stream = (self.folder / 'events.jsonl').open('x', encoding='utf-8')

    def record(self, event, **fields):
        row = {'time_utc': datetime.now(timezone.utc).isoformat(), 'event': event, **fields}
        self.stream.write(json.dumps(row, ensure_ascii=False, default=str) + '\n')
        self.stream.flush()

    def finish(self, status):
        self.record('completed', exit_code=status)
        self.stream.close()
        archive = self.folder.with_name(self.folder.name + '-logs.zip')
        with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as out:
            for path in sorted(self.folder.rglob('*')):
                if path.is_file():
                    out.write(path, path.relative_to(self.folder))
        print('\nSession folder:', self.folder)
        print('Diagnostic archive:', archive)


def load_release(*, approved):
    """Fail closed on absent, stale, mixed or known-bad release artifacts."""
    path = BUNDLE / 'installer-release.json'
    raw = path.read_bytes()
    manifest = json.loads(raw)
    require(manifest.get('format') == MANIFEST_FORMAT, 'Unknown release format')
    require(manifest.get('release') == RELEASE and manifest.get('hardware') == HARDWARE,
            'Release does not match ' + RELEASE + ' / wired AK820 VS11K28A')
    require(manifest.get('hardware_validated') is False and
            ((manifest.get('trial_only') is True and 'install_modes' not in manifest) or
             (manifest.get('trial_only') is False and manifest.get('install_modes') == ['permanent', 'trial'])),
            'Unknown install modes or unsupported hardware-validation claim')
    require(manifest.get('offline_review') == {'status': 'passed', 'report': 'reviews/independent-review.md'},
            'Independent offline review is missing')
    files = manifest.get('files', {})
    require(isinstance(files, dict) and set(files) in (
        REQUIRED_FILES, REQUIRED_FILES | {REPRODUCTION_BUILDER},
        REQUIRED_FILES | CI_EXTRA_FILES, REQUIRED_FILES | CI_EXTRA_FILES | {REPRODUCTION_BUILDER}),
        'Incomplete or unexpected release contents')
    for name in sorted(files):
        data = (BUNDLE / name).read_bytes()
        item = files[name]
        require(isinstance(item, dict) and item.get('size') == len(data) and item.get('sha256') == sha(data),
                'File modified or corrupted: ' + name)
    if REPRODUCTION_BUILDER in files:
        report = json.loads((BUNDLE / 'reports/build-report.json').read_text(encoding='utf-8'))
        require(files[REPRODUCTION_BUILDER]['sha256'] == report.get('builder_sha256'),
                'Reproduction builder differs from the build report')
    require(files['firmware/application.ihx']['sha256'] not in BAD_IHX,
            'Known-bad RC3 firmware is forbidden')
    # This binds the IHX and MAP to the actual compiler report, not just names.
    diagnostic.diagnostic_build(BUNDLE / 'firmware/application.ihx', BUNDLE / 'firmware/application.map',
                                BUNDLE / 'reports/build-report.json')
    validate_host_manifest(manifest, ROOT)
    review = read_review_record((BUNDLE / 'reviews/independent-review.md').read_text(encoding='utf-8'))
    require(review.get('host_files') == manifest['host_files'] and review.get('build') == {
        'ihx_sha256': files['firmware/application.ihx']['sha256'],
        'map_sha256': files['firmware/application.map']['sha256'],
        'build_report_sha256': files['reports/build-report.json']['sha256'],
    }, 'Independent review belongs to different build or host code')
    validate_bundle_authorization(BUNDLE, manifest, review)
    if approved:
        require(APPROVAL.is_file(), 'Release approval is missing; installation is blocked pending independent review')
        approval = json.loads(APPROVAL.read_text(encoding='utf-8'))
        require(approval == {'format': 'ak820-installer-approval-1', 'release': RELEASE,
                             'manifest_sha256': sha(raw)},
                'Approval does not match exact release bytes; installation blocked')
    return manifest


def local_references(folder):
    """Validate exact user-owned OEM inputs without opening USB."""
    require(folder is not None, 'Local OEM references required. Supply --reference-dir PATH containing your own '
            'stock-full.bin and native-installed.bin. OEM images are not distributed or downloaded.')
    folder = Path(folder).resolve()
    require((folder / 'stock-full.bin').is_file() and (folder / 'native-installed.bin').is_file(),
            'Local reference directory must contain stock-full.bin and native-installed.bin')
    stock = (folder / 'stock-full.bin').read_bytes()
    native = (folder / 'native-installed.bin').read_bytes()
    require(len(stock) == 65536 and sha(stock) == packer.STOCK_SHA and
            len(native) == packer.APP_END - packer.APP_START and sha(native) in packer.NATIVE_REFERENCE_HASHES,
            'Unknown local OEM reference images; exact supported references are required')
    return folder


def capture_references(log, backup):
    """Create private validation inputs from this owner's fully pinned ROM."""
    global RECOVERY_REFERENCE
    packer.validate_native(backup)
    if RECOVERY_REFERENCE is None:
        folder = log.folder / 'private-oem-reference'
        folder.mkdir(exist_ok=False)
        (folder / 'stock-full.bin').write_bytes(backup)
        (folder / 'native-installed.bin').write_bytes(backup[packer.APP_START:packer.APP_END])
        RECOVERY_REFERENCE = folder
    return RECOVERY_REFERENCE


def check_original():
    """The original personal backup is never used as a writable session."""
    _, recovery, backup = transport.session_image(ORIGINAL, 'restore')
    require(sha(backup) == EXPECTED_OEM and sha(recovery) == EXPECTED_RESTORE,
            'Original personal backup is corrupted')
    packer.validate_native(backup, (RECOVERY_REFERENCE / 'stock-full.bin').read_bytes(),
                           (RECOVERY_REFERENCE / 'native-installed.bin').read_bytes())
    return backup


def hid_module():
    try:
        return transport.hid_module()
    except (ImportError, RuntimeError, OSError) as error:
        raise RuntimeError('Could not load hidapi. Run AK820.sh setup (Linux) '
                           'or AK820.cmd setup (Windows). Reason: ' + str(error)) from error


def inspect(hid):
    """All relevant descriptors are counted, never select the first keyboard."""
    devices = [d for d in hid.enumerate() if (d.get('vendor_id'), d.get('product_id')) in (APP_ID, LOADER_ID)]
    apps = [d for d in devices if (d.get('vendor_id'), d.get('product_id')) == APP_ID and
            (d.get('usage_page'), d.get('usage')) in ((0xFF1C, 0x92), (0xFF60, 0x61))]
    loaders = [d for d in devices if (d.get('vendor_id'), d.get('product_id')) == LOADER_ID and
               d.get('interface_number') == 1 and (d.get('usage_page'), d.get('usage')) == (12, 1)]
    app_present = any((d.get('vendor_id'), d.get('product_id')) == APP_ID for d in devices)
    loader_present = any((d.get('vendor_id'), d.get('product_id')) == LOADER_ID for d in devices)
    if len(apps) > 1 or len(loaders) > 1 or (app_present and loader_present):
        return 'AMBIGUOUS', None, devices
    # Recognize only the control interface and known ancillary collections.
    # Missing usage metadata is not evidence of an unrelated collection: an
    # additional target-ID device could otherwise be silently discarded.
    allowed = {(0, 1, 6)}  # Boot keyboard, in both native/application modes.
    if len(apps) == 1:
        native = apps[0]['usage_page'] == 0xFF1C
        allowed.add((1, 0xFF1C if native else 0xFF60, 0x92 if native else 0x61))
        shared = 1 if native else 2
        allowed.update((shared, page, usage) for page, usage in ((1, 6), (1, 0x80), (12, 1), (1, 2)))
    elif len(loaders) == 1:
        allowed.add((1, 12, 1))
    shapes = [(d.get('interface_number'), d.get('usage_page'), d.get('usage')) for d in devices]
    if len(shapes) != len(set(shapes)):
        return 'AMBIGUOUS', None, devices
    if any(shape not in allowed for shape in shapes):
        return 'UNSUPPORTED_INTERFACE', None, devices
    if len(loaders) == 1:
        return 'LOADER', loaders[0], devices
    if len(apps) == 1:
        return ('OEM_APP' if apps[0]['usage_page'] == 0xFF1C else 'VIAL_APP'), apps[0], devices
    return ('UNSUPPORTED_INTERFACE' if devices else 'NOT_FOUND'), None, devices


def inventory(log, hid):
    state, selected, devices = inspect(hid)
    fields = ('vendor_id', 'product_id', 'interface_number', 'usage_page', 'usage', 'product_string', 'path')
    summary = [{k: (v.decode(errors='backslashreplace') if isinstance(v, bytes) else v)
                for k in fields if (v := d.get(k)) is not None} for d in devices]
    log.record('usb_inventory', state=state, devices=summary, device_opened=False)
    return state, selected


def require_state(hid, expected, path=None):
    state, selected, _ = inspect(hid)
    require(state == expected, f'Expected a single {expected} device, found {state}')
    if path is not None:
        require(selected.get('path') == path, 'Device changed after selection; operation stopped')
    return selected


def wait_state(hid, expected, seconds=25, *, cancel_event=None):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if cancel_event is not None and cancel_event.is_set():
            raise Cancelled('Ожидание отменено до записи прошивки')
        state, selected, _ = inspect(hid)
        require(state != 'AMBIGUOUS', 'Multiple devices appeared; check stopped')
        if state == expected:
            return selected
        time.sleep(0.2)
    raise TimeoutError(f'No {expected} device found within {seconds} seconds; no automatic reflash')


def capture_native(log, selected, *, references):
    print('Reading complete OEM ROM and current settings; no firmware writes.', flush=True)
    prefix = log.folder / 'native-prefix.bin'
    data = bytearray()
    app = transport.Application(selected)
    try:
        require(app.native, 'A new installation requires supported OEM firmware')
        with prefix.open('xb') as output:
            for address in range(0, 65536, 1024):
                block = app.rom(address, 1024)
                require(len(block) == 1024, 'Incomplete OEM ROM block')
                output.write(block)
                output.flush()
                data.extend(block)
        require(app.rom(0xA000, 0x3380) == data[0xA000:0xD380],
                'OEM settings changed during capture. Close configuration tools and start a fresh session')
    finally:
        app.close()
    backup = bytes(data)
    prefix.rename(log.folder / 'native-rom.bin')
    if references is None:
        capture_references(log, backup)
    else:
        packer.validate_native(backup, (references / 'stock-full.bin').read_bytes(),
                               (references / 'native-installed.bin').read_bytes())
    require(backup[0x27C0:0x27C4] == bytes.fromhex('aa5533cc'), 'OEM boot marker is missing')
    log.record('fresh_native_backup_verified', bytes=len(backup), sha256=sha(backup))
    return backup


def prepare_trial(log, backup, *, image='permanent'):
    require(image in ('trial', 'permanent'), 'Unknown install mode')
    capture_references(log, backup)
    dest = log.folder / ('trial-session' if image == 'trial' else 'permanent-session')
    result = write_trial(BUNDLE / 'firmware/application.ihx', BUNDLE / 'firmware/application.map',
                         RECOVERY_REFERENCE / 'stock-full.bin', RECOVERY_REFERENCE / 'native-installed.bin',
                         backup, dest)
    require(set(result['images']) == {'ak820-vial-trial.bin', 'restore-native.bin'},
            'Packer produced unexpected images')
    if image == 'permanent':
        data = packer.read_ihex(BUNDLE / 'firmware/application.ihx')
        symbols = packer.read_symbols(BUNDLE / 'firmware/application.map')
        stock = (RECOVERY_REFERENCE / 'stock-full.bin').read_bytes()
        nvm, _ = packer.migrate(backup, data, symbols)
        payload = packer.pack(data, symbols, stock, nvm, False)
        result['images'][transport.IMAGES[image]] = packer.verify_payload(payload)
        result['trial_only'] = False
        result['native_install_backup_sha256'] = sha(backup)
        (dest / transport.IMAGES[image]).write_bytes(payload)
        json_write(dest / 'images.json', result)
    plan = transport.plan(dest, image)
    restore = transport.plan(dest, 'restore')
    require(restore['sha256'] == sha(backup[packer.APP_START:packer.APP_END]),
            'Personal recovery image differs from the fresh backup')
    log.record('installation_prepared', session=str(dest), image=image, plan=plan, restore=restore,
               migration=result['migration'], hardware_validated=False)
    return dest, plan


def confirm(phrase, explanation, log):
    print('\n' + explanation)
    if read_input(explanation + '\nВведите ' + phrase + ' (Enter — отмена): ').strip() != phrase:
        log.record('consent_declined', phrase=phrase)
        raise Cancelled('Operation cancelled before reset/erase/flash')
    log.record('consent_received', phrase=phrase)


def confirm_preparation(log):
    print('Preparation reads the complete OEM ROM and saves your personal backup. '
          'Writing and entering the loader require a separate yes confirmation.')
    if read_input('Start preparation? [y/N] ').strip().lower() != 'y':
        log.record('preparation_declined')
        raise Cancelled('Preparation cancelled before opening the device')
    log.record('preparation_accepted')


def consent(log, plan, *, recovery, image='permanent'):
    print('\nImage:', plan['image'])
    print('SHA256:', plan['sha256'])
    print('Size:', plan['size'], 'bytes; writes limited to 0x2800..0xEFBF.')
    print('AK820 keyboard input will temporarily stop after confirmation. '
          'Keep another keyboard or on-screen input available.')
    if not recovery:
        print(RELEASE.upper() + ' ' + image.upper() + ': ' +
              ('reset enters the OEM loader after the trial clears its marker.' if image == 'trial' else
               'the boot marker is retained so the application can restart after power loss.'))
        if image == 'permanent':
            print('OEM recovery: Vial Unlock + Bootloader, then recover --session with your personal session. '
                  'If the application fails, this software recovery route is not guaranteed.')
        print('This candidate has not been validated on hardware.')
    confirm('yes', 'Authorize loader transition (installation only), application erase, '
            'writing the displayed image and restart after checksum.', log)
    return {'image': 'restore' if recovery else image, 'sha256': plan['sha256'],
            'reset': not recovery, 'erase': True, 'flash': True, 'restart': True}


def phase_guard(log, hid, authorization, initial):
    def check(phase, **fields):
        require(fields.get('image') == authorization['image'] and
                fields.get('sha256') == authorization['sha256'], 'Image does not match the confirmed plan')
        if phase == 'reset_to_loader':
            require(authorization['reset'], 'Reset is not authorized')
            require_state(hid, 'OEM_APP', initial['path'])
        elif phase in ('erase_and_flash', 'restart'):
            require(authorization['erase'] and authorization['flash'] and authorization['restart'],
                    'Erase/write/restart is not authorized')
            require_state(hid, 'LOADER', fields.get('loader_path'))
        else:
            raise ValueError('Unknown flashing phase')
        log.record('phase_guard_passed', phase=phase, sha256=authorization['sha256'])
    return check


def keyboard_smoke(log):
    print('\nEarly typing check — BEFORE Raw HID and Flash readback.')
    print('Select an English keyboard layout and type ak820 on the AK820, then press Enter.')
    print('If the AK820 cannot type, press Enter using another keyboard or on-screen input.')
    passed = read_input('AK820> ').strip() == 'ak820'
    # stdin is intentionally not presented as a device-attributed USB capture.
    log.record('keyboard_typing_smoke', passed=passed, method='operator_interactive_input',
               device_attribution='operator asserted; no OS keyboard hook installed', raw_hid_used=False)
    return passed


def boot_status(hid, selected, log, seconds=5):
    """Observe main-loop progress over EP0, independently of Raw HID/FD00.

    HIDAPI includes report id 0 in this Feature read: 0 + AKBT + v1 + stage +
    heartbeat + flags. The eight-byte feature is declared in the RC5+ descriptor.
    No SET_REPORT, firmware write, VIA getter or reset is sent here.
    """
    require_state(hid, 'VIAL_APP', selected['path'])
    dev = hid.device()
    opened = False
    previous = None
    samples = []
    deadline = time.monotonic() + seconds
    try:
        dev.open_path(selected['path'])
        opened = True
        while time.monotonic() < deadline:
            raw = bytes(dev.get_feature_report(0, 9))
            require(len(raw) == 9 and raw[:6] == b'\x00AKBT\x01',
                    'Invalid boot status Feature report; application startup is not confirmed')
            stage, heartbeat, flags = raw[6:9]
            require(stage in (1, 2, 3) and not flags & 0xFC, 'Unknown boot status fields')
            sample = {'stage': stage, 'heartbeat': heartbeat, 'flags': flags}
            samples.append(sample)
            log.record('boot_status_sample', **sample, transport='EP0 Feature GET_REPORT',
                       raw_hid_used=False, device_mutations=0)
            if stage == 3 and flags == 1:
                if previous is not None and heartbeat != previous:
                    log.record('main_loop_progress_observed', samples=len(samples),
                               proves='main loop progressed between EP0 polls; not keyboard or persistence correctness')
                    return samples
                previous = heartbeat
            else:
                # Require two samples in one uninterrupted configured main-loop
                # state, not a counter change across reset/suspend/startup.
                previous = None
            time.sleep(0.2)
        raise TimeoutError('Firmware main loop made no observed progress before timeout; '
                           'save the logs. No automatic reset or retry will be performed')
    finally:
        if opened:
            dev.close()
        json_write(log.folder / 'boot-status.json', {'samples': samples,
                   'transport': 'EP0 Feature GET_REPORT', 'physical_mutations': 0,
                   'scope': 'main-loop liveness only; HIDAPI control-transfer timeout is OS-specific'})


def verify_trial(log, hid, session, selected, *, image='permanent'):
    manifest, trial, _ = transport.session_image(session, image)
    release = load_release(approved=True)
    for filename, key in (('firmware/application.ihx', 'ihx_sha256'), ('firmware/application.map', 'map_sha256')):
        require(manifest.get(key) == release['files'][filename]['sha256'], 'Session belongs to a different build')
    require_state(hid, 'VIAL_APP', selected['path'])
    boot_status(hid, selected, log)
    typed = keyboard_smoke(log)
    code = diagnostic.diagnostic_build(BUNDLE / 'firmware/application.ihx', BUNDLE / 'firmware/application.map',
                                       BUNDLE / 'reports/build-report.json')
    output = log.folder / 'code-readback'
    report = diagnostic.capture(output, expected=trial, code=code,
                                app_factory=lambda: transport.Application(selected))
    rom = (output / 'rom.bin').read_bytes()
    transport.verify_live(rom, trial, image, (RECOVERY_REFERENCE / 'stock-full.bin').read_bytes())
    require(report['nvm_and_journal_stable_on_second_read'], 'NVM changed during verification')
    require(not report['status']['storage_failed'], 'Diagnostics reports an NVM storage failure')
    log.record('application_readback_verified', image=image, rom_sha256=sha(rom), trial_marker_clear=image == 'trial',
               code_and_protected_regions_match=True, keyboard_typing_passed=typed,
               persistence_after_power_cycle='not tested')
    require(typed, 'Typing check failed; USB enumeration and CODE readback do not prove keyboard functionality')
    return rom


def install(log, hid, *, image='permanent'):
    release = load_release(approved=True)
    require(image in ('permanent', 'trial') and
            (image == 'trial' or release.get('install_modes') == ['permanent', 'trial']),
            'This reviewed release permits trial only; permanent requires separate review and approval')
    confirm_preparation(log)
    state, selected = inventory(log, hid)
    require(state == 'OEM_APP', 'Installation requires one AK820 running OEM firmware; run diagnose/recover first')
    backup = capture_native(log, selected, references=RECOVERY_REFERENCE)
    session, plan = prepare_trial(log, backup, image=image)
    print('Personal recovery session:', session)
    authorization = consent(log, plan, recovery=False, image=image)
    # Revalidate immutable build inputs after the operator reviewed the plan.
    load_release(approved=True)
    transport.flash(session, image, True, False, reference_dir=RECOVERY_REFERENCE,
                    native_install=image == 'permanent',
                    application_descriptor=selected, phase_guard=phase_guard(log, hid, authorization, selected))
    log.record('loader_completed', note='checksum accepted; application startup not yet established')
    running = wait_state(hid, 'VIAL_APP')
    rom = verify_trial(log, hid, session, running, image=image)
    _, trial, _ = transport.session_image(session, image)
    require(rom[packer.NVM_START:packer.NVM_END] == trial[packer.NVM_START-packer.APP_START:packer.NVM_END-packer.APP_START],
            'Initial settings differ from the prepared image')
    print('\n' + image.upper() + ': typing and complete CODE readback passed. Entropy/Vial checks can now begin.')
    print('Persistence after power loss was not tested by this run.')
    print('Personal recovery session:', session)
    if image == 'trial':
        print('Trial is intended to return to the loader after reset; do not treat it as a daily-use installation.')


def update_prepared(log, hid, source):
    """Fresh physical Vial consent, limited to the reviewed RC6 repair pair."""
    release = load_release(approved=True)
    manifest, payload, backup = transport.validate_prepared_update(source)
    for filename, key in (('firmware/application.ihx', 'ihx_sha256'), ('firmware/application.map', 'map_sha256')):
        require(manifest[key] == release['files'][filename]['sha256'], 'Update session belongs to another release')
    capture_references(log, backup)
    packer.validate_native(backup, (RECOVERY_REFERENCE / 'stock-full.bin').read_bytes(),
                           (RECOVERY_REFERENCE / 'native-installed.bin').read_bytes())
    selected = require_state(hid, 'VIAL_APP')
    output = log.folder / 'before-update-readback'
    report = diagnostic.capture(output, app_factory=lambda: transport.Application(selected))
    require(report['completed'] and report['nvm_and_journal_stable_on_second_read'],
            'Current settings or journal changed; update stopped')
    snapshot = output / 'rom.bin'
    transport.validate_prepared_update(source, snapshot)
    session = log.folder / 'update-session'
    session.mkdir()
    for name in ('images.json', 'before-full-rom.bin', 'restore-native.bin', 'ak820-vial-permanent.bin'):
        shutil.copyfile(source / name, session / name)
    transport.validate_prepared_update(session, snapshot)
    plan = transport.plan(session, 'permanent')
    print('Prepared RC6 repair only. Fresh full ROM saved:', snapshot)
    print('Image SHA256:', plan['sha256'])
    print('This restores the durable settings saved before the failed encoder probe, '
          'and discards its pending journal transaction. The temporary encoder change will not be replayed.')
    print('Keep alternate keyboard input and stable power available. No automatic recovery or retry is performed.')
    def before_mutation(event):
        if CANCEL_EVENT is not None and CANCEL_EVENT.is_set():
            raise Cancelled('Обновление отменено до следующей команды')
        require_state(hid, 'VIAL_APP', selected['path'])
        if CANCEL_EVENT is not None and CANCEL_EVENT.is_set():
            raise Cancelled('Обновление отменено до следующей команды')
        log.record('device_mutation_attempt', command=event)
    instructions = ('Теперь удерживайте Esc + левый Ctrl 3 секунды. Это разрешает одну запись '
                    'показанной прошивки и перезапуск после проверки.\n'
                    'Будут возвращены сохранённые настройки до проверки энкодера и удалена '
                    'ожидающая запись журнала. Временное изменение энкодера не повторится.\n'
                    'Подготовьте запасную клавиатуру и стабильное питание.\nSHA256: ' + plan['sha256'])
    print(instructions, flush=True)
    if PROGRESS:
        PROGRESS('unlock_wait', {'sha256': plan['sha256'], 'counter': 30})
    device = transport.Application(selected)
    try:
        before_mutation('vial_lock_FE08')
        device.vial_unlock_command(8)
        require(device.vial_unlock_status() == (0,0), 'Vial did not lock; fresh consent unavailable')
        before_mutation('vial_unlock_start_FE06')
        device.vial_unlock_command(6)
        require(device.vial_unlock_status() == (0,1), 'Fresh Vial unlock did not start')
        deadline = time.monotonic() + 120
        while True:
            if CANCEL_EVENT is not None and CANCEL_EVENT.is_set():
                raise Cancelled('Ожидание физического подтверждения отменено')
            if time.monotonic() >= deadline:
                raise TimeoutError('Physical Vial unlock timed out; no automatic retry')
            require_state(hid, 'VIAL_APP', selected['path'])
            unlocked, active, counter = device.vial_unlock_status(poll=True)
            log.record('vial_unlock_poll', unlocked=unlocked, in_progress=active, counter=counter)
            if unlocked == 1 and active == 0 and counter == 0:
                break
            require(unlocked == 0 and active == 1, 'Physical unlock was rejected or interrupted')
            if PROGRESS:
                PROGRESS('unlock_wait', {'sha256': plan['sha256'], 'counter': counter})
            time.sleep(.1)
        log.record('physical_consent_received', image_sha256=plan['sha256'])
        load_release(approved=True)
        transport.validate_prepared_update(session, snapshot)
        require(device.vial_unlock_status() == (1,0), 'Vial unlock changed before bootloader entry')
        before_mutation('vial_bootloader_0B')
        device.enter_vial_loader()
    except BaseException:
        log.record('unlock_sequence_stopped', automatic_cleanup=False,
                   vial_unlock_may_remain_active=True, automatic_retry=False)
        print('Обновление остановлено. Автоматического сброса или повторной попытки нет. '
              'Запрос разблокировки Vial может оставаться активным.', flush=True)
        raise
    finally:
        device.close()
    if PROGRESS:
        PROGRESS('loader_wait', {'seconds': 25})
    loader = wait_state(hid, 'LOADER', seconds=25, cancel_event=CANCEL_EVENT)
    if CANCEL_EVENT is not None and CANCEL_EVENT.is_set():
        raise Cancelled('Ожидание отменено до записи прошивки')
    if PROGRESS:
        PROGRESS('loader_detected', {})
    load_release(approved=True)
    transport.validate_prepared_update(session, snapshot)
    authorization = {'image': 'permanent', 'sha256': plan['sha256'], 'reset': False,
                     'erase': True, 'flash': True, 'restart': True}
    if CANCEL_EVENT is not None and CANCEL_EVENT.is_set():
        raise Cancelled('Запись отменена до начала прошивки')
    guard = phase_guard(log, hid, authorization, loader)
    def update_guard(phase, **details):
        guard(phase, **details)
        # Check after the guard's enumeration and only before the first write.
        # Once erase starts, cancellation must not interrupt checksum/restart.
        if phase == 'erase_and_flash' and CANCEL_EVENT is not None and CANCEL_EVENT.is_set():
            raise Cancelled('Запись отменена до стирания прошивки')
        if phase == 'erase_and_flash':
            load_release(approved=True)
            transport.validate_prepared_update(session, snapshot)
            if CANCEL_EVENT is not None and CANCEL_EVENT.is_set():
                raise Cancelled('Запись отменена до стирания прошивки')
            log.record('device_mutation_attempt', command='loader_erase_flash')
            if PROGRESS:
                PROGRESS('flashing', {})
    transport.flash(session, 'permanent', False, False, reference_dir=RECOVERY_REFERENCE,
                    loader_descriptor=loader, prepared_update_snapshot=snapshot,
                    phase_guard=update_guard)
    running = wait_state(hid, 'VIAL_APP')
    boot_status(hid, running, log)
    code = diagnostic.diagnostic_build(BUNDLE / 'firmware/application.ihx', BUNDLE / 'firmware/application.map',
                                       BUNDLE / 'reports/build-report.json')
    post = log.folder / 'after-update-readback'
    report = diagnostic.capture(post, expected=payload, code=code,
                                app_factory=lambda: transport.Application(running))
    rom = (post / 'rom.bin').read_bytes()
    transport.verify_live(rom, payload, 'permanent', (RECOVERY_REFERENCE / 'stock-full.bin').read_bytes())
    require(report['completed'] and report['nvm_and_journal_stable_on_second_read'] and
            not report['status']['storage_failed'], 'Update readback or storage check failed')
    require(rom[packer.NVM_START:packer.NVM_END] == payload[packer.NVM_START-packer.APP_START:packer.NVM_END-packer.APP_START],
            'Update durable settings differ from prepared image')
    log.record('prepared_update_readback_verified', rom_sha256=sha(rom),
               physical_typing='not tested', persistence_after_power_cycle='not tested')
    print('Update CODE, protected regions, durable settings and main-loop progress verified. '
          'Physical typing, encoder behavior and persistence after power loss were not tested.')


def copy_recovery(log, source):
    _, recovery, backup = transport.session_image(source, 'restore')
    capture_references(log, backup)
    packer.validate_native(backup, (RECOVERY_REFERENCE / 'stock-full.bin').read_bytes(),
                           (RECOVERY_REFERENCE / 'native-installed.bin').read_bytes())
    require(backup[0x27C0:0x27C4] == bytes.fromhex('aa5533cc'), 'Invalid OEM backup: boot marker missing')
    dest = log.folder / 'recovery-session'
    dest.mkdir(exist_ok=False)
    (dest / 'before-full-rom.bin').write_bytes(backup)
    (dest / 'restore-native.bin').write_bytes(recovery)
    json_write(dest / 'images.json', {'backup_sha256': sha(backup),
                                     'images': {'restore-native.bin': {'size': len(recovery), 'sha256': sha(recovery)}},
                                     'source_recovery_session': str(source.resolve())})
    return dest, backup


def recover(log, hid, source):
    state, selected = inventory(log, hid)
    if state == 'OEM_APP':
        print('OEM firmware is already present. No erase or write is needed.')
        log.record('recovery_not_needed', device_mutations=0)
        return
    require(state == 'LOADER', 'Recovery requires an already visible OEM loader. No automatic reset is sent. '
            'For trial only, a separately authorized manual reconnect may enter the loader; then run diagnose.')
    session, backup = copy_recovery(log, source)
    plan = transport.plan(session, 'restore')
    print('Personal recovery source:', source)
    authorization = consent(log, plan, recovery=True)
    transport.flash(session, 'restore', False, False, reference_dir=RECOVERY_REFERENCE,
                    loader_descriptor=selected, phase_guard=phase_guard(log, hid, authorization, selected))
    running = wait_state(hid, 'OEM_APP')
    typed = keyboard_smoke(log)
    rom = capture_native(log, running, references=RECOVERY_REFERENCE)
    _, image, _ = transport.session_image(session, 'restore')
    transport.verify_live(rom, image, 'restore', (RECOVERY_REFERENCE / 'stock-full.bin').read_bytes())
    require(rom == backup, 'Restored ROM differs from the selected complete personal OEM backup')
    log.record('oem_recovery_verified', rom_sha256=sha(rom), full_rom_matches=True, keyboard_typing_passed=typed)
    require(typed, 'ROM restored but typing check failed; keyboard functionality remains unconfirmed')
    print('\nOEM restored: all 65536 bytes match the personal backup; typing check passed.')


def setup():
    if FROZEN:
        print('This standalone build already includes Python and hidapi. No setup is needed.')
        return
    require(sys.version_info >= (3, 10), 'Python 3.10 or newer is required (use python, not py)')
    print('Installing hidapi in the local Python environment:', VENV)
    python = VENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.is_file():
        venv.EnvBuilder(with_pip=True).create(VENV)
    else:
        # The wrapper may already be running this interpreter. Windows cannot
        # replace an in-use python.exe; reuse it, including after a pip failure.
        subprocess.run([str(python), '-m', 'ensurepip', '--upgrade'], check=True)
    pip = [str(python), '-m', 'pip', 'install', '--disable-pip-version-check']
    environment = None
    if sys.platform.startswith('linux'):
        # The pinned Linux wheel uses libusb and reports non-hidraw paths under
        # hidraw-only udev access. Build HIDAPI's hidraw backend explicitly.
        pip.extend(('--no-binary=hidapi', '--no-cache-dir', '--force-reinstall'))
        environment = os.environ.copy()
        environment.update({'HIDAPI_WITH_HIDRAW': '1', 'HIDAPI_WITH_LIBUSB': '0'})
        print('Building Linux hidapi from source with its hidraw backend. This requires gcc, Python development headers, '
              'and libudev development files (for example, libudev-dev on Debian or Ubuntu).')
    pip.extend(('-r', str(Path(__file__).with_name('requirements.txt'))))
    subprocess.run(pip, check=True, **({'env': environment} if environment is not None else {}))
    subprocess.run([str(python), '-c', 'import hid; print("hidapi", hid.__version__)'], check=True)
    print('Ready. AK820.sh / AK820.cmd will use this environment automatically.')


def udev(install_rules):
    require(sys.platform.startswith('linux'), 'udev rules apply only to Linux')
    source = Path(__file__).with_name('70-ak820.rules')
    target = '/etc/udev/rules.d/70-ak820.rules'
    commands = [['install', '-m', '0644', str(source), target],
                ['udevadm', 'control', '--reload-rules'],
                ['udevadm', 'trigger', '--subsystem-match=hidraw', '--action=add']]
    if not install_rules:
        print('To grant device access to a local desktop user, run:')
        print('./AK820.sh udev --install')
        print('Only rules for USB 320F:505B and OEM loader 0C45:7687 will be installed.')
        print('Do not run the installer itself with sudo.')
        return
    require(source.is_file(), 'udev rules file is missing')
    prefix = [] if os.geteuid() == 0 else ['sudo']
    for command in commands:
        subprocess.run(prefix + command, check=True)
    print('Rules installed and applied to hidraw. No USB reset or reconnect was performed.')


def parser():
    out = argparse.ArgumentParser(description='AK820 Linux/Windows installer. No command: HID enumeration only.')
    sub = out.add_subparsers(dest='command')
    sub.add_parser('diagnose', help='List HID interfaces without opening devices, reset or firmware writes')
    sub.add_parser('setup', help='Local Python environment and hidapi; no USB access')
    rules = sub.add_parser('udev', help='Configure Linux device access without USB reset')
    rules.add_argument('--install', action='store_true')
    prep = sub.add_parser('prepare', help='Create personal permanent/recovery session without reset/erase/flash')
    prep.add_argument('--native-rom', type=Path, help='Complete local OEM ROM for fully offline preparation')
    prep.add_argument('--trial', action='store_true', help='Prepare trial instead of permanent')
    installation = sub.add_parser('install', help='Fresh OEM backup, explicit confirmations, permanent install, typing and CODE readback')
    installation.add_argument('--trial', action='store_true', help='Explicit trial mode: returns to loader after reset')
    sub.add_parser('verify', help='Verify release files and approval entirely offline; no HID access')
    verification = sub.add_parser('check-device', help='Check running firmware without writing settings')
    verification.add_argument('--session', type=Path, required=True)
    verification.add_argument('--trial', action='store_true', help='Check trial instead of permanent')
    recovery = sub.add_parser('recover', help='Restore personal OEM backup from an existing loader; no reset sent')
    recovery.add_argument('--session', type=Path, required=True,
                          help='Your personal installation/recovery session containing a complete OEM backup')
    update = sub.add_parser('update-prepared', help='Reviewed RC6 repair; fresh physical Esc + left Ctrl consent')
    update.add_argument('--session', type=Path, required=True)
    for name in ('backup', 'restore', 'update'):
        command = sub.add_parser(name, help='Validated local settings ' + name)
        command.add_argument('--session', type=Path, required=True, help='Original valid OEM recovery session')
        command.add_argument('--output' if name == 'backup' else '--backup' if name == 'restore' else '--backup-dir',
                             type=Path, required=True)
    for command in (prep, installation, verification, recovery, update):
        command.add_argument('--reference-dir', type=Path, help='Directory with your own exact stock-full.bin and native-installed.bin; never downloaded')
    return out


def main(argv=None, *, prompt=None, interactive=None, progress=None, cancel_event=None):
    global PROMPT, RECOVERY_REFERENCE, PROGRESS, CANCEL_EVENT
    args = parser().parse_args(argv)
    mode = args.command or 'diagnose'
    if mode == 'setup':
        setup()
        return 0
    if mode == 'udev':
        udev(args.install)
        return 0
    log = Log(mode)
    old_prompt = PROMPT
    old_references = RECOVERY_REFERENCE
    old_progress, old_cancel = PROGRESS, CANCEL_EVENT
    PROMPT = prompt
    PROGRESS, CANCEL_EVENT = progress, cancel_event
    status = 1
    try:
        log.record('start', mode=mode, python=sys.version.split()[0], platform=sys.platform,
                   firmware_scope='wired AK820 VS11K28A only')
        require(sys.version_info >= (3, 10), 'Python 3.10 or newer is required')
        if mode in ('install', 'recover', 'check-device', 'update-prepared', 'restore', 'update'):
            require(interactive is True or (sys.stdin is not None and sys.stdin.isatty()),
                    'An interactive terminal or the installer GUI is required')
        # Offline release/recovery checks precede importing hid or enumeration.
        if mode in ('install', 'verify', 'check-device', 'prepare', 'update-prepared'):
            load_release(approved=mode != 'prepare')
        if mode in ('install', 'recover', 'check-device', 'prepare', 'update-prepared'):
            RECOVERY_REFERENCE = local_references(args.reference_dir) if args.reference_dir else None
            if mode == 'check-device':
                _, _, backup = transport.session_image(args.session, 'restore')
                capture_references(log, backup)
            if mode == 'update-prepared':
                transport.validate_prepared_update(args.session)
        workflow_context = None
        if mode in ('backup', 'restore', 'update'):
            import settings_workflow
            workflow_context = settings_workflow.prepare(sys.modules[__name__], log, args.session)
            if mode == 'restore':
                settings_workflow.settings.validate_backup(args.backup, workflow_context['profile'])
        if mode == 'verify':
            log.record('offline_bundle_verified', release=RELEASE,
                       approval_matches=True, device_opened=False, physical_mutations=0)
            print('Release files and independent approval match their checksums. Your device backup is made during preparation.')
            print('Verification was entirely offline; hidapi was not loaded and USB was not opened.')
        elif mode == 'prepare' and args.native_rom:
            prepare_trial(log, args.native_rom.read_bytes(), image='trial' if args.trial else 'permanent')
            print('Offline session prepared. USB was not opened; no firmware was written.')
        else:
            hid = hid_module()
            if workflow_context is not None:
                host = sys.modules[__name__]
                if mode == 'backup':
                    settings_workflow.backup(host, log, hid, workflow_context, args.output)
                elif mode == 'restore':
                    settings_workflow.restore(host, log, hid, workflow_context, args.backup)
                else:
                    settings_workflow.update(host, log, hid, workflow_context, args.backup_dir)
            elif mode == 'diagnose':
                state, _ = inventory(log, hid)
                print('State:', state)
                print('HID enumeration only: no device opened and no commands sent.')
                if state == 'OEM_APP':
                    print('OEM AK820 detected; install will first create a fresh complete personal backup.')
                elif state == 'LOADER':
                    print('OEM loader detected; recover using: recover --session <your-personal-session>.')
                elif state == 'VIAL_APP':
                    print('Vial HID detected. This does not confirm typing or main-loop progress.')
                if state in ('AMBIGUOUS', 'UNSUPPORTED_INTERFACE'):
                    raise RuntimeError('Cannot uniquely select a device using its supported HID interface')
            elif mode == 'prepare':
                require(interactive is True or (sys.stdin is not None and sys.stdin.isatty()),
                        'Device preparation requires an interactive terminal or GUI')
                confirm_preparation(log)
                state, selected = inventory(log, hid)
                require(state == 'OEM_APP', 'Preparation requires a single OEM AK820')
                prepare_trial(log, capture_native(log, selected, references=RECOVERY_REFERENCE),
                              image='trial' if args.trial else 'permanent')
                print('Session prepared without reset/erase/flash. Installation will still capture a fresh backup.')
            elif mode == 'install':
                install(log, hid, image='trial' if args.trial else 'permanent')
            elif mode == 'recover':
                recover(log, hid, args.session)
            elif mode == 'update-prepared':
                update_prepared(log, hid, args.session)
            elif mode == 'check-device':
                selected = require_state(hid, 'VIAL_APP')
                verify_trial(log, hid, args.session, selected, image='trial' if args.trial else 'permanent')
                print('Typing, CODE, protected OEM loader/tail and selected mode marker verified.')
        status = 0
    except Cancelled as error:
        print('\nCANCELLED:', error)
        log.record('cancelled', reason=str(error), physical_mutations='see device_mutation_attempt events')
        status = 2
    except (Exception, KeyboardInterrupt) as error:
        print('\nSTOPPED:', error)
        (log.folder / 'error.txt').write_text(traceback.format_exc(), encoding='utf-8')
        log.record('failed', error_type=type(error).__name__, message=str(error), auto_retry=False)
        if isinstance(error, OSError) and sys.platform.startswith('linux'):
            print('For Linux permission errors, check ./AK820.sh udev; do not run the installer with sudo.')
    finally:
        try:
            log.finish(status)
        finally:
            PROMPT = old_prompt
            PROGRESS, CANCEL_EVENT = old_progress, old_cancel
            RECOVERY_REFERENCE = old_references
    return status


if __name__ == '__main__':
    raise SystemExit(main())
