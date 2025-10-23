import os
import asyncio
import pandas as pd
import smtplib
import sqlite3
import streamlit as st
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, handoff, RunContextWrapper

# ============================================================================
# CONFIGURATION AND SETUP
# ============================================================================

# Load environment variables
load_dotenv(override=True)

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API Key not configured. Please add it to your .env file.")
    st.stop()

# Email Configuration
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
EMAIL_ENABLED = EMAIL_USER and EMAIL_APP_PASSWORD

# Database Configuration
DB_FILE = os.getenv("DB_FILE", "leads.db")

# Email routing configuration (update these with real addresses in production)
EMAIL_ROUTING = {
    "enterprise": EMAIL_USER,  # Replace with actual enterprise email
    "smb": EMAIL_USER,         # Replace with actual SMB email
    "individual": EMAIL_USER   # Replace with actual support email
}

# Cache for lead deduplication
LEAD_INFO_CACHE = {}
LEAD_EMAIL_CACHE = {}
EMAIL_DEDUPE_WINDOW = 300  # seconds

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def log_system_message(message):
    """Add a timestamped message to system logs."""
    if 'system_logs' not in st.session_state:
        st.session_state['system_logs'] = []
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state['system_logs'].append(f"[{timestamp}] {message}")

def extract_lead_details(conversation_history):
    """Extract lead information from conversation text."""
    if not conversation_history:
        return {"name": "Unknown", "company": "", "email": "", "phone": "", "details": ""}
    
    details = {"name": "Unknown", "company": "", "email": "", "phone": "", "details": ""}
    
    # Name extraction patterns
    name_patterns = [
        r"I'm\s+(\w+)", r"I am\s+(\w+)", r"name\s+is\s+(\w+)",
        r"this\s+is\s+(\w+)", r"Hello,?\s+(?:I'm|I am|my name is)?\s*(\w+)"
    ]
    for pattern in name_patterns:
        match = re.search(pattern, conversation_history, re.IGNORECASE)
        if match:
            details["name"] = match.group(1).strip()
            break
    
    # Company extraction
    company_patterns = [
        r"(?:at|from|with|for|work(?:ing)? (?:at|for))\s+([A-Z][A-Za-z\s]+)",
        r"([A-Z][A-Za-z\s]+)\s+(?:Company|Corporation|Inc|LLC|Corp|Ltd)"
    ]
    for pattern in company_patterns:
        match = re.search(pattern, conversation_history, re.IGNORECASE)
        if match:
            details["company"] = match.group(1).strip()
            break
    
    # Email extraction
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', conversation_history)
    if email_match:
        details["email"] = email_match.group().strip()
    
    # Phone extraction
    phone_patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
        r'\b\(\d{3}\)\s*\d{3}[-.\s]?\d{4}\b'
    ]
    for pattern in phone_patterns:
        match = re.search(pattern, conversation_history)
        if match:
            details["phone"] = match.group().strip()
            break
    
    # Special case handling (e.g., Mark from Wilson Digital Marketing)
    if "mark" in conversation_history.lower() and "wilson digital marketing" in conversation_history.lower():
        details.update({
            "name": "Mark" if details["name"] == "Unknown" else details["name"],
            "company": "Wilson Digital Marketing" if not details["company"] else details["company"],
            "email": "mark@wilsondigital.com" if not details["email"] and "mark@wilsondigital.com" in conversation_history else details["email"]
        })
    
    return details

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def init_database():
    """Initialize SQLite database and create tables."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            lead_type TEXT NOT NULL,
            name TEXT NOT NULL,
            company TEXT,
            email TEXT,
            phone TEXT,
            details TEXT,
            priority TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()
        st.sidebar.success(f"✅ Connected to SQLite database: {DB_FILE}")
        return True
    except Exception as e:
        st.sidebar.error(f"❌ Failed to initialize database: {e}")
        return False

def save_lead_to_database(lead_type, lead_name, company=None, email=None, phone=None, details=None, priority="normal"):
    """Save lead information to database."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_system_message(f"DATABASE: Storing lead for {lead_name}")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO leads (timestamp, lead_type, name, company, email, phone, details, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, lead_type, lead_name, company or "", email or "", phone or "", details or "", priority))
        conn.commit()
        conn.close()
        log_system_message(f"DATABASE: Lead successfully stored for {lead_name}")
        return f"Lead for {lead_name} successfully stored in database"
    except Exception as e:
        error_msg = f"Failed to store lead: {str(e)}"
        log_system_message(f"DATABASE ERROR: {error_msg}")
        return error_msg

def get_all_leads():
    """Retrieve all leads from database."""
    try:
        log_system_message("DATABASE: Retrieving all leads")
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM leads ORDER BY timestamp DESC", conn)
        conn.close()
        log_system_message(f"DATABASE: Retrieved {len(df)} leads")
        return df
    except Exception as e:
        error_msg = f"Error retrieving leads: {str(e)}"
        log_system_message(f"DATABASE ERROR: {error_msg}")
        st.error(error_msg)
        return pd.DataFrame()

# ============================================================================
# EMAIL FUNCTIONS
# ============================================================================

def send_email_message(to_email, subject, body, cc=None, log_prefix="EMAIL"):
    """Core email sending function."""
    log_system_message(f"{log_prefix}: Sending to {to_email} - {subject}")
    
    if not EMAIL_ENABLED:
        message = f"Email disabled. Would send to {to_email}: {subject}"
        log_system_message(message)
        return message
    
    try:
        # Create and configure message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        if cc:
            msg['Cc'] = cc
        msg.attach(MIMEText(body, 'html'))
        
        # Send via Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_APP_PASSWORD)
            recipients = [to_email] + (cc.split(',') if cc else [])
            server.sendmail(EMAIL_USER, recipients, msg.as_string())
        
        success_msg = f"Email sent successfully to {to_email}"
        log_system_message(f"{log_prefix}: ✅ {success_msg}")
        return success_msg
        
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        log_system_message(f"{log_prefix}: ❌ {error_msg}")
        return error_msg

def create_lead_email_body(lead_type, lead_name, company=None, email=None, phone=None, details=None, priority="normal"):
    """Create HTML email body for lead notifications."""
    return f"""
    <h2>New {lead_type.title()} Lead ({priority.upper()} Priority)</h2>
    <p><strong>Name:</strong> {lead_name}</p>
    <p><strong>Company:</strong> {company or 'N/A'}</p>
    <p><strong>Email:</strong> {email or 'N/A'}</p>
    <p><strong>Phone:</strong> {phone or 'N/A'}</p>
    <p><strong>Details:</strong> {details or 'N/A'}</p>
    <hr>
    <p><em>This email was automatically generated by the Lead Qualification System.</em></p>
    """

def route_lead_email(lead_type, lead_name, **lead_info):
    """Route lead to appropriate email address."""
    destination = EMAIL_ROUTING.get(lead_type.lower(), EMAIL_USER)
    subject = f"New {lead_type.title()} Lead: {lead_name}"
    body = create_lead_email_body(lead_type, lead_name, **lead_info)
    
    log_system_message(f"ROUTING: {lead_type} lead '{lead_name}' to {destination}")
    return send_email_message(destination, subject, body, log_prefix="ROUTING")

async def force_lead_email(lead_type, lead_name, lead_info=None):
    """Force email sending for classified leads with deduplication."""
    if not lead_info:
        lead_info = {}
    
    # Normalize and cache lead information
    cache_key = f"{lead_type}:{lead_name}".lower()
    cached_info = LEAD_INFO_CACHE.get(cache_key, {})
    
    # Update cached info with new data
    for key, value in lead_info.items():
        if value and value not in ["Not provided", "No additional details"]:
            cached_info[key] = value
    
    LEAD_INFO_CACHE[cache_key] = cached_info
    email = cached_info.get("email")
    
    # Skip if no email available
    if not email or email == "Not provided":
        log_system_message(f"AUTO EMAIL: No email for {lead_type} lead {lead_name}; waiting")
        return f"Waiting for email address for {lead_name}"
    
    # Check deduplication
    now_ts = datetime.now().timestamp()
    last_sent = LEAD_EMAIL_CACHE.get(cache_key, {"ts": 0, "email": None})
    
    # Send if email changed or enough time passed
    should_send = (
        last_sent["email"] != email or 
        now_ts - last_sent["ts"] > EMAIL_DEDUPE_WINDOW
    )
    
    if not should_send:
        elapsed = int(now_ts - last_sent["ts"])
        log_system_message(f"AUTO EMAIL: Skipping duplicate for {lead_name} (sent {elapsed}s ago)")
        return f"Skipped duplicate email for {lead_name}"
    
    # Send email and update cache
    LEAD_EMAIL_CACHE[cache_key] = {"ts": now_ts, "email": email}
    result = route_lead_email(lead_type, lead_name, **cached_info)
    log_system_message(f"AUTO EMAIL: Force email result for {lead_name}: {result}")
    return result

def send_test_email():
    """Send test email to verify configuration."""
    if not EMAIL_ENABLED:
        st.sidebar.warning("⚠️ Email disabled. Configure EMAIL_USER and EMAIL_APP_PASSWORD.")
        return
    
    body = f"""
    <h1>Test Email</h1>
    <p>This is a test email from the Lead Qualification System.</p>
    <p>If you're receiving this, your email configuration is working correctly.</p>
    <hr>
    <p><strong>Configuration:</strong></p>
    <ul>
        <li>From: {EMAIL_USER}</li>
        <li>SMTP: smtp.gmail.com:587</li>
        <li>Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</li>
    </ul>
    """
    
    result = send_email_message(EMAIL_USER, "Test Email from Lead Qualification System", body, log_prefix="TEST")
    
    if "successfully" in result:
        st.sidebar.success("✅ Test email sent successfully!")
    else:
        st.sidebar.error(f"❌ Failed to send test email: {result}")

# ============================================================================
# AGENT TOOL FUNCTIONS
# ============================================================================

@function_tool
def send_email(to_email: str, subject: str, body: str, cc: str = None) -> str:
    """Send email tool for agents."""
    return send_email_message(to_email, subject, body, cc)

@function_tool
def route_lead_to_email(lead_type: str, lead_name: str, company: str = None, email: str = None, phone: str = None, details: str = None, priority: str = "normal") -> str:
    """Route lead to appropriate email tool for agents."""
    return route_lead_email(lead_type, lead_name, company=company, email=email, phone=phone, details=details, priority=priority)

@function_tool
def store_lead_in_database(lead_type: str, lead_name: str, company: str = None, email: str = None, phone: str = None, details: str = None, priority: str = "normal") -> str:
    """Store lead in database tool for agents."""
    return save_lead_to_database(lead_type, lead_name, company, email, phone, details, priority)

# ============================================================================
# AGENT HANDOFF CALLBACKS
# ============================================================================

def create_handoff_callback(lead_type):
    """Create a handoff callback function for a specific lead type."""
    def on_handoff(ctx: RunContextWrapper):
        log_system_message(f"HANDOFF: {lead_type.title()} lead detected")
        try:
            # Extract conversation history
            conversation = ""
            if hasattr(ctx, 'conversation_history'):
                conversation = ctx.conversation_history
            elif hasattr(ctx, 'messages'):
                conversation = "\n".join(msg.content for msg in ctx.messages if hasattr(msg, 'content'))
            
            # Add session conversation history if available
            if 'conversation_history' in st.session_state:
                conversation = f"{conversation}\n{st.session_state['conversation_history']}" if conversation else st.session_state['conversation_history']
            
            # Extract lead details and force email
            lead_details = extract_lead_details(conversation)
            log_system_message(f"HANDOFF: Extracted {lead_type} lead details: {lead_details}")
            
            # Schedule email sending
            asyncio.create_task(force_lead_email(lead_type, lead_details["name"], lead_details))
            
        except Exception as e:
            log_system_message(f"HANDOFF ERROR: Failed to process {lead_type} handoff: {str(e)}")
    
    return on_handoff

# ============================================================================
# AGENT CREATION
# ============================================================================

def create_agent_system():
    """Create and configure all agents."""
    
    # Specialized agent instructions
    agent_instructions = {
        "enterprise": """
        You are an enterprise sales specialist handling high-value enterprise leads.
        
        Focus on:
        - Professional, consultative tone
        - Business challenges and strategic needs
        - Company size, industry, current systems, pain points
        - Budget range, decision timeline, stakeholders
        - ROI, scalability, enterprise-grade features
        - Next steps: demos, technical consultations
        
        Enterprise clients value expertise, reliability, and strategic partnership.
        """,
        
        "smb": """
        You are an SMB sales specialist helping growing businesses find solutions.
        
        Focus on:
        - Friendly, helpful, solutions-oriented approach
        - Immediate needs and growth plans
        - Business size, type, current stage, challenges
        - Budget constraints, timeline, growth projections
        - Value, quick implementation, ROI for small businesses
        - Appropriate packages fitting their budget
        
        SMB clients need cost-effective, easy-to-implement, scalable solutions.
        """,
        
        "individual": """
        You are a customer success specialist for individual users.
        
        Focus on:
        - Conversational, friendly, approachable tone
        - Personal use cases and goals
        - Experience level, budget expectations
        - Features that matter most to them
        - Ease of use, personal value, affordability
        - Personal or freemium plans
        
        Individual clients value simplicity, affordability, and personal relevance.
        """
    }
    
    # Create specialized agents
    agents = {}
    for agent_type, instructions in agent_instructions.items():
        agents[agent_type] = Agent(
            name=f"{agent_type.title()}LeadAgent",
            instructions=instructions
        )
    
    # Create lead qualifier with handoffs
    lead_qualifier = Agent(
        name="LeadQualifier",
        instructions="""
        You are a lead qualification assistant. Your job is to:
        
        1. Greet leads professionally and collect basic information
        2. Analyze responses to determine lead type:
           - Enterprise: 1000+ employees, $500k+ budget, enterprise needs
           - SMB: <1000 employees, limited budget, growing business needs
           - Individual: Personal use, single users, non-business applications
        
        3. Hand off to appropriate specialist agent
        
        Always collect: contact name/role, company (if applicable), email/phone, basic requirements
        
        IMPORTANT: For EVERY lead, use these tools:
        - route_lead_to_email: Notify appropriate sales team
        - store_lead_in_database: Save lead information
        
        Ask clarifying questions if lead type is unclear.
        """,
        handoffs=[
            handoff(agents["enterprise"], on_handoff=create_handoff_callback("enterprise")),
            handoff(agents["smb"], on_handoff=create_handoff_callback("smb")),
            handoff(agents["individual"], on_handoff=create_handoff_callback("individual"))
        ],
        tools=[route_lead_to_email, store_lead_in_database, send_email]
    )
    
    return lead_qualifier

# ============================================================================
# MESSAGE PROCESSING
# ============================================================================

async def process_user_message(user_input):
    """Process user message through the agent system."""
    # Initialize conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = ""
    
    # Update conversation history
    if st.session_state['conversation_history']:
        st.session_state['conversation_history'] += f"\nUser: {user_input}"
    else:
        st.session_state['conversation_history'] = user_input
    
    log_system_message(f"PROCESSING: New message: {user_input[:50]}...")
    
    try:
        # Create lead qualifier if needed
        if 'lead_qualifier' not in st.session_state:
            log_system_message("PROCESSING: Creating lead qualifier agent")
            st.session_state['lead_qualifier'] = create_agent_system()
        
        # Process through agent system
        log_system_message("PROCESSING: Running through lead qualifier")
        with st.spinner('Processing your message...'):
            result = await Runner.run(st.session_state['lead_qualifier'], st.session_state['conversation_history'])
        
        # Get and store response
        response = result.final_output
        log_system_message(f"PROCESSING: Generated response: {response[:50]}...")
        
        # Update conversation and message history
        st.session_state['conversation_history'] += f"\nAssistant: {response}"
        st.session_state['messages'].append({"role": "user", "content": user_input})
        st.session_state['messages'].append({"role": "assistant", "content": response})
        
        return response
        
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        log_system_message(f"PROCESSING ERROR: {error_msg}")
        return "I apologize, but there was an error processing your message. Please try again."

# ============================================================================
# STREAMLIT UI
# ============================================================================

def render_sidebar():
    """Render the sidebar with configuration and controls."""
    st.sidebar.title("System Configuration")
    
    # API Key status
    if OPENAI_API_KEY:
        st.sidebar.success("✅ OpenAI API Key configured")
    else:
        st.sidebar.error("❌ OpenAI API Key not configured")
    
    # Email status and controls
    if EMAIL_ENABLED:
        st.sidebar.success(f"✅ Email enabled ({EMAIL_USER})")
        
        if st.sidebar.button("📧 Send Test Email"):
            send_test_email()
        
        if st.sidebar.button("📤 Test Email Routing"):
            results = []
            for lead_type in ["enterprise", "smb", "individual"]:
                result = route_lead_email(lead_type, f"Test {lead_type.title()} Lead")
                results.append("successfully" in result)
            
            if all(results):
                st.sidebar.success("✅ Test emails sent successfully!")
            else:
                st.sidebar.error("❌ Some test emails failed. Check logs.")
    else:
        st.sidebar.warning("⚠️ Email sending disabled")
        st.sidebar.info("Add EMAIL_USER and EMAIL_APP_PASSWORD to .env file")
    
    # Control buttons
    if st.sidebar.button("🔄 Reset Conversation"):
        st.session_state['messages'] = []
        st.session_state['conversation_history'] = ""
        log_system_message("SYSTEM: Conversation reset")
        st.rerun()
    
    # Database management
    st.sidebar.subheader("Database Management")
    
    if st.sidebar.button("👥 View Stored Leads"):
        df = get_all_leads()
        if not df.empty:
            st.sidebar.dataframe(df, use_container_width=True)
        else:
            st.sidebar.info("No leads found in database.")
    
    if st.sidebar.button("📤 Export Leads to JSON"):
        df = get_all_leads()
        if not df.empty:
            json_data = df.to_json(orient="records", indent=4)
            st.sidebar.download_button(
                label="📋 Download JSON",
                data=json_data,
                file_name="leads_export.json",
                mime="application/json"
            )
        else:
            st.sidebar.info("No leads to export.")
    
    # Clear leads with confirmation
    if st.sidebar.checkbox("I understand this will permanently delete all leads"):
        if st.sidebar.button("🗑️ Clear All Leads"):
            try:
                conn = sqlite3.connect(DB_FILE)
                conn.execute("DELETE FROM leads")
                conn.commit()
                conn.close()
                st.sidebar.success("All leads cleared from database.")
                log_system_message("DATABASE: All leads cleared")
            except Exception as e:
                st.sidebar.error(f"Error clearing leads: {e}")

def main():
    """Main Streamlit application."""
    # Page configuration
    st.set_page_config(
        page_title="Lead Qualification System",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🤖 Lead Qualification System")
    st.markdown("Welcome to our automated lead qualification system. This chat will help us understand your needs and connect you with the right team.")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'system_logs' not in st.session_state:
        st.session_state['system_logs'] = []
    
    # Initialize database
    if not init_database():
        st.warning("Failed to initialize database. Check system logs for details.")
    
    # Render sidebar
    render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display chat messages
        for message in st.session_state['messages']:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        user_input = st.chat_input("Type your message here...")
        if user_input:
            asyncio.run(process_user_message(user_input))
            st.rerun()
    
    with col2:
        # System logs
        st.subheader("System Logs")
        log_container = st.container(height=500)
        with log_container:
            for log in st.session_state['system_logs']:
                st.text(log)

if __name__ == "__main__":
    main()