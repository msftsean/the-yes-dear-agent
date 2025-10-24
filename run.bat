@echo off
REM Quick launcher for Yes Dear Assistant (Windows)

echo.
echo 🚀 Starting Yes Dear Assistant...
echo.

REM Check if virtual environment exists
if not exist "env" (
    echo ❌ Virtual environment not found!
    echo Please run setup first: python setup.py
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found
    echo Creating from template...
    copy .env.example .env
    echo ✅ Created .env file - please add your API keys
)

REM Activate virtual environment
echo 📦 Activating virtual environment...
call env\Scripts\activate.bat

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit not installed!
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Launch the app
echo ✨ Launching application...
echo 📱 The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app.py
