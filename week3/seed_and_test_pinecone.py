#!/usr/bin/env python3
"""
Pinecone Database Seeder and Tester for Week 3 Multi-Agent System
==================================================================

This script:
1. Seeds Pinecone with sample documents including vacation policy
2. Tests retrieval with various queries
3. Verifies the multi-agent system can access the data

Usage:
    python seed_and_test_pinecone.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import time

# Load environment variables from root directory
root_dir = Path(__file__).parent.parent
env_path = root_dir / ".env"
load_dotenv(env_path)

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

# Sample documents to seed (rich vacation policy content)
SAMPLE_DOCUMENTS = {
    "vacation_policy_2024": {
        "title": "Vacation Policy 2024",
        "content": """ACME Corporation - Vacation and Time Off Policy 2024

VACATION ACCRUAL:
All full-time employees accrue 2.5 vacation days per month, totaling 30 days annually.
Part-time employees accrue vacation days proportional to their scheduled hours.

REQUESTING TIME OFF:
- Vacation requests must be submitted at least 2 weeks in advance through the HR portal
- Requests less than 2 weeks require manager approval
- Holiday periods (Thanksgiving, Christmas) require 4 weeks advance notice
- System will auto-deny requests that violate policy

CARRYOVER POLICY:
- Up to 5 unused vacation days can be carried over to the next calendar year
- Excess days beyond 5 are forfeited (use-it-or-lose-it)
- Carried over days must be used by March 31st of the following year

VACATION PAYOUT:
- Upon termination, unused vacation days are paid out at current salary rate
- Minimum 2 weeks notice required for payout eligibility
- Maximum payout is 30 days

BLACKOUT PERIODS:
- End of quarter (last week of March, June, September, December)
- Annual conference week (typically second week of May)
- System migration periods (announced 90 days in advance)

MANAGER DISCRETION:
Managers may approve exceptions for:
- Family emergencies (documentation required)
- Medical situations (doctor's note required)
- Unforeseen circumstances (case-by-case basis)

For questions, contact HR at hr@acmecorp.com or extension 5500."""
    },
    
    "employee_handbook_2024": {
        "title": "Employee Handbook 2024",
        "content": """ACME Corp Employee Handbook 2024

COMPANY POLICIES

Work From Home Policy:
Employees may work remotely up to 3 days per week with manager approval. Core collaboration hours are 10 AM - 3 PM PST for all remote workers. Home office equipment stipend of $500 available annually.

Vacation Policy Summary:
Full-time employees receive 30 days of vacation annually. See detailed Vacation Policy document for accrual rates, request procedures, and carryover rules.

Sick Leave:
Unlimited sick days for illness or medical appointments. Extended sick leave (>5 consecutive days) requires medical documentation. Mental health days are included and encouraged.

Holidays:
ACME observes 12 paid holidays annually including New Year's, Memorial Day, Independence Day, Labor Day, Thanksgiving (2 days), and Christmas (3 days). Floating holidays available for personal observances.

Expense Reimbursement:
Business expenses under $100 require receipt submission within 30 days. Expenses over $100 require pre-approval from department heads. Travel expenses covered per corporate travel policy.

Code of Conduct:
ACME Corp maintains a zero-tolerance policy for harassment. All incidents should be reported to HR immediately through our confidential reporting system at ethics@acmecorp.com.

IT Security:
Employees must use company-approved VPN for all remote work. Personal devices accessing company data require MDM enrollment and security compliance checks. Password requirements: 12+ characters, changed every 90 days.

Professional Development:
The company provides $2,000 annually per employee for professional development, including conferences, courses, and certifications relevant to their role. Must be pre-approved by manager.

Parental Leave:
16 weeks paid parental leave for primary caregivers, 8 weeks for secondary caregivers. Available for birth, adoption, or foster care placement.

Performance Reviews:
Conducted bi-annually in January and July. Based on OKRs (Objectives and Key Results) set quarterly. 360-degree feedback incorporated.

Benefits Enrollment:
Open enrollment period is November 1-30 annually. Mid-year changes allowed for qualifying life events only. Contact benefits@acmecorp.com with questions."""
    },
    
    "hr_faqs_vacation": {
        "title": "HR FAQs - Vacation and Time Off",
        "content": """Frequently Asked Questions: Vacation and Time Off

Q: How do I check my vacation balance?
A: Log into the HR portal (hr.acmecorp.com) and click "My Time Off" in the dashboard. Real-time balance is displayed including pending requests.

Q: Can I take vacation before it accrues?
A: New employees can take up to 5 days of advance vacation after 90-day probation period. Negative balances must be repaid if employment ends.

Q: What happens if I'm sick during scheduled vacation?
A: Notify your manager and HR immediately. With medical documentation, sick days can be reclassified as sick leave, preserving vacation days.

Q: Can I donate vacation days to colleagues?
A: Yes! ACME's Vacation Share Program allows donation to colleagues facing medical or family emergencies. Contact HR to participate.

Q: Do contractors get vacation days?
A: Contractors are not eligible for vacation accrual. Contract terms should specify any time-off arrangements.

Q: How do I request vacation?
A: Submit through HR portal at least 2 weeks in advance. Include dates, return date, and emergency contact. Manager notification is automatic.

Q: What if my vacation request is denied?
A: Managers must provide written explanation within 48 hours. You can appeal to HR or suggest alternative dates.

Q: Can I split vacation into half-days?
A: Yes! Minimum increment is 4 hours. Half-day requests follow same approval process as full days.

Q: Do I accrue vacation while on unpaid leave?
A: No accrual during unpaid leave periods. Accrual resumes upon return to active employment.

Q: What's the difference between PTO and vacation?
A: ACME uses separate banks: Vacation (30 days), Sick Leave (unlimited), and Personal Days (3 per year). Each has specific rules.

Q: Can I cash out vacation days?
A: Generally no, except at termination. Annual exception: One-time cash out of up to 5 days during open enrollment.

Q: Are there peak/off-peak vacation times?
A: Summer (June-August) is peak season. Priority given to employees with children during school breaks. Plan early!

Q: International employees - different rules?
A: Yes! Country-specific policies available on HR portal. Statutory requirements take precedence over company policy.

For more questions, contact HR Help Desk:
- Email: hr@acmecorp.com
- Phone: ext 5500
- Live Chat: hr.acmecorp.com/chat
- Office hours: M-F 8am-6pm PST"""
    },
    
    "remote_work_policy": {
        "title": "Remote Work and Flexible Schedule Policy",
        "content": """ACME Corporation - Remote Work Policy 2024

ELIGIBILITY:
All employees past 90-day probation are eligible for hybrid work arrangements. Fully remote positions require director-level approval and specific role justification.

HYBRID WORK SCHEDULE:
- Standard arrangement: 3 days remote, 2 days in office
- Core in-office days: Tuesday and Wednesday (team collaboration days)
- Flexible days: Monday, Thursday, Friday (remote or office, employee choice)
- Managers may set team-specific requirements with HR approval

REMOTE WORK REQUIREMENTS:
- Dedicated workspace with reliable internet (minimum 25 Mbps)
- Professional video background for client calls
- Response time: 1 hour during core hours (10 AM - 3 PM PST)
- Available via Slack/Teams during working hours
- Company-provided laptop and peripherals

HOME OFFICE STIPEND:
- One-time $500 setup stipend for desk, chair, monitor
- Annual $250 refresh budget for supplies and equipment
- Submit receipts through expense system

INTERNATIONAL REMOTE WORK:
- Requires legal and tax review (minimum 3 months notice)
- Available for up to 90 days per calendar year
- Must maintain time zone overlap (minimum 4 hours)
- Worker's compensation and employment law compliance required

TIME TRACKING:
- Salaried employees: No time clock, track projects in Asana
- Hourly employees: Clock in/out through TimeClock Plus
- Overtime requires pre-approval regardless of location

EQUIPMENT AND SECURITY:
- All company devices require full-disk encryption
- VPN mandatory for accessing company resources
- No personal devices for work unless MDM enrolled
- Report lost/stolen equipment within 24 hours

PERFORMANCE EXPECTATIONS:
- Same standards apply to remote and in-office work
- Measured by output and results, not hours visible
- Regular 1:1s with manager (weekly minimum)
- Quarterly review of remote work arrangement effectiveness

TEMPORARY REMOTE WORK:
- Occasional remote work (1-2 days) requires manager notification only
- Extended remote work (>2 weeks) requires HR approval
- Medical or caregiving situations handled case-by-case

TERMINATION OF REMOTE PRIVILEGE:
May be revoked for:
- Performance issues
- Communication/availability problems
- Security violations
- Team collaboration needs
- Change in role requirements

RETURNING TO OFFICE:
- Company provides 60 days notice for return-to-office requirements
- Equipment return coordinated with IT
- Workspace assigned based on attendance frequency

Questions? Contact WorkplaceFlexibility@acmecorp.com"""
    },
    
    "api_documentation": {
        "title": "ACME API Documentation v2.1",
        "content": """ACME Corporation - API Documentation v2.1

OVERVIEW:
ACME REST APIs provide programmatic access to company systems including HR, Finance, and Operations data.

AUTHENTICATION:
- OAuth 2.0 authentication required for all endpoints
- API keys available through Developer Portal (developers.acmecorp.com)
- Rate limits: 1000 requests/hour for standard tier, 10000/hour for enterprise

HR API ENDPOINTS:

GET /api/v2/employees/{id}
Returns employee profile including contact, department, manager, hire date.

GET /api/v2/employees/{id}/vacation
Returns vacation balance, accrual rate, and request history.
Response: {balance: 23.5, accrued: 2.5, pending: 0, used: 6.5}

POST /api/v2/vacation/request
Submit vacation request. Requires: employee_id, start_date, end_date, notes.
Auto-validates against policy rules. Returns request ID and approval status.

GET /api/v2/vacation/calendar/{department}
Returns department vacation calendar for planning purposes.

FINANCE API ENDPOINTS:

GET /api/v2/expenses/{employee_id}
Returns expense reports and reimbursement status.

POST /api/v2/expenses/submit
Submit expense report with receipts (base64 encoded images).

OPERATIONS API ENDPOINTS:

GET /api/v2/projects
List all active projects with team assignments.

GET /api/v2/assets/{asset_id}
Retrieve company asset information for inventory management.

ERROR CODES:
- 400: Bad Request (validation error)
- 401: Unauthorized (invalid API key)
- 403: Forbidden (insufficient permissions)
- 404: Not Found
- 429: Rate Limit Exceeded
- 500: Internal Server Error

RATE LIMITING:
X-RateLimit-Remaining header indicates remaining requests.
429 responses include Retry-After header (seconds).

WEBHOOKS:
Subscribe to events: employee.hired, vacation.approved, expense.reimbursed
Configure webhooks at developers.acmecorp.com/webhooks

SUPPORT:
Technical support: api-support@acmecorp.com
Documentation: https://docs.acmecorp.com/api
Status page: status.acmecorp.com"""
    }
}


def check_requirements():
    """Check if all required packages and API keys are available"""
    print_header("Checking Requirements")
    
    # Check API keys
    openai_key = os.environ.get("OPENAI_API_KEY")
    pinecone_key = os.environ.get("PINECONE_API_KEY")
    
    if not openai_key:
        print_error("OPENAI_API_KEY not found in .env file")
        return False
    print_success("OpenAI API key found")
    
    if not pinecone_key:
        print_error("PINECONE_API_KEY not found in .env file")
        print_warning("Pinecone is optional for real document search")
        print_info("App will work in Demo Mode without it")
        return False
    print_success("Pinecone API key found")
    
    # Check for Pinecone package using importlib to avoid importing unused symbols
    import importlib.util
    if importlib.util.find_spec('pinecone') is None:
        print_error("Pinecone package not installed")
        print_info("Run: pip install pinecone-client")
        return False
    print_success("Pinecone package appears available")
    
    return True


def seed_pinecone():
    """Seed Pinecone with sample documents"""
    print_header("Seeding Pinecone Database")
    
    try:
        from pinecone import Pinecone, ServerlessSpec
        
        # Initialize clients
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
        openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Index configuration
        index_name = "documents"
        dimension = 1536  # OpenAI text-embedding-ada-002 dimension
        
        print_info(f"Checking for index '{index_name}'...")
        
        # Check if index exists
        existing_indexes = [idx.name for idx in pc.list_indexes()]
        
        if index_name not in existing_indexes:
            print_info(f"Creating new index '{index_name}'...")
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print_info("Waiting for index to initialize (60 seconds)...")
            time.sleep(60)
            print_success(f"Index '{index_name}' created")
        else:
            # Verify dimension
            index_info = pc.describe_index(index_name)
            if index_info.dimension != dimension:
                print_warning(f"Index has wrong dimension ({index_info.dimension}). Recreating...")
                pc.delete_index(index_name)
                time.sleep(30)
                pc.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
                time.sleep(60)
                print_success(f"Index '{index_name}' recreated")
            else:
                print_success(f"Index '{index_name}' already exists")
        
        # Connect to index
        index = pc.Index(index_name)
        
        # Prepare documents
        print_info(f"Preparing {len(SAMPLE_DOCUMENTS)} documents...")
        vectors = []
        
        for doc_id, doc_data in SAMPLE_DOCUMENTS.items():
            print_info(f"  Processing: {doc_data['title']}...")
            
            # Create embedding
            embedding_response = openai_client.embeddings.create(
                input=doc_data['content'],
                model="text-embedding-ada-002"
            )
            embedding = embedding_response.data[0].embedding
            
            # Prepare vector
            vectors.append({
                "id": doc_id,
                "values": embedding,
                "metadata": {
                    "title": doc_data['title'],
                    "content": doc_data['content'][:1000] + "..." if len(doc_data['content']) > 1000 else doc_data['content'],
                    "full_content": doc_data['content'],
                    "word_count": len(doc_data['content'].split()),
                    "type": "policy_document"
                }
            })
            print_success(f"    Embedded: {doc_data['title']} ({len(doc_data['content'])} chars)")
        
        # Upload to Pinecone
        print_info(f"Uploading {len(vectors)} documents to Pinecone...")
        index.upsert(vectors=vectors)
        print_success(f"All {len(vectors)} documents uploaded successfully!")
        
        # Wait for indexing
        print_info("Waiting for indexing to complete (10 seconds)...")
        time.sleep(10)
        
        return True, index, openai_client
        
    except Exception as e:
        print_error(f"Error seeding Pinecone: {e}")
        return False, None, None


def test_vacation_queries(index, openai_client):
    """Test various vacation-related queries"""
    print_header("Testing Vacation Policy Queries")
    
    test_queries = [
        "vacation policy",
        "how many vacation days do I get",
        "vacation accrual rate",
        "can I carry over vacation days",
        "vacation request process",
        "vacation payout when I leave",
        "vacation blackout periods",
        "vacation balance check",
        "international remote work",
        "sick leave policy"
    ]
    
    all_passed = True
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{Colors.OKCYAN}Test {i}/{len(test_queries)}: '{query}'{Colors.ENDC}")
        
        try:
            # Create embedding
            embedding_response = openai_client.embeddings.create(
                input=query,
                model="text-embedding-ada-002"
            )
            query_embedding = embedding_response.data[0].embedding
            
            # Search Pinecone
            results = index.query(
                vector=query_embedding,
                top_k=3,
                include_metadata=True
            )
            
            if results.matches:
                print_success(f"Found {len(results.matches)} results:")
                for j, match in enumerate(results.matches[:3], 1):
                    title = match.metadata.get('title', 'Untitled')
                    score = match.score
                    content_preview = match.metadata.get('content', '')[:150]
                    
                    print(f"  {j}. {title} (Score: {score:.3f})")
                    print(f"     {content_preview}...")
            else:
                print_error("No results found!")
                all_passed = False
                
        except Exception as e:
            print_error(f"Query failed: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Main execution function"""
    print_header("Pinecone Database Seeder & Tester")
    print(f"{Colors.BOLD}For Week 3 Multi-Agent System{Colors.ENDC}\n")
    
    # Check requirements
    if not check_requirements():
        print_error("Requirements check failed. Please fix issues above and try again.")
        return 1
    
    # Seed database
    success, index, openai_client = seed_pinecone()
    if not success:
        print_error("Failed to seed Pinecone database")
        return 1
    
    # Test queries
    print_info("Starting query tests...")
    test_success = test_vacation_queries(index, openai_client)
    
    # Final summary
    print_header("Summary")
    
    if test_success:
        print_success("All tests passed! ✨")
        print()
        print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}")
        print("1. Run your multi-agent app: streamlit run app_multi_agent.py")
        print("2. In the sidebar, check '🔴 Use Real APIs'")
        print("3. Enable '📚 Document Search'")
        print("4. Try these queries:")
        print("   • 'Find information in our documents about vacation policy'")
        print("   • 'How many vacation days do I get?'")
        print("   • 'Can I carry over vacation days to next year?'")
        print("   • 'What is the vacation request process?'")
        print()
        print_success("Your document search should now return real Pinecone results! 🎉")
        return 0
    else:
        print_warning("Some tests failed. Check output above for details.")
        print_info("App will still work, but results may be incomplete.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
