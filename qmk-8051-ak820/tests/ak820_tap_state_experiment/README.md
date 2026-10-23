# RC5: эксперимент с общей логикой tap-действий

Дата: 2026-10-22. Это исследование исходников и размера, **не набор
устанавливаемых прошивок**. База измерений — замороженный RC5 candidate3
до последующих исправлений LM с правыми модификаторами и повторной отправки
USB reports. Для текущего выпуска использовать его собственный build report.

## Что сравнивается

`action_tapping.c` уже содержит один `tapping_key`, одну очередь
`waiting_buffer` и одну `process_tapping()` для MT/LT/OSM/OSL. Их распознаёт
`action.c:is_tap_action()`. Дополнительные постоянные состояния One Shot
(маска модификаторов/lock и состояние слоя) находятся в `action_util.c`.

`common-tail.patch` объединяет повторявшиеся **выходные действия** внутри
`process_action()`: обычный tap MT/LT с одинаковой задержкой отпускания,
путь обычного modifier для отключённого OSM, путь momentary layer для
отключённого OSL/LT hold, снятие held/locked OSM. Общая очередь и решения
о tap/hold остаются в существующем движке. Вынесение того же поведения
в общий вызываемый helper измерено отдельно и отвергнуто: +149 байт CODE.

Tap Dance требует дополнительного состояния каждой записи: число taps,
pressed/finished/interrupted, захваченные модификаторы и callbacks
`on_each_tap`/`on_each_release`/`finished`/`reset`. Его preprocess может
завершить предыдущий dance, изменить слой и заставить `quantum.c` заново
разрешить прерывающую клавишу. Слияние этих объектов с одним pending
MT/LT record не сохраняет семантику автоматически. Общие хвосты измерены
и с включённым Vial Tap Dance, без удаления его отдельных состояний.

## Результаты SDCC 4.4.0

| Профиль | Исходный CODE | Общие хвосты | Разница | XRAM до → после |
|---|---:|---:|---:|---:|
| Активный: tapping/oneshot отключены | 40461 | 40461 | 0 | 2323 → 2323 |
| Tapping + One Shot | 46444 | 46170 | −274 | 2526 → 2527 |
| Tapping + One Shot + Vial TD, 4 записи | 50557 | 50283 | −274 | 2725 → 2726 |

В активном профиле обе IHX совпадают побайтно:
`76a12ea9dda4468026dadc9edfe19876ba0ea26e1144af1874169d98a252f055`.
Отвергнутый helper даёт 46593 CODE и 2532 XRAM в tapping/oneshot профиле
против 46444/2526. Это показывает цену дополнительных вызовов и передачи
состояния на данном SDCC/8051, несмотря на уменьшение исходного C.

`measurements.json` содержит значения, SHA256 и связь с семью исходными
`reports/*.json` и `.mem`. Полные build reports сохраняют реальные `.d`
зависимости, команды и инструментальные hashes. Экспериментальные IHX в
этот каталог намеренно не включены. Профили с tapping собирались с
`--code-end 0xf700` только для оценки: они перекрывают NVM, не помещаются в
выпускной диапазон и несовместимы с обычной CPU-фикстурой NVM.

## Host-проверка общей логики

Из корня QMK после применения `common-tail.patch` к рабочей/исследовательской
копии `quantum/action.c`:

```sh
python tests/ak820_tap_state_experiment/run.py --output /tmp/common-action-results.json
```

Для отдельного файла:

```sh
python tests/ak820_tap_state_experiment/run.py --candidate /path/to/action.c --output /tmp/common-action-results.json
```

Runner читает неизменяемую `process_action()` и настоящий `is_tap_action()`
из Git `cb9ff6ea`, извлекает candidate из указанного исходника и компилирует
их с одним trace harness. Он сравнивает последовательность вызовов,
состояние и модификацию record. На каждый профиль проверяются все payload
значения семи затронутых action kinds, оба направления, все 16 tap counts
и 16 начальных состояний: **14680064 сочетания**. Четыре профиля:
активный disabled, tapping/oneshot, hold-on-interrupt и retro-tapping.
`host-results.json` фиксирует **4 PASS** с UBSan и hashes входов.

Это доказательство C-переходов выходного обработчика. Заглушки вызовов
не моделируют весь таймерный движок, callbacks, SDCC static-local alias,
IRQ и USB. Для активного профиля отдельное более сильное свидетельство —
совпадение всего связанного IHX; перед будущим включением tapping нужны
его собственные CPU-тесты и полный review взаимодействий.

## TD-порт только для измерения

`td4-size-only-port.patch` включает четыре записи и устраняет препятствия
компиляции: compound literals/range switch/empty initializer, явный
`__reentrant` ABI многопараметрических callbacks и дубль
`get_tapping_term()` (SDCC-порт игнорирует GCC weak attribute). Патч
предполагает исходный профиль с включёнными tapping/oneshot. Callback ABI
скомпилирован, но не проверен полноценными CPU-сценариями, поэтому этот
порт не переносится в активные исходники и не объявляет поддержку TD.

Чтобы повторить size comparison в отдельной копии QMK, использовать
тот же pinned SDCC/QMK environment и `util/build_ak820.py`. Для baseline
сохранить исходный `process_action()`; для варианта применить
`common-tail.patch`. Убрать `NO_ACTION_TAPPING`/`NO_ACTION_ONESHOT` только
в копии; для TD дополнительно применить `td4-size-only-port.patch`.
Каждой сборке требуется новый `--build-dir`. Числа могут отличаться на
более поздней базе; сравнивать пары с одинаковыми остальными входами.

## Caps Word: отдельная исправленная граница LT

При проверке будущего tapping профиля исправлена опечатка верхней границы
`QK_LAYER_TAP` в `process_caps_word.c`: `>= MAX` заменено на `<= MAX`.
Активная ветка без tapping от этого не меняется. Расширенный
`tests/ak820_caps_word/run.py` проверяет обычный профиль и все 4096 LT
назначений для tap/hold/release, соседние и высокие коды под ASan/UBSan.
`caps-word-boundary-results.json` содержит PASS; negative control,
возвращающий только ошибочный оператор, падает на первом held LT:
`caps-word-boundary-negative.json`. FAIL в этом файле ожидаемый и доказывает,
что проверка различает исправленный и прежний обработчик.

## One Shot-only: снятие одного флага не даёт функцию

Отдельная проверка выполнена на более позднем замороженном RC5 snapshot,
включающем Tri Layer и новые оптимизации байтового decoder/машинных
последовательностей. Она не использует базу candidate3 из таблицы выше.
Единственный изменённый негенерируемый вход — `keyboards/ajazz/ak820/config.h`:
снят `NO_ACTION_ONESHOT`, сохранён `NO_ACTION_TAPPING`. Build reports
подтверждают совпадение остальных негенерируемых source hashes.

| Профиль | CODE | XRAM | Максимальный адрес |
|---|---:|---:|---:|
| Оба NO_ACTION ограничения | 38929 | 1975 | `0xC0DC` |
| Снят только NO_ACTION_ONESHOT | 40198 | 1995 | `0xC5CE` |
| Дельта | +1269 | +20 | — |

Оба образа bounded; expanded linker ceiling не использовался. Этот рост
включает One Shot state/housekeeping, а также выход из узкого AK820 decoder:
его guard требует оба NO_ACTION флага. Число не является ценой работающей
One Shot функции. OSM decoder при `NO_ACTION_TAPPING` всё ещё выдаёт
`ACTION_MODS`, а `OP_ONESHOT` в `process_action` появляется только при снятии
обоих ограничений. Наличие исходников One Shot и успешная компиляция
не устанавливают поддержку OSM/OSL.

`oneshot_only.py` выполняет настоящий связанный 8051-код и явно включает
`keymap_config.oneshot_enable` в фикстуре. Четыре characterization сценария
подтверждают наблюдаемое ограничение: OSM действует как удерживаемый Shift,
его tap не меняет следующую A; OSL не включает слой ни на удержании,
ни на следующую клавишу после tap. `_clear_oneshot_mods` присутствует в
образе, `_process_tapping` отсутствует. **4/4 characterization PASS означает
подтверждение fallback, а не PASS работоспособного One Shot.** В production
этот флаг не меняется. Code-size reviewer независимо повторил четыре
сценария и проверил compile guards. Runner требует `_clear_oneshot_mods`
и отклоняет baseline, в котором One Shot state также выключен.

Результаты находятся в `oneshot-only-measurements.json`,
`oneshot-only-characterization.json` и `reports/oneshot-only-*.{json,mem}`.
Точный однострочный feature diff — `oneshot-only-size-and-behavior.patch`.
IHX исследовательского варианта:
`6ef121ee85b5b6a2bbd9c8f68f43c1e7057414a98dd55ffca35b925509c165c8`.

Команда повторного CPU characterization из корня QMK:

```sh
python tests/ak820_tap_state_experiment/oneshot_only.py \
  --build-dir /path/to/oneshot-only-build \
  --s51 /path/to/sdcc-4.4.0/bin/s51 \
  --output-dir /tmp/oneshot-only-characterization
```

Для воспроизведения размера используется та же команда `util/build_ak820.py`
из раздела выше, но без `--code-end 0xf700`. Сначала собрать baseline в новом
каталоге, затем применить только однострочный feature diff в изолированной
копии и собрать в другом новом каталоге. Возврат одного флага не меняет
shared production source.
