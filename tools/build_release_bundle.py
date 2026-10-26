#!/usr/bin/env python3
"""Assemble offline-reviewed RC6 installer inputs from one checked build.

This command never opens USB, grants a hardware
operation, or writes the installer's separate approval file. The output must
be a new directory. OEM reference images are supplied locally for offline
packing validation and are never copied into the release. The installer uses
the user's local references and fresh device backup at runtime.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "qmk-8051-ak820"
SDCC46_PINS = {
    "sdcc": "3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891",
    "sdas8051": "2ae1a62eb7454d80787352fc398ffe87847b1bb048988908f2241d1a4a37d877",
    "sdar": "daf57e04dc0f0dc6d61f180d2fba9e9cccc36cf77fe88d1fa93ecefa6f808833",
    "packihx": "d2a8df1033e0fa7e4ab04a2d2c7936629665806fd668e0deff01f26b9760483c",
    "sdld": "0483ffac06f1c986c9f7a912296ecfd34288ba8b166e39ba6649b337042c82c0",
    "sdcpp": "7bde79bcb4fdb0207283eb1a7c91cd107dd4020aebc0171c566eb9cc018a2b49",
}
SDCC46_BUILDER_SHA256 = "4094ceba4c883b70355fb6fefa8a219cb18a0847bfbcb623c1e5833feaf276db"
sys.path.insert(0, str(SOURCE / "util"))

import ak820_diagnose as diagnostic
import pack_ak820 as packer
import ak820_release_safety as release_safety
from prepare_ak820_trial import write_trial
from ak820_build_inputs import validate_inputs
from ak820_profiles import require_release_qualification, validate_configuration
from ak820_release_manifest import MANIFEST_FORMAT, RELEASE, host_manifest, read_review_record


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_review(review: Path, ihx: Path, mapfile: Path, report: Path) -> dict:
    """Require a completed review explicitly bound to this immutable build.

    This is a consistency gate, not a digital signature or hardware approval.
    Human independence and the supporting evidence remain review obligations.
    """
    record = read_review_record(review.read_text(encoding="utf-8"))
    expected = {"ihx_sha256": sha(ihx), "map_sha256": sha(mapfile),
                "build_report_sha256": sha(report)}
    if record.get("build") != expected:
        raise ValueError("Independent review belongs to a different build")
    report_data = json.loads(report.read_text())
    if 'configuration' in report_data:
        safety_path = ROOT / release_safety.manifest_name(report_data['configuration'])
        if record.get('release_safety_manifest_sha256') != sha(safety_path):
            raise ValueError('Independent review belongs to different release safety evidence')
    if record.get("host_files") != host_manifest(ROOT):
        raise ValueError("Independent review belongs to different host code")
    return record['host_files']


def validate_build_artifact(report: dict, path: Path) -> None:
    name = path.relative_to(SOURCE).as_posix()
    records = [item for item in report["artifacts"] if item["path"] == name]
    if len(records) != 1 or not path.is_file():
        raise ValueError("Missing or ambiguous build artifact: " + name)
    if records[0]["sha256"] != sha(path) or records[0]["size"] != path.stat().st_size:
        raise ValueError("Build artifact differs from its report: " + name)


def validate_permanent_payload(ihx: Path, mapfile: Path, stock: Path, backup: bytes,
                               target_build_id: int) -> dict:
    data, symbols = packer.read_ihex(ihx), packer.read_symbols(mapfile)
    nvm, _ = packer.migrate(backup, data, symbols)
    nvm, transition = packer.migrate_vial_nvm(
        nvm, packer.BUILD_ID, target_build_id=target_build_id)
    image = packer.pack(data, symbols, stock.read_bytes(), nvm, False,
                        target_build_id=target_build_id)
    result = packer.verify_payload(image, target_build_id=target_build_id)
    if result['trial'] is not False:
        raise ValueError('Permanent packaging unexpectedly produced a trial')
    result['nvm_schema_transition'] = transition
    return result


def validate_tools(report: dict, toolchain: Path | None = None,
                   builder_source: Path | None = None) -> tuple[Path, Path]:
    default = (ROOT / "toolchains/sdcc-4.4.0").resolve()
    production_builder = (SOURCE / "util/build_ak820.py").resolve()
    toolchain = (toolchain or default).resolve()
    builder_source = (builder_source or production_builder).resolve()
    if (not toolchain.is_relative_to(ROOT.resolve()) or not toolchain.is_dir()
            or not builder_source.is_relative_to(ROOT.resolve()) or not builder_source.is_file()):
        raise ValueError("Selected toolchain and builder must exist inside this repository")
    if toolchain == default:
        if builder_source != production_builder:
            raise ValueError("Default SDCC 4.4 requires the production builder")
    else:
        # A supplied path is not permission to use an arbitrary compiler.
        for name, expected in SDCC46_PINS.items():
            path = toolchain / "bin" / name
            if not path.is_file() or sha(path) != expected:
                raise ValueError("Selected toolchain is not the pinned SDCC 4.6: " + name)
        # Preserve the already-reviewed experimental builder for old reports,
        # and allow the current production builder when its report and source
        # manifest bind the exact bytes used for this build.
        if builder_source != production_builder and sha(builder_source) != SDCC46_BUILDER_SHA256:
            raise ValueError("Selected builder is not the pinned SDCC 4.6 builder")
    for field, path in {
        "builder_sha256": builder_source,
        "dce_sha256": SOURCE / "util/ak820_dce.py",
        "compiler_sha256": toolchain / "bin/sdcc",
        "assembler_sha256": toolchain / "bin/sdas8051",
    }.items():
        if not path.is_file() or report.get(field) != sha(path):
            raise ValueError("Build tool differs from the reviewed toolchain: " + field)
    validate_inputs(report, SOURCE, toolchain)
    return toolchain, builder_source


def assemble(build: Path, review: Path, output: Path, oem_reference_dir: Path,
             toolchain: Path | None = None, builder_source: Path | None = None,
             expected_profile: str | None = None) -> dict:
    build, review, output = build.resolve(), review.resolve(), output.resolve()
    oem_reference_dir = oem_reference_dir.resolve()
    if output.exists():
        raise ValueError("Output already exists; select a fresh directory")
    if not build.is_relative_to(SOURCE) or not output.is_relative_to(ROOT):
        raise ValueError("Build and output must remain inside this repository")
    if not review.is_file():
        raise ValueError("An independent review file is required")
    report_path = build / "build-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    require_release_qualification(report)
    actual_profile = report.get('configuration', {}).get('profile')
    if expected_profile is not None and actual_profile != expected_profile:
        raise ValueError(f'Build profile mismatch: expected {expected_profile}, got {actual_profile}')
    if report.get("keyboard") != "ajazz/ak820" or report.get("keymap") != "vial":
        raise ValueError("Wrong build target")
    configuration = validate_configuration(report.get('configuration'))
    if (report.get("build_id") != configuration['nvm_schema']
            or report.get("hardware_validated") is not False):
        raise ValueError("Unexpected schema or hardware-validation claim")
    ihx, mapfile = build / "ajazz_ak820_vial.ihx", build / "ajazz_ak820_vial.map"
    diagnostic.diagnostic_build(ihx, mapfile, report_path)
    reviewed_host_files = validate_review(review, ihx, mapfile, report_path)
    for artifact in (ihx, mapfile, ihx.with_suffix(".mem")):
        validate_build_artifact(report, artifact)
    toolchain, builder_source = validate_tools(report, toolchain, builder_source)
    stock = oem_reference_dir / "stock-full.bin"
    native = oem_reference_dir / "native-installed.bin"
    if not stock.is_file() or not native.is_file():
        raise ValueError("Local OEM reference directory must contain stock-full.bin and native-installed.bin")
    backup = stock.read_bytes()
    packer.validate_native(backup, backup, native.read_bytes())
    # Exercise packing using owner-supplied local references. Neither reference
    # is a release input; the installer validates its own local references and
    # fresh device backup when run.
    with tempfile.TemporaryDirectory(prefix="ak820-rc6-pack-") as temporary:
        session = Path(temporary) / "trial"
        packed = write_trial(ihx, mapfile, stock, native, backup, session)
        if set(packed["images"]) != {"ak820-vial-trial.bin", "restore-native.bin"}:
            raise ValueError("Unexpected trial/recovery image set")
        permanent = validate_permanent_payload(
            ihx, mapfile, stock, backup, configuration['nvm_schema'])
        if (session / "restore-native.bin").read_bytes() != backup[packer.APP_START:packer.APP_END]:
            raise ValueError("Recovery image changed during migration")
        packing = {
            "level": "offline packing using local OEM references; not a live installation",
            "physical_usb_opened": False,
            "hardware_validated": False,
            "images": packed["images"],
            "permanent": permanent,
            "install_modes": ["permanent", "trial"],
            "migration": packed["migration"],
            "recovery_byte_equal": True,
            "backup_sha256": packer.digest(backup),
        }
    files = {
        "firmware/application.ihx": ihx,
        "firmware/application.map": mapfile,
        "firmware/application.mem": build / "ajazz_ak820_vial.mem",
        "reports/build-report.json": report_path,
        "reference/info.json": SOURCE / "keyboards/ajazz/ak820/info.json",
        "reference/vial.json": SOURCE / "keyboards/ajazz/ak820/keymaps/vial/vial.json",
        "reviews/independent-review.md": review,
        "reproduction/build_ak820.py": builder_source,
    }
    # Validate every input before creating any release output.
    for name, path in files.items():
        if not path.is_file():
            raise ValueError("Missing input for " + name + ": " + str(path))
    if host_manifest(ROOT) != reviewed_host_files:
        raise ValueError("Host code changed while assembling the release")
    output.mkdir(parents=True)
    for name, path in files.items():
        destination = output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
    write_json(output / "reports/packing-validation.json", packing)
    bound = sorted(set(files) | {'reports/packing-validation.json'})
    manifest = {
        "format": MANIFEST_FORMAT, "release": RELEASE,
        "host_files": reviewed_host_files,
        "hardware": "AJAZZ AK820 wired / VS11K28A / 320F:505B",
        "trial_only": False, "install_modes": ["permanent", "trial"], "hardware_validated": False,
        "offline_review": {"status": "passed", "report": "reviews/independent-review.md"},
        "files": {name: {"size": (output / name).stat().st_size, "sha256": sha(output / name)}
                  for name in bound},
    }
    write_json(output / "installer-release.json", manifest)
    return {"directory": str(output), "manifest_sha256": sha(output / "installer-release.json"),
            "trial_only": False, "install_modes": ["permanent", "trial"], "hardware_validated": False,
            "installer_approval_written": False, "packing": packing}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", required=True, type=Path,
                        help="Existing SDCC build directory, relative to the QMK source")
    parser.add_argument("--review", required=True, type=Path,
                        help="Completed independent review, relative to the repository root")
    parser.add_argument("--oem-reference-dir", required=True, type=Path,
                        help="Local directory containing stock-full.bin and native-installed.bin; never copied to output")
    parser.add_argument("--output", type=Path, default=Path("releases/rc6"),
                        help="New bundle directory, relative to the repository root")
    parser.add_argument("--toolchain", type=Path, default=Path("toolchains/sdcc-4.4.0"),
                        help="Existing pinned toolchain directory, relative to the repository root")
    parser.add_argument("--builder-source", type=Path,
                        default=Path("qmk-8051-ak820/util/build_ak820.py"),
                        help="Actual builder source matching the report, relative to the repository root")
    parser.add_argument("--expected-profile", help="Require this exact profile in the linked build report")
    args = parser.parse_args()
    print(json.dumps(assemble(SOURCE / args.build_dir, ROOT / args.review, ROOT / args.output,
                             args.oem_reference_dir, ROOT / args.toolchain, ROOT / args.builder_source,
                             args.expected_profile),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
