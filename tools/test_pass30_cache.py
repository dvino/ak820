"""Behavioral tests for the in-process PASS30 replay cache."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location(
    "configure_firmware", Path(__file__).with_name("configure_firmware.py"))
cf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cf)
REAL_REPLAY = cf._replay_pass30


class Pass30CacheTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.qmk = self.root / "qmk"
        self.build = self.qmk / "build"
        self.toolchain = self.root / "toolchain"
        self.tools = self.root / "tools"
        for path in (self.qmk, self.tools, self.build):
            path.mkdir(parents=True, exist_ok=True)
        for name in cf._PASS30_TREES:
            (self.build / name).mkdir(parents=True, exist_ok=True)
        (self.build / "default-keymap/generation.json").write_text(json.dumps({
            "dependencies": {str(self.root / 'bootstrap.c'): "x"}, "final_dependencies": {}}))
        (self.build / "parameter-spills-context.json").write_text(json.dumps({
            "provenance_sha256": {str(self.root / 'bootstrap-proof.json'): "x"}}))
        for path in (self.root / "bootstrap.c", self.root / "bootstrap-proof.json"):
            path.write_text("proof")
        (self.build / "parameter-spills-input/intermediate.asm").write_text("asm")
        (self.build / "parameter-spills-context.json").touch()
        for folder in (self.toolchain / "share/sdcc/include", self.toolchain / "share/sdcc/lib/large"):
            folder.mkdir(parents=True)
        for name in ("sdcc", "sdcpp", "sdas8051", "sdld", "sdar", "packihx", "s51"):
            path = self.toolchain / "bin" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name)
        (self.toolchain / "share/sdcc/include/std.h").write_text("header")
        (self.toolchain / "share/sdcc/lib/large/libc.lib").write_text("library")
        self.src = self.qmk / "keyboards/ak820/keymap.c"
        self.src.parent.mkdir(parents=True)
        self.src.write_text("source")
        checker = self.tools / "checker.py"
        checker.write_text("checker")
        self.artifact = self.build / "parameter-spills-input/proof.json"
        self.artifact.write_text("artifact")
        self.report = {
            "artifacts": [{"path": self.artifact.relative_to(self.qmk).as_posix()}],
            "sources": [{"origin": "source", "path": "keyboards/ak820/keymap.c"},
                        {"origin": "toolchain", "path": "share/sdcc/include/std.h"}],
            "meta": 1,
        }
        (self.build / "build-report.json").write_text(json.dumps(self.report))
        self.patches = (
            mock.patch.object(cf, "ROOT", self.root),
            mock.patch.object(cf, "QMK", self.qmk),
            mock.patch.object(cf, "_replay_pass30", return_value={"reports": [1]}),
        )
        for patcher in self.patches:
            patcher.start()
        cf._PASS30_CACHE.clear()

    def tearDown(self):
        for patcher in reversed(self.patches):
            patcher.stop()
        cf._PASS30_CACHE.clear()
        self.tmp.cleanup()

    def check(self):
        return cf.check_pass30(self.report, self.build, self.toolchain)

    def test_identical_inputs_replay_once_and_return_deep_copies(self):
        first = self.check()
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 1)
        first["reports"].append(2)
        self.assertEqual(self.check(), {"reports": [1]})

    def test_same_length_bytes_with_restored_mtime_invalidate(self):
        self.check()
        stamp = self.src.stat().st_mtime_ns
        self.src.write_text("SOURCE")
        import os
        os.utime(self.src, ns=(stamp, stamp))
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 2)

    def test_added_and_removed_intermediate_assembly_invalidate(self):
        self.check()
        extra = self.build / "parameter-spills-output/new.asm"
        extra.write_text("new")
        self.check()
        extra.unlink()
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 3)

    def test_dependency_and_external_provenance_changes_invalidate(self):
        self.check()
        (self.build / "parameter-spills-input/proof.d").write_text("dep")
        self.check()
        (self.root / "bootstrap-proof.json").write_text("fixed")
        self.check()
        (self.root / "bootstrap.c").write_text("changed dependency")
        self.check()
        (self.root / "generation-dep.c").write_text("dep")
        generation = json.loads((self.build / "default-keymap/generation.json").read_text())
        generation["dependencies"][str(self.root / "generation-dep.c")] = "x"
        (self.build / "default-keymap/generation.json").write_text(json.dumps(generation))
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 5)

    def test_source_checker_and_toolchain_closure_changes_invalidate(self):
        self.check()
        (self.qmk / "new-header.h").write_text("header")
        self.check()
        (self.tools / "checker.py").write_text("changed")
        self.check()
        (self.toolchain / "share/sdcc/lib/large/libc.lib").write_text("changed")
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 4)

    def test_symlink_retarget_same_content_invalidates(self):
        a, b, link = self.root / "a", self.root / "b", self.qmk / "linked.h"
        a.write_text("same")
        b.write_text("same")
        link.symlink_to(a)
        self.check()
        link.unlink()
        link.symlink_to(b)
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 2)

    def test_mutation_during_replay_is_rejected_and_not_cached(self):
        def mutate(*args):
            result = {"reports": [1]}
            self.src.write_text("mutated")
            return result
        cf._replay_pass30.side_effect = mutate
        with self.assertRaisesRegex(ValueError, "changed during replay"):
            self.check()
        cf._replay_pass30.side_effect = None
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 2)

    def test_failed_replay_is_retried_after_fix(self):
        cf._replay_pass30.side_effect = [RuntimeError("fail"), {"ok": True}]
        with self.assertRaisesRegex(RuntimeError, "fail"):
            self.check()
        self.assertEqual(self.check(), {"ok": True})
        self.assertEqual(cf._replay_pass30.call_count, 2)

    def test_regression_logs_outside_input_trees_do_not_invalidate(self):
        self.check()
        (self.build / "profile-test.log").write_text("tests")
        (self.build / "qualification.log").write_text("qualification")
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 1)

    def test_changed_report_metadata_invalidates(self):
        self.check()
        self.report["meta"] = 2
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 2)

    def test_environment_change_invalidates(self):
        import os
        self.check()
        with mock.patch.dict(os.environ, {"PASS30_TEST_INPUT": "changed"}):
            self.check()
        self.assertEqual(cf._replay_pass30.call_count, 2)

    def test_missing_snapshot_input_uses_full_validator_every_time(self):
        self.check()
        (self.build / 'build-report.json').unlink()
        cf._replay_pass30.side_effect = ValueError('full validator rejected input')
        for _ in range(2):
            with self.assertRaisesRegex(ValueError, 'full validator rejected input'):
                self.check()
            self.assertFalse(cf._PASS30_CACHE)
        self.assertEqual(cf._replay_pass30.call_count, 3)

    def test_directory_link_cannot_create_a_cache_entry(self):
        target = self.root / 'linked-stage'
        target.mkdir()
        stage = self.build / 'dce'
        stage.rmdir()
        stage.symlink_to(target, target_is_directory=True)
        self.check()
        self.check()
        self.assertEqual(cf._replay_pass30.call_count, 2)
        self.assertFalse(cf._PASS30_CACHE)


if __name__ == "__main__":
    unittest.main()
