# Deployment Guide

This guide covers deploying the AI Study Assistant to various platforms.

## 📋 Table of Contents

- [Streamlit Cloud](#streamlit-cloud)
- [Docker](#docker)
- [Heroku](#heroku)
- [AWS](#aws)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Streamlit Cloud

Streamlit Cloud is the easiest way to deploy your app.

### Prerequisites

- GitHub account
- Groq API key
- Repository pushed to GitHub

### Deployment Steps

1. **Prepare Your Repository**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

3. **Create New App**
   - Click "New app"
   - Select your repository
   - Choose branch: `main`
   - Main file path: `main.py`

4. **Configure Secrets**
   
   Click "Advanced settings" and add secrets:
   
   ```toml
   [api]
   groq_api_key = "gsk_your_actual_api_key_here"
   groq_model = "llama-3.1-8b-instant"
   
   [app]
   secret_key = "your_random_secret_key_here"
   environment = "production"
   
   [features]
   enable_dark_mode = true
   enable_export = true
   enable_bookmarks = true
   enable_analytics = true
   ```

5. **Deploy**
   - Click "Deploy!"
   - Wait for deployment to complete
   - Your app will be live at `https://your-app-name.streamlit.app`

### Custom Domain (Optional)

1. Go to app settings
2. Click "Custom domain"
3. Follow instructions to configure DNS

---

## 🐳 Docker

Deploy using Docker for more control.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GROQ_MODEL=${GROQ_MODEL:-llama-3.1-8b-instant}
      - APP_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t ai-study-assistant .

# Run container
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  ai-study-assistant

# Or use docker-compose
docker-compose up -d
```

### Docker Hub

```bash
# Tag image
docker tag ai-study-assistant yourusername/ai-study-assistant:latest

# Push to Docker Hub
docker push yourusername/ai-study-assistant:latest
```

---

## 🔴 Heroku

Deploy to Heroku for a managed platform.

### Prerequisites

- Heroku account
- Heroku CLI installed

### Deployment Steps

1. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

2. **Create Procfile**
   ```
   web: sh setup.sh && streamlit run main.py
   ```

3. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GROQ_API_KEY=your_key
   heroku config:set GROQ_MODEL=llama-3.1-8b-instant
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

---

## ☁️ AWS

Deploy to AWS for enterprise-grade hosting.

### AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   eb init -p python-3.11 ai-study-assistant
   ```

3. **Create Environment**
   ```bash
   eb create production
   ```

4. **Set Environment Variables**
   ```bash
   eb setenv GROQ_API_KEY=your_key
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

### AWS ECS (Docker)

1. **Push to ECR**
   ```bash
   aws ecr create-repository --repository-name ai-study-assistant
   docker tag ai-study-assistant:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ai-study-assistant:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-study-assistant:latest
   ```

2. **Create ECS Task Definition**
   - Use AWS Console or CLI
   - Configure container with environment variables
   - Set port mappings (8501)

3. **Create ECS Service**
   - Choose Fargate or EC2 launch type
   - Configure load balancer
   - Set desired task count

---

## 🔐 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | `gsk_...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_MODEL` | Model to use | `llama-3.1-8b-instant` |
| `APP_ENV` | Environment | `production` |
| `DEBUG` | Debug mode | `false` |
| `SECRET_KEY` | Session secret | Random string |

### Setting Variables

**Streamlit Cloud:**
```toml
# In app secrets
[api]
groq_api_key = "your_key"
```

**Docker:**
```bash
docker run -e GROQ_API_KEY=your_key ...
```

**Heroku:**
```bash
heroku config:set GROQ_API_KEY=your_key
```

**AWS:**
```bash
eb setenv GROQ_API_KEY=your_key
```

---

## 🔧 Configuration

### Production Settings

Update `.streamlit/config.toml` for production:

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#e2e8f0"
```

### Performance Optimization

1. **Enable Caching**
   ```python
   # Already implemented in code
   @st.cache_data(ttl=3600)
   def expensive_function():
       pass
   ```

2. **Optimize Images**
   - Use WebP format
   - Compress images
   - Lazy load when possible

3. **Minimize Dependencies**
   - Only include necessary packages
   - Use lightweight alternatives

---

## 🐛 Troubleshooting

### Common Issues

#### App Won't Start

**Problem:** App fails to start
**Solution:**
- Check logs: `streamlit run main.py --logger.level=debug`
- Verify all dependencies installed
- Check Python version (3.8+)

#### API Key Not Working

**Problem:** API authentication fails
**Solution:**
- Verify key format (starts with `gsk_`)
- Check environment variable is set
- Ensure no extra spaces in key

#### Memory Issues

**Problem:** App crashes due to memory
**Solution:**
- Increase container memory
- Implement pagination for large datasets
- Clear cache periodically

#### Slow Performance

**Problem:** App is slow to respond
**Solution:**
- Enable caching
- Optimize database queries
- Use CDN for static assets
- Consider upgrading instance size

### Logs

**Streamlit Cloud:**
- View logs in app dashboard
- Click "Manage app" → "Logs"

**Docker:**
```bash
docker logs container_name
```

**Heroku:**
```bash
heroku logs --tail
```

**AWS:**
```bash
eb logs
```

---

## 📊 Monitoring

### Health Checks

Add health check endpoint:

```python
# In main.py
if st.query_params.get("health") == "check":
    st.write("OK")
    st.stop()
```

### Metrics

Monitor these metrics:
- Response time
- Error rate
- API usage
- User sessions
- Memory usage

### Tools

- **Streamlit Cloud**: Built-in analytics
- **Docker**: Prometheus + Grafana
- **AWS**: CloudWatch
- **Heroku**: Heroku Metrics

---

## 🔄 CI/CD

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest
      
      - name: Deploy
        run: |
          # Deployment happens automatically via Streamlit Cloud
          echo "Deployment triggered"
```

---

## 📝 Checklist

Before deploying:

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Secrets not in code
- [ ] Dependencies updated
- [ ] Documentation updated
- [ ] Error handling tested
- [ ] Performance optimized
- [ ] Security reviewed
- [ ] Backup plan ready

---

## 🆘 Support

Need help? Check:

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Project Issues](https://github.com/yourusername/AI-Study-Assistant/issues)

---

**Happy Deploying! 🚀**