import os 
import json
import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(page_title="AI Study Assistant", layout="centered")

# Read API key from environment first, then allow manual input as fallback.
api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
if not api_key:
    st.warning("OPENAI_API_KEY is not set. Enter your key below to continue.")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...").strip()

client = None
if api_key:
    if api_key.startswith("sk-"):
        client = OpenAI(api_key=api_key)
    else:
        st.error("Invalid key format. Your OpenAI key should start with 'sk-'.")

# Title
st.title("📚 AI Study Assistant")
st.markdown("""
### 🎯 Your Personal AI Learning Assistant
Get instant explanations, notes, and quizzes for any topic.
""")
st.markdown("Learn faster with AI-powered explanations, notes, and quizzes.")

# Input
st.subheader("📥 Enter Topic")
user_input = st.text_area(
    "📥 Enter topic or notes:",
    placeholder="e.g., PCA, Binary Search, Data Drift..."
)

# Button
generate = st.button("🚀 Generate Study Material")

if generate:
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a topic.")
    elif client is None:
        st.error("API key not configured. Set OPENAI_API_KEY or paste a valid key above.")
    else:
        with st.spinner("Generating study material..."):
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
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                output = response.choices[0].message.content

                try:
                    data = json.loads(output)

                    st.success("✅ Study material generated successfully!")

                    st.markdown("---")
                    st.subheader("📘 Explanation")
                    st.write(data["explanation"])

                    st.markdown("---")
                    st.subheader("📝 Short Notes")
                    for note in data["notes"]:
                        st.write(f"- {note}")

                    st.markdown("---")
                    st.subheader("❓ Quiz")
                    for q in data["quiz"]:
                        st.write(q["question"])
                        for opt in q["options"]:
                            st.write(f"- {opt}")
                        st.write(f"**✅ Answer:** {q['answer']}")
                        st.write("---")

                except Exception:
                    st.error("Formatting issue. Showing raw output:")
                    st.write(output)

            except Exception as e:
                st.error(f"Error: {e}")
