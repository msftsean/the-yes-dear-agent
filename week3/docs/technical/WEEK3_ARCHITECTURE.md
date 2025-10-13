# Week 3 Multi-Agent System Architecture
## "Yes Dear" Assistant - Microsoft Agent Framework Implementation

---

## 📋 Assignment Requirements Checklist

### ✅ Core Requirements Met

| Requirement | Implementation | Status |
|------------|----------------|--------|
| **Design Pattern** | Sequential with Parallel Capabilities | ✅ Complete |
| **3+ Specialized Agents** | 4 Agents: Coordinator, Research, Document, Summarizer | ✅ Complete |
| **Shared Memory** | WorkflowContext + SharedMemory class | ✅ Complete |
| **Error Handling** | Fallback strategies for each agent | ✅ Complete |
| **Demonstration** | Streamlit UI with live workflow visualization | ✅ Complete |
| **Documentation** | This file + inline code comments | ✅ Complete |

---

## 🏗️ System Architecture

### Overview

The "Yes Dear" Multi-Agent System automates honeydew list tasks using 4 specialized AI agents that collaborate through Microsoft Agent Framework. The system follows a **Sequential Design Pattern** with capabilities for parallel execution.

```
┌────────────────────────────────────────────────────────┐
│                   User Request                         │
│            (via Streamlit Interface)                   │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │   1. Coordinator Agent      │
         │   • Analyzes request        │
         │   • Determines routing      │
         │   • Updates shared memory   │
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │   2. Research Agent         │
         │   • Web search (Google API) │
         │   • Mock fallback           │
         │   • Stores results          │
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │   3. Document Agent         │
         │   • Vector search (Pinecone)│
         │   • Mock fallback           │
         │   • Stores results          │
         └──────────────┬──────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │   4. Summarizer Agent       │
         │   • Compiles findings       │
         │   • Synthesizes response    │
         │   • Returns to user         │
         └─────────────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────┐
         │      Shared Memory          │
         │   • Search results          │
         │   • Agent messages          │
         │   • Task history            │
         └─────────────────────────────┘
```

---

## 🤖 Agent Specifications

### 1. Coordinator Agent (CoordinatorExecutor)

**Role:** Entry point and orchestrator

**Responsibilities:**
- Receives user requests from the honeydew list
- Analyzes intent (research vs. documents vs. both)
- Routes requests to appropriate specialized agents
- Maintains task context in shared memory

**Input:** ChatMessage with user query

**Output:** Routing dictionary with agent activation flags

**Error Handling:**
- Falls back to web search if routing analysis fails
- Logs all routing decisions to shared memory

**Code Location:** Lines 175-228

---

### 2. Research Agent (ResearchExecutor)

**Role:** External information retrieval specialist

**Responsibilities:**
- Executes web searches using Google Custom Search API
- Falls back to mock data for reliable demos
- Stores search results in shared memory
- Handles API failures gracefully

**Input:** Routing dictionary from Coordinator

**Output:** Routing dictionary with web search results

**Error Handling:**
- Primary: Google Custom Search API
- Fallback: Mock search data
- Logs all search operations

**Code Location:** Lines 231-284

---

### 3. Document Agent (DocumentExecutor)

**Role:** Internal knowledge base specialist

**Responsibilities:**
- Searches private document collection via Pinecone
- Vector similarity search for relevant documents
- Falls back to mock data for reliable demos
- Stores document results in shared memory

**Input:** Routing dictionary from Research Agent

**Output:** Routing dictionary with document search results

**Error Handling:**
- Primary: Pinecone vector search
- Fallback: Mock document data
- Logs all search operations

**Code Location:** Lines 287-340

---

### 4. Summarizer Agent (SummarizerExecutor)

**Role:** Final synthesis and response generation

**Responsibilities:**
- Compiles results from all search agents
- Synthesizes coherent response using GPT-4o
- Formats response with markdown
- Cites sources appropriately

**Input:** Routing dictionary with all search results

**Output:** Final string response to user (workflow output)

**Error Handling:**
- Primary: GPT-4o synthesis
- Fallback: Formatted raw results
- Last resort: Error message

**Code Location:** Lines 343-424

---

## 🧠 Shared Memory System

### Implementation

The `SharedMemory` class provides persistent state across all agents during workflow execution.

```python
class SharedMemory:
    - search_results: Dict[str, Any]      # Web search findings
    - document_results: Dict[str, Any]    # Document search findings
    - agent_messages: List[Dict]          # Inter-agent communication log
    - task_history: List[str]             # Historical tasks
    - current_task: Optional[str]         # Active task
    - user_preferences: Dict[str, Any]    # User settings
```

### Key Features

1. **Search Result Storage**
   - Timestamps all queries
   - Stores both web and document results
   - Enables result reuse across agents

2. **Agent Communication Log**
   - Tracks agent-to-agent messages
   - Timestamps all communications
   - Visible in UI for transparency

3. **Task Context**
   - Maintains current task state
   - Prevents duplicate work
   - Enables task history tracking

**Code Location:** Lines 44-91

---

## 🔄 Design Pattern: Sequential with Parallel Capabilities

### Current Implementation: Sequential

```
Coordinator → Research → Document → Summarizer
```

Each agent waits for the previous agent to complete before executing.

### Why Sequential?

1. **Routing Logic**: Document agent needs research agent's output
2. **Resource Efficiency**: Avoids unnecessary parallel API calls
3. **Cost Control**: Reduces API usage in mock mode
4. **Debugging**: Easier to trace workflow execution

### Parallel Capabilities

The architecture supports parallel execution by modifying the workflow builder:

```python
# Current: Sequential
workflow = (
    WorkflowBuilder()
    .set_start_executor(coordinator)
    .add_edge(coordinator, research)
    .add_edge(research, document)
    .add_edge(document, summarizer)
    .build()
)

# Alternative: Parallel Research + Document
workflow = (
    WorkflowBuilder()
    .set_start_executor(coordinator)
    .add_edge(coordinator, research)
    .add_edge(coordinator, document)  # Both execute in parallel
    .add_edge(research, summarizer)
    .add_edge(document, summarizer)
    .build()
)
```

---

## 🛡️ Error Handling & Fallback Strategies

### Hierarchical Fallback System

Each agent implements a **3-tier fallback strategy**:

#### Tier 1: Primary Operation
- Real API calls (Google, Pinecone, OpenAI)
- Best quality results
- Requires API keys

#### Tier 2: Automatic Fallback
- Mock data generation
- Guaranteed to work
- Used for demos and testing

#### Tier 3: Error Messaging
- Clear error communication
- Maintains system stability
- Allows partial functionality

### Agent-Specific Fallback Strategies

**Coordinator Agent:**
```
Primary: Intent analysis
Fallback: Default to web search
Critical: Pass raw query forward
```

**Research Agent:**
```
Primary: Google Custom Search API
Fallback: Mock web search data
Critical: Skip web search, continue workflow
```

**Document Agent:**
```
Primary: Pinecone vector search
Fallback: Mock document data
Critical: Skip document search, continue workflow
```

**Summarizer Agent:**
```
Primary: GPT-4o synthesis
Fallback: Formatted raw results
Critical: Return error message to user
```

### Error Propagation Prevention

- Errors in one agent don't crash the entire workflow
- Shared memory logs all errors for debugging
- User receives best possible response given failures

---

## 🔧 Technology Stack

### Core Framework
- **Microsoft Agent Framework** (v1.0.0b251007)
  - `agent-framework-core`: Core workflow engine
  - `agent-framework-azure-ai`: Azure integration
  - Installed with `--pre` flag (preview release)

### AI Models
- **OpenAI GPT-4o**: Summarization and synthesis
- **text-embedding-ada-002**: Document embeddings (Pinecone)

### APIs & Services
- **Google Custom Search API**: Web search
- **Pinecone**: Vector database for documents
- **OpenAI API**: Chat completions and embeddings

### UI & Infrastructure
- **Streamlit**: Web interface
- **Python 3.12**: Runtime
- **asyncio**: Async workflow execution

---

## 📊 Workflow Execution Flow

### Step-by-Step Execution

1. **User Input**
   ```
   User types query in Streamlit chat interface
   → System creates ChatMessage object
   ```

2. **Workflow Initialization**
   ```
   create_multi_agent_workflow(use_real_apis)
   → Builds workflow with WorkflowBuilder
   → Creates all executor instances
   ```

3. **Coordinator Analysis**
   ```
   CoordinatorExecutor.handle(message)
   → Analyzes query intent
   → Creates routing dictionary
   → Updates shared memory
   → Sends to Research Agent
   ```

4. **Research Execution**
   ```
   ResearchExecutor.handle(routing)
   → Checks if web search needed
   → Executes Google API or mock search
   → Stores results in shared memory
   → Updates routing dictionary
   → Sends to Document Agent
   ```

5. **Document Execution**
   ```
   DocumentExecutor.handle(routing)
   → Checks if document search needed
   → Executes Pinecone search or mock
   → Stores results in shared memory
   → Updates routing dictionary
   → Sends to Summarizer
   ```

6. **Synthesis & Response**
   ```
   SummarizerExecutor.handle(routing)
   → Compiles all search results
   → Uses GPT-4o for synthesis
   → Yields final output
   → Workflow completes
   ```

7. **UI Update**
   ```
   Streamlit receives WorkflowOutputEvent
   → Displays response to user
   → Adds to chat history
   → Ready for next query
   ```

---

## 🎨 User Interface Features

### Main Chat Interface
- Claude-style chat experience
- Real-time message streaming
- Markdown formatting support

### Agent Workflow Viewer
- Expandable workflow status panel
- Shows agent execution in real-time
- Displays state transitions

### Sidebar Controls
- **API Mode Toggle**: Switch between mock and real APIs
- **Agent Activity Log**: View inter-agent communications
- **System Status**: Check API key configuration
- **Architecture Info**: View system design
- **Reset Controls**: Clear chat or restart system

### Visual Feedback
- Status indicators for each agent
- Error messages with fallback notifications
- Progress updates during workflow execution

---

## 🚀 Running the System

### Prerequisites
```bash
# Required
export OPENAI_API_KEY="your-openai-key"

# Optional (for real APIs)
export GOOGLE_API_KEY="your-google-key"
export GOOGLE_CSE_ID="your-cse-id"
export PINECONE_API_KEY="your-pinecone-key"
```

### Installation
```bash
cd week3
pip install -r ../requirements.txt
# Note: agent-framework-azure-ai requires --pre flag
```

### Launch
```bash
streamlit run app_multi_agent.py
```

### Testing

**Demo Mode (Mock APIs):**
1. Launch app
2. Ensure "Use Real APIs" is unchecked
3. Try: "Search for information about AI agents"
4. Watch workflow execute with mock data

**Live Mode (Real APIs):**
1. Configure API keys in .env
2. Launch app
3. Check "Use Real APIs" in sidebar
4. Try: "Find latest news on electric vehicles"
5. Watch real API calls execute

---

## 📈 Scalability Considerations

### Current Limitations
- Sequential execution may be slower than parallel
- All agents run in same process
- Shared memory is in-memory only

### Future Enhancements

1. **Parallel Execution**
   - Modify workflow to run Research and Document agents in parallel
   - Reduce latency for comprehensive queries

2. **Distributed Agents**
   - Agent Framework supports distributed execution
   - Can deploy agents as separate services

3. **Persistent Shared Memory**
   - Replace in-memory storage with Redis/database
   - Enable cross-session memory

4. **Additional Agents**
   - Email Agent: Send results via email
   - Calendar Agent: Schedule follow-ups
   - Task Agent: Create action items

---

## 🐛 Known Issues & Workarounds

### Issue 1: OpenAI Version Downgrade
**Problem:** Agent Framework requires `openai<2.0`
**Impact:** May conflict with other packages requiring OpenAI v2+
**Workaround:** Use separate virtual environment

### Issue 2: Async Event Loop in Streamlit
**Problem:** Streamlit doesn't have native async support
**Impact:** Must use `asyncio.run()` wrapper
**Workaround:** Implemented in code (see line 573)

### Issue 3: Shared Memory Isolation
**Problem:** Global shared memory shared across all users
**Impact:** Multi-user deployments may have conflicts
**Workaround:** Use session-specific shared memory instances

---

## 📚 References

- [Microsoft Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Pinecone Vector Database](https://docs.pinecone.io)

---

## 👨‍💻 Development Notes

### Code Organization
- **Lines 1-42**: Imports and configuration
- **Lines 44-91**: Shared memory system
- **Lines 93-173**: Search utility functions
- **Lines 175-424**: Agent executor classes
- **Lines 427-452**: Workflow builder
- **Lines 455-594**: Streamlit UI

### Testing Approach
1. Test each agent individually with mock data
2. Test workflow with mock data end-to-end
3. Test with real APIs (if available)
4. Test error handling by forcing failures

### Debugging Tips
- Enable "Show Agent Activity" in sidebar
- Check shared memory state between agents
- Use workflow status viewer to trace execution
- Check terminal for async errors

---

**Created:** October 13, 2025
**Assignment:** AI Agent Bootcamp - Week 3
**Framework:** Microsoft Agent Framework (Preview)
**Status:** ✅ Complete - All requirements met
