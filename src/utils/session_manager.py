"""
Session management utilities for AI Study Assistant.
Handles user sessions, bookmarks, and study history.
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import streamlit as st


def initialize_session_state():
    """
    CRITICAL: Initialize all session state variables with safe defaults.
    This MUST be called at app startup to prevent KeyError crashes on deployment.
    
    This function ensures that all session state keys exist before any access,
    preventing crashes on Streamlit Cloud where session state is fresh on deployment.
    """
    defaults = {
        "analytics": {
            "topics": 0,
            "accuracy": 0,
            "questions_asked": 0,
            "study_time": 0,
            "total_topics": 0,
            "total_quizzes": 0,
            "correct_answers": 0,
            "total_questions": 0,
            "last_activity": None,
        },
        "bookmarks": [],
        "history": [],
        "study_history": [],
        "chat_history": [],
        "study_mode": "comprehensive",
        "theme": "light",
        "api_configured": False,
        "study_data": None,
        "study_topic": "",
        "quiz_selected": {},
        "quiz_scores": {},
        "show_sidebar": True,
        "session_id": f"session_{int(time.time() * 1000)}",
        "session_start": time.time(),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


class SessionManager:
    """Manager for user session data."""
    
    def __init__(self):
        """Initialize session manager."""
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """
        Initialize all session state variables with safe defaults.
        This prevents KeyError crashes throughout the application.
        """
        # Study data
        if "study_data" not in st.session_state:
            st.session_state["study_data"] = None
        
        if "study_topic" not in st.session_state:
            st.session_state["study_topic"] = ""
        
        # Quiz state
        if "quiz_selected" not in st.session_state:
            st.session_state["quiz_selected"] = {}
        
        if "quiz_scores" not in st.session_state:
            st.session_state["quiz_scores"] = {}
        
        # Bookmarks
        if "bookmarks" not in st.session_state:
            st.session_state["bookmarks"] = []
        
        # History
        if "study_history" not in st.session_state:
            st.session_state["study_history"] = []
        
        # Analytics - Initialize with complete structure
        if "analytics" not in st.session_state:
            st.session_state["analytics"] = {
                "total_topics": 0,
                "total_quizzes": 0,
                "correct_answers": 0,
                "total_questions": 0,
                "study_time": 0,
                "last_activity": None,
            }
        
        # UI state - Default to light theme (no dark mode)
        if "theme" not in st.session_state:
            st.session_state["theme"] = "light"
        
        if "show_sidebar" not in st.session_state:
            st.session_state["show_sidebar"] = True
        
        # Study mode - NEW: Initialize study mode
        if "study_mode" not in st.session_state:
            st.session_state["study_mode"] = "comprehensive"
        
        # Session metadata
        if "session_id" not in st.session_state:
            st.session_state["session_id"] = self._generate_session_id()
        
        if "session_start" not in st.session_state:
            st.session_state["session_start"] = time.time()
    
    @staticmethod
    def _generate_session_id() -> str:
        """Generate a unique session ID."""
        return f"session_{int(time.time() * 1000)}"
    
    def save_study_data(self, topic: str, data: dict) -> None:
        """
        Save study data to session.
        
        Args:
            topic: Topic name
            data: Study data dictionary
        """
        st.session_state["study_data"] = data
        st.session_state["study_topic"] = topic
        st.session_state["quiz_selected"] = {}
        
        # Add to history
        self.add_to_history(topic, data)
        
        # Update analytics - Safe access
        analytics = st.session_state.get("analytics", {})
        analytics["total_topics"] = analytics.get("total_topics", 0) + 1
        analytics["last_activity"] = datetime.now().isoformat()
        st.session_state["analytics"] = analytics
    
    def get_study_data(self) -> Optional[Dict[str, Any]]:
        """
        Get current study data.
        
        Returns:
            Study data dictionary or None
        """
        return st.session_state.get("study_data")
    
    def get_study_topic(self) -> str:
        """
        Get current study topic.
        
        Returns:
            Topic string
        """
        return st.session_state.get("study_topic", "")
    
    def clear_study_data(self) -> None:
        """Clear current study data."""
        st.session_state["study_data"] = None
        st.session_state["study_topic"] = ""
        st.session_state["quiz_selected"] = {}
    
    def add_bookmark(self, topic: str, data: dict) -> bool:
        """
        Add a bookmark.
        
        Args:
            topic: Topic name
            data: Study data
        
        Returns:
            True if added, False if already exists
        """
        # Check if already bookmarked - Safe access
        bookmarks = st.session_state.get("bookmarks", [])
        for bookmark in bookmarks:
            if bookmark["topic"].lower() == topic.lower():
                return False
        
        bookmark = {
            "id": f"bookmark_{int(time.time() * 1000)}",
            "topic": topic,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        
        bookmarks.append(bookmark)
        st.session_state["bookmarks"] = bookmarks
        return True
    
    def remove_bookmark(self, bookmark_id: str) -> bool:
        """
        Remove a bookmark.
        
        Args:
            bookmark_id: Bookmark ID
        
        Returns:
            True if removed, False if not found
        """
        # Safe access
        bookmarks = st.session_state.get("bookmarks", [])
        for i, bookmark in enumerate(bookmarks):
            if bookmark["id"] == bookmark_id:
                bookmarks.pop(i)
                st.session_state["bookmarks"] = bookmarks
                return True
        return False
    
    def get_bookmarks(self) -> List[Dict[str, Any]]:
        """
        Get all bookmarks.
        
        Returns:
            List of bookmark dictionaries
        """
        return st.session_state.get("bookmarks", [])
    
    def is_bookmarked(self, topic: str) -> bool:
        """
        Check if a topic is bookmarked.
        
        Args:
            topic: Topic name
        
        Returns:
            True if bookmarked, False otherwise
        """
        # Safe access
        bookmarks = st.session_state.get("bookmarks", [])
        for bookmark in bookmarks:
            if bookmark["topic"].lower() == topic.lower():
                return True
        return False
    
    def add_to_history(self, topic: str, data: dict) -> None:
        """
        Add entry to study history.
        
        Args:
            topic: Topic name
            data: Study data
        """
        history_entry = {
            "id": f"history_{int(time.time() * 1000)}",
            "topic": topic,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        
        # Keep only last 50 entries - Safe access
        history = st.session_state.get("study_history", [])
        history.insert(0, history_entry)
        st.session_state["study_history"] = history[:50]
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get study history.
        
        Args:
            limit: Maximum number of entries to return
        
        Returns:
            List of history entries
        """
        history = st.session_state.get("study_history", [])
        if limit:
            return history[:limit]
        return history
    
    def clear_history(self) -> None:
        """Clear study history."""
        st.session_state["study_history"] = []
    
    def record_quiz_answer(self, question_id: str, is_correct: bool) -> None:
        """
        Record a quiz answer.
        
        Args:
            question_id: Question identifier
            is_correct: Whether the answer was correct
        """
        # Safe access to analytics
        analytics = st.session_state.get("analytics", {
            "total_questions": 0,
            "correct_answers": 0,
            "last_activity": None
        })
        analytics["total_questions"] = analytics.get("total_questions", 0) + 1
        if is_correct:
            analytics["correct_answers"] = analytics.get("correct_answers", 0) + 1
        analytics["last_activity"] = datetime.now().isoformat()
        st.session_state["analytics"] = analytics
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Get analytics data with safe access.
        
        Returns:
            Analytics dictionary
        """
        # Safe access with fallback
        analytics = st.session_state.get("analytics", {
            "total_topics": 0,
            "total_quizzes": 0,
            "correct_answers": 0,
            "total_questions": 0,
            "study_time": 0,
            "last_activity": None,
        }).copy()
        
        # Calculate accuracy
        if analytics.get("total_questions", 0) > 0:
            analytics["accuracy"] = (analytics.get("correct_answers", 0) / analytics["total_questions"]) * 100
        else:
            analytics["accuracy"] = 0
        
        # Calculate session duration with safe access
        session_start = st.session_state.get("session_start", time.time())
        analytics["session_duration"] = int(time.time() - session_start)
        
        return analytics
    
    def reset_analytics(self) -> None:
        """Reset analytics data."""
        st.session_state["analytics"] = {
            "total_topics": 0,
            "total_quizzes": 0,
            "correct_answers": 0,
            "total_questions": 0,
            "study_time": 0,
            "last_activity": None,
        }
    
    def set_theme(self, theme: str) -> None:
        """
        Set UI theme.
        
        Args:
            theme: Theme name ('dark' or 'light')
        """
        if theme in ["dark", "light"]:
            st.session_state["theme"] = theme
    
    def get_theme(self) -> str:
        """
        Get current theme.
        
        Returns:
            Theme name
        """
        return st.session_state.get("theme", "dark")
    
    def toggle_theme(self) -> str:
        """
        Toggle between dark and light theme.
        
        Returns:
            New theme name
        """
        current = self.get_theme()
        new_theme = "light" if current == "dark" else "dark"
        self.set_theme(new_theme)
        return new_theme
    
    def export_session_data(self) -> str:
        """
        Export all session data as JSON.
        
        Returns:
            JSON string of session data
        """
        export_data = {
            "session_id": st.session_state.get("session_id"),
            "bookmarks": st.session_state.get("bookmarks", []),
            "history": st.session_state.get("study_history", []),
            "analytics": self.get_analytics(),
            "exported_at": datetime.now().isoformat(),
        }
        return json.dumps(export_data, indent=2)
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current session.
        
        Returns:
            Session summary dictionary
        """
        analytics = self.get_analytics()
        return {
            "session_id": st.session_state.get("session_id"),
            "duration_minutes": analytics["session_duration"] // 60,
            "topics_studied": analytics["total_topics"],
            "questions_answered": analytics["total_questions"],
            "accuracy": analytics["accuracy"],
            "bookmarks_count": len(st.session_state.get("bookmarks", [])),
            "history_count": len(st.session_state.get("study_history", [])),
        }


# Global session manager instance
session_manager = SessionManager()

# Made with Bob
