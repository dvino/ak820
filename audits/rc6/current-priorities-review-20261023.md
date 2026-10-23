# Current priorities review, 2026-10-23

Reviewer: independent optimization-sources agent. Scope: English and Russian
ROADMAP and STATUS, against the owner's latest work order. This review did
not change those four files or run builds or device operations.

The new scope introductions agree in both languages: P1/P2 first, Direct
Control research only, then Breathing and settings-preserving updates. They
retain explicit device-write approval, six layers and sixteen macros. They
record reactive lighting as the owner's observation and defer the requested
device tests, popup, language/indicator changes and Windows packaging.

## Findings from the first read

1. **P1: unconditional Direct removal remains in STATUS.**
   `docs/STATUS.md:76-78` says to prioritize an editor and save/restore,
   "otherwise remove the mode". `docs/ru/STATUS.md:82-84` repeats this.
   The new introduction requires explicit permission, but these detailed
   instructions omit it. Replace the fallback with a future permission-gated
   decision and label Direct implementation deferred. A reader should not
   have to reconcile conflicting instructions before acting.
2. **P2: old work orders still read as current directions.**
   `docs/ROADMAP.md:65-82` and `docs/ru/ROADMAP.md:67-84` tell the next agent
   to continue all P0/P1/P2 and prioritize Direct implementation. The P0
   sections (`docs/ROADMAP.md:123-140`, `docs/ru/ROADMAP.md:124-142`) direct
   popup, Windows packaging and deferred physical tests. STATUS also says to
   continue the entire unfinished roadmap. The top override restricts these,
   so this is ambiguity rather than an independent authorization. Label
   prior/deferred requirements explicitly and remove present-tense work
   orders for out-of-scope work. Keep the six-layer/macro constraints active.
3. **P2: completed checkpoint is presented as a future stop.**
   `docs/ROADMAP.md:29-34` and `docs/ru/ROADMAP.md:31-36` still call one more
   candidate and device tests the agreed stopping point. Their later text
   says that installation and handoff are complete. Rename this completed
   checkpoint and use past tense so it cannot suggest another flash/test
   cycle under the resumed research scope.

No material translation disagreement was found in the new scope paragraphs.
The preserved device/build evidence was not revalidated in this document-only
review. Its resource and artifact claims are outside this review's scope.

## Closure

Reread all four corrected sections on 2026-10-23. Finding 1 is closed:
STATUS now says to research Direct only and requires explicit permission for
removal in both languages. Finding 2 is closed: roadmap future requirements
defer popup and packaging, Direct implementation is an eventual goal, P0
device tests are deferred, and STATUS follows current priorities rather than
ordering all unfinished work. Finding 3 is closed: the checkpoint is marked
completed and its introduction uses past tense in both languages.

Disposition: PASS for the current-priority documentation changes. No remaining
scope or translation finding in these four files. This does not approve a
firmware change, device operation or commit.
