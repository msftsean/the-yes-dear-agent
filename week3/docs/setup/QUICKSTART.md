# 🚀 Quick Start Guide - Week 3 Multi-Agent System

## Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd /c/Users/segayle/repos/lo
pip install agent-framework-azure-ai --pre
pip install streamlit openai python-dotenv
```

### Step 2: Set Environment Variable
```bash
# Windows
set OPENAI_API_KEY=your-key-here

# Or add to .env file in project root
echo OPENAI_API_KEY=your-key-here > .env
```

### Step 3: Run the App
```bash
cd week3
streamlit run app_multi_agent.py
```

### Step 4: Test the System
1. Browser opens to `http://localhost:8501`
2. Leave "Use Real APIs" **unchecked** (demo mode)
3. Type: `"Search for information about AI agents"`
4. Watch the 4 agents execute in sequence!

## ✅ Verification Checklist

After starting the app, verify:
- [ ] Streamlit UI loads successfully
- [ ] Sidebar shows "🤖 Multi-Agent System"
- [ ] All 4 agents listed in Architecture section
- [ ] Demo mode is active (🟢 icon)
- [ ] Chat input is ready

## 🎯 Sample Test Queries

### Test 1: Basic Research
```
Search for the latest developments in electric vehicles
```
**Expected:** Coordinator → Research → Document → Summarizer

### Test 2: Document Focus
```
Find information in my documents about project requirements
```
**Expected:** All agents execute, document search emphasized

### Test 3: Error Handling
1. Toggle "Use Real APIs" ON (without configuring keys)
2. Submit any query
3. **Expected:** Automatic fallback to mock data, no errors

## 🐛 Quick Troubleshooting

**Problem:** "Module not found: agent_framework"
```bash
pip install agent-framework-azure-ai --pre
```

**Problem:** "OpenAI API key not found"
```bash
# Check .env file exists and has:
OPENAI_API_KEY=sk-...
```

**Problem:** App won't start
```bash
# Check Python version (need 3.12+)
python --version

# Reinstall streamlit
pip install --upgrade streamlit
```

## 📊 Success Criteria

You're ready for demo when:
- ✅ App starts without errors
- ✅ Test query completes successfully
- ✅ All 4 agents show in workflow viewer
- ✅ Shared memory logs agent activity
- ✅ Error handling works (fallback test)

## 🎬 Ready to Demo!

Once verified, you're ready to present. See `DEMO_SCRIPT.md` for full presentation guide.

---

**Total setup time:** 5 minutes
**Prerequisites:** Python 3.12+, OpenAI API key
**Status:** ✅ Ready for Week 3 submission
