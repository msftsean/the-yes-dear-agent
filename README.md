# The Yes 🤖 Dear Agent

A sophisticated AI-powered task breakdown application built with Streamlit and OpenAI's GPT models. Transform your high-level goals into actionable, structured task lists with just a few clicks.

![Yes Dear Agent](couple.png)

## 🌟 Features

- **🎯 Intelligent Task Breakdown**: Convert complex goals into manageable, time-bound tasks
- **🤖 Multiple AI Models**: Choose from GPT-4o, GPT-4, and GPT-4-turbo for optimal results  
- **🎨 Beautiful UI**: Centered, responsive design with custom styling
- **📚 Task History**: Keep track of all your previous task generations
- **📊 Token Usage Tracking**: Monitor API usage with detailed token consumption stats
- **💾 Session Persistence**: Tasks remain visible until you generate new ones
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

## 🎯 How to Use

1. **Enter Your Goal**: Describe what you want to accomplish in the text area
   - Example: "Build a customer support chatbot using GPT-4"
   
2. **Select AI Model**: Choose the model that best fits your needs:
   - **GPT-4o**: Latest and most capable (default)
   - **GPT-4**: Reliable and powerful
   - **GPT-4-turbo**: Fast and efficient

3. **Generate Tasks**: Click the "Generate Tasks" button to create your breakdown

4. **Review Results**: Your tasks will appear with:
   - Numbered, hierarchical structure
   - Clear dependencies and timelines
   - Actionable, concrete steps

5. **View History**: Access previous task generations in the expandable history section

## 🏗️ Project Structure

```
lo-agent-bootcamp/
├── app.py              # Main Streamlit application
├── couple.png          # Header image
├── .env                # Environment variables (create this)
├── env/                # Virtual environment
├── .venv/              # Alternative virtual environment
├── archive/            # Legacy files and tests
│   ├── agent.py        # Alternative agent implementation
│   ├── main.py         # Console-based version
│   ├── *_test.py       # Various test files
│   └── *_backup.py     # Backup versions
└── README.md           # This file
```

## 🔧 Technical Details

### Core Technologies
- **Frontend**: Streamlit with custom CSS styling
- **AI Model**: OpenAI GPT models (4o, 4, 4-turbo)
- **Environment Management**: python-dotenv
- **Language**: Python 3.12+

### Key Components
- **Task Generation**: Specialized system prompts for optimal task breakdown
- **UI Layout**: Responsive centered design with 1:7:1 column ratio
- **Session Management**: Streamlit session state for persistence
- **Error Handling**: Comprehensive error management and user feedback

### API Configuration
- **Model Selection**: Dynamic model switching
- **Token Limits**: 1500 max completion tokens
- **Temperature**: 0.7 for balanced creativity (GPT-4 models)
- **Response Format**: Structured markdown with numbered tasks

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

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the archived test files for examples
3. Open an issue on GitHub

---

**Happy Task Breaking! 🎉**

*Transform your ambitious goals into achievable action items with the power of AI.*