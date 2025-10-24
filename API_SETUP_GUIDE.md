# 🔑 API Setup Guide

Complete guide for obtaining and configuring all API keys for the Yes Dear Assistant.

---

## Required APIs

### 1. OpenAI API (REQUIRED)

The application **will not work** without an OpenAI API key.

#### Getting Your OpenAI API Key

1. **Create OpenAI Account**
   - Go to https://platform.openai.com/signup
   - Sign up with email or Google/Microsoft account
   - Verify your email address

2. **Add Payment Method**
   - Go to https://platform.openai.com/account/billing
   - Click "Add payment method"
   - Add a credit/debit card
   - Recommended: Set up usage limits to control costs

3. **Create API Key**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name it (e.g., "Yes Dear Assistant")
   - **IMPORTANT**: Copy the key immediately - you won't see it again!
   - Key format: `sk-proj-...` (starts with sk-proj or sk-)

4. **Add to .env File**
   ```bash
   OPENAI_API_KEY=sk-proj-your_actual_key_here
   ```

#### Cost Estimates

- **GPT-4o Pricing** (main model used):
  - Input: $5.00 per 1M tokens
  - Output: $15.00 per 1M tokens

- **Typical Usage**:
  - Simple question: ~$0.01-0.02
  - Complex research: ~$0.05-0.10
  - With search tools: ~$0.10-0.25

- **Budget Recommendations**:
  - Testing/Learning: $10-20/month
  - Regular Use: $20-50/month
  - Heavy Use: $50-100/month

#### Set Usage Limits (Recommended)

1. Go to https://platform.openai.com/account/limits
2. Set "Hard limit" (e.g., $50/month)
3. Set "Soft limit" for email alerts (e.g., $30/month)
4. This prevents unexpected charges

---

## Optional APIs

These APIs enhance functionality but the app works fine without them using mock data.

### 2. Google Custom Search API (OPTIONAL)

Enables real web search functionality. Without it, the app uses mock search results.

#### Step-by-Step Setup

**Part A: Get Google Cloud API Key**

1. **Create Google Cloud Account**
   - Go to https://console.cloud.google.com/
   - Sign in with Google account
   - Accept terms of service

2. **Create a New Project**
   - Click "Select a project" → "New Project"
   - Project name: "Yes Dear Assistant" (or anything you like)
   - Click "Create"

3. **Enable Custom Search API**
   - Go to https://console.cloud.google.com/apis/library
   - Search for "Custom Search API"
   - Click on it → Click "Enable"

4. **Create API Credentials**
   - Go to https://console.cloud.google.com/apis/credentials
   - Click "Create Credentials" → "API key"
   - Copy the API key (starts with `AIza...`)
   - Click "Restrict Key" (recommended):
     - Under "API restrictions", select "Restrict key"
     - Choose "Custom Search API"
     - Click "Save"

**Part B: Create Custom Search Engine**

1. **Go to Custom Search Console**
   - Visit https://programmablesearchengine.google.com/
   - Click "Get Started" or "Add"

2. **Create Search Engine**
   - Name: "Yes Dear Web Search"
   - What to search: Select "Search the entire web"
   - Click "Create"

3. **Get Search Engine ID**
   - Click on your new search engine
   - Click "Setup" in the left menu
   - Find "Search engine ID" (looks like: `a1b2c3d4e5f6g7h8i`)
   - Copy this ID

4. **Add to .env File**
   ```bash
   GOOGLE_API_KEY=AIza_your_actual_key_here
   GOOGLE_CSE_ID=your_search_engine_id_here
   ```

#### Free Tier Limits

- **100 searches per day** (free)
- If you need more: $5 per 1,000 queries ($0.005 per query)

---

### 3. Pinecone Vector Database (OPTIONAL)

Enables document search functionality. Without it, the app uses mock document results.

#### Getting Your Pinecone API Key

1. **Create Pinecone Account**
   - Go to https://www.pinecone.io/
   - Click "Sign Up Free"
   - Sign up with email or GitHub/Google

2. **Create a Project**
   - Once logged in, you'll be prompted to create a project
   - Project name: "yes-dear-assistant"
   - Cloud provider: AWS
   - Region: us-east-1

3. **Get API Key**
   - In the Pinecone console, go to "API Keys"
   - Copy your API key (starts with `pcsk_...`)
   - Or click "Create API Key" if you need a new one

4. **Add to .env File**
   ```bash
   PINECONE_API_KEY=pcsk_your_actual_key_here
   PINECONE_ENVIRONMENT=us-east-1
   ```

5. **Seed Sample Data (Optional)**
   ```bash
   # After configuring the API key
   python scripts/seed_data.py
   ```
   This will create a `company-docs` index and populate it with sample company policy documents.

#### Free Tier

- **Starter Plan (Free)**:
  - 1 pod
  - 100K vectors
  - Perfect for testing and learning
  - No credit card required

---

## Configuration Summary

After obtaining your API keys, your `.env` file should look like this:

```bash
# =============================================================================
# API Keys
# =============================================================================

# REQUIRED - OpenAI API key
OPENAI_API_KEY=sk-proj-abc123...your_actual_openai_key

# OPTIONAL - Google Custom Search (for real web search)
GOOGLE_API_KEY=AIzaSyC...your_actual_google_key
GOOGLE_CSE_ID=a1b2c3d...your_actual_cse_id

# OPTIONAL - Pinecone (for document search)
PINECONE_API_KEY=pcsk_2fZ...your_actual_pinecone_key
PINECONE_ENVIRONMENT=us-east-1

# =============================================================================
# Production Settings (can leave as defaults)
# =============================================================================

ENVIRONMENT=development
DAILY_SPENDING_LIMIT=100.00
ALERT_THRESHOLD=70.0
MAX_REQUESTS_PER_MINUTE=10
CACHE_TTL_SECONDS=3600
```

---

## Testing Your Setup

After adding your API keys, test the configuration:

```bash
# Activate virtual environment
source env/bin/activate  # Mac/Linux
# or
env\Scripts\activate  # Windows

# Run the app
streamlit run app.py
```

Then in the app:
1. Try asking a simple question
2. If it responds, OpenAI is working! ✅
3. Try web search (enable "Real APIs" in sidebar)
4. Try document search (if you seeded data)

---

## Troubleshooting

### OpenAI API Issues

**Error: "Invalid API key"**
- Check that you copied the entire key
- Key should start with `sk-proj-` or `sk-`
- No extra spaces before/after the key
- Make sure you saved the .env file

**Error: "You exceeded your current quota"**
- You need to add a payment method in OpenAI dashboard
- Or you've hit your spending limit
- Check https://platform.openai.com/account/usage

**Error: "Rate limit exceeded"**
- You're making too many requests too quickly
- Wait a minute and try again
- Consider upgrading your OpenAI plan

### Google Search Issues

**Error: "API key not valid"**
- Make sure you enabled the Custom Search API
- Check API key restrictions (should allow Custom Search API)
- Verify the key in Google Cloud Console

**Error: "Invalid search engine ID"**
- Double-check the Search Engine ID from Programmable Search Console
- Make sure the search engine is configured to search the entire web

**No results returned**
- You might have hit the 100 queries/day free limit
- Check your quota in Google Cloud Console

### Pinecone Issues

**Error: "Invalid API key"**
- Verify you copied the correct key from Pinecone console
- Key should start with `pcsk_`

**Error: "Index not found"**
- Run the seed script: `python scripts/seed_data.py`
- Or the index name doesn't match (should be "company-docs")

**Seeding fails**
- Make sure both OpenAI and Pinecone keys are configured
- Check your internet connection
- Verify you have credits in your OpenAI account

---

## Security Best Practices

1. **Never commit .env file to git**
   - Already in .gitignore
   - Always double-check before committing

2. **Use separate keys for different projects**
   - Create project-specific API keys
   - Easier to track usage and revoke if needed

3. **Set spending limits**
   - OpenAI: Set hard limits in dashboard
   - Google: Set daily quotas
   - Monitor usage regularly

4. **Rotate keys periodically**
   - Change API keys every few months
   - Immediately if you suspect compromise

5. **Don't share your keys**
   - Each person should use their own keys
   - Never post keys in Discord/Slack/email

---

## Cost Monitoring

### In the Application

The app includes built-in cost monitoring:
- View in the **Production Dashboard** tab
- See real-time spending vs. budget
- Track cost by agent/feature
- Get alerts at 70% of daily limit

### External Monitoring

**OpenAI Dashboard:**
- https://platform.openai.com/account/usage
- See detailed usage breakdown
- Download usage reports
- Set up email alerts

**Google Cloud Console:**
- https://console.cloud.google.com/apis/dashboard
- Monitor API quota usage
- Set up billing alerts

**Pinecone Console:**
- https://app.pinecone.io/
- Check pod usage
- Monitor vector counts

---

## Getting Help

- **OpenAI Support**: https://help.openai.com/
- **Google Cloud Support**: https://cloud.google.com/support
- **Pinecone Support**: https://support.pinecone.io/

- **App Issues**: Create an issue in the GitHub repo
- **Bootcamp Questions**: Ask in your bootcamp Slack/Discord

---

## Quick Reference

| Service | Sign Up URL | API Key Format | Free Tier |
|---------|-------------|----------------|-----------|
| OpenAI | platform.openai.com | `sk-proj-...` | $5 credit (new accounts) |
| Google Search | cloud.google.com | `AIza...` | 100 queries/day |
| Pinecone | pinecone.io | `pcsk_...` | 100K vectors |

---

**Next Steps:**
1. Get your OpenAI API key (required)
2. Add it to `.env` file
3. Run `streamlit run app.py`
4. Optional: Add Google and Pinecone keys later for enhanced features

Happy building! 🚀
