Русский перевод: [AK820 Web](docs/ru/README.md).

# Firmware contracts for AK Configurator

Application source and current planning are maintained in [AK Configurator](https://github.com/dvino/ak-configurator). The imported Entropy source still needs adaptation for AK820.

This directory supplies the firmware selection matrix, exact-image capability catalog, bilingual descriptions and protocol contracts. The requirements and plan below describe the firmware integration baseline; application development is tracked in the separate repository. Start with the [firmware handoff](docs/FIRMWARE-HANDOFF.md).

- [Requirements](docs/REQUIREMENTS.md): behavior and acceptance criteria.
- [Capability catalog](docs/CAPABILITY-CATALOG.md): generate and validate local image data.
- [OS indicator protocol](docs/OS-INDICATOR-PROTOCOL.md): FD02 contract for the firmware module.
- [Implementation plan](docs/PLAN.md): stages, dependencies and completion checks.
- [Status and review](docs/REVIEW.md): source references, completed checks and limits.

Firmware installation instructions remain in the project
[installation guide](../docs/INSTALL.md).
