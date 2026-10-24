Русский перевод: [Состояние проекта](ru/STATUS.md).

# Project status

Updated 2026-10-24. [v0.6.0-alpha.2](https://github.com/dvino/ak820/releases/tag/v0.6.0-alpha.2)
is published from commit `4772c433057bde5c9ccc4f2f3f904f1dcb326c17`.
It includes eight two-key Combos and settings backup/restore for their eight
slots. Windows and Linux x86_64 installers are available. See [Install](INSTALL.md)
for package selection, checksums and launch commands.

## Source and built image

The Combo work was imported from `ak820-combos-20261024-git.zip`, based on
`4b83bb9`, through `d361501`. Release integration adds reviewed settings
preservation and native Linux packaging. The application uses 40,313 CODE
bytes: 38,492 main and 1,821 low. It leaves 120 trailing main-window bytes and
67 low-window bytes. XRAM is 2,621 bytes; initial SP is `0x5f`, with 160 bytes
allocated for the stack. These figures do not prove a worst-case stack bound.

The application IHX SHA256 is
`a64dc561ba898a0107a5c21cbdb861fc0653583856ad64bd379c35343a58022f`.
The IHX is an application, not a complete flashable ROM. The installer builds
the complete update with validated local OEM recovery data.

## Verification

The [tag CI run](https://github.com/dvino/ak820/actions/runs/40060505913)
passed all four jobs. Its firmware qualification passed 28 suites and 270 unit
tests with zero skips. The fresh local qualification before Linux packaging
passed 28 suites and 265 tests; later Linux host changes have separate
[regression evidence](../audits/rc6/alpha2-release-20261024/linux-integration.json).
Host models and linked CPU execution do not establish device behavior.

Native Windows and Ubuntu 22.04/glibc 2.35 builds passed CLI verification and
Tk startup checks. Linux also verified its frozen hidraw backend. The three
downloaded public archives passed checksum, source and packaged-input checks;
see the [asset check](../audits/rc6/alpha2-release-20261024/asset-check.json) and
[independent review](../audits/rc6/alpha2-release-20261024/published-artifact-review.md).
The downloaded Linux CLI also passed local help and offline verification.
GUI startup checks do not establish manual interaction or display scaling.

## Installed firmware

Read-only checks through the downloaded Linux installer confirmed that
`v0.6.0-alpha.1` remains installed. A new private backup verified 498 key
assignments, 12 encoder assignments, 16 macro slots and saved RGB settings.
The [preflash report](../audits/rc6/alpha2-release-20261024/read-only-preflash.json)
records the exact source image and an accepted offline restore plan into
alpha.2 defaults. No setting write or firmware flash was performed for alpha.2.
A new backup and fresh physical confirmation are still required during update.

Physical Combo timing, alpha.2 typing and encoder behavior, manual Windows/Linux
GUI use, cold-start retention and power-loss behavior remain untested. The
[earlier alpha.1 installation report](../audits/rc6/alpha-release-20261024/device-result.json)
records its restart/open failure and the separately verified settings restore.
It is evidence about alpha.1, not a new installation result.
