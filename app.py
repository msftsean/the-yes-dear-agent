import streamlit as st
import os
import json
from datetime import datetime
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
    page_title="The 'Yes Dear' Assistant",
    page_icon="🔍",
    layout="centered"
)

# Add CSS for Claude-like interface
st.markdown("""
<style>
    /* Main app container */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Chat container */
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Tool selection styling */
    .tool-selection {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e1e5e9;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Chat input at bottom */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem;
        border-top: 1px solid #e1e5e9;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 999;
    }
    
    /* Make room for fixed input */
    .main-content {
        padding-bottom: 120px;
    }
    
    /* Chat messages */
    .stChatMessage {
        margin-bottom: 1rem;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Hide default streamlit elements */
    .stDeployButton {
        display: none;
    }
    
    /* Tool checkboxes */
    .stCheckbox {
        margin: 0.2rem 0;
    }
    
    /* Success/error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main container with proper spacing
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="main-header">
    <h1>🔍 The 'Yes Dear' Assistant</h1>
    <p>Your intelligent research companion with document knowledge and web search capabilities<br>that will help you with your honeydew list</p>
</div>
""", unsafe_allow_html=True)

# Check if API key is available
if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY not found in environment variables!")
    st.info("Please add your OpenAI API key to your .env file")
    st.stop()

# Initialize OpenAI client
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Tool selection in a nice container
    with st.container():
        st.markdown('<div class="tool-selection">', unsafe_allow_html=True)
        st.markdown("**🔧 Research Tools**")
        col_web, col_doc, col_status = st.columns([1, 1, 1])
        
        with col_web:
            use_web_search = st.checkbox("🌐 Web Search", value=True, help="Search the internet for real-time information")
        
        with col_doc:
            use_doc_search = st.checkbox("📚 Document Search", value=True, help="Search your private document collection")
        
        with col_status:
            if use_web_search and use_doc_search:
                st.success("🔄 Both Active")
            elif use_web_search:
                st.info("🌐 Web Only")
            elif use_doc_search:
                st.info("📚 Docs Only")
            else:
                st.warning("⚠️ None Selected")
        st.markdown('</div>', unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Welcome message if no chat history
    if len(st.session_state.messages) == 0:
        with st.chat_message("assistant"):
            st.markdown("👋 **Welcome!** I'm your research assistant. I can help you find information using web search and document search. What would you like to research today?")

    # Chat history display
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)

    # Fixed chat input at bottom (Claude-style)
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    if prompt := st.chat_input("What can I help you research from your honeydew list today?", key="chat_input"):
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
                                "type": "function",
                                "function": {
                                    "name": "search_documents",
                                    "description": "Search through the private document collection to find relevant information",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "query": {
                                                "type": "string",
                                                "description": "The search query to find relevant documents"
                                            }
                                        },
                                        "required": ["query"]
                                    }
                                }
                            })
                        
                        if use_web_search:
                            tools.append({
                                "type": "function",
                                "function": {
                                    "name": "search_web",
                                    "description": "Search the internet for current information",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "query": {
                                                "type": "string",
                                                "description": "The search query to find information on the web"
                                            }
                                        },
                                        "required": ["query"]
                                    }
                                }
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
                        
                        # Check if the model wants to call functions
                        message = response.choices[0].message
                        
                        if message.tool_calls:
                            # Handle function calls
                            messages_for_api.append(message)
                            
                            for tool_call in message.tool_calls:
                                function_name = tool_call.function.name
                                function_args = json.loads(tool_call.function.arguments)
                                
                                # Execute the function
                                if function_name == "search_documents":
                                    function_result = f"📚 Document search results for '{function_args['query']}':\n\n" + \
                                                    f"• **Sample Document 1**: Relevant information about {function_args['query']} found in your private collection.\n" + \
                                                    f"• **Sample Document 2**: Additional context about {function_args['query']} from your knowledge base.\n" + \
                                                    f"• **Sample Document 3**: Related findings on {function_args['query']} from archived materials.\n\n" + \
                                                    f"*Note: This is a demo - actual document search would query your real vector store with ID: {VECTOR_STORE_ID}*"
                                elif function_name == "search_web":
                                    function_result = f"🌐 Web search results for '{function_args['query']}':\n\n" + \
                                                    f"• **Current Information**: Latest findings on {function_args['query']} from reputable sources.\n" + \
                                                    f"• **Recent Updates**: New developments related to {function_args['query']} as of {datetime.now().strftime('%B %Y')}.\n" + \
                                                    f"• **Expert Analysis**: Professional insights about {function_args['query']} from industry leaders.\n\n" + \
                                                    f"*Note: This is a demo - actual web search would use real-time internet data.*"
                                else:
                                    function_result = f"Function {function_name} executed successfully."
                                
                                # Add function result to messages
                                messages_for_api.append({
                                    "tool_call_id": tool_call.id,
                                    "role": "tool",
                                    "name": function_name,
                                    "content": function_result
                                })
                            
                            # Make second API call to get final response
                            second_response = client.chat.completions.create(
                                model="gpt-4o",
                                messages=messages_for_api,
                                max_completion_tokens=1500,
                                temperature=0.7
                            )
                            
                            assistant_message = second_response.choices[0].message.content
                        else:
                            assistant_message = message.content
                        
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

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat controls in sidebar
    with st.sidebar:
        st.markdown("### 💬 Chat Controls")
        if st.session_state.messages:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
        
        st.markdown("### ℹ️ About")
        st.info("This is The 'Yes Dear' Assistant built for Week 2 of the AI Agent Bootcamp - your helpful companion for tackling that honeydew list!")
        
        # Show couple image in sidebar
        st.image("couple.png", caption="The 'Yes Dear' Assistant")
        
        st.markdown("---")
        st.markdown("**Built with:**")
        st.markdown("• Streamlit")
        st.markdown("• OpenAI GPT-4o")
        st.markdown("• Function Calling")

except Exception as e:
    st.error(f"❌ Error initializing OpenAI client: {str(e)}")
    st.info("Please check your API key in the .env file")

# Close main content div
st.markdown('</div>', unsafe_allow_html=True)