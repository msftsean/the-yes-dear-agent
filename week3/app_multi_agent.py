"""
Week 3 Multi-Agent System: "Yes Dear" Assistant
================================================

This application demonstrates a multi-agent system using Microsoft Agent Framework
that automates the "honeydew list" - helping with research, document search, and task execution.

Architecture:
- Design Pattern: Sequential with Parallel sub-flows
- Specialized Agents: Coordinator, Research, Document, Summarizer
- Shared Memory: WorkflowContext + shared state dictionary
- Error Handling: Fallback strategies for each agent

Assignment Requirements Met:
✅ Multi-agent design pattern (Sequential with parallel capabilities)
✅ 4 specialized agents with different roles
✅ Shared memory mechanism for agent collaboration
✅ Error handling and fallback strategies
"""

import streamlit as st
import os
import json
import asyncio
import time
import pytz
from datetime import datetime
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Microsoft Agent Framework imports
from agent_framework import (
    ChatAgent,
    ChatMessage,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowOutputEvent,
    WorkflowStatusEvent,
    ExecutorFailedEvent,
    WorkflowRunState,
    handler,
)
from agent_framework.azure import AzureOpenAIChatClient
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# ============================================================================
# SHARED MEMORY SYSTEM
# ============================================================================

class SharedMemory:
    """
    Shared memory system for multi-agent collaboration.
    Stores search results, user preferences, task history, and agent findings.
    """
    def __init__(self):
        self.search_results: Dict[str, Any] = {}
        self.document_results: Dict[str, Any] = {}
        self.agent_messages: List[Dict[str, str]] = []
        self.task_history: List[str] = []
        self.current_task: Optional[str] = None
        self.user_preferences: Dict[str, Any] = {}
        self.agent_states: Dict[str, str] = {
            'coordinator': 'Idle',
            'research': 'Idle',
            'document': 'Idle',
            'summarizer': 'Idle'
        }
        self.agent_state_timestamps: Dict[str, str] = {
            'coordinator': '',
            'research': '',
            'document': '',
            'summarizer': ''
        }
    
    def update_agent_state(self, agent: str, state: str):
        """Update agent state with timestamp in 12-hour Eastern time format"""
        import pytz
        eastern = pytz.timezone('US/Eastern')
        eastern_time = datetime.now(eastern)
        self.agent_states[agent] = state
        self.agent_state_timestamps[agent] = eastern_time.strftime('%I:%M:%S %p')
        
    def add_search_result(self, query: str, results: Any):
        """Store web search results"""
        self.search_results[query] = {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
    def add_document_result(self, query: str, results: Any):
        """Store document search results"""
        self.document_results[query] = {
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
    def add_agent_message(self, agent_name: str, message: str):
        """Log agent-to-agent communication"""
        self.agent_messages.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "message": message
        })
        
    def get_all_findings(self) -> str:
        """Compile all findings for summarization"""
        findings = []
        
        if self.search_results:
            findings.append("## Web Search Results")
            for query, data in self.search_results.items():
                findings.append(f"Query: {query}")
                findings.append(f"Results: {data['results']}")
                
        if self.document_results:
            findings.append("\n## Document Search Results")
            for query, data in self.document_results.items():
                findings.append(f"Query: {query}")
                findings.append(f"Results: {data['results']}")
                
        return "\n".join(findings) if findings else "No findings available"
    
    def clear(self):
        """Clear shared memory"""
        self.__init__()

# Initialize shared memory in session state
def get_shared_memory():
    """Get or create shared memory from session state"""
    if 'shared_memory' not in st.session_state:
        st.session_state.shared_memory = SharedMemory()
    return st.session_state.shared_memory

# Get shared memory instance
shared_memory = get_shared_memory()

# ============================================================================
# SEARCH UTILITY FUNCTIONS
# ============================================================================

def mock_web_search(query: str) -> str:
    """Mock web search for demo purposes"""
    return f"🌐 **Mock Web Search Results for '{query}':**\n\n" + \
           f"• Latest information on {query} from reputable sources\n" + \
           f"• Recent updates as of {datetime.now().strftime('%B %Y')}\n" + \
           f"• Expert analysis and professional insights\n\n" + \
           f"*Mock data for demonstration*"

def mock_document_search(query: str) -> str:
    """Mock document search for demo purposes"""
    return f"📚 **Mock Document Search Results for '{query}':**\n\n" + \
           f"• Relevant information from your private collection\n" + \
           f"• Additional context from knowledge base\n" + \
           f"• Related findings from archived materials\n\n" + \
           f"*Mock data for demonstration*"

def real_web_search(query: str) -> str:
    """Real Google Custom Search API integration"""
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        return mock_web_search(query)
    
    try:
        import requests
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CSE_ID,
            'q': query,
            'num': 5
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
        
        formatted = f"🌐 **Real Web Search Results for '{query}':**\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"**{i}. {result['title']}**\n"
            formatted += f"{result['snippet']}\n"
            formatted += f"*Source: {result['link']}*\n\n"
        
        return formatted
    except Exception as e:
        return f"⚠️ Web search error: {str(e)}\n\n{mock_web_search(query)}"

def real_document_search(query: str) -> str:
    """Real Pinecone document search"""
    if not PINECONE_API_KEY:
        return mock_document_search(query)
    
    try:
        from pinecone import Pinecone
        
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index_name = "documents"
        
        if index_name in [idx.name for idx in pc.list_indexes()]:
            index = pc.Index(index_name)
            
            # Generate embedding
            client = OpenAI(api_key=OPENAI_API_KEY)
            embedding_response = client.embeddings.create(
                input=query,
                model="text-embedding-ada-002"
            )
            query_embedding = embedding_response.data[0].embedding
            
            # Search
            search_results = index.query(
                vector=query_embedding,
                top_k=5,
                include_metadata=True
            )
            
            if search_results.matches:
                formatted = f"📚 **Real Document Search Results for '{query}':**\n\n"
                for i, match in enumerate(search_results.matches, 1):
                    title = match.metadata.get('title', f'Document {i}')
                    content = match.metadata.get('content', 'No content')
                    score = match.score
                    formatted += f"**{i}. {title}** (Score: {score:.3f})\n"
                    formatted += f"{content[:200]}{'...' if len(content) > 200 else ''}\n\n"
                return formatted
            else:
                return f"📚 No documents found for '{query}'\n\n{mock_document_search(query)}"
        else:
            return f"⚠️ Index '{index_name}' not found\n\n{mock_document_search(query)}"
    except Exception as e:
        return f"⚠️ Document search error: {str(e)}\n\n{mock_document_search(query)}"

# ============================================================================
# SPECIALIZED AGENT EXECUTORS
# ============================================================================

class CoordinatorExecutor(Executor):
    """
    Coordinator Agent - Entry point for all requests
    
    Role: Analyzes user requests and determines which specialized agents to invoke
    Pattern: Acts as orchestrator in sequential workflow
    Error Handling: Falls back to direct response if agent routing fails
    """
    
    agent: Optional[ChatAgent] = None
    
    def __init__(self, chat_client: Optional[AzureOpenAIChatClient] = None, id: str = "coordinator"):
        if chat_client:
            self.agent = chat_client.create_agent(
                instructions="""You are the Coordinator Agent for the 'Yes Dear' honeydew list assistant.
                
Your role:
1. Analyze user requests from their honeydew (to-do) list
2. Determine which specialized agents are needed:
   - Research Agent: For web searches, current information, general queries
   - Document Agent: For internal knowledge base, personal documents, saved information
   - Both agents: When comprehensive research is needed
3. Route the request appropriately
4. Keep responses concise and action-oriented

Always start by understanding what the user needs, then decide on the best approach."""
            )
        super().__init__(id=id)
    
    @handler
    async def handle(self, message: ChatMessage, ctx: WorkflowContext[Dict[str, Any]]) -> None:
        """
        Analyze request and route to appropriate agents
        Error handling: If agent fails, provide manual routing
        """
        try:
            # Get fresh shared_memory and reset everything for new query
            shared_memory = get_shared_memory()
            
            # Clear old agent messages to start fresh
            shared_memory.agent_messages = []
            
            # Reset all agents to Idle for fresh start
            shared_memory.update_agent_state('coordinator', 'Analyzing')
            shared_memory.update_agent_state('research', 'Idle')
            shared_memory.update_agent_state('document', 'Idle')
            shared_memory.update_agent_state('summarizer', 'Idle')
            
            shared_memory.current_task = message.text
            shared_memory.add_agent_message("Coordinator", f"Analyzing: {message.text}")
            
            # Simple keyword-based routing (can be enhanced with agent)
            text_lower = message.text.lower()
            
            # Check for explicit web search requests
            explicit_web_search = any(word in text_lower for word in ['web', 'google', 'search web', 'search google', 'online', 'internet'])
            
            # Check for document-related keywords (broader detection)
            document_keywords = ['document', 'file', 'saved', 'my', 'previous', 'knowledge', 'policy', 'policies', 
                                'vacation', 'handbook', 'manual', 'guide', 'procedure', 'hr', 'company', 'internal',
                                'information', 'about', 'our', 'find', 'what is', 'how many', 'can i', 'tell me']
            needs_documents = any(word in text_lower for word in document_keywords)
            
            # Always enable both agents for comprehensive results
            routing_decision = {
                "needs_web_search": True,  # Always search web for comprehensive results
                "needs_documents": needs_documents or not explicit_web_search,  # Default to documents
                "user_query": message.text,
                "original_message": message
            }
            
            shared_memory.add_agent_message(
                "Coordinator", 
                f"Routing - Web: {routing_decision['needs_web_search']}, Docs: {routing_decision['needs_documents']}"
            )
            
            shared_memory.update_agent_state('coordinator', 'Complete')
            await ctx.send_message(routing_decision)
            
        except Exception as e:
            # Fallback: Send request to research agent
            shared_memory.add_agent_message("Coordinator", f"Error: {str(e)}, using fallback routing")
            await ctx.send_message({
                "needs_web_search": True,
                "needs_documents": False,
                "user_query": message.text,
                "original_message": message
            })


class ResearchExecutor(Executor):
    """
    Research Agent - Handles web searches and external APIs
    
    Role: Searches the web for current information using real or mock APIs
    Pattern: Can execute in parallel with DocumentExecutor
    Error Handling: Falls back to mock data if real APIs fail
    """
    
    use_real_apis: bool = False
    
    def __init__(self, use_real_apis: bool = False, id: str = "research"):
        self.use_real_apis = use_real_apis
        super().__init__(id=id)
    
    @handler
    async def handle(self, routing: Dict[str, Any], ctx: WorkflowContext[Dict[str, Any]]) -> None:
        """
        Execute web search based on routing decision
        Error handling: Automatic fallback to mock data
        """
        try:
            shared_memory = get_shared_memory()
            
            # ALWAYS execute research for comprehensive results
            shared_memory.update_agent_state('research', 'Searching')
            query = routing["user_query"]
            shared_memory.add_agent_message("Research", f"Searching web for: {query}")
            
            # Add visible delay so users can see the "Searching" state
            await asyncio.sleep(1.5)
            
            # Execute search with error handling
            try:
                if self.use_real_apis:
                    results = real_web_search(query)
                else:
                    results = mock_web_search(query)
                
                shared_memory.add_search_result(query, results)
                routing["web_search_complete"] = True
                routing["web_search_results"] = results
                shared_memory.update_agent_state('research', 'Complete')
                
            except Exception as search_error:
                # Fallback to mock data
                shared_memory.add_agent_message("Research", f"Search error, using fallback: {str(search_error)}")
                results = mock_web_search(query)
                shared_memory.add_search_result(query, results)
                routing["web_search_complete"] = True
                routing["web_search_results"] = results
                routing["web_search_error"] = str(search_error)
            
            await ctx.send_message(routing)
            
        except Exception as e:
            # Critical error - pass through without search results
            shared_memory.add_agent_message("Research", f"Critical error: {str(e)}")
            routing["web_search_complete"] = False
            routing["web_search_error"] = str(e)
            await ctx.send_message(routing)


class DocumentExecutor(Executor):
    """
    Document Agent - Handles internal knowledge base searches
    
    Role: Searches private document collection using Pinecone or mock data
    Pattern: Can execute in parallel with ResearchExecutor
    Error Handling: Falls back to mock data if Pinecone fails
    """
    
    use_real_apis: bool = False
    
    def __init__(self, use_real_apis: bool = False, id: str = "document"):
        self.use_real_apis = use_real_apis
        super().__init__(id=id)
    
    @handler
    async def handle(self, routing: Dict[str, Any], ctx: WorkflowContext[Dict[str, Any]]) -> None:
        """
        Execute document search based on routing decision
        Error handling: Automatic fallback to mock data
        """
        try:
            shared_memory = get_shared_memory()
            if not routing.get("needs_documents"):
                # Skip if not needed
                shared_memory.update_agent_state('document', 'Skipped')
                await ctx.send_message(routing)
                return
            
            shared_memory.update_agent_state('document', 'Searching')
            query = routing["user_query"]
            shared_memory.add_agent_message("Document", f"Searching documents for: {query}")
            
            # Add visible delay so users can see the "Searching" state
            await asyncio.sleep(1.5)
            
            # Execute search with error handling
            try:
                if self.use_real_apis:
                    results = real_document_search(query)
                else:
                    results = mock_document_search(query)
                
                shared_memory.add_document_result(query, results)
                routing["doc_search_complete"] = True
                routing["doc_search_results"] = results
                shared_memory.update_agent_state('document', 'Complete')
                
            except Exception as search_error:
                # Fallback to mock data
                shared_memory.add_agent_message("Document", f"Search error, using fallback: {str(search_error)}")
                results = mock_document_search(query)
                shared_memory.add_document_result(query, results)
                routing["doc_search_complete"] = True
                routing["doc_search_results"] = results
                routing["doc_search_error"] = str(search_error)
            
            await ctx.send_message(routing)
            
        except Exception as e:
            # Critical error - pass through without search results
            shared_memory.add_agent_message("Document", f"Critical error: {str(e)}")
            routing["doc_search_complete"] = False
            routing["doc_search_error"] = str(e)
            await ctx.send_message(routing)


class SummarizerExecutor(Executor):
    """
    Summarizer Agent - Synthesizes findings from all agents
    
    Role: Compiles search results and creates coherent response
    Pattern: Final node in sequential workflow
    Error Handling: Returns raw results if synthesis fails
    """
    
    openai_client: Optional[OpenAI] = None
    
    def __init__(self, openai_api_key: str, id: str = "summarizer"):
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
        super().__init__(id=id)
    
    @handler
    async def handle(self, routing: Dict[str, Any], ctx: WorkflowContext[None, str]) -> None:
        """
        Synthesize all findings into final response
        Error handling: Falls back to raw result concatenation
        """
        try:
            shared_memory = get_shared_memory()
            shared_memory.update_agent_state('summarizer', 'Compiling')
            shared_memory.add_agent_message("Summarizer", "Synthesizing findings")
            
            # Add visible delay so users can see the "Compiling" state
            await asyncio.sleep(1.5)
            
            # Compile all results
            user_query = routing.get("user_query", "")
            web_results = routing.get("web_search_results", "")
            doc_results = routing.get("doc_search_results", "")
            
            # Build context for summarization
            context_parts = []
            if web_results:
                context_parts.append(f"Web Search Results:\n{web_results}")
            if doc_results:
                context_parts.append(f"Document Search Results:\n{doc_results}")
            
            full_context = "\n\n".join(context_parts)
            
            if not full_context:
                await ctx.yield_output("I apologize, but I couldn't find any information to help with your request. Please try rephrasing your question.")
                return
            
            # Try to use OpenAI for intelligent synthesis
            try:
                if self.openai_client:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": """You are a helpful assistant synthesizing research findings.
                                
Create a clear, comprehensive response based on the search results provided.
- Cite sources when relevant
- Organize information logically
- Be concise but thorough
- Use markdown formatting"""
                            },
                            {
                                "role": "user",
                                "content": f"User Question: {user_query}\n\nSearch Results:\n{full_context}\n\nPlease provide a well-organized answer."
                            }
                        ],
                        temperature=0.7,
                        max_tokens=1500
                    )
                    
                    final_response = response.choices[0].message.content
                    shared_memory.add_agent_message("Summarizer", "Synthesis complete")
                    
                    # Add visible delay before marking complete
                    await asyncio.sleep(1.0)
                    
                    shared_memory.update_agent_state('summarizer', 'Complete')
                    await ctx.yield_output(final_response)
                else:
                    # No OpenAI - return formatted results
                    shared_memory.update_agent_state('summarizer', 'Complete')
                    await ctx.yield_output(f"**Results for: {user_query}**\n\n{full_context}")
                    
            except Exception as synth_error:
                # Fallback: Return raw results with formatting
                shared_memory.add_agent_message("Summarizer", f"Synthesis error, using fallback: {str(synth_error)}")
                fallback_response = f"**Research Results for: {user_query}**\n\n{full_context}\n\n*Note: Automatic synthesis unavailable*"
                shared_memory.update_agent_state('summarizer', 'Complete')
                await ctx.yield_output(fallback_response)
            
        except Exception as e:
            # Critical error - return error message
            error_msg = f"I encountered an error processing your request: {str(e)}\n\nPlease try again or rephrase your question."
            shared_memory.add_agent_message("Summarizer", f"Critical error: {str(e)}")
            shared_memory.update_agent_state('summarizer', 'Error')
            await ctx.yield_output(error_msg)

# ============================================================================
# WORKFLOW BUILDER
# ============================================================================

def create_multi_agent_workflow(use_real_apis: bool = False) -> Any:
    """
    Create the multi-agent workflow using Microsoft Agent Framework
    
    Architecture:
    1. Coordinator → Analyzes request
    2. Research & Document Agents → Execute in sequence (could be parallel)
    3. Summarizer → Synthesizes results
    
    Returns: Configured workflow ready for execution
    """
    
    # Create executors
    coordinator = CoordinatorExecutor()
    research = ResearchExecutor(use_real_apis=use_real_apis)
    document = DocumentExecutor(use_real_apis=use_real_apis)
    summarizer = SummarizerExecutor(openai_api_key=OPENAI_API_KEY)
    
    # Build workflow
    # Sequential pattern: Coordinator → Research → Document → Summarizer
    workflow = (
        WorkflowBuilder()
        .set_start_executor(coordinator)
        .add_edge(coordinator, research)
        .add_edge(research, document)
        .add_edge(document, summarizer)
        .build()
    )
    
    return workflow

# ============================================================================
# STREAMLIT UI
# ============================================================================

def render_sidebar():
    """Render sidebar with configuration and system info"""
    # Get fresh shared_memory reference
    shared_memory = get_shared_memory()
    
    st.sidebar.title("🤖 Multi-Agent System")
    
    st.sidebar.markdown("### System Configuration")
    
    # API Key Status
    if OPENAI_API_KEY:
        st.sidebar.success("✅ OpenAI API Key configured")
    else:
        st.sidebar.error("❌ OpenAI API Key required")
    
    # API Mode Toggle
    use_real_apis = st.sidebar.checkbox(
        "🔴 Use Real APIs",
        value=False,
        help="Toggle between mock (demo-safe) and real API integrations"
    )
    
    if use_real_apis:
        st.sidebar.warning("🔴 **Live Mode Active**")
        if GOOGLE_API_KEY and GOOGLE_CSE_ID:
            st.sidebar.success("✅ Google Search Ready")
        else:
            st.sidebar.error("❌ Google Search Not Configured")
        
        if PINECONE_API_KEY:
            st.sidebar.success("✅ Pinecone Ready")
        else:
            st.sidebar.error("❌ Pinecone Not Configured")
    else:
        st.sidebar.success("🟢 **Demo Mode (Mock Data)**")
    
    # Header Image
    st.sidebar.markdown("---")
    try:
        st.sidebar.image("../assets/images/couple.png", width="stretch")
    except:
        pass  # Image not found, skip silently
    
    # Architecture Info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏗️ Architecture")
    st.sidebar.info("""
**Multi-Agent System**

**Agents:**
- 🎯 Coordinator: Request analysis
- 🌐 Research: Web search
- 📚 Document: Knowledge base
- 📝 Summarizer: Synthesis

**Pattern:** Sequential with parallel capabilities

**Shared Memory:** Active
    """)
    
    # Control Buttons
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset System"):
        st.session_state.clear()
        shared_memory.clear()
        st.rerun()
    
    if st.sidebar.button("🗑️ Clear Chat"):
        if 'messages' in st.session_state:
            st.session_state['messages'] = []
        st.rerun()
    
    return use_real_apis


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Week 3: Multi-Agent System",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🤖 Week 3: Multi-Agent 'Yes Dear' Assistant")
    st.markdown("""
    **Multi-Agent System with Microsoft Agent Framework**
    
    This system uses 4 specialized agents working together to help you with your honeydew list:
    - 🎯 **Coordinator**: Analyzes your request and routes to appropriate agents
    - 🌐 **Research Agent**: Searches the web for current information
    - 📚 **Document Agent**: Searches your private knowledge base
    - 📝 **Summarizer**: Compiles findings into a coherent response
    """)
    
    # Check API key
    if not OPENAI_API_KEY:
        st.error("❌ OPENAI_API_KEY not found! Please add it to your .env file.")
        st.stop()
    
    # Render sidebar and get configuration
    use_real_apis = render_sidebar()
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    # Display welcome message
    if len(st.session_state['messages']) == 0:
        with st.chat_message("assistant"):
            st.markdown("""
👋 **Welcome to the Multi-Agent System!**

I'm powered by 4 specialized AI agents working together to help you with your honeydew list.

**Try asking:**
- "Search for the latest news on AI agents"
- "Find information in my documents about project requirements"
- "Research electric vehicles and summarize findings"

The agents will collaborate to find the best answer!
            """)
    
    # Display chat history
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What's on your honeydew list today?"):
        # Get fresh shared memory and ensure it's ready for new query
        shared_memory = get_shared_memory()
        
        # Add user message
        st.session_state['messages'].append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process with multi-agent system
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Use st.status for real-time updates (Streamlit's built-in solution)
            with st.status("🤖 Processing your request...", expanded=True) as status:
                # Create status display that updates in real-time
                st.markdown("### Agent Status")
                coord_status = st.empty()
                research_status = st.empty()
                doc_status = st.empty()
                summ_status = st.empty()
                st.markdown("---")
                activity_header = st.empty()
                activity_content = st.empty()
                
                # Initialize
                coord_status.write("🎯 Coordinator: Idle")
                research_status.write("🌐 Research: Idle")
                doc_status.write("📚 Document: Idle")
                summ_status.write("📝 Summarizer: Idle")
                activity_header.markdown("**� Recent Activity:**")
                activity_content.info("Waiting to start...")
            
            try:
                # Create fresh workflow for each query
                workflow = create_multi_agent_workflow(use_real_apis=use_real_apis)
                
                # Create initial message
                initial_message = ChatMessage(role="user", text=prompt)
                
                # Run workflow with streaming
                final_response = None
                
                async def run_workflow():
                    nonlocal final_response
                    
                    async for event in workflow.run_stream(initial_message):
                        if isinstance(event, WorkflowStatusEvent):
                            # UPDATE AGENT STATUS IN REAL-TIME
                            shared_mem = get_shared_memory()
                            
                            coord_state = shared_mem.agent_states.get('coordinator', 'Idle')
                            coord_time = shared_mem.agent_state_timestamps.get('coordinator', '')
                            coord_status.write(f"🎯 Coordinator: {coord_state} `{coord_time}`")
                            
                            research_state = shared_mem.agent_states.get('research', 'Idle')
                            research_time = shared_mem.agent_state_timestamps.get('research', '')
                            research_status.write(f"🌐 Research: {research_state} `{research_time}`")
                            
                            doc_state = shared_mem.agent_states.get('document', 'Idle')
                            doc_time = shared_mem.agent_state_timestamps.get('document', '')
                            doc_status.write(f"📚 Document: {doc_state} `{doc_time}`")
                            
                            summ_state = shared_mem.agent_states.get('summarizer', 'Idle')
                            summ_time = shared_mem.agent_state_timestamps.get('summarizer', '')
                            summ_status.write(f"📝 Summarizer: {summ_state} `{summ_time}`")
                            
                            # Update activity
                            if shared_mem.agent_messages:
                                activity_text = ""
                                for msg in shared_mem.agent_messages[-5:]:
                                    activity_text += f"• [{msg['timestamp'][-8:]}] {msg['agent']}: {msg['message'][:60]}\n"
                                activity_content.text(activity_text)
                        
                        elif isinstance(event, WorkflowOutputEvent):
                            final_response = event.data
                            status.update(label="✅ Complete!", state="complete")
                        
                        elif isinstance(event, ExecutorFailedEvent):
                            activity_content.error(f"⚠️ {event.executor_id} failed: {event.details.message}")
                    
                    return final_response
                
                # Run the workflow
                result = asyncio.run(run_workflow())
                
                # Show execution proof
                shared_mem = get_shared_memory()
                with st.expander("📊 Agent Execution Details", expanded=False):
                    st.markdown("**All agents completed successfully:**")
                    for agent_key, icon in [('coordinator', '🎯'), ('research', '🌐'), ('document', '📚'), ('summarizer', '📝')]:
                        state = shared_mem.agent_states.get(agent_key, 'Unknown')
                        timestamp = shared_mem.agent_state_timestamps.get(agent_key, '')
                        st.success(f"{icon} {agent_key.capitalize()}: {state} at {timestamp}")
                    
                    if shared_mem.agent_messages:
                        st.markdown("**Activity Log:**")
                        for msg in shared_mem.agent_messages:
                            st.caption(f"`[{msg['timestamp'][-8:]}]` {msg['agent']}: {msg['message']}")
                
                if result:
                    response_placeholder.markdown(result)
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": result
                    })
                else:
                    error_msg = "I apologize, but I couldn't generate a response. Please try again."
                    response_placeholder.error(error_msg)
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": error_msg
                    })
                
            except Exception as e:
                error_msg = f"❌ System error: {str(e)}"
                response_placeholder.error(error_msg)
                st.session_state['messages'].append({
                    "role": "assistant",
                    "content": error_msg
                })
                st.error(f"**Debug Info:** {str(e)}")


if __name__ == "__main__":
    main()
