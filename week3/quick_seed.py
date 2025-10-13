#!/usr/bin/env python3
"""Quick Pinecone seeder - run this to populate vacation policy documents"""
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import time

# Add parent directory to path to find .env
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

# Sample vacation policy document
VACATION_DOC = """ACME Corporation - Vacation and Time Off Policy 2024

VACATION ACCRUAL:
All full-time employees accrue 2.5 vacation days per month, totaling 30 days annually.
Part-time employees accrue vacation days proportional to their scheduled hours.

REQUESTING TIME OFF:
- Vacation requests must be submitted at least 2 weeks in advance through the HR portal
- Requests less than 2 weeks require manager approval
- Holiday periods require 4 weeks advance notice

CARRYOVER POLICY:
- Up to 5 unused vacation days can be carried over to the next calendar year
- Excess days are forfeited (use-it-or-lose-it policy)
- Carried over days must be used by March 31st

VACATION PAYOUT:
- Upon termination, unused vacation days are paid out at current salary rate
- Minimum 2 weeks notice required for payout eligibility

For questions, contact HR at hr@acmecorp.com"""

def main():
    print("🚀 Seeding Pinecone with Vacation Policy...")
    
    # Check API keys
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found")
        return
    if not os.environ.get("PINECONE_API_KEY"):
        print("❌ PINECONE_API_KEY not found")
        return
    
    try:
        from pinecone import Pinecone, ServerlessSpec
        
        # Initialize
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        
        index_name = "documents"
        
        # Create index if needed
        if index_name not in [idx.name for idx in pc.list_indexes()]:
            print(f"Creating index '{index_name}'...")
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            print("Waiting 60 seconds for index...")
            time.sleep(60)
        
        index = pc.Index(index_name)
        
        # Create embedding
        print("Creating embedding...")
        response = openai_client.embeddings.create(
            input=VACATION_DOC,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        
        # Upload
        print("Uploading to Pinecone...")
        index.upsert(vectors=[{
            "id": "vacation_policy_2024",
            "values": embedding,
            "metadata": {
                "title": "Vacation Policy 2024",
                "content": VACATION_DOC[:500],
                "full_content": VACATION_DOC
            }
        }])
        
        print("✅ Success! Waiting 5 seconds for indexing...")
        time.sleep(5)
        
        # Test search
        print("\n🔍 Testing search...")
        test_response = openai_client.embeddings.create(
            input="vacation policy",
            model="text-embedding-ada-002"
        )
        test_embedding = test_response.data[0].embedding
        
        results = index.query(
            vector=test_embedding,
            top_k=3,
            include_metadata=True
        )
        
        if results.matches:
            print(f"✅ Found {len(results.matches)} results!")
            for match in results.matches:
                print(f"  📄 {match.metadata['title']} (Score: {match.score:.3f})")
            print("\n🎉 Success! Now enable 'Real APIs' in your app and try:")
            print("   'Find information in our documents about vacation policy'")
        else:
            print("⚠️  No results found in test search")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
