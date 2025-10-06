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

# Add CSS for center alignment
st.markdown("""
<style>
    .stApp > div > div > div > div {
        text-align: center;
    }
    .stSelectbox > div > div {
        text-align: center;
    }
    .stTextArea > div > div {
        text-align: center;
    }
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    .stAlert {
        text-align: center;
    }
    .stSuccess {
        text-align: center;
    }
    .stError {
        text-align: center;
    }
    .stWarning {
        text-align: center;
    }
    .stInfo {
        text-align: center;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: center !important;
    }
    p {
        text-align: center !important;
    }
    .stMarkdown {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Center the main content
col1, col2, col3 = st.columns([1, 7, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>The Yes 🤖 Dear Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Let AI break down your honeydew list!</p>", unsafe_allow_html=True)
    
    # Add couple image
    st.image("couple.png", width="stretch", caption="")

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
                
                # API parameters for task generation
                api_params = {
                    "model": "gpt-4o",  # Use available model
                    "messages": messages,
                    "max_completion_tokens": 1500,
                    "temperature": 0.7
                }
                
                response = client.chat.completions.create(**api_params)
                
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
        model_choice = st.selectbox(
            "Select Model:",
            ["gpt-4o", "gpt-4", "gpt-4-turbo"],  # Changed gpt-5 to gpt-4o (which exists)
            help="GPT-4o is the latest and most capable model for task breakdowns"
        )
        
        # Set default temperature for different models
        temperature = 0.7  # Default for GPT-4 models
        
        # Display any generated tasks from session state
        if 'current_tasks' in st.session_state and st.session_state.current_tasks:
            st.markdown("<div style='text-align: center;'>✅ <strong>Tasks generated successfully!</strong></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>📋 Generated Task Breakdown:</h3>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: left; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin: 10px 0;'>{st.session_state.current_tasks}</div>", unsafe_allow_html=True)
        
        # Generate tasks button (centered)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            generate_clicked = st.button("Generate Tasks", type="primary")
            
        if generate_clicked:
            if not user_goal.strip():
                st.warning("Please enter a goal first.")
            else:
                try:
                    with st.spinner("Analyzing your goal and generating tasks..."):
                        # Create messages for the API call
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
                        
                        # Prepare API parameters based on model
                        api_params = {
                            "model": model_choice,
                            "messages": messages,
                            "max_completion_tokens": 1500
                        }
                        
                        # Add temperature for all models (gpt-4o supports temperature)
                        api_params["temperature"] = temperature
                        
                        # Make the API call
                        response = client.chat.completions.create(**api_params)
                        
                        # Extract the generated tasks
                        tasks = response.choices[0].message.content
                        
                        # Check if tasks were generated
                        if tasks and tasks.strip():
                            # Store current tasks for display
                            st.session_state.current_tasks = tasks
                            
                            # Store in session state for history
                            if 'task_history' not in st.session_state:
                                st.session_state.task_history = []
                            st.session_state.task_history.append({
                                'goal': user_goal,
                                'tasks': tasks,
                                'model': model_choice
                            })
                            
                            # Trigger rerun to display the tasks
                            st.rerun()
                        else:
                            st.error("❌ No tasks were generated. The response was empty.")
                        
                        # Show token usage if available
                        if hasattr(response, 'usage'):
                            with st.expander("📊 Token Usage"):
                                st.write(f"**Prompt tokens:** {response.usage.prompt_tokens}")
                                st.write(f"**Completion tokens:** {response.usage.completion_tokens}")
                                st.write(f"**Total tokens:** {response.usage.total_tokens}")
                        
                except Exception as e:
                    st.error(f"❌ Error generating tasks: {str(e)}")
                    st.error("Please check your API key and try again.")
        
        # Display task history
        if 'task_history' in st.session_state and st.session_state.task_history:
            st.markdown("---")
            st.subheader("📋 Task History")
            for i, item in enumerate(reversed(st.session_state.task_history)):
                with st.expander(f"Goal {len(st.session_state.task_history)-i}: {item['goal'][:50]}..."):
                    st.markdown("**Goal:**")
                    st.write(item['goal'])
                    st.markdown(f"**Model Used:** {item['model']}")
                    st.markdown("**Generated Tasks:**")
                    st.markdown(f"<div style='text-align: left; padding: 15px; background-color: #f8f9fa; border-radius: 8px; margin: 5px 0;'>{item['tasks']}</div>", unsafe_allow_html=True)
        
        # Clear history button (centered)
        col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
        with col_clear2:
            clear_clicked = st.button("Clear History")
        
        if clear_clicked:
            if 'task_history' in st.session_state:
                st.session_state.task_history = []
                st.markdown("<div style='text-align: center; color: green;'>✅ History cleared!</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error initializing OpenAI client: {str(e)}")
        st.info("Please check your API key in the .env file")

    # Footer
    st.markdown("<hr style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Built with Streamlit and OpenAI API</p>", unsafe_allow_html=True)