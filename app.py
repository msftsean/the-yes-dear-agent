import streamlit as st
import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(override=True)

# Check for OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Real API Configuration
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT", "us-east-1-aws")

# Define placeholder vector store ID
VECTOR_STORE_ID = "vs_placeholder_id_12345"

# System prompts (kept as short physical lines to satisfy linters)
SYSTEM_MESSAGE_SEARCH = (
    "You are a research assistant with access to search tools. You MUST use the "
    "available search tools before answering questions.\n\n"
    "CRITICAL: When users ask about specific information (policies, procedures, "
    "documentation, etc.), you MUST use the search_documents function to look for "
    "relevant information in the document collection.\n\n"
    "TOOL USAGE RULES:\n"
    "- For questions about company policies, procedures, documentation: USE search_documents FIRST\n"
    "- For current events, recent information, general web queries: USE search_web FIRST\n"
    "- When user explicitly asks to \"search documents\" or \"find in documents\": ALWAYS use search_documents\n"
    "- When user explicitly asks to \"search web\" or \"look online\": ALWAYS use search_web\n\n"
    "TASK: Always search first, then provide well-cited responses based on search results.\n\n"
    "OUTPUT: Clear, well-formatted answers using markdown. Always cite sources from search results.\n\n"
    "CONSTRAINTS: Never answer from general knowledge when search tools are available. "
    "Always search first, then respond based on findings."
)

SYSTEM_MESSAGE_DEFAULT = (
    "You are a helpful research assistant. Provide clear, accurate, and informative responses to user questions.\n\n"
    "TASK: Answer questions directly using your knowledge base. Provide comprehensive, well-structured responses.\n\n"
    "OUTPUT: Clear, well-formatted answers using markdown. Be thorough and educational in your explanations.\n\n"
    "CONSTRAINTS: If you're not certain about something, acknowledge the uncertainty. "
    "Focus on being helpful and informative."
)

# Real API Integration Functions



def real_web_search(query, max_results=5):
    """Real Google Custom Search API integration"""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return "⚠️ Google API keys not configured. Using mock data."

    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CSE_ID,
            'q': query,
            'num': max_results
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for item in data.get('items', []):
            results.append({
                'title': item.get('title', ''),
                'snippet': item.get('snippet', ''),
                'link': item.get('link', '')
            })

        # Format results for display
        formatted_results = f"🌐 **Real web search results for '{query}':**\n\n"
        for i, result in enumerate(results, 1):
            formatted_results += f"**{i}. {result['title']}**\n"
            formatted_results += f"{result['snippet']}\n"
            formatted_results += f"*Source: {result['link']}*\n\n"

        return formatted_results

    except Exception as e:
        return f"⚠️ Real web search failed: {str(e)}. Using mock data."


def real_document_search(query: str, max_results: int = 5) -> str:
    """Query a Pinecone index for the given query and format results.

    This function guards the Pinecone import and returns a helpful message
    if Pinecone isn't installed or the API key/index isn't configured.
    """
    if not PINECONE_API_KEY:
        return "⚠️ Pinecone API key not configured. Using mock data."

    try:
        try:
            from pinecone import Pinecone  # type: ignore
        except Exception:  # pragma: no cover - optional dependency
            return "⚠️ Pinecone package not installed. Run: pip install pinecone-client"

        pc = Pinecone(api_key=PINECONE_API_KEY)
        index_name = "documents"

        if index_name not in [idx.name for idx in pc.list_indexes()]:
            return (
                f"⚠️ Pinecone index '{index_name}' not found. "
                "Please create an index named '{index_name}' in your Pinecone console."
            )

        index = pc.Index(index_name)

        client = OpenAI(api_key=OPENAI_API_KEY)
        emb_resp = client.embeddings.create(input=query, model="text-embedding-ada-002")
        query_embedding = emb_resp.data[0].embedding

        search_results = index.query(vector=query_embedding, top_k=max_results, include_metadata=True)

        if not getattr(search_results, "matches", None):
            return f"📚 No documents found for '{query}'"

        lines = [f"📚 Document search results for '{query}':"]
        for i, match in enumerate(search_results.matches, 1):
            title = match.metadata.get("title", f"Document {i}")
            content = match.metadata.get("content", "No content available")
            score = getattr(match, "score", None)
            score_str = f"{score:.3f}" if score is not None else "n/a"
            lines.append(f"{i}. {title} (Score: {score_str})")
            lines.append(content[:200] + ("..." if len(content) > 200 else ""))
            lines.append("")

        return "\n".join(lines)
    except Exception as exc:  # pragma: no cover - runtime errors
        return f"⚠️ Real document search failed: {exc}. Using mock data."


def get_mock_web_search(query):
    """Enhanced mock web search for reliable demos"""
    month_year = datetime.now().strftime('%B %Y')
    parts = [
        "🌐 **Web search results for '" + query + "':**\n\n",
        "• **Current Information**: Latest findings on " + query + " from reputable sources.\n",
        "• **Recent Updates**: New developments related to " + query + " as of " + month_year + ".\n",
        "• **Expert Analysis**: Professional insights about " + query + " from industry leaders.\n\n",
        "*Note: This is enhanced mock data for demonstration purposes.*",
    ]
    return "".join(parts)


def get_mock_document_search(query):
    """Enhanced mock document search for reliable demos"""
    parts = [
        "📚 **Document search results for '" + query + "':**\n\n",
        "• **Sample Document 1**: Relevant information about " + query + " found in your private collection.\n",
        "• **Sample Document 2**: Additional context about " + query + " from your knowledge base.\n",
        "• **Sample Document 3**: Related findings on " + query + " from archived materials.\n\n",
        "*Note: This is enhanced mock data - actual search would query vector store ID: " + VECTOR_STORE_ID + "*",
    ]
    return "".join(parts)

# Streamlit UI


st.set_page_config(
    page_title="The 'Yes Dear' Assistant",
    page_icon="🔍",
    layout="centered"
)

# Add CSS for Claude-like interface
try:
    css_path = os.path.join("assets", "css", "app_styles.css")
    with open(css_path, "r", encoding="utf-8") as _css_file:
        css_text = _css_file.read()
    st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)
except Exception:
    # If the CSS file is missing, fall back to minimal inline styles
    st.markdown("<style>.stApp{background-color:#f8f9fa;}</style>", unsafe_allow_html=True)

# Main container with proper spacing
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Header section (loaded from template to reduce in-file line length)
try:
    header_path = os.path.join("assets", "templates", "header.html")
    with open(header_path, "r", encoding="utf-8") as _h:
        header_html = _h.read()
    st.markdown(header_html, unsafe_allow_html=True)
except Exception:
    # Fallback to a short header if file missing
    st.markdown("<div class='main-header'><h1>🔍 The 'Yes Dear' Assistant</h1></div>", unsafe_allow_html=True)

# Check if API key is available
if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY not found in environment variables!")
    st.info("Please add your OpenAI API key to your .env file")
    st.stop()

# Initialize OpenAI client
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    # Load template files to keep long strings out of this file
    def _load_template(name: str, **kwargs) -> str:
        try:
            path = os.path.join("assets", "templates", name)
            with open(path, "r", encoding="utf-8") as _t:
                content = _t.read()
            if kwargs:
                return content.format(**kwargs)
            return content
        except Exception:
            return ""

    # Tool selection in a nice container
    with st.container():
        st.markdown('<div class="tool-selection">', unsafe_allow_html=True)
        st.markdown("**🔧 Research Tools & Model Selection**")

        # First row: Model selection
        col_model1, col_model2, col_model_status = st.columns([1, 1, 1])
        with col_model1:
            selected_model = st.selectbox(
                "🤖 AI Model",
                ["gpt-5", "gpt-4o"],
                index=1,  # Default to GPT-4o
                help="Choose your AI model: GPT-5 (experimental) or GPT-4o (reliable)"
            )

        with col_model2:
            st.markdown("**Selected Model:**")
            if selected_model == "gpt-5":
                st.success("🚀 GPT-5 (Latest)")
            else:
                st.info("⚡ GPT-4o (Fast)")

        with col_model_status:
            st.markdown("**Status:**")
            st.success("✅ Ready")

        st.markdown("---")

        # API Integration Mode
        col_api1, col_api2, col_api_status = st.columns([1, 1, 1])
        with col_api1:
            use_real_apis = st.checkbox(
                "🔴 Real APIs",
                value=False,
                help="Toggle between mock (demo-safe) and real API integrations"
            )

        with col_api2:
            if use_real_apis:
                st.warning("🔴 **Live Mode**")
            else:
                st.success("🟢 **Demo Mode**")

        with col_api_status:
            if use_real_apis:
                # Show API status
                api_ready = bool(GOOGLE_API_KEY and GOOGLE_CSE_ID)
                if api_ready:
                    st.success("✅ APIs Ready")
                else:
                    st.error("❌ APIs Missing")
            else:
                st.success("✅ Mock Ready")

        st.markdown("---")

        # Second row: Search tools
        col_web, col_doc, col_status = st.columns([1, 1, 1])

        with col_web:
            use_web_search = st.checkbox(
                "🌐 Web Search",
                value=True,
                help="Search the internet for real-time information",
            )

        with col_doc:
            use_doc_search = st.checkbox(
                "📚 Document Search",
                value=True,
                help="Search your private document collection",
            )

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
            welcome_msg = (
                "👋 **Welcome!** I'm your research assistant powered by GPT-4o. "
                "I can help you find information using web search and document search. "
                "You can also switch between GPT-4o and GPT-5 models above. What would you like to research today?"
            )
            st.markdown(welcome_msg)

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
                # Create placeholder for chain of thought (stays visible)
                thinking_placeholder = st.empty()

                # Create placeholder for loading message that will be replaced
                response_placeholder = st.empty()

                with response_placeholder:
                    st.markdown("🔍 **Processing your request...** Please wait while I research your question.")

                # Show initial thinking process immediately
                with thinking_placeholder:
                    with st.expander("🤔 Agent Thinking Process", expanded=True):
                        thinking_steps = st.empty()
                        thinking_steps.markdown("🤔 **Starting analysis of your question...**")

                with st.spinner("Researching your question..."):
                    try:
                        # Update thinking process
                        thinking_steps.markdown("🤔 **Starting analysis...**\n\n🔍 **Preparing search tools...**")

                        # Prepare tools based on user selection
                        tools = []

                        if use_doc_search:
                            thinking_steps.markdown(
                                "🤔 **Starting analysis...**\n\n"
                                "🔍 **Preparing search tools...**\n\n"
                                "📁 **Document search enabled"
                            )
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
                            if use_doc_search:
                                thinking_steps.markdown(
                                    "🤔 **Starting analysis...**\n\n"
                                    "🔍 **Preparing search tools...**\n\n"
                                    "📁 **Document search enabled**\n\n"
                                    "🌐 **Web search enabled**"
                                )
                            else:
                                thinking_steps.markdown(
                                    "🤔 **Starting analysis...**\n\n"
                                    "🔍 **Preparing search tools...**\n\n"
                                    "🌐 **Web search enabled**"
                                )
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
                        if tools:
                            system_message = {"role": "system", "content": SYSTEM_MESSAGE_SEARCH}
                        else:
                            system_message = {"role": "system", "content": SYSTEM_MESSAGE_DEFAULT}

                        # Build complete message history
                        messages_for_api = [system_message] + st.session_state.messages

                        # Prepare API parameters
                        api_params = {
                            "model": selected_model,
                            "messages": messages_for_api,
                            "max_completion_tokens": 1500
                        }

                        # Only add temperature for models that support it (not GPT-5)
                        if selected_model != "gpt-5":
                            api_params["temperature"] = 0.7

                        # Add tools if any are selected
                        if tools:
                            api_params["tools"] = tools

                        # Update thinking - making API call
                        tool_text = ("\n\n📁 **Document search enabled**" if use_doc_search else "")
                        tool_text += ("\n\n🌐 **Web search enabled**" if use_web_search else "")
                        thinking_msg = (
                            "🤔 **Starting analysis...**\n\n"
                            "🔍 **Preparing search tools...**"
                            f"{tool_text}\n\n"
                            f"🤖 **Connecting to AI model ({selected_model})...**"
                        )
                        thinking_steps.markdown(thinking_msg)

                        # Make API call
                        response = client.chat.completions.create(**api_params)

                        # Update thinking - analyzing response
                        thinking_msg2 = (
                            "🤔 **Starting analysis...**\n\n"
                            "🔍 **Preparing search tools...**"
                            f"{tool_text}\n\n"
                            f"🤖 **Connected to {selected_model}**\n\n"
                            "💭 **Analyzing your question...**"
                        )
                        thinking_steps.markdown(thinking_msg2)

                        # Check if the model wants to call functions
                        message = response.choices[0].message

                        # Always check for chain of thought content first
                        chain_of_thought = getattr(message, 'content', None)
                        is_thinking = False

                        # Detect if this is thinking/reasoning vs final answer
                        if chain_of_thought and chain_of_thought.strip():
                            thinking_indicators = [
                                "i'm going to", "let me", "searching", "i'll", "checking",
                                "looking up", "fetching", "accessing", "querying", "attempting",
                                "initiating", "performing", "calling", "using", "proceeding"
                            ]
                            is_thinking = any(indicator in chain_of_thought.lower() for indicator in thinking_indicators)

                            # Also check length - very long responses are usually thinking
                            if len(chain_of_thought) > 800:
                                is_thinking = True

                        # Initialize thinking display
                        thinking_content = []

                        # Capture initial reasoning if present
                        if chain_of_thought and chain_of_thought.strip():
                            thinking_content.append(f"**Initial reasoning:**\n{chain_of_thought}")

                        if message.tool_calls:

                            # Handle function calls
                            messages_for_api.append(message)

                            # Show real-time tool execution
                            for i, tool_call in enumerate(message.tool_calls):
                                function_name = tool_call.function.name
                                function_args = json.loads(tool_call.function.arguments)

                                # Update thinking display in real-time
                                query = function_args.get('query', 'N/A')
                                tool_icon = "📁" if function_name == "search_documents" else "🌐"
                                exec_msg = (
                                    "🤔 **Starting analysis...**\n\n"
                                    "🔍 **Search tools prepared**"
                                    f"{tool_text}\n\n"
                                    f"🤖 **Connected to {selected_model}**\n\n"
                                    "💭 **Question analyzed**\n\n"
                                    f"{tool_icon} **Executing {function_name}**\n\n"
                                    f"🔎 Query: \"*{query}*\""
                                )
                                thinking_steps.markdown(exec_msg)

                                # Add tool activity to thinking content for later display
                                thinking_content.append(f"**Tool {i+1}: {function_name}**\nQuery: {query}")

                                # Execute the function with hybrid system
                                if function_name == "search_documents":
                                    if use_real_apis:
                                        function_result = real_document_search(function_args['query'])
                                    else:
                                        function_result = get_mock_document_search(function_args['query'])
                                elif function_name == "search_web":
                                    if use_real_apis:
                                        function_result = real_web_search(function_args['query'])
                                    else:
                                        function_result = get_mock_web_search(function_args['query'])
                                else:
                                    function_result = f"Function {function_name} executed successfully."

                                # Add function result to messages
                                messages_for_api.append({
                                    "tool_call_id": tool_call.id,
                                    "role": "tool",
                                    "name": function_name,
                                    "content": function_result
                                })

                            # Update thinking - synthesizing response
                                finish_search_msg = (
                                    "🤔 **Starting analysis...**\n\n"
                                    "🔍 **Search completed**"
                                    f"{tool_text}\n\n"
                                    f"🤖 **Connected to {selected_model}**\n\n"
                                    "💭 **Question analyzed**\n\n"
                                    "✅ **Search results obtained**\n\n"
                                    "🧠 **Synthesizing final response..."
                                )
                                thinking_steps.markdown(finish_search_msg)

                            # Make second API call to get final response
                            second_api_params = {
                                "model": selected_model,
                                "messages": messages_for_api,
                                "max_completion_tokens": 1500
                            }

                            # Only add temperature for models that support it (not GPT-5)
                            if selected_model != "gpt-5":
                                second_api_params["temperature"] = 0.7

                            second_response = client.chat.completions.create(**second_api_params)

                            assistant_message = second_response.choices[0].message.content

                            # Capture any reasoning from the second response for thinking display
                            second_message_content = getattr(second_response.choices[0].message, 'content', '')
                            if second_message_content and len(second_message_content) > 200:
                                # Check if this looks like thinking
                                thinking_indicators = ["i'm going to", "let me", "searching", "i'll", "checking", "looking up"]
                                if any(indicator in second_message_content.lower() for indicator in thinking_indicators):
                                    thinking_content.append(f"**Agent reasoning:**\n{second_message_content}")

                            # Finalize thinking display - mark as complete using template
                            complete_template = _load_template("thinking_complete.md", model=selected_model)
                            if complete_template:
                                thinking_steps.markdown(complete_template)
                            else:
                                thinking_steps.markdown(
                                    "🤔 **Analysis Complete!**\n\n"
                                    "🔍 **Search completed**\n\n"
                                    f"🤖 **Used {selected_model}**\n\n"
                                    "✅ **Search results obtained**\n\n"
                                    "🧠 **Response synthesized**\n\n"
                                    "✨ **Ready to respond!**"
                                )

                            # GPT-5 tool response fallback - if content is empty after tool calls, try GPT-4o
                            if (not assistant_message or assistant_message.strip() == "") and selected_model == "gpt-5":
                                # Create simplified messages for GPT-4o including tool results
                                fallback_messages = [
                                    {"role": "system", "content": "You are a helpful research assistant. Based on the search results provided, give a comprehensive answer to the user's question. Cite your sources and provide clear, well-formatted information."},
                                    {"role": "user", "content": st.session_state.messages[-1]["content"]}
                                ]

                                # Add tool results as context for GPT-4o
                                tool_context = []
                                for msg in messages_for_api:
                                    # Handle both dict messages and ChatCompletionMessage objects
                                    role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", None)
                                    if role == "tool":
                                        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")
                                        tool_context.append(f"Search Results: {content}")

                                if tool_context:
                                    fallback_messages.append({
                                        "role": "user",
                                        "content": f"Based on these search results:\n\n{chr(10).join(tool_context)}\n\nPlease provide a comprehensive answer to my question."
                                    })

                                fallback_response = client.chat.completions.create(
                                    model="gpt-4o",
                                    messages=fallback_messages,
                                    max_completion_tokens=1500,
                                    temperature=0.7
                                )

                                assistant_message = fallback_response.choices[0].message.content
                                if assistant_message:
                                    assistant_message = f"*[Response generated using GPT-4o due to GPT-5 tool response issue]*\n\n{assistant_message}"
                                else:
                                    # Final fallback - create response from tool results
                                    if tool_context:
                                        assistant_message = f"Based on my search, here's what I found:\n\n{chr(10).join(tool_context)}\n\n*Note: This is a summary of search results. For more detailed information, please try asking a more specific question.*"
                                    else:
                                        assistant_message = "I searched for information but encountered an issue generating the response. Please try rephrasing your question or switch to GPT-4o model."

                            # Show error in thinking display
                            if not assistant_message and (use_doc_search or use_web_search):
                                analysis_issue_template = _load_template("analysis_issue.md")
                                if analysis_issue_template:
                                    thinking_steps.markdown(analysis_issue_template)
                                else:
                                    thinking_steps.markdown(
                                        "🤔 **Analysis Issues**\n\n"
                                        "🔍 **Search tools prepared**"
                                        f"{tool_text}\n\n"
                                        "⚠️ **Model compatibility issue detected**\n\n"
                                        "🔄 **Attempting recovery...**"
                                    )
                                assistant_message = "I attempted to search for information about your question, but encountered an issue. Please try switching to the GPT-4o model or rephrase your question."
                        else:
                            # Extract content from message
                            assistant_message = getattr(message, 'content', None)

                            # If this looks like thinking, show it in the live display
                            if is_thinking and assistant_message:
                                agent_reasoning_msg = (
                                    "🤔 **Agent's Reasoning:**\n\n"
                                    f"{assistant_message}"
                                )
                                thinking_steps.markdown(agent_reasoning_msg)

                                # Generate a proper response since this was just thinking
                                try:
                                    proper_response = client.chat.completions.create(
                                        model="gpt-4o",  # Use GPT-4o for reliable responses
                                        messages=[
                                            {"role": "system", "content": "You are a helpful assistant. Provide a clear, direct answer to the user's question. Be concise and informative."},
                                            {"role": "user", "content": st.session_state.messages[-1]["content"]}
                                        ],
                                        max_completion_tokens=800,
                                        temperature=0.7
                                    )
                                    assistant_message = proper_response.choices[0].message.content
                                    if assistant_message:
                                        assistant_message = f"*[Thinking process shown above, response generated using GPT-4o]*\n\n{assistant_message}"
                                except Exception:
                                    assistant_message = (
                                        "I've been thinking about your question (see above), but I'm having trouble "
                                        "generating a proper response. Please try rephrasing your question."
                                    )

                            # GPT-5 fallback - if content is empty, try a simplified prompt
                            if not assistant_message and selected_model == "gpt-5":
                                fallback_messages = [
                                    {"role": "system", "content": "You are a helpful assistant. Provide a clear and informative response."},
                                    {"role": "user", "content": st.session_state.messages[-1]["content"]}
                                ]

                                fallback_response = client.chat.completions.create(
                                    model="gpt-4o",  # Use GPT-4o as fallback
                                    messages=fallback_messages,
                                    max_completion_tokens=1500,
                                    temperature=0.7
                                )

                                assistant_message = fallback_response.choices[0].message.content
                                if assistant_message:
                                    assistant_message = f"*[Answered using GPT-4o fallback due to GPT-5 response issue]*\n\n{assistant_message}"

                        # Display response - clear loading message and show actual response
                        if assistant_message and assistant_message.strip():
                            response_placeholder.markdown(assistant_message)

                            # Add assistant response to chat history
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": assistant_message
                            })

                            # Show token usage
                            if hasattr(response, 'usage'):
                                with st.expander("📊 Usage Stats"):
                                    st.write(f"**Model:** {selected_model}")
                                    st.write(f"**Prompt tokens:** {response.usage.prompt_tokens}")
                                    st.write(f"**Completion tokens:** {response.usage.completion_tokens}")
                                    st.write(f"**Total tokens:** {response.usage.total_tokens}")
                        else:
                            # Clear loading message and show debug information
                            response_placeholder.empty()
                            st.error("❌ No response generated. Please try again.")
                            st.write("**Debug Info:**")
                            st.write(f"- Model: {selected_model}")
                            st.write(f"- Message content: {repr(message.content) if hasattr(message, 'content') else 'No content'}")
                            st.write(f"- Tool calls: {bool(getattr(message, 'tool_calls', None))}")
                            st.write(f"- Assistant message: {repr(assistant_message)}")
                            if hasattr(response, 'usage'):
                                st.write(f"- Tokens used: {response.usage.total_tokens}")

                            # Plain English analysis
                            st.markdown("---")
                            st.write("**🔍 What This Means:**")

                            tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
                            has_tools = bool(getattr(message, 'tool_calls', None))
                            has_content = bool(message.content if hasattr(message, 'content') else False)

                            if tokens_used > 0 and not has_content and not has_tools:
                                st.warning("The AI model processed your question (used tokens) but returned an empty response. This usually means there's a problem with the system prompt or model configuration.")
                            elif has_tools and not has_content:
                                st.info("The model tried to use search tools but didn't provide a final response. This might be a tool integration issue.")
                            elif tokens_used == 0:
                                st.error("No tokens were used, which means the API call failed completely. Check your internet connection and API key.")
                            else:
                                st.info("The response appears to be empty for an unknown reason. Try switching models or clearing your chat history.")

                    except Exception as e:
                        # Update thinking display with error (template-based)
                        interrupted_template = _load_template("analysis_interrupted.md", error=str(e))
                        if interrupted_template:
                            thinking_steps.markdown(interrupted_template)
                        else:
                            thinking_steps.markdown(f"🤔 **Analysis Interrupted**\n\n❌ **Error encountered:** {str(e)}\n\n🔄 **Please try again**")

                        # Clear loading message and show error
                        response_placeholder.empty()
                        error_message = f"❌ Error: {str(e)}"
                        st.error(error_message)

                        # Simple error analysis
                        st.markdown("---")
                        st.write("**🔍 What This Means:**")

                        error_str = str(e).lower()
                        if "api key" in error_str or "unauthorized" in error_str:
                            st.warning("There's an issue with your OpenAI API key. Please check that it's set correctly in your environment variables.")
                        elif "rate limit" in error_str or "quota" in error_str:
                            st.warning("You've hit the API rate limit or quota. Please wait a moment and try again, or check your OpenAI account usage.")
                        elif "network" in error_str or "connection" in error_str or "timeout" in error_str:
                            st.warning("There's a network connectivity issue. Please check your internet connection and try again.")
                        elif "chatcompletionmessage" in error_str or "attribute" in error_str:
                            st.warning("There's a compatibility issue with the AI model response format. Try switching to GPT-4o or refresh the page.")
                        else:
                            st.info("An unexpected error occurred. Try refreshing the page, switching models, or clearing your chat history.")

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
        st.image("assets/images/couple.png", caption="The 'Yes Dear' Assistant")

        st.markdown("---")
        st.markdown("**Built with:**")
        st.markdown("• Streamlit")
        st.markdown(f"• OpenAI {selected_model.upper()}")
        st.markdown("• Google Search API")
        st.markdown("• Pinecone Vector DB")
        st.markdown("• Function Calling")

except Exception as e:
    st.error(f"❌ Error initializing OpenAI client: {str(e)}")
    st.info("Please check your API key in the .env file")

# Close main content div
st.markdown('</div>', unsafe_allow_html=True)
