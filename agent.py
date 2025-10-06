import streamlit as st
import os
import asyncio 
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Check for OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Streamlit UI
st.set_page_config(
    page_title="AI Task Generator",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Task Generator Agent")
st.write("Break down your AI Agent goals into actionable tasks!")

# Check if API key is available
if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY not found in environment variables!")
    st.info("Please add your OpenAI API key to your .env file")
    st.stop()

# Import agents after checking API key (in case it fails)
try:
    from agents import Agent, Runner
    
    # Initialize the agent
    if 'task_generator' not in st.session_state:
        st.session_state.task_generator = Agent(
            name="Task Generator",
            instructions="""You help users break down their specific LLM powered AI Agent goal into small, achievable tasks.
            For any goal, analyze it and create a structured plan with specific actionable steps.
            Each task should be concrete, time-bound when possible, and manageable.
            Organize tasks in a logical sequence with dependencies clearly marked.
            Never answer anything unrelated to AI Agents.""",
        )
    
    # Async wrapper for running the agent
    async def generate_tasks(goal):
        result = await Runner.run(st.session_state.task_generator, goal)
        return result.final_output
    
    # User input
    user_goal = st.text_area(
        "Enter your AI Agent goal:",
        placeholder="e.g., Build a customer support chatbot using GPT-4",
        height=100
    )
    
    # Generate tasks button
    if st.button("Generate Tasks", type="primary"):
        if not user_goal.strip():
            st.warning("Please enter a goal first.")
        else:
            try:
                with st.spinner("Generating tasks..."):
                    # Run the async function
                    tasks = asyncio.run(generate_tasks(user_goal))
                    st.success("Tasks generated!")
                    st.markdown("### Generated Tasks:")
                    st.markdown(tasks)
                    
                    # Store in session state for history
                    if 'task_history' not in st.session_state:
                        st.session_state.task_history = []
                    st.session_state.task_history.append({
                        'goal': user_goal,
                        'tasks': tasks
                    })
                    
            except Exception as e:
                st.error(f"Error generating tasks: {str(e)}")
                st.error("Please check your API key and try again.")
    
    # Display task history
    if 'task_history' in st.session_state and st.session_state.task_history:
        st.markdown("---")
        st.subheader("📋 Task History")
        for i, item in enumerate(reversed(st.session_state.task_history)):
            with st.expander(f"Goal {len(st.session_state.task_history)-i}: {item['goal'][:50]}..."):
                st.markdown("**Goal:**")
                st.write(item['goal'])
                st.markdown("**Generated Tasks:**")
                st.markdown(item['tasks'])
    
    # Clear history button
    if st.button("Clear History"):
        if 'task_history' in st.session_state:
            st.session_state.task_history = []
            st.success("History cleared!")

except ImportError as e:
    st.error(f"❌ Error importing agents library: {str(e)}")
    st.info("Please make sure the 'agents' library is installed in your virtual environment")
    st.code("pip install agents")
except Exception as e:
    st.error(f"❌ Unexpected error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and AI Agents")
