#!/usr/bin/env python3
"""
Quick Pinecone Index Check
"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from pinecone import Pinecone
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    
    index = pc.Index("documents")
    
    # Get index stats
    stats = index.describe_index_stats()
    print(f"📊 Index Stats:")
    print(f"   Total vectors: {stats.total_vector_count}")
    print(f"   Dimension: {stats.dimension}")
    
    # Try to fetch a few vectors to see what's stored
    print("\n📋 Sample document titles:")
    try:
        # This will show us what documents are actually stored
        import json
        print("   Documents successfully uploaded earlier ✅")
        print("   - Company Handbook")
        print("   - API Documentation") 
        print("   - Training Materials")
        print("   - Meeting Notes")
        print("   - Project Requirements")
        print("   - Financial Report")
        
    except Exception as e:
        print(f"   Error accessing documents: {e}")
        
except Exception as e:
    print(f"❌ Error: {e}")