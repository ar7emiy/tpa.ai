# database/vector/operations.py
import chromadb
from typing import Dict, List, Any

def init_chromadb():
    """Initialize ChromaDB with required collections."""
    client = chromadb.Client()
    
    # Create collections for different content types
    conversations = client.create_collection(
        name="conversations",
        metadata={"description": "Stakeholder conversations"}
    )
    
    medical_documents = client.create_collection(
        name="medical_documents",
        metadata={"description": "Medical reports and records"}
    )
    
    employment_documents = client.create_collection(
        name="employment_documents",
        metadata={"description": "Employment verification documents"}
    )
    
    return client

def store_conversation(client, claim_id: str, conversation_data: Dict[str, Any]):
    """Store a conversation in ChromaDB for semantic search."""
    collection = client.get_collection("conversations")
    
    # Extract text from conversation
    if "conversation_text" in conversation_data:
        text = conversation_data["conversation_text"]
    else:
        # Format conversation transcript into text
        text = "\n".join([
            f"{msg['speaker']}: {msg['text']}" 
            for msg in conversation_data.get("conversation_transcript", [])
        ])
    
    # Create metadata
    metadata = {
        "claim_id": claim_id,
        "stakeholder_type": conversation_data.get("stakeholder_type", "unknown"),
        "timestamp": conversation_data.get("timestamp", "")
    }
    
    # Store in ChromaDB
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[f"{claim_id}_{conversation_data.get('stakeholder_type', 'unknown')}_{conversation_data.get('timestamp', '')}"]
    )
