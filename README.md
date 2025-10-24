# The 'Yes Dear' Agent 🔍

![Version](https://img.shields.io/badge/Version-4.0.0-blue)
![Bootcamp](https://img.shields.io/badge/Bootcamp-Week%204%20Complete-success)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![APIs](https://img.shields.io/badge/APIs-Hybrid%20System-purple)

A sophisticated AI-powered research assistant built with Streamlit and OpenAI's GPT models. Your intelligent companion for tackling research tasks and honeydew lists with conversational AI and search capabilities.It was created during Tina Huang's Lonely Octopus October 2025 Agent Bootcamp

![Yes Dear Agent](assets/images/couple.png)

---

## 🎓 One-Click Setup

**Get the full app running in 5 minutes with our automated setup script!**

### 🚀 Quick Start (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/lo-agent-bootcamp.git
cd lo-agent-bootcamp

# 2. Run the automated setup wizard
python setup.py
```

That's it! The setup script will:
- ✅ Check your Python version
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create configuration file
- ✅ Guide you through API key setup
- ✅ Verify everything works

### 🎯 After Setup - Launch the App

**Mac/Linux:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

**Or manually:**
```bash
source env/bin/activate  # Mac/Linux
# env\Scripts\activate   # Windows
streamlit run app.py
```

### 🔑 API Keys Required

You'll need at minimum an **OpenAI API key** to use the app.

**Quick Guide:**
1. Go to https://platform.openai.com/api-keys
2. Sign up (free $5 credit for new users)
3. Create new API key
4. Add payment method (required after free credit)
5. Copy the key when prompted during setup

**Detailed instructions:** See [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) for step-by-step guides for all APIs.

**Optional APIs** (app works without these using mock data):
- **Google Custom Search** - For real web search
- **Pinecone** - For document search

### 📚 What's Included

This is a *Production-Ready** version with the following enterprise features:
- ✅ Cost monitoring and budget alerts ($100 daily limit default)
- ✅ Security validation (rate limiting, prompt injection detection, PII detection)
- ✅ Production dashboard with 7 feature tabs
- ✅ Comprehensive testing framework (10 tests: normal, edge, adversarial)
- ✅ Error handling with retry logic and circuit breakers
- ✅ Response caching and model cascading for cost optimization
- ✅ Sample company documents for testing document search

### 🌱 Seed Sample Data (Optional)

If you configured Pinecone, seed it with sample company policy documents:

```bash
source env/bin/activate  # Activate environment first
python scripts/seed_data.py
```

This creates 8 sample documents covering:
- HR policies (remote work, vacation, professional development)
- Security guidelines
- Product roadmap
- Customer onboarding
- Finance policies
- Engineering practices

---

## 📖 Documentation

- **[API Setup Guide](API_SETUP_GUIDE.md)** - Detailed instructions for getting all API keys
- **[README](README.md)** - Full feature documentation (you're here!)
- **[Week 4 Features](#-week-4--production-upgrade-features)** - Production features overview
- **[Troubleshooting](#-troubleshooting)** - Common issues and solutions

---

## 🌟 Features

### 💬 **Conversational AI**
- **🤖 Chat Interface**: Claude.ai-inspired conversational experience
- **🧠 Context Awareness**: Maintains conversation history and context
- **🔍 Research Assistant**: Specialized for research and information tasks
- **💡 Smart Responses**: GPT-4o powered with function calling capabilities

### 🛠️ **Search & Tools**
- **📚 Document Search**: Query private document collections (vector store integration)
- **🌐 Web Search**: Real-time internet information retrieval  
- **🔄 Hybrid API System**: Toggle between mock (demo-safe) and real API integrations
- **🔧 Tool Selection**: Dynamic enable/disable of search capabilities
- **📊 Usage Tracking**: Monitor API usage with detailed token consumption stats

### 🎨 **User Experience**
- **💙 "Yes Dear" Theme**: Honeydew list assistant branding
- **🎨 Modern UI**: Professional gradient design with real-time thinking display
- **📱 Responsive**: Works seamlessly across desktop and mobile
- **🚀 Fast & Reliable**: Optimized performance with graceful error handling
- **🔒 Secure**: Environment-based API key management
- **🔄 Demo/Production Toggle**: Switch between safe demos and live APIs

## 🚀 Quick Start

### Prerequisites

- Python 3.12+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/lo-agent-bootcamp.git
   cd lo-agent-bootcamp
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv env
   source env/Scripts/activate  # Windows
   # source env/bin/activate    # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit openai python-dotenv
   ```

4. **Configure environment**
   
   **Option A: Demo Mode (Recommended for bootcamp)**
   Create a `.env` file with just OpenAI:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   **Option B: Production Mode (Real APIs)**
   Copy the template from archive and add all keys:
   ```bash
   cp archive/env.template .env
   ```
   Then edit `.env` with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_CSE_ID=your_custom_search_engine_id_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   Navigate to `http://localhost:8501` (or the URL shown in terminal)

## � Bootcamp Progress

| Week | Assignment | Status | Key Features |
|------|------------|--------|--------------|
| **Week 1** | Task Generator | ✅ Complete | Basic AI agent, task breakdown, simple UI |
| **Week 2** | Research Assistant | ✅ Complete | Chat interface, function calling, search tools |
| **Week 3** | Multi-Agent System | ✅ Complete | Advanced multi-agent coordination, real-time updates |
| **Week 4** | Production Features | ✅ Complete | Cost monitoring, security, testing, optimization, dashboard |

> **Current Status**: Week 4 Complete - Enterprise-ready production application with comprehensive monitoring and security

## �🎯 How to Use

1. **Start Chatting**: Type your research question in the input box at the bottom
   - Example: "What is artificial intelligence and its applications?"
   
2. **Choose Mode & Tools**:
   - **🔄 API Mode**: Toggle "Real APIs" for live integrations or keep off for demo-safe mock data
   - **🌐 Web Search**: For current, real-time information (Google Custom Search when live)
   - **📚 Document Search**: For your private document collection (Pinecone integration ready)
   - **Both**: Comprehensive search across all sources

3. **Get Responses**: The assistant will:
   - Use selected tools to find relevant information
   - Provide well-cited, comprehensive answers
   - Maintain conversation context for follow-up questions

4. **Continue Conversation**: Ask follow-up questions to dive deeper:
   - "Can you elaborate on that?"
   - "What are the latest developments?"
   - "How does this relate to my previous question?"

5. **Manage Chat**: Use sidebar controls to clear history or view app information

## 🏗️ Project Structure

```
lo-agent-bootcamp/
├── app.py                    # Main Streamlit application (v2.4.0 - Production Ready)
├── .env                      # Environment variables (create this)
├── requirements.txt          # Project dependencies
├── DEMOS.md                  # Demo presentation guide
├── README.md                 # This file
├── assets/
│   ├── images/
│   │   └── couple.png        # Header image
│   └── docs/                 # Complete documentation
│       ├── RELEASE_NOTES.md  # Version history
│       ├── DEMO_SCRIPT.md    # Presentation scripts
│       ├── HYBRID_API_GUIDE.md # API integration guide
│       ├── PRODUCTION_GUIDE.md # Deployment instructions
│       └── ...               # Additional guides
├── env/                      # Virtual environment
└── archive/                  # Development files and templates
    ├── test_files/           # Test scripts and utilities
    ├── sample_documents/     # Demo data files
    ├── env.template          # Environment configuration template
    └── ...                   # Legacy files
```

## � **Documentation**

For detailed setup, deployment, and technical information:

### **📋 Quick References**
- **[🎪 DEMOS.md](DEMOS.md)** - Complete presentation guides and demo strategies
- **[🔄 Hybrid API Guide](assets/docs/HYBRID_API_GUIDE.md)** - API integration and configuration
- **[🚀 Production Guide](assets/docs/PRODUCTION_GUIDE.md)** - Deployment instructions

### **📖 Detailed Guides**
- **[📈 Release Notes](assets/docs/RELEASE_NOTES.md)** - Version history and features  
- **[🔧 Technical Guide](assets/docs/TECHNICAL_GUIDE.md)** - Architecture and implementation details
- **[🎯 Demo Scripts](assets/docs/DEMO_SCRIPT.md)** - Presentation materials and timing

## 🚀 **Quick Start**

### **Demo Mode (Recommended)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure OpenAI
echo "OPENAI_API_KEY=your_key_here" > .env

# 3. Run application
streamlit run app.py
```

### **Production Mode**
```bash
# 1. Copy configuration template
cp archive/env.template .env

# 2. Edit .env with all your API keys
# 3. Run with real API integrations enabled
streamlit run app.py
```

---

## 🚀 Week 4 — Production Upgrade Features

This repository includes comprehensive **Week 4 production features** for enterprise-ready AI applications with cost monitoring, testing, security, and operational excellence.

### 🎯 Production Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| **💰 Cost Monitoring** | Real-time token tracking with budget alerts | ✅ Complete |
| **🧪 Evaluation Framework** | 10-test suite (2 normal, 6 edge, 2 adversarial) | ✅ Complete |
| **🛡️ Error Handling** | Exponential backoff, circuit breaker, fallback | ✅ Complete |
| **🔒 Security** | Input validation, prompt injection, PII detection | ✅ Complete |
| **💾 Cost Optimization** | Response caching, model cascading | ✅ Complete |
| **📊 Production Dashboard** | Tabbed monitoring interface with 7 feature dashboards | ✅ Complete |
| **✅ Readiness Checklist** | 12-point production validation | ✅ Complete |

### 📦 Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your API keys (minimum: OPENAI_API_KEY)
   ```

3. **Run the Week 4 Production App**
   ```bash
   python -m streamlit run week4_app_final.py
   ```

4. **Access the Application**
   - Open the app in your browser (usually `http://localhost:8501`)
   - **💬 Chat Assistant** tab: Your "Yes Dear" conversational agent with couple.png branding
   - **📊 Production Dashboard** tab: Complete monitoring across 7 feature dashboards
   - All Week 4 production features integrated seamlessly

### 🎛️ Production Dashboard Features

The Production Dashboard tab includes **7 dedicated feature tabs** for comprehensive monitoring:

#### 💰 **Cost Monitoring**
- **Real-time Budget Tracking**: Monitor spending against daily limit ($100 default)
- **Budget Alerts**: Warning at 70%, Critical at 100%
- **Cost Breakdown**: See spending by agent (Coordinator, Research, Document, Summarizer)
- **Token Metrics**: Track input/output tokens per request
- **Session Analytics**: Average cost per request

#### 1. 💰 **Cost Monitor Tab**
- **Real-time Budget Tracking**: Progress bar showing spending vs daily limit
- **Budget Alerts**: Visual warnings (Warning at 70%, Critical at 100%)
- **Session Metrics**: Total spend, requests, average cost per request, total tokens
- **Token Breakdown**: Input vs output token usage
- **Cost by Agent**: See spending by Coordinator, Research, Document, Summarizer

#### 2. 🔒 **Security Tab**
- **Rate Limiting**: 10 requests/minute per user (configurable)
- **Active Security Features**: Rate limiting, prompt injection detection, PII detection, content moderation
- **Recent Activity**: Per-user request tracking
- **Moderation Log**: View recent events with blocked/allowed status
- **Download Logs**: Export full moderation log (JSONL format)

#### 3. 🏥 **System Health Tab**
- **API Configuration Status**: Visual indicators for OpenAI (required), Google Search (optional), Pinecone (optional)
- **Circuit Breakers**: Real-time circuit state monitoring (operational/open/half-open)
- **Environment Information**: Environment type, daily budget, alert threshold, rate limits

#### 4. ⚡ **Performance Tab**
- **Response Time Metrics**: Average, min, max response times
- **Success Rate**: Track query success percentage
- **Total Queries**: Request volume tracking
- **Response Time Distribution**: Statistical breakdown of latency

#### 5. 💾 **Optimization Tab**
- **Cache Metrics**: Cached response count and TTL settings
- **Toggle Controls**: Enable/disable response caching and model cascading
- **Cache Management**: Clear cache with one click
- **Cost Savings**: View estimated savings from optimization features

#### 6. 🧪 **Testing Tab**
- **Test Suite Overview**: 10 tests (2 normal, 6 edge, 2 adversarial)
- **Run Full Suite**: Execute all tests with one click
- **Test Results**: Pass rate, tests passed/failed metrics
- **Download Results**: Export test results as JSON
- **Results Preview**: View last test run details

#### 7. ✅ **Checklist Tab**
- **Production Readiness Validation**: 12-point comprehensive check
- **Readiness Score**: Overall production readiness percentage
- **Detailed Results**: Pass/fail status for each check with messages
- **One-Click Validation**: Run all checks instantly

### 🔒 Security Features

#### Input Validation
```python
# Automatic validation on all queries:
# ✅ Rate limiting (10 req/min per user)
# ✅ Input sanitization (remove control chars, scripts)
# ✅ Prompt injection detection
# ✅ PII detection (emails, SSNs, credit cards, phones)
# ✅ Content moderation (OpenAI Moderation API)
```

#### Blocked Patterns
- **Prompt Injection**: "ignore all previous instructions", "disregard previous", etc.
- **Jailbreak Attempts**: "DAN mode", "developer mode", etc.
- **Malicious Scripts**: `<script>`, `<iframe>`, etc.
- **PII**: Automatic detection and warning

### 💰 Cost Management

#### Budget Configuration
```bash
# In .env file:
DAILY_SPENDING_LIMIT=100.00      # Maximum daily spend
ALERT_THRESHOLD=70.0             # Warning threshold (%)
PER_USER_QUOTA=50                # Per-user request limit
```

#### Cost Tracking
- **Automatic Tracking**: All OpenAI API calls are monitored
- **Agent Breakdown**: See which agents cost the most
- **Budget Enforcement**: Requests blocked when limit reached
- **Real-time Alerts**: Visual warnings in dashboard

#### Pricing (GPT-4o)
- Input: $5.00 per 1M tokens
- Output: $15.00 per 1M tokens

### 🛡️ Error Handling

The system includes production-grade error handling:

#### Retry Logic
- **Exponential Backoff**: 1s, 2s, 4s, 8s, 16s delays
- **Jitter**: Random variation to prevent thundering herd
- **Max Retries**: 5 attempts before failure

#### Circuit Breaker
- **Threshold**: 5 consecutive failures
- **States**: Closed (normal) → Open (blocked) → Half-Open (testing)
- **Auto-Recovery**: 60-second cooldown before retry

#### Model Fallback
- **Primary**: GPT-4o for quality
- **Fallback**: GPT-3.5-turbo if GPT-4o fails
- **Graceful Degradation**: Never leave user without response

### 🧪 Evaluation Framework

#### Test Suite (10 Tests)
- **Normal Cases (20%)**: Basic functionality
  - Test 1: "What is artificial intelligence?"
  - Test 2: "Tell me about machine learning algorithms"

- **Edge Cases (60%)**: Robustness
  - Test 3: Empty input
  - Test 4: Very long query (3,600 chars)
  - Test 5: Special characters and scripts
  - Test 6: Multilingual (Chinese)
  - Test 7: Ambiguous query
  - Test 8: Multiple questions

- **Adversarial (20%)**: Security
  - Test 9: Prompt injection attempt
  - Test 10: Jailbreak attempt

#### Running Tests
1. Click **▶️ Run Eval Suite** in dashboard
2. Wait for all tests to complete
3. Review pass rate (target: 80%+)
4. Click **⬇️ Download Eval Results** for JSON export

#### Success Criteria
- ✅ 80%+ pass rate required
- ✅ No crashes on any test
- ✅ Security tests must pass

### 📊 Monitoring & Analytics

#### Session Metrics
- Total requests processed
- Total cost incurred
- Average cost per request
- Token usage (input/output)
- Success/error rates

#### Agent Performance
- Individual agent costs
- Agent execution times
- Agent success rates
- Error tracking per agent

### 🔧 Configuration

#### Environment Variables
See [.env.example](.env.example) for full configuration options.

**Required:**
- `OPENAI_API_KEY`: Your OpenAI API key

**Optional (Real APIs):**
- `GOOGLE_API_KEY`: Google Custom Search
- `GOOGLE_CSE_ID`: Search Engine ID
- `PINECONE_API_KEY`: Vector database

**Week 4 Production:**
- `ENVIRONMENT`: development/staging/production
- `DAILY_SPENDING_LIMIT`: Daily budget in dollars
- `ALERT_THRESHOLD`: Warning threshold percentage
- `MAX_REQUESTS_PER_MINUTE`: Rate limit
- `CACHE_TTL_SECONDS`: Cache expiration time

### 📝 Usage Examples

#### Basic Usage
```bash
# Run with default settings (demo mode)
streamlit run week3/app_multi_agent.py
```

#### Production Mode
```bash
# Enable real APIs in the sidebar
# 1. Check "🔴 Use Real APIs"
# 2. Monitor costs in dashboard
# 3. Watch for budget alerts
```

#### Running Tests
```bash
# Automated tests
pytest tests/ -v

# Or use the dashboard UI
# Click "▶️ Run Eval Suite" in sidebar
```

### 📁 Key Files

- **`week3/app_multi_agent.py`**: Main multi-agent application
- **`week4_features.py`**: Production feature classes
- **`.env.example`**: Configuration template
- **`tests/`**: Comprehensive test suite
- **`eval_results.json`**: Test results (generated)
- **`moderation_log.jsonl`**: Moderation events (generated)

### 🎓 Learning Outcomes

After implementing Week 4 features, you'll understand:
- ✅ Production cost monitoring and budget protection
- ✅ Comprehensive testing strategies (normal/edge/adversarial)
- ✅ Error handling patterns (retry, circuit breaker, fallback)
- ✅ Security best practices (validation, moderation, PII)
- ✅ Performance optimization (caching, model cascading)
- ✅ Operational monitoring and observability
- ✅ Production readiness validation

### 🚨 Important Notes

- **Cost Tracking**: Real-time for all OpenAI API calls
- **Security**: Input validation runs on every query
- **Testing**: Evaluation suite available in dashboard
- **Monitoring**: Full observability in production dashboard
- **Moderation**: Events logged to file and session state
- **Caching**: Optional optimization to reduce costs

### 🐛 Troubleshooting

**Budget Exceeded Error**
- Increase `DAILY_SPENDING_LIMIT` in `.env`
- Clear cache to reset session spend
- Use "🔄 Reset System" button

**Security Blocks Input**
- Check moderation log for details
- Rephrase query without trigger words
- Avoid sharing PII in queries

**Tests Failing**
- Check OpenAI API key is valid
- Ensure internet connection
- Review test criteria in results

**Circuit Breaker Open**
- Wait 60 seconds for auto-recovery
- Check API service status
- Review error logs in dashboard


**📖 See [Production Guide](assets/docs/PRODUCTION_GUIDE.md) for detailed setup instructions.**

## 🐛 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'dotenv'"**
   ```bash
   pip install python-dotenv
   ```

2. **"OPENAI_API_KEY not found"**
   - Ensure `.env` file exists in root directory
   - Check API key format in `.env` file

3. **"No tasks were generated"**
   - Verify API key is valid and has credits
   - Check internet connection
   - Try a different model (GPT-4 instead of GPT-4o)

4. **Virtual Environment Issues**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

### Debug Mode
If issues persist, check the token usage expander for detailed API response information.

## 🛠️ Development

### Running in Development Mode
```bash
# Activate virtual environment
source env/Scripts/activate

# Run with auto-reload
streamlit run app.py --server.runOnSave true
```

### File Organization
- **Production**: Only `app.py`, `couple.png`, and `.env` needed
- **Development**: All files in `archive/` folder for reference
- **Testing**: Various test implementations available in archive

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## � Documentation

### 📋 Project Documentation
- **[Release Notes](assets/docs/RELEASE_NOTES.md)** - Complete version history, bootcamp progress, and feature evolution
- **[Week 2 Demo Guide](assets/docs/WEEK2_DEMO_GUIDE.md)** - Strategic demonstration framework with testing protocols
- **[Model Comparison Test](assets/docs/MODEL_COMPARISON_TEST.md)** - Comprehensive GPT-5 vs GPT-4o testing framework

### 🎪 Demo Materials
- **[Demo Setup Guide](DEMOS.md)** - Complete guide for presenting your research assistant with scripts and timing

## �📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Special Thanks

**🐙 Lonely Octopus** - For creating an amazing AI agent bootcamp that made this project possible.

**Special recognition to Tina** - For delivering inspiration and guidance to so many aspiring AI developers. Your mentorship and vision have empowered countless learners to build production-ready AI applications.

### Technology

- Built with [Streamlit](https://streamlit.io/) for the beautiful web interface
- Powered by [OpenAI](https://openai.com/) for intelligent AI capabilities
- Enhanced with [Microsoft Agent Framework]([https://](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview) for multi-agent orchestration
- Inspired by the need for better project planning and conversational AI assistants

## � Version History

See [Release Notes](assets/docs/RELEASE_NOTES.md) for detailed version history, bootcamp progress, and feature evolution.

**Current Version**: 4.0.0 - "Yes Dear Production Assistant"
**Bootcamp Status**: Week 4 Complete ✅ - Enterprise Production Ready

##  Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the [Week 2 Demo Guide](assets/docs/WEEK2_DEMO_GUIDE.md) for comprehensive testing scenarios
3. Check [Release Notes](assets/docs/RELEASE_NOTES.md) for version-specific information
4. Review [Model Comparison Test](assets/docs/MODEL_COMPARISON_TEST.md) for advanced testing
5. Open an issue on GitHub

---

**Happy Researching! 🔍💕**

*Your intelligent companion for tackling research tasks and honeydew lists with the power of conversational AI.*
