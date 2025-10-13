# 🧪 Complete Testing Script for Multi-Agent "Yes Dear" Assistant

This script provides a comprehensive step-by-step guide to test every feature of your multi-agent system.

**Estimated Time**: 20-30 minutes  
**Difficulty**: Easy  
**Prerequisites**: None (runs in demo mode by default)

---

## 📋 Pre-Test Checklist

Before starting, verify:

- [ ] You're in the `week3` folder
- [ ] Python virtual environment is activated
- [ ] Agent Framework is installed (check: `pip list | grep agent-framework`)
- [ ] `.env` file exists in root folder with OPENAI_API_KEY

---

## 🚀 Phase 1: Launch & Initial Setup (5 minutes)

### Step 1.1: Start the Application

```bash
cd c:\Users\segayle\repos\lo\week3
streamlit run app_multi_agent.py
```

**Expected Result**:
- Browser opens automatically to `http://localhost:8501`
- You see the "Yes Dear Multi-Agent Assistant" title
- Sidebar shows configuration options
- No error messages appear

**✅ Checkpoint**: If the app loads successfully, proceed. If not, check error messages.

---

### Step 1.2: Verify Initial UI State

**Check the following elements are visible**:

1. **Header Section**:
   - Title: "🎯 Yes Dear Multi-Agent Assistant"
   - Subtitle describing the system
   - Week 3 badge/indicator

2. **Sidebar - Configuration Panel**:
   - [ ] System Configuration section
   - [ ] OpenAI API Key status (should show ✅)
   - [ ] "Use Real APIs" checkbox (should be UNCHECKED)
   - [ ] API Mode indicator showing "🟢 Demo Mode"
   - [ ] Model Selection dropdown (default: gpt-4o)

3. **Main Chat Area**:
   - [ ] Welcome message from assistant
   - [ ] Empty chat input field at bottom
   - [ ] Status indicators showing "Ready"

4. **Agent Status Panel** (below sidebar):
   - [ ] Shows 4 agents: Coordinator, Research, Document, Summarizer
   - [ ] All agents showing "Idle" status
   - [ ] No active workflows

**✅ Checkpoint**: All UI elements present and properly styled.

---

## 🧪 Phase 2: Test Individual Agent Activation (10 minutes)

### Test 2.1: Research Agent Only

**Objective**: Verify Research Agent activates for web search queries.

**Test Query**:
```
Search for the latest developments in artificial intelligence
```

**What to Watch For**:

1. **Agent Status Panel Updates**:
   - ⏳ Coordinator Agent: "Analyzing..." → ✅ "Complete"
   - ⏳ Research Agent: "Searching web..." → ✅ "Complete"
   - 💤 Document Agent: "Idle" (should NOT activate)
   - ⏳ Summarizer Agent: "Compiling..." → ✅ "Complete"

2. **Workflow Visualization**:
   - Should show: `Coordinator → Research → Summarizer`
   - Visual flow indicator with arrows
   - Timestamp for each stage

3. **Agent Messages Log** (expandable section):
   ```
   [Coordinator] Detected: Web search request
   [Coordinator] → Routing to Research Agent
   [Research] Executing web search...
   [Research] Found X results
   [Research] → Sending to Summarizer
   [Summarizer] Compiling results...
   [Summarizer] Complete!
   ```

4. **Shared Memory Inspector** (expandable):
   - Should show:
     - `search_type: "web"`
     - `search_query: "latest developments in artificial intelligence"`
     - `web_results: [...]` (mock data with titles, snippets, URLs)
     - `document_results: null`

5. **Final Response**:
   - Should include web search results formatted nicely
   - Citations with URLs (mock sources)
   - Clear section headers
   - Professional formatting

**Expected Response Format**:
```markdown
🌐 Web Search Results

Based on my research, here are the latest developments in artificial intelligence:

**1. [Topic Title]**
[Summary content from mock data]
*Source: [Mock URL]*

**2. [Topic Title]**
[Summary content]
*Source: [Mock URL]*

[Additional results...]

---
*Search completed using Research Agent with web search capabilities*
```

**✅ Checkpoint**: 
- Research Agent activated ✅
- Document Agent stayed idle ✅
- Response received with proper formatting ✅

---

### Test 2.2: Document Agent Only

**Objective**: Verify Document Agent activates for internal knowledge queries.

**Test Query**:
```
Find information in our documents about vacation policy
```

**What to Watch For**:

1. **Agent Status Panel**:
   - ✅ Coordinator: Activated
   - 💤 Research Agent: Idle (should NOT activate)
   - ⏳ Document Agent: "Searching documents..." → ✅ "Complete"
   - ✅ Summarizer: Activated

2. **Workflow Visualization**:
   - Should show: `Coordinator → Document → Summarizer`
   - Different path than previous test

3. **Shared Memory Inspector**:
   ```json
   {
     "search_type": "documents",
     "search_query": "vacation policy",
     "web_results": null,
     "document_results": [...] (mock documents)
   }
   ```

4. **Final Response**:
   - Should reference internal documents
   - Include document titles and excerpts
   - Match scores or relevance indicators
   - Clear document citations

**Expected Response Format**:
```markdown
📚 Document Search Results

Found relevant information in your private knowledge base:

**Document 1: Employee Handbook - Vacation Policy**
Score: 0.95
[Summary of vacation policy from mock data]

**Document 2: HR Guidelines**
Score: 0.87
[Related policy information]

---
*Results from Document Agent searching 3 internal documents*
```

**✅ Checkpoint**:
- Document Agent activated ✅
- Research Agent stayed idle ✅
- Response shows internal document structure ✅

---

### Test 2.3: Both Agents in Parallel

**Objective**: Verify both Research and Document agents activate for comprehensive queries.

**Test Query**:
```
Research electric vehicles and check our company documents for any related policies
```

**What to Watch For**:

1. **Agent Status Panel** - PARALLEL EXECUTION:
   - ✅ Coordinator: "Analyzing..." → "Routing to multiple agents"
   - ⏳ Research Agent: Activates (shows timestamp)
   - ⏳ Document Agent: Activates (shows similar timestamp - parallel!)
   - ⏳ Summarizer: Waits for both → "Compiling..."

2. **Workflow Visualization**:
   ```
   Coordinator
        ↓
      ┌─┴─┐
      ↓   ↓
   Research | Document
      ↓   ↓
      └─┬─┘
        ↓
   Summarizer
   ```

3. **Timing Metrics**:
   - Research Agent start time: e.g., 10:30:15.234
   - Document Agent start time: e.g., 10:30:15.237 (within milliseconds!)
   - This proves parallel execution

4. **Shared Memory Inspector**:
   ```json
   {
     "search_type": "both",
     "search_query": "electric vehicles + company policies",
     "web_results": [...],
     "document_results": [...],
     "execution_mode": "parallel"
   }
   ```

5. **Final Response** - COMBINED RESULTS:
   ```markdown
   🔍 Comprehensive Search Results

   ## 🌐 Web Research Findings
   [Electric vehicle information from web]

   ## 📚 Internal Documentation
   [Company EV policies from documents]

   ## 💡 Summary
   [Synthesized insights combining both sources]

   ---
   *Parallel search completed: Research Agent + Document Agent → Summarizer*
   ```

**✅ Checkpoint**:
- Both agents activated ✅
- Parallel execution confirmed by timestamps ✅
- Combined results properly merged ✅

---

## 🛡️ Phase 3: Error Handling & Fallback Testing (5 minutes)

### Test 3.1: Ambiguous Query (Coordinator Decision Making)

**Objective**: Test Coordinator's ability to handle unclear requests.

**Test Query**:
```
What's the latest?
```

**Expected Behavior**:
- Coordinator detects ambiguity
- Asks clarifying question: "What would you like to know about? Please be more specific..."
- Does NOT activate Research or Document agents yet
- Waits for user clarification

**Follow-up Query**:
```
Latest AI news
```

**Expected Behavior**:
- Coordinator now routes to Research Agent
- Normal workflow proceeds

**✅ Checkpoint**: Coordinator properly handles ambiguity ✅

---

### Test 3.2: API Failure Simulation (Mock Fallback)

**Objective**: Verify fallback to mock data when real APIs would fail.

**Test Query** (with Real APIs still disabled):
```
Search for quantum computing breakthroughs
```

**What to Watch For**:

1. **System Logs** (in sidebar):
   ```
   [System] Demo Mode: Using mock data
   [Research] Real API not configured
   [Research] → Falling back to mock search results
   [Research] Mock data loaded successfully
   ```

2. **Agent Status Shows**:
   - No error states
   - Smooth continuation with fallback
   - Warning indicator: "⚠️ Using mock data"

3. **Response Includes Disclaimer**:
   ```
   Note: This is mock data for demonstration purposes.
   Configure real APIs in .env file for actual search results.
   ```

**✅ Checkpoint**: Graceful fallback to mock data ✅

---

### Test 3.3: Long Query Processing

**Objective**: Test system handles lengthy, complex requests.

**Test Query**:
```
I need you to research the following topics extensively: first, look into recent developments in renewable energy technology, particularly solar and wind power advances in 2024-2025; second, search our company documents for any sustainability initiatives or green energy policies we currently have in place; third, find information about government incentives for corporate renewable energy adoption; and finally, synthesize all this information into a comprehensive report with recommendations for our company.
```

**Expected Behavior**:

1. **Coordinator Analysis**:
   - Successfully parses multi-part request
   - Identifies: web search + document search needed
   - Extracts key topics: renewable energy, company policies, incentives

2. **Agent Activation**:
   - Research Agent: 2 searches (renewable tech + gov incentives)
   - Document Agent: 1 search (sustainability policies)
   - Summarizer: Comprehensive synthesis

3. **Response Structure**:
   - Clear sections for each topic
   - Well-organized with headers
   - Actionable recommendations
   - Full citation list

**✅ Checkpoint**: Complex query handled properly ✅

---

## 🎨 Phase 4: UI/UX Feature Testing (5 minutes)

### Test 4.1: Workflow Visualization

**Steps**:
1. Submit any query
2. Expand "🔄 Workflow Visualization" section
3. Watch real-time updates

**Verify**:
- [ ] Nodes appear for each agent
- [ ] Arrows show data flow direction
- [ ] Active node is highlighted
- [ ] Completed nodes show checkmarks
- [ ] Failed nodes (if any) show warning icons
- [ ] Timestamps on each transition

---

### Test 4.2: Shared Memory Inspector

**Steps**:
1. After query completes
2. Expand "🧠 Shared Memory" section
3. Review stored data

**Verify**:
- [ ] Shows conversation history
- [ ] Displays search queries
- [ ] Contains search results
- [ ] Has agent messages
- [ ] Includes metadata (timestamps, status)
- [ ] Properly formatted JSON/dictionary view
- [ ] Can copy/inspect values

---

### Test 4.3: Agent Communication Log

**Steps**:
1. Expand "💬 Agent Messages" section
2. Review message exchange

**Verify Each Message Has**:
- [ ] Timestamp
- [ ] Agent name/icon
- [ ] Message content
- [ ] Message type (info/success/error)
- [ ] Proper threading (responses to specific messages)

**Expected Flow**:
```
10:30:15 [Coordinator] 📋 New request received
10:30:15 [Coordinator] 🎯 Analysis: Web search needed
10:30:16 [Research] 🌐 Starting web search...
10:30:18 [Research] ✅ Found 5 results
10:30:18 [Summarizer] 📝 Compiling response...
10:30:20 [Summarizer] ✅ Response ready
```

---

### Test 4.4: Model Selection

**Steps**:
1. In sidebar, locate "Model Selection"
2. Switch from GPT-4o to GPT-5
3. Submit a test query
4. Observe differences (if any)

**Verify**:
- [ ] Dropdown shows both options
- [ ] Selection persists during session
- [ ] Model indicator updates
- [ ] Response generation uses selected model
- [ ] No errors on model switch

---

### Test 4.5: Chat History Persistence

**Steps**:
1. Submit 3-4 queries
2. Scroll up to see chat history
3. Verify all messages are visible
4. Click "🗑️ Clear Chat History" button
5. Confirm history clears

**Verify**:
- [ ] All messages preserved in order
- [ ] User messages styled differently from assistant
- [ ] Timestamps visible
- [ ] Clear button works
- [ ] Confirmation dialog appears
- [ ] After clear, only welcome message remains

---

## 🔧 Phase 5: Configuration Testing (Optional - 5 minutes)

### Test 5.1: Enable Real APIs (If you have API keys)

**Prerequisites**: 
- Google API Key configured in .env
- Pinecone API Key configured in .env

**Steps**:
1. In sidebar, check "🔴 Use Real APIs"
2. Mode indicator changes to "🔴 Live Mode"
3. Submit query: "Latest news on artificial intelligence"

**Expected Behavior**:
- Research Agent makes real Google API call
- Actual search results returned
- URLs are real (not mock)
- Response time may be longer
- More current/accurate information

**Verify**:
- [ ] Real API call logged
- [ ] Actual search results
- [ ] Valid URLs returned
- [ ] No mock data disclaimer

**Note**: If APIs not configured, system should:
- Show warning: "❌ APIs Missing"
- Fall back to mock data automatically
- Log: "Real API requested but not configured"

---

### Test 5.2: API Configuration Validation

**Steps**:
1. Go to sidebar "API Configuration" section
2. Review status indicators

**Verify Display Shows**:
```
Google Search API: ✅ Configured / ❌ Missing
Pinecone API: ✅ Configured / ❌ Missing
OpenAI API: ✅ Configured (Required)
```

**Click "Test APIs" button**:
- Should run connectivity tests
- Display results for each service
- Show latency metrics
- Report any configuration issues

---

## 📊 Phase 6: Performance & Reliability (5 minutes)

### Test 6.1: Rapid Fire Queries

**Objective**: Test system handles quick successive requests.

**Steps**:
1. Submit query: "AI news"
2. Immediately submit: "Quantum computing"
3. Then: "Renewable energy"
4. Then: "Space exploration"

**Expected Behavior**:
- System queues requests
- Shows "Processing..." indicator
- Completes each in order
- No crashes or errors
- All responses properly delivered

**Verify**:
- [ ] No dropped requests
- [ ] No mixed responses
- [ ] Proper order maintained
- [ ] Status indicators update correctly

---

### Test 6.2: Session Persistence

**Steps**:
1. Have an active conversation (3-4 messages)
2. Note the session data in Shared Memory
3. Check if conversation context is maintained
4. Submit follow-up: "Tell me more about the last topic"

**Expected Behavior**:
- System references previous conversation
- Shared memory contains full history
- Follow-up understood contextually
- No "I don't know what you're referring to"

---

### Test 6.3: Token Usage Monitoring

**Steps**:
1. After completing a query
2. Expand "📊 Token Usage" section (if available)

**Verify Shows**:
- [ ] Prompt tokens used
- [ ] Completion tokens used
- [ ] Total tokens
- [ ] Estimated cost (if configured)
- [ ] Model used
- [ ] Breakdown by agent

---

## ✅ Final Validation Checklist

After completing all tests, verify:

### Core Functionality
- [ ] Coordinator Agent properly routes all request types
- [ ] Research Agent successfully searches web (mock or real)
- [ ] Document Agent successfully searches documents (mock or real)
- [ ] Summarizer Agent compiles results coherently
- [ ] Parallel execution works for combined queries
- [ ] All agents communicate via shared memory

### Error Handling
- [ ] Ambiguous queries handled gracefully
- [ ] API failures trigger fallbacks
- [ ] Invalid inputs rejected with helpful messages
- [ ] System never crashes or hangs
- [ ] Error messages are user-friendly

### UI/UX
- [ ] All interface elements functional
- [ ] Workflow visualization updates in real-time
- [ ] Shared memory inspector shows live data
- [ ] Agent status panel accurate
- [ ] Chat history preserved correctly
- [ ] Responsive design works on different screen sizes

### Performance
- [ ] Queries complete within reasonable time (5-15 seconds)
- [ ] No memory leaks during extended use
- [ ] Rapid queries handled properly
- [ ] System recovers from errors automatically

### Documentation
- [ ] README instructions accurate
- [ ] Architecture diagram matches implementation
- [ ] Code comments helpful and accurate
- [ ] Demo script works as written

---

## 🐛 Troubleshooting Guide

### Issue: App won't start

**Check**:
1. Virtual environment activated?
   ```bash
   source env/Scripts/activate
   ```
2. Dependencies installed?
   ```bash
   pip install agent-framework-azure-ai --pre
   ```
3. In correct directory?
   ```bash
   cd week3
   ```

---

### Issue: Import errors

**Solution**:
```bash
pip uninstall agent-framework-azure-ai -y
pip install agent-framework-azure-ai --pre
```

---

### Issue: "API Key not found"

**Check**:
1. .env file exists in root folder (not week3)
2. Contains: `OPENAI_API_KEY=sk-...`
3. No extra spaces or quotes
4. Restart Streamlit after adding

---

### Issue: Agents not activating

**Debug Steps**:
1. Check System Logs in sidebar
2. Look for error messages
3. Verify Coordinator is receiving the query
4. Check shared memory for routing decision
5. Review agent status indicators

---

### Issue: Mock data not showing

**Solution**:
- Ensure "Use Real APIs" is UNCHECKED
- Check logs for fallback messages
- Verify mock_data functions in code
- Clear browser cache and reload

---

## 📸 Screenshot Checklist for Documentation

Capture these for your assignment submission:

1. **Main UI** - Full application view with welcome message
2. **Agent Status Panel** - All 4 agents visible
3. **Active Query** - Agents working with status updates
4. **Workflow Visualization** - Flow diagram with active nodes
5. **Shared Memory** - Expanded view with data
6. **Agent Messages** - Communication log
7. **Web Search Result** - Research Agent output
8. **Document Search Result** - Document Agent output
9. **Combined Search** - Both agents in parallel
10. **Error Handling** - Fallback in action
11. **Configuration Panel** - Sidebar with settings
12. **Performance Stats** - Token usage display

---

## 🎉 Success Criteria

**Your system passes all tests if**:

✅ All 4 agents activate appropriately  
✅ Shared memory properly stores and retrieves data  
✅ Workflow visualization shows accurate flow  
✅ Error handling prevents crashes  
✅ Mock data works reliably  
✅ UI is responsive and intuitive  
✅ Chat history persists correctly  
✅ Parallel execution demonstrated  
✅ Sequential flow confirmed  
✅ All documentation accurate  

---

## 📝 Test Results Template

Use this to document your testing:

```markdown
# Test Results - Week 3 Multi-Agent System

**Tested By**: [Your Name]
**Date**: October 13, 2025
**Duration**: [X] minutes

## Phase 1: Launch ✅/❌
- App started successfully: 
- UI elements present: 
- No errors on load: 

## Phase 2: Agent Activation ✅/❌
- Research Agent only: 
- Document Agent only: 
- Both agents parallel: 

## Phase 3: Error Handling ✅/❌
- Ambiguous query: 
- API fallback: 
- Long query: 

## Phase 4: UI/UX ✅/❌
- Workflow visualization: 
- Shared memory: 
- Agent messages: 
- Model selection: 
- Chat history: 

## Phase 5: Configuration ✅/❌
- Real APIs: 
- API validation: 

## Phase 6: Performance ✅/❌
- Rapid queries: 
- Session persistence: 
- Token tracking: 

## Overall Assessment
**Pass/Fail**: 
**Notes**: 
**Issues Found**: 
**Recommendations**: 
```

---

**Time to test!** Follow this script step by step and document your results. Good luck! 🚀
