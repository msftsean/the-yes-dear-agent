# 🚀 Deployment Guide

Complete guide to deploying the Yes Dear Assistant from zero to production.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Detailed Setup](#detailed-setup)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Seeding Sample Data](#seeding-sample-data)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## Quick Start

### One-Command Setup

```bash
# Clone and setup in one go
git clone https://github.com/YOUR_USERNAME/lo-agent-bootcamp.git
cd lo-agent-bootcamp
python setup.py
```

The automated setup wizard handles everything:
- ✅ Python version check (3.12+ required)
- ✅ Virtual environment creation
- ✅ Dependency installation
- ✅ Configuration file setup
- ✅ Interactive API key configuration
- ✅ Installation verification

### Launch After Setup

**Mac/Linux:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

Your browser will automatically open to `http://localhost:8501`

---

## Detailed Setup

### Step 1: Prerequisites

**Required:**
- Python 3.12 or higher ([Download](https://www.python.org/downloads/))
- pip (comes with Python)
- Git ([Download](https://git-scm.com/downloads))

**Verify installations:**
```bash
python --version  # Should be 3.12+
pip --version
git --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/lo-agent-bootcamp.git
cd lo-agent-bootcamp
```

### Step 3: Run Setup Wizard

```bash
python setup.py
```

The wizard will:
1. Check Python version
2. Create virtual environment in `env/` directory
3. Upgrade pip
4. Install core dependencies (streamlit, openai, python-dotenv, etc.)
5. Install optional dependencies (google-api-python-client, pinecone, pytest)
6. Create `.env` configuration file
7. Prompt for API keys (interactive)
8. Verify installation

**Interactive Prompts:**
- OpenAI API key (required)
- Google Search API (optional - skip if you don't have one)
- Pinecone API key (optional - skip if you don't have one)

### Step 4: API Keys

See [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) for detailed instructions on obtaining API keys.

**Minimum Required:**
- OpenAI API key from https://platform.openai.com/api-keys

**Optional (for enhanced features):**
- Google Custom Search API + CSE ID
- Pinecone API key

---

## Configuration

### Environment Variables

Your `.env` file is created automatically by `setup.py`. Edit if needed:

```bash
# Required
OPENAI_API_KEY=sk-proj-your_key_here

# Optional - for real web search
GOOGLE_API_KEY=your_google_key_here
GOOGLE_CSE_ID=your_cse_id_here

# Optional - for document search
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENVIRONMENT=us-east-1

# Production settings (defaults)
ENVIRONMENT=development
DAILY_SPENDING_LIMIT=100.00
ALERT_THRESHOLD=70.0
MAX_REQUESTS_PER_MINUTE=10
CACHE_TTL_SECONDS=3600
```

### Production Settings Explained

| Setting | Description | Default | Notes |
|---------|-------------|---------|-------|
| `ENVIRONMENT` | Deployment environment | development | Options: development, staging, production |
| `DAILY_SPENDING_LIMIT` | Max daily OpenAI cost | 100.00 | In USD, blocks requests when exceeded |
| `ALERT_THRESHOLD` | Warning percentage | 70.0 | Alert at 70% of daily limit |
| `MAX_REQUESTS_PER_MINUTE` | Rate limit | 10 | Per user, prevents abuse |
| `CACHE_TTL_SECONDS` | Cache duration | 3600 | 1 hour, saves costs on repeated queries |

---

## Running the Application

### Option 1: Quick Launch Scripts

**Mac/Linux:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

These scripts automatically:
- Check for virtual environment
- Activate environment
- Verify dependencies
- Launch Streamlit server

### Option 2: Manual Launch

```bash
# Activate virtual environment
source env/bin/activate  # Mac/Linux
# or
env\Scripts\activate  # Windows

# Run the app
streamlit run app.py
```

### Option 3: Background Mode

```bash
# Run in background (Mac/Linux)
nohup streamlit run app.py &

# Run in background (Windows with PowerShell)
Start-Process -NoNewWindow streamlit run app.py
```

### Accessing the App

Once running, the app is available at:
- **Local:** http://localhost:8501
- **Network:** http://YOUR_IP:8501 (for access from other devices)

**Ports:**
- Default: 8501
- Change with: `streamlit run app.py --server.port 8080`

---

## Seeding Sample Data

### Pinecone Document Search

If you configured Pinecone API, seed it with sample company documents:

```bash
# Activate environment first
source env/bin/activate  # Mac/Linux
# env\Scripts\activate   # Windows

# Run seed script
python scripts/seed_data.py
```

**What it does:**
1. Connects to Pinecone
2. Creates `company-docs` index (if doesn't exist)
3. Generates embeddings for 8 sample documents
4. Uploads vectors to Pinecone

**Sample documents included:**
- Company Remote Work Policy
- Vacation and PTO Policy
- Information Security Guidelines
- Professional Development Program
- Q4 2024 Product Roadmap
- Customer Onboarding Best Practices
- Expense Reimbursement Policy
- Code Review Guidelines

**Cost:** ~$0.02-0.05 in OpenAI embedding costs

### Custom Data

To add your own documents:

1. Edit `scripts/seed_data.py`
2. Add to `SAMPLE_DOCUMENTS` array:
   ```python
   {
       "title": "Your Document Title",
       "content": "Your document content here...",
       "metadata": {
           "category": "Category",
           "department": "Dept",
           "date": "2024-01-01"
       }
   }
   ```
3. Run: `python scripts/seed_data.py`

---

## Verification

### Quick Health Check

After setup, verify everything works:

1. **Launch the app:**
   ```bash
   ./run.sh  # or run.bat on Windows
   ```

2. **In the browser:**
   - Chat tab should load
   - Ask a simple question: "What is AI?"
   - Should get a response from GPT-4o

3. **Check Production Dashboard:**
   - Click "Production Dashboard" tab
   - Should see 7 feature tabs
   - Cost Monitor shows $0.00 spent
   - System Health shows API status

4. **Test features:**
   - Enable "Real APIs" in sidebar (if configured)
   - Try web search: "Latest news on AI"
   - Try document search: "vacation policy" (if seeded)

### Run Tests

```bash
# Activate environment
source env/bin/activate

# Run test suite
pytest tests/ -v

# Run specific test
pytest tests/test_week4_features.py -v
```

**Expected results:**
- 80%+ pass rate
- No critical failures
- Some tests may fail if optional APIs not configured

---

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'streamlit'"**
```bash
# Ensure virtual environment is activated
source env/bin/activate  # Mac/Linux
env\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**"OPENAI_API_KEY not found"**
```bash
# Check .env file exists
ls -la .env

# Verify key is set
cat .env | grep OPENAI_API_KEY

# If missing, add to .env:
echo "OPENAI_API_KEY=sk-proj-your_key_here" >> .env
```

**"Port 8501 already in use"**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
lsof -ti:8501 | xargs kill  # Mac/Linux
# netstat -ano | findstr :8501  # Windows (find PID then taskkill)
```

**"Invalid API key" from OpenAI**
- Verify key starts with `sk-proj-` or `sk-`
- No extra spaces in .env file
- Check on OpenAI dashboard if key is active
- Regenerate key if needed

**Setup script fails on dependencies**
```bash
# Try manual installation
source env/bin/activate
pip install --upgrade pip
pip install streamlit openai python-dotenv requests

# Skip optional deps if they fail
pip install google-api-python-client  # optional
pip install pinecone-client  # optional
```

### Getting Help

1. Check [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) for API-specific issues
2. Review error logs in terminal
3. Check OpenAI dashboard for API errors
4. Search existing GitHub issues
5. Create new issue with:
   - Python version
   - Operating system
   - Error message
   - Steps to reproduce

---

## Production Deployment

### Cloud Platforms

#### Streamlit Community Cloud (Free)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin master
   ```

2. **Deploy:**
   - Go to https://share.streamlit.io/
   - Connect GitHub account
   - Select repository
   - Set main file: `app.py`
   - Add secrets (API keys) in dashboard

3. **Configure secrets:**
   - In Streamlit Cloud dashboard → Settings → Secrets
   - Add each API key:
     ```toml
     OPENAI_API_KEY = "sk-proj-your_key"
     GOOGLE_API_KEY = "your_key"
     GOOGLE_CSE_ID = "your_id"
     PINECONE_API_KEY = "your_key"
     ```

**Pros:** Free, easy, automatic updates from GitHub
**Cons:** Public URL, limited resources

#### Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run app.py --server.port $PORT" > Procfile

# Create Heroku app
heroku create your-app-name

# Set config vars
heroku config:set OPENAI_API_KEY=sk-proj-your_key

# Deploy
git push heroku master
```

#### AWS EC2

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Clone repo
git clone https://github.com/YOUR_USERNAME/lo-agent-bootcamp.git
cd lo-agent-bootcamp

# Run setup
python3 setup.py

# Run with systemd service
sudo nano /etc/systemd/system/yesdear.service
```

**Service file:**
```ini
[Unit]
Description=Yes Dear Assistant
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/lo-agent-bootcamp
ExecStart=/home/ubuntu/lo-agent-bootcamp/env/bin/streamlit run app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl enable yesdear
sudo systemctl start yesdear
```

### Production Checklist

Before deploying to production:

- [ ] Regenerate all API keys (don't use dev keys)
- [ ] Set production environment: `ENVIRONMENT=production`
- [ ] Configure appropriate spending limits
- [ ] Set up monitoring/alerts
- [ ] Configure custom domain (optional)
- [ ] Enable HTTPS
- [ ] Set up automated backups
- [ ] Review security settings
- [ ] Load test the application
- [ ] Document incident response procedures

### Security Best Practices

1. **API Keys:**
   - Never commit .env to git
   - Use secrets management (Streamlit Secrets, AWS Secrets Manager)
   - Rotate keys every 90 days
   - Use different keys per environment

2. **Access Control:**
   - Add authentication if needed (Streamlit supports auth)
   - Use firewall rules to restrict access
   - Monitor for unusual usage patterns

3. **Cost Control:**
   - Set strict daily limits
   - Monitor spending daily
   - Set up budget alerts in OpenAI dashboard
   - Use caching aggressively

4. **Monitoring:**
   - Set up uptime monitoring (UptimeRobot, etc.)
   - Log all errors
   - Track user metrics
   - Monitor API usage

---

## Quick Reference

### File Structure

```
lo-agent-bootcamp/
├── setup.py              # Automated setup wizard
├── app.py                # Main application (Week 4)
├── week4_features.py     # Production features module
├── run.sh / run.bat      # Quick launch scripts
├── .env                  # Configuration (create this)
├── .env.example          # Template
├── requirements.txt      # Dependencies
├── API_SETUP_GUIDE.md    # Detailed API instructions
├── DEPLOYMENT.md         # This file
├── README.md             # Project overview
├── scripts/
│   └── seed_data.py      # Pinecone seeding script
├── tests/                # Test suite
├── week3/                # Previous versions (reference)
└── archive/              # Old files (reference)
```

### Useful Commands

```bash
# Setup
python setup.py                    # Run setup wizard

# Launch
./run.sh                           # Quick launch (Mac/Linux)
run.bat                            # Quick launch (Windows)

# Manual
source env/bin/activate            # Activate venv
streamlit run app.py               # Start app
python scripts/seed_data.py        # Seed data

# Testing
pytest tests/ -v                   # Run all tests
pytest tests/test_week4_features.py  # Run specific test

# Maintenance
pip install --upgrade streamlit    # Update Streamlit
pip list --outdated                # Check for updates
```

### Support Resources

- **OpenAI:** https://help.openai.com/
- **Streamlit:** https://docs.streamlit.io/
- **Pinecone:** https://docs.pinecone.io/
- **GitHub Issues:** Create issue in repo
- **Bootcamp:** Ask in Slack/Discord

---

**Happy Deploying! 🚀**

For questions or issues, create an issue on GitHub or reach out to your bootcamp instructors.
