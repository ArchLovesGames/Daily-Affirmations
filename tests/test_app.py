import unittest

import app


class AppDataTests(unittest.TestCase):
    def test_affirmation_files_load_for_all_languages(self):
        for language in app.LANGUAGES.values():
            with self.subTest(language=language["code"]):
                affirmations = app.load_affirmations(language["code"])

                self.assertIsNotNone(affirmations)
                self.assertGreater(len(affirmations), 0)

    def test_native_script_fallback_keeps_english_unchanged(self):
        text = "My project demo feels important"

        self.assertEqual(app.apply_native_script_fallback(text, "English"), text)

    def test_native_script_fallback_transliterates_common_words(self):
        hindi_text = app.apply_native_script_fallback("project demo", "हिन्दी")
        telugu_text = app.apply_native_script_fallback("project demo", "తెలుగు")

        self.assertEqual(hindi_text, "प्रोजेक्ट डेमो")
        self.assertEqual(telugu_text, "ప్రాజెక్ట్ డెమో")


if __name__ == "__main__":
    unittest.main()
