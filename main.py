"""
AI Study Assistant - Main Application
A comprehensive study tool powered by AI that generates explanations, notes, and quizzes.
"""

import streamlit as st
from datetime import datetime
import traceback

# Import custom modules
from src.config import settings
from src.utils import (
    api_client,
    session_manager,
    validate_topic,
    sanitize_text,
    extract_json,
    normalize_data,
    format_for_export,
    DataProcessor
)
from src.components.modern_ui_styles import ModernUIStyles
from src.components.ui_styles import UIStyles  # Keep for backward compatibility

# Page configuration
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "AI Study Assistant - Learn Smarter with AI 🚀",
        "Get Help": "https://github.com/yourusername/AI-Study-Assistant",
        "Report a bug": "https://github.com/yourusername/AI-Study-Assistant/issues"
    }
)

# Apply modern professional theme with safe fallback
try:
    current_theme = session_manager.get_theme()
    st.markdown(ModernUIStyles.get_theme_css(current_theme), unsafe_allow_html=True)
except Exception as e:
    st.error(f"Theme loading error: {e}")
    current_theme = "light"  # Default to light theme for professional look


def render_sidebar():
    """Render the sidebar with settings and navigation."""
    with st.sidebar:
        st.markdown("### 🎛️ Settings")
        
        # Theme toggle with safe attribute access
        enable_dark_mode = getattr(settings.features, "enable_dark_mode", True)
        if enable_dark_mode:
            try:
                theme_label = "🌙 Dark Mode" if current_theme == "dark" else "☀️ Light Mode"
                if st.button(theme_label, use_container_width=True):
                    new_theme = session_manager.toggle_theme()
                    st.rerun()
            except Exception as e:
                st.error(f"Theme toggle error: {e}")
        
        st.markdown("---")
        
        # API Key management
        if not settings.api.groq_api_key:
            st.warning("🔑 API Key not found")
            manual_key = st.text_input(
                "Enter Groq API Key",
                type="password",
                placeholder="gsk-...",
                help="Get your API key from https://console.groq.com"
            )
            if manual_key:
                if api_client.update_api_key(manual_key):
                    st.success("✅ API key validated!")
                else:
                    st.error("❌ Invalid API key format")
        else:
            st.success("✅ API Key configured")
            if st.checkbox("Use different key?"):
                manual_key = st.text_input(
                    "Enter Groq API Key",
                    type="password",
                    placeholder="gsk-..."
                )
                if manual_key:
                    api_client.update_api_key(manual_key)
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📑 Navigation")
        page = st.radio(
            "Go to",
            ["🏠 Home", "📊 Analytics", "🔖 Bookmarks", "📜 History"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick tips
        st.markdown("### 💡 Quick Tips")
        st.info(
            "**Try topics like:**\n"
            "- Machine Learning\n"
            "- Quantum Physics\n"
            "- Data Structures\n"
            "- World History\n"
            "- Biology Concepts"
        )
        
        st.markdown("---")
        
        # Useful links
        st.markdown("### 🔗 Useful Links")
        st.markdown("[📌 Get API Key](https://console.groq.com)")
        st.markdown("[⭐ GitHub](https://github.com)")
        st.markdown("[📖 Documentation](https://github.com)")
        
        return page


def render_hero():
    """Render the hero section."""
    st.markdown(
        """
        <div class="hero-box">
            <h1 style="margin:0; text-align:center; color:#ff6b9d;">✨ AI Study Assistant ✨</h1>
            <p style="text-align:center; margin:10px 0 0 0; font-size:1.1rem; color:#8b5a8e; font-weight:500;">
                🌸 Transform any topic into clear, concise explanations and fun quizzes! 🌸
            </p>
            <div class="chip-row">
                <span class="chip">💖 Super Easy</span>
                <span class="chip">⚡ Lightning Fast</span>
                <span class="chip">🎯 Precise Answers</span>
                <span class="chip">🧠 Smart Quizzes</span>
                <span class="chip">🌟 Track Progress</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_input_section():
    """Render the topic input section."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📝 What would you like to learn?")
        user_input = st.text_area(
            "Topic or concept",
            placeholder="e.g., Neural Networks, Photosynthesis, Binary Search Trees, Renaissance Art...",
            height=120,
            help="Enter any topic you want to learn about. Keep it focused for best results.",
            key="topic_input"
        )
    
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.caption("Click to generate")
        generate = st.button(
            "🚀 Generate Study Pack",
            use_container_width=True,
            disabled=not user_input.strip(),
            type="primary"
        )
    
    return user_input, generate


def render_study_material(topic: str, data: dict):
    """Render the generated study material."""
    st.success("✅ Study material generated successfully!")
    
    # Bookmark button with safe attribute access
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        enable_bookmarks = getattr(settings.features, "enable_bookmarks", True)
        if enable_bookmarks:
            try:
                is_bookmarked = session_manager.is_bookmarked(topic)
                bookmark_label = "🔖 Saved" if is_bookmarked else "🔖 Save"
                if st.button(bookmark_label, use_container_width=True):
                    if not is_bookmarked:
                        if session_manager.add_bookmark(topic, data):
                            st.success("Bookmark added!")
                            st.rerun()
                        else:
                            st.info("Already bookmarked!")
            except Exception as e:
                st.error(f"Bookmark error: {e}")
    
    with col3:
        enable_export = getattr(settings.features, "enable_export", True)
        if enable_export:
            try:
                export_format = st.selectbox(
                    "Export",
                    ["Markdown", "Text", "JSON"],
                    label_visibility="collapsed"
                )
                if st.button("📥 Export", use_container_width=True):
                    export_data = format_for_export(
                        data,
                        topic,
                        export_format.lower()
                    )
                    st.download_button(
                        "Download",
                        export_data,
                        file_name=f"{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.{export_format.lower()}",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Export error: {e}")
    
    st.markdown("---")
    
    # Tabs for content
    tab1, tab2, tab3 = st.tabs(["📘 Explanation", "📝 Notes", "❓ Quiz"])
    
    with tab1:
        render_explanation_tab(topic, data)
    
    with tab2:
        render_notes_tab(data)
    
    with tab3:
        render_quiz_tab(data)


def render_explanation_tab(topic: str, data: dict):
    """Render the explanation tab."""
    with st.container(border=True):
        st.markdown(f"### 📖 {topic.title()}")
        st.markdown(
            f"<div class='result-card'>{data['explanation']}</div>",
            unsafe_allow_html=True
        )
        
        # Show statistics
        stats = DataProcessor.calculate_study_stats(data)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Words", stats['explanation_words'])
        with col2:
            st.metric("Read Time", f"{stats['estimated_read_time']} min")
        with col3:
            st.metric("Notes", stats['notes_count'])


def render_notes_tab(data: dict):
    """Render the notes tab."""
    with st.container(border=True):
        st.markdown("### 📌 Key Points to Remember")
        
        for idx, note in enumerate(data["notes"], 1):
            st.markdown(
                f"<div class='result-card'>"
                f"<strong>📍 Point {idx}:</strong> {note}"
                f"</div>",
                unsafe_allow_html=True
            )


def render_quiz_tab(data: dict):
    """Render the quiz tab with interactive questions."""
    with st.container(border=True):
        st.markdown("### 🧠 Test Your Knowledge")
        st.caption("Click on an option to check your answer")
        
        if "quiz_selected" not in st.session_state:
            st.session_state["quiz_selected"] = {}
        
        for idx, q in enumerate(data["quiz"], 1):
            st.markdown(f"**Question {idx}:** {q['question']}")
            
            options = [str(opt) for opt in q.get("options", [])]
            correct_answer = DataProcessor.resolve_correct_option(
                q.get("answer", ""),
                options
            )
            state_key = f"selected_{idx}"
            
            # Create option buttons
            cols = st.columns(len(options))
            for i, (col, opt) in enumerate(zip(cols, options)):
                with col:
                    if st.button(
                        opt,
                        key=f"q{idx}_{i}",
                        use_container_width=True
                    ):
                        st.session_state["quiz_selected"][state_key] = opt
            
            # Show result
            selected = st.session_state["quiz_selected"].get(state_key)
            if selected:
                is_correct = (
                    DataProcessor.normalize_option_text(selected) ==
                    DataProcessor.normalize_option_text(correct_answer)
                )
                
                if is_correct:
                    st.success(f"✅ Correct! {selected}")
                    session_manager.record_quiz_answer(f"q{idx}", True)
                else:
                    st.error(f"❌ Wrong. You selected: {selected}")
                    st.info(f"💡 Correct answer: {correct_answer}")
                    session_manager.record_quiz_answer(f"q{idx}", False)
            
            st.divider()


def render_analytics_page():
    """Render the analytics dashboard."""
    st.markdown("## 📊 Your Study Analytics")
    
    analytics = session_manager.get_analytics()
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{analytics['total_topics']}</div>
                <div class="stat-label">Topics Studied</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{analytics['total_questions']}</div>
                <div class="stat-label">Questions Answered</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{analytics['accuracy']:.1f}%</div>
                <div class="stat-label">Accuracy</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{analytics['session_duration'] // 60}</div>
                <div class="stat-label">Minutes Active</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Session summary
    summary = session_manager.get_session_summary()
    st.markdown("### 📈 Session Summary")
    st.json(summary)
    
    # Reset button
    if st.button("🔄 Reset Analytics", type="secondary"):
        session_manager.reset_analytics()
        st.success("Analytics reset!")
        st.rerun()


def render_bookmarks_page():
    """Render the bookmarks page."""
    st.markdown("## 🔖 Your Bookmarks")
    
    bookmarks = session_manager.get_bookmarks()
    
    if not bookmarks:
        st.info("No bookmarks yet. Save your favorite study materials!")
        return
    
    for bookmark in bookmarks:
        with st.expander(f"📚 {bookmark['topic']} - {bookmark['timestamp'][:10]}"):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                st.markdown(f"**Explanation:** {bookmark['data']['explanation'][:200]}...")
            
            with col2:
                if st.button("🗑️ Remove", key=f"remove_{bookmark['id']}"):
                    session_manager.remove_bookmark(bookmark['id'])
                    st.success("Bookmark removed!")
                    st.rerun()
            
            if st.button("📖 Load", key=f"load_{bookmark['id']}"):
                session_manager.save_study_data(bookmark['topic'], bookmark['data'])
                st.success("Loaded!")
                st.rerun()


def render_history_page():
    """Render the history page."""
    st.markdown("## 📜 Study History")
    
    history = session_manager.get_history(limit=20)
    
    if not history:
        st.info("No history yet. Start studying to build your history!")
        return
    
    for entry in history:
        with st.expander(f"📚 {entry['topic']} - {entry['timestamp'][:16]}"):
            st.markdown(f"**Explanation:** {entry['data']['explanation'][:200]}...")
            
            if st.button("📖 Load", key=f"load_history_{entry['id']}"):
                session_manager.save_study_data(entry['topic'], entry['data'])
                st.success("Loaded!")
                st.rerun()
    
    if st.button("🗑️ Clear History", type="secondary"):
        session_manager.clear_history()
        st.success("History cleared!")
        st.rerun()


def main():
    """Main application logic."""
    # Render sidebar and get current page
    page = render_sidebar()
    
    # Route to appropriate page
    if page == "📊 Analytics":
        render_analytics_page()
    elif page == "🔖 Bookmarks":
        render_bookmarks_page()
    elif page == "📜 History":
        render_history_page()
    else:
        # Home page
        render_hero()
        
        # Input section
        user_input, generate = render_input_section()
        
        # Handle generation with comprehensive error handling
        if generate:
            try:
                # Validate input with safe attribute access
                max_length = getattr(settings.app, "max_topic_length", 1000)
                is_valid, error_msg = validate_topic(user_input, max_length)
                
                if not is_valid:
                    st.error(f"❌ {error_msg}")
                elif not api_client.is_configured():
                    st.error("❌ API key not configured. Check the settings in the sidebar.")
                else:
                    # Sanitize input
                    clean_topic = sanitize_text(user_input)
                    
                    with st.spinner("🤖 Generating study material..."):
                        # Call API
                        response = api_client.generate_study_material(clean_topic)
                        
                        if response["success"]:
                            try:
                                # Parse and normalize data
                                raw_data = extract_json(response["content"])
                                normalized_data = normalize_data(raw_data)
                                
                                # Save to session
                                session_manager.save_study_data(clean_topic, normalized_data)
                                
                                st.rerun()
                            
                            except Exception as e:
                                st.error(f"❌ Failed to parse response: {str(e)}")
                                with st.expander("Show raw output"):
                                    st.code(response["content"], language="text")
                        else:
                            st.error(f"❌ {response['message']}")
                            debug_mode = getattr(settings.app, "debug", False)
                            if debug_mode:
                                st.error(f"Details: {response.get('details', 'N/A')}")
            
            except Exception as e:
                st.error(f"❌ Unexpected error during generation: {str(e)}")
                import traceback
                with st.expander("Show error details"):
                    st.code(traceback.format_exc())
        
        # Display current study material if available
        current_data = session_manager.get_study_data()
        current_topic = session_manager.get_study_topic()
        
        if current_data and current_topic:
            render_study_material(current_topic, current_data)


if __name__ == "__main__":
    main()

# Made with Bob
