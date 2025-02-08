"""Language management for the i18n system."""

from typing import Dict, Optional, List
from .string_provider import StringProvider, DefaultStringProvider
from . import strings_en, strings_es


class Language:
    """Language identifier class."""
    ENGLISH = 'en'
    SPANISH = 'es'


class LanguageManager:
    """Manages language selection and switching."""
    
    def __init__(self):
        """Initialize the language manager."""
        self._providers: Dict[str, StringProvider] = {
            Language.ENGLISH: DefaultStringProvider(strings_en.STRINGS),
            Language.SPANISH: DefaultStringProvider(strings_es.STRINGS),
        }
        self._current_language = Language.ENGLISH
        self._current_provider = self._providers[self._current_language]

    @property
    def current_language(self) -> str:
        """Get the current language code.
        
        Returns:
            str: The current language code (e.g., 'en', 'es')
        """
        return self._current_language

    @property
    def available_languages(self) -> List[str]:
        """Get list of available language codes.
        
        Returns:
            List[str]: List of available language codes
        """
        return list(self._providers.keys())

    def get_string(self, key: str, default: Optional[str] = None, **kwargs) -> str:
        """Get a string in the current language.
        
        Args:
            key (str): The key identifying the string to retrieve
            default (Optional[str]): Default value if key is not found
            **kwargs: Format arguments for the string
            
        Returns:
            str: The localized string
        """
        string = self._current_provider.get_string(key, default)
        if kwargs:
            try:
                return string.format(**kwargs)
            except KeyError:
                return string
        return string

    def switch_language(self, language_code: str) -> bool:
        """Switch to a different language.
        
        Args:
            language_code (str): The language code to switch to
            
        Returns:
            bool: True if switch was successful, False otherwise
        """
        if language_code in self._providers:
            self._current_language = language_code
            self._current_provider = self._providers[language_code]
            return True
        return False 