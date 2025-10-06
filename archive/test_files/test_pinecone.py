#!/usr/bin/env python3
"""
Test Pinecone Document Search
Quick test to see if Pinecone is working correctly
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_pinecone_search():
    """Test Pinecone search functionality"""
    
    # Check for required API keys
    openai_key = os.environ.get("OPENAI_API_KEY")
    pinecone_key = os.environ.get("PINECONE_API_KEY")
    
    if not openai_key or not pinecone_key:
        print("❌ Missing API keys")
        return False
    
    try:
        # Import and initialize
        from pinecone import Pinecone
        pc = Pinecone(api_key=pinecone_key)
        openai_client = OpenAI(api_key=openai_key)
        
        # Connect to index
        index = pc.Index("documents")
        
        # Test queries that should match your documents
        test_queries = [
            "employee training duration",
            "how long is training",
            "onboarding time",
            "training materials",
            "employee development"
        ]
        
        print("🔍 Testing Pinecone search with different queries...\n")
        
        for query in test_queries:
            print(f"📝 Query: '{query}'")
            
            # Create embedding
            embedding_response = openai_client.embeddings.create(
                input=query,
                model="text-embedding-ada-002"
            )
            query_embedding = embedding_response.data[0].embedding
            
            # Search Pinecone
            search_results = index.query(
                vector=query_embedding,
                top_k=3,
                include_metadata=True
            )
            
            if search_results.matches:
                print(f"✅ Found {len(search_results.matches)} results:")
                for i, match in enumerate(search_results.matches, 1):
                    title = match.metadata.get('title', 'No title')
                    content = match.metadata.get('content', 'No content')
                    score = match.score
                    print(f"   {i}. {title} (Score: {score:.3f})")
                    print(f"      {content[:100]}...")
            else:
                print("❌ No results found")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Pinecone Search Test")
    print("=" * 40)
    test_pinecone_search()