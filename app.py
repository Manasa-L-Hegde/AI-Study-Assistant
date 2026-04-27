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

# Custom CSS for a dark, cute floral design
st.markdown("""
<style>
    :root {
        --bg-0: #020305;
        --bg-1: #05070d;
        --bg-2: #0b1020;
        --card: rgba(10, 14, 24, 0.88);
        --text: #e7edf8;
        --muted: #aab4c8;
        --line: rgba(180, 190, 210, 0.22);
        --shadow: 0 18px 44px rgba(0, 0, 0, 0.58);
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 12%, rgba(255,255,255,0.08) 0 1.6px, transparent 1.7px),
            radial-gradient(circle at 22% 28%, rgba(255,255,255,0.06) 0 1.2px, transparent 1.3px),
            radial-gradient(circle at 78% 18%, rgba(255,255,255,0.08) 0 1.5px, transparent 1.6px),
            radial-gradient(circle at 86% 35%, rgba(255,255,255,0.06) 0 1.1px, transparent 1.2px),
            radial-gradient(circle at 15% 78%, rgba(255,255,255,0.07) 0 1.4px, transparent 1.5px),
            radial-gradient(circle at 68% 82%, rgba(255,255,255,0.06) 0 1.2px, transparent 1.3px),
            radial-gradient(circle at 40% 55%, rgba(255,255,255,0.05) 0 1.2px, transparent 1.3px),
            linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 45%, var(--bg-2) 100%);
        color: var(--text);
    }

    h1, h2, h3 {
        color: var(--text);
        letter-spacing: 0.2px;
    }

    .hero-box {
        backdrop-filter: blur(10px);
        background: linear-gradient(120deg, rgba(18, 23, 36, 0.92), rgba(8, 11, 18, 0.92));
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 1.1rem 1.2rem;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
        justify-content: center;
    }

    .chip {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid var(--line);
        color: var(--text);
        border-radius: 999px;
        font-size: 0.82rem;
        padding: 5px 10px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070b12 0%, #0c1322 100%);
        border-right: 1px solid var(--line);
    }

    .stButton > button {
        background: linear-gradient(110deg, #f8fafc, #dbeafe);
        color: #050816 !important;
        border: 0;
        border-radius: 16px;
        padding: 0.62rem 0.95rem;
        font-weight: 800;
        box-shadow: 0 10px 22px rgba(255, 255, 255, 0.10);
        transition: transform .15s ease, box-shadow .15s ease;
        width: 100%;
    }

    .stButton > button * {
        color: #050816 !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 24px rgba(255, 255, 255, 0.15);
        color: #020305 !important;
    }

    .stButton > button:hover * {
        color: #020305 !important;
    }

    .stButton > button:focus,
    .stButton > button:active {
        color: #020305 !important;
        outline: 2px solid rgba(103, 232, 249, 0.45);
        outline-offset: 1px;
    }

    .stButton > button:focus *,
    .stButton > button:active * {
        color: #020305 !important;
    }

    .stTextArea textarea {
        border-radius: 14px;
        border: 2px solid rgba(255, 255, 255, 0.18);
        background: rgba(3, 6, 15, 0.92);
        color: var(--text);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-weight: 600;
        color: var(--text);
    }

    .stContainer {
        border-radius: 14px;
    }

    .stAlert {
        border-radius: 12px;
        border: 1px solid var(--line);
    }

    .result-card {
        background: rgba(9, 14, 24, 0.92);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 14px;
        margin-top: 6px;
    }

    .result-card p,
    .result-card li,
    .result-card strong,
    .result-card div {
        color: #e7edf8 !important;
    }

    .quiz-option-hint {
        color: #b7c4dd;
        font-size: 0.9rem;
        margin-bottom: 6px;
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

manual_api_key = ""
with st.sidebar:
    st.markdown("### 🎛️ Settings")
    if not env_api_key:
        st.warning("🔑 API Key not found in environment")
        manual_api_key = st.text_input("Enter Groq API Key", type="password", placeholder="gsk-...").strip()
    else:
        st.success("✅ API Key loaded from environment")
        if st.checkbox("Use different key?"):
            manual_api_key = st.text_input("Enter Groq API Key", type="password", placeholder="gsk-...").strip()

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


def normalize_option_text(value: str) -> str:
    """Normalize option/answer text for robust comparison."""
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def resolve_correct_option(answer: str, options: list) -> str:
    """Resolve model answer to the exact option text when possible."""
    if not options:
        return ""

    answer_raw = str(answer or "").strip()
    answer_norm = normalize_option_text(answer_raw)

    # 1) Exact text match (case-insensitive)
    for opt in options:
        if normalize_option_text(opt) == answer_norm:
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
        opt_norm = normalize_option_text(opt)
        if answer_norm and (answer_norm in opt_norm or opt_norm in answer_norm):
            return opt

    # If unresolved, keep original answer so UI can still display something meaningful.
    return answer_raw


def render_study_pack(topic: str, data: dict) -> None:
    """Render persisted results so Streamlit reruns do not hide quiz state."""
    st.success("✅ Study material generated successfully!")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📘 Explanation", "📝 Notes", "❓ Quiz"])

    with tab1:
        with st.container(border=True):
            st.markdown(f"### 📖 {topic.title()}")
            st.markdown(f"<div class='result-card'>{data['explanation']}</div>", unsafe_allow_html=True)

    with tab2:
        with st.container(border=True):
            st.markdown("### 📌 Important Notes")
            notes_md = "".join(
                [f"<p><strong>Important {idx}:</strong> {note}</p>" for idx, note in enumerate(data["notes"], 1)]
            )
            st.markdown(f"<div class='result-card'>{notes_md}</div>", unsafe_allow_html=True)

    with tab3:
        with st.container(border=True):
            st.markdown("### 🧠 Test Your Knowledge")
            if "quiz_selected" not in st.session_state:
                st.session_state["quiz_selected"] = {}

            for idx, q in enumerate(data["quiz"], 1):
                st.markdown(f"**Question {idx}:** {q['question']}")
                st.markdown("<div class='quiz-option-hint'>Click one option to check your answer.</div>", unsafe_allow_html=True)

                options = [str(opt) for opt in q.get("options", [])]
                correct_answer = resolve_correct_option(q.get("answer", ""), options)
                state_key = f"selected_{idx}"

                for i, opt in enumerate(options):
                    if st.button(f"Option {i + 1}: {opt}", key=f"q{idx}_{i}", use_container_width=True):
                        st.session_state["quiz_selected"][state_key] = opt

                selected = st.session_state["quiz_selected"].get(state_key)
                if selected:
                    if normalize_option_text(selected) == normalize_option_text(correct_answer):
                        st.success(f"Correct! You clicked: {selected}")
                    else:
                        st.error(f"Wrong. You clicked: {selected}")
                        st.info("Try again.")

                st.divider()


if "study_data" not in st.session_state:
    st.session_state["study_data"] = None

if "study_topic" not in st.session_state:
    st.session_state["study_topic"] = ""
# Main title
st.markdown(
    """
    <div class="hero-box">
        <h1 style="margin:0; text-align:center;">📚 AI Study Assistant</h1>
        <p style="text-align:center; margin:10px 0 0 0; font-size:1.05rem; color:#cbd5e1;">
            Turn any topic into simple explanations, important notes, and quiz practice in seconds.
        </p>
        <div class="chip-row">
            <span class="chip">Beginner Friendly</span>
            <span class="chip">Fast Summaries</span>
            <span class="chip">Quiz Practice</span>
            <span class="chip">Hackathon Ready</span>
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
    "explanation": "A clear, detailed but simple explanation in 2 to 4 short paragraphs.",
    "notes": [
        "Detailed important point 1 with a small explanation",
        "Detailed important point 2 with a small explanation",
        "Detailed important point 3 with a small explanation",
        "Detailed important point 4 with a small explanation",
        "Detailed important point 5 with a small explanation"
    ],
    "quiz": [
        {{
            "question": "A good concept-check question",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct option text"
        }},
        {{
            "question": "Another concept-check question",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct option text"
        }},
        {{
            "question": "Another concept-check question",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct option text"
        }}
    ]
}}

Topic: {user_input}
Explain in simple terms, but make the notes detailed and useful for revision.
Do not keep it too short.
"""

            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                output = response.choices[0].message.content

                try:
                    data = normalize_study_data(extract_json_payload(output))
                    st.session_state["study_data"] = data
                    st.session_state["study_topic"] = user_input
                    st.session_state["quiz_selected"] = {}

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

if st.session_state["study_data"] is not None:
    render_study_pack(st.session_state["study_topic"], st.session_state["study_data"])
