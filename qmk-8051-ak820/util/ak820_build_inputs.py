"""Hash the actual C include closure and the pinned build inputs.

SDCC assembly comments omit headers that only define types and constants.
Use preprocessor dependency files instead, including SDCC system headers.
Paths stay relative to the source/toolchain roots so a copied checkout can
validate the same evidence. This module never accesses a USB device.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import shlex

FORMAT = "ak820-build-inputs-2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dependency_paths(depfile: Path, source: Path) -> set[Path]:
    """Read one compiler-produced Make rule, with escaped spaces/continuations."""
    text = depfile.read_text(encoding="utf-8").replace("\\\n", " ")
    target, separator, prerequisites = text.partition(":")
    if not separator or not target.strip():
        raise ValueError("Malformed dependency file: " + str(depfile))
    # We request -MD without -MP, hence there must be exactly one rule.
    if "\n" in prerequisites.strip():
        raise ValueError("Unexpected dependency rules: " + str(depfile))
    names = shlex.split(prerequisites.replace("$$", "$"), comments=False)
    if not names:
        raise ValueError("Empty dependency file: " + str(depfile))
    paths = {(source / name).resolve() for name in names}
    for path in paths:
        if not path.is_file():
            raise ValueError("Missing compiler dependency: " + str(path))
    return paths


def input_snapshot(source: Path, toolchain: Path) -> dict[Path, str]:
    """Detect a relevant source edit occurring while the compiler is running.

The initial snapshot is deliberately wider than the final include closure;
only used files are compared and recorded in the report. Generated build
files are compiled and hashed in their fresh, private build directory.
"""
    result = {}
    suffixes = {".c", ".h", ".mk", ".py", ".json", ".hjson", ".txt", ".inc"}
    ignored = {".git", ".build", ".venv", "venv", "__pycache__"}
    for directory, subdirs, files in os.walk(source):
        subdirs[:] = [name for name in subdirs if name not in ignored]
        for name in files:
            path = Path(directory) / name
            if path.suffix in suffixes or name == "Makefile":
                result[path.resolve()] = digest(path)
    for path in (toolchain / "share/sdcc/include").rglob("*.h"):
        result[path.resolve()] = digest(path)
    for path in (toolchain / "share/sdcc/lib/large").glob("*.lib"):
        result[path.resolve()] = digest(path)
    for name in ("sdcc", "sdcpp", "sdas8051", "sdld"):
        path = toolchain / "bin" / name
        result[path.resolve()] = digest(path)
    return result


def collect_inputs(source: Path, toolchain: Path, build: Path, objects: list[str],
                   before: dict[Path, str]) -> tuple[list[dict], list[Path]]:
    source, toolchain, build = source.resolve(), toolchain.resolve(), build.resolve()
    paths: set[Path] = set()
    evidence: list[Path] = []
    for name in objects:
        depfile = (source / name).with_suffix(".d")
        if not depfile.is_file():
            raise ValueError("Missing compiler dependency file: " + str(depfile))
        paths.update(dependency_paths(depfile, source))
        evidence.append(depfile)
    makefile_lists = list(build.glob("obj_*/makefiles.txt"))
    if len(makefile_lists) != 1:
        raise ValueError("Missing or ambiguous Make input manifest")
    makefiles = makefile_lists[0]
    if not makefiles.is_file():
        raise ValueError("Missing Make input manifest")
    paths.update((source / name).resolve() for name in makefiles.read_text().splitlines())
    for path in (source / "keyboards/ajazz/ak820").rglob("*"):
        if path.is_file() and path.suffix in {".c", ".h", ".mk", ".json"}:
            paths.add(path.resolve())
    evidence.append(makefiles)
    # Include generator implementation and data schemas as well as the C
    # dependencies. Conservative extra inputs are preferable to missing one.
    for folder, pattern in (("lib/python/qmk", "*.py"), ("data", "*.hjson"), ("data", "*.json")):
        paths.update(path.resolve() for path in (source / folder).rglob(pattern))
    for name in ("requirements-ak820-build.txt", "util/build_id.py",
                 "util/vial_generate_definition.py", "util/ak820_dce.py",
                 "util/build_ak820.py", "util/ak820_build_inputs.py", "util/ak820_outline_audit.py"):
        paths.add((source / name).resolve())
    for name in ("sdcc", "sdcpp", "sdas8051", "sdld"):
        paths.add((toolchain / "bin" / name).resolve())
    paths.update(path.resolve() for path in (toolchain / "share/sdcc/lib/large").glob("*.lib"))
    records = []
    for path in sorted(paths):
        current = digest(path)
        if not path.is_relative_to(build) and before.get(path) != current:
            raise ValueError("Build input changed during compilation: " + str(path))
        if path.is_relative_to(source):
            origin, relative = "source", path.relative_to(source)
        elif path.is_relative_to(toolchain):
            origin, relative = "toolchain", path.relative_to(toolchain)
        else:
            raise ValueError("Build input outside the pinned roots: " + str(path))
        records.append({"path": relative.as_posix(), "origin": origin, "sha256": current})
    return records, evidence


def validate_inputs(report: dict, source: Path, toolchain: Path) -> None:
    if report.get("source_manifest_format") != FORMAT or not report.get("sources"):
        raise ValueError("Build has no complete compiler dependency evidence")
    seen = set()
    roots = {"source": source.resolve(), "toolchain": toolchain.resolve()}
    for item in report["sources"]:
        origin, name = item.get("origin"), item.get("path")
        if origin not in roots or not isinstance(name, str) or not name:
            raise ValueError("Invalid build input record")
        # Older Windows reports used backslashes. Interpret those separators
        # on every host, without accepting Windows drive or rooted paths.
        portable = name.replace("\\", "/")
        if PureWindowsPath(name).drive or PureWindowsPath(name).root or PurePosixPath(portable).is_absolute():
            raise ValueError("Build input path escapes its root")
        key = origin, portable
        if key in seen:
            raise ValueError("Duplicate build input record")
        seen.add(key)
        root = roots[origin]
        path = (root / portable).resolve()
        if Path(name).is_absolute() or not path.is_relative_to(root):
            raise ValueError("Build input path escapes its root")
        if not path.is_file() or digest(path) != item.get("sha256"):
            raise ValueError("Source differs from the linked build: " + name)
