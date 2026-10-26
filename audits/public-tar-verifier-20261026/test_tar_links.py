#!/usr/bin/env python3
"""Standalone external-verifier fixtures; no product imports or device access."""
import importlib.util
import io
import json
from pathlib import Path
import stat
import tarfile
import tempfile
import unittest

VERIFIER = Path(__file__).resolve().parents[1] / 'rc6/beta2-release-20261025/verify-public-assets.py'
spec = importlib.util.spec_from_file_location('public_verifier', VERIFIER)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class TarLinks(unittest.TestCase):
    def archive(self, members):
        path = Path(self.tmp.name) / 'fixture.tar.gz'
        with tarfile.open(path, 'w:gz') as archive:
            for name, kind, target in members:
                member = tarfile.TarInfo(name)
                member.type = kind
                member.mode = 0o755 if name.endswith('bin') else 0o600
                if kind == tarfile.REGTYPE:
                    member.size = len(target)
                    archive.addfile(member, io.BytesIO(target))
                else:
                    member.linkname = target
                    archive.addfile(member)
        return path

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_links_flatten_and_inherit_target_mode(self):
        path = self.archive([
            ('pkg', tarfile.DIRTYPE, ''),
            ('pkg/lib', tarfile.DIRTYPE, ''),
            ('pkg/lib/alias', tarfile.SYMTYPE, '../bin'),
            ('pkg/hard', tarfile.LNKTYPE, 'pkg/lib/alias'),
            ('pkg/chain', tarfile.SYMTYPE, 'hard'),
            ('pkg/nested', tarfile.SYMTYPE, 'lib/../bin'),
            ('pkg/bin', tarfile.REGTYPE, b'executable'),
        ])
        files, modes = v.tar_contents(path)
        self.assertEqual(set(files), {'pkg/bin','pkg/lib/alias','pkg/hard','pkg/chain','pkg/nested'})
        self.assertTrue(all(data == b'executable' for data in files.values()))
        self.assertTrue(all(mode == 0o755 for mode in modes.values()))
        dest = Path(self.tmp.name) / 'extracted'
        v.check_safe_extract(files, dest, modes)
        for name in files:
            out = dest / name
            self.assertFalse(out.is_symlink())
            self.assertTrue(stat.S_ISREG(out.stat().st_mode))
            self.assertEqual(out.read_bytes(), b'executable')
            self.assertEqual(stat.S_IMODE(out.stat().st_mode), 0o755)
        self.assertNotEqual((dest/'pkg/bin').stat().st_ino, (dest/'pkg/hard').stat().st_ino)
        self.assertEqual(v.tar_map(path), files)
        self.assertEqual(v.tar_modes(path), modes)

    def test_reject_adversarial_members(self):
        reg = ('pkg/bin', tarfile.REGTYPE, b'x')
        cases = {
            'absolute-member': [('/bad',tarfile.REGTYPE,b'x')],
            'escaping-member': [('../bad',tarfile.REGTYPE,b'x')],
            'backslash-member': [('pkg\\bad',tarfile.REGTYPE,b'x')],
            'dot-member': [('pkg/./bad',tarfile.REGTYPE,b'x')],
            'duplicate-file': [reg,reg],
            'duplicate-dir': [('pkg',tarfile.DIRTYPE,''),('pkg/',tarfile.DIRTYPE,'')],
            'file-dir-duplicate': [reg,('pkg/bin',tarfile.DIRTYPE,'')],
            'ancestor-file': [reg,('pkg/bin/child',tarfile.REGTYPE,b'x')],
            'ancestor-link': [('pkg/a',tarfile.SYMTYPE,'bin'),('pkg/a/child',tarfile.REGTYPE,b'x'),reg],
            'absolute-symlink': [reg,('pkg/a',tarfile.SYMTYPE,'/pkg/bin')],
            'absolute-hardlink': [reg,('pkg/a',tarfile.LNKTYPE,'/pkg/bin')],
            'escaping-symlink': [('pkg/a',tarfile.SYMTYPE,'../../outside')],
            'escaping-hardlink': [('pkg/a',tarfile.LNKTYPE,'../outside')],
            'missing-parent-traversal': [reg,('pkg/a',tarfile.SYMTYPE,'missing/../bin')],
            'file-parent-traversal': [reg,('pkg/a',tarfile.SYMTYPE,'bin/../bin')],
            'link-parent-traversal': [reg,('pkg/b',tarfile.SYMTYPE,'bin'),('pkg/a',tarfile.SYMTYPE,'b/../bin')],
            'nested-missing-alias': [reg,('pkg/b',tarfile.SYMTYPE,'missing/../bin'),('pkg/a',tarfile.SYMTYPE,'b')],
            'file-trailing-slash': [reg,('pkg/a',tarfile.SYMTYPE,'bin/')],
            'hardlink-missing-parent': [reg,('pkg/a',tarfile.LNKTYPE,'pkg/missing/../bin')],
            'missing-target': [('pkg/a',tarfile.SYMTYPE,'absent')],
            'empty-target': [('pkg/a',tarfile.SYMTYPE,'')],
            'backslash-target': [('pkg/a',tarfile.SYMTYPE,'b\\c')],
            'self-cycle': [('pkg/a',tarfile.SYMTYPE,'a')],
            'mixed-cycle': [('pkg/a',tarfile.SYMTYPE,'b'),('pkg/b',tarfile.LNKTYPE,'pkg/a')],
            'directory-target': [('pkg',tarfile.DIRTYPE,''),('a',tarfile.LNKTYPE,'pkg')],
            'fifo': [('fifo',tarfile.FIFOTYPE,'')],
            'character-device': [('dev',tarfile.CHRTYPE,'')],
            'block-device': [('dev',tarfile.BLKTYPE,'')],
            'unknown-type': [('unknown',b'Z','')],
        }
        for label, members in cases.items():
            with self.subTest(label=label):
                path = self.archive(members)
                for helper in (v.tar_map, v.tar_modes):
                    with self.assertRaises(ValueError): helper(path)

if __name__ == '__main__':
    unittest.main(verbosity=2)
