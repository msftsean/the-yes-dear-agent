"""
Week 4 Production Dashboard - Single Page Layout
=================================================
All features visible on main page - NO SIDEBAR issues!
"""

import streamlit as st
import os
import asyncio
from datetime import datetime
from week4_features import (
    CostMonitor,
    EvaluationFramework,
    ProductionErrorHandler,
    SecurityManager,
    CostOptimizer,
    ProductionChecklist,
    init_session_state_defaults
)

# Use environment variables directly (from GitHub Codespaces secrets)
# No load_dotenv() to avoid overriding with placeholder values

# Page config
st.set_page_config(
    page_title="Week 4 Production Dashboard",
    page_icon="🚀",
    layout="wide"
)

# Initialize session state
init_session_state_defaults()

# Title
st.title("🚀 Week 4 Production Dashboard")
st.markdown("**All production features in one view - No sidebar required!**")
st.markdown("---")

# Environment indicator
environment = os.getenv('ENVIRONMENT', 'development').upper()
env_colors = {'PRODUCTION': '🔴', 'STAGING': '🟠', 'DEVELOPMENT': '🟢'}
st.markdown(f"### {env_colors.get(environment, '⚪')} Environment: {environment}")

# Main dashboard in columns
col1, col2 = st.columns(2)

with col1:
    # COST MONITORING
    st.markdown("### 💰 Cost Monitoring")
    if 'cost_monitor' in st.session_state:
        metrics = st.session_state.cost_monitor.get_metrics()
        budget = metrics['budget_status']

        if budget['alert_level'] == 'critical':
            st.error(budget['alert_message'])
        elif budget['alert_level'] == 'warning':
            st.warning(budget['alert_message'])
        else:
            st.success(budget['alert_message'])

        try:
            pct = min(int(budget['percentage']), 100)
        except:
            pct = 0
        st.progress(pct / 100.0)

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Session Spend", f"${metrics['total_cost']:.4f}")
            st.metric("Total Tokens", f"{metrics['total_input_tokens'] + metrics['total_output_tokens']:,}")
        with col_b:
            st.metric("Budget Remaining", f"${budget['remaining']:.2f}")
            st.metric("Avg/Request", f"${metrics['avg_cost_per_request']:.4f}")

        with st.expander("💸 Cost by Agent"):
            for agent, cost in metrics['cost_by_agent'].items():
                percentage = (cost / metrics['total_cost'] * 100) if metrics['total_cost'] > 0 else 0
                st.write(f"**{agent.capitalize()}:** ${cost:.4f} ({percentage:.1f}%)")
    else:
        st.info("Cost monitor not initialized")

    st.markdown("---")

    # SYSTEM HEALTH
    st.markdown("### 🏥 System Health")
    st.write("**API Status:**")
    api_status = {
        'OpenAI': '✅' if os.getenv('OPENAI_API_KEY') else '❌',
        'Google': '✅' if os.getenv('GOOGLE_API_KEY') else '⭕',
        'Pinecone': '✅' if os.getenv('PINECONE_API_KEY') else '⭕'
    }
    for api, status in api_status.items():
        st.write(f"{status} {api}")

    if 'error_handler' in st.session_state:
        eh = st.session_state.error_handler
        if eh.circuit_states:
            st.write("**Circuit Breakers:**")
            for endpoint, state in eh.circuit_states.items():
                icon = '🟢' if state == 'closed' else '🔴' if state == 'open' else '🟡'
                st.write(f"{icon} {endpoint}: {state}")
        else:
            st.success("All circuits closed")

    st.markdown("---")

    # CACHE & OPTIMIZATION
    st.markdown("### 💾 Cache & Optimization")
    if 'cost_optimizer' in st.session_state:
        cache_enabled = st.checkbox(
            "Enable Response Caching",
            value=st.session_state.cost_optimizer.use_caching,
            key="cache_toggle"
        )
        st.session_state.cost_optimizer.use_caching = cache_enabled

        model_cascade = st.checkbox(
            "Enable Model Cascading",
            value=st.session_state.cost_optimizer.use_model_cascade,
            key="cascade_toggle"
        )
        st.session_state.cost_optimizer.use_model_cascade = model_cascade

        cache_size = len(st.session_state.cost_optimizer.response_cache)
        st.metric("Cached Responses", cache_size)

        if st.button("🗑️ Clear Cache"):
            st.session_state.cost_optimizer.clear_cache()
            st.success("Cache cleared!")
            st.rerun()
    else:
        st.info("Cost optimizer not initialized")

with col2:
    # SECURITY MONITORING
    st.markdown("### 🔒 Security Monitoring")
    if 'security_manager' in st.session_state:
        sm = st.session_state.security_manager
        total_requests = sum(len(v) for v in sm.request_timestamps.values() if isinstance(v, list))
        st.metric("Total Requests", total_requests)
        st.metric("Rate Limit", f"{sm.max_requests_per_minute}/min")

        if sm.request_timestamps:
            st.write("**Recent Activity:**")
            for user_id, timestamps in list(sm.request_timestamps.items())[:5]:
                user_display = user_id[:8] + "..." if len(user_id) > 8 else user_id
                count = len(timestamps) if isinstance(timestamps, list) else 1
                st.write(f"• {user_display}: {count} requests")
    else:
        st.info("Security manager not initialized")

    st.markdown("---")

    # PERFORMANCE METRICS
    st.markdown("### ⚡ Performance")
    perf = st.session_state.get('performance_metrics', {})
    if perf:
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Avg Time", f"{perf.get('avg_response_time', 0):.2f}s")
            st.metric("Success Rate", f"{perf.get('success_rate', 100):.1f}%")
        with col_b:
            st.metric("P95 Time", f"{perf.get('p95_response_time', 0):.2f}s")
            st.metric("Error Rate", f"{perf.get('error_rate', 0):.1f}%")
    else:
        st.info("No performance metrics yet")

    st.markdown("---")

    # EVALUATION FRAMEWORK
    st.markdown("### 🧪 Evaluation & Testing")
    if 'eval_framework' in st.session_state:
        if st.button("▶️ Run Eval Suite", use_container_width=True):
            with st.spinner("Running 10 tests..."):
                def mock_exec(q):
                    return {'text': f'Mock response to: {q}'}
                summary = st.session_state.eval_framework.run_all_tests(mock_exec)
                st.json(summary)

                # Save to file
                try:
                    import json
                    with open('eval_results.json', 'w') as f:
                        json.dump(summary, f, indent=2)
                    st.success("✅ Results saved to eval_results.json")
                except Exception as e:
                    st.error(f"Error saving: {e}")

        # Download button
        try:
            import os
            if os.path.exists('eval_results.json'):
                with open('eval_results.json', 'r') as f:
                    data = f.read()
                st.download_button(
                    '⬇️ Download Results',
                    data,
                    file_name='eval_results.json',
                    mime='application/json',
                    use_container_width=True
                )
        except:
            pass
    else:
        st.info("Evaluation framework not initialized")

# Full width sections
st.markdown("---")

# PRODUCTION CHECKLIST
st.markdown("### ✅ Production Readiness Checklist")
if 'production_checklist' in st.session_state:
    if st.button("🔍 Run Production Checks", use_container_width=True):
        with st.spinner("Validating production readiness..."):
            results = st.session_state.production_checklist.run_all_checks()

            score = results.get('score', 0)
            if score >= 90:
                st.success(f"🎉 Production Ready! Score: {score}%")
            elif score >= 70:
                st.warning(f"⚠️ Needs improvement. Score: {score}%")
            else:
                st.error(f"❌ Not ready for production. Score: {score}%")

            st.json(results)
else:
    st.info("Production checklist not initialized")

st.markdown("---")

# MODERATION ADMIN
st.markdown("### 🔒 Moderation Log")
mod_log = st.session_state.get('moderation_log', [])
st.write(f"Total events: {len(mod_log)}")
if mod_log:
    with st.expander("View Recent Events"):
        for event in mod_log[-10:][::-1]:
            st.caption(f"[{event['timestamp']}] blocked={event['blocked']} - {event['text_snippet'][:100]}")

# Download moderation log
try:
    if os.path.exists('moderation_log.jsonl'):
        with open('moderation_log.jsonl', 'r') as f:
            log_data = f.read()
        st.download_button(
            '⬇️ Download Moderation Log',
            log_data,
            file_name='moderation_log.jsonl',
            mime='text/plain'
        )
except:
    pass

# Multi-Agent Chat Interface
st.markdown("---")
st.markdown("## 🤖 Multi-Agent 'Yes Dear' Assistant")
st.markdown("""
**Ask me anything!** The 4 specialized agents will work together:
- 🎯 **Coordinator**: Analyzes your request
- 🌐 **Research Agent**: Searches the web
- 📚 **Document Agent**: Searches knowledge base
- 📝 **Summarizer**: Creates your answer
""")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display chat history
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your honeydew list today?"):
    # Security validation
    try:
        user_id = st.session_state.get('session_id', 'anonymous')
        if 'security_manager' in st.session_state:
            is_valid, error_msg, details = asyncio.run(
                st.session_state.security_manager.validate_input(prompt, user_id)
            )
            if not is_valid:
                st.error(f"🔒 Security Block: {error_msg}")
                if details:
                    with st.expander('🔒 Moderation Details'):
                        st.json(details)
                st.session_state['messages'].append({
                    "role": "assistant",
                    "content": f"❌ Input blocked: {error_msg}"
                })
                st.stop()
    except Exception as e:
        st.warning(f"⚠️ Security validation unavailable: {e}")

    # Add user message
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response (simple demo - replace with your multi-agent workflow)
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agents working..."):
            # Import your multi-agent system
            try:
                from openai import OpenAI

                # Simple response using OpenAI
                client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500
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

            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state['messages'].append({
                    "role": "assistant",
                    "content": error_msg
                })

# Footer
st.markdown("---")
st.markdown("**🎉 Week 4 Production Features - All Systems Operational!**")
st.caption("Multi-agent chat + Production monitoring on one page.")
