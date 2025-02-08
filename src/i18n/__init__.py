"""Initialization module for the i18n system."""

from .string_provider import StringProvider
from .language_manager import LanguageManager, Language

# Global language manager instance
_manager = LanguageManager()


def get_string(key: str, default: str = None, **kwargs) -> str:
    """Get a localized string.
    
    Args:
        key (str): The key identifying the string to retrieve
        default (str, optional): Default value if key is not found
        **kwargs: Format arguments for the string
        
    Returns:
        str: The localized string
    """
    return _manager.get_string(key, default, **kwargs)


def get_current_language() -> str:
    """Get the current language code.
    
    Returns:
        str: The current language code (e.g., 'en', 'es')
    """
    return _manager.current_language


def get_available_languages() -> list[str]:
    """Get list of available language codes.
    
    Returns:
        list[str]: List of available language codes
    """
    return _manager.available_languages


def switch_language(language_code: str) -> bool:
    """Switch to a different language.
    
    Args:
        language_code (str): The language code to switch to
        
    Returns:
        bool: True if switch was successful, False otherwise
    """
    return _manager.switch_language(language_code)


# For backward compatibility
def set_string_provider(provider: StringProvider) -> None:
    """Set a custom string provider (deprecated).
    
    This method is kept for backward compatibility with tests.
    New code should use switch_language() instead.
    
    Args:
        provider (StringProvider): The string provider to use
    """
    global _manager
    _manager = LanguageManager()
    _manager._current_provider = provider  # type: ignore 