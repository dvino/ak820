# Development integration — 2026-10-24

Incoming commit `4151edd` was merged into `dev` with the alpha.3 documentation
corrections from `8ffa3e6`. Published and installed firmware remains alpha.3.

Independent review covered source, tools, documentation and retained evidence.
No source blocker was found. Two profile-guide links now point to the frozen
runtime report, and the roadmap names alpha.3 for the current settings policy.
Merge resolution retains the published alpha.3 resource numbers and installed
state. Review findings are closed.

Acceptance checks passed: 49 public documents with no broken local links;
25 configurator tests; 16 short-call tests; Dynamic Macro, GUI, Auto Shift and
Mouse Keys host checks. Independent host checks also passed core differential
coverage. All 18 frozen variants match 90 IHX, MAP, MEM, build-report and raw
archive hashes; raw archive sizes match their records. Existing build and CPU
results remain bound to clean source `55acbb0`; no new firmware build was run
for this integration. Whole-program stack and physical behavior remain unproved.
No device was accessed.

## Archive size

The input archive contains 539,932,156 file bytes before compression:
315,531,644 in `audits`, 215,025,656 in `.git`, and 7,482,476 in firmware
source. Git history and worktree copies both retain build evidence. Multiple
branch refs and superseded raw builds make this a full repository handoff,
not a source-only package. The final runtime matrix is acceptance evidence;
older experiments are not required to use the source. Nothing was removed.
The original archive remains outside the repository. Future handoffs can use
a Git bundle relative to an agreed base, with only newly required evidence,
instead of copying the whole `.git` directory and checkout.
