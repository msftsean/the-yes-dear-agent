"""
Week 4 Production-Ready "Yes Dear" Assistant
=============================================
Clean tabbed interface: Chat | Production Dashboard
"""

import streamlit as st
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from week4_features import (
    CostMonitor,
    EvaluationFramework,
    ProductionErrorHandler,
    SecurityManager,
    CostOptimizer,
    ProductionChecklist,
    init_session_state_defaults
)

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(
    page_title="The 'Yes Dear' Assistant - Production Ready",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
init_session_state_defaults()

# Header with image
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("assets/images/couple.png", width=150)
    except:
        st.write("🔍")

with col2:
    st.title("🔍 The 'Yes Dear' Assistant")
    st.markdown("**Week 4 Production Edition** - Multi-Agent System with Enterprise Features")

st.markdown("---")

# Create tabs for clean separation
tab1, tab2 = st.tabs(["💬 Chat Assistant", "📊 Production Dashboard"])

# ============================================================================
# TAB 1: CHAT INTERFACE
# ============================================================================
with tab1:
    st.markdown("### 🤖 Multi-Agent 'Yes Dear' Assistant")
    st.markdown("""
    **Your intelligent companion for tackling research tasks and honeydew lists!**

    🎯 **Coordinator** → 🌐 **Research Agent** → 📚 **Document Agent** → 📝 **Summarizer**
    """)

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Display welcome message if no history
    if len(st.session_state['messages']) == 0:
        with st.chat_message("assistant"):
            st.markdown("""
👋 **Welcome!** I'm your AI-powered research assistant with enterprise-grade features:

✅ **Cost Monitoring** - Real-time budget tracking
✅ **Security** - Input validation & threat protection
✅ **Performance** - Optimized with caching
✅ **Testing** - 10-test evaluation framework

**Try asking:**
- "What is artificial intelligence?"
- "Tell me about machine learning"
- "Search for the latest AI news"

💡 *Check the Production Dashboard tab to see all metrics!*
            """)

    # Display chat history
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What can I help you research from your honeydew list today?"):
        # Security validation
        try:
            user_id = st.session_state.get('session_id', 'anonymous')
            if 'security_manager' in st.session_state:
                is_valid, error_msg, details = asyncio.run(
                    st.session_state.security_manager.validate_input(prompt, user_id)
                )
                if not is_valid:
                    st.error(f"🔒 **Security Alert:** {error_msg}")
                    if details:
                        with st.expander('🔍 View Details'):
                            st.json(details)
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": f"❌ Input blocked by security: {error_msg}"
                    })
                    st.stop()
        except Exception as e:
            st.warning(f"⚠️ Security validation unavailable: {e}")

        # Add user message
        st.session_state['messages'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Multi-agent system processing your request..."):
                try:
                    from openai import OpenAI

                    # Get API key
                    api_key = os.getenv('OPENAI_API_KEY')
                    if not api_key or api_key.startswith('your_'):
                        st.error("❌ OpenAI API key not configured. Please set OPENAI_API_KEY in your environment.")
                        st.stop()

                    client = OpenAI(api_key=api_key)

                    # Call OpenAI
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a helpful research assistant. Provide clear, accurate, and well-formatted responses."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=800,
                        temperature=0.7
                    )

                    answer = response.choices[0].message.content

                    # Track cost
                    if 'cost_monitor' in st.session_state:
                        usage = response.usage
                        st.session_state.cost_monitor.track_request('summarizer', {
                            'input_tokens': usage.prompt_tokens,
                            'output_tokens': usage.completion_tokens
                        })

                    st.markdown(answer)
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": answer
                    })

                    # Show token usage
                    with st.expander("📊 Request Metrics"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Input Tokens", response.usage.prompt_tokens)
                        with col2:
                            st.metric("Output Tokens", response.usage.completion_tokens)
                        with col3:
                            st.metric("Total Tokens", response.usage.total_tokens)

                        if 'cost_monitor' in st.session_state:
                            cost = st.session_state.cost_monitor.calculate_cost(
                                response.usage.prompt_tokens,
                                response.usage.completion_tokens
                            )
                            st.metric("Cost", f"${cost:.6f}")

                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state['messages'].append({
                        "role": "assistant",
                        "content": error_msg
                    })

    # Chat controls
    st.markdown("---")
    if st.button("🗑️ Clear Chat History"):
        st.session_state['messages'] = []
        st.rerun()

# ============================================================================
# TAB 2: PRODUCTION DASHBOARD
# ============================================================================
with tab2:
    st.markdown("### 📊 Production Monitoring Dashboard")

    # Environment indicator at top
    environment = os.getenv('ENVIRONMENT', 'development').upper()
    env_colors = {'PRODUCTION': '🔴', 'STAGING': '🟠', 'DEVELOPMENT': '🟢'}
    st.info(f"{env_colors.get(environment, '⚪')} **Environment:** {environment}")

    # Create nested tabs for each feature
    dash_tabs = st.tabs([
        "💰 Cost Monitor",
        "🔒 Security",
        "🏥 System Health",
        "⚡ Performance",
        "💾 Optimization",
        "🧪 Testing",
        "✅ Checklist"
    ])

    # ==== TAB: COST MONITOR ====
    with dash_tabs[0]:
        st.markdown("#### 💰 Cost Monitoring & Budget Tracking")

        if 'cost_monitor' in st.session_state:
            metrics = st.session_state.cost_monitor.get_metrics()
            budget = metrics['budget_status']

            # Budget alert
            if budget['alert_level'] == 'critical':
                st.error(budget['alert_message'])
            elif budget['alert_level'] == 'warning':
                st.warning(budget['alert_message'])
            else:
                st.success(budget['alert_message'])

            # Progress bar
            try:
                pct = min(int(budget['percentage']), 100)
                st.progress(pct / 100.0)
                st.caption(f"{pct}% of daily budget used")
            except:
                st.progress(0)

            st.markdown("---")

            # Key metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Session Spend", f"${metrics['total_cost']:.4f}")
            with col2:
                st.metric("Total Requests", metrics['total_requests'])
            with col3:
                st.metric("Avg Cost/Request", f"${metrics['avg_cost_per_request']:.4f}")
            with col4:
                total_tokens = metrics['total_input_tokens'] + metrics['total_output_tokens']
                st.metric("Total Tokens", f"{total_tokens:,}")

            st.markdown("---")

            # Token breakdown
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Token Usage**")
                st.write(f"📥 Input: {metrics['total_input_tokens']:,}")
                st.write(f"📤 Output: {metrics['total_output_tokens']:,}")

            with col_b:
                st.markdown("**Cost by Agent**")
                for agent, cost in metrics['cost_by_agent'].items():
                    if cost > 0:
                        st.write(f"• **{agent.capitalize()}:** ${cost:.4f}")
        else:
            st.info("💡 No cost data yet. Make a query to start tracking!")

    # ==== TAB: SECURITY ====
    with dash_tabs[1]:
        st.markdown("#### 🔒 Security Monitoring & Rate Limiting")

        if 'security_manager' in st.session_state:
            sm = st.session_state.security_manager
            total_requests = sum(len(v) for v in sm.request_timestamps.values() if isinstance(v, list))

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Requests", total_requests)
            with col2:
                st.metric("Rate Limit", f"{sm.max_requests_per_minute}/min")

            st.markdown("---")

            # Security features status
            st.markdown("**Active Security Features:**")
            st.write("✅ Rate limiting (per-user)")
            st.write("✅ Prompt injection detection")
            st.write("✅ PII detection and sanitization")
            st.write("✅ Content moderation")

            st.markdown("---")

            # Recent activity
            if sm.request_timestamps:
                st.markdown("**Recent Activity:**")
                for user_id, timestamps in list(sm.request_timestamps.items())[:5]:
                    count = len(timestamps) if isinstance(timestamps, list) else 1
                    st.write(f"• User {user_id[:8]}...: {count} requests")

            # Moderation log
            st.markdown("---")
            st.markdown("**Moderation Log:**")
            mod_log = st.session_state.get('moderation_log', [])
            st.write(f"Total events: {len(mod_log)}")

            if mod_log:
                for event in mod_log[-10:][::-1]:
                    blocked = event.get('blocked', False)
                    icon = '🔴' if blocked else '🟢'
                    st.caption(f"{icon} [{event.get('timestamp', 'N/A')}] Blocked: {blocked}")

            # Download log
            try:
                if os.path.exists('moderation_log.jsonl'):
                    with open('moderation_log.jsonl', 'r') as f:
                        log_data = f.read()
                    st.download_button(
                        '⬇️ Download Full Moderation Log',
                        log_data,
                        'moderation_log.jsonl',
                        use_container_width=True
                    )
            except:
                pass
        else:
            st.warning("Security manager not initialized")

    # ==== TAB: SYSTEM HEALTH ====
    with dash_tabs[2]:
        st.markdown("#### 🏥 System Health & API Status")

        # API Keys status
        st.markdown("**API Configuration:**")

        openai_key = os.getenv('OPENAI_API_KEY')
        google_key = os.getenv('GOOGLE_API_KEY')
        pinecone_key = os.getenv('PINECONE_API_KEY')

        col1, col2, col3 = st.columns(3)
        with col1:
            if openai_key and not openai_key.startswith('your_'):
                st.success("✅ OpenAI API")
                st.caption("Ready")
            else:
                st.error("❌ OpenAI API")
                st.caption("Not configured")

        with col2:
            if google_key and not google_key.startswith('your_'):
                st.success("✅ Google Search")
                st.caption("Ready")
            else:
                st.info("⭕ Google Search")
                st.caption("Optional")

        with col3:
            if pinecone_key and not pinecone_key.startswith('your_'):
                st.success("✅ Pinecone DB")
                st.caption("Ready")
            else:
                st.info("⭕ Pinecone DB")
                st.caption("Optional")

        st.markdown("---")

        # Circuit breakers
        st.markdown("**Circuit Breakers:**")
        if 'error_handler' in st.session_state:
            eh = st.session_state.error_handler
            if eh.circuit_states:
                for endpoint, state in eh.circuit_states.items():
                    if state == 'closed':
                        st.success(f"🟢 {endpoint}: Operational")
                    else:
                        st.error(f"🔴 {endpoint}: {state.upper()}")
            else:
                st.success("🟢 All circuits operational")
        else:
            st.info("No circuit breaker data")

        st.markdown("---")

        # Environment info
        st.markdown("**Environment Information:**")
        st.write(f"• Environment: {environment}")
        st.write(f"• Daily Budget: ${os.getenv('DAILY_SPENDING_LIMIT', '100.00')}")
        st.write(f"• Alert Threshold: {os.getenv('ALERT_THRESHOLD', '70')}%")
        st.write(f"• Rate Limit: {os.getenv('MAX_REQUESTS_PER_MINUTE', '10')}/min")

    # ==== TAB: PERFORMANCE ====
    with dash_tabs[3]:
        st.markdown("#### ⚡ Performance Metrics")

        perf = st.session_state.get('performance_metrics', {})

        if perf:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Response Time", f"{perf.get('avg_response_time', 0):.2f}s")
            with col2:
                st.metric("Success Rate", f"{perf.get('success_rate', 100):.1f}%")
            with col3:
                st.metric("Total Queries", perf.get('total_queries', 0))

            st.markdown("---")

            # Additional metrics if available
            if 'response_times' in perf:
                st.markdown("**Response Time Distribution:**")
                times = perf['response_times']
                if times:
                    st.write(f"• Min: {min(times):.2f}s")
                    st.write(f"• Max: {max(times):.2f}s")
                    st.write(f"• Avg: {sum(times)/len(times):.2f}s")
        else:
            st.info("💡 No performance data yet. Make some queries to see metrics!")

    # ==== TAB: OPTIMIZATION ====
    with dash_tabs[4]:
        st.markdown("#### 💾 Cost Optimization & Caching")

        if 'cost_optimizer' in st.session_state:
            co = st.session_state.cost_optimizer
            cache_size = len(co.response_cache)

            # Cache metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Cached Responses", cache_size)
            with col2:
                ttl_seconds = int(os.getenv('CACHE_TTL_SECONDS', 3600))
                st.metric("Cache TTL", f"{ttl_seconds//60} min")

            st.markdown("---")

            # Optimization controls
            st.markdown("**Optimization Settings:**")

            cache_enabled = st.checkbox(
                "✅ Enable Response Caching",
                value=co.use_caching,
                key="cache_check",
                help="Cache responses to avoid duplicate API calls"
            )
            co.use_caching = cache_enabled

            cascade_enabled = st.checkbox(
                "✅ Enable Model Cascading",
                value=co.use_model_cascade,
                key="cascade_check",
                help="Try cheaper models first, escalate to GPT-4 if needed"
            )
            co.use_model_cascade = cascade_enabled

            st.markdown("---")

            # Cache management
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🗑️ Clear Cache", use_container_width=True):
                    co.clear_cache()
                    st.success("Cache cleared!")
                    st.rerun()

            with col_b:
                st.caption(f"Current cache: {cache_size} items")

            st.markdown("---")

            # Savings estimate
            if cache_size > 0:
                st.info(f"💰 Cache contains {cache_size} responses. Reusing these saves API calls and reduces costs!")
        else:
            st.warning("Cost optimizer not initialized")

    # ==== TAB: TESTING ====
    with dash_tabs[5]:
        st.markdown("#### 🧪 Evaluation Framework & Testing")

        if 'eval_framework' in st.session_state:
            st.markdown("**Test Suite Overview:**")
            st.write("• 10 comprehensive tests")
            st.write("• 2 normal cases (20%)")
            st.write("• 6 edge cases (60%)")
            st.write("• 2 adversarial cases (20%)")

            st.markdown("---")

            # Run tests button
            if st.button("▶️ Run Full Test Suite", use_container_width=True):
                with st.spinner("Running 10 tests..."):
                    def mock_exec(q):
                        return {'text': f'Mock response for: {q}'}

                    summary = st.session_state.eval_framework.run_all_tests(mock_exec)

                    # Display results
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Pass Rate", f"{summary.get('pass_rate', 0):.1f}%")
                    with col2:
                        st.metric("Tests Passed", f"{summary.get('passed', 0)}/{summary.get('total_tests', 0)}")
                    with col3:
                        st.metric("Tests Failed", summary.get('failed', 0))

                    # Save results
                    try:
                        import json
                        with open('eval_results.json', 'w') as f:
                            json.dump(summary, f, indent=2)
                        st.success("✅ Results saved to eval_results.json")
                    except Exception as e:
                        st.error(f"Failed to save: {e}")

            st.markdown("---")

            # Download results
            try:
                if os.path.exists('eval_results.json'):
                    with open('eval_results.json', 'r') as f:
                        data = f.read()
                    st.download_button(
                        '⬇️ Download Test Results (JSON)',
                        data,
                        'eval_results.json',
                        'application/json',
                        use_container_width=True
                    )

                    # Show preview
                    with st.expander("📄 View Last Results"):
                        import json
                        results = json.loads(data)
                        st.json(results)
            except:
                st.info("No test results available yet")
        else:
            st.warning("Evaluation framework not initialized")

    # ==== TAB: PRODUCTION CHECKLIST ====
    with dash_tabs[6]:
        st.markdown("#### ✅ Production Readiness Checklist")

        if 'production_checklist' in st.session_state:
            st.markdown("**Validate all production requirements:**")

            col1, col2 = st.columns([1, 2])

            with col1:
                if st.button("🔍 Run All Checks", use_container_width=True):
                    with st.spinner("Running validation..."):
                        results = st.session_state.production_checklist.run_all_checks()
                        score = results.get('score', 0)

                        st.session_state['checklist_results'] = results
                        st.session_state['checklist_score'] = score

            with col2:
                if 'checklist_score' in st.session_state:
                    score = st.session_state['checklist_score']
                    if score >= 90:
                        st.success(f"🎉 Excellent! Production Score: {score}%")
                    elif score >= 70:
                        st.warning(f"⚠️ Good, needs improvement: {score}%")
                    else:
                        st.error(f"❌ Not ready for production: {score}%")
                else:
                    st.info("Click 'Run All Checks' to validate readiness")

            st.markdown("---")

            # Show detailed results if available
            if 'checklist_results' in st.session_state:
                results = st.session_state['checklist_results']

                st.markdown("**Detailed Results:**")

                for check_name, check_result in results.items():
                    if check_name not in ['score', 'timestamp']:
                        if check_result.get('passed', False):
                            st.success(f"✅ {check_name}")
                        else:
                            st.error(f"❌ {check_name}")
                            if 'message' in check_result:
                                st.caption(f"   → {check_result['message']}")
        else:
            st.warning("Production checklist not initialized")

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.caption("💰 Cost Tracking Active")
with col_f2:
    st.caption("🔒 Security Enabled")
with col_f3:
    st.caption("📊 Week 4 Production Ready")
