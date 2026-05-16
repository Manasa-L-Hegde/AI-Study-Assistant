"""
Modern Professional UI Styling for AI Study Assistant.
Clean, elegant academic/professional design with soft gradients and glassmorphism.
"""

from typing import Dict


class ModernUIStyles:
    """Manager for modern professional UI styles."""
    
    @staticmethod
    def get_professional_theme() -> str:
        """
        Get modern professional theme CSS - Clean academic design.
        
        Returns:
            CSS string for professional theme
        """
        return """
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
            
            :root {
                /* Color Palette - Deep Blue & Indigo */
                --primary: #4F46E5;
                --primary-light: #6366F1;
                --primary-dark: #4338CA;
                --secondary: #7C3AED;
                --secondary-light: #8B5CF6;
                
                /* Backgrounds */
                --bg-primary: #FFFFFF;
                --bg-secondary: #F8FAFC;
                --bg-tertiary: #F1F5F9;
                --bg-card: rgba(255, 255, 255, 0.95);
                --bg-glass: rgba(255, 255, 255, 0.7);
                
                /* Text Colors */
                --text-primary: #0F172A;
                --text-secondary: #475569;
                --text-muted: #94A3B8;
                --text-inverse: #FFFFFF;
                
                /* Borders & Lines */
                --border-light: #E2E8F0;
                --border-medium: #CBD5E1;
                --border-dark: #94A3B8;
                
                /* Shadows */
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                --shadow-glow: 0 0 20px rgba(79, 70, 229, 0.3);
                
                /* Status Colors */
                --success: #10B981;
                --error: #EF4444;
                --warning: #F59E0B;
                --info: #3B82F6;
                
                /* Spacing */
                --spacing-xs: 0.25rem;
                --spacing-sm: 0.5rem;
                --spacing-md: 1rem;
                --spacing-lg: 1.5rem;
                --spacing-xl: 2rem;
                
                /* Border Radius */
                --radius-sm: 0.375rem;
                --radius-md: 0.5rem;
                --radius-lg: 0.75rem;
                --radius-xl: 1rem;
                --radius-2xl: 1.5rem;
                --radius-full: 9999px;
                
                /* Transitions */
                --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
                --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
                --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            /* Global Styles */
            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }
            
            .stApp {
                background: linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 50%, #E0E7FF 100%);
                color: var(--text-primary);
            }
            
            /* Typography */
            h1, h2, h3, h4, h5, h6 {
                color: var(--text-primary);
                font-weight: 700;
                letter-spacing: -0.025em;
                line-height: 1.2;
            }
            
            h1 {
                font-size: 2.5rem;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            h2 {
                font-size: 2rem;
                color: var(--primary-dark);
            }
            
            h3 {
                font-size: 1.5rem;
                color: var(--text-primary);
            }
            
            p {
                line-height: 1.7;
                color: var(--text-secondary);
            }
            
            code {
                font-family: 'JetBrains Mono', monospace;
                background: var(--bg-tertiary);
                padding: 0.125rem 0.375rem;
                border-radius: var(--radius-sm);
                font-size: 0.875em;
                color: var(--primary);
            }
            
            /* Hero Section */
            .hero-box {
                background: linear-gradient(135deg, 
                    rgba(255, 255, 255, 0.95) 0%, 
                    rgba(238, 242, 255, 0.95) 100%);
                backdrop-filter: blur(20px);
                border: 2px solid var(--border-light);
                border-radius: var(--radius-2xl);
                padding: var(--spacing-xl);
                box-shadow: var(--shadow-xl);
                margin-bottom: var(--spacing-xl);
                position: relative;
                overflow: hidden;
                animation: fadeInUp 0.6s ease-out;
            }
            
            .hero-box::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(79, 70, 229, 0.1) 0%, transparent 70%);
                animation: rotate 20s linear infinite;
            }
            
            .hero-box > * {
                position: relative;
                z-index: 1;
            }
            
            /* Feature Chips */
            .chip-row {
                display: flex;
                flex-wrap: wrap;
                gap: var(--spacing-sm);
                margin-top: var(--spacing-lg);
                justify-content: center;
            }
            
            .chip {
                background: linear-gradient(135deg, var(--primary), var(--primary-light));
                color: var(--text-inverse);
                border: none;
                border-radius: var(--radius-full);
                font-size: 0.875rem;
                font-weight: 600;
                padding: 0.5rem 1rem;
                transition: all var(--transition-base);
                box-shadow: var(--shadow-md);
                cursor: default;
            }
            
            .chip:hover {
                transform: translateY(-2px) scale(1.05);
                box-shadow: var(--shadow-lg), var(--shadow-glow);
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, 
                    rgba(255, 255, 255, 0.98) 0%, 
                    rgba(248, 250, 252, 0.98) 100%);
                backdrop-filter: blur(10px);
                border-right: 1px solid var(--border-light);
            }
            
            [data-testid="stSidebar"] .stMarkdown {
                color: var(--text-primary);
            }
            
            /* Buttons */
            .stButton > button {
                background: linear-gradient(135deg, var(--primary), var(--primary-light));
                color: var(--text-inverse) !important;
                border: none;
                border-radius: var(--radius-lg);
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                font-size: 1rem;
                box-shadow: var(--shadow-md);
                transition: all var(--transition-base);
                width: 100%;
                letter-spacing: 0.025em;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg), var(--shadow-glow);
                background: linear-gradient(135deg, var(--primary-light), var(--secondary));
            }
            
            .stButton > button:active {
                transform: translateY(0);
                box-shadow: var(--shadow-sm);
            }
            
            .stButton > button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            /* Input Fields */
            .stTextArea textarea, .stTextInput input {
                background: var(--bg-card);
                border: 2px solid var(--border-light);
                border-radius: var(--radius-lg);
                color: var(--text-primary);
                padding: 0.75rem 1rem;
                font-size: 1rem;
                transition: all var(--transition-base);
            }
            
            .stTextArea textarea:focus, .stTextInput input:focus {
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
                outline: none;
            }
            
            .stTextArea textarea::placeholder, .stTextInput input::placeholder {
                color: var(--text-muted);
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background: var(--bg-glass);
                backdrop-filter: blur(10px);
                border: 1px solid var(--border-light);
                border-radius: var(--radius-xl);
                padding: 0.375rem;
                gap: 0.25rem;
                box-shadow: var(--shadow-sm);
            }
            
            .stTabs [data-baseweb="tab"] {
                border-radius: var(--radius-lg);
                font-weight: 600;
                color: var(--text-secondary);
                transition: all var(--transition-base);
                padding: 0.75rem 1.5rem;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                background: rgba(79, 70, 229, 0.05);
                color: var(--primary);
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
                color: var(--text-inverse) !important;
                box-shadow: var(--shadow-md);
            }
            
            /* Content Cards */
            .content-card {
                background: var(--bg-card);
                backdrop-filter: blur(10px);
                border: 1px solid var(--border-light);
                border-radius: var(--radius-xl);
                padding: var(--spacing-lg);
                margin: var(--spacing-md) 0;
                box-shadow: var(--shadow-md);
                transition: all var(--transition-base);
                animation: fadeInUp 0.4s ease-out;
            }
            
            .content-card:hover {
                box-shadow: var(--shadow-lg);
                transform: translateY(-2px);
            }
            
            .result-card {
                background: var(--bg-card);
                border: 1px solid var(--border-light);
                border-left: 4px solid var(--primary);
                border-radius: var(--radius-lg);
                padding: var(--spacing-lg);
                margin-top: var(--spacing-md);
                box-shadow: var(--shadow-sm);
                animation: slideInLeft 0.3s ease-out;
            }
            
            /* Quiz Options */
            .quiz-option {
                background: var(--bg-card);
                border: 2px solid var(--border-light);
                border-radius: var(--radius-lg);
                padding: 1rem 1.25rem;
                margin: 0.5rem 0;
                cursor: pointer;
                transition: all var(--transition-base);
                font-weight: 500;
            }
            
            .quiz-option:hover {
                background: rgba(79, 70, 229, 0.05);
                border-color: var(--primary);
                transform: translateX(4px);
                box-shadow: var(--shadow-md);
            }
            
            .quiz-option.correct {
                background: rgba(16, 185, 129, 0.1);
                border-color: var(--success);
                color: var(--success);
            }
            
            .quiz-option.incorrect {
                background: rgba(239, 68, 68, 0.1);
                border-color: var(--error);
                color: var(--error);
            }
            
            /* Alerts */
            .stAlert {
                border-radius: var(--radius-lg);
                border: 1px solid var(--border-light);
                box-shadow: var(--shadow-sm);
                animation: fadeIn 0.3s ease-in;
            }
            
            /* Stats Cards */
            .stat-card {
                background: linear-gradient(135deg, 
                    rgba(79, 70, 229, 0.05) 0%, 
                    rgba(124, 58, 237, 0.05) 100%);
                border: 1px solid var(--border-light);
                border-radius: var(--radius-xl);
                padding: var(--spacing-lg);
                text-align: center;
                transition: all var(--transition-base);
                box-shadow: var(--shadow-sm);
            }
            
            .stat-card:hover {
                transform: translateY(-4px);
                box-shadow: var(--shadow-lg);
                border-color: var(--primary);
            }
            
            .stat-value {
                font-size: 2.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                line-height: 1;
            }
            
            .stat-label {
                font-size: 0.875rem;
                color: var(--text-secondary);
                margin-top: var(--spacing-sm);
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background: var(--bg-glass);
                border-radius: var(--radius-lg);
                border: 1px solid var(--border-light);
                font-weight: 600;
                transition: all var(--transition-base);
            }
            
            .streamlit-expanderHeader:hover {
                background: rgba(79, 70, 229, 0.05);
                border-color: var(--primary);
            }
            
            /* Metrics */
            [data-testid="stMetricValue"] {
                font-size: 2rem;
                font-weight: 700;
                color: var(--primary);
            }
            
            /* Loading Spinner */
            .stSpinner > div {
                border-color: var(--primary) transparent transparent transparent !important;
            }
            
            /* Scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--bg-secondary);
                border-radius: var(--radius-sm);
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--border-medium);
                border-radius: var(--radius-sm);
                transition: background var(--transition-base);
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--primary);
            }
            
            /* Animations */
            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes rotate {
                from {
                    transform: rotate(0deg);
                }
                to {
                    transform: rotate(360deg);
                }
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .hero-box {
                    padding: var(--spacing-lg);
                    border-radius: var(--radius-xl);
                }
                
                h1 {
                    font-size: 2rem;
                }
                
                h2 {
                    font-size: 1.5rem;
                }
                
                .chip {
                    font-size: 0.75rem;
                    padding: 0.375rem 0.75rem;
                }
                
                .stat-value {
                    font-size: 2rem;
                }
            }
            
            /* Accessibility */
            *:focus-visible {
                outline: 2px solid var(--primary);
                outline-offset: 2px;
                border-radius: var(--radius-sm);
            }
            
            /* Print Styles */
            @media print {
                .stButton, [data-testid="stSidebar"] {
                    display: none;
                }
                
                .content-card, .result-card {
                    break-inside: avoid;
                }
            }
        </style>
        """
    
    @staticmethod
    def get_dark_professional_theme() -> str:
        """
        Get dark professional theme CSS.
        
        Returns:
            CSS string for dark professional theme
        """
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
            
            :root {
                --primary: #6366F1;
                --primary-light: #818CF8;
                --primary-dark: #4F46E5;
                --secondary: #8B5CF6;
                --secondary-light: #A78BFA;
                
                --bg-primary: #0F172A;
                --bg-secondary: #1E293B;
                --bg-tertiary: #334155;
                --bg-card: rgba(30, 41, 59, 0.95);
                --bg-glass: rgba(30, 41, 59, 0.7);
                
                --text-primary: #F1F5F9;
                --text-secondary: #CBD5E1;
                --text-muted: #64748B;
                --text-inverse: #0F172A;
                
                --border-light: #334155;
                --border-medium: #475569;
                --border-dark: #64748B;
                
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
                --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
                --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.4);
                
                --success: #10B981;
                --error: #EF4444;
                --warning: #F59E0B;
                --info: #3B82F6;
            }
            
            .stApp {
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
                color: var(--text-primary);
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: var(--text-primary);
            }
            
            .hero-box {
                background: linear-gradient(135deg, 
                    rgba(30, 41, 59, 0.95) 0%, 
                    rgba(51, 65, 85, 0.95) 100%);
                backdrop-filter: blur(20px);
                border: 1px solid var(--border-light);
            }
            
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, 
                    rgba(15, 23, 42, 0.98) 0%, 
                    rgba(30, 41, 59, 0.98) 100%);
                border-right: 1px solid var(--border-light);
            }
            
            .stTextArea textarea, .stTextInput input {
                background: var(--bg-card);
                border-color: var(--border-light);
                color: var(--text-primary);
            }
            
            .content-card, .result-card {
                background: var(--bg-card);
                border-color: var(--border-light);
            }
            
            .quiz-option {
                background: var(--bg-card);
                border-color: var(--border-light);
                color: var(--text-primary);
            }
            
            code {
                background: var(--bg-tertiary);
                color: var(--primary-light);
            }
        </style>
        """
    
    @staticmethod
    def get_theme_css(theme: str = "light") -> str:
        """
        Get CSS for specified theme.
        
        Args:
            theme: Theme name ('light' or 'dark')
        
        Returns:
            CSS string
        """
        if theme == "dark":
            return ModernUIStyles.get_dark_professional_theme()
        return ModernUIStyles.get_professional_theme()


# Made with Bob