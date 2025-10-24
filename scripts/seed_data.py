#!/usr/bin/env python3
"""
🌱 Seed Sample Data to Pinecone
================================
Seeds the Pinecone vector database with sample company documents
for testing the document search functionality.

Usage:
    python scripts/seed_data.py
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sample company documents to seed
SAMPLE_DOCUMENTS = [
    {
        "title": "Company Remote Work Policy",
        "content": """
Remote Work Policy - Updated 2024

All employees are eligible for hybrid remote work (3 days office, 2 days remote).
Full remote positions require manager approval and are evaluated case-by-case.

Equipment: Company provides laptop, monitor, keyboard, mouse, and headset.
Home office stipend: $500 annually for desk, chair, or other office equipment.

Working Hours: Core hours 10 AM - 3 PM (your timezone). Flex time outside core hours.
Communication: Must be available on Slack/Teams during core hours.
Meetings: Video-on encouraged for team meetings. Camera optional for 1:1s.

Security Requirements:
- Use company VPN for all work activities
- Lock screen when away from desk
- No public WiFi without VPN
- Report lost/stolen equipment immediately

Performance: Measured by output and results, not hours logged.
        """,
        "metadata": {"category": "HR Policy", "department": "Human Resources", "date": "2024-01-15"}
    },
    {
        "title": "Employee Vacation and PTO Policy",
        "content": """
Vacation and Paid Time Off Policy

PTO Accrual:
- 0-2 years: 15 days per year
- 3-5 years: 20 days per year
- 6+ years: 25 days per year

PTO accrues monthly and can be used as it accrues (no waiting period).
Maximum rollover: 5 days into next year. Use-it-or-lose-it after that.

Requesting Time Off:
1. Submit request in Workday at least 2 weeks in advance
2. Manager approval required
3. Add to team calendar once approved
4. Set Slack/email out-of-office status

Holidays: 10 paid company holidays + 2 floating holidays per year.
Holiday list published annually in December.

Sick Leave: Unlimited sick days (not deducted from PTO).
Medical appointments: Use sick time, no PTO deduction.

Parental Leave: 12 weeks paid for primary caregiver, 6 weeks for secondary.
        """,
        "metadata": {"category": "HR Policy", "department": "Human Resources", "date": "2024-02-01"}
    },
    {
        "title": "Information Security Guidelines",
        "content": """
Information Security Guidelines - Mandatory Compliance

Password Policy:
- Minimum 12 characters
- Must include uppercase, lowercase, numbers, and symbols
- Change every 90 days
- Cannot reuse last 5 passwords
- Use password manager (1Password or LastPass approved)

Multi-Factor Authentication (MFA):
- Required for all systems
- Use company-approved authenticator app
- Hardware keys available for high-security roles

Data Classification:
- Public: Can be shared externally
- Internal: Company-only, no external sharing
- Confidential: Restricted access, encryption required
- Highly Confidential: Executive/Legal approval required

Email Security:
- Verify sender before clicking links
- Report phishing to security@company.com
- Never share credentials via email
- Use encrypted email for confidential data

Device Security:
- Full disk encryption required
- Auto-lock after 5 minutes
- Remote wipe enabled
- No personal devices for company data

Incident Reporting: Report any security concerns to IT Security within 1 hour.
        """,
        "metadata": {"category": "Security", "department": "IT Security", "date": "2024-03-10"}
    },
    {
        "title": "Professional Development and Training",
        "content": """
Professional Development Program

Annual Learning Budget: $2,000 per employee for:
- Online courses (Coursera, Udemy, LinkedIn Learning)
- Conference attendance
- Professional certifications
- Books and learning materials
- Workshops and seminars

Conference Attendance:
- Up to 2 conferences per year
- Submit proposal 60 days in advance
- Manager approval required
- Company covers registration, travel, hotel
- Present learnings to team after conference

Certification Reimbursement:
- 100% reimbursement for job-related certifications
- Includes exam fees, study materials, prep courses
- Renewal fees covered annually
- Must pass exam for reimbursement

Learning Time:
- 5 hours per month for learning during work hours
- "Learning Fridays" - last Friday of month
- Lunch & Learn sessions (1st Wednesday monthly)

Tuition Assistance:
- Up to $5,000/year for degree programs
- Must be relevant to current or future role
- Minimum 1-year commitment after completion
- Grades of B or higher required

Career Growth:
- Annual performance reviews
- Career development discussions quarterly
- Internal mobility encouraged
- Mentorship program available
        """,
        "metadata": {"category": "HR Policy", "department": "Learning & Development", "date": "2024-01-20"}
    },
    {
        "title": "Q4 2024 Product Roadmap",
        "content": """
Q4 2024 Product Roadmap - Confidential

Major Features:
1. AI-Powered Search (October)
   - Natural language query interface
   - Semantic search across all content
   - Personalized results based on user behavior
   - Target: 50% improvement in search relevance

2. Mobile App v2.0 (November)
   - Complete redesign with new UI
   - Offline mode for core features
   - Push notifications for important updates
   - Biometric authentication

3. Enterprise Dashboard (December)
   - Real-time analytics and reporting
   - Custom KPI tracking
   - Data export to BI tools
   - Role-based access controls

Performance Goals:
- Page load time: < 2 seconds
- API response time: < 200ms
- 99.9% uptime SLA
- Mobile app rating: > 4.5 stars

Technical Debt:
- Database migration to PostgreSQL 15
- Upgrade to React 18
- Implement GraphQL API
- Migrate to Kubernetes

Launch Dates:
- Beta release: October 15
- Early access: November 1
- General availability: December 1
        """,
        "metadata": {"category": "Product", "department": "Product Management", "date": "2024-09-01"}
    },
    {
        "title": "Customer Onboarding Best Practices",
        "content": """
Customer Onboarding Best Practices Guide

Phase 1: Kickoff (Week 1)
- Welcome email within 24 hours of signup
- Schedule kickoff call within 48 hours
- Assign dedicated success manager
- Create custom onboarding plan
- Set success metrics and goals

Phase 2: Implementation (Weeks 2-4)
- Technical setup and integration
- Data migration (if applicable)
- User training sessions (3-5 sessions)
- Configure security and permissions
- Customize workflows and templates

Phase 3: Activation (Weeks 5-6)
- Launch to pilot user group
- Gather feedback and iterate
- Address technical issues
- Additional training as needed
- Monitor usage metrics

Phase 4: Expansion (Weeks 7-12)
- Roll out to broader organization
- Advanced feature training
- Best practices workshops
- Integration with other tools
- Quarterly business reviews

Success Metrics:
- Time to first value: < 7 days
- User activation rate: > 70% in 30 days
- Feature adoption: > 50% using core features
- Customer satisfaction: NPS > 50
- Support ticket volume: < 5 per week

Red Flags:
- No login in first week
- Less than 3 active users
- High support ticket volume
- No data uploaded
- Missed kickoff meeting

Escalation: Contact Customer Success Director if red flags persist > 2 weeks
        """,
        "metadata": {"category": "Sales", "department": "Customer Success", "date": "2024-02-15"}
    },
    {
        "title": "Expense Reimbursement Policy",
        "content": """
Expense Reimbursement Policy

Eligible Expenses:
✅ Business travel (flights, hotels, ground transportation)
✅ Client meals and entertainment
✅ Office supplies and equipment
✅ Professional development and training
✅ Business phone and internet (50% if work from home)
✅ Mileage ($0.67 per mile for business use)

Non-Reimbursable:
❌ Personal expenses
❌ Alcohol (except client meals with approval)
❌ Entertainment without business purpose
❌ First-class flights (unless no other option)
❌ Expensive hotels (use company rate or < $200/night)

Submission Requirements:
- Submit within 30 days of expense
- Use Expensify app
- Attach itemized receipts (required for expenses > $25)
- Provide business purpose description
- Manager approval required

Reimbursement Timeline:
- Submitted by 15th of month → Reimbursed by end of month
- Submitted after 15th → Reimbursed by 15th of next month
- Direct deposit to bank account on file

Travel Booking:
- Book through corporate travel portal (Concur)
- Economy class for flights < 5 hours
- Premium economy for flights 5+ hours (pre-approval)
- Use preferred hotel chains (Marriott, Hilton)
- Reasonable meals: Breakfast $15, Lunch $25, Dinner $50

Company Credit Card:
- Available for directors and above
- Monthly reconciliation required
- Personal use prohibited
- Lost/stolen cards: Report immediately
        """,
        "metadata": {"category": "Finance", "department": "Finance", "date": "2024-01-10"}
    },
    {
        "title": "Code Review Guidelines",
        "content": """
Code Review Guidelines - Engineering Team

Purpose:
- Catch bugs before production
- Share knowledge across team
- Maintain code quality standards
- Ensure consistency and best practices

Code Review Checklist:
✅ Code follows style guide (see CONTRIBUTING.md)
✅ All tests pass (unit + integration)
✅ Test coverage > 80% for new code
✅ No security vulnerabilities
✅ Documentation updated (README, API docs)
✅ No hardcoded secrets or credentials
✅ Error handling implemented
✅ Performance considerations addressed

Review Process:
1. Create pull request with clear description
2. Link to ticket/issue number
3. Request 1-2 reviewers (required)
4. Address all comments before merging
5. Squash commits before merge
6. Delete branch after merge

Response Time SLAs:
- Critical bugs: 2 hours
- Normal PRs: 24 hours
- Large features: 48 hours

Review Comments:
- Be respectful and constructive
- Explain "why" not just "what"
- Suggest specific improvements
- Use: "Consider...", "What if...", "Could we..."
- Praise good code!

Auto-Merge Criteria:
- All required reviewers approved
- All CI/CD checks passed
- No merge conflicts
- Branch up to date with main

Large PRs (> 500 lines):
- Consider breaking into smaller PRs
- Provide detailed overview
- Highlight high-risk areas
- Schedule sync review meeting if needed
        """,
        "metadata": {"category": "Engineering", "department": "Engineering", "date": "2024-03-01"}
    }
]

def print_status(message, status="info"):
    """Print colored status messages"""
    colors = {
        "info": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "endc": "\033[0m"
    }

    symbols = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }

    print(f"{colors[status]}{symbols[status]} {message}{colors['endc']}")

def check_environment():
    """Check if required environment variables are set"""
    print_status("Checking environment configuration...", "info")

    openai_key = os.getenv('OPENAI_API_KEY')
    pinecone_key = os.getenv('PINECONE_API_KEY')

    if not openai_key or openai_key == 'your_openai_api_key_here':
        print_status("OPENAI_API_KEY not configured in .env file", "error")
        return False

    if not pinecone_key or pinecone_key == 'your_pinecone_api_key_here':
        print_status("PINECONE_API_KEY not configured in .env file", "error")
        print_status("Please add your Pinecone API key to the .env file", "info")
        return False

    print_status("Environment variables configured", "success")
    return True

def seed_pinecone():
    """Seed Pinecone with sample documents"""
    try:
        from pinecone import Pinecone, ServerlessSpec
        from openai import OpenAI
    except ImportError:
        print_status("Required packages not installed", "error")
        print_status("Run: pip install pinecone-client openai", "info")
        return False

    print_status("Connecting to Pinecone...", "info")

    # Initialize Pinecone
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    # Initialize OpenAI
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Define index name
    index_name = "company-docs"

    # Check if index exists
    existing_indexes = [idx.name for idx in pc.list_indexes()]

    if index_name not in existing_indexes:
        print_status(f"Creating index '{index_name}'...", "info")
        pc.create_index(
            name=index_name,
            dimension=1536,  # OpenAI embedding dimension
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
        print_status(f"Index '{index_name}' created", "success")
    else:
        print_status(f"Index '{index_name}' already exists", "info")

    # Connect to index
    index = pc.Index(index_name)

    print_status(f"Seeding {len(SAMPLE_DOCUMENTS)} documents...", "info")

    # Process and upload each document
    for i, doc in enumerate(SAMPLE_DOCUMENTS, 1):
        print_status(f"Processing document {i}/{len(SAMPLE_DOCUMENTS)}: {doc['title']}", "info")

        # Create embedding
        try:
            response = openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=doc['content']
            )
            embedding = response.data[0].embedding

            # Prepare metadata
            metadata = {
                "title": doc['title'],
                "content": doc['content'][:1000],  # Store first 1000 chars in metadata
                **doc['metadata']
            }

            # Upsert to Pinecone
            index.upsert(
                vectors=[
                    {
                        "id": f"doc_{i}",
                        "values": embedding,
                        "metadata": metadata
                    }
                ]
            )

            print_status(f"✓ Uploaded: {doc['title']}", "success")

        except Exception as e:
            print_status(f"Failed to process {doc['title']}: {e}", "error")
            continue

    # Get index stats
    stats = index.describe_index_stats()
    print_status(f"\nSeeding complete! Total vectors: {stats.total_vector_count}", "success")

    return True

def main():
    """Main function"""
    print("\n" + "="*60)
    print("🌱 Pinecone Data Seeding Script")
    print("="*60 + "\n")

    # Check environment
    if not check_environment():
        print_status("\nPlease configure your .env file and try again", "error")
        sys.exit(1)

    # Confirm with user
    print("\nThis will seed Pinecone with sample company documents.")
    response = input("Do you want to continue? (y/N): ").strip().lower()

    if response != 'y':
        print_status("Seeding cancelled", "warning")
        sys.exit(0)

    # Seed data
    if seed_pinecone():
        print_status("\n✨ All done! Your Pinecone database is ready to use.", "success")
        print_status("You can now search these documents in the 'Yes Dear' Assistant", "info")
    else:
        print_status("\nSeeding failed. Check the errors above.", "error")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_status("\n\nSeeding cancelled by user", "warning")
        sys.exit(1)
    except Exception as e:
        print_status(f"\nUnexpected error: {e}", "error")
        sys.exit(1)
