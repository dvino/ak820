Test alpha for the wired AJAZZ AK820 with VS11K28A. AK820 V2, Pro and Max are unsupported. Match the PCB revision; the model name or USB VID:PID alone is insufficient.

Includes compact Mod-Tap / Layer-Tap, six remappable layers, encoder mappings, macros, and C/W indicator outputs. C follows the host Caps Lock LED; W follows an active non-base layer. Existing Caps assignments are preserved. Lighting palette experiments remain outside the production build.

Both ZIP files are built by this tag’s GitHub Actions run. Check the adjacent SHA256 files before extracting. `AK820-Windows.zip` contains the portable installer. `firmware-bundle.zip` contains the application and its verification evidence; its IHX is not a complete flashable ROM. Linux setup and recovery: [INSTALL](https://github.com/dvino/ak820/blob/v0.6.0-alpha.1/docs/INSTALL.md).

Pre-install offline qualification: 26 suites, 258 unit tests, no skips, linked CPU checks and independent source review. Release CI separately rebuilds and checks the firmware and Windows packages. Physical typing, encoder behavior, C/W connection/polarity and power-cycle persistence are not established by these checks. Native Windows interactive acceptance is pending.

Use the installer update workflow with valid private OEM recovery inputs and a fresh settings backup. It requires a fresh physical Esc + left Control hold for three seconds, then a second confirmation for settings restoration. Keep alternate input and stable power available. Stop on any verification or storage failure; do not retry blindly.

The software is provided AS IS under GPLv3, without warranty to the extent permitted by law. Firmware changes and resulting damage are the user’s responsibility; see the license and README.

---

Тестовый alpha-выпуск для проводной AJAZZ AK820 с VS11K28A. V2, Pro и Max не поддерживаются. Необходимо проверить ревизию платы: названия модели и VID:PID недостаточно.

Добавлены компактные Mod-Tap / Layer-Tap и выходы индикаторов C/W. C показывает Caps Lock хоста, W — активный дополнительный слой. Назначение Caps не изменяется. Все файлы собраны CI этого тега; перед распаковкой проверьте SHA256. IHX в firmware-bundle.zip — приложение, а не полный ROM для прямой прошивки.

До установки локально прошли 26 наборов и 258 юнит-тестов без пропусков, CPU-модели и независимое ревью. Это не подтверждает физическую печать, энкодер, видимые C/W и сохранение после отключения питания. Интерактивная проверка Windows ещё не выполнена. [Установка и восстановление](https://github.com/dvino/ak820/blob/v0.6.0-alpha.1/docs/ru/INSTALL.md).

Код распространяется как есть, без гарантий в пределах закона. Ответственность за действия и возможные поломки несёт пользователь; подробности — в GPLv3 и README.


Installation follow-up, 2026-10-24: the downloaded GitHub release was flashed once. The initial installer stopped with `OSError: open failed` immediately after restart; it did not retry. Later read-only diagnosis verified the exact new CODE/full manifest and healthy storage, then a separate guarded restore with a fresh target backup and physical confirmation restored and verified settings. Final read-only checks passed for 498 key assignments, 12 encoder assignments, 16 macro slots and RGB getters. Manual smoke checks reported typing, both encoder directions, Fn and C/W working. Power-cycle persistence remains untested. The open failure cause is not established; do not repeat flashing to work around it. Preserve logs and backup, verify the running image and storage before any separate restoration.

Результат установки, 2026-10-24: скачанный релиз прошит один раз. После перезапуска установщик остановился с `open failed`, без повтора. Затем точный новый код и исправность хранилища проверены чтением; отдельная штатная команда с новой копией текущего состояния и физическим подтверждением восстановила и проверила настройки. Итоговая проверка чтением прошла; ручная проверка подтвердила печать, колесо в обе стороны, Fn и C/W. Сохранение после отключения питания ещё не проверено. Причина ошибки открытия не установлена. Не повторяйте прошивку для её обхода; сохраняйте журнал и копию, сначала проверяйте текущий образ и хранилище.
