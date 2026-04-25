# AI Study Assistant

AI Study Assistant is a modern Streamlit web app that turns any topic into a simple explanation, short study notes, and a quiz with answers. It is designed for quick revision, self-study, and hackathon demos, with a clean dark UI and a responsive layout that works well on desktop and mobile.

## Features
- AI-generated explanation for any topic
- Short bullet-point notes for revision
- Quiz questions with correct answers
- Dark, responsive, hackathon-friendly UI
- Groq-powered model integration

## Tech Stack
- Python 3.8+
- Streamlit
- Groq API
- OpenAI Python SDK
- HTML/CSS for custom styling

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Manasa-L-Hegde/AI-Study-Assistant.git
cd AI-Study-Assistant
```

### 2. Create and activate a virtual environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your Groq API key
**Windows (PowerShell):**
```powershell
setx GROQ_API_KEY "gsk_YOUR_KEY"
$env:GROQ_API_KEY = "gsk_YOUR_KEY"
```

**Windows (CMD):**
```cmd
setx GROQ_API_KEY gsk_YOUR_KEY
```

**macOS/Linux:**
```bash
export GROQ_API_KEY="gsk_YOUR_KEY"
```

Optional model override:
```powershell
setx GROQ_MODEL "llama-3.1-8b-instant"
```

### 5. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Usage
1. Enter a topic such as `PCA` or `Binary Search`.
2. Click **Generate Study Pack**.
3. Read the explanation, notes, and quiz in separate tabs.

## Deployment
This project is ready to deploy with **Streamlit Community Cloud**.

Recommended flow:
1. Push the repo to GitHub.
2. Connect the repo to Streamlit Cloud.
3. Add `GROQ_API_KEY` in the app secrets/settings.
4. Share the live demo link with judges or users.

## Security Notes
- API keys should stay in environment variables or deployment secrets.
- Do not commit keys into `app.py`, README, screenshots, or git history.
- `.gitignore` already excludes `.venv/`, `.env`, and cache folders.

## Project Structure
```
.
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Troubleshooting
- **Invalid key format**: Ensure the key starts with `gsk_` or `gsk-`.
- **API key not found**: Set `GROQ_API_KEY` and restart the terminal.
- **Model error**: Update `GROQ_MODEL` if Groq changes the default.
- **No JSON output**: Retry or adjust the prompt/model settings.

## Why this project
Helps students learn faster by turning complex topics into clear explanations, concise notes, and quiz practice in a single app.

## License
MIT

---
Built for Hackathon | April 2026
