"""
Data processing utilities for AI Study Assistant.
Handles JSON parsing, normalization, and data transformation.
"""

import json
import re
from typing import Dict, Any, List, Optional
from src.utils.robust_json_parser import RobustJSONParser


class DataProcessor:
    """Processor for study material data."""
    
    @staticmethod
    def extract_json_payload(text: str) -> dict:
        """
        Best-effort extraction of a JSON object from LLM output.
        
        Args:
            text: Raw text from LLM that may contain JSON
        
        Returns:
            Parsed JSON dictionary
        
        Raises:
            json.JSONDecodeError: If no valid JSON found
        """
        candidates = []
        cleaned = (text or "").strip()
        
        # Try to extract from code fences
        fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", cleaned, re.IGNORECASE)
        if fenced:
            candidates.append(fenced.group(1).strip())
        
        # Try to extract JSON object
        object_start = cleaned.find("{")
        object_end = cleaned.rfind("}")
        if object_start != -1 and object_end != -1 and object_end > object_start:
            candidates.append(cleaned[object_start : object_end + 1])
        
        # Try to extract JSON array
        array_start = cleaned.find("[")
        array_end = cleaned.rfind("]")
        if array_start != -1 and array_end != -1 and array_end > array_start:
            candidates.append(cleaned[array_start : array_end + 1])
        
        # Try the whole text as-is
        candidates.append(cleaned)
        
        last_error = None
        for candidate in candidates:
            try:
                return json.loads(candidate)
            except json.JSONDecodeError as exc:
                last_error = exc
        
        raise last_error or json.JSONDecodeError("No valid JSON found", cleaned, 0)
    
    @staticmethod
    def normalize_study_data(raw_data: dict) -> dict:
        """
        Normalize LLM response so the UI can always render safely.
        
        Args:
            raw_data: Raw data from API
        
        Returns:
            Normalized study data dictionary
        """
        notes = raw_data.get("notes", [])
        quiz_items = raw_data.get("quiz", [])
        
        # Normalize notes
        if not isinstance(notes, list):
            notes = [str(notes)] if notes else []
        
        # Ensure all notes are strings
        notes = [str(note) for note in notes if note]
        
        # Normalize quiz
        if not isinstance(quiz_items, list):
            quiz_items = []
        
        normalized_quiz = []
        for item in quiz_items:
            if isinstance(item, dict):
                normalized_quiz.append(
                    {
                        "question": str(item.get("question", "Question unavailable.")),
                        "options": DataProcessor._normalize_options(item.get("options", [])),
                        "answer": str(item.get("answer", "Answer unavailable.")),
                    }
                )
        
        # Ensure at least one quiz question
        if not normalized_quiz:
            normalized_quiz = [
                {
                    "question": "No quiz was returned by the model.",
                    "options": ["Try generating again"],
                    "answer": "Try generating again",
                }
            ]
        
        return {
            "explanation": str(raw_data.get("explanation", "No explanation was returned.")),
            "notes": notes or ["No notes were returned."],
            "quiz": normalized_quiz,
        }
    
    @staticmethod
    def _normalize_options(options: Any) -> List[str]:
        """
        Normalize quiz options to a list of strings.
        
        Args:
            options: Options from API (could be list, dict, or other)
        
        Returns:
            List of option strings
        """
        if not options:
            return ["Option unavailable"]
        
        if isinstance(options, list):
            return [str(opt) for opt in options if opt]
        
        if isinstance(options, dict):
            return [str(v) for v in options.values() if v]
        
        return [str(options)]
    
    @staticmethod
    def normalize_option_text(value: str) -> str:
        """
        Normalize option/answer text for robust comparison.
        
        Args:
            value: Option or answer text
        
        Returns:
            Normalized text
        """
        return re.sub(r"\s+", " ", str(value or "")).strip().lower()
    
    @staticmethod
    def resolve_correct_option(answer: str, options: List[str]) -> str:
        """
        Resolve model answer to the exact option text when possible.
        
        Args:
            answer: Answer from the model
            options: List of available options
        
        Returns:
            Resolved option text
        """
        if not options:
            return ""
        
        answer_raw = str(answer or "").strip()
        answer_norm = DataProcessor.normalize_option_text(answer_raw)
        
        # 1) Exact text match (case-insensitive)
        for opt in options:
            if DataProcessor.normalize_option_text(opt) == answer_norm:
                return opt
        
        # 2) Letter/index match (A/B/C/D, Option B, 1/2/3/4)
        letter_match = re.search(r"\b([A-D])\b", answer_raw, re.IGNORECASE)
        if letter_match:
            idx = ord(letter_match.group(1).upper()) - ord("A")
            if 0 <= idx < len(options):
                return options[idx]
        
        number_match = re.search(r"\b([1-9]\d*)\b", answer_raw)
        if number_match:
            idx = int(number_match.group(1)) - 1
            if 0 <= idx < len(options):
                return options[idx]
        
        # 3) Partial containment fallback
        for opt in options:
            opt_norm = DataProcessor.normalize_option_text(opt)
            if answer_norm and (answer_norm in opt_norm or opt_norm in answer_norm):
                return opt
        
        # If unresolved, keep original answer
        return answer_raw
    
    @staticmethod
    def format_for_export(data: dict, topic: str, format_type: str = "markdown") -> str:
        """
        Format study data for export.
        
        Args:
            data: Study data dictionary
            topic: Topic name
            format_type: Export format (markdown, text, json)
        
        Returns:
            Formatted string
        """
        if format_type == "json":
            return json.dumps({"topic": topic, "data": data}, indent=2)
        
        elif format_type == "text":
            output = []
            output.append(f"TOPIC: {topic}")
            output.append("=" * 50)
            output.append("\nEXPLANATION:")
            output.append(data.get("explanation", ""))
            output.append("\n\nNOTES:")
            for idx, note in enumerate(data.get("notes", []), 1):
                output.append(f"{idx}. {note}")
            output.append("\n\nQUIZ:")
            for idx, q in enumerate(data.get("quiz", []), 1):
                output.append(f"\nQuestion {idx}: {q.get('question', '')}")
                for i, opt in enumerate(q.get("options", []), 1):
                    output.append(f"  {i}. {opt}")
                output.append(f"Answer: {q.get('answer', '')}")
            return "\n".join(output)
        
        else:  # markdown (default)
            output = []
            output.append(f"# {topic}")
            output.append("\n## 📖 Explanation")
            output.append(data.get("explanation", ""))
            output.append("\n## 📝 Notes")
            for idx, note in enumerate(data.get("notes", []), 1):
                output.append(f"{idx}. {note}")
            output.append("\n## ❓ Quiz")
            for idx, q in enumerate(data.get("quiz", []), 1):
                output.append(f"\n### Question {idx}")
                output.append(q.get("question", ""))
                output.append("\n**Options:**")
                for i, opt in enumerate(q.get("options", []), 1):
                    output.append(f"- {opt}")
                output.append(f"\n**Answer:** {q.get('answer', '')}")
            return "\n".join(output)
    
    @staticmethod
    def calculate_study_stats(data: dict) -> Dict[str, Any]:
        """
        Calculate statistics for study material.
        
        Args:
            data: Study data dictionary
        
        Returns:
            Dictionary with statistics
        """
        explanation = data.get("explanation", "")
        notes = data.get("notes", [])
        quiz = data.get("quiz", [])
        
        return {
            "explanation_length": len(explanation),
            "explanation_words": len(explanation.split()),
            "notes_count": len(notes),
            "quiz_count": len(quiz),
            "total_words": len(explanation.split()) + sum(len(str(note).split()) for note in notes),
            "estimated_read_time": max(1, len(explanation.split()) // 200),  # ~200 words per minute
        }


# Convenience functions
def extract_json(text: str) -> dict:
    """Extract JSON from text."""
    return DataProcessor.extract_json_payload(text)


def normalize_data(raw_data: dict) -> dict:
    """Normalize study data."""
    return DataProcessor.normalize_study_data(raw_data)


def format_for_export(data: dict, topic: str, format_type: str = "markdown") -> str:
    """Format data for export."""
    return DataProcessor.format_for_export(data, topic, format_type)

# Made with Bob
