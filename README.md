# The 'Yes Dear' Assistant 🔍

![Version](https://img.shields.io/badge/Version-2.1.0-blue)
![Bootcamp](https://img.shields.io/badge/Bootcamp-Week%202%20Complete-success)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

A sophisticated AI-powered research assistant built with Streamlit and OpenAI's GPT models. Your intelligent companion for tackling research tasks and honeydew lists with conversational AI and search capabilities.

![Yes Dear Agent](couple.png)

## 🌟 Features

### 💬 **Conversational AI**
- **🤖 Chat Interface**: Claude.ai-inspired conversational experience
- **🧠 Context Awareness**: Maintains conversation history and context
- **🔍 Research Assistant**: Specialized for research and information tasks
- **💡 Smart Responses**: GPT-4o powered with function calling capabilities

### 🛠️ **Search & Tools**
- **📚 Document Search**: Query private document collections (vector store integration)
- **🌐 Web Search**: Real-time internet information retrieval
- **🔧 Tool Selection**: Dynamic enable/disable of search capabilities
- **📊 Usage Tracking**: Monitor API usage with detailed token consumption stats

### 🎨 **User Experience**
- **� "Yes Dear" Theme**: Honeydew list assistant branding
- **🎨 Modern UI**: Professional gradient design with sidebar navigation
- **📱 Responsive**: Works seamlessly across desktop and mobile
- **🚀 Fast & Reliable**: Optimized performance with graceful error handling
- **🔒 Secure**: Environment-based API key management

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
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
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
   
2. **Choose Tools**: Select your search preferences:
   - **🌐 Web Search**: For current, real-time information
   - **📚 Document Search**: For your private document collection
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
├── app.py              # Main Streamlit application (Week 2 - Research Assistant)
├── couple.png          # Header image
├── .env                # Environment variables (create this)
├── requirements.txt    # Project dependencies
├── RELEASE_NOTES.md    # Version history and bootcamp progress
├── TEST_SCRIPT.md      # Comprehensive testing guide
├── env/                # Virtual environment
├── archive/            # Week 1 files and development history
│   ├── agent.py        # Week 1 - Alternative agent implementation
│   ├── app_backup.py   # Week 1 - Task generator backup
│   ├── *_test.py       # Development test files
│   └── virtualenv-readme.md # Setup documentation
└── README.md           # This file
```

## 🔧 Technical Details

### Core Technologies
- **Frontend**: Streamlit with Claude.ai-inspired custom CSS
- **AI Model**: OpenAI GPT-4o with function calling
- **Search Tools**: Document search (vector store) + Web search
- **Environment Management**: python-dotenv for secure API keys
- **Language**: Python 3.12+

### Key Components
- **Conversational AI**: Chat interface with context memory
- **Function Calling**: OpenAI tools integration for search capabilities
- **UI Layout**: Modern gradient design with fixed bottom input
- **Session Management**: Streamlit session state for chat persistence
- **Error Handling**: Graceful degradation and user-friendly messages

### API Configuration
- **Model**: GPT-4o (latest and most capable)
- **Token Limits**: 1500 max completion tokens
- **Temperature**: 0.7 for balanced accuracy and creativity
- **Tools**: Dynamic function calling based on user selection
- **Context**: Full conversation history maintained

## 🎨 UI Features

### Visual Design
- **Centered Layout**: Professional, focused appearance
- **Custom CSS**: Enhanced styling for better UX
- **Responsive Images**: Proportional scaling across devices
- **Color Scheme**: Clean, modern aesthetic

### User Experience
- **Left-Justified Tasks**: Optimal readability for structured content
- **Centered Controls**: Intuitive form element placement
- **Visual Feedback**: Success/error states with appropriate colors
- **Progressive Disclosure**: Collapsible sections for advanced features

## 🔒 Security Best Practices

- **Environment Variables**: API keys stored securely in `.env`
- **Git Ignore**: Sensitive files excluded from version control
- **Error Handling**: No sensitive data exposed in error messages

## 📊 Performance

- **Token Efficiency**: Optimized prompts for cost-effective API usage
- **Session Persistence**: Efficient state management
- **Responsive Loading**: Spinner feedback during API calls

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

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the beautiful web interface
- Powered by [OpenAI](https://openai.com/) for intelligent task generation
- Inspired by the need for better project planning and task management

## � Version History

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for detailed version history, bootcamp progress, and feature evolution.

**Current Version**: 2.1.0 - "The 'Yes Dear' Assistant"  
**Bootcamp Status**: Week 2 Complete ✅

## �📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the [TEST_SCRIPT.md](TEST_SCRIPT.md) for comprehensive testing scenarios
3. Check [RELEASE_NOTES.md](RELEASE_NOTES.md) for version-specific information
4. Review archived files for development examples
5. Open an issue on GitHub

---

**Happy Researching! 🔍💕**

*Your intelligent companion for tackling research tasks and honeydew lists with the power of conversational AI.*