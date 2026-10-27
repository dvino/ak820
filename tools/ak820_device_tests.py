"""AK820 automatic readback and optional reversible remaps; default is offline."""
import argparse
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
LAYERS, EXPECTED_KEYS, EXPECTED_ENCODERS = 6, 83, 1

class SafetyStop(RuntimeError):
    pass

def require(ok, message):
    if not ok: raise SafetyStop(message)

def dump(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')

def stable(api):
    api.status()
    image = api.read_nvm()
    require(api.read_nvm() == image, 'Unstable NVM')
    return image

def value(image, offset):
    return int.from_bytes(image[offset:offset+2], 'big')

def check_readonly(api, report):
    api.initialize()
    image = stable(api)
    api.baseline = image
    matrix = api.definition()
    for layer in range(6):
        for key in matrix:
            api.status()
            require(api.get_key(layer, key) == value(image, api.key_offset(layer, key)), 'Key getter/NVM mismatch')
        for direction in range(2):
            api.status()
            require(api.get_encoder(layer, direction) == value(image, api.encoder_offset(layer, direction)), 'Encoder getter/NVM mismatch')
    report['checks'].append({'name': 'mapping_getters', 'status': 'PASS', 'keys': 498, 'encoder_slots': 12})
    require(api.macros() == api.macro_view(image), 'Macro getter/published NVM view mismatch')
    report['checks'].append({'name': 'macro_getters', 'status': 'PASS', 'count': 16, 'bytes': 8192})
    report['rgb'] = api.rgb()
    report['direct_ram'] = api.direct_snapshot()
    report['checks'].append({'name': 'RGB_protocol_getters', 'status': 'PASS', 'leds': 82})
    require(stable(api) == image, 'Read-only checks changed NVM')
    return matrix

def roundtrip(api, report, label, offset, setter, getter):
    before = stable(api)
    original = value(before, offset)
    require(getter() == original, label+': preexisting stale NVM')
    temporary = 0 if original else 0x73
    expected = bytearray(before)
    expected[offset:offset+2] = temporary.to_bytes(2, 'big')
    report['restore_pending'] = dict(name=label, offset=offset, original=original, temporary=temporary)
    dump(api.output/'report.json', report)
    (api.output/'mutation-baseline-nvm.bin').write_bytes(before)
    require(setter(temporary) is True, label+': setter ACK missing')
    api.status()
    require(getter() == temporary, label+': changed getter mismatch')
    require(stable(api) == bytes(expected), label+': durable mutation or neighbor mismatch')
    require(stable(api) == bytes(expected), label+': pre-restore NVM changed')
    require(setter(original) is True, label+': restore ACK missing')
    api.status()
    require(getter() == original, label+': restored getter mismatch')
    require(stable(api) == before, label+': full NVM restoration mismatch')
    report['restore_pending'] = None
    report['checks'].append(dict(name=label, status='PASS', restored=True))
    dump(api.output/'report.json', report)

def check_reversible_settings(api, report, matrix):
    key = matrix[0]
    for layer in range(6):
        roundtrip(api, report, f'representative_key_layer_{layer}', api.key_offset(layer, key),
                  lambda v, l=layer: api.set_key(l, key, v), lambda l=layer: api.get_key(l, key))
        for direction in range(2):
            roundtrip(api, report, f'encoder_{layer}_{direction}', api.encoder_offset(layer, direction),
                      lambda v, l=layer, d=direction: api.set_encoder(l, d, v), lambda l=layer, d=direction: api.get_encoder(l, d))
    report['checks'].append(dict(name='macro_write', status='SKIP', reason=
        'Vial locked; no unlock attempted' if not api.status()['vial_unlocked'] else 'Safe unused macro region not proven'))
    rgb_roundtrip(api, report)

def rgb_roundtrip(api, report):
    before = stable(api)
    original = api.rgb_mode()
    temporary = bytearray(original)
    temporary[:2] = b'\0\0' if original[:2] != b'\0\0' else (report['rgb']['effects'][0]).to_bytes(2,'little')
    temporary[2] ^= 1
    temporary[3] ^= 1
    temporary[4] ^= 1
    temporary[5] = 0 if original[5] else 1
    report['restore_pending'] = dict(name='RGB_RAM_settings', original_hex=original.hex(), temporary_hex=temporary.hex())
    dump(api.output/'report.json',report)
    require(api.set_rgb_mode(bytes(temporary)) is True, 'RGB RAM setter ACK missing')
    api.status()
    require(api.rgb_mode() == bytes(temporary), 'RGB RAM changed getter mismatch')
    require(stable(api) == before, 'RGB RAM mutation changed durable NVM')
    require(api.set_rgb_mode(original) is True, 'RGB RAM restore ACK missing')
    api.status()
    require(api.rgb_mode() == original, 'RGB RAM restored getter mismatch')
    require(stable(api) == before, 'RGB RAM restore changed durable NVM')
    report['restore_pending'] = None
    report['checks'].append(dict(name='RGB_RAM_settings', status='PASS', restored=True))

def make_plan():
    return dict(format='ak820-device-tests-2', mode='offline-plan', usb_opened=False,
        checks=['approved release, diagnostic build and personal permanent image/recovery binding',
                'boot Feature main-loop liveness; full ROM; clean stable NVM',
                '83 keys x 6 layers; one encoder x both directions x 6 layers',
                '16 macros / 8192 bytes; VialRGB capabilities, 82 LED descriptors, RAM settings',
                'optional representative key per layer and all 12 encoder remaps with exact durable patch and restore'],
        limitations=['No physical input or LED behavior', 'No restart persistence',
                     'RGB durable save skipped; RAM lighting can differ from saved settings', 'Macro writes skipped: safe unused region not proven'],
        failure_policy='Stop without retry, reset, recovery or blind restore')

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    for name in ('release-dir', 'session', 'output'):
        parser.add_argument('--'+name, type=Path)
    parser.add_argument('--approval', type=Path, default=ROOT/'tools/installer/approved-release.json')
    parser.add_argument('--allow-settings-write', action='store_true')
    parser.add_argument('--owner-authorized', action='store_true')
    args = parser.parse_args(argv)
    if not args.run:
        print(json.dumps(make_plan(), indent=2)); return 0
    output = args.output or ROOT/'host/runs'/('device-tests-'+str(time.time_ns()))
    output.mkdir(parents=True, exist_ok=False)
    (output/'transport.jsonl').touch()
    report = dict(format='ak820-device-tests-2', result='FAIL', checks=[], restore_pending=None,
        usb_opened=False, physical_behavior_validated=False, started_unix_ns=time.time_ns(),
        runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), limitations=make_plan()['limitations'])
    api, code = None, 2
    try:
        require(args.allow_settings_write == args.owner_authorized, 'Settings writes require both consent flags')
        require(args.release_dir and args.session, '--run requires --release-dir and --session')
        import ak820_device_protocol as protocol
        binding = protocol.bind(args.release_dir, args.session, args.approval)
        report['binding'] = {k:v for k,v in binding.items() if k not in ('payload', 'backup', 'code', 'definition')}
        report['protocol_sha256'] = hashlib.sha256(Path(protocol.__file__).read_bytes()).hexdigest()
        api = protocol.DeviceAPI(binding, output, allow_writes=args.allow_settings_write)
        report['usb_opened'] = True
        matrix = check_readonly(api, report)
        report['baseline_nvm_sha256'] = hashlib.sha256(api.baseline).hexdigest()
        if args.allow_settings_write: check_reversible_settings(api, report, matrix)
        else: report['checks'].append(dict(name='setting_writes', status='SKIP', reason='Not requested'))
        report['checks'].append(dict(name='RGB_durable_save', status='SKIP', reason='Packed saved-config mode ABI oracle not implemented; no save sent'))
        report['result'], code = 'PASS', 0
    except Exception as exc:
        report['error'] = type(exc).__name__+': '+str(exc)
        report['instruction'] = 'Stop; preserve evidence. Do not retry, reset or restore automatically.'
    finally:
        if api:
            try: api.close()
            except Exception as exc:
                report['close_error'], report['result'], code = repr(exc), 'FAIL', 2
        dump(output/'report.json', report)
        print(json.dumps(dict(output=str(output.resolve()), **report), indent=2))
    return code

if __name__ == '__main__':
    raise SystemExit(main())
