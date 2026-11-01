# AK820 v0.6.0-beta.5

This beta updates the ten firmware profiles and their exact-image capability
and settings catalogs. Typing, Code, Pointer and Multi-OS add Tap Dance;
Creative adds NKRO control; Shortcuts adds Dynamic Macros and NKRO control.
See the profile documentation for the full feature sets and limitations.

Settings backups now retain the Leader key timeout together with the other
settings, so a restore returns the timeout to the value saved from the
source image.

Caps Word gestures (both Shifts, double left Shift) are build-time switches
now; the default profile behavior is unchanged. Profiles that enable Mouse
Keys accept build-time overrides for the cursor and wheel step and period.

Settings migration recognizes the exact published beta.4.1 image identities
and current image identities; restore targets must be current beta.5 images.
The published beta.4 and beta.4.1 images have identical identities and cannot
be distinguished by image identity. Other source identities are unsupported.
Back up settings before updating; image identity and compatibility checks
remain mandatory.

The release is based on offline build, simulator, packing and migration
checks. It has **not** been validated on physical hardware. Settings writes
remain separately gated; follow the installation guide and retain a recovery
backup.
