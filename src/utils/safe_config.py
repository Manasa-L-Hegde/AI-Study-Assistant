"""
Safe configuration access utilities.
Provides fallback mechanisms to prevent AttributeError crashes.
"""

from typing import Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_getattr(obj: Any, attr: str, default: Any = None, log_missing: bool = True) -> Any:
    """
    Safely get an attribute from an object with fallback.
    
    Args:
        obj: Object to get attribute from
        attr: Attribute name
        default: Default value if attribute doesn't exist
        log_missing: Whether to log missing attributes
    
    Returns:
        Attribute value or default
    """
    try:
        value = getattr(obj, attr, default)
        if value is None and default is not None:
            if log_missing:
                logger.warning(f"Attribute '{attr}' not found on {type(obj).__name__}, using default: {default}")
            return default
        return value
    except Exception as e:
        if log_missing:
            logger.error(f"Error accessing attribute '{attr}': {e}")
        return default


def safe_dict_get(dictionary: dict, key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary with fallback.
    
    Args:
        dictionary: Dictionary to get value from
        key: Key name
        default: Default value if key doesn't exist
    
    Returns:
        Value or default
    """
    try:
        return dictionary.get(key, default)
    except Exception as e:
        logger.error(f"Error accessing key '{key}': {e}")
        return default


class SafeConfig:
    """Wrapper for safe configuration access."""
    
    def __init__(self, config_obj: Any):
        """
        Initialize safe config wrapper.
        
        Args:
            config_obj: Configuration object to wrap
        """
        self._config = config_obj
    
    def get(self, attr: str, default: Any = None) -> Any:
        """
        Get configuration attribute safely.
        
        Args:
            attr: Attribute name (supports dot notation like 'features.enable_dark_mode')
            default: Default value
        
        Returns:
            Attribute value or default
        """
        try:
            # Handle dot notation
            if '.' in attr:
                parts = attr.split('.')
                obj = self._config
                for part in parts:
                    obj = safe_getattr(obj, part, default, log_missing=False)
                    if obj is None or obj == default:
                        return default
                return obj
            else:
                return safe_getattr(self._config, attr, default)
        except Exception as e:
            logger.error(f"Error getting config '{attr}': {e}")
            return default
    
    def has(self, attr: str) -> bool:
        """
        Check if configuration has an attribute.
        
        Args:
            attr: Attribute name
        
        Returns:
            True if attribute exists, False otherwise
        """
        try:
            if '.' in attr:
                parts = attr.split('.')
                obj = self._config
                for part in parts:
                    if not hasattr(obj, part):
                        return False
                    obj = getattr(obj, part)
                return True
            else:
                return hasattr(self._config, attr)
        except Exception:
            return False


# Made with Bob