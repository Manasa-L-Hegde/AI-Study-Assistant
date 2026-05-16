# 📚 AI Study Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.35+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

**Transform any topic into clear explanations, detailed notes, and interactive quizzes in seconds.**

[Live Demo](https://your-app-url.streamlit.app) • [Documentation](./docs) • [Report Bug](https://github.com/yourusername/AI-Study-Assistant/issues) • [Request Feature](https://github.com/yourusername/AI-Study-Assistant/issues)

</div>

---

## ✨ Features

### 🎯 Core Functionality
- **AI-Powered Explanations**: Get clear, concise explanations for any topic
- **Smart Note Generation**: Automatically extract key points and important concepts
- **Interactive Quizzes**: Test your knowledge with AI-generated questions
- **Real-time Generation**: Fast response times powered by Groq's LLM API

### 🎨 User Experience
- **Modern UI/UX**: Beautiful, intuitive interface with smooth animations
- **Dark/Light Mode**: Toggle between themes for comfortable studying
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Accessibility**: ARIA labels, keyboard navigation, and screen reader support

### 📊 Study Management
- **Progress Tracking**: Monitor your learning journey with detailed analytics
- **Bookmarks**: Save your favorite study materials for quick access
- **Study History**: Review previously generated content
- **Export Options**: Download study materials in Markdown, Text, or JSON format

### 🔒 Security & Performance
- **Secure API Key Management**: Environment-based configuration
- **Input Validation**: Comprehensive validation and sanitization
- **Error Handling**: Robust error handling with user-friendly messages
- **Caching**: Optimized performance with intelligent caching

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-Study-Assistant.git
   cd AI-Study-Assistant
   ```

2. **Create a virtual environment**
   
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

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   GROQ_MODEL=llama-3.1-8b-instant
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

The app will open at `http://localhost:8501`

---

## 📖 Usage Guide

### Generating Study Material

1. **Enter a Topic**: Type any subject or concept you want to learn about
2. **Click Generate**: The AI will create comprehensive study material
3. **Explore Content**: Navigate through Explanation, Notes, and Quiz tabs
4. **Test Knowledge**: Answer quiz questions to reinforce learning

### Managing Your Studies

#### Bookmarks
- Click the 🔖 button to save study materials
- Access saved content from the Bookmarks page
- Remove bookmarks you no longer need

#### Analytics
- View your study statistics on the Analytics page
- Track topics studied, questions answered, and accuracy
- Monitor your learning progress over time

#### Export
- Select export format (Markdown, Text, or JSON)
- Click the Export button to download
- Use exported files for offline study or sharing

### Keyboard Shortcuts

- `Tab`: Navigate between elements
- `Enter`: Activate buttons and links
- `Esc`: Close modals and dialogs
- `Ctrl/Cmd + K`: Focus search (when available)

---

## 🏗️ Project Structure

```
AI-Study-Assistant/
├── main.py                      # Main application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
│
├── .streamlit/
│   ├── config.toml             # Streamlit configuration
│   └── secrets.toml.example    # Secrets template for deployment
│
├── src/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration management
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── api_client.py       # API client for Groq
│   │   ├── validators.py       # Input validation
│   │   ├── data_processor.py   # Data processing utilities
│   │   └── session_manager.py  # Session state management
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   └── ui_styles.py        # UI styling and themes
│   │
│   └── assets/                 # Static assets (images, icons)
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_validators.py
│   ├── test_data_processor.py
│   └── test_api_client.py
│
└── docs/                       # Documentation
    ├── API.md
    ├── CONTRIBUTING.md
    └── DEPLOYMENT.md
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROQ_API_KEY` | Your Groq API key | - | Yes |
| `GROQ_MODEL` | Model to use | `llama-3.1-8b-instant` | No |
| `APP_ENV` | Environment (development/production) | `development` | No |
| `DEBUG` | Enable debug mode | `false` | No |
| `ENABLE_DARK_MODE` | Enable theme toggle | `true` | No |
| `ENABLE_EXPORT` | Enable export functionality | `true` | No |
| `ENABLE_BOOKMARKS` | Enable bookmarks | `true` | No |
| `ENABLE_ANALYTICS` | Enable analytics | `true` | No |

### Available Models

- `llama-3.1-8b-instant` (Default - Fast, efficient)
- `llama-3.1-70b-versatile` (More capable, slower)
- `mixtral-8x7b-32768` (Large context window)
- `gemma2-9b-it` (Google's Gemma model)

---

## 🚢 Deployment

### Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `main.py` as the main file
   - Add secrets in the app settings:
     ```toml
     [api]
     groq_api_key = "gsk_your_api_key_here"
     ```

3. **Deploy!**
   - Click Deploy
   - Your app will be live in minutes

### Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
```

Build and run:
```bash
docker build -t ai-study-assistant .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key ai-study-assistant
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_validators.py
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for details on our code of conduct and development process.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Groq** for providing fast LLM inference
- **Streamlit** for the amazing web framework
- **OpenAI** for the Python SDK
- All contributors and users of this project

---

## 📧 Contact

- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Email**: your.email@example.com
- **Twitter**: [@yourhandle](https://twitter.com/yourhandle)

---

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Voice input for topics
- [ ] Collaborative study sessions
- [ ] Spaced repetition system
- [ ] Mobile app (React Native)
- [ ] Integration with note-taking apps
- [ ] Advanced analytics and insights
- [ ] Custom quiz difficulty levels
- [ ] Study group features
- [ ] Gamification elements

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/AI-Study-Assistant?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/AI-Study-Assistant?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/AI-Study-Assistant)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/AI-Study-Assistant)

---

<div align="center">

**Made with ❤️ by [Your Name](https://github.com/yourusername)**

⭐ Star this repo if you find it helpful!

</div>
