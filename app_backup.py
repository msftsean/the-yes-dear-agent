import streamlit as st
import os
from openai import OpenAI
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

# Center the main content
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🤖 AI Task Generator Agent")
    st.write("Break down your AI Agent goals into actionable tasks!")

    # Check if API key is available
    if not OPENAI_API_KEY:
        st.error("❌ OPENAI_API_KEY not found in environment variables!")
        st.info("Please add your OpenAI API key to your .env file")
        st.stop()

    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Function to generate tasks using OpenAI
        def generate_tasks(goal):
            try:
                messages = [
                    {
                        "role": "system", 
                        "content": """You are a task breakdown specialist that helps users break down their specific LLM powered AI Agent goals into small, achievable tasks.
                        For any goal, analyze it and create a structured plan with specific actionable steps.
                        Each task should be concrete, time-bound when possible, and manageable.
                        Organize tasks in a logical sequence with dependencies clearly marked.
                        Format your response in clear markdown with numbered tasks and subtasks.
                        Never answer anything unrelated to AI Agents."""
                    },
                    {
                        "role": "user", 
                        "content": f"Please break down this AI Agent goal into specific, actionable tasks:\n\n{goal}\n\nProvide a structured plan with clear steps, timelines, and dependencies."
                    }
                ]
                
                response = client.chat.completions.create(
                    model="gpt-5",  # Default fallback
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1500
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                return f"Error generating tasks: {str(e)}"
        
        # User input
        user_goal = st.text_area(
            "Enter your AI Agent goal:",
            placeholder="e.g., Build a customer support chatbot using GPT-5",
            height=100
        )
        
        # Model selection
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            model_choice = st.selectbox(
                "Select Model:",
                ["gpt-5", "gpt-4", "gpt-4-turbo"],
                help="GPT-5 is the latest and most capable model for task breakdowns"
            )
        
        with subcol2:
            temperature = st.slider(
                "Creativity Level:",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make responses more creative"
            )
        
        
        # Generate tasks button
        if st.button("Generate Tasks", type="primary"):
            if not user_goal.strip():
                st.warning("Please enter a goal first.")
            else:
                try:
                    with st.spinner("Analyzing your goal and generating tasks..."):
                    # Update the model choice
                    messages = [
                        {
                            "role": "system", 
                            "content": """You are a task breakdown specialist that helps users break down their specific LLM powered AI Agent goals into small, achievable tasks.
                            For any goal, analyze it and create a structured plan with specific actionable steps.
                            Each task should be concrete, time-bound when possible, and manageable.
                            Organize tasks in a logical sequence with dependencies clearly marked.
                            Format your response in clear markdown with numbered tasks and subtasks.
                            Never answer anything unrelated to AI Agents."""
                        },
                        {
                            "role": "user", 
                            "content": f"Please break down this AI Agent goal into specific, actionable tasks:\n\n{user_goal}\n\nProvide a structured plan with clear steps, timelines, and dependencies."
                        }
                    ]
                    
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=1500
                    )
                    
                    tasks = response.choices[0].message.content
                    
                    st.success("Tasks generated successfully!")
                    st.markdown("### 📋 Generated Task Breakdown:")
                    st.markdown(tasks)
                    
                    # Store in session state for history
                    if 'task_history' not in st.session_state:
                        st.session_state.task_history = []
                    st.session_state.task_history.append({
                        'goal': user_goal,
                        'tasks': tasks,
                        'model': model_choice,
                        'temperature': temperature
                    })
                    
                    # Show token usage if available
                    if hasattr(response, 'usage'):
                        with st.expander("Token Usage"):
                            st.write(f"Prompt tokens: {response.usage.prompt_tokens}")
                            st.write(f"Completion tokens: {response.usage.completion_tokens}")
                            st.write(f"Total tokens: {response.usage.total_tokens}")
                    
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
                st.markdown(f"**Model Used:** {item['model']} | **Temperature:** {item['temperature']}")
                st.markdown("**Generated Tasks:**")
                st.markdown(item['tasks'])
    
    # Clear history button
    if st.button("Clear History"):
        if 'task_history' in st.session_state:
            st.session_state.task_history = []
            st.success("History cleared!")

except Exception as e:
    st.error(f"❌ Error initializing OpenAI client: {str(e)}")
    st.info("Please check your API key in the .env file")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and OpenAI API")