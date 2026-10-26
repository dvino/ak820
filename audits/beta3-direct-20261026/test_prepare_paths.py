"""Offline checks for explicit profile build locations."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('prepare_release', Path(__file__).with_name('prepare_release.py'))
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class BuildPaths(unittest.TestCase):
    def test_default_and_override_preserve_actual_build_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root / 'qmk-8051-ak820' / '.build'
            default = base / 'group-a' / 'main'
            explicit = base / 'group-b' / 'code'
            default.mkdir(parents=True)
            explicit.mkdir(parents=True)
            args = SimpleNamespace(builds_root=base / 'group-a', build_overrides={'code': explicit})
            with patch.object(prepare, 'ROOT', root):
                self.assertEqual(prepare.profile_build(args, 'main'), default.resolve())
                self.assertEqual(prepare.profile_build(args, 'code'), explicit.resolve())

    def test_missing_external_and_symlink_builds_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root / 'qmk-8051-ak820' / '.build'
            base.mkdir(parents=True)
            external = root / 'external'
            external.mkdir()
            link = base / 'linked'
            link.symlink_to(external, target_is_directory=True)
            with patch.object(prepare, 'ROOT', root):
                for path in (base / 'missing', external, link):
                    args = SimpleNamespace(builds_root=base, build_overrides={'main': path})
                    with self.subTest(path=path), self.assertRaises(ValueError):
                        prepare.profile_build(args, 'main')


if __name__ == '__main__':
    unittest.main()
