"""
AI Study Assistant - Upgraded Main Application v2.0
A comprehensive, professional study tool powered by AI with modern UI and advanced features.
"""

import streamlit as st
from datetime import datetime
import traceback
import json

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
from src.utils.session_manager import initialize_session_state
from src.components.modern_ui_styles import ModernUIStyles
from src.components.diagram_renderer import DiagramRenderer, CodeRenderer

# Page configuration
st.set_page_config(
    page_title="AI Study Assistant - Professional Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "AI Study Assistant v2.0 - Professional Learning Platform 🚀",
        "Get Help": "https://github.com/yourusername/AI-Study-Assistant",
        "Report a bug": "https://github.com/yourusername/AI-Study-Assistant/issues"
    }
)

# CRITICAL: Initialize session state FIRST to prevent KeyError crashes
# This must happen BEFORE any UI rendering or session_state access
# This prevents deployment crashes on Streamlit Cloud where session state is fresh
initialize_session_state()

# Apply modern professional theme (light mode only)
try:
    st.markdown(ModernUIStyles.get_theme_css("light"), unsafe_allow_html=True)
except Exception as e:
    st.error(f"Theme loading error: {e}")


def render_sidebar():
    """Render the enhanced sidebar with settings and navigation."""
    with st.sidebar:
        # Logo/Title
        st.markdown("# 🎓 AI Study Assistant")
        st.markdown("*Professional Learning Platform*")
        st.markdown("---")
        
        # Settings Section
        st.markdown("### ⚙️ Settings")
        
        # Study Mode Selection with safe initialization
        st.markdown("#### 📚 Study Mode")
        
        # Get current mode safely
        current_mode = st.session_state.get("study_mode", "comprehensive")
        default_index = 0 if current_mode == "comprehensive" else 1
        
        study_mode = st.radio(
            "Select mode",
            ["Comprehensive", "Quick"],
            index=default_index,
            help="Comprehensive: Detailed explanations with diagrams\nQuick: Concise summaries",
            label_visibility="collapsed"
        )
        
        # Update session state safely
        st.session_state["study_mode"] = study_mode.lower()
        
        st.markdown("---")
        
        # API Key management
        if not settings.api.groq_api_key:
            st.warning("🔑 API Key Required")
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
            st.success("✅ API Key Configured")
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
        
        # Quick Stats
        analytics = session_manager.get_analytics()
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Topics", analytics.get("total_topics", 0))
        with col2:
            st.metric("Accuracy", f"{analytics.get('accuracy', 0):.0f}%")
        
        st.markdown("---")
        
        # Quick Tips
        st.markdown("### 💡 Study Tips")
        st.info(
            "**Try these topics:**\n"
            "- Machine Learning Basics\n"
            "- Quantum Computing\n"
            "- Data Structures\n"
            "- World History Events\n"
            "- Biology Concepts"
        )
        
        st.markdown("---")
        
        # Links
        st.markdown("### 🔗 Resources")
        st.markdown("[📌 Get API Key](https://console.groq.com)")
        st.markdown("[⭐ GitHub](https://github.com)")
        st.markdown("[📖 Documentation](https://github.com)")
        
        return page


def render_hero():
    """Render the enhanced hero section."""
    st.markdown(
        """
        <div class="hero-box">
            <h1 style="margin:0; text-align:center;">🎓 AI Study Assistant</h1>
            <p style="text-align:center; margin:10px 0 0 0; font-size:1.2rem; font-weight:500; color: var(--text-secondary);">
                Transform any topic into comprehensive, structured learning material
            </p>
            <div class="chip-row">
                <span class="chip">📚 Detailed Explanations</span>
                <span class="chip">📊 Visual Diagrams</span>
                <span class="chip">💡 Real Examples</span>
                <span class="chip">🧠 Smart Quizzes</span>
                <span class="chip">📈 Track Progress</span>
                <span class="chip">⚡ AI-Powered</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_input_section():
    """Render the enhanced topic input section."""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown("### 📝 What would you like to learn today?")
        user_input = st.text_area(
            "Enter your topic",
            placeholder="e.g., Neural Networks, Photosynthesis, Binary Search Trees, Renaissance Art, Quantum Mechanics...",
            height=120,
            help="Enter any topic you want to learn about. Be specific for best results.",
            key="topic_input"
        )
    
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.caption("Generate study material")
        generate = st.button(
            "🚀 Generate",
            use_container_width=True,
            disabled=not user_input.strip(),
            type="primary"
        )
    
    return user_input, generate


def render_comprehensive_content(topic: str, data: dict):
    """Render comprehensive study material with all features."""
    st.success("✅ Study material generated successfully!")
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
    
    with col1:
        enable_bookmarks = getattr(settings.features, "enable_bookmarks", True)
        if enable_bookmarks:
            try:
                is_bookmarked = session_manager.is_bookmarked(topic)
                if st.button("🔖 Save" if not is_bookmarked else "✓ Saved", use_container_width=True):
                    if not is_bookmarked:
                        session_manager.add_bookmark(topic, data)
                        st.success("Bookmarked!")
                        st.rerun()
            except Exception as e:
                st.error(f"Bookmark error: {e}")
    
    with col2:
        if st.button("🔄 New Topic", use_container_width=True):
            session_manager.clear_study_data()
            st.rerun()
    
    with col3:
        enable_export = getattr(settings.features, "enable_export", True)
        if enable_export:
            try:
                export_format = st.selectbox(
                    "Format",
                    ["PDF", "Markdown", "JSON"],
                    label_visibility="collapsed"
                )
            except Exception:
                pass
    
    st.markdown("---")
    
    # Main content tabs
    tabs = st.tabs([
        "📘 Explanation",
        "🔑 Key Concepts",
        "📊 Visual Diagram",
        "💡 Examples",
        "📝 Quick Revision",
        "🎯 Interview Points",
        "❓ Quiz"
    ])
    
    # Tab 1: Detailed Explanation
    with tabs[0]:
        render_explanation_tab(topic, data)
    
    # Tab 2: Key Concepts
    with tabs[1]:
        render_key_concepts_tab(data)
    
    # Tab 3: Visual Diagram
    with tabs[2]:
        render_diagram_tab(data)
    
    # Tab 4: Examples
    with tabs[3]:
        render_examples_tab(data)
    
    # Tab 5: Quick Revision
    with tabs[4]:
        render_quick_revision_tab(data)
    
    # Tab 6: Interview Points
    with tabs[5]:
        render_interview_points_tab(data)
    
    # Tab 7: Quiz
    with tabs[6]:
        render_enhanced_quiz_tab(data)


def render_explanation_tab(topic: str, data: dict):
    """Render the detailed explanation tab."""
    st.markdown(f"## 📖 {topic.title()}")
    
    explanation = data.get("explanation", "No explanation available")
    
    # Render explanation in a nice card
    st.markdown(
        f'<div class="content-card">{explanation}</div>',
        unsafe_allow_html=True
    )
    
    # Show detailed breakdown if available
    detailed_breakdown = data.get("detailed_breakdown", {})
    if detailed_breakdown:
        st.markdown("### 🔍 Detailed Breakdown")
        
        for key, value in detailed_breakdown.items():
            title = key.replace("_", " ").title()
            with st.expander(f"**{title}**", expanded=False):
                st.markdown(value)
    
    # Statistics
    stats = DataProcessor.calculate_study_stats(data)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Words", stats.get('explanation_words', 0))
    with col2:
        st.metric("Read Time", f"{stats.get('estimated_read_time', 0)} min")
    with col3:
        st.metric("Concepts", len(data.get('key_concepts', [])))
    with col4:
        st.metric("Examples", len(data.get('examples', [])))


def render_key_concepts_tab(data: dict):
    """Render key concepts tab."""
    st.markdown("### 🔑 Key Concepts")
    
    key_concepts = data.get("key_concepts", data.get("notes", []))
    
    if key_concepts:
        for idx, concept in enumerate(key_concepts, 1):
            st.markdown(
                f'<div class="content-card">**{idx}.** {concept}</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("No key concepts available")


def render_diagram_tab(data: dict):
    """Render visual diagram tab."""
    diagram_data = data.get("visual_diagram", {})
    
    if diagram_data and diagram_data.get("mermaid_code"):
        DiagramRenderer.render_diagram_from_data(diagram_data)
    else:
        st.info("💡 No diagram available for this topic. Diagrams are generated for topics that benefit from visual representation.")


def render_examples_tab(data: dict):
    """Render examples tab."""
    st.markdown("### 💡 Real-World Examples")
    
    examples = data.get("examples", [])
    
    if examples:
        for idx, example in enumerate(examples, 1):
            with st.expander(f"**Example {idx}: {example.get('title', 'Example')}**", expanded=True):
                st.markdown(f"**Description:** {example.get('description', '')}")
                st.markdown(f"**Why it matters:** {example.get('explanation', '')}")
    else:
        st.info("No examples available")
    
    # Render formulas or code if available
    formulas_or_code = data.get("formulas_or_code", [])
    if formulas_or_code:
        st.markdown("### 📐 Formulas & Code")
        for item in formulas_or_code:
            st.markdown(f"**{item.get('title', 'Formula')}**")
            st.code(item.get('content', ''), language="python")
            st.caption(item.get('explanation', ''))


def render_quick_revision_tab(data: dict):
    """Render quick revision tab."""
    st.markdown("### ⚡ Quick Revision Points")
    
    quick_revision = data.get("quick_revision", [])
    
    if quick_revision:
        for idx, point in enumerate(quick_revision, 1):
            st.markdown(f"**{idx}.** {point}")
    else:
        st.info("No quick revision points available")
    
    # Common mistakes
    common_mistakes = data.get("common_mistakes", [])
    if common_mistakes:
        st.markdown("### ⚠️ Common Mistakes to Avoid")
        for mistake in common_mistakes:
            st.warning(mistake)
    
    # Related topics
    related_topics = data.get("related_topics", [])
    if related_topics:
        st.markdown("### 🔗 Related Topics")
        cols = st.columns(3)
        for idx, topic in enumerate(related_topics):
            with cols[idx % 3]:
                st.info(topic)


def render_interview_points_tab(data: dict):
    """Render interview/exam points tab."""
    st.markdown("### 🎯 Important Interview & Exam Points")
    
    interview_points = data.get("interview_points", [])
    
    if interview_points:
        for idx, point in enumerate(interview_points, 1):
            st.markdown(
                f'<div class="content-card">**Point {idx}:** {point}</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("No interview points available")


def render_enhanced_quiz_tab(data: dict):
    """Render enhanced quiz tab with explanations."""
    st.markdown("### 🧠 Test Your Knowledge")
    st.caption("Select an answer to see if you're correct")
    
    if "quiz_selected" not in st.session_state:
        st.session_state["quiz_selected"] = {}
    
    quiz_questions = data.get("quiz", [])
    
    if not quiz_questions:
        st.info("No quiz questions available")
        return
    
    for idx, q in enumerate(quiz_questions, 1):
        st.markdown(f"#### Question {idx}")
        st.markdown(f"**{q.get('question', 'Question not available')}**")
        
        options = [str(opt) for opt in q.get("options", [])]
        correct_answer = DataProcessor.resolve_correct_option(
            q.get("answer", ""),
            options
        )
        state_key = f"selected_{idx}"
        
        # Create option buttons
        cols = st.columns(len(options) if len(options) <= 4 else 2)
        for i, opt in enumerate(options):
            with cols[i % len(cols)]:
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
                st.error(f"❌ Incorrect. You selected: {selected}")
                st.info(f"💡 Correct answer: {correct_answer}")
                session_manager.record_quiz_answer(f"q{idx}", False)
            
            # Show explanation if available
            explanation = q.get("explanation", "")
            if explanation:
                with st.expander("📖 Explanation"):
                    st.markdown(explanation)
        
        st.divider()


def render_analytics_page():
    """Render the analytics dashboard."""
    st.markdown("## 📊 Your Learning Analytics")
    
    analytics = session_manager.get_analytics()
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{analytics.get('total_topics', 0)}</div>
                <div class="stat-label">Topics Studied</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{analytics.get('total_questions', 0)}</div>
                <div class="stat-label">Questions Answered</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{analytics.get('accuracy', 0):.1f}%</div>
                <div class="stat-label">Accuracy</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{analytics.get('session_duration', 0) // 60}</div>
                <div class="stat-label">Minutes Active</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Session summary
    summary = session_manager.get_session_summary()
    st.markdown("### 📈 Session Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.json(summary)
    
    with col2:
        if st.button("🔄 Reset Analytics", type="secondary"):
            session_manager.reset_analytics()
            st.success("Analytics reset!")
            st.rerun()


def render_bookmarks_page():
    """Render the bookmarks page."""
    st.markdown("## 🔖 Your Saved Bookmarks")
    
    bookmarks = session_manager.get_bookmarks()
    
    if not bookmarks:
        st.info("📚 No bookmarks yet. Save your favorite study materials to access them quickly!")
        return
    
    for bookmark in bookmarks:
        with st.expander(f"📚 {bookmark['topic']} - {bookmark['timestamp'][:10]}"):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                explanation = bookmark['data'].get('explanation', '')
                preview = explanation[:300] + "..." if len(explanation) > 300 else explanation
                st.markdown(f"**Preview:** {preview}")
            
            with col2:
                if st.button("🗑️", key=f"remove_{bookmark['id']}", help="Remove bookmark"):
                    session_manager.remove_bookmark(bookmark['id'])
                    st.success("Removed!")
                    st.rerun()
            
            if st.button("📖 Load This Topic", key=f"load_{bookmark['id']}", use_container_width=True):
                session_manager.save_study_data(bookmark['topic'], bookmark['data'])
                st.success("Loaded! Go to Home to view.")
                st.rerun()


def render_history_page():
    """Render the history page."""
    st.markdown("## 📜 Study History")
    
    history = session_manager.get_history(limit=20)
    
    if not history:
        st.info("📖 No history yet. Start studying to build your learning history!")
        return
    
    for entry in history:
        with st.expander(f"📚 {entry['topic']} - {entry['timestamp'][:16]}"):
            explanation = entry['data'].get('explanation', '')
            preview = explanation[:300] + "..." if len(explanation) > 300 else explanation
            st.markdown(f"**Preview:** {preview}")
            
            if st.button("📖 Load", key=f"load_history_{entry['id']}", use_container_width=True):
                session_manager.save_study_data(entry['topic'], entry['data'])
                st.success("Loaded! Go to Home to view.")
                st.rerun()
    
    if st.button("🗑️ Clear All History", type="secondary"):
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
        
        # Handle generation
        if generate:
            try:
                # Validate input with safe attribute access
                max_length = getattr(settings.app, "max_topic_length", 1000)
                is_valid, error_msg = validate_topic(user_input, max_length)
                
                if not is_valid:
                    st.error(f"❌ {error_msg}")
                elif not api_client.is_configured():
                    st.error("❌ API key not configured. Please add your Groq API key in the sidebar.")
                else:
                    # Sanitize input
                    clean_topic = sanitize_text(user_input)
                    
                    # Get study mode
                    study_mode = st.session_state.get("study_mode", "comprehensive")
                    
                    with st.spinner(f"🤖 Generating {study_mode} study material..."):
                        # Call API with mode
                        response = api_client.generate_study_material(clean_topic, mode=study_mode)
                        
                        if response["success"]:
                            try:
                                # Use pre-parsed data from API client (already validated)
                                if "parsed_data" in response:
                                    normalized_data = response["parsed_data"]
                                else:
                                    # Fallback to manual parsing (shouldn't happen with new system)
                                    from src.utils.robust_json_parser import RobustJSONParser
                                    normalized_data = RobustJSONParser.extract_and_parse_json(response["content"])
                                
                                # Check if there was a parsing error
                                if "parsing_error" in response:
                                    st.warning(f"⚠️ Response was partially parsed. Some features may be limited.")
                                
                                # Save to session
                                session_manager.save_study_data(clean_topic, normalized_data)
                                
                                st.rerun()
                            
                            except Exception as e:
                                st.error(f"❌ Failed to process response: {str(e)}")
                                with st.expander("Show raw output for debugging"):
                                    st.code(response.get("content", "No content")[:1000], language="text")
                                with st.expander("Show error details"):
                                    st.code(traceback.format_exc())
                        else:
                            st.error(f"❌ {response['message']}")
                            debug_mode = getattr(settings.app, "debug", False)
                            if debug_mode:
                                st.error(f"Details: {response.get('details', 'N/A')}")
            
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                with st.expander("Show error details"):
                    st.code(traceback.format_exc())
        
        # Display current study material if available
        current_data = session_manager.get_study_data()
        current_topic = session_manager.get_study_topic()
        
        if current_data and current_topic:
            render_comprehensive_content(current_topic, current_data)


if __name__ == "__main__":
    main()

# Made with Bob - AI Study Assistant v2.0