# Week 3 Multi-Agent System Demo Script
## "Yes Dear" Assistant Demonstration

---

## 🎬 Demo Overview

**Duration:** 10-15 minutes
**Audience:** AI Agent Bootcamp - Week 3 Presentation
**Objective:** Demonstrate multi-agent system meeting all assignment requirements

---

## 📋 Pre-Demo Checklist

- [ ] Application running: `streamlit run app_multi_agent.py`
- [ ] Browser open to `http://localhost:8501`
- [ ] Demo mode enabled (Real APIs unchecked)
- [ ] Chat history cleared
- [ ] Terminal visible (for debugging if needed)
- [ ] Architecture diagram ready (optional)

---

## 🎯 Demo Script

### Part 1: Introduction (2 minutes)

**Opening Statement:**
> "Today I'm demonstrating my Week 3 multi-agent system called 'Yes Dear' - an assistant that helps automate my honeydew list using 4 specialized AI agents built with Microsoft Agent Framework."

**Show System Architecture:**
1. Point to sidebar showing the 4 agents
2. Explain the flow:
   ```
   Coordinator → Research → Document → Summarizer
   ```

**Highlight Requirements Met:**
- ✅ Design Pattern: Sequential (with parallel capabilities)
- ✅ 4 Specialized Agents (Coordinator, Research, Document, Summarizer)
- ✅ Shared Memory: Active and visible
- ✅ Error Handling: Built-in fallbacks

---

### Part 2: Basic Functionality Demo (3 minutes)

**Demo Query 1: Simple Research Request**

**Say:** "Let me show you a basic query. I'll ask the system to research electric vehicles."

**Type in chat:**
```
Search for information about electric vehicles and their environmental impact
```

**Point out while processing:**
1. Click "Agent Workflow" expander
2. Show real-time status updates
3. Point out each agent executing:
   - ✅ Coordinator analyzing request
   - ✅ Research agent searching web
   - ✅ Document agent searching knowledge base
   - ✅ Summarizer compiling results

**When complete:**
- Show the synthesized response
- Point out markdown formatting
- Note source citations (if present)

---

### Part 3: Shared Memory Demo (2 minutes)

**Say:** "Now let me show you the shared memory system that enables agent collaboration."

**Actions:**
1. Check "Show Agent Activity" in sidebar
2. Scroll through agent messages
3. Point out:
   - Coordinator's routing decision
   - Research agent's search confirmation
   - Document agent's search confirmation
   - Summarizer's synthesis note

**Explain:**
> "This shared memory allows agents to communicate and share findings. The Coordinator logs its routing decision, search agents store their results, and the Summarizer accesses all findings to create a coherent response."

---

### Part 4: Agent Specialization Demo (3 minutes)

**Demo Query 2: Research-Heavy Query**

**Say:** "Let me demonstrate how agents specialize. This query focuses on web research."

**Type:**
```
What are the latest developments in AI agent technology from 2025?
```

**Point out:**
- Coordinator routes primarily to Research agent
- Research agent returns current web information
- Summarizer synthesizes findings
- Response includes recent information

**Demo Query 3: Document-Focused Query**

**Say:** "Now a query that would use the document search."

**Type:**
```
Find information in my documents about project requirements
```

**Point out:**
- Coordinator routes to Document agent
- System would search Pinecone (or mock data)
- Different type of results (internal knowledge)

---

### Part 5: Error Handling Demo (2 minutes)

**Say:** "One of our key requirements was robust error handling. Let me demonstrate the fallback system."

**Actions:**
1. Toggle "Use Real APIs" checkbox ON
2. Show red warning in sidebar (if APIs not configured)
3. Submit a query:
   ```
   Search for quantum computing breakthroughs
   ```

**Point out:**
- System attempts real APIs
- Automatically falls back to mock data
- Workflow completes successfully
- No system crash or failure

**Explain:**
> "Each agent has a 3-tier fallback strategy. If real APIs fail, they use mock data. If that fails, they pass the error gracefully. The workflow continues and users get the best possible response."

**Toggle "Use Real APIs" back OFF**

---

### Part 6: Code Walkthrough (3 minutes)

**Say:** "Let me briefly show you the code structure."

**Open:** `week3/app_multi_agent.py`

**Highlight Key Sections:**

1. **Shared Memory Class (Lines 44-91):**
   ```python
   class SharedMemory:
       def __init__(self):
           self.search_results: Dict[str, Any] = {}
           self.document_results: Dict[str, Any] = {}
           self.agent_messages: List[Dict[str, str]] = []
   ```
   - "This is our shared memory implementation"

2. **Agent Executors (Lines 175-424):**
   - Show CoordinatorExecutor
   - "Each agent is an Executor subclass"
   - Point out `@handler` decorator
   - Show error handling try-catch blocks

3. **Workflow Builder (Lines 427-452):**
   ```python
   workflow = (
       WorkflowBuilder()
       .set_start_executor(coordinator)
       .add_edge(coordinator, research)
       .add_edge(research, document)
       .add_edge(document, summarizer)
       .build()
   )
   ```
   - "This defines our sequential pattern"
   - "Could be modified for parallel execution"

---

### Part 7: Documentation Review (2 minutes)

**Say:** "I've created comprehensive documentation for this system."

**Open:** `week3/WEEK3_ARCHITECTURE.md`

**Scroll through sections:**
1. Requirements checklist (all checked)
2. Architecture diagram
3. Agent specifications
4. Shared memory system
5. Error handling strategies
6. Code organization

**Highlight:**
- Complete requirements traceability
- Detailed agent specifications
- Error handling documentation
- Future enhancement notes

---

### Part 8: Q&A Topics (Be Prepared)

**Likely Questions:**

**Q: Why sequential instead of parallel?**
> A: Sequential provides better control and debugging. The architecture supports parallel - I can show how to modify the WorkflowBuilder to run Research and Document agents simultaneously.

**Q: How does shared memory persist across agents?**
> A: The SharedMemory instance is global during workflow execution. Each agent updates it via `shared_memory.add_*()` methods. In production, this could be Redis or a database.

**Q: What happens if the Summarizer fails?**
> A: It has a 3-tier fallback: (1) GPT-4o synthesis, (2) formatted raw results, (3) error message. Users always get some response.

**Q: Can you add more agents?**
> A: Yes! I've documented potential additions in the architecture doc - Email Agent, Calendar Agent, and Action Agent. The framework makes this straightforward.

**Q: How would you deploy this?**
> A: Agent Framework supports distributed execution. Each agent could be a separate microservice. Shared memory would move to Redis. WorkflowBuilder configuration stays the same.

---

## 🎯 Key Talking Points

### Strengths to Emphasize

1. **Complete Requirements Coverage**
   - All 4 core requirements met
   - Documentation exceeds expectations
   - Demonstration is live and interactive

2. **Production-Ready Error Handling**
   - Multi-tier fallback strategies
   - No single point of failure
   - Graceful degradation

3. **Extensible Architecture**
   - Easy to add new agents
   - Simple to modify patterns
   - Framework supports scaling

4. **Developer Experience**
   - Clear code organization
   - Comprehensive comments
   - Easy to test and debug

---

## 🚨 Common Issues & Fixes

### Issue: App won't start
**Fix:** Check OPENAI_API_KEY in .env file

### Issue: Workflow hangs
**Fix:** Refresh browser, check terminal for errors

### Issue: No agent messages showing
**Fix:** Check "Show Agent Activity" in sidebar

### Issue: Mock data not appearing
**Fix:** Ensure "Use Real APIs" is unchecked

---

## 🎬 Closing Statement

**End with:**
> "This multi-agent system demonstrates all Week 3 requirements: 4 specialized agents working together through a sequential pattern, robust shared memory for collaboration, and comprehensive error handling. The Microsoft Agent Framework made it straightforward to implement these patterns, and the result is a production-ready system that's both powerful and maintainable. Thank you!"

---

## 📊 Backup Slides (If Needed)

### Slide 1: Architecture Diagram
```
┌─────────────┐
│ Coordinator │
└──────┬──────┘
       │
   ┌───┴───┐
   ▼       ▼
┌──────┐ ┌──────┐
│Research Document│
└───┬──┘ └──┬───┘
    │       │
    └───┬───┘
        ▼
  ┌────────────┐
  │ Summarizer │
  └────────────┘
```

### Slide 2: Requirements Matrix

| Requirement | Implementation | Evidence |
|------------|----------------|----------|
| Design Pattern | Sequential | WorkflowBuilder code |
| 3+ Agents | 4 Agents | Executor classes |
| Shared Memory | SharedMemory class | Code + UI log |
| Error Handling | 3-tier fallbacks | Try-catch blocks |

### Slide 3: Technology Stack
- Microsoft Agent Framework (Preview)
- OpenAI GPT-4o
- Streamlit
- Python 3.12
- Google Custom Search API (optional)
- Pinecone Vector DB (optional)

---

## 🔧 Demo Environment Setup

### Terminal Commands (Pre-Demo)
```bash
# Navigate to project
cd /c/Users/segayle/repos/lo

# Activate environment (if using)
source env/Scripts/activate  # or env\Scripts\activate on Windows

# Start app
streamlit run week3/app_multi_agent.py
```

### Browser Setup
- Open: `http://localhost:8501`
- Zoom: 125% (for visibility in presentation)
- Developer tools: Closed (cleaner view)
- Sidebar: Expanded

---

## 📝 Demo Notes Template

**Date:** _______________
**Audience:** _______________
**Duration:** _______________

**Demo Flow:**
- [ ] Introduction completed
- [ ] Basic demo completed
- [ ] Shared memory shown
- [ ] Specialization demonstrated
- [ ] Error handling shown
- [ ] Code walkthrough completed
- [ ] Documentation reviewed
- [ ] Q&A handled

**Issues Encountered:**
_____________________

**Audience Feedback:**
_____________________

**Improvements for Next Time:**
_____________________

---

**Good luck with your demo! 🚀**
