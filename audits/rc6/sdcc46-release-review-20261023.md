# SDCC 4.6 release review

Independent review, 2026-10-23. PASS for offline bundle assembly of the exact
build and host files bound below. No blocking finding remains. This is not
installer approval, hardware validation or authorization for a USB operation.
The final closure and machine record supersede the earlier pending notes.

I reviewed the new compiler-selection helper and tests in
`tools/build_release_bundle.py` and `tools/test_build_release_bundle.py`, the
SDCC 4.6 probe and packaging audits, and the completed SDCC 4.4 combined-build
and RGB CPU reviews. The working tree contains older changes; this review
does not treat every change from HEAD as part of the compiler-selection work.
I authored no implementation, ran no compiler or simulator, assembled no
bundle, and did not access USB.

## Packaging check

The default remains SDCC 4.4 with the production builder. Explicit selection
of another directory requires the six recorded SDCC 4.6 executable hashes
and the exact private builder hash. The selected compiler, assembler, builder
and dead-code tool must match the build report. Source and toolchain records
still pass through `validate_inputs`. IHX, MAP and memory-report checks,
independent build and host binding, and the second host snapshot remain in
place. The bundle copies the selected builder and hashes it in the manifest.
No weakening of these gates was found in the selection helper.

I ran `python -m unittest discover -s tools -p test_build_release_bundle.py`:
11 tests passed. This is host validation; it does not run the compiler or
prove firmware behavior. The packaging audit correctly records that the
private builder requires its original staging layout for reproduction.

The installer follow-up is also reviewed. `load_release` accepts exactly the
previous required file set or that set plus `reproduction/build_ak820.py`.
It hashes every listed file and requires the optional builder hash to equal
the checked build report's `builder_sha256`. Unknown extra files remain
rejected. The original release and installer-approval bindings still follow
these checks. I ran the amended installer suite: 48 tests passed. No defect
was found in this bounded integration change.

## Initial gates (historical; closed below)

1. Close the known SDCC issue 3845 for the actual image. A failing `__data`
   boolean-member-pointer fixture cannot be dismissed merely because XDATA,
   generic-pointer or current-record fixtures pass. Show which affected
   patterns are reachable in this build and why their emitted code is safe,
   or keep this compiler out of the release.
2. Disposition the compiler diagnostics. I independently compared the saved
   4.4 and 4.6 logs and found the same 11 new warning sites reported by the
   probe: read-only-code warnings at `gpio.c:6` and `_pin_defs.h:41`, enum
   range at `keycodes.h:89`, optimizer flow warnings at `action.c:683`,
   `action.c:920`, `action.c:977`, `dynamic_keymap.c:685` and `vial.c:417`,
   plus unreachable-code warnings at three of those locations. Explain
   these against the configured source and emitted code.
3. Close the five separate Internal issue diagnostics for `clear_keys`,
   `add_key`, `del_key`, `timer_read_fast` and `timer_elapsed_fast`. Check the
   required definitions and callers in the linked image. A successful link
   alone does not establish correct extern-inline behavior.
4. Review completed full regression and RGB CPU reports bound to candidate
   IHX SHA256 `f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e`.
   Check the actual reports and their input identities, rather than a running
   process number or an earlier image's PASS.
5. Recheck the final source, artifact, host and documentation identities
   before creating any exact-build offline review record.

## Boolean-store and RGB follow-up

I reviewed the compiler fixture, both runners, their README and the compiler
audit. The fixture starts each Boolean at the opposite value and tests false
and true, so the missing store cannot pass by retaining a matching initial
byte. The general gate remains FAIL: both compilers pass 14 of 16 cases,
including with the current callee list. This is a known defect in both tested
compilers, not evidence that the compiler is generally correct.

The current-image applicability part of gate 1 is closed within the stated
scope. I independently repeated the source near-declaration and alias search
and retained-ASM indirect-store search. The only near indirect store is the
atomic helper at `main.asm:607`, which writes an r3 byte. I inspected the
matrix factory's carry-to-byte materialization and XDATA event store at
offset five. The linked runner checks both matrix Boolean values, their
action records and all four encoder event objects. Its saved 4.6 report
passes eight checks and binds the candidate hash above. These checks support
the audit's conclusion that the discovered defective near-pointer shape is
absent from these retained paths. They do not prove every Boolean operation
or future configuration safe. No backport is needed for these paths on this
evidence; the reusable failing compiler gate must stay explicit.

I also checked the completed RGB CPU report. Its control hash is
`4b68ae92d95538e4c0af1d445c723645b1d7f570b3ea206002d7521b45fe7ce3`
and its candidate hash matches the 4.6 image above. It passes the same five
seeds, 200 events per seed and image, and 200 exact callback checks per image.
The recorded foreground state-run stack use is 22 control bytes and 18
candidate bytes. This closes the RGB part of gate 4; the full regression
remains pending. No simulator was run by this reviewer.

The probe explains the five-byte HOME hole and compiler elision of twelve
empty stubs. Those observations do not close the correctness gates above.
The 38,100 occupied CODE bytes and smaller image are build measurements.
Physical USB, key and encoder behavior, LED timing, storage durability,
power-loss behavior and worst-case interrupt stack use remain untested by
these host and CPU checks. No candidate image has been installed here.

## Completed regression and diagnostic checks

I checked `host/runs/20261023-sdcc46-full-regression.json`: all 19 stages
exit zero, all 19 saved log hashes match, and the report binds the current
IHX and MAP before and after testing. The guarded-erase profile is recorded;
the package stage reports 75 tests with no skips. This is the completed
offline run, not a claim about device behavior. Later packaging and installer
changes were also covered by my separate 11- and 48-test runs above.

I rechecked the actual selected toolchain and builder with `validate_tools`,
all 465 source/toolchain records, and all 76 artifact sizes and hashes.
There were no mismatches. The selected private builder and production
default remain distinct. The candidate has 2,067 XRAM bytes, matching the
control; an earlier probe description of 2,071 control bytes was corrected.

The diagnostic disposition table explains all 11 new warning sites against
the current configured source and emitted paths: read-only lookup data,
zero configured delays, disabled mouse-key bodies and the intentional
16-bit keycode enum extension. The five inline diagnostics are closed for
this image: I confirmed no retained call to the missing out-of-line names
and confirmed concrete calls to the downstream report/timer functions.
This does not resolve the compiler's out-of-line inline-definition problem
for configurations that require those symbols.

Technical review gates are closed for this candidate's offline packaging.

## Final closure

English and Russian STATUS now agree with the completed 19-stage regression,
75 package tests with no skips, the five-byte reserved HOME range, measured
memory, focused checks and known 14/16 compiler result. The probe's final-ASM
line references were corrected. These documentation findings are closed.
Its earlier applicability-under-review note is superseded by the bounded
compiler audit and this independent review. Packaging remains a separate
offline step and the installed keyboard remains unchanged.

The following record binds this verdict to the exact IHX, MAP, build report
and current host files. Changing any bound file requires a fresh agreement
check. The known general compiler fixture failure is accepted only with the
documented current-image applicability limit; this verdict is not a blanket
SDCC correctness claim. No installer approval file was written.

## Candidate bundle closure

I independently checked `releases/rc6-sdcc46-breathing-20261023` after
assembly. Its manifest SHA256 is
`1603385c0c1f77e76052432f6b11a116b17b03bdd4a7c1e29408e9924ce2a47e`.
All nine bound files match their recorded sizes and hashes. The directory
contains exactly those nine files plus the manifest, with no OEM binaries.
Copied IHX, MAP, memory report, build report and private builder match the
reviewed inputs. The copied review binds the exact build and current host
files, and the real installer `load_release(approved=False)` passes offline.

The packing report records trial and permanent 51,136-byte payload checks,
build ID 532482, unchanged recovery bytes, six-layer/83-key migration and
both encoder directions. It explicitly records no physical USB access and
no hardware validation. This review checks the saved report's consistency;
it does not repeat packing or establish device persistence.

No finding blocks reversible offline promotion to the active release,
binding its installer approval to this exact manifest, or a Windows
standalone build. The lead owns preservation and path checks for promotion.
This is not permission to reset, enter bootloader, flash or write to USB.
This appended closure exists only in the root audit. The already copied
review inside the candidate bundle remains unchanged and bound by its
manifest; no candidate bundle bytes were modified during this review.

## Active bundle and Windows artifacts

The promoted `releases/rc6` is byte-equal to the reviewed candidate. Its
manifest remains `1603385c0c1f77e76052432f6b11a116b17b03bdd4a7c1e29408e9924ce2a47e`.
The source installer loads it with `approved=True` offline. Both standalone
apps embed that same bundle, approval and all 16 current host files: I
independently rehashed 20 embedded bundle copies and 32 host copies.
The embedded project files agree with the builder's explicit input allowlist.

Both executable hashes and sizes match
`host/runs/20261023-sdcc46-windows.json`. I also checked the ZIP against every
packaged file: all 1,162 archive members agree with the output directory.
The archive is 20,445,885 bytes, SHA256
`a80338dafdc06f39534db53d4cf23eecdfa18383883549248fdea8f769035fa6`.
Its inventory contains no OEM reference binaries, device backups, evidence
directory or host run logs. This inventory check does not claim a general
scan of every third-party runtime binary for personal data.

The saved Windows report records CLI help, CLI verify and GUI self-test PASS.
I did not rebuild or rerun the executables; this follow-up independently
checks immutable bytes and source approval loading. No artifact finding
remains. Promotion and standalone packaging do not establish installed
firmware behavior or grant permission for a hardware operation. Only this
root audit was appended; the bound review copies remain unchanged.

```json
{
  "format": "ak820-offline-review-2",
  "release": "rc6",
  "status": "passed",
  "hardware_validated": false,
  "host_files": {
    "AK820.cmd": {
      "size": 1149,
      "sha256": "dddbfaad0da2f79d3353bd2238eae323db53b0a066736c7743e84a845b77aaa0"
    },
    "AK820.sh": {
      "size": 515,
      "sha256": "9a8ebbc2ed64d2d0ac6ea7f4d1251d5de630c8af78465dee3acfdc833b4528fb"
    },
    "qmk-8051-ak820/util/ak820_diagnose.py": {
      "size": 13505,
      "sha256": "2a3dd74d73d1b135107468d330818896a7158e16f4e4031b1c1757f14854dc0d"
    },
    "qmk-8051-ak820/util/ak820_release_manifest.py": {
      "size": 2279,
      "sha256": "d5e2a9ddaf47e17db30735df565bfe1277f3b610a802acd808071d1e6c2e632f"
    },
    "qmk-8051-ak820/util/ak820_tool.py": {
      "size": 22039,
      "sha256": "3a0cd520d0ba0b0125300095e5537e5abab2740f7098c836dc562c39eb6d4e1b"
    },
    "qmk-8051-ak820/util/native_macro_import.py": {
      "size": 2499,
      "sha256": "572f153de6ec9a71eefa8fd87c5ba2bd7da602619131e3ec66fa63d9a742b07f"
    },
    "qmk-8051-ak820/util/pack_ak820.py": {
      "size": 23558,
      "sha256": "9e2454b0aaa790874bbb7117680c67fd134b45d4ece7281bf6b5b8ea17e59a7f"
    },
    "qmk-8051-ak820/util/prepare_ak820_trial.py": {
      "size": 5745,
      "sha256": "91458b9a14bad55f9bb9a056ec43f8daec0ffe996f21f4ffc15e9f6730aa9fc2"
    },
    "tools/build_release_bundle.py": {
      "size": 11946,
      "sha256": "8c3bfa8e8ca2f736fb7d284158f9f76179b724d098a65a0bc49364c0cd333655"
    },
    "tools/build_windows_installer.py": {
      "size": 3692,
      "sha256": "53fb19ad029610154a7a1c6a10d616f0f1c9f25ea6215eb44a36e84671a4bd09"
    },
    "tools/installer/70-ak820.rules": {
      "size": 339,
      "sha256": "f0b85bb730963057350a6a9cfe35e1f17e2859a5bfbcebfce9fccaa6534a3a52"
    },
    "tools/installer/ak820.py": {
      "size": 47011,
      "sha256": "b6eff1487c07d4d871b0df7bab44e58e870a23170ac827d066eab8777e2c905d"
    },
    "tools/installer/gui.py": {
      "size": 15632,
      "sha256": "c7406dc28815a7bf5daa2084adc8c8fffb7280daa9566a21161db346a38cdea6"
    },
    "tools/installer/i18n.py": {
      "size": 14399,
      "sha256": "c72831bc8e9b3a5f036e56d72baf2dc8fc0c5e9ba4c6801178a6115b87956018"
    },
    "tools/installer/requirements-build-windows.txt": {
      "size": 235,
      "sha256": "fe92377176d05e83a805899a51be8569cfc63768609bae64c543641f9d715bd5"
    },
    "tools/installer/requirements.txt": {
      "size": 15,
      "sha256": "6e78c6c5a61dbebf36f570a14685c795efcdb3d8bb6b6118b6aa78dd0aca54d4"
    }
  },
  "build": {
    "ihx_sha256": "f1c4347e60ca5f7ea6c557debe60272259f4ddf9acfac9897fa992210bf7ef2e",
    "map_sha256": "d458979b4f3239e01e67e433e6d564637f7439e18cbfa27defa51b29cad62639",
    "build_report_sha256": "248710547b6a61d7e1e6fdf38a2b7eb90b4a4ba9765f6168eb32024c7636f4fa"
  }
}
```
