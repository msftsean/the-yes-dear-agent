#!/usr/bin/env python3
"""
Test the exact search that should work
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

try:
    from pinecone import Pinecone
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index = pc.Index("documents")
    
    # Initialize OpenAI
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Test the exact query
    query = "vacation policy"
    
    print(f"🔍 Testing query: '{query}'")
    
    # Generate embedding
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
            print(f"\n{i}. **{title}** (Score: {score:.3f})")
            print(f"   Content: {content}")
            
        print("\n🎯 This should have been returned by your app!")
    else:
        print("❌ No results found - this is the problem!")
        
except Exception as e:
    print(f"❌ Error: {e}")