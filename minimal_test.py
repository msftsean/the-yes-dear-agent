import streamlit as st
from openai import OpenAI

st.title("🤖 AI Technical Assistant")
st.markdown("Ask any technical question and get clear, concise answers!")

# Test the problematic part
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        help="You can get your API key from https://platform.openai.com/api-keys"
    )

st.write("**API Key Status:**", "Provided" if api_key else "Not provided")

# The issue is likely here - let me test the conditional logic
if api_key:
    st.success("✅ API key provided - showing main interface")
    # This section might be causing issues
    try:
        client = OpenAI(api_key=api_key)
        st.write("OpenAI client initialized successfully")
    except Exception as e:
        st.error(f"OpenAI client error: {e}")
else:
    st.info("👈 Please enter your OpenAI API key in the sidebar to get started.")
    st.markdown("This should always show when no API key is provided")

st.markdown("---")
st.markdown("Footer should always show")