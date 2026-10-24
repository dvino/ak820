English source of truth: [Build profiles](../BUILD-PROFILES.md).

# Профили сборки

Конфигуратор содержит 24 именованных профиля разработки. Набор `full`
соответствует функциям опубликованной alpha.3. Каждый новый профиль сохраняет
`full` и добавляет только свой модуль; все три модуля вместе не включаются. Другие профили добавляют Mouse
Keys, Auto Shift, управление GUI, перестановку модификаторов, динамические
макросы, Leader или индикатор OS в сочетаниях ниже. Этим исходникам нужна
собственная проверка точного образа. Каждая сборка сначала доказывает границы
стека основного кода, запуска и прерываний для целого образа, затем запускает
регрессию. Неизвестные границы или переполнение завершают сборку ошибкой.
Текущие проверки приведены в [статусе](STATUS.md).

## Сборка профиля

Запускайте команды из корня репозитория. Выберите профиль и новый каталог
сборки внутри `qmk-8051-ak820`:

```sh
python tools/configure_firmware.py list
python tools/configure_firmware.py build --profile standard \
  --build-dir qmk-8051-ak820/.build/new \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

Можно выбрать любой профиль из списка. Вместо `--profile` используйте
`--features` со списком поддерживаемых названий функций. Допустимы только
сочетания из списка конфигуратора. Три новых профиля модулей требуют
`--short-calls`; этот параметр также нужен двум прежним профилям. Например:

```sh
python tools/configure_firmware.py build --features nkro-control one-shot \
  --build-dir qmk-8051-ak820/.build/nkro-one-shot \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

Профилям `full-mouse-auto-shift-gui`, `full-auto-shift-dynamic-macro`,
`full-tap-dance`, `full-key-overrides` и `full-qmk-settings` нужен параметр
`--short-calls`; по умолчанию он выключен. Для `full` и `full-mouse-auto-shift`
также есть прежние варианты сборки с этим параметром.
Используйте новый каталог сборки:

```sh
python tools/configure_firmware.py build --profile full-mouse-auto-shift-gui \
  --short-calls \
  --build-dir qmk-8051-ak820/.build/full-input \
  --toolchain toolchains/sdcc-4.6.0 \
  --qmk-bin qmk-8051-ak820/.venv/bin/qmk \
  --python qmk-8051-ak820/.venv/bin/python
```

`--profile` и `--features` — альтернативные параметры. Команда `build`
связывает образ, проверяет размещение в обоих окнах CODE и RAM, затем доказывает границы
стека и прерываний точного образа и только после этого запускает обычные
регрессионные проверки и host/CPU-наборы выбранной функции. Неизвестная нужная
граница или переполнение стека завершают сборку ошибкой. В каталоге сборки сохраняются конфигурация, квалификация и
результаты наборов профиля. Эти автономные проверки не подтверждают работу
физической клавиатуры и безопасность выпуска.

Чтобы повторно проверить сборку, выполните:

```sh
python tools/configure_firmware.py inspect --build-dir qmk-8051-ak820/.build/new --toolchain toolchains/sdcc-4.6.0
```

`inspect` заново проверяет размещение ресурсов и идентификатор образа. Чтобы
повторить проверку runtime для готовой сборки, выполните:

```sh
python tools/configure_firmware.py check-runtime \
  --build-dir qmk-8051-ak820/.build/new \
  --toolchain toolchains/sdcc-4.6.0
```

Область и предпосылки описаны в [проверке стека](RUNTIME-STACK.md). Упаковка
разрешена только для точного опубликованного образа alpha.3 и закреплённых
входных данных. Название `full` само по себе не разрешает изменённый образ.
Текущие профили разработки не прошли квалификацию выпуска.

## Профили

Во всех профилях остаются шесть слоёв, 16 макросов Vial с буфером 8192 байта,
восемь двухклавишных Combo с фиксированным адресом `0x658`, компактный tap-hold, карта энкодера, мультимедиа, отчёты NKRO, Caps Word,
Repeat и Alt Repeat, Grave Escape, Tri Layer, RGB-эффекты и VialRGB Direct в
RAM. По умолчанию время Combo — 40 мс, компактного tap-hold — 200 мс.
В `full-qmk-settings` эти значения меняются через QSIDs 2 и 7.
QMK Settings доступны только в `full-qmk-settings` и остаются функцией
исходников для разработки. Только три новых профиля используют схему `0x082003`;
старый формат `0x082002` не меняется. Дополнительные модули выбираются при сборке.

| Профиль | Дополнительные функции |
| --- | --- |
| `standard` | Нет |
| `nkro` | `nkro-control` |
| `one-shot` | `one-shot` |
| `nkro-one-shot` | `nkro-control`, `one-shot` |
| `space-cadet` | `space-cadet` |
| `nkro-space-cadet` | `nkro-control`, `space-cadet` |
| `one-shot-space-cadet` | `one-shot`, `space-cadet` |
| `full` | `nkro-control`, `one-shot`, `space-cadet` |
| `full-leader` | `nkro-control`, `one-shot`, `space-cadet`, компактный Leader |
| `full-mouse` | `nkro-control`, `one-shot`, `space-cadet`, компактные Mouse Keys |
| `full-auto-shift` | `nkro-control`, `one-shot`, `space-cadet`, компактный Auto Shift |
| `full-mouse-auto-shift` | `nkro-control`, `one-shot`, `space-cadet`, компактные Mouse Keys и Auto Shift |
| `full-gui-lock` | `nkro-control`, `one-shot`, `space-cadet`, управление GUI |
| `full-ctrl-gui` | `nkro-control`, `one-shot`, `space-cadet`, управление GUI, перестановка Ctrl/GUI слева и справа |
| `full-os-indicators` | базовые функции `full` и временное управление индикатором OS по FD02 |
| `full-mac-pc` | базовые функции `full` и временная перестановка Alt/GUI слева и справа |
| `full-mac-pc-os-indicators` | `full-mac-pc` и временное управление индикатором OS по FD02 |
| `full-dynamic-macro` | `nkro-control`, `one-shot`, `space-cadet`, компактные динамические макросы |
| `full-dynamic-macro-gui` | `nkro-control`, `one-shot`, `space-cadet`, динамические макросы и управление GUI |
| `full-mouse-auto-shift-gui` | `nkro-control`, `one-shot`, `space-cadet`, Mouse Keys, Auto Shift и управление GUI |
| `full-auto-shift-dynamic-macro` | `nkro-control`, `one-shot`, `space-cadet`, Auto Shift и динамические макросы |
| `full-tap-dance` | `full` и компактный Tap Dance |
| `full-key-overrides` | `full` и компактный Key Overrides |
| `full-qmk-settings` | `full` и типизированные QMK Settings |

`full-leader` запускает существующий макрос Vial: нажмите физическую клавишу
`QK_LEAD`, затем в течение 300 мс одну клавишу выбора. `1`–`9`, `0`, `A`–`F`
соответствуют слотам 0–15. Содержимое макросов редактируется в Vial. Запуск
через энкодер и виртуальные события, длинные последовательности и редактируемый
словарь не реализованы. См. [Leader](COMPACT-LEADER.md).

`full-ctrl-gui` добавляет `CG_SWAP`, `CG_NORM` и `CG_TOGG`. Они меняют
местами вывод левых и правых Ctrl/GUI и сбрасываются после перезапуска.
Преобразование выполняется до блокировки GUI; владельцы модификаторов
сохраняются. Настройка временная и не включает постоянные параметры Magic.
Подробности приведены в разделе [Клавиши Win/GUI](GUI-CONTROL.md).

Управление NKRO включает `NK_ON`, `NK_OFF` и `NK_TOGG`. Режим отчёта
сохраняется до перезапуска; после него используется сохранённый режим или
режим по умолчанию. Переключение очищает удерживаемые клавиши и ожидающие
действия — отпустите клавиши перед повторным нажатием. Записи во flash нет.
Другие действия Magic не включены.

One Shot поддерживает сочетания модификаторов. Нажмите и отпустите OSM, затем
клавишу: модификаторы действуют до отпускания этой клавиши. Можно заранее
набрать несколько модификаторов. Удержание OSM работает как обычный
модификатор. Пока целевая клавиша нажата, новая OSM работает только при
удержании. Работают матричные клавиши и оба направления энкодера. One Shot
для слоёв, тайм-аут, фиксация и tap-toggle отсутствуют. Назначить OSM клавише
через Vial можно; отправить виртуальное событие OSM из Vial или макроса — нет.

Space Cadet назначает `SC_LSPO` на левый Shift при удержании и Shift + `9`
(`(`) при коротком нажатии; `SC_RSPC` — на правый Shift при удержании и Shift
+ `0` (`)`) при коротком нажатии; `SC_SENT` — на правый Shift при удержании и
Enter при коротком нажатии. Эти клавиши используют существующий компактный
tap-hold и его владение модификаторами. Space Cadet нельзя назначить входом
Combo. Полный движок Space Cadet из QMK не включён. Проверенные особенности и ограничения функций приведены в исторической
[матрице компактных функций](../../audits/rc6/compact-runtime-20261024/final/README.md). Предыдущий точный образ и его доказательства описаны в [техническом отчёте](../../audits/rc6/leader-next-20261024/final/README.md); они не подтверждают изменённые профили.

Ресурсы зависят от полного связанного образа. Измеряйте каждый профиль по его
отчёту: затраты функций не складываются. Для точного опубликованного образа alpha.3 `full` проверка ограничивает стек
основного пути 93 байтами, CRT — 2 байтами, трёх IRQ-путей вместе — 61 байтом.
Всего используется 156 из 162 байт, запас — 6 байт. Эти числа относятся только к точному опубликованному образу alpha.3. Для
каждого профиля изменённых исходников нужны отдельные доказательства стека и
IRQ. `check-runtime` повторяет проверку существующей сборки; она не подтверждает
установленный образ или выпуск. См. [предыдущую границу runtime](../../audits/rc6/leader-next-20261024/final/README.md), текущую [квалификацию точных образов](../../audits/rc6/web-firmware-20261024/runtime-all/README.md) и [статус](STATUS.md).

## Оставшиеся ограничения

Три компактных модуля доступны только в указанных профилях разработки и не одобрены для выпуска. Каждый профиль добавляет свой модуль к `full`; сочетания всех трёх модулей нет. Точное поведение, ограничения входов, хранения и протокола описаны в руководствах [Tap Dance](COMPACT-TAP-DANCE.md), [Key Overrides](COMPACT-KEY-OVERRIDES.md), [QMK Settings](QMK-SETTINGS.md) и [хранение модулей](MODULE-STORAGE.md).

Поддержка Magic ограничена временными командами GUI и перестановкой Ctrl/GUI или Alt/GUI в отдельных профилях. Варианты Caps и постоянные настройки Magic не входят в текущий контракт модулей. См. [управление GUI](GUI-CONTROL.md) и [режим Mac/PC](MAC-PC.md). Console и Command отключены.
