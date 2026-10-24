# Documentation review, 2026-10-24

Scope: the 39 public Markdown documents selected by `tools/check_docs.py`,
including English and Russian guides, README and contribution instructions.
Root `AGENTS.md` was also read. The review checks documented behavior against
selected firmware code, installer commands, CI configuration and retained
alpha.2 release evidence. It does not review every upstream source document or
revalidate external websites.

The published and installed image remains `v0.6.0-alpha.2`, source commit
`4772c433057bde5c9ccc4f2f3f904f1dcb326c17`, application IHX SHA256
`a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f`.
This documentation work changes no firmware, installer or release artifacts.

## Checks

The source comparison covered the selected port's `rules.mk`, `config.h`,
`keymaps/vial/keymap.c`, compact tap-hold and Combo engines, macro and RGB code,
keycode decoding, owned keyboard reports, Caps Word, Repeat, Grave Escape,
Tri Layer and indicator behavior. Installer checks covered CLI arguments,
GUI action routing, accepted settings-image identities, backup limits, native
package builders and the release workflow. Sizes and validation claims were
compared with the retained alpha.2 asset and device results.

`python3 tools/check_docs.py` passed: 39 documents, zero failures. A separate
offline scan resolved local Markdown heading anchors, including Russian
headings: zero unresolved anchors. File paths, language counterpart links and
command examples were also inspected. These checks neither run the documented
device commands nor establish external-link availability.

## Findings and closure

The review identified these documentation issues during editing:

- README claimed usable NKRO although the selected build disables Magic
  keycodes and offers no supported mode switch. The guide now describes
  default 6KRO and names the unsupported switch.
- Several technical pages described an earlier development candidate instead
  of the released and installed alpha.2. Current state and dated experiments
  are now separated; current pages link to Status for exact evidence.
- The English Roadmap temporarily contained Russian prose. Both versions now
  describe the planned next stage, with unknown feature costs, qualified
  profiles, actual-build resource checks and exact-image update compatibility.
- Build instructions lacked native Linux packaging, described publication as
  firmware and Windows only, and used a Markdown extension for a JSON approval
  example. Native Linux packaging and current publication outputs were added;
  the approval example is now a fenced command with a `.json` path.
- Installation lacked the initial OEM installation path; settings guidance
  pointed to Status as a complete accepted-image list even though the installer
  accepts five exact images. Source installer setup, backup snapshot limits,
  the single-device requirement and several Russian counterpart links also
  needed clarification. These are corrected in both languages. The generated
  five-image profile record matches the source hash and all IHX/CODE identities.
- Configuration needed exact 6KRO overflow wording, Caps Word continuation and
  timeout behavior, usable named action codes and the compact build's `TT`
  fallback behavior. These are now documented. Further review corrected the
  directional Alt Repeat examples, the Grave Escape character example and a
  Russian editing fragment.
- The live test example selected the retained legacy bundle while describing
  alpha.2 diagnosis. It now requires an exact alpha.2 bundle, approval and
  matching permanent-image session; it does not imply the settings backup is
  such a session.
- After the next-stage plan changed, Space Options still said that further
  code reduction was not scheduled. Both language versions now link to the planned analysis in the Roadmap.
- Generic layer-table wording implied that `TO` or `TG` could cancel held
  layers. Source inspection showed separate persistent and held owners; the
  table and following paragraph now preserve that distinction.

Review decision: approved for this documentation work package after closure
of the findings above. The final public-document link and anchor checks passed;
`git diff --check` passed. No unresolved documentation finding remains. This
record is not firmware approval or permission for a device operation.

## Limits

No builds, hardware reads or writes, resets, loader transitions or flashes were
performed for this review. Existing host/CPU and device evidence was inspected;
none was repeated. A link or source match does not prove physical typing,
Combo timing, encoder signals, lighting appearance, power-cycle retention or
manual GUI acceptance. These remain subject to the limits recorded in Status.
