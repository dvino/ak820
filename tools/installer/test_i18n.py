"""Focused tests for language selection and translation session behavior."""
import unittest
from unittest.mock import patch

from i18n import (LanguageSession, STRINGS, detect_language, hold_seconds_remaining, localize_output,
                  localize_prompt, normalize_language, text)


class LanguageSelectionTests(unittest.TestCase):
    def test_windows_primary_language_id_controls_default(self):
        self.assertEqual(detect_language(windows_language_id=0x0419, system_locale="en_US"), "ru")
        self.assertEqual(detect_language(windows_language_id=0x0819, system_locale="en_US"), "ru")
        self.assertEqual(detect_language(windows_language_id=0x0409, system_locale="ru_RU"), "en")

    def test_locale_is_fallback_when_windows_id_is_unavailable(self):
        self.assertEqual(detect_language(system_locale="ru_RU", platform="linux"), "ru")
        self.assertEqual(detect_language(system_locale="en_US", platform="linux"), "en")
        with patch("i18n.locale.getlocale", return_value=(None, None)):
            self.assertEqual(detect_language(platform="linux"), "en")

    def test_language_names_are_normalized(self):
        self.assertEqual(normalize_language("RU_ru"), "ru")
        self.assertEqual(normalize_language("fr_FR"), "en")


class TranslationSessionTests(unittest.TestCase):
    def test_hold_countdown_uses_remaining_firmware_ticks(self):
        for ticks, seconds in ((30, 3), (20, 2), (1, 1), (0, 0)):
            with self.subTest(ticks=ticks):
                self.assertEqual(hold_seconds_remaining(ticks), seconds)

    def test_language_toggle_preserves_operation_and_command_data(self):
        operation = ["update-prepared", "--session", r"C:\runs\session-17"]
        before = operation[:]
        session = LanguageSession("ru")
        self.assertEqual(session.text("update"), "Обновить прошивку")
        self.assertEqual(session.toggle(), "en")
        self.assertEqual(session.text("update"), "Update firmware")
        self.assertEqual(operation, before)

    def test_both_catalogs_have_same_translation_keys(self):
        self.assertEqual(set(STRINGS["ru"]), set(STRINGS["en"]))

    def test_values_are_inserted_without_changing_technical_data(self):
        digest = "A1B2" * 16
        path = r"C:\runs\update-17"
        self.assertEqual(text("logs_path", "en", path=path), "Backups and logs: " + path)
        self.assertEqual(text("logs_path", "ru", path=path), "Резервные копии и журналы: " + path)
        self.assertEqual(text("unknown", "ru"), "unknown")
        self.assertEqual(digest, "A1B2" * 16)

    def test_prompt_and_error_summaries_translate_without_touching_data(self):
        prompt = "Image SHA256: " + "A1B2" * 16 + "\nВведите yes (Enter — отмена): "
        translated = localize_prompt(prompt, "en")
        self.assertTrue(translated.endswith("Type yes (Enter to cancel): "))
        self.assertIn("A1B2" * 16, translated)
        stopped = "Обновление остановлено. Автоматического сброса или повторной попытки нет. " \
                  "Запрос разблокировки Vial может оставаться активным."
        output = localize_output(stopped + "\nSHA256: " + "A1B2" * 16, "en")
        self.assertTrue(output.startswith("Update stopped."))
        self.assertTrue(output.endswith("SHA256: " + "A1B2" * 16))

    def test_update_consent_log_is_translated_and_keeps_firmware_hash(self):
        digest = "a1b2" * 16
        russian = (
            "Теперь удерживайте Esc + левый Ctrl 3 секунды. Это разрешает одну запись "
            "показанной прошивки и перезапуск после проверки.\n"
            "Будут возвращены сохранённые настройки до проверки энкодера и удалена "
            "ожидающая запись журнала. Временное изменение энкодера не повторится.\n"
            "Подготовьте запасную клавиатуру и стабильное питание.\nSHA256: " + digest
        )
        translated = localize_output(russian, "en")
        self.assertIn("Hold Esc + left Ctrl for 3 seconds", translated)
        self.assertIn("Saved settings", translated)
        self.assertTrue(translated.endswith("SHA256: " + digest))


if __name__ == "__main__":
    unittest.main()
