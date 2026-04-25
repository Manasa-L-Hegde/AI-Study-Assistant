import os
import json
import re
import streamlit as st
from openai import OpenAI, APIError, AuthenticationError, RateLimitError, BadRequestError, APITimeoutError

# Page config with custom theme
st.set_page_config(
    page_title="AI Study Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "AI Study Assistant - Learn Smarter with AI 🚀"}
)

# Custom CSS for a dark, responsive cute design
st.markdown("""
<style>
    :root {
        --bg-0: #0b1220;
        --bg-1: #111b2e;
        --bg-2: #14233a;
        --card: rgba(17, 27, 46, 0.78);
        --mint: #86efac;
        --cyan: #67e8f9;
        --amber: #fbbf24;
        --text: #e7edf8;
        --muted: #9fb0ca;
        --line: rgba(148, 163, 184, 0.28);
        --soft-shadow: 0 14px 34px rgba(2, 6, 23, 0.45);
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 8%, rgba(103, 232, 249, 0.10) 0 20%, transparent 21%),
            radial-gradient(circle at 86% 22%, rgba(251, 191, 36, 0.12) 0 16%, transparent 17%),
            linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 45%, var(--bg-2) 100%);
        color: var(--text);
    }

    h1, h2, h3 {
        color: var(--text);
        letter-spacing: 0.2px;
    }

    .hero-box {
        backdrop-filter: blur(6px);
        background: linear-gradient(120deg, rgba(22, 35, 58, 0.88), rgba(17, 27, 46, 0.88));
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 1.1rem 1.2rem;
        box-shadow: var(--soft-shadow);
        margin-bottom: 1rem;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 8px;
    }

    .chip {
        background: rgba(15, 23, 42, 0.62);
        border: 1px solid var(--line);
        color: var(--text);
        border-radius: 999px;
        font-size: 0.82rem;
        padding: 5px 10px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e1729 0%, #121f36 100%);
        border-right: 1px solid var(--line);
    }

    .stButton > button {
        background: linear-gradient(110deg, #22d3ee, #34d399);
        color: #0a1526;
        border: 0;
        border-radius: 16px;
        padding: 0.62rem 0.95rem;
        font-weight: 700;
        box-shadow: 0 10px 22px rgba(16, 185, 129, 0.30);
        transition: transform .15s ease, box-shadow .15s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 24px rgba(34, 211, 238, 0.35);
    }

    .stTextArea textarea {
        border-radius: 14px;
        border: 2px solid rgba(103, 232, 249, 0.35);
        background: rgba(15, 23, 42, 0.66);
        color: var(--text);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.80), rgba(30, 41, 59, 0.80));
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-weight: 600;
        color: var(--text);
    }

    .stAlert {
        border-radius: 12px;
        border: 1px solid var(--line);
    }

    p, label, .stCaption, .stMarkdown {
        color: var(--text);
    }

    @media (max-width: 900px) {
        .hero-box {
            padding: 0.95rem;
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
</style>
""", unsafe_allow_html=True)

# Read Groq API key from environment first, then allow manual input as fallback.
env_api_key = (os.getenv("GROQ_API_KEY") or "").strip()
model_name = (os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant").strip()

# Sidebar for API key management and settings
with st.sidebar:
    st.markdown("### 🎛️ Settings")
    if not env_api_key:
        st.warning("🔑 API Key not found in environment")
        manual_api_key = st.text_input("Enter Groq API Key", type="password", placeholder="gsk-...").strip()
    else:
        st.success("✅ API Key loaded from environment")
        if st.checkbox("Use different key?"):
            manual_api_key = st.text_input("Enter Groq API Key", type="password", placeholder="gsk-...").strip()
        else:
            manual_api_key = ""

    st.markdown("---")
    st.markdown("### 🌟 Quick Tips")
    st.info("Try topics like:\n- Python\n- Machine Learning\n- Data Science\n- Biology\n- History")
    
    st.markdown("---")
    st.markdown("### 🔗 Useful Links")
    st.markdown("[📌 Get Groq API Key](https://console.groq.com)")
    st.markdown("[⭐ GitHub](https://github.com)")

api_key = env_api_key or manual_api_key

client = None
if api_key:
    if api_key.startswith("gsk_") or api_key.startswith("gsk-"):
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    else:
        st.error("❌ Invalid key format. Your Groq key should start with 'gsk_' or 'gsk-'.")


def extract_json_payload(text: str) -> dict:
    """Best-effort extraction of a JSON object from LLM output."""
    candidates = []
    cleaned = (text or "").strip()

    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", cleaned, re.IGNORECASE)
    if fenced:
        candidates.append(fenced.group(1).strip())

    object_start = cleaned.find("{")
    object_end = cleaned.rfind("}")
    if object_start != -1 and object_end != -1 and object_end > object_start:
        candidates.append(cleaned[object_start : object_end + 1])

    array_start = cleaned.find("[")
    array_end = cleaned.rfind("]")
    if array_start != -1 and array_end != -1 and array_end > array_start:
        candidates.append(cleaned[array_start : array_end + 1])

    candidates.append(cleaned)

    last_error = None
    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as exc:
            last_error = exc

    raise last_error or json.JSONDecodeError("No valid JSON found", cleaned, 0)


def normalize_study_data(raw_data: dict) -> dict:
    """Normalize LLM response so the UI can always render safely."""
    notes = raw_data.get("notes", [])
    quiz_items = raw_data.get("quiz", [])

    if not isinstance(notes, list):
        notes = [str(notes)] if notes else []

    if not isinstance(quiz_items, list):
        quiz_items = []

    normalized_quiz = []
    for item in quiz_items:
        if isinstance(item, dict):
            normalized_quiz.append(
                {
                    "question": str(item.get("question", "Question unavailable.")),
                    "options": item.get("options", ["Option unavailable"]),
                    "answer": str(item.get("answer", "Answer unavailable.")),
                }
            )

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

# Main title
st.markdown(
    """
    <div class="hero-box">
        <h1 style="margin:0; text-align:center;">📚 AI Study Assistant</h1>
        <p style="text-align:center; margin:8px 0 0 0; font-size:1.05rem; color:#cbd5e1;">
            Cute, quick study support with explanations, short notes, and quiz practice.
        </p>
        <div class="chip-row">
            <span class="chip">Beginner Friendly</span>
            <span class="chip">Fast Summaries</span>
            <span class="chip">Quiz Ready</span>
            <span class="chip">Hackathon Demo</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 📝 What topic should we break down?")
    user_input = st.text_area(
        "Topic / concept",
        placeholder="e.g., PCA, Binary Search, Data Drift, Photosynthesis...",
        height=110,
        help="Enter one topic or concept. Keep it short for the best response.",
    )

with col2:
    st.write("")
    st.write("")
    st.write("")
    st.caption("Tap once to generate")
    generate = st.button(
        "🚀 Generate Study Pack",
        use_container_width=True,
        disabled=not user_input.strip(),
    )

if generate:
    if user_input.strip() == "":
        st.error("⚠️ Please enter a topic to learn about!")
    elif len(user_input) > 1000:
        st.warning("⚠️ Please keep the topic under 1000 characters for a better response.")
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
                    data = normalize_study_data(extract_json_payload(output))

                    st.success("✅ Study material generated successfully!")
                    st.markdown("---")

                    # Tabs for better organization
                    tab1, tab2, tab3 = st.tabs(["📘 Explanation", "📝 Notes", "❓ Quiz"])

                    with tab1:
                        with st.container(border=True):
                            st.markdown(f"### 📖 {user_input.title()}")
                            st.markdown(data["explanation"])

                    with tab2:
                        with st.container(border=True):
                            st.markdown("### 📌 Key Points")
                            for idx, note in enumerate(data["notes"], 1):
                                st.markdown(f"**{idx}.** ✨ {note}")

                    with tab3:
                        with st.container(border=True):
                            st.markdown("### 🧠 Test Your Knowledge")
                            for idx, q in enumerate(data["quiz"], 1):
                                with st.container(border=True):
                                    st.markdown(f"**Question {idx}:** {q['question']}")
                                    st.markdown("**Options:**")
                                    for opt in q["options"]:
                                        st.markdown(f"  • {opt}")
                                    st.markdown(f"**✅ Correct Answer:** {q['answer']}")

                except json.JSONDecodeError:
                    st.error("❌ The model returned an unreadable format. Showing raw output:")
                    st.code(output, language="text")

            except AuthenticationError:
                st.error("❌ Invalid Groq API key. Please check your key and try again.")
            except RateLimitError:
                st.error("❌ Rate limit reached. Please wait a moment and try again.")
            except (APITimeoutError, BadRequestError, APIError):
                st.error("❌ Groq API request failed. Please try again in a few seconds.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                st.info("💡 Try checking your API key or try again in a few seconds.")
