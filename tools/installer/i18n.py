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
            "1. Выберите OEM-сессию восстановления и папку для новой копии настроек.\n"
            "2. Нажмите «Обновить прошивку». После проверки удерживайте Esc + левый Ctrl 3 секунды.\n"
            "3. Установщик сохранит настройки, запишет одну проверенную прошивку и восстановит настройки.\n"
            "После перезапуска для восстановления макросов потребуется ещё одно физическое подтверждение.\n"
            "Подготовьте запасную клавиатуру и стабильное питание. Ничего не запускается автоматически."
        ),
        "logs_path": "Резервные копии и журналы: {path}",
        "ready": "Готово к выбору действия. Клавиатура ещё не проверялась.",
        "update_folder": "Исходная сессия OEM-восстановления:",
        "backup_output": "Папка для копии настроек:",
        "restore_backup": "Копия настроек для восстановления:",
        "choose_output_title": "Выберите папку для новой копии настроек",
        "choose_backup_title": "Выберите папку резервной копии настроек",
        "backup": "Сохранить настройки…",
        "restore": "Восстановить настройки…",
        "backup_scope": "Копия включает сохранённые настройки, которые можно прочитать и восстановить. Поля текущей RAM без способа чтения будут перечислены в отчёте.",
        "backup_target": "Новая копия будет сохранена сюда: {path}",
        "update_backup_target": "Свежая копия для обновления будет сохранена сюда: {path}",
        "choose_folder": "Выбрать папку…",
        "choose_session_title": "Выберите исходную OEM-сессию восстановления с images.json и before-full-rom.bin",
        "choose_prepared_update_title": "Выберите старую подготовленную папку обновления RC6",
        "oem_folder": "Свои файлы OEM (необязательно):",
        "choose_oem_title": "Выберите папку со своими stock-full.bin и native-installed.bin",
        "oem_note": "Файлы OEM не входят в комплект и не скачиваются. При установке из OEM программа читает полную личную копию с вашей клавиатуры.",
        "checking": "Выполняется проверка. Не отключайте клавиатуру.",
        "update": "Обновить прошивку",
        "cancel_wait": "Отменить ожидание",
        "physical_unlock_title": "Физическое подтверждение",
        "physical_unlock_update": "На подключённой клавиатуре удерживайте Esc + левый Ctrl 3 секунды, чтобы разрешить показанное обновление. Отмена ожидания остановит операцию до следующего изменения.",
        "physical_unlock_restore": "Для восстановления защищённых настроек требуется новая физическая разблокировка Vial. На подключённой клавиатуре удерживайте Esc + левый Ctrl 3 секунды, чтобы разрешить восстановление макросов и защищённых клавиш.",
        "backup_stage": "Чтение и проверка настроек перед сохранением копии…",
        "preflight_stage": "Проверка устройства, копии и целевой прошивки…",
        "restore_stage": "Восстановление сохранённых настроек…",
        "verify_stage": "Проверка настроек после восстановления…",
        "complete_stage": "Операция завершена; итог проверки приведён в журнале.",
        "other_actions": "Другие действия — установка из OEM и восстановление",
        "verify_package": "Проверить пакет без USB",
        "find_keyboard": "Найти клавиатуру",
        "backup_oem": "Сохранить резервную копию OEM",
        "install_oem": "Установить из OEM",
        "restore_oem": "Восстановить OEM…",
        "legacy_update": "Старое обновление RC6 — только для расширенного сценария",
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
            "1. Choose an OEM recovery session and a folder for the new settings backup.\n"
            "2. Click Update firmware. After checks, hold Esc + left Ctrl for 3 seconds.\n"
            "3. The installer saves settings, flashes one approved firmware image, then restores the settings.\n"
            "After restart, a second physical confirmation is needed to restore macros.\n"
            "Prepare a spare keyboard and stable power. Nothing starts automatically."
        ),
        "logs_path": "Backups and logs: {path}",
        "ready": "Ready. The keyboard has not been checked yet.",
        "update_folder": "Original OEM recovery session:",
        "backup_output": "Settings backup output folder:",
        "restore_backup": "Settings backup to restore:",
        "choose_output_title": "Choose a folder for a new settings backup",
        "choose_backup_title": "Choose a settings backup folder",
        "backup": "Back up settings…",
        "restore": "Restore settings…",
        "backup_scope": "The backup contains saved settings that can be read and restored. Current RAM fields with no read method will be listed in the report.",
        "backup_target": "New backup will be saved here: {path}",
        "update_backup_target": "Fresh backup for the update will be saved here: {path}",
        "choose_folder": "Choose folder…",
        "choose_session_title": "Choose your original OEM recovery session containing images.json and before-full-rom.bin",
        "choose_prepared_update_title": "Choose the legacy prepared RC6 update folder",
        "oem_folder": "Your OEM files (optional):",
        "choose_oem_title": "Choose the folder containing your stock-full.bin and native-installed.bin",
        "oem_note": "OEM files are not included or downloaded. OEM installation reads a full personal copy from your keyboard.",
        "checking": "Checking. Do not disconnect the keyboard.",
        "update": "Update firmware",
        "cancel_wait": "Cancel waiting",
        "physical_unlock_title": "Physical confirmation",
        "physical_unlock_update": "On the connected keyboard, hold Esc + left Ctrl for 3 seconds to authorize the displayed update. Cancelling this wait stops the operation before the next change.",
        "physical_unlock_restore": "Restoring protected settings requires a fresh physical Vial unlock. On the connected keyboard, hold Esc + left Ctrl for 3 seconds to authorize restoring macros and protected keys.",
        "backup_stage": "Reading and checking settings before saving the backup…",
        "preflight_stage": "Checking the device, backup and target firmware…",
        "restore_stage": "Restoring saved settings…",
        "verify_stage": "Checking settings after restoration…",
        "complete_stage": "Operation complete; the verification result is in the log.",
        "other_actions": "Other actions — OEM installation and recovery",
        "verify_package": "Verify package without USB",
        "find_keyboard": "Find keyboard",
        "backup_oem": "Save OEM backup",
        "install_oem": "Install from OEM",
        "restore_oem": "Restore OEM…",
        "legacy_update": "Legacy RC6 update — advanced use only",
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


def progress_text(stage: str, data: dict | None, language: str) -> tuple[str, str]:
    """Render shared installer progress stages as GUI instruction and status."""
    values = data if isinstance(data, dict) else {}
    if stage in ("unlock_wait", "restore_unlock_wait"):
        if stage == "unlock_wait" and values.get("purpose") not in ("update", "restore"):
            instruction = text("prompt_update_unlock_hash", language,
                               sha256=values.get("sha256", ""))
            return instruction, text("hold_remaining", language,
                                     seconds=hold_seconds_remaining(values.get("counter", 0)))
        restoring = stage == "restore_unlock_wait" or values.get("purpose") == "restore"
        instruction = text("physical_unlock_restore" if restoring else "physical_unlock_update", language)
        digest = values.get("sha256")
        if digest:
            instruction += "\nSHA256: " + str(digest)
        return instruction, text("hold_remaining", language,
                                 seconds=hold_seconds_remaining(values.get("counter", 0)))
    stage_keys = {
        "backup": "backup_stage",
        "preflight": "preflight_stage",
        "loader_wait": "prompt_loader",
        "loader_detected": "prompt_loader_detected",
        "flashing": "prompt_flashing",
        "restoring": "restore_stage",
        "verifying": "verify_stage",
        "complete": "complete_stage",
    }
    key = stage_keys.get(stage)
    if key:
        rendered = text(key, language)
        return rendered, rendered
    message = str(values.get("message", stage))
    return message, message


def needs_unlock_dialog(stage: str, data: dict | None) -> bool:
    """Only the new backup/update/restore workflow uses the modal unlock dialog."""
    values = data if isinstance(data, dict) else {}
    return (stage == "restore_unlock_wait" or
            (stage == "unlock_wait" and values.get("purpose") in ("update", "restore")))


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
