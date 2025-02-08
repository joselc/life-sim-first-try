"""Tests for the i18n system."""

import unittest
from src.i18n.string_provider import StringProvider, DefaultStringProvider
from src.i18n.language_manager import Language
from src import i18n


class MockStringProvider(StringProvider):
    """Mock string provider for testing."""
    def get_string(self, key: str, default: str = None) -> str:
        return f"MOCK_{key}"


class TestStringProvider(unittest.TestCase):
    """Test cases for the string provider system."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_strings = {
            'test.key': 'Test Value',
            'test.format': 'Value: {value}',
        }
        self.provider = DefaultStringProvider(self.test_strings)

    def test_get_existing_string(self):
        """Test retrieving an existing string."""
        result = self.provider.get_string('test.key')
        self.assertEqual(result, 'Test Value')

    def test_get_missing_string_with_default(self):
        """Test retrieving a missing string with a default value."""
        result = self.provider.get_string('missing.key', default='Default')
        self.assertEqual(result, 'Default')

    def test_get_missing_string_without_default(self):
        """Test retrieving a missing string without a default value."""
        result = self.provider.get_string('missing.key')
        self.assertEqual(result, 'missing.key')


class TestI18N(unittest.TestCase):
    """Test cases for the i18n module functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Store initial language
        self.initial_language = i18n.get_current_language()

    def test_get_string_basic(self):
        """Test basic string retrieval."""
        result = i18n.get_string('state.paused')
        self.assertEqual(result, 'PAUSED')

    def test_get_string_with_format(self):
        """Test string retrieval with format arguments."""
        result = i18n.get_string('state.speed', speed='1.5')
        self.assertEqual(result, 'Speed: 1.5x')

    def test_get_string_with_invalid_format(self):
        """Test string retrieval with invalid format arguments."""
        # Should return unformatted string if format args don't match
        result = i18n.get_string('state.paused', invalid_arg='value')
        self.assertEqual(result, 'PAUSED')

    def test_get_string_missing(self):
        """Test retrieval of missing string."""
        result = i18n.get_string('nonexistent.key')
        self.assertEqual(result, 'nonexistent.key')

    def test_get_string_with_default(self):
        """Test retrieval with default value."""
        result = i18n.get_string('nonexistent.key', default='Default Value')
        self.assertEqual(result, 'Default Value')

    def test_language_switching(self):
        """Test switching between languages."""
        # Test switching to Spanish
        i18n.switch_language(Language.SPANISH)
        self.assertEqual(i18n.get_current_language(), Language.SPANISH)
        
        # Check a Spanish string
        paused_es = i18n.get_string('state.paused')
        self.assertEqual(paused_es, 'PAUSADO')
        
        # Switch back to English
        i18n.switch_language(Language.ENGLISH)
        self.assertEqual(i18n.get_current_language(), Language.ENGLISH)
        
        # Check the same string in English
        paused_en = i18n.get_string('state.paused')
        self.assertEqual(paused_en, 'PAUSED')

    def test_available_languages(self):
        """Test getting available languages."""
        languages = i18n.get_available_languages()
        self.assertIn(Language.ENGLISH, languages)
        self.assertIn(Language.SPANISH, languages)
        self.assertEqual(len(languages), 2)

    def test_invalid_language_switch(self):
        """Test switching to an invalid language."""
        initial_lang = i18n.get_current_language()
        success = i18n.switch_language('invalid_code')
        self.assertFalse(success)
        self.assertEqual(i18n.get_current_language(), initial_lang)

    def test_format_consistency_across_languages(self):
        """Test that string formatting works consistently across languages."""
        # Test in English
        i18n.switch_language(Language.ENGLISH)
        speed_en = i18n.get_string('state.speed', speed='2.0')
        self.assertIn('2.0', speed_en)
        
        # Test in Spanish
        i18n.switch_language(Language.SPANISH)
        speed_es = i18n.get_string('state.speed', speed='2.0')
        self.assertIn('2.0', speed_es)
        
        # Strings should be different but both contain the value
        self.assertNotEqual(speed_en, speed_es)

    def test_set_string_provider_compatibility(self):
        """Test backward compatibility of set_string_provider."""
        mock_provider = MockStringProvider()
        i18n.set_string_provider(mock_provider)
        
        result = i18n.get_string('test.key')
        self.assertEqual(result, 'MOCK_test.key')

    def tearDown(self):
        """Clean up after each test method."""
        # Restore initial language
        i18n.switch_language(self.initial_language)


if __name__ == '__main__':
    unittest.main() 