#!/usr/bin/env python3
"""Verify a beta.3 Git bundle by importing it into the isolated baseline."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = "b35b77cddbefdb509058f1fbaaeafaa3982ce172"
BRANCH = "codex/beta3-direct-w"
BASELINE_META = "/tmp/ak820-beta3-bundle-import-baseline.json"


class CheckFailure(Exception):
    pass


def parse_bundle_header(path):
    data = path.read_bytes()
    header, sep, _payload = data.partition(b"\n\n")
    if not sep:
        raise CheckFailure("bundle header has no blank-line terminator")
    lines = header.splitlines()
    if not lines or lines[0] != b"# v2 git bundle":
        raise CheckFailure("bundle header is not Git bundle version 2")
    prereqs, refs = [], []
    for raw in lines[1:]:
        try:
            line = raw.decode("ascii")
        except UnicodeDecodeError as e:
            raise CheckFailure("bundle header contains non-ASCII metadata") from e
        fields = line.split()
        if line.startswith("-"):
            prereqs.append(fields[0][1:] if fields else "")
        elif len(fields) >= 2:
            refs.append((fields[0], fields[1]))
        else:
            raise CheckFailure(f"unrecognized bundle header line: {line!r}")
    return prereqs, refs


def run(record, name, args, cwd=None):
    p = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=False)
    record.append({"name": name, "command": list(map(str, args)),
                   "returncode": p.returncode, "stdout": p.stdout,
                   "stderr": p.stderr})
    if p.returncode:
        raise CheckFailure(f"{name} failed with exit code {p.returncode}")
    return p.stdout


def git(record, name, repo, *args):
    return run(record, name, ["git", "-C", str(repo), *args])


def ensure_new_regular(path, label):
    if path.is_symlink() or path.exists():
        raise CheckFailure(f"{label} already exists or is a symlink: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--source-commit", required=True, help="C1 commit")
    ap.add_argument("--output", required=True, help="new JSON receipt path")
    a = ap.parse_args()
    repo, baseline, bundle, output = map(Path, (a.repo, a.baseline, a.bundle, a.output))
    log = output.with_suffix(output.suffix + ".log")
    ensure_new_regular(output, "receipt")
    ensure_new_regular(log, "command log")
    record = []
    result = {"format": "ak820-beta3-bundle-import-receipt-1", "status": "FAIL",
              "base": BASE, "source_commit": a.source_commit, "commands": record,
              "checks": {}, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    failure = None
    try:
        if repo.is_symlink() or baseline.is_symlink() or bundle.is_symlink():
            raise CheckFailure("repo, baseline, and bundle paths must not be symlinks")
        if not bundle.is_file() or not output.parent.is_dir():
            raise CheckFailure("bundle must be a regular file and output parent must exist")
        result["bundle_sha256"] = hashlib.sha256(bundle.read_bytes()).hexdigest()
        meta = json.loads(Path(BASELINE_META).read_text())
        if meta.get("base") != BASE or Path(meta.get("repository", "")).resolve() != baseline.resolve():
            raise CheckFailure("baseline metadata does not match expected isolated baseline")
        if meta.get("uses_alternates") is not False or meta.get("future_commit_objects_available") is not False:
            raise CheckFailure("baseline metadata does not attest to independent pre-import state")
        if git(record, "baseline-is-bare", baseline, "rev-parse", "--is-bare-repository").strip() != "true":
            raise CheckFailure("baseline is not bare")
        alt = git(record, "baseline-object-info", baseline, "rev-parse", "--git-path", "objects/info/alternates").strip()
        altpath = Path(alt)
        if not altpath.is_absolute():
            altpath = baseline / altpath
        if altpath.exists() and altpath.read_text().strip():
            raise CheckFailure("baseline has objects/info/alternates")
        if os.environ.get("GIT_ALTERNATE_OBJECT_DIRECTORIES"):
            raise CheckFailure("GIT_ALTERNATE_OBJECT_DIRECTORIES is set")
        git(record, "baseline-base-present", baseline, "cat-file", "-e", BASE + "^{commit}")
        source = a.source_commit
        head = git(record, "source-head", repo, "rev-parse", "HEAD^{commit}").strip()
        result["head"] = head
        if git(record, "source-branch", repo, "branch", "--show-current").strip() != BRANCH:
            raise CheckFailure("source repository is on the wrong branch")
        if git(record, "source-clean", repo, "status", "--porcelain").strip():
            raise CheckFailure("source repository is not clean")
        git(record, "source-commit-valid", repo, "cat-file", "-e", source + "^{commit}")
        git(record, "base-ancestor", repo, "merge-base", "--is-ancestor", BASE, head)
        git(record, "source-ancestor", repo, "merge-base", "--is-ancestor", source, head)
        # Require the precise final commit to be unavailable before bundle verification/fetch.
        cmd = ["git", "-C", str(baseline), "cat-file", "--batch-check"]
        p = subprocess.run(cmd, input=head + "\n", text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        record.append({"name": "preimport-final-commit-absence", "command": cmd,
                       "stdin": head + "\n", "returncode": p.returncode,
                       "stdout": p.stdout, "stderr": p.stderr})
        if p.returncode != 0:
            raise CheckFailure("cat-file --batch-check failed while checking final HEAD absence")
        if p.stdout != head + " missing\n":
            raise CheckFailure(f"final HEAD object is present or absence was ambiguous: {p.stdout!r}")
        result["checks"]["preimport_final_commit_absent"] = True
        result["checks"]["baseline_base_present"] = True
        prereqs, refs = parse_bundle_header(bundle)
        if prereqs != [BASE]:
            raise CheckFailure(f"bundle prerequisite list differs from expected base: {prereqs!r}")
        if refs != [(head, f"refs/heads/{BRANCH}")]:
            raise CheckFailure(f"bundle exported refs differ from expected single branch/head: {refs!r}")
        listed = git(record, "bundle-list-heads", repo, "bundle", "list-heads", bundle).strip().splitlines()
        listed_fields = [line.split() for line in listed]
        expected_listed = [[head, f"refs/heads/{BRANCH}"]]
        if listed_fields != expected_listed:
            raise CheckFailure(f"bundle list-heads differs from expected single branch/head: {listed_fields!r}")
        result["checks"]["bundle_v2_exact_prerequisite_and_ref"] = True
        git(record, "bundle-verify", baseline, "bundle", "verify", bundle)
        dest = f"refs/codex/beta3-imported/{BRANCH}"
        chk = subprocess.run(["git", "-C", str(baseline), "show-ref", "--verify", "--quiet", dest],
                             text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        record.append({"name": "destination-ref-absence", "command": ["git", "-C", str(baseline), "show-ref", "--verify", "--quiet", dest],
                       "returncode": chk.returncode, "stdout": chk.stdout, "stderr": chk.stderr})
        if chk.returncode != 1:
            raise CheckFailure("owned destination ref already exists or its absence could not be established")
        git(record, "bundle-fetch", baseline, "fetch", "--no-tags", str(bundle),
            f"refs/heads/{BRANCH}:{dest}")
        imported = git(record, "imported-ref", baseline, "rev-parse", f"{dest}^{{commit}}").strip()
        if imported != head:
            raise CheckFailure("imported ref does not equal source final HEAD")
        src_tree = git(record, "source-tree", repo, "rev-parse", head + "^{tree}").strip()
        dst_tree = git(record, "imported-tree", baseline, "rev-parse", imported + "^{tree}").strip()
        if src_tree != dst_tree:
            raise CheckFailure("imported tree differs from source final HEAD")
        git(record, "fsck-full", baseline, "fsck", "--full")
        result["checks"].update({"bundle_has_exact_branch_and_head": True, "bundle_verify": True,
                                "imported_commit_matches_head": True, "tree_matches": True,
                                "fsck_full": True})
        result["status"] = "PASS"
    except Exception as e:
        failure = f"{type(e).__name__}: {e}"
        result["failure"] = failure
    result["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    # Output paths were checked absent; use exclusive creation so prior evidence is never overwritten.
    with log.open("x", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
        f.write("\n")
    with output.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(json.dumps({k: result.get(k) for k in ("status", "base", "head", "source_commit", "bundle_sha256", "failure")}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
