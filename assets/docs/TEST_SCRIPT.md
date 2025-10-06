# Test Script for Context-Aware Research Assistant

## 🧪 Testing Guidelines

### Prerequisites
- ✅ Virtual environment activated
- ✅ OpenAI API key configured in `.env`
- ✅ Streamlit app running

### Test Scenarios

## 1. Interface Testing

### A. Initial Load Test
**Objective**: Verify the app loads correctly
**Steps**:
1. Navigate to http://localhost:8530
2. Check that the title displays: "🔍 Context-Aware Research Assistant"
3. Verify the couple image loads properly
4. Confirm search tool checkboxes are visible

**Expected Result**: Clean interface with centered layout and all elements visible

### B. Search Tool Controls Test
**Objective**: Test the search tool selection UI
**Steps**:
1. Toggle "🌐 Web Search" checkbox on/off
2. Toggle "📚 Document Search" checkbox on/off
3. Try all combinations:
   - Both enabled → Should show "🔄 Both Sources Active"
   - Web only → Should show "🌐 Web Only" 
   - Docs only → Should show "📚 Docs Only"
   - None selected → Should show "⚠️ No Sources Selected"

**Expected Result**: Status indicator updates correctly for each combination

## 2. Chat Interface Testing

### A. Basic Chat Functionality
**Objective**: Verify chat input and display works
**Test Messages**:
1. "Hello, can you help me research something?"
2. "What is artificial intelligence?"
3. "Tell me about machine learning algorithms"

**Expected Results**:
- Messages appear in chat bubbles
- User messages align left, assistant responses align right
- Chat history persists between messages
- Loading spinner shows during processing

### B. Conversational Memory Test
**Objective**: Verify the assistant remembers context
**Test Conversation**:
1. User: "What is Python programming?"
2. Assistant: [Provides response about Python]
3. User: "What are its main advantages?" (testing context awareness)
4. User: "Can you give me examples?" (testing follow-up context)

**Expected Result**: Assistant should understand "its" refers to Python from previous context

## 3. Search Tool Integration Testing

### A. Web Search Only Test
**Steps**:
1. Disable Document Search checkbox
2. Enable only Web Search checkbox
3. Ask: "What's the latest news about AI developments in 2025?"

**Expected Result**: 
- Response should indicate web search was used
- May include current/recent information
- Should cite web sources if available

### B. Document Search Only Test
**Steps**:
1. Disable Web Search checkbox  
2. Enable only Document Search checkbox
3. Ask: "Search my documents for information about project plans"

**Expected Result**:
- Should attempt to search vector store (placeholder ID)
- May return error about vector store not found (expected with placeholder)
- Should not use web search

### C. Both Sources Test
**Steps**:
1. Enable both Web Search and Document Search
2. Ask: "Find information about Streamlit development both from my docs and the web"

**Expected Result**:
- Should attempt to use both search tools
- Response should be comprehensive
- May combine information from multiple sources

## 4. Error Handling Testing

### A. No Sources Selected Test
**Steps**:
1. Disable both checkboxes
2. Ask any question
3. Check response handling

**Expected Result**: Should still provide a response using the assistant's knowledge

### B. API Error Simulation
**Test Cases**:
- Very long message (test token limits)
- Special characters and emojis
- Empty message (should be prevented by UI)

### C. Network/API Issues
**Scenarios to observe**:
- Response when API is slow
- Behavior during network interruptions
- Token usage tracking accuracy

## 5. UI/UX Testing

### A. Responsive Design Test
**Steps**:
1. Resize browser window
2. Test on different screen sizes
3. Verify mobile compatibility

**Expected Result**: Layout remains functional and readable

### B. Chat History Management
**Steps**:
1. Have a long conversation (10+ messages)
2. Check scrolling behavior
3. Test "Clear Chat History" button
4. Verify history is properly cleared

### C. Token Usage Display
**Steps**:
1. Ask a complex question
2. Expand the "📊 Usage Stats" section
3. Verify token counts are displayed

**Expected Result**: Accurate token usage information shown

## 6. Performance Testing

### A. Response Time Test
**Measure**:
- Time from message send to response start
- Time for complete response
- UI responsiveness during processing

### B. Memory Usage Test
**Monitor**:
- Chat history accumulation
- Session state management
- Browser performance with long conversations

## 7. Advanced Feature Testing

### A. Markdown Rendering Test
**Test with**:
```
Can you format a response with:
- **Bold text**
- *Italic text*  
- `Code blocks`
- [Links](http://example.com)
- Lists and bullet points
```

### B. Citation Testing (when tools work)
**Ask**: "Please provide a well-cited response about a technical topic"
**Expected**: Proper source citations and formatting

## 8. Edge Cases

### A. Special Characters
**Test Messages**:
- Emojis: "🚀🤖🔍 What about AI?"
- Foreign characters: "¿Qué es inteligencia artificial?"
- Code: "Explain this code: `print('hello')`"

### B. Long Conversations
**Test**: Sustained conversation with 20+ back-and-forth messages
**Monitor**: Memory usage, response quality, context retention

### C. Rapid Messages
**Test**: Send multiple messages quickly
**Expected**: Proper queuing and response handling

## 9. Security Testing

### A. Input Sanitization
**Test dangerous inputs** (safely):
- HTML tags: `<script>alert('test')</script>`
- SQL-like syntax: `'; DROP TABLE users; --`
- Very long strings

**Expected**: Inputs should be safely handled without breaking the app

## 10. Documentation Verification

### A. README Accuracy Test
**Verify**:
- Installation steps work correctly
- All dependencies are listed
- Usage instructions are accurate
- Screenshots/examples match current UI

## Success Criteria

✅ **Pass**: All basic chat functionality works
✅ **Pass**: Search tool toggles function correctly  
✅ **Pass**: Conversational memory is maintained
✅ **Pass**: Error handling is graceful
✅ **Pass**: UI is responsive and user-friendly
✅ **Pass**: Token usage tracking works
✅ **Pass**: Chat history management functions

## Known Limitations (Expected)

⚠️ **Vector Store**: Placeholder ID will cause document search to fail (expected)
⚠️ **Web Search**: May have limited functionality depending on API access
⚠️ **Tools**: Some tool responses may be simulated until full integration

## Reporting Issues

When testing, note:
1. **What you did** (exact steps)
2. **What you expected** to happen
3. **What actually happened**
4. **Browser/system info** if relevant
5. **Screenshots** if helpful

## Quick Test Commands

```bash
# Start the app (ensure virtual env is active)
source env/Scripts/activate
streamlit run app.py

# Test basic functionality
# 1. Open browser to localhost:8501 (or shown URL)
# 2. Try basic chat: "Hello, how can you help me?"
# 3. Toggle search options and test responses
# 4. Test conversational memory with follow-up questions
```

Happy testing! 🧪✨