import streamlit as st
from openai import OpenAI
import os

print("DEBUG: Starting app execution")

try:
    # Page configuration
    st.set_page_config(
        page_title="AI Assistant",
        page_icon="🤖",
        layout="wide"
    )
    print("DEBUG: Page config set successfully")
except Exception as e:
    print(f"DEBUG: Error setting page config: {e}")

try:
    # Title and description
    st.title("🤖 AI Technical Assistant")
    st.markdown("Ask any technical question and get clear, concise answers!")
    print("DEBUG: Title and description rendered")
except Exception as e:
    print(f"DEBUG: Error rendering title: {e}")

try:
    # Sidebar for API key input
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
    print("DEBUG: Sidebar rendered successfully")
except Exception as e:
    print(f"DEBUG: Error rendering sidebar: {e}")
    st.error(f"Sidebar error: {e}")

try:
    # Main interface
    if api_key:
        st.success("API key provided - main interface should show")
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Input section
        user_question = st.text_area(
            "Enter your technical question:",
            placeholder="e.g., How does machine learning work?",
            height=100
        )
        
        # Generate response button
        if st.button("Get Answer", type="primary"):
            if user_question:
                try:
                    with st.spinner("Generating response..."):
                        # Prepare messages for the model
                        messages = [
                            {"role": "system", "content": "You are a technical assistant that provides clear, accurate, and helpful explanations for technical questions."},
                            {"role": "user", "content": f"Please help me answer this technical question:\n{user_question}. Write your answer in clear and concise bullet points."}
                        ]
                        
                        # Send request to OpenAI
                        response = client.chat.completions.create(
                            model=model_choice,
                            messages=messages,
                            temperature=temperature
                        )
                        
                        # Extract and display response
                        response_message = response.choices[0].message.content
                        
                        # Display the response in a nice format
                        st.subheader("📝 Response:")
                        st.markdown(response_message)
                        
                        # Optional: Show token usage
                        if hasattr(response, 'usage'):
                            with st.expander("Token Usage"):
                                st.write(f"Prompt tokens: {response.usage.prompt_tokens}")
                                st.write(f"Completion tokens: {response.usage.completion_tokens}")
                                st.write(f"Total tokens: {response.usage.total_tokens}")
                                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.error("Please check your API key and try again.")
            else:
                st.warning("Please enter a question before generating a response.")
        
        # Chat history section (optional enhancement)
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Display previous conversations
        if st.session_state.chat_history:
            with st.expander("Chat History"):
                for i, (question, answer) in enumerate(reversed(st.session_state.chat_history)):
                    st.markdown(f"**Q{len(st.session_state.chat_history)-i}:** {question}")
                    st.markdown(f"**A{len(st.session_state.chat_history)-i}:** {answer}")
                    st.divider()
        
        # Save to history when answer is generated
        if st.button("Clear History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")

    else:
        # Instructions when no API key is provided
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

    print("DEBUG: Main content rendered successfully")
except Exception as e:
    print(f"DEBUG: Error in main content: {e}")
    st.error(f"Main content error: {e}")

try:
    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit and OpenAI API")
    print("DEBUG: Footer rendered successfully")
except Exception as e:
    print(f"DEBUG: Error rendering footer: {e}")

print("DEBUG: App execution completed")