"""
Enhanced prompt templates for educational AI responses.
Provides comprehensive, detailed, and structured learning content.
"""

from typing import Dict, Any


class EducationalPrompts:
    """Manager for educational prompt templates."""
    
    @staticmethod
    def build_comprehensive_study_prompt(topic: str) -> str:
        """
        Build a comprehensive educational prompt for detailed learning.
        
        Args:
            topic: The topic to generate study material for
        
        Returns:
            Formatted prompt string
        """
        return f"""You are an expert educational AI tutor. Create comprehensive, detailed study material for: "{topic}"

CRITICAL OUTPUT REQUIREMENTS:
1. Return ONLY raw, valid JSON - NO markdown formatting
2. Do NOT wrap your response in ```json or ``` code fences
3. Do NOT use backticks anywhere in your response
4. Start directly with {{ and end with }}
5. Properly escape all quotes and newlines in string values
6. Use double quotes for all strings, never single quotes
7. No trailing commas in arrays or objects
8. No comments in the JSON
9. No text before or after the JSON object

OUTPUT FORMAT: Return ONLY valid JSON in this exact structure (no code fences):

{{
    "explanation": "Detailed multi-paragraph explanation (see requirements below)",
    "key_concepts": [
        "Concept 1 with brief explanation",
        "Concept 2 with brief explanation",
        "Concept 3 with brief explanation",
        "Concept 4 with brief explanation",
        "Concept 5 with brief explanation"
    ],
    "detailed_breakdown": {{
        "what_it_is": "Clear definition and overview",
        "why_it_matters": "Real-world importance and applications",
        "how_it_works": "Step-by-step explanation of mechanisms/processes",
        "key_principles": "Fundamental principles and rules"
    }},
    "examples": [
        {{
            "title": "Example 1 Title",
            "description": "Detailed example with context",
            "explanation": "Why this example matters"
        }},
        {{
            "title": "Example 2 Title",
            "description": "Detailed example with context",
            "explanation": "Why this example matters"
        }}
    ],
    "visual_diagram": {{
        "type": "flowchart|mindmap|sequence|class|graph",
        "mermaid_code": "Valid Mermaid diagram code",
        "description": "What the diagram shows"
    }},
    "formulas_or_code": [
        {{
            "title": "Formula/Code 1",
            "content": "The actual formula or code",
            "explanation": "What it means and when to use it"
        }}
    ],
    "quick_revision": [
        "Quick point 1 - one sentence summary",
        "Quick point 2 - one sentence summary",
        "Quick point 3 - one sentence summary",
        "Quick point 4 - one sentence summary",
        "Quick point 5 - one sentence summary"
    ],
    "interview_points": [
        "Important interview/exam point 1",
        "Important interview/exam point 2",
        "Important interview/exam point 3"
    ],
    "common_mistakes": [
        "Common mistake 1 and how to avoid it",
        "Common mistake 2 and how to avoid it",
        "Common mistake 3 and how to avoid it"
    ],
    "related_topics": [
        "Related topic 1",
        "Related topic 2",
        "Related topic 3"
    ],
    "quiz": [
        {{
            "question": "Conceptual question testing understanding",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct option text (must match one of the options exactly)",
            "explanation": "Why this is the correct answer"
        }},
        {{
            "question": "Application-based question",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct option text",
            "explanation": "Why this is the correct answer"
        }},
        {{
            "question": "Analysis question",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct option text",
            "explanation": "Why this is the correct answer"
        }},
        {{
            "question": "Synthesis question",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct option text",
            "explanation": "Why this is the correct answer"
        }},
        {{
            "question": "Evaluation question",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Correct option text",
            "explanation": "Why this is the correct answer"
        }}
    ]
}}

CRITICAL REQUIREMENTS FOR "explanation":

1. **Length**: Write 4-6 comprehensive paragraphs (minimum 800 words total)

2. **Structure**:
   - Paragraph 1: Introduction - What is {topic}? Why is it important?
   - Paragraph 2: Historical context or foundational concepts
   - Paragraph 3: Core mechanisms/principles - How does it work?
   - Paragraph 4: Real-world applications and examples
   - Paragraph 5: Advanced concepts or current developments
   - Paragraph 6: Summary and future implications

3. **Content Quality**:
   - Use clear, educational language
   - Define all technical terms when first used
   - Include specific examples and analogies
   - Explain cause-and-effect relationships
   - Connect concepts to real-world scenarios
   - Use transition words between ideas

4. **Educational Value**:
   - Explain WHY things work, not just WHAT they are
   - Break down complex ideas into digestible parts
   - Provide context and background
   - Highlight key insights and takeaways
   - Address common misconceptions

5. **Formatting**:
   - Use proper paragraphs (not bullet points in explanation)
   - Include relevant terminology
   - Maintain academic yet accessible tone
   - Ensure logical flow between paragraphs

DIAGRAM REQUIREMENTS:
- If the topic involves processes, create a flowchart
- If it involves relationships, create a mindmap or graph
- If it involves sequences, create a sequence diagram
- Use valid Mermaid syntax
- Make diagrams clear and educational

EXAMPLES REQUIREMENTS:
- Provide concrete, real-world examples
- Explain why each example is relevant
- Show practical applications

QUIZ REQUIREMENTS:
- Create 5 questions at different cognitive levels
- Questions should test understanding, not just memorization
- Include clear explanations for correct answers
- Make distractors (wrong options) plausible but clearly incorrect

Remember: This is for serious learning. Be thorough, detailed, and educational. Think like a university professor creating comprehensive course material."""

    @staticmethod
    def build_quick_study_prompt(topic: str) -> str:
        """
        Build a quick study prompt for faster responses.
        
        Args:
            topic: The topic to generate study material for
        
        Returns:
            Formatted prompt string
        """
        return f"""Create concise study material for: "{topic}"

Return ONLY valid JSON:

{{
    "explanation": "Clear 2-3 paragraph explanation covering key points",
    "key_concepts": [
        "Key concept 1",
        "Key concept 2",
        "Key concept 3",
        "Key concept 4",
        "Key concept 5"
    ],
    "quick_revision": [
        "Quick point 1",
        "Quick point 2",
        "Quick point 3",
        "Quick point 4",
        "Quick point 5"
    ],
    "quiz": [
        {{
            "question": "Question 1",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct option",
            "explanation": "Why this is correct"
        }},
        {{
            "question": "Question 2",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct option",
            "explanation": "Why this is correct"
        }},
        {{
            "question": "Question 3",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct option",
            "explanation": "Why this is correct"
        }}
    ]
}}

Keep it focused and educational."""

    @staticmethod
    def get_prompt_by_mode(topic: str, mode: str = "comprehensive") -> str:
        """
        Get prompt based on selected mode.
        
        Args:
            topic: The topic to generate study material for
            mode: 'comprehensive' or 'quick'
        
        Returns:
            Formatted prompt string
        """
        if mode == "quick":
            return EducationalPrompts.build_quick_study_prompt(topic)
        return EducationalPrompts.build_comprehensive_study_prompt(topic)


# Made with Bob