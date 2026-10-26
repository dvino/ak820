#!/usr/bin/env python3
"""Read-only verification runner for final AK820 beta.3 release assets.

This intentionally does not build assets. It checks the three published archives,
their detached checksums and the Python installer’s offline verify path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile

PROFILES = ("main", "game", "mmo", "typing", "code", "pointer", "onehand",
            "creative", "shortcuts", "multios")
PACKAGES = ("AK820-Windows.zip", "AK820-Linux-x86_64.tar.gz",
            "AK820-Beta3-Catalog.zip")
PY_PREFIX = "AK820-Python/"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(name: str) -> str:
    if (not name or "\\" in name or name.startswith("/") or
            re.match(r"^[A-Za-z]:", name)):
        raise ValueError(f"unsafe archive path: {name!r}")
    parts = name.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError(f"unsafe archive path: {name!r}")
    if str(PurePosixPath(name)) != name:
        raise ValueError(f"non-canonical archive path: {name!r}")
    return name


def zip_members(path: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            name = info.filename
            if info.is_dir():
                raise ValueError(f"directory entry is not expected: {name!r}")
            safe_name(name)
            if name in result:
                raise ValueError(f"duplicate ZIP member: {name}")
            mode = (info.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode):
                raise ValueError(f"symlink ZIP member: {name}")
            if mode and not stat.S_ISREG(mode):
                raise ValueError(f"non-regular ZIP member: {name}")
            result[name] = archive.read(info)
    return result


def tar_members(path: Path) -> dict[str, tuple[bytes, int]]:
    result: dict[str, tuple[bytes, int]] = {}
    with tarfile.open(path, "r:gz") as archive:
        for info in archive.getmembers():
            name = safe_name(info.name)
            if name in result:
                raise ValueError(f"duplicate tar member: {name}")
            if not info.isfile():
                raise ValueError(f"non-regular tar member: {name}")
            stream = archive.extractfile(info)
            if stream is None:
                raise ValueError(f"unreadable tar member: {name}")
            result[name] = (stream.read(), info.mode)
    return result


def check_checksum(assets: Path, name: str) -> dict:
    archive = assets / name
    sidecar = assets / (name + ".sha256")
    if archive.is_symlink() or sidecar.is_symlink() or not archive.is_file() or not sidecar.is_file():
        raise ValueError(f"missing or unsafe package/checksum: {name}")
    raw = sidecar.read_text(encoding="ascii").strip()
    match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw)
    if not match or match.group(2) != name:
        raise ValueError(f"malformed checksum sidecar: {name}.sha256")
    actual = sha256_file(archive)
    if actual != match.group(1):
        raise ValueError(f"checksum mismatch: {name}")
    return {"file": name, "sha256": actual, "size_bytes": archive.stat().st_size,
            "checksum_file_sha256": sha256_file(sidecar)}


def check_payload_surface(files: dict[str, bytes], label: str) -> None:
    lower_names = {name.lower() for name in files}
    denied_exact = {
        "tools/installer/gui.py", "tools/installer/requirements-build-windows.txt",
        "tools/installer/requirements-build-linux.txt",
        "tools/build_windows_installer.py", "tools/build_linux_installer.py",
    }
    if denied_exact & lower_names:
        raise ValueError(f"GUI source/build requirement included in {label}: " +
                         ", ".join(sorted(denied_exact & lower_names)))
    denied_suffixes = (".exe", ".dll", ".so", ".dylib", ".pyd", ".pyc")
    forbidden = []
    for name in files:
        low = name.lower()
        base = low.rsplit("/", 1)[-1]
        if low.endswith(denied_suffixes) or base in {
                "stock-full.bin", "oem-backup.bin", "before-full-rom.bin",
                "native-installed.bin", "saved-nvm.bin", "restore-native.bin"}:
            forbidden.append(name)
        if "pyinstaller" in low or "runtime" in low and low.endswith((".zip", ".7z")):
            forbidden.append(name)
        if "oem-backup" in low or "private-rom" in low or "stock-rom" in low:
            forbidden.append(name)
    if forbidden:
        raise ValueError(f"forbidden GUI runtime/binary/private input in {label}: " +
                         ", ".join(sorted(set(forbidden))))


def atomic_report(path: Path, report: dict) -> None:
    path = path.absolute()
    if path.exists() or path.is_symlink():
        raise ValueError(f"report path must be fresh: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp-{os.getpid()}")
    try:
        with tmp.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def verify(assets_arg: Path) -> dict:
    assets = assets_arg.absolute()
    if assets.is_symlink() or not assets.is_dir():
        raise ValueError("assets must be an existing ordinary directory")
    assets = assets.resolve(strict=True)
    package_records = [check_checksum(assets, name) for name in PACKAGES]

    windows = zip_members(assets / PACKAGES[0])
    linux_raw = tar_members(assets / PACKAGES[1])
    catalog = zip_members(assets / PACKAGES[2])
    check_payload_surface(catalog, "catalog ZIP")

    windows_python = {name[len(PY_PREFIX):]: data for name, data in windows.items()
                      if name.startswith(PY_PREFIX)}
    if len(windows_python) != len(windows):
        raise ValueError("Windows archive has members outside AK820-Python/")
    linux_python = {name[len(PY_PREFIX):]: data for name, (data, _mode) in linux_raw.items()
                    if name.startswith(PY_PREFIX)}
    if len(linux_python) != len(linux_raw):
        raise ValueError("Linux archive has members outside AK820-Python/")
    if windows_python != linux_python:
        missing_linux = sorted(windows_python.keys() - linux_python.keys())
        missing_windows = sorted(linux_python.keys() - windows_python.keys())
        changed = sorted(k for k in windows_python.keys() & linux_python.keys()
                         if windows_python[k] != linux_python[k])
        raise ValueError(f"Windows/Linux payload mismatch; Linux missing={missing_linux}, "
                         f"Windows missing={missing_windows}, changed={changed}")
    check_payload_surface(windows_python, "Python packages")
    required = {"tools/installer/ak820.py", "AK820.sh"}
    for profile in PROFILES:
        required.add(f"releases/beta3/{profile}/installer-release.json")
        required.add(f"releases/beta3/{profile}/approved-release.json")
    missing = sorted(required - windows_python.keys())
    if missing:
        raise ValueError("Python packages omit required installer/profile files: " + ", ".join(missing))
    if not (linux_raw[PY_PREFIX + "AK820.sh"][1] & 0o111):
        raise ValueError("Linux AK820.sh is not executable")

    commands = []
    with tempfile.TemporaryDirectory(prefix="ak820-beta3-verify-") as td:
        work = Path(td)
        for name in windows:
            target = work.joinpath(*name.split("/"))
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(windows[name])
        package_root = work / "AK820-Python"
        installer = package_root / "tools" / "installer" / "ak820.py"
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env.pop("PYTHONHOME", None)
        cmd_list = [("help", [sys.executable, str(installer), "--help"])]
        cmd_list.extend((f"verify:{profile}", [sys.executable, str(installer),
                                               "--profile", profile, "verify"])
                        for profile in PROFILES)
        for label, command in cmd_list:
            proc = subprocess.run(command, cwd=work, env=env, stdin=subprocess.DEVNULL,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  text=True, timeout=120, check=False)
            commands.append({"label": label, "argv": command, "exit_code": proc.returncode,
                             "output": proc.stdout[-12000:]})
            if proc.returncode != 0:
                raise ValueError(f"offline installer command failed ({label}), exit {proc.returncode}; "
                                 f"output: {proc.stdout[-12000:]}")

    return {
        "status": "PASS", "assets_dir": str(assets), "packages": package_records,
        "payload": {"file_count": len(windows_python),
                    "uncompressed_bytes": sum(len(data) for data in windows_python.values()),
                    "windows_archive_file_count": len(windows),
                    "linux_archive_file_count": len(linux_raw),
                    "catalog_archive_file_count": len(catalog),
                    "windows_payload_sha256": hashlib.sha256(b"".join(
                        name.encode() + b"\0" + windows_python[name] for name in sorted(windows_python))).hexdigest(),
                    "linux_payload_sha256": hashlib.sha256(b"".join(
                        name.encode() + b"\0" + linux_python[name] for name in sorted(linux_python))).hexdigest()},
        "profiles_verified": list(PROFILES), "commands": commands,
        "physical_device_commands": 0, "hardware_validated": False,
        "execution_scope": "offline --help and verify only; no setup, diagnose, device, or write command",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = verify(args.assets)
    except Exception as exc:
        report = {"status": "FAIL", "assets_dir": str(args.assets.absolute()),
                  "error": f"{type(exc).__name__}: {exc}"}
        try:
            atomic_report(args.output, report)
        except Exception as report_exc:
            print(f"verification failed: {report['error']}; report failed: {report_exc}", file=sys.stderr)
            return 2
        print(report["error"], file=sys.stderr)
        return 1
    try:
        atomic_report(args.output, report)
    except Exception as exc:
        print(f"verification passed but report could not be written: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"status": report["status"], "output": str(args.output.absolute())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
