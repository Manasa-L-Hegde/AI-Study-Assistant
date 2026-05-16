"""Tests for validation utilities."""

import pytest
from src.utils.validators import InputValidator, DataValidator, validate_topic, validate_api_key


class TestInputValidator:
    """Test cases for InputValidator class."""
    
    def test_validate_topic_valid(self):
        """Test validation of valid topics."""
        is_valid, error = InputValidator.validate_topic("Machine Learning")
        assert is_valid is True
        assert error is None
    
    def test_validate_topic_empty(self):
        """Test validation of empty topic."""
        is_valid, error = InputValidator.validate_topic("")
        assert is_valid is False
        assert "cannot be empty" in error.lower()
    
    def test_validate_topic_too_long(self):
        """Test validation of topic that's too long."""
        long_topic = "a" * 1001
        is_valid, error = InputValidator.validate_topic(long_topic, max_length=1000)
        assert is_valid is False
        assert "too long" in error.lower()
    
    def test_validate_topic_whitespace_only(self):
        """Test validation of whitespace-only topic."""
        is_valid, error = InputValidator.validate_topic("   ")
        assert is_valid is False
        assert "cannot be empty" in error.lower()
    
    def test_validate_api_key_valid(self):
        """Test validation of valid API key."""
        is_valid, error = InputValidator.validate_api_key("gsk_1234567890abcdefghij")
        assert is_valid is True
        assert error is None
    
    def test_validate_api_key_invalid_prefix(self):
        """Test validation of API key with invalid prefix."""
        is_valid, error = InputValidator.validate_api_key("invalid_key")
        assert is_valid is False
        assert "invalid" in error.lower()
    
    def test_validate_api_key_empty(self):
        """Test validation of empty API key."""
        is_valid, error = InputValidator.validate_api_key("")
        assert is_valid is False
        assert "cannot be empty" in error.lower()
    
    def test_validate_api_key_too_short(self):
        """Test validation of API key that's too short."""
        is_valid, error = InputValidator.validate_api_key("gsk_short")
        assert is_valid is False
        assert "too short" in error.lower()
    
    def test_sanitize_text(self):
        """Test text sanitization."""
        dirty_text = "<script>alert('xss')</script>  Multiple   spaces  "
        clean_text = InputValidator.sanitize_text(dirty_text)
        assert "<script>" not in clean_text
        assert "  " not in clean_text
        assert clean_text == clean_text.strip()
    
    def test_validate_session_data_valid(self):
        """Test validation of valid session data."""
        data = {
            "explanation": "Test explanation",
            "notes": ["Note 1", "Note 2"],
            "quiz": [
                {
                    "question": "Test question?",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A"
                }
            ]
        }
        is_valid, error = InputValidator.validate_session_data(data)
        assert is_valid is True
        assert error is None
    
    def test_validate_session_data_missing_key(self):
        """Test validation of session data with missing key."""
        data = {
            "explanation": "Test explanation",
            "notes": ["Note 1"]
        }
        is_valid, error = InputValidator.validate_session_data(data)
        assert is_valid is False
        assert "missing" in error.lower()


class TestDataValidator:
    """Test cases for DataValidator class."""
    
    def test_validate_study_data(self):
        """Test validation of study data."""
        data = {
            "explanation": "Test",
            "notes": ["Note"],
            "quiz": [{"question": "Q?", "options": ["A"], "answer": "A"}]
        }
        is_valid, error = DataValidator.validate_study_data(data)
        assert is_valid is True
        assert error is None
    
    def test_validate_bookmark_valid(self):
        """Test validation of valid bookmark."""
        bookmark = {
            "id": "bookmark_123",
            "topic": "Test Topic",
            "timestamp": "2024-01-01T00:00:00",
            "data": {
                "explanation": "Test",
                "notes": ["Note"],
                "quiz": [{"question": "Q?", "options": ["A"], "answer": "A"}]
            }
        }
        is_valid, error = DataValidator.validate_bookmark(bookmark)
        assert is_valid is True
        assert error is None
    
    def test_validate_bookmark_missing_field(self):
        """Test validation of bookmark with missing field."""
        bookmark = {
            "id": "bookmark_123",
            "topic": "Test Topic"
        }
        is_valid, error = DataValidator.validate_bookmark(bookmark)
        assert is_valid is False
        assert "missing" in error.lower()


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_validate_topic_function(self):
        """Test validate_topic convenience function."""
        is_valid, error = validate_topic("Python Programming")
        assert is_valid is True
    
    def test_validate_api_key_function(self):
        """Test validate_api_key convenience function."""
        is_valid, error = validate_api_key("gsk_1234567890abcdefghij")
        assert is_valid is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
