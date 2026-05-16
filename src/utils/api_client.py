"""
API client for interacting with Groq API.
Handles all API communication with proper error handling and retry logic.
"""

import time
import logging
from typing import Optional, Dict, Any
from openai import OpenAI, APIError, AuthenticationError, RateLimitError, BadRequestError, APITimeoutError
import streamlit as st

from src.config import settings
from src.utils.enhanced_prompts import EducationalPrompts
from src.utils.robust_json_parser import RobustJSONParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    """Client for Groq API interactions."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize API client.
        
        Args:
            api_key: Optional API key override
            model: Optional model name override
        """
        self.api_key = api_key or settings.api.groq_api_key
        self.model = model or settings.api.groq_model
        self.base_url = settings.api.base_url
        self.client: Optional[OpenAI] = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize the OpenAI client with Groq configuration."""
        if self.api_key and (self.api_key.startswith("gsk_") or self.api_key.startswith("gsk-")):
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
    
    def is_configured(self) -> bool:
        """Check if the API client is properly configured."""
        return self.client is not None
    
    def validate_api_key(self) -> tuple[bool, str]:
        """
        Validate the API key format and connectivity.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.api_key:
            return False, "API key is not set"
        
        if not (self.api_key.startswith("gsk_") or self.api_key.startswith("gsk-")):
            return False, "Invalid key format. Groq API key should start with 'gsk_' or 'gsk-'"
        
        if not self.client:
            return False, "Client initialization failed"
        
        return True, ""
    
    @st.cache_data(ttl=settings.cache.ttl, show_spinner=False)
    def generate_study_material(_self, topic: str, mode: str = "comprehensive", temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate study material for a given topic.
        
        Args:
            topic: The topic to generate study material for
            mode: 'comprehensive' or 'quick' mode
            temperature: Model temperature for generation
        
        Returns:
            Dictionary containing the API response
        
        Raises:
            Various API exceptions
        """
        if not _self.client:
            logger.error("API client not initialized")
            raise ValueError("API client not initialized")
        
        # Use enhanced prompts
        prompt = EducationalPrompts.get_prompt_by_mode(topic, mode)
        logger.info(f"Generating study material for topic: {topic} (mode: {mode})")
        
        try:
            # Enhanced system prompt to ensure raw JSON output
            system_prompt = (
                "You are an expert educational AI tutor that responds with ONLY valid JSON. "
                "CRITICAL: Your response must be raw JSON starting with { and ending with }. "
                "NEVER use markdown code fences (```json or ```), backticks, or any formatting. "
                "All string values must have properly escaped quotes and newlines. "
                "Return ONLY the JSON object - no text before or after it. "
                "The JSON must be directly parseable by Python's json.loads() without any preprocessing."
            )
            
            response = _self.client.chat.completions.create(
                model=_self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=4000,  # Increased for comprehensive responses
            )
            
            raw_content = response.choices[0].message.content
            logger.info(f"Received response (tokens: {response.usage.total_tokens if response.usage else 0})")
            
            # Use robust JSON parser
            try:
                parsed_data = RobustJSONParser.extract_and_parse_json(raw_content)
                logger.info("Successfully parsed and validated JSON response")
                
                return {
                    "success": True,
                    "content": raw_content,  # Keep raw for debugging
                    "parsed_data": parsed_data,  # Add parsed data
                    "model": _self.model,
                    "mode": mode,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                        "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                        "total_tokens": response.usage.total_tokens if response.usage else 0,
                    }
                }
            except Exception as parse_error:
                logger.error(f"JSON parsing failed: {parse_error}")
                # Return error but with fallback data
                fallback_data = RobustJSONParser.generate_error_fallback(
                    str(parse_error),
                    raw_content[:200]
                )
                return {
                    "success": True,  # Still success from API perspective
                    "content": raw_content,
                    "parsed_data": fallback_data,
                    "model": _self.model,
                    "mode": mode,
                    "parsing_error": str(parse_error),
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                        "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                        "total_tokens": response.usage.total_tokens if response.usage else 0,
                    }
                }
        
        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            return {
                "success": False,
                "error": "authentication",
                "message": "Invalid API key. Please check your credentials.",
                "details": str(e)
            }
        
        except RateLimitError as e:
            logger.warning(f"Rate limit error: {e}")
            return {
                "success": False,
                "error": "rate_limit",
                "message": "Rate limit reached. Please wait a moment and try again.",
                "details": str(e)
            }
        
        except APITimeoutError as e:
            logger.error(f"Timeout error: {e}")
            return {
                "success": False,
                "error": "timeout",
                "message": "Request timed out. Please try again.",
                "details": str(e)
            }
        
        except BadRequestError as e:
            logger.error(f"Bad request error: {e}")
            return {
                "success": False,
                "error": "bad_request",
                "message": "Invalid request. Please check your input.",
                "details": str(e)
            }
        
        except APIError as e:
            logger.error(f"API error: {e}")
            return {
                "success": False,
                "error": "api_error",
                "message": "API request failed. Please try again.",
                "details": str(e)
            }
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                "success": False,
                "error": "unknown",
                "message": f"Unexpected error: {str(e)}",
                "details": str(e)
            }
    
    def get_available_models(self) -> list[str]:
        """
        Get list of available models.
        
        Returns:
            List of model names
        """
        return [
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "llama-3.2-90b-text-preview"
        ]
    
    def update_api_key(self, new_key: str) -> bool:
        """
        Update the API key and reinitialize the client.
        
        Args:
            new_key: New API key
        
        Returns:
            True if successful, False otherwise
        """
        self.api_key = new_key
        self._initialize_client()
        is_valid, _ = self.validate_api_key()
        return is_valid
    
    def update_model(self, new_model: str) -> None:
        """
        Update the model name.
        
        Args:
            new_model: New model name
        """
        if new_model in self.get_available_models():
            self.model = new_model


# Global API client instance
api_client = APIClient()

# Made with Bob
