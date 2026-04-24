import os
import json
import streamlit as st
from openai import OpenAI

# Page config with custom theme
st.set_page_config(
    page_title="AI Study Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "AI Study Assistant - Learn Smarter with AI 🚀"}
)

# Custom CSS for cute design
st.markdown("""
<style>
    /* Gradient background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Title styling */
    h1 {
        color: #667eea;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #764ba2;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5em;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 1.1em;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #667eea;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        border-radius: 10px;
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Read Groq API key from environment first, then allow manual input as fallback.
api_key = (os.getenv("GROQ_API_KEY") or "").strip()
model_name = (os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant").strip()

# Sidebar for API key management and settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if not api_key:
        st.warning("🔑 API Key not found in environment")
        api_key = st.text_input("Enter Groq API Key", type="password", placeholder="gsk-...").strip()
    else:
        st.success("✅ API Key loaded from environment")
        if st.checkbox("Use different key?"):
            api_key = st.text_input("Enter Groq API Key", type="password", placeholder="gsk-...").strip()
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.info("Try topics like:\n- Python\n- Machine Learning\n- Data Science\n- Biology\n- History")
    
    st.markdown("---")
    st.markdown("### 🔗 Useful Links")
    st.markdown("[📌 Get Groq API Key](https://console.groq.com)")
    st.markdown("[⭐ GitHub](https://github.com)")

client = None
if api_key:
    if api_key.startswith("gsk_") or api_key.startswith("gsk-"):
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    else:
        st.error("❌ Invalid key format. Your Groq key should start with 'gsk_' or 'gsk-'.")

# Main title
st.markdown("<h1>📚 AI Study Assistant</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #764ba2; font-size: 1.2em; margin-bottom: 2em;'>🎯 Learn Smarter with AI | Get Explanations, Notes & Quizzes</div>", unsafe_allow_html=True)

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 📝 What would you like to learn?")
    user_input = st.text_area(
        "Enter topic or concept:",
        placeholder="e.g., PCA, Binary Search, Data Drift, Photosynthesis...",
        height=100
    )

with col2:
    st.write("")
    st.write("")
    st.write("")
    generate = st.button("🚀 Generate", use_container_width=True)

if generate:
    if user_input.strip() == "":
        st.error("⚠️ Please enter a topic to learn about!")
    elif client is None:
        st.error("❌ API key not configured. Check the settings in the sidebar.")
    else:
        with st.spinner("🤖 Generating study material..."):
            prompt = f"""
Give output ONLY in JSON format like this:

{{
    "explanation": "...",
    "notes": ["point1", "point2", "point3"],
    "quiz": [
        {{
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "answer": "..."
        }}
    ]
}}

Topic: {user_input}
Explain in simple terms.
"""

            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                output = response.choices[0].message.content

                try:
                    data = json.loads(output)

                    st.success("✅ Study material generated successfully!")
                    st.markdown("---")

                    # Tabs for better organization
                    tab1, tab2, tab3 = st.tabs(["📘 Explanation", "📝 Notes", "❓ Quiz"])

                    with tab1:
                        st.markdown(f"### 📖 {user_input.title()}")
                        st.markdown(data["explanation"])

                    with tab2:
                        st.markdown("### 📌 Key Points")
                        for idx, note in enumerate(data["notes"], 1):
                            st.markdown(f"**{idx}.** ✨ {note}")

                    with tab3:
                        st.markdown("### 🧠 Test Your Knowledge")
                        for idx, q in enumerate(data["quiz"], 1):
                            with st.container():
                                st.markdown(f"**Question {idx}:** {q['question']}")
                                st.markdown("**Options:**")
                                for opt in q["options"]:
                                    st.markdown(f"  • {opt}")
                                st.markdown(f"**✅ Correct Answer:** {q['answer']}")
                                st.divider()

                except json.JSONDecodeError:
                    st.error("❌ Formatting issue. Showing raw output:")
                    st.code(output, language="text")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try checking your API key or try again in a few seconds.")
