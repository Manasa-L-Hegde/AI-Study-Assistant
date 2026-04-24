# AI Study Assistant

An AI-powered web app that helps students learn faster by generating explanations, notes, and quiz questions for any topic.

## Features
- Simple explanation of any topic
- Bullet-point notes
- Auto-generated MCQs with answers
- Fast and interactive UI using Streamlit

## Tech Stack
- Python 3.8+
- Streamlit
- Groq API (free LLM provider)

## Prerequisites
- Python 3.8 or higher
- Groq API key (free from https://console.groq.com)

## Installation

### 1. Clone this repository
```bash
git clone <your-repo-url>
cd AI-Study-Assistant
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate virtual environment
**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up Groq API key
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

### 6. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage Example
1. Enter a topic: "PCA"
2. Click "Generate Study Material"
3. Get:
   - Simple explanation
   - Bullet-point notes
   - Multiple-choice quiz with answers

## API Key Management
- Get free API key: https://console.groq.com
- Free tier: Valid for 7 days, then generate a new key
- **IMPORTANT:** Never commit API keys to GitHub
- Keep `.env` and environment variables local only
- Rotate keys regularly (set reminder for May 22, 2026)

## Project Structure
```
.
├── app.py              # Main Streamlit application
├── README.md           # This file
├── requirements.txt    # Python dependencies
└── .gitignore          # Git ignore file
```

## Security Notes
- API keys are loaded from environment variables only
- No secrets are stored in code or configuration files
- Fallback: If env var not set, app shows input box for manual key entry
- All keys in code/chat were rotated and should be ignored

## Troubleshooting
- **Invalid key format error:** Ensure key starts with `gsk_`
- **GROQ_API_KEY not set:** Set environment variable and restart terminal
- **Model decommissioned:** Default model `llama-3.1-8b-instant` is current; update `GROQ_MODEL` env var if needed
- **Quiz not rendering:** Check JSON format of LLM response

## Use Case
Helps students quickly understand any concept and self-test knowledge through AI-generated quizzes.

## License
MIT

---
Built for Hackathon | April 2026
