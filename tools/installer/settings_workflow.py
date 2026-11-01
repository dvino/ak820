"""Shared, fail-closed installer settings workflows; no automatic recovery."""
from pathlib import Path
import sys
import hashlib
import os
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


def prepare(host, log, source, *, release_context=None, reference_dir=None):
    """Validate and copy OEM recovery inputs before opening any USB handle."""
    release_context = release_context or host.release_context(approved=True)
    release = host.load_release(approved=True, context=release_context)
    host.require(release_context.snapshot is not None, 'Validated release snapshot is missing')
    source = Path(source)
    source_data = host.transport.session_image(source, 'restore')
    native = source_data[2]
    references = host.operation_references(native, reference_dir)
    host.require_operation_recovery(source, native)
    session, _ = host.copy_recovery(log, source, session_data=source_data, reference_bytes=references)
    profile = settings.load_profile(release_context.bundle, native, trusted_catalog=trusted_catalog(host, release_context),
                                    release_files=release_context.snapshot.files)
    target, plan = host.prepare_trial(log, native, image='permanent', context=release_context, reference_bytes=references)
    _, payload, copied = host.transport.session_image(target, 'permanent', target_build_id=release_context.nvm_schema)
    host.require(copied == native and payload == profile['payload'],
                 'Reconstructed target differs from the supported settings profile')
    paths = [release_context.approval, release_context.bundle / 'installer-release.json']
    paths += [release_context.bundle / name for name in release['files']]
    paths += [host.ROOT / name for name in release['host_files']]
    paths += [host.ROOT / 'tools/installer/settings_workflow.py',
              host.ROOT / 'tools/installer/settings_backup.py']
    for folder in (Path(source), session, target):
        paths += [folder / name for name in ('images.json', 'before-full-rom.bin', 'restore-native.bin')]
    paths += [target / host.transport.IMAGES['permanent']]
    pins = {path: host.sha(path.read_bytes()) for path in paths}
    if reference_dir is not None:
        for name, data in zip(('stock-full.bin', 'native-installed.bin'), references):
            pins[Path(reference_dir) / name] = host.sha(data)
    context = {'source': source, 'source_data': source_data, 'recovery': session, 'native': native,
               'references': references, 'release_context': release_context, 'profile': profile,
               'target': target, 'plan': plan, 'pins': pins,
               'verification': (release_context.bundle, target, release_context.approval)}
    revalidate(host, context)
    recheck_pins(host, context)
    return context


def trusted_catalog(host, release_context):
    if release_context.profile == 'legacy':
        return None
    import json
    path = host.ROOT / 'tools/installer/settings-catalog.json'
    host.require(path.is_file(), 'Exact settings catalog missing; settings operations blocked')
    # load_release already verified this file through the approved host manifest.
    host.require('tools/installer/settings-catalog.json' in release_context.manifest['host_files'],
                 'Settings catalog is not bound to approved host code')
    host.require(release_context.snapshot is not None, 'Validated release snapshot is missing')
    return json.loads(release_context.snapshot.host_files['tools/installer/settings-catalog.json'].decode('utf-8'))


def revalidate(host, context):
    release_context = context['release_context']
    host.load_release(approved=True, context=release_context)
    host.require(host.transport.session_image(context['source'], 'restore') == context['source_data'],
                 'OEM source session changed')
    for session in (context['source'], context['recovery'], context['target']):
        host.require_operation_recovery(session, context['native'])
    host.require_operation_references(context['native'], context['references'])
    profile = settings.load_profile(release_context.bundle, context['native'],
        trusted_catalog=trusted_catalog(host, release_context), release_files=release_context.snapshot.files)
    manifest, payload, native = host.transport.session_image(context['target'], 'permanent', target_build_id=release_context.nvm_schema)
    host.require_session_release(manifest, release_context)
    host.require(payload == context['profile']['payload'] == profile['payload'] and
                 native == context['native'], 'Approved update inputs changed')


def recheck_pins(host, context):
    for path, digest in context['pins'].items():
        host.require(host.sha(path.read_bytes()) == digest, 'Approved input changed: ' + str(path))


def fingerprint(path):
    path = Path(path)
    settings.require(path.is_dir() and not path.is_symlink(), 'Backup must be a real directory')
    limits = {**settings.FILES, 'manifest.json': 65536}
    allowed = set(limits) | {'direct-ram.json'}
    names = set()
    with os.scandir(path) as entries:
        for entry in entries:
            settings.require(entry.name in allowed, 'Unexpected backup directory entries')
            names.add(entry.name)
    if 'direct-ram.json' in names:
        limits['direct-ram.json'] = 4096
    settings.require(names == set(limits), 'Unexpected backup directory entries')
    return {name: hashlib.sha256(settings._read_file(path, name, limit)).hexdigest()
            for name, limit in limits.items()}


def check_backup(host, path, pinned, profile, identity):
    result = settings.validate_backup(Path(path), profile, expected_identity=identity)
    host.require(fingerprint(path) == pinned, 'Settings backup files changed after validation')
    return result


def freeze_backup(value):
    if isinstance(value, dict):
        return ('dict', tuple((key, freeze_backup(item)) for key, item in value.items()))
    if isinstance(value, list):
        return ('list', tuple(freeze_backup(item) for item in value))
    if isinstance(value, tuple):
        return ('tuple', tuple(freeze_backup(item) for item in value))
    if isinstance(value, Path):
        return ('path', str(value))
    if isinstance(value, (str, int, bool, bytes, type(None))):
        return ('value', value)
    raise TypeError('Unsupported backup snapshot value: ' + type(value).__name__)


def thaw_backup(snapshot):
    kind, value = snapshot
    if kind == 'dict':
        return {key: thaw_backup(item) for key, item in value}
    if kind == 'list':
        return [thaw_backup(item) for item in value]
    if kind == 'tuple':
        return tuple(thaw_backup(item) for item in value)
    if kind == 'path':
        return Path(value)
    if kind == 'value':
        return value
    raise ValueError('Invalid backup snapshot')


def select_backup(host, path, profile):
    saved, files = settings.validate_backup(Path(path), profile, retain_files=True)
    pinned = fingerprint(saved['path'])
    host.require(all(pinned.get(name) == hashlib.sha256(data).hexdigest() for name, data in files.items()),
                 'Settings backup bytes changed during selection')
    host.require(check_backup(host, saved['path'], pinned, profile, saved['identity']) == saved,
                 'Settings backup changed during selection')
    return freeze_backup(saved), tuple(sorted(pinned.items())), tuple(sorted(files.items()))


def selected_values(selection):
    snapshot, pinned, _files = selection
    return thaw_backup(snapshot), dict(pinned)


def open_api(host, log, selected, profile, *, writes=False, verification=None):
    return DeviceAPI(profile, log.folder,
                     app_factory=lambda: host.transport.Application(selected), allow_writes=writes,
                     verification=verification)


def physical_unlock(host, log, hid, selected, digest, *, purpose='update', prewrite=None):
    """A fresh lock/unlock sequence; timeout never resets or retries."""
    print('Hold Esc + left Control for three seconds. SHA256: ' + digest, flush=True)
    stage = 'restore_unlock_wait' if purpose == 'restore' else 'unlock_wait'
    emit(host, stage, purpose, sha256=digest, counter=30)
    app = host.transport.Application(selected)
    def check(command):
        cancelled(host)
        host.require_state(hid, 'VIAL_APP', selected['path'])
        if prewrite is not None:
            prewrite()
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
        revalidate(host, context)
        recheck_pins(host, context)
        log.record('settings_backup_verified', path=str(result['path']))
        print('Validated settings backup: ' + str(result['path']), flush=True)
        if purpose == 'backup':
            emit(host, 'complete', purpose, path=str(result['path']))
        return result
    finally:
        api.close()


def restore(host, log, hid, context, backup_path, *, target_backup=None, nested=False, selected_backup=None):
    profile = context['profile']
    selection = selected_backup if selected_backup is not None else select_backup(host, backup_path, profile)
    saved, pinned = selected_values(selection)
    host.require(Path(backup_path).absolute() == Path(saved['path']).absolute(), 'Selected backup path changed')
    host.require(check_backup(host, backup_path, pinned, profile, saved['identity']) == saved,
                 'Selected backup changed')
    selected = host.require_state(hid, 'VIAL_APP')
    target = (target_backup if isinstance(target_backup, dict) else
              backup(host, log, hid, context, target_backup or log.folder / 'before-restore-settings', purpose='restore'))
    target = settings.require_target_backup(target, profile)
    target_pinned = fingerprint(target['path'])
    check_backup(host, target['path'], target_pinned, profile, target['identity'])
    emit(host, 'preflight', 'restore')
    plan = settings.plan_restore(saved, profile, target_nvm=target['nvm'])
    describe(context, saved, plan, 'restore')
    def unlock_guard():
        revalidate(host, context)
        recheck_pins(host, context)
        check_backup(host, backup_path, pinned, profile, saved['identity'])
        check_backup(host, target['path'], target_pinned, profile, target['identity'])
    physical_unlock(host, log, hid, selected, context['plan']['sha256'], purpose='restore', prewrite=unlock_guard)
    revalidate(host, context)
    api = open_api(host, log, selected, profile, writes=True,
                   verification=context.get('verification'))
    try:
        settings.recheck_source(api, target, profile)
        check_backup(host, target['path'], target_pinned, profile, target['identity'])
        def before_write(*_args, **_kwargs):
            cancelled(host)
            host.require_state(hid, 'VIAL_APP', selected['path'])
            revalidate(host, context)
            recheck_pins(host, context)
            check_backup(host, backup_path, pinned, profile, saved['identity'])
            check_backup(host, target['path'], target_pinned, profile, target['identity'])
            cancelled(host)
        emit(host, 'restoring', 'restore')
        result = settings.restore_settings(api, saved, profile, before_write=before_write, target_backup=target)
        emit(host, 'verifying', 'restore')
        revalidate(host, context)
        recheck_pins(host, context)
        check_backup(host, backup_path, pinned, profile, saved['identity'])
        check_backup(host, target['path'], target_pinned, profile, target['identity'])
        log.record('nested_settings_restore_verified' if nested else 'settings_restore_verified', result=result)
        if not nested:
            emit(host, 'complete', 'restore', path=str(backup_path))
            print('Settings restored and verified. Backup: ' + str(backup_path), flush=True)
        return result
    finally:
        api.close()


def describe(context, saved, plan, purpose):
    print('Profile:', context['release_context'].profile)
    print('Linked image SHA256:', context['profile']['ihx_sha256'])
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
    exported = backup(host, log, hid, context, output, purpose='update')
    selection = select_backup(host, output, profile)
    saved, pinned = selected_values(selection)
    host.require(saved == exported, 'Exported settings backup changed before selection')
    target_nvm = profile['payload'][host.packer.NVM_START-host.packer.APP_START:
                                    host.packer.NVM_END-host.packer.APP_START]
    emit(host, 'preflight', 'update')
    plan = settings.plan_restore(saved, profile, target_nvm=target_nvm)
    describe(context, saved, plan, 'update')
    selected = host.require_state(hid, 'VIAL_APP')
    def unlock_guard():
        revalidate(host, context)
        recheck_pins(host, context)
        check_backup(host, output, pinned, profile, saved['identity'])
    physical_unlock(host, log, hid, selected, context['plan']['sha256'], prewrite=unlock_guard)
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
        recheck_pins(host, context)
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
        if phase in ('erase_and_flash', 'restart'):
            if phase == 'erase_and_flash':
                emit(host, 'flashing', 'update')
            cancelled(host)
            revalidate(host, context)
            recheck_pins(host, context)
            check_backup(host, output, pinned, profile, saved['identity'])
            cancelled(host)
            if phase == 'erase_and_flash':
                log.record('device_mutation_attempt', command='loader_erase_flash')
    def payload_guard(payload, native):
        host.require(payload == profile['payload'] and native == context['native'],
                     'Flash bytes differ from the retained target and OEM recovery backup')
    host.transport.flash(context['target'], 'permanent', False, False,
                         target_build_id=context['release_context'].nvm_schema,
                         reference_bytes=context['references'], loader_descriptor=loader,
                         payload_guard=payload_guard,
                         host_update_snapshot={'payload_sha256': context['plan']['sha256'],
                                               'backup_sha256': host.sha(context['native'])},
                         phase_guard=flash_guard)
    emit(host, 'verifying', 'update')
    selected = host.wait_state(hid, 'VIAL_APP')
    host.boot_status(hid, selected, log)
    check_backup(host, output, pinned, profile, saved['identity'])
    target = backup(host, log, hid, context, log.folder / 'after-update-settings', purpose='update')
    target = settings.require_target_backup(target, profile)
    target_pinned = fingerprint(target['path'])
    check_backup(host, target['path'], target_pinned, profile, target['identity'])
    at = host.packer.MANIFEST_START
    host.require(target['rom'][at:host.packer.APP_END] ==
                 profile['payload'][at-host.packer.APP_START:],
                 'Flashed full application manifest differs from the exact target')
    host.require(target['nvm'] == target_nvm, 'Flashed durable NVM differs from the exact target')
    result = restore(host, log, hid, context, saved['path'], target_backup=target, nested=True,
                     selected_backup=selection)
    revalidate(host, context)
    recheck_pins(host, context)
    check_backup(host, output, pinned, profile, saved['identity'])
    check_backup(host, target['path'], target_pinned, profile, target['identity'])
    log.record('settings_update_verified', result=result)
    emit(host, 'complete', 'update', path=str(saved['path']))
    print('Settings restored and verified. Backup: ' + str(saved['path']), flush=True)
    return result
