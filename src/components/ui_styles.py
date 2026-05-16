"""
UI styling and theme management for AI Study Assistant.
Provides CSS styles for dark and light themes with modern design.
"""

from typing import Dict


class UIStyles:
    """Manager for UI styles and themes."""
    
    @staticmethod
    def get_dark_theme() -> str:
        """
        Get dark theme CSS - Cute pastel pink/purple theme.
        
        Returns:
            CSS string for dark theme
        """
        return """
        <style>
            :root {
                --bg-0: #fef3f8;
                --bg-1: #ffe5f1;
                --bg-2: #ffd4e9;
                --card: rgba(255, 255, 255, 0.95);
                --text: #2d1b2e;
                --text-muted: #8b5a8e;
                --line: rgba(255, 107, 157, 0.2);
                --shadow: 0 8px 24px rgba(255, 107, 157, 0.15);
                --primary: #ff6b9d;
                --primary-light: #ff8fb3;
                --secondary: #c77dff;
                --success: #06d6a0;
                --error: #ff6b9d;
                --warning: #ffd166;
            }

            .stApp {
                background:
                    radial-gradient(circle at 20% 20%, rgba(255, 107, 157, 0.08) 0 2px, transparent 2.1px),
                    radial-gradient(circle at 80% 30%, rgba(199, 125, 255, 0.08) 0 2px, transparent 2.1px),
                    radial-gradient(circle at 40% 70%, rgba(255, 209, 102, 0.06) 0 1.5px, transparent 1.6px),
                    radial-gradient(circle at 70% 80%, rgba(6, 214, 160, 0.06) 0 1.5px, transparent 1.6px),
                    linear-gradient(135deg, #fef3f8 0%, #ffe5f1 50%, #ffd4e9 100%);
                color: var(--text);
            }

            h1, h2, h3, h4, h5, h6 {
                color: var(--text);
                letter-spacing: 0.2px;
            }

            .hero-box {
                backdrop-filter: blur(10px);
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 229, 241, 0.95));
                border: 2px solid var(--primary);
                border-radius: 24px;
                padding: 2rem 2.5rem;
                box-shadow: var(--shadow);
                margin-bottom: 1.5rem;
                animation: fadeIn 0.5s ease-in;
            }

            .chip-row {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 15px;
                justify-content: center;
            }

            .chip {
                background: linear-gradient(135deg, #ff6b9d, #c77dff);
                border: none;
                color: white;
                border-radius: 999px;
                font-size: 0.85rem;
                padding: 8px 16px;
                transition: all 0.3s ease;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(255, 107, 157, 0.3);
            }

            .chip:hover {
                transform: translateY(-2px) scale(1.05);
                box-shadow: 0 6px 16px rgba(255, 107, 157, 0.4);
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #fff5fa 0%, #ffe5f1 100%);
                border-right: 2px solid var(--line);
            }

            .stButton > button {
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: #ffffff !important;
                border: 0;
                border-radius: 20px;
                padding: 0.8rem 1.5rem;
                font-weight: 700;
                box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
                transition: all 0.3s ease;
                width: 100%;
            }

            .stButton > button:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(255, 107, 157, 0.5);
            }

            .stButton > button:active {
                transform: translateY(0);
            }

            .stTextArea textarea, .stTextInput input {
                border-radius: 14px;
                border: 2px solid var(--line);
                background: rgba(3, 6, 15, 0.92);
                color: var(--text);
                transition: border-color 0.2s ease;
            }

            .stTextArea textarea:focus, .stTextInput input:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
            }

            .stTabs [data-baseweb="tab-list"] {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 6px;
                gap: 4px;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 10px;
                font-weight: 600;
                color: var(--text-muted);
                transition: all 0.2s ease;
            }

            .stTabs [aria-selected="true"] {
                background: var(--primary) !important;
                color: white !important;
            }

            .result-card {
                background: rgba(9, 14, 24, 0.92);
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 1.2rem;
                margin-top: 0.8rem;
                animation: slideIn 0.3s ease-out;
            }

            .quiz-option {
                background: rgba(255, 255, 255, 0.04);
                border: 2px solid var(--line);
                border-radius: 12px;
                padding: 0.8rem 1rem;
                margin: 0.5rem 0;
                cursor: pointer;
                transition: all 0.2s ease;
            }

            .quiz-option:hover {
                background: rgba(255, 255, 255, 0.08);
                border-color: var(--primary);
                transform: translateX(4px);
            }

            .quiz-option.correct {
                background: rgba(16, 185, 129, 0.1);
                border-color: var(--success);
            }

            .quiz-option.incorrect {
                background: rgba(239, 68, 68, 0.1);
                border-color: var(--error);
            }

            .stAlert {
                border-radius: 12px;
                border: 1px solid var(--line);
                animation: fadeIn 0.3s ease-in;
            }

            .bookmark-btn {
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid var(--line);
                border-radius: 50%;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s ease;
            }

            .bookmark-btn:hover {
                background: var(--primary);
                transform: scale(1.1);
            }

            .stat-card {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
                border: 1px solid var(--line);
                border-radius: 14px;
                padding: 1rem;
                text-align: center;
                transition: all 0.2s ease;
            }

            .stat-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            }

            .stat-value {
                font-size: 2rem;
                font-weight: 700;
                color: var(--primary);
            }

            .stat-label {
                font-size: 0.9rem;
                color: var(--text-muted);
                margin-top: 0.3rem;
            }

            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @media (max-width: 900px) {
                .hero-box {
                    padding: 1rem;
                    border-radius: 16px;
                }

                h1 {
                    font-size: 1.7rem !important;
                }

                .chip-row {
                    gap: 6px;
                }

                .chip {
                    font-size: 0.74rem;
                    padding: 4px 8px;
                }
            }

            /* Loading animation */
            .loading-spinner {
                border: 3px solid rgba(255, 255, 255, 0.1);
                border-top: 3px solid var(--primary);
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 2rem auto;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            /* Accessibility improvements */
            *:focus-visible {
                outline: 2px solid var(--primary);
                outline-offset: 2px;
            }

            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 10px;
            }

            ::-webkit-scrollbar-track {
                background: var(--bg-1);
            }

            ::-webkit-scrollbar-thumb {
                background: var(--line);
                border-radius: 5px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: var(--primary);
            }
        </style>
        """
    
    @staticmethod
    def get_light_theme() -> str:
        """
        Get light theme CSS.
        
        Returns:
            CSS string for light theme
        """
        return """
        <style>
            :root {
                --bg-0: #f8fafc;
                --bg-1: #f1f5f9;
                --bg-2: #e2e8f0;
                --card: rgba(255, 255, 255, 0.95);
                --text: #1e293b;
                --text-muted: #64748b;
                --line: rgba(100, 116, 139, 0.2);
                --shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                --primary: #667eea;
                --primary-light: #8b9ef5;
                --secondary: #764ba2;
                --success: #10b981;
                --error: #ef4444;
                --warning: #f59e0b;
            }

            .stApp {
                background: linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 50%, var(--bg-2) 100%);
                color: var(--text);
            }

            h1, h2, h3, h4, h5, h6 {
                color: var(--text);
            }

            .hero-box {
                background: var(--card);
                border: 1px solid var(--line);
                border-radius: 22px;
                padding: 1.5rem 1.8rem;
                box-shadow: var(--shadow);
                margin-bottom: 1.5rem;
            }

            .chip {
                background: rgba(102, 126, 234, 0.1);
                border: 1px solid var(--primary);
                color: var(--primary);
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border-right: 1px solid var(--line);
            }

            .stButton > button {
                background: linear-gradient(110deg, var(--primary), var(--primary-light));
                color: #ffffff !important;
            }

            .stTextArea textarea, .stTextInput input {
                background: white;
                border: 2px solid var(--line);
                color: var(--text);
            }

            .result-card {
                background: var(--card);
                border: 1px solid var(--line);
                box-shadow: var(--shadow);
            }

            .quiz-option {
                background: white;
                border: 2px solid var(--line);
            }

            .stat-card {
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
                border: 1px solid var(--line);
            }

            ::-webkit-scrollbar-track {
                background: var(--bg-1);
            }

            ::-webkit-scrollbar-thumb {
                background: var(--line);
            }
        </style>
        """
    
    @staticmethod
    def get_theme_css(theme: str = "dark") -> str:
        """
        Get CSS for specified theme.
        
        Args:
            theme: Theme name ('dark' or 'light')
        
        Returns:
            CSS string
        """
        if theme == "light":
            return UIStyles.get_light_theme()
        return UIStyles.get_dark_theme()
    
    @staticmethod
    def get_custom_components() -> Dict[str, str]:
        """
        Get custom HTML components.
        
        Returns:
            Dictionary of component names to HTML strings
        """
        return {
            "loading_spinner": '<div class="loading-spinner"></div>',
            "success_icon": '✅',
            "error_icon": '❌',
            "warning_icon": '⚠️',
            "info_icon": 'ℹ️',
            "bookmark_icon": '🔖',
            "star_icon": '⭐',
            "fire_icon": '🔥',
            "brain_icon": '🧠',
            "book_icon": '📚',
            "quiz_icon": '❓',
            "chart_icon": '📊',
        }

# Made with Bob
