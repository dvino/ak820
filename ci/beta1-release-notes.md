Trial firmware baseline for designing the AK Configurator companion application.

- Nine fixed profiles: `work` (default), `essential`, `typing`, `mouse`, `mouse-typing`, `system`, `tap-dance`, `key-overrides` and `settings`.
- `work` adds Leader, temporary Dynamic Macros and companion-controlled OS indication. Specialist profiles provide Mouse Keys, Auto Shift, modifier mappings, Tap Dance, Key Overrides or QMK Settings.
- Exact-image capability data, profile compatibility and bilingual descriptions let the companion show the controls supported by each image. Missing module pairs mean no matching profile in this catalog.
- Six layers, 16 Vial macros, 8192 shared macro bytes and eight Combo slots remain available.

Only `work` is available for installation in this beta. The other eight profiles support companion development. Cross-image settings restore requires an explicitly supported source/target pair; schema 03 cannot be restored to schema 02.

[Profile matrix](https://github.com/dvino/ak820/blob/v0.6.0-beta.1/docs/MODULE-MATRIX.md) · [Firmware contracts](https://github.com/dvino/ak820/blob/v0.6.0-beta.1/web/docs/FIRMWARE-HANDOFF.md)

---

Пробная основа прошивки для проектирования приложения-компаньона AK Configurator.

- Девять готовых профилей: `work` (по умолчанию), `essential`, `typing`, `mouse`, `mouse-typing`, `system`, `tap-dance`, `key-overrides` и `settings`.
- `work` добавляет Leader, временные динамические макросы и индикатор OS под управлением компаньона. Специализированные профили предоставляют управление мышью, Auto Shift, перестановки модификаторов, Tap Dance, Key Overrides или QMK Settings.
- Возможности точных образов, совместимость профилей и описания на двух языках позволяют компаньону показывать поддерживаемые элементы управления. Отсутствующая пара модулей означает, что в каталоге нет подходящего профиля.
- Сохранены шесть слоёв, 16 макросов Vial с общим буфером 8192 байта и восемь Combo.

В этой бете для установки доступен только `work`. Остальные восемь профилей служат для разработки компаньона. Восстановление настроек между образами требует явно поддерживаемой пары исходного и целевого образа; схему 03 нельзя восстановить в схему 02.

[Матрица профилей](https://github.com/dvino/ak820/blob/v0.6.0-beta.1/docs/ru/MODULE-MATRIX.md) · [Контракты прошивки](https://github.com/dvino/ak820/blob/v0.6.0-beta.1/web/docs/ru/FIRMWARE-HANDOFF.md)
