"""
Input validation utilities for AI Study Assistant.
Provides validation functions for user inputs and data.
"""

import re
from typing import Tuple, Optional


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class InputValidator:
    """Validator for user inputs."""
    
    @staticmethod
    def validate_topic(topic: str, max_length: int = 1000) -> Tuple[bool, Optional[str]]:
        """
        Validate topic input.
        
        Args:
            topic: The topic string to validate
            max_length: Maximum allowed length
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not topic or not topic.strip():
            return False, "Topic cannot be empty"
        
        if len(topic) > max_length:
            return False, f"Topic is too long. Maximum {max_length} characters allowed"
        
        # Check for potentially harmful content
        if InputValidator._contains_harmful_patterns(topic):
            return False, "Topic contains invalid characters or patterns"
        
        return True, None
    
    @staticmethod
    def validate_api_key(api_key: str) -> Tuple[bool, Optional[str]]:
        """
        Validate API key format.
        
        Args:
            api_key: The API key to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not api_key or not api_key.strip():
            return False, "API key cannot be empty"
        
        if not (api_key.startswith("gsk_") or api_key.startswith("gsk-")):
            return False, "Invalid API key format. Groq API keys should start with 'gsk_' or 'gsk-'"
        
        if len(api_key) < 20:
            return False, "API key is too short"
        
        return True, None
    
    @staticmethod
    def _contains_harmful_patterns(text: str) -> bool:
        """
        Check if text contains potentially harmful patterns.
        
        Args:
            text: Text to check
        
        Returns:
            True if harmful patterns found, False otherwise
        """
        # Check for excessive special characters
        special_char_ratio = len(re.findall(r'[^a-zA-Z0-9\s\-_.,!?]', text)) / max(len(text), 1)
        if special_char_ratio > 0.3:
            return True
        
        # Check for script injection patterns
        harmful_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
            r'onclick=',
            r'eval\(',
            r'exec\(',
        ]
        
        text_lower = text.lower()
        for pattern in harmful_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Sanitize text input by removing potentially harmful content.
        
        Args:
            text: Text to sanitize
        
        Returns:
            Sanitized text
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Trim
        text = text.strip()
        
        return text
    
    @staticmethod
    def validate_session_data(data: dict) -> Tuple[bool, Optional[str]]:
        """
        Validate session data structure.
        
        Args:
            data: Session data dictionary
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_keys = ['explanation', 'notes', 'quiz']
        
        for key in required_keys:
            if key not in data:
                return False, f"Missing required key: {key}"
        
        # Validate notes is a list
        if not isinstance(data['notes'], list):
            return False, "Notes must be a list"
        
        # Validate quiz is a list
        if not isinstance(data['quiz'], list):
            return False, "Quiz must be a list"
        
        # Validate quiz items
        for idx, quiz_item in enumerate(data['quiz']):
            if not isinstance(quiz_item, dict):
                return False, f"Quiz item {idx} must be a dictionary"
            
            if 'question' not in quiz_item:
                return False, f"Quiz item {idx} missing 'question'"
            
            if 'options' not in quiz_item:
                return False, f"Quiz item {idx} missing 'options'"
            
            if 'answer' not in quiz_item:
                return False, f"Quiz item {idx} missing 'answer'"
            
            if not isinstance(quiz_item['options'], list):
                return False, f"Quiz item {idx} options must be a list"
        
        return True, None


class DataValidator:
    """Validator for data structures."""
    
    @staticmethod
    def validate_study_data(data: dict) -> Tuple[bool, Optional[str]]:
        """
        Validate study data structure from API response.
        
        Args:
            data: Study data dictionary
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        return InputValidator.validate_session_data(data)
    
    @staticmethod
    def validate_bookmark(bookmark: dict) -> Tuple[bool, Optional[str]]:
        """
        Validate bookmark data structure.
        
        Args:
            bookmark: Bookmark dictionary
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_keys = ['id', 'topic', 'timestamp', 'data']
        
        for key in required_keys:
            if key not in bookmark:
                return False, f"Missing required key: {key}"
        
        # Validate the study data within bookmark
        is_valid, error = DataValidator.validate_study_data(bookmark['data'])
        if not is_valid:
            return False, f"Invalid study data in bookmark: {error}"
        
        return True, None


# Convenience functions
def validate_topic(topic: str, max_length: int = 1000) -> Tuple[bool, Optional[str]]:
    """Validate topic input."""
    return InputValidator.validate_topic(topic, max_length)


def validate_api_key(api_key: str) -> Tuple[bool, Optional[str]]:
    """Validate API key format."""
    return InputValidator.validate_api_key(api_key)


def sanitize_text(text: str) -> str:
    """Sanitize text input."""
    return InputValidator.sanitize_text(text)

# Made with Bob
