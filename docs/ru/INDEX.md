English source of truth: [Documentation](../INDEX.md).

# Документация

В английских руководствах описана поддерживаемая работа прошивки. Русские
руководства передают то же самое по-русски. Если тексты расходятся, следуйте
английскому руководству и сообщите о расхождении.

| Задача | Руководство |
| --- | --- |
| Установка, копия и восстановление | [Установка](INSTALL.md) |
| Клавиши, слои, энкодер и RGB | [Настройка](CONFIGURATION.md) |
| Настроить комбинации двух клавиш | [Combo](COMBOS.md) |
| Caps Word, Repeat, Grave Escape и Tri Layer | [Действия клавиш](CONFIGURATION.md) |
| Макросы и эффекты RGB | [Настройка](CONFIGURATION.md) |
| Читать или менять палитру Direct | [Direct](DIRECT.md) |
| Сохранить или восстановить настройки | [Резервные копии](SETTINGS-BACKUP.md) |
| Mod-Tap и Layer-Tap | [Mod-Tap и Layer-Tap](TAP-HOLD.md) |
| Использовать One Shot, Space Cadet и управление NKRO | [Настройка](CONFIGURATION.md) |
| Управлять блокировкой и перестановкой клавиш Win/GUI | [Клавиши Win/GUI](GUI-CONTROL.md) |
| Записывать и воспроизводить компактные динамические макросы | [Динамические макросы](COMPACT-DYNAMIC-MACROS.md) |
| Запускать макрос Vial через клавишу-префикс | [Компактный Leader](COMPACT-LEADER.md) |
| Индикаторы Caps Lock, слоя и OS | [Индикаторы C, W и OS](INDICATORS.md) |
| Переключить Alt и GUI для Mac/PC | [Режим Mac/PC](MAC-PC.md) |
| Сборка закреплённым инструментарием | [Сборка](BUILD.md) |
| Выбрать один из десяти профилей прошивки | [Профили и общие функции](profiles/README.md) |
| Выбрать пакет профиля и собрать его | [Профили сборки](BUILD-PROFILES.md) |
| Сравнить совместимость функций и размер образа | [Матрица модулей](MODULE-MATRIX.md) |
| Прочитать краткие описания функций и ограничений | [Каталог функций](FEATURES.md) |
| Проверка стека и IRQ для образа | [Автономная проверка стека](RUNTIME-STACK.md) |
| Проверки push и выпуск релизов | [CI и выпуски](CI.md) |
| Изменения кода и участие | [Разработка](DEVELOPMENT.md) |
| Офлайн-проверки и устройство | [Проверки](TESTING.md) |
| Опубликованный образ и проверки устройства | [Статус](STATUS.md) |
| Будущие функции | [Планы](ROADMAP.md) |
| Разработка веб- и автономного конфигуратора | [ТЗ и план](../../web/docs/ru/README.md) |
| Назначить действия на нажатие, удержание и двойное нажатие | [Компактный Tap Dance](COMPACT-TAP-DANCE.md) |
| Заменить клавишу при выбранных модификаторах | [Компактные Key Overrides](COMPACT-KEY-OVERRIDES.md) |
| Изменить доступные интервалы и параметры Grave Escape | [QMK Settings](QMK-SETTINGS.md) |
| Подключить хранение и резервные копии модулей | [Хранение модулей](MODULE-STORAGE.md) |
| Определить возможности точного образа разработки | [Каталог разработки](DEVELOPMENT-CATALOG.md) |

Порт предназначен для проводной AJAZZ AK820 с контроллером VS11K28A и USB
`320F:505B`. В AK820 V2, Pro и Max установлено другое оборудование.

Отдельный проект [AK Configurator](https://github.com/dvino/ak-configurator) содержит [требования](https://github.com/dvino/ak-configurator/blob/main/docs/REQUIREMENTS.md) и [план разработки](https://github.com/dvino/ak-configurator/blob/main/docs/PLAN.md).
