# 🎯 Quick Test Cheat Sheet - Multi-Agent System

**Use this for rapid testing - detailed guide in TESTING_SCRIPT.md**

---

## 🚀 Quick Start (30 seconds)

```bash
cd week3
streamlit run app_multi_agent.py
```

Browser opens → Verify all UI elements visible → Start testing!

---

## 🧪 5 Essential Test Queries

### 1️⃣ Research Agent Only (Web Search)
```
Search for the latest AI developments
```
**Expected**: Coordinator → Research → Summarizer  
**Look for**: Web results with URLs, no document search

---

### 2️⃣ Document Agent Only (Internal Search)
```
Find information in our documents about vacation policy
```
**Expected**: Coordinator → Document → Summarizer  
**Look for**: Document titles with match scores, no web search

---

### 3️⃣ Both Agents Parallel (Combined)
```
Research electric vehicles and check our company documents for related policies
```
**Expected**: Coordinator → [Research + Document] → Summarizer  
**Look for**: Both sections in response, parallel timestamps

---

### 4️⃣ Ambiguous Query (Coordinator Decision)
```
What's the latest?
```
**Expected**: Coordinator asks for clarification  
**Look for**: No agent activation, request for more info

---

### 5️⃣ Complex Multi-Part Query
```
Research renewable energy technology, find our sustainability policies, and summarize with recommendations
```
**Expected**: All agents activate, comprehensive response  
**Look for**: Multiple sections, well-structured output

---

## 👀 What to Watch For

### Agent Status Panel
```
🎯 Coordinator: [Analyzing/Routing/Complete]
🌐 Research: [Idle/Searching/Complete]
📚 Document: [Idle/Searching/Complete]
📝 Summarizer: [Idle/Compiling/Complete]
```

### Workflow Visualization
```
Query 1: Coordinator → Research → Summarizer
Query 2: Coordinator → Document → Summarizer
Query 3: Coordinator → [Research + Document] → Summarizer
```

### Shared Memory (Expand to view)
```json
{
  "search_type": "web|documents|both",
  "search_query": "...",
  "web_results": [...],
  "document_results": [...],
  "execution_mode": "sequential|parallel"
}
```

---

## ✅ Quick Validation Checklist

- [ ] **Coordinator** routes all queries correctly
- [ ] **Research Agent** activates for web queries
- [ ] **Document Agent** activates for document queries
- [ ] **Both agents** activate for combined queries
- [ ] **Parallel execution** shown by timestamps
- [ ] **Summarizer** compiles all results
- [ ] **Shared memory** updates in real-time
- [ ] **Error handling** works (try ambiguous queries)
- [ ] **UI updates** show workflow progress
- [ ] **Chat history** preserved across queries

---

## 🎨 UI Elements to Verify

### Header
- [ ] Title: "Yes Dear Multi-Agent Assistant"
- [ ] Week 3 badge visible
- [ ] Status indicator (Ready/Processing)

### Sidebar
- [ ] System Configuration section
- [ ] API status indicators
- [ ] "Use Real APIs" toggle (leave OFF for testing)
- [ ] Model selection dropdown
- [ ] Clear chat button

### Main Area
- [ ] Chat messages display
- [ ] Agent status panel (4 agents visible)
- [ ] Workflow visualization (expandable)
- [ ] Shared memory inspector (expandable)
- [ ] Agent messages log (expandable)
- [ ] Chat input at bottom

---

## 🐛 Quick Troubleshooting

**App won't start?**
```bash
source env/Scripts/activate
pip install agent-framework-azure-ai --pre
cd week3
streamlit run app_multi_agent.py
```

**Import errors?**
```bash
pip uninstall agent-framework-azure-ai -y
pip install agent-framework-azure-ai --pre
```

**No responses?**
- Check OPENAI_API_KEY in .env file
- Verify API status in sidebar (should show ✅)
- Look at System Logs for error messages

**Agents not activating?**
- Check Agent Status Panel for activity
- Expand Agent Messages to see routing decisions
- Review Shared Memory for execution data

---

## 📊 Test Results Quick Log

```
Test 1 (Research Only):     ✅/❌
Test 2 (Document Only):     ✅/❌
Test 3 (Both Parallel):     ✅/❌
Test 4 (Ambiguous):         ✅/❌
Test 5 (Complex):           ✅/❌

UI Elements Working:        ✅/❌
Error Handling:             ✅/❌
Parallel Execution:         ✅/❌
Shared Memory:              ✅/❌
Workflow Visualization:     ✅/❌

Overall: PASS / FAIL
```

---

## 🎓 Assignment Requirements Check

- [ ] **Design Pattern**: Sequential with parallel ✅
- [ ] **4 Agents**: Coordinator, Research, Document, Summarizer ✅
- [ ] **Shared Memory**: WorkflowContext + SharedMemory class ✅
- [ ] **Error Handling**: Fallbacks for each agent ✅
- [ ] **Demo**: Working Streamlit app ✅
- [ ] **Documentation**: 6+ markdown files ✅

---

## 🎬 Demo Tips

1. **Start with Research Agent test** - Shows web search capability
2. **Then Document Agent** - Shows internal knowledge base
3. **Show parallel execution** - The "wow" moment!
4. **Demonstrate error handling** - Try ambiguous query
5. **Expand visualizations** - Show workflow and shared memory
6. **Walk through architecture** - Open WEEK3_ARCHITECTURE.md

**Demo Time**: 10-15 minutes  
**Success Rate**: Should be 100% in demo mode  
**Impressive Factor**: High! 🎉

---

## 📸 Screenshot Moments

1. All 4 agents showing in status panel
2. Parallel execution with both agents active
3. Workflow visualization with branching
4. Shared memory with combined results
5. Agent messages showing communication
6. Final response with both web + document results

---

## 💡 Pro Tips

- **Always test in Demo Mode first** (Real APIs OFF)
- **Demo Mode is reliable** - No API failures
- **Open all expandable sections** - Shows full capability
- **Try follow-up questions** - Tests conversation context
- **Show the documentation** - Demonstrates thoroughness
- **Highlight error handling** - Shows production-ready thinking

---

**Ready to test? Follow this guide for a quick 10-minute validation!**

For comprehensive testing, see **TESTING_SCRIPT.md**
