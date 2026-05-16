"""
Tests for robust JSON parser.
Ensures bulletproof parsing of LLM outputs.
"""

import pytest
from src.utils.robust_json_parser import RobustJSONParser


class TestRobustJSONParser:
    """Test suite for RobustJSONParser."""
    
    def test_valid_json(self):
        """Test parsing of valid JSON."""
        response = '{"title": "Test Topic", "explanation": "Test explanation"}'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Test Topic"
        assert result["explanation"] == "Test explanation"
        assert isinstance(result["key_concepts"], list)
    
    def test_json_with_code_fences(self):
        """Test parsing JSON wrapped in markdown code fences."""
        response = '```json\n{"title": "Test", "explanation": "..."}\n```'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Test"
        assert "explanation" in result
    
    def test_json_with_backticks(self):
        """Test parsing JSON with backticks."""
        response = '`{"title": "Test", "explanation": "..."}`'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Test"
    
    def test_json_with_text_before(self):
        """Test parsing JSON with text before it."""
        response = 'Here is the JSON:\n{"title": "Test", "explanation": "..."}'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Test"
    
    def test_json_with_text_after(self):
        """Test parsing JSON with text after it."""
        response = '{"title": "Test", "explanation": "..."}\nThat was the JSON.'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Test"
    
    def test_json_with_trailing_comma(self):
        """Test parsing JSON with trailing commas."""
        response = '{"title": "Test", "explanation": "...",}'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Test"
    
    def test_empty_response(self):
        """Test handling of empty response."""
        response = ''
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Response Parsing Error"
        assert "key_concepts" in result
    
    def test_none_response(self):
        """Test handling of None response."""
        response = None
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Response Parsing Error"
    
    def test_complete_garbage(self):
        """Test handling of complete garbage input."""
        response = 'This is not JSON at all! Just random text.'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Response Parsing Error"
        assert isinstance(result["key_concepts"], list)
    
    def test_partial_json(self):
        """Test extraction of partial JSON data."""
        response = '{"title": "Test", "explanation": "Incomplete...'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        # Should return fallback but not crash
        assert "title" in result
        assert isinstance(result, dict)
    
    def test_structure_validation(self):
        """Test that all required fields are present."""
        response = '{"title": "Test"}'  # Minimal JSON
        result = RobustJSONParser.extract_and_parse_json(response)
        
        # All required fields should be present
        assert "title" in result
        assert "explanation" in result
        assert "key_concepts" in result
        assert "detailed_breakdown" in result
        assert "examples" in result
        assert "visual_diagram" in result
        assert "quiz" in result
    
    def test_type_validation(self):
        """Test that all fields have correct types."""
        response = '{"title": "Test", "key_concepts": ["A", "B"]}'
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert isinstance(result["title"], str)
        assert isinstance(result["key_concepts"], list)
        assert isinstance(result["detailed_breakdown"], dict)
        assert isinstance(result["quiz"], list)
    
    def test_quiz_validation(self):
        """Test quiz question validation."""
        response = '''{
            "title": "Test",
            "quiz": [
                {
                    "question": "Q1",
                    "options": ["A", "B", "C", "D"],
                    "answer": "A",
                    "explanation": "Because A"
                }
            ]
        }'''
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert len(result["quiz"]) == 1
        assert result["quiz"][0]["question"] == "Q1"
        assert len(result["quiz"][0]["options"]) == 4
    
    def test_examples_validation(self):
        """Test examples validation."""
        response = '''{
            "title": "Test",
            "examples": [
                {
                    "title": "Example 1",
                    "description": "Desc",
                    "explanation": "Exp"
                }
            ]
        }'''
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert len(result["examples"]) == 1
        assert result["examples"][0]["title"] == "Example 1"
    
    def test_diagram_validation(self):
        """Test diagram validation."""
        response = '''{
            "title": "Test",
            "visual_diagram": {
                "type": "flowchart",
                "mermaid_code": "graph TD\\nA-->B",
                "description": "Test diagram"
            }
        }'''
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["visual_diagram"]["type"] == "flowchart"
        assert "mermaid_code" in result["visual_diagram"]
    
    def test_aggressive_cleaning(self):
        """Test aggressive JSON cleaning."""
        # Test with various malformations
        malformed = '{"title": "Test", "key_concepts": ["A", "B",]}'  # Trailing comma
        result = RobustJSONParser.extract_and_parse_json(malformed)
        
        assert result["title"] == "Test"
    
    def test_logging(self, caplog):
        """Test that parsing stages are logged."""
        response = '{"title": "Test"}'
        RobustJSONParser.extract_and_parse_json(response)
        
        # Check that logging occurred
        assert len(caplog.records) > 0
    
    def test_fallback_response_structure(self):
        """Test that fallback response has valid structure."""
        fallback = RobustJSONParser.generate_error_fallback("Test error", "Preview")
        
        assert fallback["title"] == "Response Parsing Error"
        assert "error" in fallback["explanation"].lower()
        assert isinstance(fallback["key_concepts"], list)
        assert len(fallback["key_concepts"]) > 0
    
    def test_real_world_llm_output(self):
        """Test with realistic LLM output patterns."""
        # Simulate common LLM output with code fences and extra text
        response = '''Here's the study material you requested:

```json
{
    "title": "Machine Learning",
    "explanation": "Machine learning is a subset of AI...",
    "key_concepts": [
        "Supervised learning",
        "Unsupervised learning",
        "Neural networks"
    ],
    "quiz": [
        {
            "question": "What is ML?",
            "options": ["A", "B", "C", "D"],
            "answer": "A"
        }
    ]
}
```

I hope this helps!'''
        
        result = RobustJSONParser.extract_and_parse_json(response)
        
        assert result["title"] == "Machine Learning"
        assert len(result["key_concepts"]) == 3
        assert len(result["quiz"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
