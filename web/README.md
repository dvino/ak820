Русский перевод: [AK820 Web](docs/ru/README.md).

# AK820 configurator

The planned configurator brings supported AK820 settings, backups, firmware
updates and stock-firmware recovery into one website. A shared desktop app
will work offline on Windows, Linux and macOS. If Entropy is selected, native
adaptation starts first and the browser version develops in parallel; desktop
release does not wait for the website.

Development uses the `web-dev` branch. The first foundation to evaluate is
Entropy: its Rust/egui interface can be shared with a browser through
WebAssembly. Pipette is the fallback with an existing browser implementation.
The final choice follows the prototype results.

Native development uses `desktop-dev`; `desktop` holds the native version
prepared for release. Shared changes are merged between the development branches.

- [Requirements](docs/REQUIREMENTS.md): behavior and acceptance criteria.
- [Implementation plan](docs/PLAN.md): stages, dependencies and completion checks.
- [Status and review](docs/REVIEW.md): source references, completed checks and limits.

Firmware installation instructions remain in the project
[installation guide](../docs/INSTALL.md).
