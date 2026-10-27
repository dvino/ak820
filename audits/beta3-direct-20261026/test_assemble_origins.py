"""Offline negative tests for the audit-only origin orchestration boundary."""
import copy
import importlib.util
import json
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from contextlib import redirect_stderr
import io
import zipfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('assemble_origins', HERE / 'assemble_origins.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class BoundaryTests(unittest.TestCase):
    def test_proof_and_assembly_toolchains_are_distinct_but_byte_identical(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shared = root / 'shared'
            origin = root / 'origin'
            for rel in ('shared/bin', 'origin/mirror/bin'):
                path = root / rel
                path.mkdir(parents=True)
                (path / 'sdcc').write_bytes(b'pinned tool')
            (origin / 'toolchains').symlink_to(shared, target_is_directory=True)
            with patch.object(a, 'ROOT', root):
                proof_path = (origin / 'toolchains').resolve()
                assembly_path = a.checked(origin, Path('mirror'))
                proof = a.toolchain_inventory(proof_path)
                mirror = a.toolchain_inventory(assembly_path)
                self.assertEqual(proof, mirror)
                a.require_same_toolchain(proof, mirror)
                self.assertEqual(proof['bin/sdcc'], hashlib.sha256(b'pinned tool').hexdigest())
                self.assertEqual(proof_path, shared)
                self.assertEqual(assembly_path, origin / 'mirror')
                (origin / 'mirror/bin/sdcc').write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError, 'differs'):
                    a.require_same_toolchain(proof, a.toolchain_inventory(assembly_path))

    def test_toolchain_inventory_rejects_symlinks_and_external_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'tools').mkdir()
            (root / 'tools/link').symlink_to(root / 'outside')
            with patch.object(a, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'Symlink'):
                    a.toolchain_inventory((root / 'tools').resolve())
                with self.assertRaises(ValueError):
                    a.checked(root, Path('../outside'))

    def test_failed_worker_diagnostic_is_preserved_and_status_propagates(self):
        with tempfile.TemporaryDirectory() as folder:
            log = Path(folder) / 'worker.log'
            error = subprocess.CalledProcessError(9, ['worker'])
            def fail(*args, **kwargs):
                kwargs['stdout'].write(b'actual worker failure detail\n')
                raise error
            stderr = io.StringIO()
            with patch.object(a.subprocess, 'run', side_effect=fail), redirect_stderr(stderr):
                with self.assertRaises(subprocess.CalledProcessError) as raised:
                    a.run_worker_process(['worker'], folder, log)
            self.assertIs(raised.exception, error)
            self.assertIn('actual worker failure detail', log.read_text())
            self.assertIn('actual worker failure detail', stderr.getvalue())

    def test_incomplete_and_duplicate_origins_rejected(self):
        with self.assertRaisesRegex(ValueError, 'exactly ten'):
            a.origins([])
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                a.origins(['main=' + folder, 'main=' + folder])

    def test_path_escape_and_symlink_rejected(self):
        for path in ('../policy', '/tmp/policy', 'x/../../policy'):
            with self.assertRaises(ValueError):
                a.relative(path)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'link').symlink_to(root, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, 'Symlink'):
                a.checked(root, 'link/policy')

    def test_catalog_order_and_duplicates_rejected_before_measurement(self):
        for rows in ([], [{'profile': 'main'}] * 10,
                     [{'profile': name} for name in reversed(a.ci.release_profile_names())]):
            with self.assertRaisesRegex(ValueError, 'ten ordered'):
                a.catalog_rows({'format': a.matrix.FORMAT, 'settings_transitions': [], 'profiles': rows})

    def test_unqualified_row_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Incomplete exact-profile'):
            a.bind_row('main', {'profile': 'main', 'configuration': a.profiles.configuration('main')}, {}, {})

    def test_stale_identity_configuration_and_approval_claims_rejected(self):
        configuration = a.profiles.configuration('main')
        identity = {'profile': 'main', 'ihx_sha256': 'a' * 64,
                    'nvm_schema': configuration['nvm_schema']}
        row = {'profile': 'main', 'configuration': configuration, 'identity': identity,
               'measurement_status': 'linked-memory-pass', 'runtime_status': 'exact-image-pass',
               'offline_tests_status': 'exact-image-pass', 'release_approved': False, 'installable': False}
        approved = {'identity': identity, 'reproducible_identity': identity,
                    'settings_identity': identity, 'configuration': configuration,
                    'release_approved': False, 'installable': False}
        self.assertEqual(a.bind_row('main', row, approved, identity)['settings_status'], 'exact-image-contract')
        for key, value in (('release_approved', True), ('installable', True),
                           ('reproducible_identity', dict(identity, ihx_sha256='b' * 64)),
                           ('settings_identity', dict(identity, nvm_schema=-1)),
                           ('configuration', a.profiles.configuration('game'))):
            changed = copy.deepcopy(approved)
            changed[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Static settings contract'):
                a.bind_row('main', row, changed, identity)
        with self.assertRaisesRegex(ValueError, 'claims approval'):
            a.bind_row('main', dict(row, installable=True), approved, identity)

    def test_partial_or_duplicate_results_rejected(self):
        for rows in ([], [{'profile': 'main'}] * 10):
            with self.assertRaisesRegex(ValueError, 'exactly ten ordered'):
                a.combine(rows, {})

    def test_changed_source_and_missing_committed_helper_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL)
            git('init')
            (root / 'source').write_text('approved')
            git('add', 'source')
            git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'fixture')
            head = git('rev-parse', 'HEAD').decode().strip()
            with self.assertRaisesRegex(ValueError, 'helper must be committed'):
                a.source_snapshot(root, head)
            (root / 'source').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'Tracked source differs'):
                a.source_snapshot(root, head)
            with self.assertRaisesRegex(ValueError, 'HEAD differs'):
                a.source_snapshot(root, '0' * 40)

    def test_dangling_worker_siblings_rejected_without_touching_sentinel(self):
        for suffix in ('.zip', '.zip.sha256', '.worker.json'):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                output = root / 'bundle'
                sentinel = root / 'missing-sentinel'
                sibling = output.with_suffix(suffix)
                sibling.symlink_to(sentinel)
                with self.assertRaisesRegex(ValueError, 'Worker output already exists'):
                    a.require_fresh_worker_output(output)
                with patch.object(a, 'ROOT', root), patch.object(a, 'source_snapshot') as snapshot:
                    with self.assertRaisesRegex(ValueError, 'Worker output already exists'):
                        a.worker(SimpleNamespace(output='bundle', worker='main'))
                    snapshot.assert_not_called()
                self.assertTrue(sibling.is_symlink())
                self.assertEqual(sibling.readlink(), sentinel)
                self.assertFalse(sentinel.exists())

    def test_archive_is_sorted_fixed_metadata_and_byte_preserving(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'bundle'
            source.mkdir()
            (source / 'z').write_bytes(b'z')
            (source / 'a').write_bytes(b'a')
            output = root / 'bundle.zip'
            a.archive_tree(source, output, 'profiles/main/')
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.namelist(), ['profiles/main/a', 'profiles/main/z'])
                for info in archive.infolist():
                    self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                    self.assertEqual(info.external_attr, 0o100644 << 16)
                self.assertEqual(archive.read('profiles/main/a'), b'a')
            self.assertEqual(output.with_suffix('.zip.sha256').read_text(), a.sha(output) + '  bundle.zip\n')


if __name__ == '__main__':
    unittest.main()
