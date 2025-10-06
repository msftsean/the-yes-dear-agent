# The 'Yes Dear' Assistant 🔍

![Version](https://img.shields.io/badge/Version-2.2.0-blue)
![Bootcamp](https://img.shields.io/badge/Bootcamp-Week%202%20Complete-success)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

A sophisticated AI-powered research assistant built with Streamlit and OpenAI's GPT models. Your intelligent companion for tackling research tasks and honeydew lists with conversational AI and search capabilities.

![Yes Dear Agent](assets/images/couple.png)

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
   git clone https://github.com/msftsean/lo-agent-bootcamp.git
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
| **Week 3** | Advanced Features | 🔄 Coming Soon | Enhanced integrations, production features |

> **Current Status**: Week 2 Complete - Full conversational research assistant with tool integration

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

- Built with [Streamlit](https://streamlit.io/) for the beautiful web interface
- Powered by [OpenAI](https://openai.com/) for intelligent task generation
- Inspired by the need for better project planning and task management

## � Version History

See [Release Notes](assets/docs/RELEASE_NOTES.md) for detailed version history, bootcamp progress, and feature evolution.

**Current Version**: 2.4.0 - "Production-Ready Research Assistant"  
**Bootcamp Status**: Week 2 Complete ✅ + Production Deployment Ready

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