# 🎓 AI Study Assistant v2.0 - Professional Learning Platform

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq-purple)](https://groq.com/)

A comprehensive, professional AI-powered study assistant that transforms any topic into structured, detailed learning material with visual diagrams, real-world examples, and interactive quizzes.

## ✨ What's New in v2.0

### 🎨 Modern Professional UI
- **Clean Academic Design**: Elegant deep blue & indigo color scheme
- **Glassmorphism Effects**: Modern, premium aesthetic
- **Smooth Animations**: Professional transitions and hover effects
- **Responsive Layout**: Perfect on all devices
- **Dark/Light Themes**: Toggle between professional themes

### 🧠 Enhanced AI Responses
- **Comprehensive Explanations**: 4-6 detailed paragraphs (800+ words)
- **Structured Breakdown**: What, Why, How, and Key Principles
- **Real-World Examples**: Concrete applications with explanations
- **Visual Diagrams**: Mermaid flowcharts, mindmaps, and more
- **Code & Formulas**: Syntax-highlighted examples
- **Quick Revision**: Bullet-point summaries
- **Interview Points**: Important exam/interview topics
- **Common Mistakes**: What to avoid and why

### 📊 Visual Learning
- **Mermaid Diagrams**: Automatic diagram generation
- **Flowcharts**: Process visualization
- **Mindmaps**: Concept relationships
- **Sequence Diagrams**: Step-by-step flows
- **Code Blocks**: Syntax-highlighted examples

### 🚀 Advanced Features
- **Study Modes**: Comprehensive or Quick
- **Smart Bookmarks**: Save favorite topics
- **Study History**: Track learning progress
- **Analytics Dashboard**: Detailed statistics
- **Export Options**: PDF, Markdown, JSON
- **Quiz with Explanations**: Learn from mistakes
- **Session Management**: Persistent state
- **Error Handling**: Robust fallbacks

## 📸 Screenshots

### Home Page
![Home Page](docs/screenshots/home.png)

### Comprehensive Study Material
![Study Material](docs/screenshots/study.png)

### Visual Diagrams
![Diagrams](docs/screenshots/diagrams.png)

### Analytics Dashboard
![Analytics](docs/screenshots/analytics.png)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one free](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AI-Study-Assistant.git
cd AI-Study-Assistant
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your Groq API key
GROQ_API_KEY=gsk_your_api_key_here
```

5. **Run the application**
```bash
# Use the upgraded version
streamlit run main_upgraded_v2.py

# Or the original version
streamlit run main.py
```

6. **Open in browser**
```
http://localhost:8501
```

## 📚 Usage Guide

### Basic Usage

1. **Enter a Topic**: Type any subject you want to learn about
2. **Select Mode**: Choose Comprehensive or Quick study mode
3. **Generate**: Click the generate button
4. **Explore**: Navigate through tabs to see different aspects

### Study Modes

#### Comprehensive Mode
- Detailed 800+ word explanations
- Visual diagrams
- Multiple examples
- Interview points
- Common mistakes
- Related topics
- 5 quiz questions with explanations

#### Quick Mode
- Concise 2-3 paragraph explanations
- Key concepts
- Quick revision points
- 3 quiz questions

### Features

#### 📖 Explanation Tab
- Comprehensive overview
- Detailed breakdown
- Reading statistics

#### 🔑 Key Concepts Tab
- Important points
- Core principles
- Essential knowledge

#### 📊 Visual Diagram Tab
- Mermaid diagrams
- Flowcharts
- Mindmaps
- Process flows

#### 💡 Examples Tab
- Real-world applications
- Code examples
- Formulas
- Practical use cases

#### ⚡ Quick Revision Tab
- Bullet-point summary
- Common mistakes
- Related topics

#### 🎯 Interview Points Tab
- Exam-focused content
- Important questions
- Key talking points

#### ❓ Quiz Tab
- Interactive questions
- Instant feedback
- Detailed explanations
- Progress tracking

## 🎨 Customization

### Themes

Toggle between light and dark themes using the sidebar button.

### Study Mode

Select your preferred study mode:
- **Comprehensive**: For deep learning
- **Quick**: For quick reviews

### API Configuration

Configure in `.env` or Streamlit secrets:
```toml
[api]
groq_api_key = "your_key"
groq_model = "llama-3.1-8b-instant"

[features]
enable_dark_mode = true
enable_export = true
enable_bookmarks = true
enable_analytics = true
```

## 🌐 Deployment

### Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Create new app
4. Select `main_upgraded_v2.py` as main file
5. Add secrets in app settings
6. Deploy!

See [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md) for detailed instructions.

### Docker

```bash
docker build -t ai-study-assistant .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key ai-study-assistant
```

### Heroku

```bash
heroku create your-app-name
git push heroku main
heroku config:set GROQ_API_KEY=your_key
```

## 📁 Project Structure

```
AI-Study-Assistant/
├── main.py                          # Original application
├── main_upgraded_v2.py              # Upgraded v2.0 application
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .streamlit/
│   ├── config.toml                  # Streamlit configuration
│   └── secrets.toml.example         # Secrets template
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Application settings
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── api_client.py            # Groq API client
│   │   ├── validators.py            # Input validation
│   │   ├── data_processor.py        # Data processing
│   │   ├── session_manager.py       # Session management
│   │   ├── enhanced_prompts.py      # AI prompt templates
│   │   └── safe_config.py           # Safe configuration access
│   └── components/
│       ├── __init__.py
│       ├── ui_styles.py             # Original UI styles
│       ├── modern_ui_styles.py      # Modern professional UI
│       └── diagram_renderer.py      # Diagram rendering
├── tests/
│   ├── __init__.py
│   └── test_validators.py
├── docs/
│   ├── CONTRIBUTING.md
│   ├── DEPLOYMENT.md
│   └── screenshots/
├── README.md                        # This file
├── CHANGELOG.md
├── LICENSE
└── setup.py
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
GROQ_API_KEY=gsk_your_api_key_here

# Optional
GROQ_MODEL=llama-3.1-8b-instant
APP_ENV=production
DEBUG=false
MAX_TOPIC_LENGTH=1000
CACHE_TTL=3600
```

### Streamlit Secrets

For Streamlit Cloud deployment:

```toml
[api]
groq_api_key = "gsk_your_key"
groq_model = "llama-3.1-8b-instant"

[app]
environment = "production"

[features]
enable_dark_mode = true
enable_export = true
enable_bookmarks = true
enable_analytics = true
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_validators.py
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 🐛 Known Issues

- Mermaid diagrams require internet connection for rendering
- PDF export requires additional dependencies
- Some complex diagrams may not render on mobile

## 🗺️ Roadmap

### v2.1 (Planned)
- [ ] Voice input support
- [ ] File upload (PDF, DOCX)
- [ ] Flashcard generation
- [ ] Study planner
- [ ] Spaced repetition
- [ ] Multi-language support

### v2.2 (Planned)
- [ ] Collaborative study rooms
- [ ] AI tutor chat
- [ ] Progress tracking
- [ ] Achievement system
- [ ] Mobile app

## 💡 Tips & Best Practices

### For Best Results

1. **Be Specific**: "Neural Networks in Deep Learning" vs "AI"
2. **Use Comprehensive Mode**: For new topics
3. **Use Quick Mode**: For revision
4. **Save Bookmarks**: For important topics
5. **Review Analytics**: Track your progress
6. **Take Quizzes**: Test your understanding

### Study Workflow

1. Generate comprehensive material
2. Read explanation thoroughly
3. Study visual diagrams
4. Review examples
5. Take the quiz
6. Save as bookmark
7. Use quick mode for revision

## 🔒 Privacy & Security

- API keys are never logged or stored
- All data stays in your session
- No personal information collected
- Open source and transparent

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: For providing fast AI inference
- **Streamlit**: For the amazing framework
- **OpenAI**: For the API client library
- **Mermaid**: For diagram rendering
- **Community**: For feedback and contributions

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/yourusername/AI-Study-Assistant/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/AI-Study-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AI-Study-Assistant/discussions)
- **Email**: support@example.com

## ⭐ Star History

If you find this project helpful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/AI-Study-Assistant&type=Date)](https://star-history.com/#yourusername/AI-Study-Assistant&Date)

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/AI-Study-Assistant)
![GitHub forks](https://img.shields.io/github/forks/yourusername/AI-Study-Assistant)
![GitHub issues](https://img.shields.io/github/issues/yourusername/AI-Study-Assistant)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/AI-Study-Assistant)

---

**Made with ❤️ by Bob** | **Powered by Groq** | **Built with Streamlit**

*Transform your learning experience with AI* 🚀