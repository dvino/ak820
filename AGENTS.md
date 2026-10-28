Русский перевод: [Инструкции для агентов](docs/ru/AGENTS.md).

@C:\Users\vinok\.codex\RTK.md

# Working on AK820

## Code, documentation and evidence

- Update code and affected documentation together when behavior, formats,
  commands, addresses, sizes, APIs or limits change. Keep README and STATUS
  current; ROADMAP describes future work.
- Regenerate affected machine reports. Verify sizes, SHA256, versions,
  addresses and commands against actual artifacts.
- Distinguish source inspection, static analysis, builds, host/CPU models,
  read-only device diagnosis and physical behavior. A pass at one level does
  not prove another; record skipped checks and untested conditions.
  Keep the source project, built artifact and installed implementation distinct.
- Obtain independent review of code, documentation and evidence before commit.
  Authors cannot approve their own changes. Resolve disagreements, record
  findings and closure, and retest substantive corrections.

## Documentation

- Write plain, concise, impersonal EN/RU text in the owner's style, including
  translations. Use supplied examples and write-like-me for substantial text;
  do not claim unavailable style retrieval. Explain necessary terms; avoid
  bureaucracy, marketing, generic AI phrasing and overloaded headings.
- README introduces the project, features and getting started. INSTALL covers
  package paths, download, checksums, extraction, minimal Python dependencies
  and launch. STATUS and technical reports contain validation, installed state
  and internal evidence. User guides explain actions and behavior.
- Public release notes describe only user-visible changes, fixes and relevant
  limits; omit tests, packaging/licence details, installed state, audits and
  agent process. Do not repeat README.
- Replace obsolete claims or mark historical claims with a date and explanation.
  Remove obsolete instructions and historical documents from the current tree;
  retain tracked history in Git and preserve unique uncommitted material in an
  external private backup before deletion. Do not create a docs archive.

## Firmware and device checks

- Every new feature or profile closes stack and interrupt checks in the same
  change. Bound foreground calls, startup and all enabled interrupt sources
  for the exact linked image. Pass this gate before full regression suites.
  Unknown paths, incomplete IRQ contracts or bounds above capacity block
  completion. Retain machine evidence; another profile cannot qualify changes.
- Maintain a reusable regression suite for supported functions and remapping,
  including both encoder directions. Current automatic tests require no key
  presses, knob rotation, reconnect or manual Vial unlock. Keep host/CPU,
  live protocol and durable-storage evidence separate.
- Default tests are offline or read-only. Settings changes require an explicit
  execution option and authorization. Timeout, storage fault or bad readback
  stops the operation without blind retry, restore, reset or recovery.
- Local development, offline checks and previously authorized read-only diagnosis
  remain authorized; read-only access does not authorize writes. Each hardware
  flash needs explicit confirmation so
  alternate input and stable power can be prepared. USB writes, reset and
  loader transitions require authorization for that operation.
- The installer update flow uses a fresh three-second Esc + left Control hold
  after Update to confirm the displayed image, then unlocks, enters the loader,
  flashes once and verifies. Preserve fresh backup, exact image checks,
  cancellation before erase and failure stops. Typed yes/ready, separate Vial
  or manual Bootloader do not replace this flow. Modeling it offline does not
  authorize a live update.

## Releases

During beta, require backward compatibility only with the immediately preceding
build to avoid spending firmware CODE on older compatibility paths. Determine
that predecessor from the target release; do not extend support back to alpha.

The 2026-10-26 policy supersedes the beta.1 installer direction for beta.3:
provide Python installation scripts for Windows and Linux x86_64, matching
SHA256 and EN/RU instructions. Do not build or publish standalone GUI installers
or bundled runtime dependencies unless a later request changes this policy.
Preserve exact image identities and all ten catalog profiles; state installation
and hardware limits. Companion integration is separate from the beta.3 packet.

## Agent routing and handoffs

- The lead checks current state and ownership, coordinates integration and
  evidence, and assigns bounded tasks with explicit owned files. Avoid duplicate
  work and concurrent builds sharing a working tree or output paths.
- For any long-running operation, including CI, immediately start one persistent
  watcher script or native wait command tied to the exact process, container or
  CI run. Wait for that watcher; an agent repeatedly checking logs or status is
  not a watcher. Stay quiet while unchanged and report completion, failure or
  needed action. Never start a duplicate operation to obtain progress.
- Use fresh GPT-6 Luna at medium reasoning for small edits, docs and routine
  builds; GPT-6.1 Terra (`gpt-6.1-terra`) at low for bounded code implementation/refactoring,
  native UI and visual/browser/desktop tasks. Use GPT-6.1 Sol at low for complex
  ABI/NVM/contracts and independent review. The lead may adjust effort and routing
  within these role limits when the task requires it.
- GPT-6.1 Sol at high is a last resort for architecture/complex planning. Before
  delegation, record the unresolved question and why ordinary work/review cannot
  settle it. Do not use this route for routine work.
- Use fresh contexts for new bounded tasks or grown context. Give a concise
  handoff with ownership, current facts, evidence, dependencies and stop
  conditions rather than the full routine-task conversation. Communicate with
  agents in English and with the user in their chosen language.
- Before finishing a task, clean up temporary files, build outputs and worktrees
  created for it after preserving required artifacts and evidence. Check ownership
  and dirty state first; do not remove active work, unrelated changes, recovery
  backups or the only copy of useful data. Record any retained paths and why.
- Apply the evidence, review and device-authorization rules above to every agent.
