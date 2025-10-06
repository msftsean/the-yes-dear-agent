import streamlit as st
import sys
import traceback

st.write("🔍 **DEBUG MODE - App.py Analysis**")
st.write("---")

try:
    st.write("✅ **Step 1**: Basic Streamlit import successful")
    
    # Test OpenAI import
    try:
        from openai import OpenAI
        st.write("✅ **Step 2**: OpenAI import successful")
    except Exception as e:
        st.error(f"❌ **Step 2**: OpenAI import failed: {e}")
        st.write("**Solution**: Run `pip install openai` in your virtual environment")
    
    import os
    st.write("✅ **Step 3**: OS import successful")
    
    # Test page configuration
    try:
        st.set_page_config(
            page_title="AI Assistant",
            page_icon="🤖",
            layout="wide"
        )
        st.write("⚠️ **Step 4**: Page config attempted (may show warning if already set)")
    except Exception as e:
        st.error(f"❌ **Step 4**: Page config failed: {e}")
        st.write("**Note**: This is normal if page config was already set")
    
    # Test basic UI elements
    try:
        st.title("🤖 AI Technical Assistant")
        st.markdown("Ask any technical question and get clear, concise answers!")
        st.write("✅ **Step 5**: Title and markdown rendering successful")
    except Exception as e:
        st.error(f"❌ **Step 5**: Title/markdown failed: {e}")
    
    # Test sidebar
    try:
        with st.sidebar:
            st.header("Configuration")
            api_key = st.text_input(
                "Enter your OpenAI API Key:",
                type="password",
                help="You can get your API key from https://platform.openai.com/api-keys"
            )
            
            model_choice = st.selectbox(
                "Select Model:",
                ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
                help="GPT-4 models are more capable but cost more"
            )
            
            temperature = st.slider(
                "Temperature:",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1,
                help="Lower values make responses more focused and deterministic"
            )
        st.write("✅ **Step 6**: Sidebar rendering successful")
    except Exception as e:
        st.error(f"❌ **Step 6**: Sidebar failed: {e}")
        st.code(traceback.format_exc())
    
    # Test main content area
    try:
        if api_key:
            st.success("🔑 API key provided!")
            
            # Test OpenAI client initialization
            try:
                client = OpenAI(api_key=api_key)
                st.write("✅ **Step 7a**: OpenAI client created successfully")
            except Exception as e:
                st.error(f"❌ **Step 7a**: OpenAI client creation failed: {e}")
            
            # Test input elements
            user_question = st.text_area(
                "Enter your technical question:",
                placeholder="e.g., How does machine learning work?",
                height=100
            )
            
            if st.button("Get Answer", type="primary"):
                st.info("Button clicked! (Response generation disabled in debug mode)")
            
            st.write("✅ **Step 7b**: Input elements rendered successfully")
            
        else:
            # Test instructions section
            st.info("👈 Please enter your OpenAI API key in the sidebar to get started.")
            
            st.markdown("""
            ### How to get your OpenAI API Key:
            1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
            2. Sign in to your account
            3. Click "Create new secret key"
            4. Copy the key and paste it in the sidebar
            
            ### Features:
            - 🔧 Multiple model options (GPT-3.5, GPT-4)
            - 🎛️ Adjustable temperature for response creativity
            - 📊 Token usage tracking
            - 💬 Chat history
            - 🔒 Secure API key input
            """)
            
            st.write("✅ **Step 7c**: Instructions section rendered successfully")
    
    except Exception as e:
        st.error(f"❌ **Step 7**: Main content area failed: {e}")
        st.code(traceback.format_exc())
    
    # Test footer
    try:
        st.markdown("---")
        st.markdown("Built with Streamlit and OpenAI API")
        st.write("✅ **Step 8**: Footer rendered successfully")
    except Exception as e:
        st.error(f"❌ **Step 8**: Footer failed: {e}")
    
    # Environment info
    st.write("---")
    st.write("**🔧 Environment Information:**")
    st.write(f"- Python version: {sys.version}")
    st.write(f"- Streamlit version: {st.__version__}")
    
    # Test if we can import and check OpenAI version
    try:
        import openai
        st.write(f"- OpenAI version: {openai.__version__}")
    except:
        st.write("- OpenAI version: Not available")

except Exception as e:
    st.error(f"**CRITICAL ERROR**: {e}")
    st.code(traceback.format_exc())

st.write("---")
st.success("🎉 **DEBUG COMPLETE** - If you see this message, basic Streamlit rendering is working!")