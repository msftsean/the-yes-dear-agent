#!/usr/bin/env python3
"""
Pinecone Document Upload Script
Uploads sample documents to Pinecone for testing document search functionality
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import time

# Load environment variables
load_dotenv()

def upload_documents_to_pinecone():
    """Upload sample documents to Pinecone index for testing"""
    
    # Check for required API keys
    openai_key = os.environ.get("OPENAI_API_KEY")
    pinecone_key = os.environ.get("PINECONE_API_KEY")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in .env file")
        return False
        
    if not pinecone_key:
        print("❌ PINECONE_API_KEY not found in .env file")
        return False
    
    try:
        # Import and initialize Pinecone
        from pinecone import Pinecone, ServerlessSpec
        pc = Pinecone(api_key=pinecone_key)
        
        # Initialize OpenAI for embeddings
        openai_client = OpenAI(api_key=openai_key)
        
        # Index configuration
        index_name = "documents"
        dimension = 1536  # OpenAI embedding dimension
        
        print(f"🔍 Checking for existing index '{index_name}'...")
        
        # Create index if it doesn't exist or recreate if wrong dimension
        existing_indexes = [idx.name for idx in pc.list_indexes()]
        if index_name not in existing_indexes:
            print(f"🆕 Creating new index '{index_name}'...")
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print("⏳ Waiting for index to be ready...")
            time.sleep(60)  # Wait for index to initialize
        else:
            # Check if existing index has correct dimension
            index_info = pc.describe_index(index_name)
            existing_dimension = index_info.dimension
            if existing_dimension != dimension:
                print(f"⚠️ Existing index has dimension {existing_dimension}, but we need {dimension}")
                print(f"🗑️ Deleting existing index '{index_name}'...")
                pc.delete_index(index_name)
                print("⏳ Waiting for deletion to complete...")
                time.sleep(30)
                
                print(f"🆕 Creating new index '{index_name}' with correct dimension...")
                pc.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                print("⏳ Waiting for index to be ready...")
                time.sleep(60)
            else:
                print(f"✅ Index '{index_name}' already exists with correct dimension")
        
        # Connect to index
        index = pc.Index(index_name)
        
        # Get sample documents
        docs_dir = Path("sample_documents")
        if not docs_dir.exists():
            print(f"❌ Sample documents directory not found: {docs_dir}")
            return False
        
        # Process each document
        documents = []
        doc_files = list(docs_dir.glob("*.txt"))
        
        if not doc_files:
            print(f"❌ No .txt files found in {docs_dir}")
            return False
        
        print(f"📚 Processing {len(doc_files)} documents...")
        
        for doc_file in doc_files:
            print(f"  📄 Processing {doc_file.name}...")
            
            # Read document content
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create embedding using OpenAI
            try:
                embedding_response = openai_client.embeddings.create(
                    input=content,
                    model="text-embedding-ada-002"
                )
                embedding = embedding_response.data[0].embedding
                
                # Prepare document for Pinecone
                doc_id = doc_file.stem  # filename without extension
                metadata = {
                    "title": doc_file.stem.replace("_", " ").title(),
                    "content": content[:500] + "..." if len(content) > 500 else content,  # Truncate for demo
                    "full_content": content,
                    "filename": doc_file.name,
                    "word_count": len(content.split()),
                    "type": "document"
                }
                
                documents.append({
                    "id": doc_id,
                    "values": embedding,
                    "metadata": metadata
                })
                
                print(f"    ✅ Embedded {doc_file.name} ({len(content)} chars)")
                
            except Exception as e:
                print(f"    ❌ Error embedding {doc_file.name}: {e}")
                continue
        
        # Upload to Pinecone
        if documents:
            print(f"🚀 Uploading {len(documents)} documents to Pinecone...")
            
            # Upsert documents in batches
            batch_size = 10
            for i in range(0, len(documents), batch_size):
                batch = documents[i:i + batch_size]
                index.upsert(vectors=batch)
                print(f"  📤 Uploaded batch {i//batch_size + 1}")
            
            print("✅ All documents uploaded successfully!")
            
            # Test search
            print("\\n🔍 Testing search functionality...")
            test_query = "vacation policy"
            
            # Create test embedding
            test_embedding_response = openai_client.embeddings.create(
                input=test_query,
                model="text-embedding-ada-002"
            )
            test_embedding = test_embedding_response.data[0].embedding
            
            # Search Pinecone
            search_results = index.query(
                vector=test_embedding,
                top_k=3,
                include_metadata=True
            )
            
            print(f"\\n📋 Search results for '{test_query}':")
            for match in search_results.matches:
                print(f"  📄 {match.metadata['title']} (Score: {match.score:.3f})")
                print(f"     {match.metadata['content'][:100]}...")
            
            print(f"\\n🎉 Setup complete! Your Pinecone index '{index_name}' is ready for testing.")
            print("\\n💡 Now you can:")
            print("   1. Toggle 'Real APIs' ON in your Streamlit app")
            print("   2. Enable 'Document Search' in the sidebar")
            print("   3. Try queries like:")
            print("      - 'vacation policy'")
            print("      - 'API documentation'")
            print("      - 'meeting notes'")
            print("      - 'financial report'")
            print("      - 'training materials'")
            
            return True
        else:
            print("❌ No documents were successfully processed")
            return False
            
    except ImportError:
        print("❌ Pinecone package not installed. Run: pip install pinecone-client")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Pinecone Document Upload Script")
    print("=" * 50)
    success = upload_documents_to_pinecone()
    
    if success:
        print("\\n🎯 Ready for your demo!")
    else:
        print("\\n😞 Upload failed. Check the errors above.")