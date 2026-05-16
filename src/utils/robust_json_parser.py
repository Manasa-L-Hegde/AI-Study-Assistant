"""
Robust JSON parsing utilities for AI Study Assistant.
Multi-layer defensive parsing system that never crashes.
"""

import json
import re
import logging
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustJSONParser:
    """Bulletproof JSON parser with multiple fallback strategies."""
    
    @staticmethod
    def extract_and_parse_json(raw_response: str) -> Dict[str, Any]:
        """
        Multi-stage JSON extraction and parsing with comprehensive fallbacks.
        
        Args:
            raw_response: Raw string response from LLM
        
        Returns:
            Valid dictionary with complete structure
        """
        if not raw_response or not isinstance(raw_response, str):
            logger.error("Invalid input: empty or non-string response")
            return RobustJSONParser.generate_error_fallback(
                "Invalid input type",
                str(raw_response)[:200]
            )
        
        # Stage 1: Strip whitespace
        cleaned = raw_response.strip()
        logger.info(f"Stage 1: Stripped whitespace (length: {len(cleaned)})")
        
        # Stage 2: Remove markdown code fences
        cleaned = re.sub(r'```(?:json)?\s*', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'```\s*$', '', cleaned)
        cleaned = cleaned.strip()
        logger.info(f"Stage 2: Removed markdown fences (length: {len(cleaned)})")
        
        # Stage 3: Remove backticks
        cleaned = cleaned.replace('`', '')
        
        # Stage 4: Extract JSON object using regex
        json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if json_match:
            cleaned = json_match.group(0)
            logger.info(f"Stage 4: Extracted JSON object (length: {len(cleaned)})")
        else:
            logger.warning("Stage 4: No JSON object found in response")
            return RobustJSONParser.generate_error_fallback(
                "No JSON object found",
                raw_response[:200]
            )
        
        # Stage 5: First parsing attempt
        try:
            parsed = json.loads(cleaned)
            logger.info("Stage 5: Successfully parsed JSON on first attempt")
            return RobustJSONParser.validate_and_complete_structure(parsed)
        except json.JSONDecodeError as e:
            logger.warning(f"Stage 5: First parse failed: {e}")
            
            # Stage 6: Aggressive cleaning
            try:
                # Fix common issues
                cleaned = RobustJSONParser.aggressive_json_cleaning(cleaned)
                parsed = json.loads(cleaned)
                logger.info("Stage 6: Successfully parsed after aggressive cleaning")
                return RobustJSONParser.validate_and_complete_structure(parsed)
            except json.JSONDecodeError as e2:
                logger.error(f"Stage 6: Aggressive cleaning failed: {e2}")
                
                # Stage 7: Last resort - try to extract partial data
                try:
                    partial_data = RobustJSONParser.extract_partial_json(cleaned)
                    if partial_data:
                        logger.info("Stage 7: Extracted partial data")
                        return RobustJSONParser.validate_and_complete_structure(partial_data)
                except Exception as e3:
                    logger.error(f"Stage 7: Partial extraction failed: {e3}")
                
                # Stage 8: Complete fallback
                logger.error("All parsing stages failed, returning error fallback")
                return RobustJSONParser.generate_error_fallback(
                    str(e),
                    raw_response[:200]
                )
    
    @staticmethod
    def aggressive_json_cleaning(json_str: str) -> str:
        """
        Aggressively clean JSON string to make it parseable.
        
        Args:
            json_str: Potentially malformed JSON string
        
        Returns:
            Cleaned JSON string
        """
        # Remove control characters except newlines in strings
        json_str = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', json_str)
        
        # Fix unescaped newlines in strings (but not in mermaid code)
        # This is tricky - we need to escape newlines that are inside string values
        # but not break the JSON structure
        
        # Fix trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        json_str = re.sub(r',\s*]', ']', json_str)
        
        # Fix single quotes (replace with double quotes, but be careful)
        # Only replace single quotes that are clearly meant to be double quotes
        json_str = re.sub(r"'([^']*)':", r'"\1":', json_str)
        
        # Remove any remaining backticks
        json_str = json_str.replace('`', '')
        
        return json_str
    
    @staticmethod
    def extract_partial_json(json_str: str) -> Optional[Dict[str, Any]]:
        """
        Try to extract partial valid JSON from malformed string.
        
        Args:
            json_str: Malformed JSON string
        
        Returns:
            Partial dictionary or None
        """
        partial_data = {}
        
        # Try to extract title
        title_match = re.search(r'"title"\s*:\s*"([^"]*)"', json_str)
        if title_match:
            partial_data["title"] = title_match.group(1)
        
        # Try to extract explanation
        explanation_match = re.search(r'"explanation"\s*:\s*"([^"]*)"', json_str, re.DOTALL)
        if explanation_match:
            partial_data["explanation"] = explanation_match.group(1)
        
        # Try to extract arrays
        for field in ["key_concepts", "quick_revision", "interview_points", "examples"]:
            array_match = re.search(rf'"{field}"\s*:\s*\[(.*?)\]', json_str, re.DOTALL)
            if array_match:
                items = re.findall(r'"([^"]*)"', array_match.group(1))
                partial_data[field] = items
        
        return partial_data if partial_data else None
    
    @staticmethod
    def validate_and_complete_structure(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure all required keys exist with proper types.
        
        Args:
            data: Parsed dictionary (potentially incomplete)
        
        Returns:
            Complete dictionary with all required fields
        """
        # Define the complete template
        template = {
            "title": str(data.get("title", "Study Topic")),
            "explanation": str(data.get("explanation", "No explanation provided")),
            "key_concepts": [],
            "detailed_breakdown": {
                "what_it_is": "",
                "why_it_matters": "",
                "how_it_works": "",
                "key_principles": ""
            },
            "examples": [],
            "visual_diagram": {
                "type": "none",
                "mermaid_code": "",
                "description": ""
            },
            "formulas_or_code": [],
            "quick_revision": [],
            "interview_points": [],
            "common_mistakes": [],
            "related_topics": [],
            "quiz": []
        }
        
        # Safely extract and validate each field
        
        # Key concepts (also check for 'notes' as fallback)
        key_concepts = data.get("key_concepts", data.get("notes", []))
        if isinstance(key_concepts, list):
            template["key_concepts"] = [str(item) for item in key_concepts if item]
        
        # Detailed breakdown
        breakdown = data.get("detailed_breakdown", {})
        if isinstance(breakdown, dict):
            template["detailed_breakdown"] = {
                "what_it_is": str(breakdown.get("what_it_is", "")),
                "why_it_matters": str(breakdown.get("why_it_matters", "")),
                "how_it_works": str(breakdown.get("how_it_works", "")),
                "key_principles": str(breakdown.get("key_principles", ""))
            }
        
        # Examples
        examples = data.get("examples", [])
        if isinstance(examples, list):
            validated_examples = []
            for ex in examples:
                if isinstance(ex, dict):
                    validated_examples.append({
                        "title": str(ex.get("title", "Example")),
                        "description": str(ex.get("description", "")),
                        "explanation": str(ex.get("explanation", ""))
                    })
                elif isinstance(ex, str):
                    validated_examples.append({
                        "title": "Example",
                        "description": str(ex),
                        "explanation": ""
                    })
            template["examples"] = validated_examples
        
        # Visual diagram
        diagram = data.get("visual_diagram", {})
        if isinstance(diagram, dict) and diagram.get("mermaid_code"):
            template["visual_diagram"] = {
                "type": str(diagram.get("type", "flowchart")),
                "mermaid_code": str(diagram.get("mermaid_code", "")),
                "description": str(diagram.get("description", ""))
            }
        
        # Formulas or code
        formulas = data.get("formulas_or_code", [])
        if isinstance(formulas, list):
            validated_formulas = []
            for formula in formulas:
                if isinstance(formula, dict):
                    validated_formulas.append({
                        "title": str(formula.get("title", "Formula")),
                        "content": str(formula.get("content", "")),
                        "explanation": str(formula.get("explanation", ""))
                    })
                elif isinstance(formula, str):
                    validated_formulas.append({
                        "title": "Formula",
                        "content": str(formula),
                        "explanation": ""
                    })
            template["formulas_or_code"] = validated_formulas
        
        # Simple arrays
        for field in ["quick_revision", "interview_points", "common_mistakes", "related_topics"]:
            value = data.get(field, [])
            if isinstance(value, list):
                template[field] = [str(item) for item in value if item]
        
        # Quiz
        quiz = data.get("quiz", [])
        if isinstance(quiz, list):
            validated_quiz = []
            for q in quiz:
                if isinstance(q, dict):
                    options = q.get("options", [])
                    if isinstance(options, list) and len(options) >= 2:
                        validated_quiz.append({
                            "question": str(q.get("question", "Question")),
                            "options": [str(opt) for opt in options],
                            "answer": str(q.get("answer", q.get("correct", options[0] if options else ""))),
                            "explanation": str(q.get("explanation", ""))
                        })
            template["quiz"] = validated_quiz
        
        logger.info(f"Validated structure with {len(template['key_concepts'])} concepts, "
                   f"{len(template['examples'])} examples, {len(template['quiz'])} quiz questions")
        
        return template
    
    @staticmethod
    def generate_error_fallback(error_msg: str, preview: str) -> Dict[str, Any]:
        """
        Generate valid fallback response when parsing completely fails.
        
        Args:
            error_msg: Error message
            preview: Preview of the failed response
        
        Returns:
            Valid fallback dictionary
        """
        logger.error(f"Generating error fallback: {error_msg}")
        
        return {
            "title": "Response Parsing Error",
            "explanation": (
                f"⚠️ The AI response could not be parsed correctly.\n\n"
                f"**Error:** {error_msg}\n\n"
                f"**What happened:** The AI generated a response that wasn't in the expected format. "
                f"This is usually temporary. Please try again with a different topic or rephrase your request.\n\n"
                f"**Preview of response:** {preview}..."
            ),
            "key_concepts": [
                "JSON parsing failed - this is a temporary issue",
                "Try rephrasing your topic",
                "The AI will work correctly on the next attempt"
            ],
            "detailed_breakdown": {
                "what_it_is": "A temporary parsing error occurred",
                "why_it_matters": "The AI response format was unexpected",
                "how_it_works": "The system attempted multiple parsing strategies",
                "key_principles": "Fallback response generated to maintain functionality"
            },
            "examples": [],
            "visual_diagram": {
                "type": "none",
                "mermaid_code": "",
                "description": "No diagram available due to parsing error"
            },
            "formulas_or_code": [],
            "quick_revision": [
                "This was a temporary error",
                "Try again with a different topic",
                "The system is working normally"
            ],
            "interview_points": [],
            "common_mistakes": [
                "Don't worry - this is not your fault",
                "Simply try again with your topic",
                "The AI will generate proper content next time"
            ],
            "related_topics": [],
            "quiz": []
        }


# Convenience function for backward compatibility
def extract_json(raw_response: str) -> Dict[str, Any]:
    """
    Extract and parse JSON from raw LLM response.
    
    Args:
        raw_response: Raw string response from LLM
    
    Returns:
        Valid dictionary with complete structure
    """
    return RobustJSONParser.extract_and_parse_json(raw_response)


# Made with Bob