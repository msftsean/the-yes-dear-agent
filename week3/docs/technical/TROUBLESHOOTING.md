# 🔧 Troubleshooting Guide - Multi-Agent System

Common issues and their solutions for the Week 3 Multi-Agent "Yes Dear" Assistant.

---

## 🚨 Critical Issues (App Won't Start)

### Issue 1: "ModuleNotFoundError: No module named 'agent_framework'"

**Symptoms**:
```python
ModuleNotFoundError: No module named 'agent_framework'
```

**Cause**: Agent Framework not installed or wrong environment

**Solution**:
```bash
# Activate virtual environment
cd c:\Users\segayle\repos\lo
source env/Scripts/activate

# Install with --pre flag (REQUIRED)
pip install agent-framework-azure-ai --pre

# Verify installation
pip list | grep agent-framework
# Should show:
# agent-framework-azure-ai    1.0.0b251007
# agent-framework-core        1.0.0b251007

# Now run the app
cd week3
streamlit run app_multi_agent.py
```

---

### Issue 2: "streamlit: command not found"

**Symptoms**:
```bash
bash: streamlit: command not found
```

**Cause**: Streamlit not installed or environment not activated

**Solution**:
```bash
# Activate environment first
source env/Scripts/activate

# Install streamlit
pip install streamlit

# Verify
streamlit --version

# Run app
cd week3
streamlit run app_multi_agent.py
```

---

### Issue 3: "OPENAI_API_KEY not found"

**Symptoms**:
- Red error banner in app
- Message: "❌ OpenAI API Key not configured"
- App loads but can't process queries

**Cause**: Missing or incorrect .env file

**Solution**:
```bash
# 1. Create .env file in ROOT folder (not week3!)
cd c:\Users\segayle\repos\lo
notepad .env

# 2. Add your API key (no quotes, no spaces):
OPENAI_API_KEY=sk-your-actual-key-here

# 3. Save and close

# 4. Restart Streamlit (Ctrl+C, then rerun)
cd week3
streamlit run app_multi_agent.py

# 5. Verify in sidebar: Should show ✅ OpenAI API Key configured
```

**Important Notes**:
- .env file goes in **root folder** (lo/), NOT in week3/
- No quotes around the API key
- No spaces before or after the =
- File must be named exactly `.env` (with the dot)

---

### Issue 4: "Address already in use" / Port 8501 busy

**Symptoms**:
```
OSError: [Errno 98] Address already in use
```

**Cause**: Another Streamlit instance running

**Solution**:
```bash
# Option 1: Kill the existing process
# Windows:
taskkill /F /IM streamlit.exe

# Then restart
streamlit run app_multi_agent.py

# Option 2: Use a different port
streamlit run app_multi_agent.py --server.port 8502

# Option 3: Find and close the existing browser tab running Streamlit
```

---

## ⚠️ Functionality Issues (App Runs But Doesn't Work Right)

### Issue 5: Agents Not Activating

**Symptoms**:
- Query submitted but no agent status changes
- All agents remain "Idle"
- No response generated

**Debugging Steps**:

1. **Check System Logs** (in sidebar):
   - Look for error messages
   - Check if Coordinator received the query
   - Verify routing decisions

2. **Expand Agent Messages**:
   - Should see [Coordinator] analyzing message
   - Should see routing decision
   - Look for error indicators

3. **Check Shared Memory**:
   - Should populate with query data
   - Look for execution_status field
   - Check for error entries

**Common Causes & Fixes**:

**A) Coordinator not routing**:
```python
# Check if query is too short or ambiguous
# Try more specific queries:
❌ "Search"  → Too vague
✅ "Search for AI news"  → Clear intent
```

**B) API errors (even in demo mode)**:
- Check browser console (F12) for JavaScript errors
- Refresh the page (Ctrl+R)
- Clear browser cache

**C) Shared memory not initialized**:
- Restart Streamlit
- Clear chat history
- Try again with fresh session

---

### Issue 6: Parallel Execution Not Working

**Symptoms**:
- Agents activate sequentially instead of parallel
- Timestamps show significant gaps
- Combined queries don't activate both agents

**Diagnosis**:
```bash
# Check agent timestamps in status panel:
Research:  10:30:15.234
Document:  10:30:18.891  ← Gap > 1 second = NOT parallel
```

**Solution**:

1. **Verify query triggers both**:
```
❌ "Search for AI"           → Only Research
❌ "Check documents"         → Only Document
✅ "Search AI and check docs" → Both agents
```

2. **Check workflow configuration**:
- Open app_multi_agent.py
- Verify WorkflowBuilder has parallel edges
- Confirm both agents are connected to Coordinator

3. **Review execution logic**:
```python
# Should see code like:
if needs_web and needs_docs:
    # Trigger both in parallel
    await asyncio.gather(
        research_agent.run(...),
        document_agent.run(...)
    )
```

---

### Issue 7: Responses Are Empty or Generic

**Symptoms**:
- Agent activates but response is vague
- No actual search results shown
- Generic "I can help with that" messages

**Cause**: Mock data not loading or Summarizer not receiving results

**Solution**:

1. **Check Shared Memory**:
```json
{
  "web_results": null,  ← Problem! Should have data
  "document_results": null
}
```

2. **Verify mock data functions**:
```bash
# In app code, search for:
get_mock_web_search()
get_mock_document_search()
```

3. **Test with simple query**:
```
Search for AI news
```

4. **Check System Logs for**:
```
[Research] Mock data loaded successfully
[Research] Found X results
```

5. **If still failing**:
- Restart Streamlit
- Clear browser cache
- Try incognito/private window

---

### Issue 8: "Use Real APIs" Causes Errors

**Symptoms**:
- Checking "Use Real APIs" breaks the app
- Error messages about API keys
- Agents fail with exceptions

**Expected Behavior**:
If real APIs are not configured, system should:
1. Show warning: "⚠️ APIs not configured"
2. Automatically fall back to mock data
3. Continue working normally

**If that's not happening**:

1. **Check error handling in code**:
```python
try:
    # Real API call
    results = real_web_search(query)
except Exception as e:
    # Should fall back
    results = get_mock_web_search(query)
```

2. **Verify .env file** (if you have API keys):
```bash
GOOGLE_API_KEY=your-key-here
GOOGLE_CSE_ID=your-cse-id-here
PINECONE_API_KEY=your-key-here
```

3. **If you don't have API keys**:
- Keep "Use Real APIs" UNCHECKED
- System should work fine in Demo Mode

---

### Issue 9: Workflow Visualization Not Showing

**Symptoms**:
- "Workflow Visualization" section is empty
- No diagram/flow chart visible
- Just shows loading spinner or blank

**Solution**:

1. **Make sure query completed**:
- Wait for Summarizer to finish
- Status should show all agents "Complete"

2. **Expand the section manually**:
- Click on "🔄 Workflow Visualization"
- Should toggle open

3. **Check browser compatibility**:
- Works best in Chrome/Edge
- May have issues in older browsers

4. **Clear and retry**:
- Clear chat history
- Submit new query
- Workflow should populate

---

### Issue 10: Shared Memory Inspector Empty

**Symptoms**:
- "Shared Memory" section shows nothing
- Says "No data available"
- Even after successful query

**Cause**: Memory not being populated or displayed

**Solution**:

1. **Check session state**:
```python
# In Streamlit, memory stored in st.session_state
# Verify it's being updated after each query
```

2. **Submit a test query**:
```
Search for AI developments
```

3. **Immediately expand Shared Memory**:
- Should show at minimum:
  - search_query
  - search_type
  - timestamp

4. **If still empty**, check browser console (F12):
- Look for JavaScript errors
- May need to refresh page

---

## 🐌 Performance Issues

### Issue 11: Very Slow Responses (30+ seconds)

**Symptoms**:
- Queries take forever
- Agents seem stuck
- System appears frozen

**Possible Causes**:

**A) Real API calls timing out**:
- If "Use Real APIs" is checked
- Google/Pinecone calls taking too long
- **Solution**: Uncheck "Use Real APIs"

**B) Model selection issue**:
- GPT-5 may be slower than GPT-4o
- **Solution**: Switch to GPT-4o in sidebar

**C) Large conversation history**:
- Too many messages in context
- **Solution**: Clear chat history

**D) Network issues**:
- OpenAI API slow
- **Solution**: Check internet connection

---

### Issue 12: Memory Usage Growing

**Symptoms**:
- Browser gets slower over time
- System RAM usage increasing
- Eventually crashes

**Solution**:
1. Clear chat history regularly
2. Refresh browser page after 10-15 queries
3. Close and reopen Streamlit if memory leak suspected

---

## 🎨 UI/Display Issues

### Issue 13: Layout Looks Broken

**Symptoms**:
- Elements overlapping
- Text cut off
- Buttons not visible

**Solutions**:

1. **Check browser zoom**:
   - Should be at 100%
   - Press Ctrl+0 to reset

2. **Try different browser**:
   - Chrome/Edge work best
   - Firefox should work
   - Safari may have issues

3. **Adjust window size**:
   - Minimum 1200px width recommended
   - Use full screen if needed

4. **Clear browser cache**:
   - Ctrl+Shift+Delete
   - Clear cached images and files

---

### Issue 14: Agent Status Not Updating

**Symptoms**:
- Agents remain "Idle" even when working
- No status transitions visible
- Stuck in "Processing..."

**Solution**:

1. **Check if Streamlit is streaming updates**:
   - Should see real-time changes
   - If frozen, may be a Streamlit issue

2. **Force refresh**:
   - Press 'r' in terminal where Streamlit is running
   - Or restart Streamlit entirely

3. **Check browser DevTools**:
   - F12 → Network tab
   - Should see WebSocket connection active
   - If disconnected, refresh page

---

## 📱 Browser-Specific Issues

### Chrome/Edge
- **Issue**: None expected, these work best
- **Tip**: Use DevTools (F12) for debugging

### Firefox
- **Issue**: May have WebSocket delays
- **Solution**: Refresh page if updates lag

### Safari
- **Issue**: Some CSS may not render correctly
- **Solution**: Use Chrome/Edge instead

### Internet Explorer
- **Issue**: Not supported
- **Solution**: Use modern browser

---

## 🧪 Testing-Specific Issues

### Issue 15: Can't Reproduce Parallel Execution

**Symptoms**:
- Both agents activate but timestamps identical or far apart
- Not clear if parallel or sequential

**How to Verify Parallel Execution**:

1. **Use this specific query**:
```
Research artificial intelligence and check our company documents for AI policies
```

2. **Watch Agent Status Panel**:
```
Before query:
  Research: Idle
  Document: Idle

During query (parallel):
  Research: Searching (10:30:15.234)
  Document: Searching (10:30:15.237)  ← Within milliseconds!

After:
  Research: Complete (10:30:18.123)
  Document: Complete (10:30:18.456)
```

3. **Check system logs**:
```
[System] Parallel execution mode activated
[Research] Starting at 10:30:15.234
[Document] Starting at 10:30:15.237
[System] Parallel tasks completed
```

4. **If timestamps show large gap** (>1 second):
- May be sequential execution
- Check code in app_multi_agent.py
- Look for `asyncio.gather()` usage

---

### Issue 16: Demo Mode Responses Too Generic

**Symptoms**:
- Mock data is too simple
- Not realistic enough for demo
- Reviewers may think system is broken

**Enhance Mock Data**:

1. **Edit mock data functions** in app_multi_agent.py
2. **Add more realistic content**:
```python
def get_mock_web_search(query):
    return f"""
    🌐 Web Search Results for '{query}'
    
    1. **Latest {query} Developments**
       Comprehensive analysis shows significant progress...
       Source: https://example.com/article1
    
    2. **Expert Insights on {query}**
       Industry leaders report breakthrough findings...
       Source: https://example.com/article2
    
    [3 more detailed results...]
    """
```

3. **Make it query-aware**:
- Parse query keywords
- Generate relevant mock content
- Include realistic URLs and dates

---

## 🆘 Emergency Fixes

### Nuclear Option 1: Complete Reset

If everything is broken:

```bash
# 1. Stop Streamlit (Ctrl+C)

# 2. Deactivate and reactivate environment
deactivate
source env/Scripts/activate

# 3. Reinstall Agent Framework
pip uninstall agent-framework-azure-ai agent-framework-core -y
pip install agent-framework-azure-ai --pre

# 4. Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +

# 5. Restart Streamlit
cd week3
streamlit run app_multi_agent.py
```

---

### Nuclear Option 2: Fresh Browser Session

```bash
# 1. Close ALL browser tabs
# 2. Clear ALL browser data (Ctrl+Shift+Delete)
# 3. Restart browser
# 4. Go to http://localhost:8501 in new tab
```

---

### Nuclear Option 3: Restart Everything

```bash
# 1. Stop Streamlit (Ctrl+C)
# 2. Close terminal
# 3. Close VS Code
# 4. Reboot computer (if desperate!)
# 5. Start fresh
```

---

## 📞 Getting Help

If none of these solutions work:

1. **Check System Logs** thoroughly
2. **Check Browser Console** (F12)
3. **Review error messages** carefully
4. **Test with minimal query**: "Search for AI"
5. **Try different browser**
6. **Review QUICKSTART.md** for setup steps

---

## ✅ Verification After Fixes

After applying any fix, verify:

- [ ] Streamlit starts without errors
- [ ] Sidebar shows ✅ OpenAI configured
- [ ] All 4 agents visible in status panel
- [ ] Simple query works: "Search for AI news"
- [ ] Response is generated and displayed
- [ ] No red error messages anywhere

---

## 📝 Known Limitations (Not Bugs!)

1. **Demo Mode uses mock data** - This is intentional!
2. **GPT-5 may give different responses** - Model variation
3. **Timestamps in milliseconds** - System-dependent
4. **Mock URLs aren't real** - By design for testing
5. **Document search finds "mock documents"** - Expected in demo mode

---

**Most issues can be fixed by**:
1. Restarting Streamlit
2. Checking .env file
3. Verifying environment activated
4. Clearing browser cache

**Still stuck?** Review SETUP_COMPLETE.md for initial setup verification.
