"""Offline tests for the pinned SDCC 4.6 installer and archive boundary."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import contextlib
import io as stringio
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "install_sdcc46_toolchain", ROOT / "tools" / "install_sdcc46_toolchain.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / ".build")
        self.base = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def make_archive(self, members):
        path = self.base / "fixture.tar.bz2"
        with tarfile.open(path, "w:bz2") as archive:
            root = tarfile.TarInfo("sdcc-4.6.0")
            root.type = tarfile.DIRTYPE
            archive.addfile(root)
            for name, payload, kind in members:
                item = tarfile.TarInfo("sdcc-4.6.0/" + name)
                if kind == "dir":
                    item.type = tarfile.DIRTYPE
                    archive.addfile(item)
                elif kind == "symlink":
                    item.type = tarfile.SYMTYPE
                    item.linkname = payload
                    archive.addfile(item)
                else:
                    data = payload if isinstance(payload, bytes) else payload.encode()
                    item.size = len(data)
                    item.mode = 0o755
                    archive.addfile(item, io.BytesIO(data))
        return path

    def install_fixture(self, archive, target):
        pins = {name: hashlib.sha256(name.encode()).hexdigest()
                for name in installer.EXECUTABLE_PINS}
        return installer.install_archive(
            archive, target, expected_sha=installer.sha256(archive),
            expected_size=archive.stat().st_size, executable_pins=pins)

    def fixture_members(self):
        return [("bin", "", "dir"),
                *(("bin/" + name, name.encode(), "file")
                  for name in installer.EXECUTABLE_PINS)]

    def test_offline_archive_installs_to_local_target_and_is_idempotent(self):
        archive = self.make_archive(self.fixture_members())
        target = self.base / "local-toolchains" / "sdcc-4.6.0"
        version = mock.Mock(returncode=0, stdout="SDCC 4.6.0 fixture", stderr="")
        with mock.patch.object(installer.subprocess, "run", return_value=version):
            installed = self.install_fixture(archive, target)
            second = self.install_fixture(archive, target)
        self.assertFalse(installed["already_installed"])
        self.assertTrue(second["already_installed"])
        receipt = json.loads((target / "ak820-toolchain-receipt.json").read_text())
        self.assertEqual(receipt["archive_sha256"], installer.sha256(archive))
        for name in installer.EXECUTABLE_PINS:
            self.assertEqual(installer.sha256(target / "bin" / name),
                             hashlib.sha256(name.encode()).hexdigest())

    def test_wrong_archive_hash_is_rejected_before_target_creation(self):
        archive = self.make_archive(self.fixture_members())
        target = self.base / "local-toolchains" / "sdcc-4.6.0"
        with self.assertRaisesRegex(ValueError, "SHA256"):
            installer.install_archive(archive, target, expected_sha="0" * 64,
                                      expected_size=archive.stat().st_size)
        self.assertFalse(target.exists())

    def test_wrong_archive_size_is_rejected(self):
        archive = self.make_archive(self.fixture_members())
        with self.assertRaisesRegex(ValueError, "size mismatch"):
            installer.verify_archive(archive, expected_size=archive.stat().st_size + 1)

    def test_parent_traversal_is_rejected_before_extraction(self):
        archive = self.make_archive([("../outside", b"x", "file")])
        target = self.base / "local-toolchains" / "sdcc-4.6.0"
        with self.assertRaisesRegex(ValueError, "escapes expected SDCC root"):
            self.install_fixture(archive, target)
        self.assertFalse(target.exists())

    def test_absolute_and_escaping_symlinks_are_rejected(self):
        for link in ("/tmp/outside", "../../outside"):
            with self.subTest(link=link):
                archive = self.make_archive([("bin", "", "dir"),
                                             ("bin/escape", link, "symlink")])
                with tarfile.open(archive, "r:bz2") as opened:
                    with self.assertRaisesRegex(ValueError, "(Absolute symlink|Link escapes)"):
                        installer.validate_members(opened)

    def test_duplicate_member_is_rejected(self):
        archive = self.make_archive([("bin", "", "dir"), ("bin/a", b"one", "file"),
                                     ("bin/a", b"two", "file")])
        with tarfile.open(archive, "r:bz2") as opened:
            with self.assertRaisesRegex(ValueError, "Duplicate archive member"):
                installer.validate_members(opened)

    def test_redirect_allowlist_requires_https_sourceforge(self):
        self.assertTrue(installer.trusted_source("https://pilotfiber.dl.sourceforge.net/file"))
        self.assertFalse(installer.trusted_source("http://downloads.sourceforge.net/file"))
        self.assertFalse(installer.trusted_source("https://example.com/file"))

    def test_cli_local_archive_path_does_not_download(self):
        archive = self.base / "already-downloaded.tar.bz2"
        archive.write_bytes(b"fixture")
        target = self.base / "local-toolchains" / "sdcc-4.6.0"
        output = stringio.StringIO()
        with (mock.patch.object(sys, "argv", ["installer", "--archive", str(archive),
                                               "--target", str(target)]),
              mock.patch.object(installer, "verify_archive", return_value={"bytes": 7,
                                                                           "sha256": "a" * 64}),
              mock.patch.object(installer, "download_archive",
                                side_effect=AssertionError("offline setup attempted a download")),
              mock.patch.object(installer, "install_archive", return_value={
                  "installed_directory": str(target), "already_installed": False}),
              mock.patch.object(installer.platform, "system", return_value="Linux"),
              contextlib.redirect_stdout(output)):
            installer.main()
        result = json.loads(output.getvalue())
        self.assertTrue(result["offline_archive"])
        self.assertEqual(result["download"]["bytes"], 7)


if __name__ == "__main__":
    unittest.main()
