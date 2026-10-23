"""Small, dependency-free translations for the installer interface."""
from __future__ import annotations

import ctypes
import locale
import re
import sys


STRINGS = {
    "ru": {
        "language_button": "English",
        "title": "AK820 — обновление прошивки",
        "instructions": (
            "1. Выберите личную папку подготовленного обновления.\n"
            "2. Нажмите «Обновить прошивку». После проверки удерживайте Esc + левый Ctrl 3 секунды.\n"
            "3. Это разрешит запись показанной прошивки. Программа сама запишет её и проверит результат.\n"
            "Подготовьте запасную клавиатуру и стабильное питание. Ничего не запускается автоматически."
        ),
        "logs_path": "Резервные копии и журналы: {path}",
        "ready": "Готово к выбору действия. Клавиатура ещё не проверялась.",
        "update_folder": "Папка обновления:",
        "choose_folder": "Выбрать папку…",
        "choose_session_title": "Выберите личную папку обновления с images.json",
        "oem_folder": "Свои файлы OEM (необязательно):",
        "choose_oem_title": "Выберите папку со своими stock-full.bin и native-installed.bin",
        "oem_note": "Файлы OEM не входят в комплект и не скачиваются. При установке из OEM программа читает полную личную копию с вашей клавиатуры.",
        "checking": "Выполняется проверка. Не отключайте клавиатуру.",
        "update": "Обновить прошивку",
        "cancel_wait": "Отменить ожидание",
        "other_actions": "Другие действия — установка из OEM и восстановление",
        "verify_package": "Проверить пакет без USB",
        "find_keyboard": "Найти клавиатуру",
        "backup_oem": "Сохранить резервную копию OEM",
        "install_oem": "Установить из OEM",
        "restore_oem": "Восстановить OEM…",
        "recover_title": "Выберите личную папку установки или восстановления",
        "prepare_prompt_title": "AK820 — подготовка",
        "confirm_write_title": "AK820 — подтверждение записи",
        "confirm_instruction": "Подтвердите действие указанным словом. Пустой ответ отменяет действие.\n\n{message}",
        "yes_entry_label": "Введите в поле ниже:",
        "yes_confirm": "Подтвердить",
        "cancel": "Отмена",
        "yes_title": "AK820 — подтверждение записи",
        "action_running_title": "AK820 — действие выполняется",
        "wait_for_completion": "Дождитесь завершения действия. До записи можно отменить запрос или ожидание загрузчика. Во время записи не отключайте клавиатуру.",
        "completed": "Завершено. Код: {code}. Результаты проверок — в журнале ниже.",
        "loader_wait": "Ожидание загрузчика — до 25 секунд.",
        "prompt_cancelled": "Действие отменено.",
        "stopped_error": "Остановлено: {error}",
        "prompt_prepare": "Перед подготовкой проверьте подключённую клавиатуру.",
        "prompt_update_unlock": "На клавиатуре удерживайте Esc + левый Ctrl в течение 3 секунд. Это подтверждает показанное обновление. Дождитесь перехода в загрузчик.",
        "prompt_update_unlock_hash": "Удерживайте Esc + левый Ctrl 3 секунды, чтобы подтвердить одну запись этой прошивки и перезапуск после проверки. SHA256 прошивки: {sha256}. Перед проверкой энкодера будут восстановлены сохранённые настройки и удалена ожидающая запись журнала. Временное изменение энкодера не повторится. Подготовьте запасную клавиатуру и стабильное питание.",
        "hold_remaining": "Продолжайте удерживать клавиши ещё {seconds} с.",
        "prompt_loader": "Переход в загрузчик. Не отключайте клавиатуру.",
        "prompt_loader_detected": "Загрузчик найден. Сейчас начнётся запись и проверка.",
        "prompt_flashing": "Идёт запись прошивки и проверка результата. Не отключайте клавиатуру.",
        "prompt_update_complete": "Обновление завершено; результат проверки показан в журнале.",
    },
    "en": {
        "language_button": "Русский",
        "title": "AK820 firmware update",
        "instructions": (
            "1. Choose your prepared update folder.\n"
            "2. Click Update firmware. After the checks, hold Esc + left Ctrl for 3 seconds.\n"
            "3. This confirms the displayed firmware. The installer flashes it once and verifies the result.\n"
            "Prepare a spare keyboard and stable power. Nothing starts automatically."
        ),
        "logs_path": "Backups and logs: {path}",
        "ready": "Ready. The keyboard has not been checked yet.",
        "update_folder": "Update folder:",
        "choose_folder": "Choose folder…",
        "choose_session_title": "Choose your prepared update folder containing images.json",
        "oem_folder": "Your OEM files (optional):",
        "choose_oem_title": "Choose the folder containing your stock-full.bin and native-installed.bin",
        "oem_note": "OEM files are not included or downloaded. OEM installation reads a full personal copy from your keyboard.",
        "checking": "Checking. Do not disconnect the keyboard.",
        "update": "Update firmware",
        "cancel_wait": "Cancel waiting",
        "other_actions": "Other actions — OEM installation and recovery",
        "verify_package": "Verify package without USB",
        "find_keyboard": "Find keyboard",
        "backup_oem": "Save OEM backup",
        "install_oem": "Install from OEM",
        "restore_oem": "Restore OEM…",
        "recover_title": "Choose your personal installation or recovery folder",
        "prepare_prompt_title": "AK820 — preparation",
        "confirm_write_title": "AK820 — write confirmation",
        "confirm_instruction": "Confirm the action with the requested word. An empty response cancels it.\n\n{message}",
        "yes_entry_label": "Type the word below:",
        "yes_confirm": "Confirm",
        "cancel": "Cancel",
        "yes_title": "AK820 — write confirmation",
        "action_running_title": "AK820 — action in progress",
        "wait_for_completion": "Wait for the action to finish. Before writing, you can cancel the request or loader wait. Do not disconnect the keyboard while it is being written.",
        "completed": "Finished. Code: {code}. Check results in the log below.",
        "loader_wait": "Waiting for the bootloader — up to 25 seconds.",
        "prompt_cancelled": "Action cancelled.",
        "stopped_error": "Stopped: {error}",
        "prompt_prepare": "Check the connected keyboard before preparation.",
        "prompt_update_unlock": "On the keyboard, hold Esc + left Ctrl for 3 seconds. This confirms the displayed update. Wait for the bootloader.",
        "prompt_update_unlock_hash": "Hold Esc + left Ctrl for 3 seconds to authorize one write of this firmware and a restart after verification. Firmware SHA256: {sha256}. Saved settings from before the encoder check will be restored and its pending journal entry removed. The temporary encoder change will not be replayed. Prepare a spare keyboard and stable power.",
        "hold_remaining": "Keep holding for {seconds} more seconds.",
        "prompt_loader": "Entering the bootloader. Do not disconnect the keyboard.",
        "prompt_loader_detected": "Bootloader found. Flashing and verification are starting.",
        "prompt_flashing": "Firmware is being flashed and verified. Do not disconnect the keyboard.",
        "prompt_update_complete": "Update complete; the verification result is shown in the log.",
    },
}


def normalize_language(language: str | None) -> str:
    """Return the supported language code, defaulting to English."""
    return "ru" if (language or "").lower().replace("_", "-").startswith("ru") else "en"


def hold_seconds_remaining(counter: int) -> int:
    """Convert the firmware's remaining 100 ms ticks to whole seconds."""
    return max(0, (int(counter) + 9) // 10)


def detect_language(*, windows_language_id=None, system_locale=None, platform=None) -> str:
    """Select Russian only for Russian Windows UI; use locale as a fallback."""
    platform = sys.platform if platform is None else platform
    if windows_language_id is None and platform == "win32":
        try:
            windows_language_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        except (AttributeError, OSError):
            windows_language_id = None
    if windows_language_id is not None:
        return "ru" if int(windows_language_id) & 0x3FF == 0x19 else "en"
    if system_locale is None:
        try:
            system_locale = locale.getlocale()[0]
        except (ValueError, TypeError):
            system_locale = None
    return normalize_language(system_locale)


def text(key: str, language: str = "en", **values) -> str:
    """Translate a UI string; unknown strings remain intact as data."""
    catalog = STRINGS[normalize_language(language)]
    template = catalog.get(key)
    if template is None:
        template = STRINGS["en"].get(key, key)
    return template.format(**values) if values else template


def localize_prompt(message: str, language: str) -> str:
    """Translate only known UI wording; leave the supplied operation context intact."""
    if normalize_language(language) == "en":
        message = message.replace("Введите yes (Enter — отмена): ", "Type yes (Enter to cancel): ")
    return message


def localize_output(message: str, language: str) -> str:
    """Translate a known error summary without altering technical log data."""
    if normalize_language(language) == "en":
        consent_instructions = (
            "Hold Esc + left Ctrl for 3 seconds to authorize one write of the displayed firmware "
            "and a restart after verification.\n"
            "Saved settings from before the encoder check will be restored and its pending journal "
            "entry removed. The temporary encoder change will not be replayed.\n"
            "Prepare a spare keyboard and stable power.\nSHA256: "
        )
        message = re.sub(
            r"Теперь удерживайте Esc \+ левый Ctrl 3 секунды\. Это разрешает одну запись "
            r"показанной прошивки и перезапуск после проверки\.\n"
            r"Будут возвращены сохранённые настройки до проверки энкодера и удалена "
            r"ожидающая запись журнала\. Временное изменение энкодера не повторится\.\n"
            r"Подготовьте запасную клавиатуру и стабильное питание\.\nSHA256: ",
            consent_instructions,
            message,
        )
        replacements = {
            "Обновление остановлено. Автоматического сброса или повторной попытки нет. Запрос разблокировки Vial может оставаться активным.":
                "Update stopped. No automatic reset or retry will be attempted. The Vial unlock request may remain active.",
            "Ожидание физического подтверждения отменено": "Physical confirmation wait cancelled",
            "Ожидание отменено до записи прошивки": "Wait cancelled before firmware writing",
            "Запись отменена до начала прошивки": "Writing cancelled before firmware flashing",
            "Запись отменена до стирания прошивки": "Writing cancelled before firmware erase",
            "Обновление отменено до следующей команды": "Update cancelled before the next command",
            "Рабочая папка:": "Session folder:",
            "Диагностический архив:": "Diagnostic archive:",
        }
        for original, translated in replacements.items():
            message = message.replace(original, translated)
    return message


class LanguageSession:
    """Language choice for one run; switching does not touch action arguments."""
    def __init__(self, language: str | None = None):
        self.language = normalize_language(language or detect_language())

    def toggle(self) -> str:
        self.language = "en" if self.language == "ru" else "ru"
        return self.language

    def text(self, key: str, **values) -> str:
        return text(key, self.language, **values)

    def status(self, event_key: str, **values) -> str:
        """Render a semantic progress key while retaining any supplied data."""
        return self.text(event_key, **values)
