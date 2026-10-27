# AK820 v0.6.0-beta.3

- Two-key Combos can toggle Caps Word, for example A + S. The input letters are suppressed; repeating the Combo turns Caps Word off.
- Layer-Tap can run a saved Vial macro on a short press and activate a layer while held. This allows a Caps key to switch layout on tap and use A for Caps Word on the held layer. The macro form supports layers 0–5 and saved macros 0–15 on physical keys.
- The profile catalog retains ten choices, including `main`. Settings can move from earlier beta.2 images through the supported forward transitions. Earlier firmware cannot use the new macro Layer-Tap codes.
- `main` adds Auto Shift and does not include GUI lock; `typing` keeps Auto Shift.
- VialRGB Direct can read a coherent 82-color HSV8 palette and apply a complete frame. Palette data remains in RAM; the protocol does not enable or select RGB and does not save EEPROM. Upload brightness is limited to 160.
- In `game` and `mmo`, GUI lock starts off and makes W pulse on a 2000 ms cycle while active. A nonbase active or default layer lights W steadily instead.

The companion application remains in development. The macro Layer-Tap form requires an editor that accepts numeric keycodes. Only the matching wired AJAZZ AK820 with a VS11K28A controller is supported; V2, Pro and Max are excluded.

## Русский

- Комбинации двух клавиш переключают Caps Word, например A + S. Входные буквы не печатаются; повторное сочетание выключает Caps Word.
- Layer-Tap запускает сохранённый макрос Vial по короткому нажатию и включает слой при удержании. Так Caps может переключать раскладку по нажатию, а A на удерживаемом слое — переключать Caps Word. Макросный вариант поддерживает слои 0–5 и сохранённые макросы 0–15 на физических клавишах.
- В каталоге остаются десять профилей, включая `main`. Настройки из прежних образов beta.2 переносятся по поддерживаемым переходам вперёд. Старые прошивки не поддерживают новые коды макросного Layer-Tap.
- В `main` добавлен Auto Shift, блокировки GUI в нём нет; в `typing` Auto Shift сохраняется.
- VialRGB Direct читает согласованную палитру из 82 цветов HSV8 и применяет полный кадр. Палитра хранится только в RAM; протокол не включает RGB, не выбирает режим и не сохраняет данные в EEPROM. Яркость при передаче ограничена значением 160.
- В `game` и `mmo` блокировка GUI по умолчанию выключена; при её включении W пульсирует с циклом 2000 мс. Активный или начальный слой выше 0 включает постоянный свет W.

Приложение-компаньон пока разрабатывается. Для макросного Layer-Tap нужен редактор с вводом числовых кодов. Поддерживается только соответствующая проводная AJAZZ AK820 с VS11K28A; V2, Pro и Max не поддерживаются.
