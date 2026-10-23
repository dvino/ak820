#!/usr/bin/env python3
"""Check or restore the pinned LUFA source into the QMK source tree.

The default command is offline and read-only. Installing requires an explicit
archive path or --fetch. Archive contents are hash checked and unpacked without
following links or writing outside the destination.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tarfile
import tempfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCK = ROOT / "qmk-8051-ak820" / "dependencies" / "lufa.json"
MAX_ARCHIVE_BYTES = 100 * 1024 * 1024
MAX_EXPANDED_BYTES = 256 * 1024 * 1024
MAX_MEMBERS = 20000


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_lock(path: Path) -> dict:
    lock = json.loads(path.read_text(encoding="utf-8"))
    if lock.get("format") != "ak820-external-dependency-1" or lock.get("name") != "lufa":
        raise ValueError("Unsupported LUFA dependency lock")
    for key in ("repository", "revision", "download_url", "archive_root", "destination"):
        if not isinstance(lock.get(key), str) or not lock[key]:
            raise ValueError("Invalid LUFA lock field: " + key)
    for key in ("archive_sha256",):
        value = lock.get(key)
        if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
            raise ValueError("Invalid LUFA lock hash: " + key)
    files = lock.get("required_files")
    if not isinstance(files, dict) or not files:
        raise ValueError("LUFA lock has no required files")
    for name, digest in files.items():
        safe_member_path(name)
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("Invalid required-file hash: " + name)
    if lock.get("license_path") not in files:
        raise ValueError("LUFA license must be included in required_files")
    safe_member_path(lock["archive_root"])
    safe_member_path(lock["destination"])
    return lock


def safe_member_path(name: str) -> PurePosixPath:
    if not isinstance(name, str) or not name or "\\" in name or "\x00" in name:
        raise ValueError("Unsafe archive path")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("Unsafe archive path: " + name)
    if any(":" in part for part in path.parts):
        raise ValueError("Unsafe archive path: " + name)
    return path


def _archive_members(archive: tarfile.TarFile, lock: dict) -> tuple[str, dict[str, tarfile.TarInfo]]:
    members = archive.getmembers()
    if len(members) > MAX_MEMBERS:
        raise ValueError("LUFA archive has too many entries")
    root = lock["archive_root"]
    found: dict[str, tarfile.TarInfo] = {}
    expanded = 0
    for member in members:
        path = safe_member_path(member.name.rstrip("/"))
        if not path.parts or path.parts[0] != root:
            raise ValueError("LUFA archive has an unexpected top-level path")
        if len(path.parts) == 1:
            if not member.isdir():
                raise ValueError("LUFA archive root is not a directory")
            continue
        relative = PurePosixPath(*path.parts[1:]).as_posix()
        if relative in found:
            raise ValueError("Duplicate LUFA archive path: " + relative)
        if member.isdir():
            if member.size != 0:
                raise ValueError("Invalid LUFA directory entry")
        elif member.isfile():
            if member.size < 0:
                raise ValueError("Invalid LUFA file size")
            expanded += member.size
            if expanded > MAX_EXPANDED_BYTES:
                raise ValueError("LUFA archive expands beyond the size limit")
        else:
            raise ValueError("LUFA archive contains a link or special file: " + member.name)
        found[relative] = member
    for required, expected in lock["required_files"].items():
        member = found.get(required)
        if member is None or not member.isfile():
            raise ValueError("Pinned LUFA archive is missing: " + required)
        stream = archive.extractfile(member)
        if stream is None:
            raise ValueError("Cannot read pinned LUFA file: " + required)
        with stream:
            digest = hashlib.sha256()
            remaining = member.size
            while remaining:
                block = stream.read(min(1024 * 1024, remaining))
                if not block:
                    raise ValueError("Truncated LUFA archive member: " + required)
                digest.update(block)
                remaining -= len(block)
        if digest.hexdigest() != expected:
            raise ValueError("Pinned LUFA file hash mismatch: " + required)
    return root, found


def verify_archive(path: Path, lock: dict) -> None:
    if path.stat().st_size > MAX_ARCHIVE_BYTES:
        raise ValueError("LUFA archive exceeds the compressed size limit")
    if sha256_file(path) != lock["archive_sha256"]:
        raise ValueError("LUFA archive SHA256 differs from the pinned archive")
    try:
        with tarfile.open(path, mode="r:gz") as archive:
            _archive_members(archive, lock)
    except (tarfile.TarError, OSError) as exc:
        raise ValueError("Cannot read pinned LUFA tar.gz archive") from exc


def check_existing(destination: Path, lock: dict) -> None:
    for name, expected in lock["required_files"].items():
        path = destination.joinpath(*safe_member_path(name).parts)
        if not path.is_file():
            raise ValueError("Required LUFA file is missing: " + str(path))
        if sha256_file(path) != expected:
            raise ValueError("Required LUFA file hash mismatch: " + name)


def _tree_hashes(root: Path) -> dict[str, str]:
    result = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("LUFA destination contains a symlink: " + str(path))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = sha256_file(path)
        elif not path.is_dir():
            raise ValueError("LUFA destination contains a special file: " + str(path))
    return result


def _tree_difference(left: dict[str, str], right: dict[str, str]) -> list[str]:
    result = []
    for name in sorted(left.keys() | right.keys()):
        if name not in left:
            result.append("archive-only:" + name)
        elif name not in right:
            result.append("local-only:" + name)
        elif left[name] != right[name]:
            result.append("changed:" + name)
    return result


def install_archive(path: Path, destination: Path, lock: dict) -> bool:
    """Install a pinned complete archive; return False when already identical."""
    verify_archive(path, lock)
    if destination.is_symlink():
        raise ValueError("LUFA destination is a symlink; refusing to follow it")
    destination = destination.parent.resolve() / destination.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(path, mode="r:gz") as archive:
        root, members = _archive_members(archive, lock)
        staging = Path(tempfile.mkdtemp(prefix=".lufa-install-", dir=destination.parent))
        try:
            extracted = staging / root
            for relative, member in members.items():
                target = extracted.joinpath(*PurePosixPath(relative).parts)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError("Cannot extract LUFA file: " + relative)
                written = 0
                with stream, target.open("xb") as output:
                    while block := stream.read(1024 * 1024):
                        written += len(block)
                        if written > member.size:
                            raise ValueError("LUFA member exceeds declared size: " + relative)
                        output.write(block)
                if written != member.size:
                    raise ValueError("Truncated LUFA file: " + relative)
            check_existing(extracted, lock)
            if destination.exists():
                if not destination.is_dir():
                    raise ValueError("LUFA destination exists and is not a directory")
                differences = _tree_difference(_tree_hashes(destination), _tree_hashes(extracted))
                if differences:
                    preview = ", ".join(differences[:30])
                    more = " ..." if len(differences) > 30 else ""
                    raise ValueError("Existing LUFA directory differs; refusing to overwrite it. "
                                     + str(len(differences)) + " differing paths: " + preview + more)
                return False
            os.replace(extracted, destination)
            return True
        finally:
            shutil.rmtree(staging, ignore_errors=True)


def fetch_archive(url: str, expected_sha256: str, temporary_directory: Path) -> Path:
    """Fetch only a bounded archive; hash verification is performed by caller."""
    path = temporary_directory / "lufa.tar.gz"
    digest = hashlib.sha256()
    total = 0
    with urlopen(url, timeout=60) as response, path.open("xb") as output:
        while block := response.read(1024 * 1024):
            total += len(block)
            if total > MAX_ARCHIVE_BYTES:
                raise ValueError("LUFA download exceeds the compressed size limit")
            digest.update(block)
            output.write(block)
    if digest.hexdigest() != expected_sha256:
        path.unlink(missing_ok=True)
        raise ValueError("Downloaded LUFA archive SHA256 differs from the pinned archive")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--fetch", action="store_true", help="download and install the pinned archive")
    action.add_argument("--archive", type=Path, help="install from this local pinned archive")
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--target", type=Path, help="LUFA directory (default: qmk-8051-ak820/lib/lufa)")
    args = parser.parse_args(argv)
    try:
        lock = load_lock(args.lock)
        target = args.target or ROOT / "qmk-8051-ak820" / lock["destination"]
        if target.is_symlink():
            raise ValueError("LUFA destination is a symlink; refusing to follow it")
        if args.target is None:
            resolved_target = target.parent.resolve() / target.name
            if not resolved_target.is_relative_to(ROOT.resolve()):
                raise ValueError("LUFA destination escapes the project root")
            target = resolved_target
        if not args.fetch and args.archive is None:
            check_existing(target, lock)
            print("Offline check passed: locked LUFA headers and license match.")
            return 0
        if args.archive is not None:
            archive_path = args.archive.resolve()
            installed = install_archive(archive_path, target, lock)
        else:
            with tempfile.TemporaryDirectory(prefix="ak820-lufa-fetch-") as temporary:
                archive_path = fetch_archive(lock["download_url"], lock["archive_sha256"], Path(temporary))
                installed = install_archive(archive_path, target, lock)
        print("Pinned LUFA archive installed." if installed else "Pinned LUFA archive already matches target.")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
