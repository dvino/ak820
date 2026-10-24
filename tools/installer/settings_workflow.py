"""Shared, fail-closed installer settings workflows; no automatic recovery."""
from pathlib import Path
import sys
import hashlib
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ak820_device_protocol import DeviceAPI
import settings_backup as settings


def cancelled(host):
    if host.CANCEL_EVENT is not None and host.CANCEL_EVENT.is_set():
        raise host.Cancelled('Operation cancelled before the next write')


def emit(host, stage, purpose, **fields):
    if host.PROGRESS:
        host.PROGRESS(stage, {'purpose': purpose, **fields})


def prepare(host, log, source):
    """Validate and copy OEM recovery inputs before opening any USB handle."""
    release = host.load_release(approved=True)
    session, native = host.copy_recovery(log, Path(source))
    profile = settings.load_profile(host.BUNDLE, native)
    target, plan = host.prepare_trial(log, native, image='permanent')
    _, payload, copied = host.transport.session_image(target, 'permanent')
    host.require(copied == native and payload == profile['payload'],
                 'Reconstructed target differs from the supported settings profile')
    paths = [host.APPROVAL, host.BUNDLE / 'installer-release.json']
    paths += [host.BUNDLE / name for name in release['files']]
    paths += [host.ROOT / name for name in release['host_files']]
    paths += [host.ROOT / 'tools/installer/settings_workflow.py',
              host.ROOT / 'tools/installer/settings_backup.py']
    for folder in (Path(source), session, target):
        paths += [folder / name for name in ('images.json', 'before-full-rom.bin', 'restore-native.bin')]
    paths += [target / host.transport.IMAGES['permanent']]
    paths += [host.RECOVERY_REFERENCE / name for name in ('stock-full.bin', 'native-installed.bin')]
    pins = {path: host.sha(path.read_bytes()) for path in paths}
    return {'source': Path(source), 'recovery': session, 'native': native,
            'profile': profile, 'target': target, 'plan': plan, 'pins': pins}


def revalidate(host, context):
    host.load_release(approved=True)
    for session in (context['source'], context['recovery']):
        _, _, native = host.transport.session_image(session, 'restore')
        host.require(native == context['native'], 'OEM recovery inputs changed')
    profile = settings.load_profile(host.BUNDLE, context['native'])
    _, payload, native = host.transport.session_image(context['target'], 'permanent')
    host.require(payload == context['profile']['payload'] == profile['payload'] and
                 native == context['native'], 'Approved update inputs changed')


def recheck_pins(host, context):
    for path, digest in context['pins'].items():
        host.require(host.sha(path.read_bytes()) == digest, 'Approved input changed: ' + str(path))


def fingerprint(path):
    path = Path(path)
    return {str(p.relative_to(path)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(path.rglob('*')) if p.is_file()}


def check_backup(host, path, pinned, profile, identity):
    result = settings.validate_backup(Path(path), profile, expected_identity=identity)
    host.require(fingerprint(path) == pinned, 'Settings backup files changed after validation')
    return result


def open_api(host, log, selected, profile, *, writes=False):
    return DeviceAPI(profile, log.folder,
                     app_factory=lambda: host.transport.Application(selected), allow_writes=writes)


def physical_unlock(host, log, hid, selected, digest, *, purpose='update'):
    """A fresh lock/unlock sequence; timeout never resets or retries."""
    print('Hold Esc + left Control for three seconds. SHA256: ' + digest, flush=True)
    stage = 'restore_unlock_wait' if purpose == 'restore' else 'unlock_wait'
    emit(host, stage, purpose, sha256=digest, counter=30)
    app = host.transport.Application(selected)
    def check(command):
        cancelled(host)
        host.require_state(hid, 'VIAL_APP', selected['path'])
        cancelled(host)
        log.record('device_mutation_attempt', command=command)
    try:
        check('vial_lock_FE08')
        app.vial_unlock_command(8)
        host.require(app.vial_unlock_status() == (0, 0), 'Fresh Vial lock failed')
        check('vial_unlock_start_FE06')
        app.vial_unlock_command(6)
        host.require(app.vial_unlock_status() == (0, 1), 'Fresh Vial unlock failed to start')
        deadline = time.monotonic() + 120
        while True:
            cancelled(host)
            host.require(time.monotonic() < deadline, 'Physical unlock timed out; no automatic retry')
            host.require_state(hid, 'VIAL_APP', selected['path'])
            unlocked, active, counter = app.vial_unlock_status(poll=True)
            if (unlocked, active, counter) == (1, 0, 0):
                break
            host.require(unlocked == 0 and active == 1, 'Physical unlock interrupted')
            emit(host, stage, purpose, sha256=digest, counter=counter)
            time.sleep(.1)
        log.record('physical_consent_received', image_sha256=digest, purpose=purpose)
    finally:
        app.close()


def backup(host, log, hid, context, output, *, purpose='backup'):
    emit(host, 'backup', purpose, path=str(output))
    selected = host.require_state(hid, 'VIAL_APP')
    api = open_api(host, log, selected, context['profile'])
    try:
        result = settings.export_settings(api, Path(output), context['profile'])
        log.record('settings_backup_verified', path=str(result['path']))
        print('Validated settings backup: ' + str(result['path']), flush=True)
        if purpose == 'backup':
            emit(host, 'complete', purpose, path=str(result['path']))
        return result
    finally:
        api.close()


def restore(host, log, hid, context, backup_path, *, target_backup=None):
    profile = context['profile']
    saved = settings.validate_backup(Path(backup_path), profile)
    pinned = fingerprint(backup_path)
    selected = host.require_state(hid, 'VIAL_APP')
    target = (target_backup if isinstance(target_backup, dict) else
              backup(host, log, hid, context, target_backup or log.folder / 'before-restore-settings', purpose='restore'))
    settings.require_target_backup(target, profile)
    emit(host, 'preflight', 'restore')
    plan = settings.plan_restore(saved, profile, target_nvm=target['nvm'])
    describe(context, saved, plan, 'restore')
    physical_unlock(host, log, hid, selected, context['plan']['sha256'], purpose='restore')
    revalidate(host, context)
    api = open_api(host, log, selected, profile, writes=True)
    try:
        settings.recheck_source(api, target, profile)
        def before_write(*_args, **_kwargs):
            cancelled(host)
            host.require_state(hid, 'VIAL_APP', selected['path'])
            recheck_pins(host, context)
            check_backup(host, backup_path, pinned, profile, saved['identity'])
            cancelled(host)
        emit(host, 'restoring', 'restore')
        result = settings.restore_settings(api, saved, profile, before_write=before_write, target_backup=target)
        emit(host, 'verifying', 'restore')
        log.record('settings_restore_verified', result=result)
        emit(host, 'complete', 'restore', path=str(backup_path))
        print('Settings restored and verified. Backup: ' + str(backup_path), flush=True)
        return result
    finally:
        api.close()


def describe(context, saved, plan, purpose):
    print('Operation: ' + purpose + '. Backup: ' + str(saved['path']), flush=True)
    print('Exact firmware SHA256: ' + context['plan']['sha256'], flush=True)
    print('Preserves 498 key assignments, 12 encoder assignments, supported layout options, '
          '16 macros and saved RGB values. Physical behavior and power-loss persistence '
          'are not tested by this operation.', flush=True)
    for limitation in plan.get('limitations', []):
        print('Limitation: ' + str(limitation), flush=True)
    if purpose == 'update':
        print('One firmware flash, then a second physical confirmation to restore settings. '
              'Keep alternate keyboard input and stable power available.', flush=True)


def update(host, log, hid, context, output):
    profile = context['profile']
    saved = backup(host, log, hid, context, output, purpose='update')
    pinned = fingerprint(output)
    target_nvm = profile['payload'][host.packer.NVM_START-host.packer.APP_START:
                                    host.packer.NVM_END-host.packer.APP_START]
    emit(host, 'preflight', 'update')
    plan = settings.plan_restore(saved, profile, target_nvm=target_nvm)
    describe(context, saved, plan, 'update')
    selected = host.require_state(hid, 'VIAL_APP')
    physical_unlock(host, log, hid, selected, context['plan']['sha256'])
    revalidate(host, context)
    api = open_api(host, log, selected, profile)
    try:
        settings.recheck_source(api, saved, profile)
    finally:
        api.close()
    cancelled(host)
    app = host.transport.Application(selected)
    try:
        host.require_state(hid, 'VIAL_APP', selected['path'])
        host.require(app.vial_unlock_status() == (1, 0), 'Unlock changed before loader entry')
        revalidate(host, context)
        check_backup(host, output, pinned, profile, saved['identity'])
        cancelled(host)
        log.record('device_mutation_attempt', command='vial_bootloader_0B')
        app.enter_vial_loader()
    finally:
        app.close()
    emit(host, 'loader_wait', 'update', seconds=25)
    loader = host.wait_state(hid, 'LOADER', cancel_event=host.CANCEL_EVENT)
    emit(host, 'loader_detected', 'update')
    authorization = {'image': 'permanent', 'sha256': context['plan']['sha256'],
                     'reset': False, 'erase': True, 'flash': True, 'restart': True}
    guard = host.phase_guard(log, hid, authorization, loader)
    def flash_guard(phase, **fields):
        guard(phase, **fields)
        if phase == 'erase_and_flash':
            cancelled(host)
            revalidate(host, context)
            check_backup(host, output, pinned, profile, saved['identity'])
            cancelled(host)
            log.record('device_mutation_attempt', command='loader_erase_flash')
            emit(host, 'flashing', 'update')
    host.transport.flash(context['target'], 'permanent', False, False,
                         reference_dir=host.RECOVERY_REFERENCE, loader_descriptor=loader,
                         host_update_snapshot={'payload_sha256': context['plan']['sha256'],
                                               'backup_sha256': host.sha(context['native'])},
                         phase_guard=flash_guard)
    emit(host, 'verifying', 'update')
    selected = host.wait_state(hid, 'VIAL_APP')
    host.boot_status(hid, selected, log)
    target = backup(host, log, hid, context, log.folder / 'after-update-settings', purpose='update')
    at = host.packer.MANIFEST_START
    host.require(target['rom'][at:host.packer.APP_END] ==
                 profile['payload'][at-host.packer.APP_START:],
                 'Flashed full application manifest differs from the exact target')
    host.require(target['nvm'] == target_nvm, 'Flashed durable NVM differs from the exact target')
    result = restore(host, log, hid, context, saved['path'], target_backup=target)
    emit(host, 'complete', 'update', path=str(saved['path']))
    return result
