#!/usr/bin/env python3
"""Build and verify the offline AK820 Windows GUI and CLI package.

Run on native Windows with the pinned build requirements. The build and smoke
checks never open USB. Personal backups and runtime sessions are not packaged.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools' / 'installer'))
import ak820
from ak820_release_manifest import HOST_FILES

FORMAT = 'ak820-windows-package-v1'

# User-facing guide closure for the standalone installer. Keep this explicit:
# never discover Markdown by walking the repository, which also contains
# private audits and development notes.
PUBLIC_GUIDES = (
    'README.md', 'docs/ru/README.md',
    'docs/profiles/README.md', 'docs/ru/profiles/README.md',
    *(f'docs/profiles/{profile}.md' for profile in
      ('main', 'game', 'mmo', 'typing', 'code', 'pointer', 'onehand', 'creative', 'shortcuts', 'multios')),
    *(f'docs/ru/profiles/{profile}.md' for profile in
      ('main', 'game', 'mmo', 'typing', 'code', 'pointer', 'onehand', 'creative', 'shortcuts', 'multios')),
    *(f'docs/{name}.md' for name in (
      'FEATURES', 'CONFIGURATION', 'INSTALL', 'COMBOS', 'SETTINGS-BACKUP', 'DIRECT',
      'BUILD-PROFILES', 'MODULE-MATRIX', 'STATUS', 'COMPACT-MOUSE-KEYS', 'COMPACT_AUTOSHIFT',
      'TAP-HOLD', 'GUI-CONTROL', 'COMPACT-DYNAMIC-MACROS', 'COMPACT-LEADER',
      'INDICATORS', 'MAC-PC', 'COMPACT-TAP-DANCE', 'COMPACT-KEY-OVERRIDES',
      'QMK-SETTINGS', 'MODULE-STORAGE')),
    *(f'docs/ru/{name}.md' for name in (
      'FEATURES', 'CONFIGURATION', 'INSTALL', 'COMBOS', 'SETTINGS-BACKUP', 'DIRECT',
      'BUILD-PROFILES', 'MODULE-MATRIX', 'STATUS', 'COMPACT-MOUSE-KEYS', 'COMPACT_AUTOSHIFT',
      'TAP-HOLD', 'GUI-CONTROL', 'COMPACT-DYNAMIC-MACROS', 'COMPACT-LEADER',
      'INDICATORS', 'MAC-PC', 'COMPACT-TAP-DANCE', 'COMPACT-KEY-OVERRIDES',
      'QMK-SETTINGS', 'MODULE-STORAGE')),
    'web/docs/OS-INDICATOR-PROTOCOL.md',
    'web/docs/ru/OS-INDICATOR-PROTOCOL.md',
)

# Images embedded by the public English and Russian READMEs. Keep these paths
# explicit so package inventory never admits arbitrary repository binaries.
PUBLIC_ASSETS = (
    'docs/images/banner.webp', 'docs/images/pcb.webp',
    'docs/images/controller.webp', 'docs/images/pcb-markings.webp',
)


def guide_files():
    """Return the fixed guide and README image allowlists after strict checks."""
    for name in (*PUBLIC_GUIDES, *PUBLIC_ASSETS):
        path = Path(name)
        allowed_root = (path.parts[0] == 'docs' or name == 'README.md' or name in (
            'web/docs/OS-INDICATOR-PROTOCOL.md',
            'web/docs/ru/OS-INDICATOR-PROTOCOL.md',
        ))
        if path.is_absolute() or '..' in path.parts or not allowed_root:
            raise ValueError('Unsafe public guide path: ' + name)
        source = ROOT / path
        current = ROOT
        has_symlink = False
        for part in path.parts:
            current = current / part
            has_symlink |= current.is_symlink()
        if has_symlink or not source.is_file():
            raise ValueError('Missing or unsafe public guide: ' + name)
        if name in PUBLIC_GUIDES:
            try:
                source.read_text(encoding='utf-8')
            except UnicodeError as error:
                raise ValueError('Invalid UTF-8 public guide: ' + name) from error
        elif source.suffix.lower() != '.webp':
            raise ValueError('Invalid public guide asset type: ' + name)
    return [*PUBLIC_GUIDES, *PUBLIC_ASSETS]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def package_files():
    """Return the explicit release/host allowlist; never scan personal data."""
    names = set(HOST_FILES)
    names.update(guide_files())
    contexts = ak820.release_contexts(approved=True)
    if not contexts:
        raise ValueError('No approved profiles are available for standalone packaging')
    for context in contexts:
        manifest = context.manifest
        if manifest.get('install_modes') != ['permanent', 'trial']:
            raise ValueError('Standalone permanent installer requires every selectable profile to support permanent install')
        relative_bundle = context.bundle.relative_to(ROOT)
        relative_approval = context.approval.relative_to(ROOT)
        names.update((relative_bundle / name).as_posix() for name in manifest['files'])
        names.add((relative_bundle / 'installer-release.json').as_posix())
        names.add(relative_approval.as_posix())
    for name in names:
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] in ('evidence', 'host'):
            raise ValueError('Unsafe standalone package input: ' + name)
        if not (ROOT / path).is_file():
            raise ValueError('Missing standalone package input: ' + name)
    return sorted(names)


def build_commands(output: Path, work: Path, names: list[str]):
    common = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir',
              '--contents-directory', '_internal',
              '--distpath', str(output), '--workpath', str(work / 'work'), '--specpath', str(work),
              '--paths', str(ROOT / 'tools/installer'), '--paths', str(ROOT / 'tools'),
              '--paths', str(ROOT / 'qmk-8051-ak820/util'), '--hidden-import', 'hid']
    for name in names:
        common.extend(['--add-data', str(ROOT / name) + ';' + str(Path(name).parent)])
    return [common + ['--windowed', '--name', 'AK820', str(ROOT / 'tools/installer/gui.py')],
            common + ['--console', '--name', 'AK820-cli', str(ROOT / 'tools/installer/ak820.py')]]


def snapshot_inputs(names: list[str]) -> dict[str, str]:
    return {name: sha256(ROOT / name) for name in names}


def verify_collected(app_dir: Path, names: list[str]) -> dict[str, str]:
    # PyInstaller 6 onedir uses _internal as its default contents directory.
    contents = app_dir / '_internal'
    result = {}
    for name in names:
        bundled = contents / Path(name)
        if not bundled.is_file():
            raise RuntimeError(f'{app_dir.name} is missing packaged approved input: {name}')
        expected = sha256(ROOT / name)
        actual = sha256(bundled)
        if actual != expected:
            raise RuntimeError(f'{app_dir.name} packaged input hash mismatch: {name}')
        result[name] = actual
    return result


def verify_sources_unchanged(hashes: dict[str, str]) -> None:
    for name, expected in hashes.items():
        actual = sha256(ROOT / name)
        if actual != expected:
            raise RuntimeError(f'Approved input changed during build: {name}')


def write_package(output: Path, archive: Path, names: list[str], initial_hashes: dict[str, str]):
    """Smoke, attest and archive a synthetic or real pair of completed apps."""
    gui_dir, cli_dir = output / 'AK820', output / 'AK820-cli'
    gui_exe, cli_exe = gui_dir / 'AK820.exe', cli_dir / 'AK820-cli.exe'
    if not gui_exe.is_file() or not cli_exe.is_file():
        raise RuntimeError('PyInstaller did not create both expected application directories')
    collected = {'AK820': verify_collected(gui_dir, names),
                 'AK820-cli': verify_collected(cli_dir, names)}
    if initial_hashes != {name: collected['AK820'][name] for name in names}:
        raise RuntimeError('GUI collected inputs differ from pre-build approved input hashes')
    if initial_hashes != {name: collected['AK820-cli'][name] for name in names}:
        raise RuntimeError('CLI collected inputs differ from pre-build approved input hashes')
    subprocess.run([str(cli_exe), '--help'], check=True, cwd=output)
    subprocess.run([str(cli_exe), 'verify'], check=True, cwd=output)
    # This creates and destroys Tk widgets; it does not test manual interaction.
    subprocess.run([str(gui_exe), '--self-test'], check=True, cwd=output)
    verify_sources_unchanged(initial_hashes)
    after_smoke = {'AK820': verify_collected(gui_dir, names),
                   'AK820-cli': verify_collected(cli_dir, names)}
    if after_smoke != collected:
        raise RuntimeError('Packaged approved inputs changed during smoke checks')
    shutil.copyfile(ROOT / 'AK820.cmd', output / 'AK820.cmd')
    if sha256(output / 'AK820.cmd') != initial_hashes['AK820.cmd']:
        raise RuntimeError('Copied launcher does not match the approved input')
    release_contexts = ak820.release_contexts(approved=True)
    release_reports = {}
    for context in release_contexts:
        manifest_name = (context.bundle.relative_to(ROOT) / 'installer-release.json').as_posix()
        release_reports[context.profile] = {'manifest': manifest_name,
            'manifest_sha256': initial_hashes[manifest_name]}
    report = {
        'format': FORMAT,
        'platform': {'system': 'Windows', 'python': sys.version.split()[0], 'pyinstaller': '6.16.0'},
        'releases': release_reports,
        'approved_inputs': initial_hashes,
        'collected_inputs': collected,
        'apps': {'gui_exe_sha256': sha256(gui_exe), 'cli_exe_sha256': sha256(cli_exe)},
        'checks': {'cli_help': 'passed', 'offline_verify': 'passed',
                   'native_tk_ui_smoke': 'passed'},
        'limits': ['No USB enumeration or access was performed.',
                   'Native UI smoke creates and destroys Tk widgets; it does not verify manual interaction, display scaling, or accessibility.',
                   'No physical keyboard, USB protocol, firmware update, or settings persistence was tested.'],
        'private_data': 'OEM backups and runtime sessions were not included.',
    }
    (output / 'build-provenance.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    (output / 'smoke-report.json').write_text(json.dumps(report['checks'] | {'limits': report['limits']}, indent=2) + '\n', encoding='utf-8')
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(output.rglob('*')):
            if path.is_file():
                bundle.write(path, (Path(output.name) / path.relative_to(output)).as_posix())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist' / 'AK820-Windows')
    parser.add_argument('--work', type=Path, default=ROOT / '.build-windows-installer')
    args = parser.parse_args(argv)
    if sys.platform != 'win32':
        parser.error('Build and Tk UI smoke must run on native Windows; cross-compiling is unsupported')
    if importlib.metadata.version('pyinstaller') != '6.16.0':
        parser.error('Use the pinned requirements-build-windows.txt environment')
    output = args.output.resolve()
    work = args.work.resolve()
    archive = Path(str(output) + '.zip')
    if output.exists() or archive.exists():
        parser.error(f'refusing to overwrite existing output or ZIP: {output} / {archive}')
    names = package_files()
    initial_hashes = snapshot_inputs(names)
    work.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    for command in build_commands(output, work, names):
        subprocess.run(command, check=True, cwd=ROOT)

    write_package(output, archive, names, initial_hashes)
    print('Portable package:', archive)
    print('GUI and CLI full directories, launcher, provenance and smoke report verified.')


if __name__ == '__main__':
    main()
