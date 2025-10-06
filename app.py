import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Check for OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Define placeholder vector store ID
VECTOR_STORE_ID = "vs_placeholder_id_12345"

# Streamlit UI
st.set_page_config(
    page_title="Context-Aware Research Assistant",
    page_icon="🔍",
    layout="centered"
)

# Add CSS for center alignment
st.markdown("""
<style>
    .stApp > div > div > div > div {
        text-align: center;
    }
    .stCheckbox > div {
        text-align: center;
    }
    .stAlert {
        text-align: center;
    }
    .stSuccess {
        text-align: center;
    }
    .stError {
        text-align: center;
    }
    .stWarning {
        text-align: center;
    }
    .stInfo {
        text-align: center;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: center !important;
    }
    p {
        text-align: center !important;
    }
    .chat-message {
        text-align: left !important;
    }
</style>
""", unsafe_allow_html=True)

# Center the main content
col1, col2, col3 = st.columns([1, 7, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🔍 Context-Aware Research Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your intelligent research companion with document knowledge and web search capabilities</p>", unsafe_allow_html=True)
    
    # Add couple image
    st.image("couple.png", width="stretch", caption="")

    # Check if API key is available
    if not OPENAI_API_KEY:
        st.error("❌ OPENAI_API_KEY not found in environment variables!")
        st.info("Please add your OpenAI API key to your .env file")
        st.stop()

    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Search tool selection UI
        st.markdown("### 🔧 Research Tools")
        col_web, col_doc, col_both = st.columns(3)
        
        with col_web:
            use_web_search = st.checkbox("🌐 Web Search", value=True, help="Search the internet for real-time information")
        
        with col_doc:
            use_doc_search = st.checkbox("📚 Document Search", value=True, help="Search your private document collection")
        
        with col_both:
            if use_web_search and use_doc_search:
                st.success("🔄 Both Sources Active")
            elif use_web_search:
                st.info("🌐 Web Only")
            elif use_doc_search:
                st.info("📚 Docs Only")
            else:
                st.warning("⚠️ No Sources Selected")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        st.markdown("---")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask me anything about your documents or search the web..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Researching your question..."):
                    try:
                        # Prepare tools based on user selection
                        tools = []
                        
                        if use_doc_search:
                            tools.append({
                                "type": "file_search",
                                "file_search": {
                                    "vector_store_ids": [VECTOR_STORE_ID]
                                }
                            })
                        
                        if use_web_search:
                            tools.append({
                                "type": "web_search_preview"
                            })

                        # Prepare messages with system prompt and chat history
                        system_message = {
                            "role": "system",
                            "content": """You are a research assistant who helps users find information from their private document collection and the web.

TASK: Answer questions accurately by searching available sources (vector store documents and/or web), and provide well-cited, clear responses.

OUTPUT: Clear, well-formatted answers using markdown. Always cite sources when using search tools. Maintain conversational context.

CONSTRAINTS: Never fabricate information - if you don't know, say so. Acknowledge when information might be incomplete."""
                        }
                        
                        # Build complete message history
                        messages_for_api = [system_message] + st.session_state.messages

                        # Prepare API parameters
                        api_params = {
                            "model": "gpt-4o",
                            "messages": messages_for_api,
                            "max_completion_tokens": 1500,
                            "temperature": 0.7
                        }
                        
                        # Add tools if any are selected
                        if tools:
                            api_params["tools"] = tools

                        # Make API call
                        response = client.chat.completions.create(**api_params)
                        
                        # Extract response content
                        assistant_message = response.choices[0].message.content
                        
                        # Display response
                        if assistant_message:
                            st.markdown(assistant_message)
                            
                            # Add assistant response to chat history
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": assistant_message
                            })
                            
                            # Show token usage
                            if hasattr(response, 'usage'):
                                with st.expander("📊 Usage Stats"):
                                    st.write(f"**Prompt tokens:** {response.usage.prompt_tokens}")
                                    st.write(f"**Completion tokens:** {response.usage.completion_tokens}")
                                    st.write(f"**Total tokens:** {response.usage.total_tokens}")
                        else:
                            st.error("❌ No response generated. Please try again.")
                        
                    except Exception as e:
                        error_message = f"❌ Error: {str(e)}"
                        st.error(error_message)
                        
                        # Add error to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": error_message
                        })

        # Chat controls
        if st.session_state.messages:
            st.markdown("---")
            col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
            with col_clear2:
                if st.button("🗑️ Clear Chat History"):
                    st.session_state.messages = []
                    st.rerun()

    except Exception as e:
        st.error(f"❌ Error initializing OpenAI client: {str(e)}")
        st.info("Please check your API key in the .env file")

    # Footer
    st.markdown("<hr style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Built with Streamlit and OpenAI API</p>", unsafe_allow_html=True)