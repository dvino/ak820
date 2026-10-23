"""Offline safety tests for the pinned LUFA dependency installer."""
import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import tarfile
import unittest


SCRIPT = Path(__file__).with_name("install_lufa_dependency.py")
spec = importlib.util.spec_from_file_location("install_lufa_dependency", SCRIPT)
lufa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lufa)


class LufaDependencyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ak820-lufa-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.files = {
            "LUFA/License.txt": b"license text\n",
            "LUFA/Common/USB.h": b"header bytes\n",
            "README.txt": b"complete archive payload\n",
        }
        self.lock = {
            "format": "ak820-external-dependency-1",
            "name": "lufa",
            "repository": "https://example.invalid/lufa",
            "revision": "a" * 40,
            "download_url": "https://example.invalid/lufa.tar.gz",
            "archive_root": "lufa-" + "a" * 40,
            "archive_sha256": "",
            "destination": "lib/lufa",
            "license_path": "LUFA/License.txt",
            "required_files": {
                name: hashlib.sha256(self.files[name]).hexdigest()
                for name in ("LUFA/License.txt", "LUFA/Common/USB.h")
            },
        }
        self.archive = self.root / "lufa.tar.gz"
        self.write_archive()

    def write_archive(self, extra=(), symlink=False):
        with tarfile.open(self.archive, "w:gz") as tar:
            root = self.lock["archive_root"]
            root_info = tarfile.TarInfo(root + "/")
            root_info.type = tarfile.DIRTYPE
            tar.addfile(root_info)
            for name, content in self.files.items():
                info = tarfile.TarInfo(root + "/" + name)
                info.size = len(content)
                tar.addfile(info, io.BytesIO(content))
            for name, content in extra:
                info = tarfile.TarInfo(root + "/" + name)
                info.size = len(content)
                tar.addfile(info, io.BytesIO(content))
            if symlink:
                info = tarfile.TarInfo(root + "/link")
                info.type = tarfile.SYMTYPE
                info.linkname = "../../outside"
                tar.addfile(info)
        self.lock["archive_sha256"] = hashlib.sha256(self.archive.read_bytes()).hexdigest()

    def test_installs_verified_archive_atomically(self):
        target = self.root / "checkout" / "lib" / "lufa"
        target.parent.mkdir(parents=True)
        self.assertTrue(lufa.install_archive(self.archive, target, self.lock))
        self.assertEqual((target / "LUFA" / "License.txt").read_bytes(), self.files["LUFA/License.txt"])
        self.assertEqual((target / "README.txt").read_bytes(), self.files["README.txt"])
        self.assertFalse(lufa.install_archive(self.archive, target, self.lock))

    def test_default_style_check_detects_mismatch(self):
        target = self.root / "lib" / "lufa"
        (target / "LUFA" / "Common").mkdir(parents=True)
        (target / "LUFA" / "License.txt").write_bytes(self.files["LUFA/License.txt"])
        (target / "LUFA" / "Common" / "USB.h").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            lufa.check_existing(target, self.lock)

    def test_divergent_destination_is_never_overwritten(self):
        target = self.root / "lib" / "lufa"
        target.mkdir(parents=True)
        sentinel = target / "local-change"
        sentinel.write_text("preserve", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
            lufa.install_archive(self.archive, target, self.lock)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")

    def test_archive_hash_mismatch_stops_before_install(self):
        target = self.root / "lib" / "lufa"
        self.lock["archive_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "differs from the pinned"):
            lufa.install_archive(self.archive, target, self.lock)
        self.assertFalse(target.exists())

    def test_archive_rejects_path_traversal(self):
        self.write_archive(extra=(("../../escape", b"bad"),))
        with self.assertRaisesRegex(ValueError, "Unsafe archive path"):
            lufa.install_archive(self.archive, self.root / "lib" / "lufa", self.lock)
        self.assertFalse((self.root / "escape").exists())

    def test_archive_rejects_symlink(self):
        self.write_archive(symlink=True)
        with self.assertRaisesRegex(ValueError, "link or special file"):
            lufa.install_archive(self.archive, self.root / "lib" / "lufa", self.lock)

    def test_archive_checks_required_file_hashes(self):
        self.files["LUFA/Common/USB.h"] = b"unreviewed bytes"
        self.write_archive()
        with self.assertRaisesRegex(ValueError, "file hash mismatch"):
            lufa.install_archive(self.archive, self.root / "lib" / "lufa", self.lock)


if __name__ == "__main__":
    unittest.main()
