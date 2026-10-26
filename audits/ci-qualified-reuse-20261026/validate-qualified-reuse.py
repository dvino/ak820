import json
import os
import re
import subprocess
import urllib.request

PROFILES = "main game mmo typing code pointer onehand creative shortcuts multios".split()
WORKFLOW = ".github/workflows/windows-installer.yml"


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def allowed_path(path):
    if path == WORKFLOW or path.startswith("audits/"):
        return True
    if path == "ci/beta2-release-notes.md":
        return True
    if re.fullmatch(r"(?:README(?:[^/]*)|docs/.+)\.md", path):
        return True
    return any(path == f"ci/profiles/{profile}/{name}" for profile in PROFILES
               for name in ("release-policy.json", "program-review.md",
                            "release-safety.json", "packing-validation.json"))


def validate_metadata(run, jobs, artifacts, repository, run_id, workflow_id):
    require(str(run.get("id")) == run_id, "Run ID mismatch")
    require(run.get("repository", {}).get("full_name") == repository,
            "Run repository mismatch")
    require(run.get("head_repository", {}).get("full_name") == repository,
            "Run head repository mismatch")
    require(run.get("workflow_id") == workflow_id and run.get("path") == WORKFLOW,
            "Run workflow mismatch")
    require(run.get("status") == "completed", "Run is not completed")
    head = run.get("head_sha", "")
    require(re.fullmatch(r"[0-9a-f]{40}", head) is not None, "Invalid source SHA")
    for profile in PROFILES:
        matches = [job for job in jobs if job.get("name") == f"Qualify firmware ({profile})"]
        require(len(matches) == 1 and matches[0].get("status") == "completed"
                and matches[0].get("conclusion") == "success",
                "Missing, duplicate or unsuccessful latest qualification: " + profile)
    qualified = [a for a in artifacts if a.get("name", "").startswith("ak820-qualified-profile-")]
    expected = {"ak820-qualified-profile-" + p for p in PROFILES}
    require(len(qualified) == 10 and {a.get("name") for a in qualified} == expected,
            "Missing, duplicate or unexpected qualified artifact")
    require(all(a.get("expired") is False for a in qualified), "Expired qualified artifact")
    return head


def main():
    run_id = os.environ["QUALIFIED_RUN_ID"]
    require(re.fullmatch(r"[1-9][0-9]*", run_id) is not None, "Invalid numeric run ID")
    require(os.environ["EVENT_NAME"] == "workflow_dispatch"
            and os.environ["REF"].startswith("refs/tags/v"),
            "Reuse requires dispatch on a version tag")
    repository = os.environ["GITHUB_REPOSITORY"]
    require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) is not None,
            "Invalid repository")
    base = os.environ["GITHUB_API_URL"] + "/repos/" + repository + "/actions/"

    def api(path):
        request = urllib.request.Request(base + path, headers={
            "Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)

    def pages(path, key):
        result = []
        page = 1
        while True:
            data = api(path + ("&" if "?" in path else "?") + f"per_page=100&page={page}")[key]
            result.extend(data)
            if len(data) < 100:
                return result
            page += 1

    run = api("runs/" + run_id)
    workflow = api("workflows/windows-installer.yml")
    head = validate_metadata(run, pages("runs/" + run_id + "/jobs?filter=latest", "jobs"),
                             pages("runs/" + run_id + "/artifacts", "artifacts"),
                             repository, run_id, workflow["id"])
    current = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    require(current == os.environ["GITHUB_SHA"], "Checkout source mismatch")
    subprocess.run(["git", "merge-base", "--is-ancestor", head, current], check=True)
    changed = subprocess.check_output(["git", "diff", "--name-only", "-z", head, current]).decode().split("\0")
    rejected = [path for path in changed if path and not allowed_path(path)]
    require(not rejected, "Unqualified source changes: " + repr(rejected))
    print("Qualified artifact reuse accepted from " + run_id + " at " + head)


if __name__ == "__main__":
    main()
