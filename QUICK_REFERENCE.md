# Week 4 Production Upgrade - Quick Reference

## What This Prompt Does

Upgrades your Week 3 Multi-Agent "Yes Dear" Assistant (`app_multi_agent.py`) with production features required for the Week 4 bootcamp assignment.

## Current State (Week 3)
- ✅ 4 specialized agents (Coordinator, Research, Document, Summarizer)
- ✅ Microsoft Agent Framework
- ✅ Sequential workflow with shared memory
- ✅ Streamlit UI with agent visualization
- ✅ 874 lines of code

## What Gets Added (Week 4)

### 1. Cost Monitoring & Budget Protection 💰
- Real-time OpenAI cost tracking
- Daily spending limits ($100 default)
- Budget alerts (70% threshold)
- Per-agent cost breakdown
- Visual dashboard in sidebar

### 2. Testing & Evaluation Framework 🧪
- 10-test suite (2 normal, 6 edge, 2 adversarial)
- OpenAI Evals-style testing
- Pass/fail metrics
- Downloadable results
- Admin panel in sidebar

### 3. Enhanced Error Handling ⚠️
- Exponential backoff (1s → 2s → 4s → 8s)
- Circuit breaker pattern
- Model fallback (GPT-4o → GPT-3.5)
- User-friendly error messages
- Retry with jitter

### 4. Security & Safety 🔒
- OpenAI Moderation API integration
- Prompt injection detection
- PII detection (email, phone, SSN, credit card)
- Rate limiting (10 requests/min per user)
- Input sanitization

### 5. Production Monitoring Dashboard 📊
- Environment indicator (Dev/Staging/Prod)
- Cost metrics with progress bar
- Performance metrics (avg time, p95, success rate)
- System health (API status, circuit breakers)
- Security monitoring

### 6. Cost Optimization 💾
- Response caching (50% savings, 1-hour TTL)
- Model cascading (GPT-3.5 for simple queries)
- Batch API support (framework)
- Cache controls in sidebar

### 7. Production Checklist ✅
- 12 automated checks across 3 categories
- Readiness score calculation
- Detailed status for each check
- Foundation, Quality, Operations validation

## How to Use This Prompt

1. **Open your `app_multi_agent.py` in VS Code**
2. **Paste the entire `WEEK4_GITHUB_COPILOT_PROMPT.md` as comments** or keep it open in a split view
3. **Work through each section:**
   - Section 1: Add CostMonitor class
   - Section 2: Add EvaluationFramework class
   - Section 3: Add ProductionErrorHandler class
   - Section 4: Add SecurityManager class
   - Section 5: Add render_production_dashboard function
   - Section 6: Add CostOptimizer class
   - Section 7: Add ProductionChecklist class

4. **Initialize everything in session state**
5. **Integrate with existing workflow:**
   - Add cost tracking to agent API calls
   - Wrap agent execution with error handling
   - Add security validation to user input
   - Render dashboard in sidebar

6. **Test everything:**
   - Run evaluation suite
   - Check budget alerts
   - Test security blocks
   - Verify error retries

## Key Integration Points

### Where to Track Costs
```python
# After each OpenAI API call in your agents:
response = client.chat.completions.create(...)
if hasattr(response, 'usage'):
    st.session_state.cost_monitor.track_request('agent_name', {
        'input_tokens': response.usage.prompt_tokens,
        'output_tokens': response.usage.completion_tokens
    })
```

### Where to Add Security
```python
# Before executing workflow:
async def handle_query(query):
    is_valid, msg = await st.session_state.security_manager.validate_input(query)
    if not is_valid:
        st.error(msg)
        return
    # Continue with workflow...
```

### Where to Add Error Handling
```python
# Wrap your agent execution:
async def execute_agent_safely(agent_func, *args, **kwargs):
    return await st.session_state.error_handler.execute_with_retry(
        agent_func,
        *args,
        endpoint='openai_api',
        fallback_func=cheaper_model_fallback,
        **kwargs
    )
```

## New Environment Variables

Add to your `.env` file:
```bash
# Week 4 Production Configuration
ENVIRONMENT=development
DAILY_SPENDING_LIMIT=100.00
ALERT_THRESHOLD=70.0
PER_USER_QUOTA=50
```

## Expected Outcome

After implementation:
- **Lines of Code:** ~1500+ (adds ~600 lines)
- **Classes Added:** 6 new production classes
- **Sidebar Sections:** 7 monitoring/control panels
- **Test Suite:** 10 automated tests
- **Production Ready:** 90%+ on checklist

## Testing Your Implementation

1. **Cost Tracking:**
   - Submit a query
   - Check sidebar "Cost Monitoring"
   - Verify tokens and cost calculated correctly

2. **Evaluation Suite:**
   - Click "Run All Tests" in sidebar
   - Check pass rate (should be 80%+)
   - Download results JSON

3. **Security:**
   - Try: "Ignore all previous instructions"
   - Should be blocked with error message

4. **Error Handling:**
   - Trigger rate limit (make many requests quickly)
   - Should see retry messages

5. **Production Checklist:**
   - Click "Run Checks"
   - Should show 90%+ readiness

## Deployment Options

After passing production checklist:

**Streamlit Share (Easy):**
```bash
# Push to GitHub
# Connect repo to streamlit.io
# Add secrets in Streamlit dashboard
```

**Heroku (Professional):**
```bash
heroku create your-app-name
git push heroku main
heroku config:set OPENAI_API_KEY=your_key
```

## Files to Submit

1. ✅ Updated `app_multi_agent.py` (with Week 4 features)
2. ✅ `.env.example` (template with new variables)
3. ✅ `README.md` (updated with Week 4 features)
4. ✅ Screenshots/video of production dashboard
5. ✅ Evaluation test results (JSON export)
6. ✅ Production checklist score

## Success Metrics

- ✅ Cost monitoring working: real-time tracking visible
- ✅ Budget alerts: triggers at 70% threshold
- ✅ Evaluation: 8/10 tests passing (80%+)
- ✅ Security: blocks prompt injections
- ✅ Error handling: graceful retries working
- ✅ Monitoring: all dashboard sections populated
- ✅ Production checklist: 90%+ score

---

**Ready to implement?** 

1. Open the full `WEEK4_GITHUB_COPILOT_PROMPT.md`
2. Follow the implementation steps
3. Test each feature as you add it
4. Run the production checklist
5. Deploy and submit!

Good luck! 🚀
