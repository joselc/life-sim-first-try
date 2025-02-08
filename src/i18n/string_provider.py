"""String provider interface and implementations for i18n support."""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class StringProvider(ABC):
    """Interface for providing localized strings."""

    @abstractmethod
    def get_string(self, key: str, default: Optional[str] = None) -> str:
        """Get a localized string for the given key.
        
        Args:
            key (str): The key identifying the string to retrieve
            default (Optional[str]): Default value if key is not found
            
        Returns:
            str: The localized string
        """
        pass


class DefaultStringProvider(StringProvider):
    """Default implementation of StringProvider using a dictionary."""
    
    def __init__(self, strings: Dict[str, str]):
        """Initialize with a dictionary of strings.
        
        Args:
            strings (Dict[str, str]): Dictionary mapping keys to strings
        """
        self._strings = strings

    def get_string(self, key: str, default: Optional[str] = None) -> str:
        """Get a string from the dictionary.
        
        Args:
            key (str): The key identifying the string to retrieve
            default (Optional[str]): Default value if key is not found
            
        Returns:
            str: The string value
        """
        return self._strings.get(key, default if default is not None else key) 