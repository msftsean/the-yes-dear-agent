# 🎯 Production Deployment Guide

![Version](https://img.shields.io/badge/version-v2.4.0-blue.svg)
![Status](https://img.shields.io/badge/status-production--ready-green.svg)
![API](https://img.shields.io/badge/api-hybrid--system-orange.svg)
![Tested](https://img.shields.io/badge/integration-fully--tested-green.svg)

## 🚀 **Quick Start**

### **Demo Mode (5 minutes)**
```bash
# 1. Clone and setup
git clone <repository>
cd lo-agent-bootcamp
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure OpenAI only
echo "OPENAI_API_KEY=your_key_here" > .env

# 4. Run application
streamlit run app.py
```

**Perfect for:** Bootcamp demos, presentations, development

### **Production Mode (15 minutes)**
```bash
# 1-2. Same as demo mode

# 3. Full API configuration
cp env.template .env
# Edit .env with all API keys

# 4. Verify connections
streamlit run app.py
# Toggle "Real APIs" ON to test
```

**Perfect for:** Live deployments, real-world usage

## 🔑 **API Configuration**

### **Required APIs**

#### **OpenAI** (Required for all modes)
- **Purpose**: GPT-5 and GPT-4o language models
- **Get Key**: https://platform.openai.com/api-keys
- **Cost**: ~$0.01-0.03 per conversation
- **Variable**: `OPENAI_API_KEY`

#### **Google Custom Search** (Optional - Production)
- **Purpose**: Live web search results
- **Get Key**: https://developers.google.com/custom-search/v1/introduction
- **Cost**: Free tier: 100 queries/day, then $5 per 1000 queries
- **Variables**: `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`

#### **Pinecone** (Optional - Production)
- **Purpose**: Vector database for document search
- **Get Key**: https://www.pinecone.io/
- **Cost**: Free tier available, then usage-based
- **Variable**: `PINECONE_API_KEY`

### **Configuration Examples**

#### **Demo Mode `.env`**
```env
OPENAI_API_KEY=sk-proj-abc123...
```

#### **Production Mode `.env`**
```env
OPENAI_API_KEY=sk-proj-abc123...
GOOGLE_API_KEY=AIza456...
GOOGLE_CSE_ID=012345...
PINECONE_API_KEY=abc789...
```

## 🏗️ **Architecture Overview**

### **Hybrid System Benefits**
- **Demo Safety**: Mock APIs ensure reliable presentations
- **Production Ready**: Real APIs provide live functionality
- **Cost Efficient**: Develop with mocks, deploy with real APIs
- **Scalable**: Easy transition between modes

### **Smart Routing Logic**
```python
def route_to_api(query, use_real_apis):
    if use_real_apis and has_required_keys():
        return real_api_call(query)
    else:
        return enhanced_mock_call(query)
```

### **Error Handling Strategy**
- Missing keys → Graceful fallback to mocks
- Network errors → Cached responses
- Rate limits → Intelligent backoff
- Invalid responses → Enhanced error messages

## 🌍 **Deployment Platforms**

### **Streamlit Cloud**
1. **Connect Repository**
   - Link GitHub repository
   - Streamlit auto-detects `streamlit run app.py`

2. **Configure Secrets**
   - Add API keys in Streamlit Cloud secrets
   - Use demo mode for public demos

3. **Deploy**
   - Automatic deployment on git push
   - Public URL for sharing

### **Docker Deployment**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### **Local Development**
```bash
# Development server
streamlit run app.py --server.port=8501

# Production server  
streamlit run app.py --server.port=80 --server.address=0.0.0.0
```

## 📊 **Monitoring & Analytics**

### **Built-in Metrics**
- Token usage tracking
- API response times
- Error rates and types
- User interaction patterns

### **Custom Monitoring**
```python
# Add to your deployment
import logging
logging.basicConfig(level=logging.INFO)

# Track API usage
if st.session_state.use_real_apis:
    log_api_usage(query, response_time, tokens_used)
```

## 🔒 **Security Considerations**

### **API Key Security**
- Never commit keys to version control
- Use environment variables exclusively
- Rotate keys regularly
- Monitor usage for anomalies

### **Rate Limiting**
```python
# Implement usage limits
MAX_QUERIES_PER_HOUR = 100
if get_user_query_count() > MAX_QUERIES_PER_HOUR:
    return "Rate limit exceeded"
```

### **Input Validation**
- Sanitize user inputs
- Validate query lengths
- Filter malicious content
- Log security events

## 🧪 **Testing Strategies**

### **Automated Testing**
```bash
# Unit tests
python -m pytest tests/

# Integration tests
python test_api_integration.py

# Load testing
python test_performance.py
```

### **Manual Testing Checklist**
- [ ] Demo mode functionality
- [ ] Real API integrations
- [ ] Error handling scenarios
- [ ] Mobile responsiveness
- [ ] Performance under load

## 📈 **Scaling Considerations**

### **Performance Optimization**
- Implement response caching
- Use async operations for API calls
- Optimize Streamlit rendering
- Monitor memory usage

### **Cost Management**
- Set API usage budgets
- Implement query limits per user
- Monitor costs regularly
- Use caching to reduce API calls

### **High Availability**
- Deploy on multiple servers
- Implement health checks
- Use load balancers
- Set up monitoring alerts

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Streamlit Won't Start**
```bash
# Check Python version
python --version  # Should be 3.12+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Streamlit cache
streamlit cache clear
```

#### **API Keys Not Working**
```bash
# Verify .env file
cat .env

# Test API keys manually
python -c "
from openai import OpenAI
client = OpenAI()
print('OpenAI connection: OK')
"
```

#### **Performance Issues**
```bash
# Monitor resource usage
htop  # or Task Manager on Windows

# Check Streamlit logs
tail -f ~/.streamlit/logs/streamlit.log
```

### **Debug Mode**
Add debug information to your deployment:
```python
if st.sidebar.button("Debug Info"):
    st.json({
        "api_keys_configured": check_api_keys(),
        "session_state": dict(st.session_state),
        "system_info": get_system_info()
    })
```

## 📚 **Additional Resources**

### **Documentation Links**
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Google Custom Search API](https://developers.google.com/custom-search/v1/reference)
- [Pinecone Documentation](https://docs.pinecone.io/)

### **Support Channels**
- GitHub Issues for bugs
- Streamlit Community Forum
- OpenAI Community Forum
- Stack Overflow for general questions

---

## 🎯 **Success Metrics**

After deployment, monitor these key indicators:
- **User Engagement**: Session duration, repeat visits
- **Technical Performance**: Response times, error rates
- **Cost Efficiency**: API usage vs. value delivered
- **User Satisfaction**: Feedback and adoption rates

Your Context-Aware Research Assistant is production-ready! 🚀