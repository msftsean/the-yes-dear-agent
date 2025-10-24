#!/usr/bin/env python3
"""
🚀 Yes Dear Assistant - One-Click Setup Script
==============================================
This script will help you set up the entire application from scratch.

Usage:
    python setup.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def check_python_version():
    """Check if Python version is 3.12 or higher"""
    print_header("Step 1: Checking Python Version")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print_error(f"Python 3.12+ required. You have {version.major}.{version.minor}.{version.micro}")
        print_info("Please install Python 3.12 or higher from https://www.python.org/downloads/")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_pip():
    """Check if pip is installed"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"],
                      check=True, capture_output=True)
        print_success("pip is installed")
        return True
    except subprocess.CalledProcessError:
        print_error("pip is not installed")
        return False

def create_virtual_env():
    """Create virtual environment if it doesn't exist"""
    print_header("Step 2: Setting Up Virtual Environment")

    venv_path = Path("env")
    if venv_path.exists():
        print_info("Virtual environment already exists")
        response = input("Do you want to recreate it? (y/N): ").strip().lower()
        if response == 'y':
            print_info("Removing existing virtual environment...")
            import shutil
            shutil.rmtree(venv_path)
        else:
            print_success("Using existing virtual environment")
            return True

    print_info("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "env"], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def get_pip_command():
    """Get the correct pip command based on OS"""
    if platform.system() == "Windows":
        return os.path.join("env", "Scripts", "pip")
    else:
        return os.path.join("env", "bin", "pip")

def install_dependencies():
    """Install required dependencies"""
    print_header("Step 3: Installing Dependencies")

    pip_cmd = get_pip_command()

    print_info("Upgrading pip...")
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        print_success("pip upgraded")
    except subprocess.CalledProcessError:
        print_warning("Failed to upgrade pip, continuing anyway...")

    print_info("Installing core dependencies (this may take a few minutes)...")
    core_deps = [
        "streamlit>=1.50.0",
        "openai>=1.109.1",
        "python-dotenv>=1.1.1",
        "requests>=2.31.0",
    ]

    try:
        subprocess.run([pip_cmd, "install"] + core_deps, check=True)
        print_success("Core dependencies installed")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install core dependencies: {e}")
        return False

    # Optional dependencies
    print_info("Installing optional dependencies...")
    optional_deps = [
        "google-api-python-client>=2.100.0",
        "pinecone-client>=3.0.0",
        "pytz>=2023.3",
        "pytest>=7.4.0"
    ]

    try:
        subprocess.run([pip_cmd, "install"] + optional_deps,
                      check=True, capture_output=True)
        print_success("Optional dependencies installed")
    except subprocess.CalledProcessError:
        print_warning("Some optional dependencies failed to install (this is OK)")

    return True

def create_env_file():
    """Create .env file from template"""
    print_header("Step 4: Creating Configuration File")

    env_path = Path(".env")
    env_example_path = Path(".env.example")

    if env_path.exists():
        print_warning(".env file already exists")
        response = input("Do you want to reconfigure it? (y/N): ").strip().lower()
        if response != 'y':
            print_info("Keeping existing .env file")
            return True

    # Copy from template
    if env_example_path.exists():
        import shutil
        shutil.copy(env_example_path, env_path)
        print_success(".env file created from template")
    else:
        # Create basic .env file
        with open(env_path, 'w') as f:
            f.write("# API Keys\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# Optional APIs\n")
            f.write("GOOGLE_API_KEY=your_google_api_key_here\n")
            f.write("GOOGLE_CSE_ID=your_google_cse_id_here\n")
            f.write("PINECONE_API_KEY=your_pinecone_api_key_here\n")
            f.write("PINECONE_ENVIRONMENT=us-east-1\n\n")
            f.write("# Production Settings\n")
            f.write("ENVIRONMENT=development\n")
            f.write("DAILY_SPENDING_LIMIT=100.00\n")
            f.write("ALERT_THRESHOLD=70.0\n")
            f.write("MAX_REQUESTS_PER_MINUTE=10\n")
            f.write("CACHE_TTL_SECONDS=3600\n")
        print_success(".env file created with defaults")

    return True

def configure_api_keys():
    """Interactive API key configuration"""
    print_header("Step 5: Configuring API Keys")

    print_info("You'll need at least an OpenAI API key to use this application.")
    print_info("Other APIs are optional - the app works with mock data if not provided.\n")

    # Read current .env
    env_path = Path(".env")
    with open(env_path, 'r') as f:
        env_content = f.read()

    # OpenAI API Key (Required)
    print(f"{Colors.BOLD}OpenAI API Key (REQUIRED){Colors.ENDC}")
    print("Get your key at: https://platform.openai.com/api-keys")
    openai_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()

    if openai_key and openai_key != "your_openai_api_key_here":
        env_content = env_content.replace("OPENAI_API_KEY=your_openai_api_key_here",
                                         f"OPENAI_API_KEY={openai_key}")
        print_success("OpenAI API key configured")
    elif not openai_key:
        print_warning("Skipped - You'll need to add this manually to .env file")

    # Google Search API (Optional)
    print(f"\n{Colors.BOLD}Google Custom Search API (OPTIONAL){Colors.ENDC}")
    print("For real web search functionality")
    print("Setup guide: https://developers.google.com/custom-search/v1/overview")
    response = input("Do you want to configure Google Search? (y/N): ").strip().lower()

    if response == 'y':
        google_key = input("Enter your Google API key: ").strip()
        google_cse = input("Enter your Custom Search Engine ID: ").strip()

        if google_key:
            env_content = env_content.replace("GOOGLE_API_KEY=your_google_api_key_here",
                                             f"GOOGLE_API_KEY={google_key}")
        if google_cse:
            env_content = env_content.replace("GOOGLE_CSE_ID=your_google_cse_id_here",
                                             f"GOOGLE_CSE_ID={google_cse}")
        print_success("Google Search API configured")

    # Pinecone API (Optional)
    print(f"\n{Colors.BOLD}Pinecone Vector Database (OPTIONAL){Colors.ENDC}")
    print("For document search functionality")
    print("Get your key at: https://www.pinecone.io/")
    response = input("Do you want to configure Pinecone? (y/N): ").strip().lower()

    if response == 'y':
        pinecone_key = input("Enter your Pinecone API key: ").strip()
        if pinecone_key:
            env_content = env_content.replace("PINECONE_API_KEY=your_pinecone_api_key_here",
                                             f"PINECONE_API_KEY={pinecone_key}")
            print_success("Pinecone API configured")

    # Write updated .env
    with open(env_path, 'w') as f:
        f.write(env_content)

    print_success("Configuration saved to .env file")
    return True

def seed_pinecone_data():
    """Optionally seed Pinecone with sample data"""
    print_header("Step 6: Seeding Sample Data (Optional)")

    # Check if Pinecone is configured
    from dotenv import load_dotenv
    load_dotenv()

    pinecone_key = os.getenv('PINECONE_API_KEY')
    if not pinecone_key or pinecone_key == 'your_pinecone_api_key_here':
        print_info("Pinecone not configured - skipping data seeding")
        print_info("You can run 'python scripts/seed_data.py' later to add sample data")
        return True

    response = input("Do you want to seed Pinecone with sample company documents? (y/N): ").strip().lower()

    if response == 'y':
        print_info("Seeding sample data...")
        # Check if seed script exists
        seed_script = Path("scripts/seed_data.py")
        if seed_script.exists():
            python_cmd = os.path.join("env", "Scripts", "python") if platform.system() == "Windows" else os.path.join("env", "bin", "python")
            try:
                subprocess.run([python_cmd, str(seed_script)], check=True)
                print_success("Sample data seeded successfully")
            except subprocess.CalledProcessError:
                print_warning("Failed to seed data - you can do this manually later")
        else:
            print_info("Seed script not found - skipping")

    return True

def verify_installation():
    """Verify the installation is working"""
    print_header("Step 7: Verifying Installation")

    # Check if .env has OpenAI key
    from dotenv import load_dotenv
    load_dotenv()

    openai_key = os.getenv('OPENAI_API_KEY')
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print_warning("OpenAI API key not configured")
        print_info("The app will not work without an OpenAI API key")
        print_info("Please edit .env file and add your OpenAI API key")
        return False

    print_success("OpenAI API key is configured")

    # Check if main files exist
    if not Path("app.py").exists():
        print_error("app.py not found!")
        return False

    if not Path("week4_features.py").exists():
        print_error("week4_features.py not found!")
        return False

    print_success("All required files present")
    print_success("Installation verified!")

    return True

def print_next_steps():
    """Print next steps for the user"""
    print_header("🎉 Setup Complete!")

    print(f"{Colors.OKGREEN}{Colors.BOLD}Your 'Yes Dear' Assistant is ready to use!{Colors.ENDC}\n")

    print(f"{Colors.BOLD}To start the application:{Colors.ENDC}")

    if platform.system() == "Windows":
        print(f"{Colors.OKCYAN}    env\\Scripts\\activate{Colors.ENDC}")
    else:
        print(f"{Colors.OKCYAN}    source env/bin/activate{Colors.ENDC}")

    print(f"{Colors.OKCYAN}    streamlit run app.py{Colors.ENDC}\n")

    print(f"{Colors.BOLD}Or use the quick launch script:{Colors.ENDC}")
    if platform.system() == "Windows":
        print(f"{Colors.OKCYAN}    .\\run.bat{Colors.ENDC}\n")
    else:
        print(f"{Colors.OKCYAN}    ./run.sh{Colors.ENDC}\n")

    print(f"{Colors.BOLD}Features included:{Colors.ENDC}")
    print("  ✅ Production-ready Week 4 application")
    print("  ✅ Cost monitoring and budget alerts")
    print("  ✅ Security validation (rate limiting, injection detection)")
    print("  ✅ Production dashboard with 7 feature tabs")
    print("  ✅ Comprehensive testing framework")
    print("  ✅ Error handling with retry logic\n")

    print(f"{Colors.BOLD}Useful commands:{Colors.ENDC}")
    print(f"  📚 View documentation: See README.md and docs/ folder")
    print(f"  🧪 Run tests: pytest tests/")
    print(f"  🌱 Seed data: python scripts/seed_data.py")
    print(f"  📝 View logs: Check moderation_log.jsonl (generated on first run)\n")

    print(f"{Colors.WARNING}Remember:{Colors.ENDC}")
    print("  • Keep your .env file secure (never commit it)")
    print("  • Monitor your OpenAI API usage/costs")
    print("  • Optional APIs (Google, Pinecone) enhance features but aren't required\n")

def main():
    """Main setup function"""
    print_header("🚀 Yes Dear Assistant - Setup Wizard")
    print(f"{Colors.BOLD}This wizard will help you set up the application from scratch.{Colors.ENDC}\n")

    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)

    # Check pip
    if not check_pip():
        print_error("Please install pip before continuing")
        sys.exit(1)

    # Step 2: Create virtual environment
    if not create_virtual_env():
        sys.exit(1)

    # Step 3: Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Step 4: Create .env file
    if not create_env_file():
        sys.exit(1)

    # Step 5: Configure API keys
    try:
        if not configure_api_keys():
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)

    # Step 6: Seed data (optional)
    try:
        seed_pinecone_data()
    except Exception as e:
        print_warning(f"Data seeding skipped: {e}")

    # Step 7: Verify installation
    verify_installation()

    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
