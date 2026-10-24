"""Offline consistency gates for a release assembled after independent review."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_release_bundle as builder
import ak820_profiles
from build_release_bundle import ROOT, validate_review, validate_build_artifact, host_manifest


class ReviewBindingTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="ak820-review-test-")
        self.addCleanup(self.directory.cleanup)
        root = Path(self.directory.name)
        self.files = [root / name for name in ("app.ihx", "app.map", "build.json")]
        for index, path in enumerate(self.files):
            path.write_bytes(bytes([index]))
        self.review = root / "review.md"
        self.record = {
            "format": "ak820-offline-review-2", "release": "rc6", "status": "passed",
            "hardware_validated": False,
            "host_files": host_manifest(ROOT),
            "build": {name: hashlib.sha256(path.read_bytes()).hexdigest()
                      for name, path in zip(("ihx_sha256", "map_sha256", "build_report_sha256"),
                                            self.files)},
        }

    def write_review(self, record=None):
        self.review.write_text("# Review\n\n```json\n" + json.dumps(record or self.record)
                               + "\n```\n", encoding="utf-8")

    def test_exact_build_accepted(self):
        self.write_review()
        validate_review(self.review, *self.files)

    def test_changed_artifact_rejected(self):
        self.write_review()
        for path in self.files:
            original = path.read_bytes()
            path.write_bytes(original + b"changed")
            with self.subTest(path=path.name), self.assertRaisesRegex(ValueError, "different build"):
                validate_review(self.review, *self.files)
            path.write_bytes(original)

    def test_missing_or_duplicate_record_rejected(self):
        self.review.write_text("# A review without a build binding\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            validate_review(self.review, *self.files)
        self.write_review()
        self.review.write_text(self.review.read_text() * 2)
        with self.assertRaisesRegex(ValueError, "exactly one"):
            validate_review(self.review, *self.files)

    def test_pending_or_hardware_claim_rejected(self):
        for key, value in (("status", "pending"), ("hardware_validated", True)):
            with self.subTest(key=key):
                self.write_review(dict(self.record, **{key: value}))
                with self.assertRaisesRegex(ValueError, "offline pass"):
                    validate_review(self.review, *self.files)

    def test_host_code_must_match_the_independent_review(self):
        self.write_review()
        changed = dict(self.record['host_files'])
        changed['AK820.sh'] = {'size': 1, 'sha256': 'changed'}
        with patch('build_release_bundle.host_manifest', return_value=changed):
            with self.assertRaisesRegex(ValueError, 'different host code'):
                validate_review(self.review, *self.files)


class BuildArtifactTests(unittest.TestCase):
    def test_memory_report_is_bound_by_size_and_hash(self):
        with tempfile.TemporaryDirectory(prefix="ak820-mem-test-") as directory:
            root = Path(directory)
            path = root / "application.mem"
            path.write_bytes(b"correct report")
            item = {"path": path.name, "size": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            report = {"artifacts": [item]}
            with patch("build_release_bundle.SOURCE", root):
                validate_build_artifact(report, path)
                for invalid in (b"changed report", b"truncated"):
                    path.write_bytes(invalid)
                    with self.subTest(invalid=invalid), self.assertRaisesRegex(ValueError, "differs"):
                        validate_build_artifact(report, path)
                with self.assertRaisesRegex(ValueError, "Missing or ambiguous"):
                    validate_build_artifact({"artifacts": [item, item]}, path)


class ToolSelectionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="ak820-tools-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / "qmk-8051-ak820"
        self.default = self.root / "toolchains/sdcc-4.4.0"
        self.selected = self.root / ".build/sdcc-4.6.0"
        self.production = self.source / "util/build_ak820.py"
        self.custom = self.root / ".build/build_ak820_experimental.py"
        for path in [self.production, self.custom, self.source / "util/ak820_dce.py"] + [
                root / "bin" / name for root in (self.default, self.selected)
                for name in builder.SDCC46_PINS]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(str(path.relative_to(self.root)).encode())
        for name, value in (("ROOT", self.root), ("SOURCE", self.source)):
            mock = patch.object(builder, name, value)
            mock.start()
            self.addCleanup(mock.stop)

    def report(self, toolchain, source):
        return {field: builder.sha(path) for field, path in {
            "compiler_sha256": toolchain / "bin/sdcc",
            "assembler_sha256": toolchain / "bin/sdas8051",
            "builder_sha256": source,
            "dce_sha256": self.source / "util/ak820_dce.py",
        }.items()}

    def pins(self):
        # Fixtures exercise the gates without shipping or executing a compiler.
        return patch.object(builder, "SDCC46_PINS", {
            name: builder.sha(self.selected / "bin" / name) for name in builder.SDCC46_PINS})

    def test_default_44_still_checks_report_and_inputs(self):
        report = self.report(self.default, self.production)
        with patch.object(builder, "validate_inputs") as inputs:
            self.assertEqual(builder.validate_tools(report), (self.default, self.production))
            inputs.assert_called_once_with(report, self.source, self.default)
            for field in report:
                with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                    builder.validate_tools(dict(report, **{field: "changed"}))
            with self.assertRaisesRegex(ValueError, "production builder"):
                builder.validate_tools(report, self.default, self.custom)

    def test_selected_46_and_swapped_tools_builder_report(self):
        report = self.report(self.selected, self.custom)
        with self.pins(), patch.object(builder, "SDCC46_BUILDER_SHA256", builder.sha(self.custom)), \
             patch.object(builder, "validate_inputs") as inputs:
            builder.validate_tools(report, self.selected, self.custom)
            inputs.assert_called_once_with(report, self.source, self.selected)
            for name in builder.SDCC46_PINS:
                path = self.selected / "bin" / name
                original = path.read_bytes()
                path.write_bytes(b"swapped")
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, "pinned SDCC 4.6"):
                    builder.validate_tools(self.report(self.selected, self.custom), self.selected, self.custom)
                path.write_bytes(original)
            self.custom.write_bytes(b"swapped builder")
            with self.assertRaisesRegex(ValueError, "pinned SDCC 4.6 builder"):
                builder.validate_tools(self.report(self.selected, self.custom), self.selected, self.custom)

    def test_selected_46_accepts_current_production_builder_bound_by_report(self):
        report = self.report(self.selected, self.production)
        with self.pins(), patch.object(builder, "validate_inputs") as inputs:
            self.assertEqual(builder.validate_tools(report, self.selected, self.production),
                             (self.selected, self.production))
            inputs.assert_called_once_with(report, self.source, self.selected)
            with self.assertRaisesRegex(ValueError, "builder_sha256"):
                builder.validate_tools(dict(report, builder_sha256="changed"),
                                       self.selected, self.production)

    def test_selected_report_mismatch_and_input_failure_propagate(self):
        report = self.report(self.selected, self.custom)
        with self.pins(), patch.object(builder, "SDCC46_BUILDER_SHA256", builder.sha(self.custom)):
            for field in report:
                with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                    builder.validate_tools(dict(report, **{field: "swapped"}), self.selected, self.custom)
            with patch.object(builder, "validate_inputs", side_effect=ValueError("stale source")):
                with self.assertRaisesRegex(ValueError, "stale source"):
                    builder.validate_tools(report, self.selected, self.custom)

    def test_path_outside_repository_rejected(self):
        with self.assertRaisesRegex(ValueError, "inside this repository"):
            builder.validate_tools({}, self.root.parent, self.custom)


class AssemblySnapshotTests(unittest.TestCase):
    def test_changed_host_during_packaging_stops_before_release_creation(self):
        """A second snapshot must never silently replace the reviewed one.

        The packer and independent firmware/source checks are mocked here;
        their own suites cover those contracts. The real review parser and
        assembler must reject the race before producing a release directory.
        """
        with tempfile.TemporaryDirectory(prefix="ak820-host-race-") as directory:
            root = Path(directory)
            source = root / "qmk-8051-ak820"
            build = source / ".build/reviewed"
            output = root / "releases/rc6"
            review = root / "review.md"
            names = (
                "qmk-8051-ak820/.build/reviewed/ajazz_ak820_vial.ihx",
                "qmk-8051-ak820/.build/reviewed/ajazz_ak820_vial.map",
                "qmk-8051-ak820/.build/reviewed/ajazz_ak820_vial.mem",
                "qmk-8051-ak820/util/build_ak820.py",
                "qmk-8051-ak820/util/ak820_dce.py",
                "qmk-8051-ak820/keyboards/ajazz/ak820/info.json",
                "qmk-8051-ak820/keyboards/ajazz/ak820/keymaps/vial/vial.json",
                "toolchains/sdcc-4.4.0/bin/sdcc",
                "toolchains/sdcc-4.4.0/bin/sdas8051",
                "local-oem/stock-full.bin",
                "local-oem/native-installed.bin",
            )
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(name.encode())
            report = {"keyboard": "ajazz/ak820", "keymap": "vial",
                      "build_id": builder.packer.BUILD_ID, "hardware_validated": False}
            for field, path in {
                "builder_sha256": source / "util/build_ak820.py",
                "dce_sha256": source / "util/ak820_dce.py",
                "compiler_sha256": root / "toolchains/sdcc-4.4.0/bin/sdcc",
                "assembler_sha256": root / "toolchains/sdcc-4.4.0/bin/sdas8051",
            }.items():
                report[field] = builder.sha(path)
            report_path = build / "build-report.json"
            report_path.write_text(json.dumps(report))
            reviewed = host_manifest(ROOT)
            changed = dict(reviewed)
            changed["AK820.sh"] = {"size": 1, "sha256": "edited-during-packaging"}
            record = {
                "format": "ak820-offline-review-2", "release": "rc6", "status": "passed",
                "hardware_validated": False, "host_files": reviewed,
                "build": {
                    "ihx_sha256": builder.sha(build / "ajazz_ak820_vial.ihx"),
                    "map_sha256": builder.sha(build / "ajazz_ak820_vial.map"),
                    "build_report_sha256": builder.sha(report_path),
                },
            }
            review.write_text("# Review\n\n```json\n" + json.dumps(record) + "\n```\n")

            def trial(*args):
                session = args[-1]
                session.mkdir()
                (session / "restore-native.bin").write_bytes(
                    args[4][builder.packer.APP_START:builder.packer.APP_END])
                return {"images": {"ak820-vial-trial.bin": {}, "restore-native.bin": {}},
                        "migration": {}}

            # This synthetic builder stands in for a reviewed historical build.
            # Profile approval itself has separate negative-control tests.
            with patch.object(ak820_profiles, "LEGACY_BUILDERS", {report["builder_sha256"]}), \
                 patch.object(builder, "ROOT", root), patch.object(builder, "SOURCE", source), \
                 patch.object(builder, "host_manifest", side_effect=[reviewed, changed]), \
                 patch.object(builder.diagnostic, "diagnostic_build"), \
                 patch.object(builder, "validate_build_artifact"), patch.object(builder, "validate_inputs"), \
                 patch.object(builder.packer, "validate_native"), \
                 patch.object(builder, "validate_permanent_payload", return_value={'trial': False}), \
                 patch.object(builder, "write_trial", side_effect=trial) as pack:
                with self.assertRaisesRegex(ValueError, "Host code changed while assembling"):
                    builder.assemble(build, review, output, root / "local-oem")
                pack.assert_called_once()
            self.assertFalse((root / "evidence/oem-backup/before-full-rom.bin").exists())
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
