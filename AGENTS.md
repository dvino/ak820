Русский перевод: [Инструкции для агентов](docs/ru/AGENTS.md).

@C:\Users\vinok\.codex\RTK.md

## Code, documentation and independent review

Owner's rule, 2026-10-21: update documentation alongside code; review must check agreement.

- Update documents in the same work package when behavior, formats, commands,
  addresses, sizes, APIs or limitations change.
- Keep README.md and docs/STATUS.md current. ROADMAP describes the future;
  distinguish the source project, built artifact and installed implementation.
- Regenerate affected machine reports after changing inputs or generators.
  Check sizes, SHA256, versions, addresses and commands against actual artifacts.
- Distinguish static analysis, builds, CPU/host models and device tests.
  A PASS at one level does not prove another; list untested conditions.
- Before committing, obtain review from an independent reviewer who did not
  author the changes. Include code, documentation and verification evidence.
- Resolve disagreements before committing. Save review results and finding
  closure in documentation; retest substantive corrections.
- Mark obsolete descriptions as historical or replace them. Do not leave
  conflicting current-state claims without a date and explanation.

## Documentation language and style

Documentation rule, 2026-10-23: use impersonal wording throughout documentation.
Do not describe an owner's keyboard, personal installation or who performed a
check. Record the result and its evidence without identifying a person.
README introduces the project, features and getting started. Put package paths,
extraction and launch instructions in INSTALL, and validation results and
deployment state in STATUS or technical reports, never in the README introduction.

Owner's rule, 2026-10-23: write all documentation in the owner's style, in
plain language that a person can understand on the first reading. Apply this
to new text and to documents changed during the task, including translations.
Use direct sentences, concrete actions and familiar words. Explain technical
terms when the reader needs them; keep internal audit details in the relevant
technical reports. Avoid bureaucratic wording, marketing, generic AI phrasing
and titles overloaded with architecture or development status. README should
introduce the project and help someone use it. Remove obsolete instructions
and historical documents from the current tree instead of keeping a docs
archive there. Keep tracked versions in Git history; preserve unique
uncommitted material in the external private backup before removing it.
Use the owner's supplied wording and examples; apply the write-like-me skill
when composing substantial documentation, without claiming unavailable style
retrieval.

## Current work boundary

Owner's GUI update rule, 2026-10-23: the update stays inside the installer.
After clicking Update, a fresh physical Esc + left Control hold for three
seconds confirms the displayed update. The installer requests unlock, enters
the loader, flashes once and verifies the result. Do not require typed yes,
ready, a separate Vial app or a manual Bootloader action in this workflow.
Keep fresh backup, exact image checks, cancellation before erase and failure
stop conditions. This does not authorize an agent to start a live update.

Owner's testing rule, 2026-10-23: prepare a reusable automatic regression suite
for use after firmware updates. Cover the supported functions and remapping,
including both encoder directions. The current test work must require no
physical key presses, knob rotation, cable reconnect or manual Vial unlock.
Keep host/CPU tests separate from live protocol and durable-storage checks.
Default test commands must be offline or read-only; setting changes need an
explicit execution option and authorization. A timeout, storage fault or bad
readback is a failure: stop without blind restore, retry, reset or recovery.
Report skipped checks and the physical behavior the suite cannot prove.

Offline checks and local development are authorized. Hardware flashing needs
the owner's explicit confirmation before each operation so alternate input
and stable power can be prepared. Do not send programming, reset or bootloader
transition commands before confirmation. Read-only diagnosis was separately
authorized on 2026-10-23; it does not authorize flashing.

## Agent routing and handoffs

- Communicate with subagents in English: task assignments, clarifications, coordination messages, handoffs and result reports. Continue communicating with the owner in their chosen language.
- The root lead coordinates ownership, integration, current-state checks and the evidence record. Keep each delegated task bounded and explicit about its owned files.
- Use a fresh GPT-6 Luna agent at medium reasoning for limited implementation, documentation or build tasks. Use GPT-6.1 Sol at low reasoning only when a task needs complex reasoning about ABI, NVM, architecture or an independent review. The root lead may adjust this routing when the task requires it.
- Start a fresh agent for a new bounded task or when the current context has grown. Give it a short, self-contained handoff with ownership, relevant current facts, required evidence and stop conditions. Do not fork the full conversation history for routine work.
- Check task ownership before starting. Do not duplicate another agent's work, and do not run simultaneous builds that share a working tree or output paths.
- Authors cannot independently approve their own code. Independent review covers code, documentation and verification evidence; resolve findings and record closure before commit.
- Update documentation alongside implementation. State separately what is known about source, built artifacts and installed firmware, and distinguish static checks, builds, host/CPU models, read-only device diagnosis and device behavior.
- No agent may write to USB, enter bootloader, reset or flash the keyboard without the owner's explicit confirmation for that operation. Read-only diagnosis authorization does not grant flash authorization.
