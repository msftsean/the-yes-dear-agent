#!/bin/bash
# Quick launcher for Yes Dear Assistant (Mac/Linux)

echo "🚀 Starting Yes Dear Assistant..."
echo ""

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup first: python setup.py"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file - please add your API keys"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source env/bin/activate

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Launch the app
echo "✨ Launching application..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
