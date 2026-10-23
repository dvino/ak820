"""Install the pinned official SDCC 4.6.0 Linux archive as a local dependency.

On Windows this runs the extraction and version check in the configured Ubuntu
WSL distribution. Pass --archive to use an already downloaded archive without
network access. The toolchain is installed under the repository's ignored
toolchains/ directory; it never changes the system compiler or PATH.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import posixpath
import shutil
import ssl
import subprocess
import tarfile
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
VERSION = "4.6.0"
ARCHIVE_NAME = "sdcc-4.6.0-amd64-unknown-linux2.5.tar.bz2"
ARCHIVE_ROOT = "sdcc-4.6.0"
ARCHIVE_URLS = (
    "https://sourceforge.net/projects/sdcc/files/sdcc-linux-amd64/4.6.0/"
    + ARCHIVE_NAME + "/download",
    "https://pilotfiber.dl.sourceforge.net/project/sdcc/sdcc-linux-amd64/4.6.0/"
    + ARCHIVE_NAME,
    "https://downloads.sourceforge.net/project/sdcc/sdcc-linux-amd64/4.6.0/"
    + ARCHIVE_NAME,
)
ARCHIVE_URL = (
    "https://downloads.sourceforge.net/project/sdcc/sdcc-linux-amd64/4.6.0/"
    + ARCHIVE_NAME
)
ARCHIVE_SIZE = 23_853_152
ARCHIVE_SHA256 = "f6b929c62ed3082a26087885e0f1f9bf41878602ef1f57e40b11b4a01bf4f366"
EXECUTABLE_PINS = {
    "sdcc": "3387975f6c295af8913065804c2f7f8d54a668849237ba98b119ad9b38d27891",
    "sdas8051": "2ae1a62eb7454d80787352fc398ffe87847b1bb048988908f2241d1a4a37d877",
    "sdar": "daf57e04dc0f0dc6d61f180d2fba9e9cccc36cf77fe88d1fa93ecefa6f808833",
    "packihx": "d2a8df1033e0fa7e4ab04a2d2c7936629665806fd668e0deff01f26b9760483c",
    "sdld": "0483ffac06f1c986c9f7a912296ecfd34288ba8b166e39ba6649b337042c82c0",
    "sdcpp": "7bde79bcb4fdb0207283eb1a7c91cd107dd4020aebc0171c566eb9cc018a2b49",
}
TARGET = ROOT / "toolchains" / "sdcc-4.6.0"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def trusted_source(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    host = (parsed.hostname or "").lower()
    return parsed.scheme == "https" and (host == "sourceforge.net" or host.endswith(".sourceforge.net"))


class SourceForgeRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, new_url):
        if not trusted_source(new_url):
            raise ValueError("Redirect outside HTTPS SourceForge download infrastructure")
        return super().redirect_request(request, file, code, message, headers, new_url)


def verify_archive(path: Path, *, expected_sha: str = ARCHIVE_SHA256,
                   expected_size: int = ARCHIVE_SIZE) -> dict:
    if not path.is_file():
        raise ValueError("Archive file does not exist")
    size = path.stat().st_size
    if size != expected_size:
        raise ValueError(f"Archive size mismatch: {size} != {expected_size}")
    digest = sha256(path)
    if digest != expected_sha:
        raise ValueError("Archive SHA256 mismatch")
    return {"bytes": size, "sha256": digest}


def download_archive(path: Path) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(
        SourceForgeRedirects(),
        urllib.request.HTTPSHandler(context=ssl.create_default_context()),
    )
    errors = []
    for url in ARCHIVE_URLS:
        digest = hashlib.sha256()
        size = 0
        try:
            with opener.open(url, timeout=60) as response:
                if not trusted_source(response.geturl()):
                    raise ValueError("Untrusted final download URL")
                with path.open("wb") as output:
                    for chunk in iter(lambda: response.read(1024 * 1024), b""):
                        size += len(chunk)
                        if size > ARCHIVE_SIZE:
                            raise ValueError("Archive exceeds pinned size")
                        output.write(chunk)
                        digest.update(chunk)
            if size != ARCHIVE_SIZE or digest.hexdigest() != ARCHIVE_SHA256:
                raise ValueError("Downloaded archive does not match pinned size and SHA256")
            return {"bytes": size, "sha256": digest.hexdigest(), "url": url}
        except (OSError, ValueError) as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
            path.unlink(missing_ok=True)
    raise RuntimeError("All official SourceForge routes failed: " + "; ".join(errors))


def validate_members(archive: tarfile.TarFile) -> tuple[list[tuple[tarfile.TarInfo, PurePosixPath, str | None]], int]:
    members = archive.getmembers()
    if len(members) > 100_000:
        raise ValueError("Too many archive members")
    checked = []
    names: dict[str, tarfile.TarInfo] = {}
    links: set[str] = set()
    total = 0
    for item in members:
        path = PurePosixPath(item.name)
        if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != ARCHIVE_ROOT:
            raise ValueError("Archive member escapes expected SDCC root: " + item.name)
        relative = PurePosixPath(*path.parts[1:])
        if str(relative) == ".":
            if not item.isdir():
                raise ValueError("Archive root must be a directory")
            continue
        key = str(relative)
        if key in names:
            raise ValueError("Duplicate archive member: " + key)
        if not (item.isfile() or item.isdir() or item.issym() or item.islnk()):
            raise ValueError("Special archive member rejected")
        target = None
        if item.issym():
            raw = PurePosixPath(item.linkname)
            if raw.is_absolute():
                raise ValueError("Absolute symlink rejected")
            target = posixpath.normpath(str(relative.parent / raw))
        elif item.islnk():
            raw = PurePosixPath(item.linkname)
            if raw.is_absolute() or ".." in raw.parts or not raw.parts or raw.parts[0] != ARCHIVE_ROOT:
                raise ValueError("Unsafe hardlink target")
            target = str(PurePosixPath(*raw.parts[1:]))
        if target is not None:
            if target in (".", "..") or target.startswith("../"):
                raise ValueError("Link escapes archive root")
            links.add(key)
        if item.size < 0 or item.size > 128 * 1024 * 1024:
            raise ValueError("Invalid archive member size")
        total += item.size
        if total > 1024 * 1024 * 1024:
            raise ValueError("Uncompressed archive limit exceeded")
        names[key] = item
        checked.append((item, relative, target))
    for item, relative, target in checked:
        for parent in relative.parents:
            if str(parent) in links:
                raise ValueError("Archive member would traverse a link")
            parent_item = names.get(str(parent))
            if parent_item is not None and not parent_item.isdir():
                raise ValueError("Archive member parent is not a directory")
        if target is not None:
            target_item = names.get(target)
            if target_item is None or target in links or not (target_item.isfile() or target_item.isdir()):
                raise ValueError("Link target must be an existing regular member")
    return checked, total


def install_archive(archive_path: Path, target: Path, *, expected_sha: str = ARCHIVE_SHA256,
                    expected_size: int = ARCHIVE_SIZE,
                    executable_pins: dict[str, str] = EXECUTABLE_PINS) -> dict:
    archive_path, target = archive_path.resolve(), target.resolve()
    if not target.is_relative_to(ROOT.resolve()):
        raise ValueError("Toolchain target must remain inside this repository")
    archive_record = verify_archive(archive_path, expected_sha=expected_sha, expected_size=expected_size)
    if target.is_symlink():
        raise ValueError("Toolchain target may not be a symlink")
    receipt_path = target / "ak820-toolchain-receipt.json"
    if target.exists():
        if not receipt_path.is_file():
            raise ValueError("Existing toolchain has no installer receipt; refusing to overwrite")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt.get("archive_sha256") != expected_sha:
            raise ValueError("Existing toolchain receipt belongs to a different archive")
        for name, expected in executable_pins.items():
            binary = target / "bin" / name
            if not binary.is_file() or sha256(binary) != expected:
                raise ValueError("Existing toolchain executable differs from pin: " + name)
        return {"installed_directory": str(target), "already_installed": True, "receipt": receipt}

    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)
    if parent.resolve() != parent or target.exists():
        raise ValueError("Toolchain parent redirects or target appeared during setup")
    staging = parent / f".{target.name}.staging-{time.time_ns()}"
    staging.mkdir()
    try:
        with tarfile.open(archive_path, "r:bz2") as archive:
            checked, total = validate_members(archive)
            for item, relative, _ in checked:
                if item.issym() or item.islnk():
                    continue
                destination = staging / str(relative)
                if not destination.resolve().is_relative_to(staging.resolve()):
                    raise ValueError("Resolved extraction path escaped staging")
                if item.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(item) as source, destination.open("xb") as output:
                        shutil.copyfileobj(source, output)
                    destination.chmod(0o755 if item.mode & 0o111 else 0o644)
            for item, relative, _ in checked:
                if not (item.issym() or item.islnk()):
                    continue
                destination = staging / str(relative)
                destination.parent.mkdir(parents=True, exist_ok=True)
                if item.issym():
                    destination.symlink_to(item.linkname)
                else:
                    link_target = str(PurePosixPath(*PurePosixPath(item.linkname).parts[1:]))
                    os.link(staging / link_target, destination)

        binary_hashes = {}
        for name, expected in executable_pins.items():
            binary = staging / "bin" / name
            if not binary.is_file():
                raise ValueError("Archive is missing pinned executable: " + name)
            actual = sha256(binary)
            if actual != expected:
                raise ValueError("Archive executable SHA256 mismatch: " + name)
            binary_hashes[name] = actual
        compiler = subprocess.run([str(staging / "bin" / "sdcc"), "--version"],
                                  capture_output=True, text=True, timeout=30)
        if compiler.returncode != 0 or "4.6.0" not in compiler.stdout:
            raise ValueError("Extracted compiler did not report SDCC 4.6.0")
        receipt = {
            "archive_name": ARCHIVE_NAME,
            "archive_sha256": archive_record["sha256"],
            "archive_bytes": archive_record["bytes"],
            "archive_members": len(checked),
            "uncompressed_bytes": total,
            "executable_sha256": binary_hashes,
            "version_output": compiler.stdout.strip(),
            "path_validation_before_extraction": True,
        }
        (staging / "ak820-toolchain-receipt.json").write_text(
            json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        staging.rename(target)
        return {"installed_directory": str(target), "already_installed": False, "receipt": receipt}
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def mounted(path: Path) -> str:
    path = path.resolve()
    return "/mnt/" + path.drive[0].lower() + "/" + path.as_posix()[3:]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path,
                        help="Use a local archive (offline); it must match the pinned size and SHA256")
    parser.add_argument("--target", type=Path, default=TARGET)
    parser.add_argument("--linux-stage", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.linux_stage:
        print(json.dumps(install_archive(args.archive, args.target), indent=2))
        return

    archive = args.archive
    if archive is None:
        archive = ROOT / ".build" / "toolchain-cache" / ARCHIVE_NAME
        if not archive.is_file():
            record = download_archive(archive)
        else:
            record = verify_archive(archive)
    else:
        record = verify_archive(archive)

    if platform.system() == "Windows":
        command = ["wsl", "-d", "Ubuntu", "--exec", "python3", mounted(Path(__file__)),
                   "--linux-stage", "--archive", mounted(archive), "--target", mounted(args.target)]
        # Extracting thousands of small files onto a Windows-mounted checkout
        # is substantially slower than extracting to WSL's Linux filesystem.
        result = subprocess.run(command, capture_output=True, text=True, timeout=900)
        if result.returncode:
            raise RuntimeError("WSL toolchain install failed: " + result.stderr.strip())
        stage = json.loads(result.stdout)
    else:
        stage = install_archive(archive, args.target)
    print(json.dumps({"passed": True, "offline_archive": args.archive is not None,
                      "download": record, "installation": stage}, indent=2))


if __name__ == "__main__":
    main()
