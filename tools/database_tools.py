# tools/database_tools.py
from typing import Dict, Any, List
from google.generativeai.types import FunctionDeclaration, Tool
import json
import uuid
import datetime
import sqlite3
import chromadb

# SQLite Operations
def save_claim_data(claim_id: str, data_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Save claim data to SQLite database."""
    conn = sqlite3.connect('wc_claims.db')
    cursor = conn.cursor()
    
    data_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO extracted_data (data_id, claim_id, data_type, data_json, timestamp) VALUES (?, ?, ?, ?, ?)",
        (data_id, claim_id, data_type, json.dumps(data), timestamp)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "data_id": data_id,
        "timestamp": timestamp
    }

def retrieve_claim_data(claim_id: str, data_type: str = None) -> Dict[str, Any]:
    """Retrieve claim data from SQLite database."""
    conn = sqlite3.connect('wc_claims.db')
    cursor = conn.cursor()
    
    if data_type:
        cursor.execute(
            "SELECT data_id, data_type, data_json FROM extracted_data WHERE claim_id = ? AND data_type = ? ORDER BY timestamp DESC",
            (claim_id, data_type)
        )
    else:
        cursor.execute(
            "SELECT data_id, data_type, data_json FROM extracted_data WHERE claim_id = ? ORDER BY timestamp DESC",
            (claim_id,)
        )
    
    results = cursor.fetchall()
    conn.close()
    
    # Format results
    formatted_results = {}
    for data_id, data_type, data_json in results:
        if data_type not in formatted_results:
            formatted_results[data_type] = []
        
        formatted_results[data_type].append({
            "data_id": data_id,
            "data": json.loads(data_json)
        })
    
    return formatted_results

# ChromaDB Operations
def save_to_vector_db(text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Save text to ChromaDB for vector search."""
    client = chromadb.Client()
    collection_name = metadata.get("collection", "general")
    
    # Get or create collection
    try:
        collection = client.get_collection(collection_name)
    except:
        collection = client.create_collection(collection_name)
    
    # Generate ID
    doc_id = str(uuid.uuid4())
    
    # Add to collection
    collection.add(
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id]
    )
    
    return {
        "status": "success",
        "doc_id": doc_id,
        "collection": collection_name
    }

def search_vector_db(query: str, metadata_filter: Dict[str, Any] = None, limit: int = 5) -> List[Dict[str, Any]]:
    """Search ChromaDB for relevant documents."""
    client = chromadb.Client()
    collection_name = metadata_filter.get("collection", "general") if metadata_filter else "general"
    
    try:
        collection = client.get_collection(collection_name)
    except:
        return []
    
    # Prepare metadata filter
    where_clause = {}
    if metadata_filter:
        for key, value in metadata_filter.items():
            if key != "collection":
                where_clause[key] = value
    
    # Perform search
    results = collection.query(
        query_texts=[query],
        where=where_clause if where_clause else None,
        n_results=limit
    )
    
    # Format results
    formatted_results = []
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        formatted_results.append({
            "document": doc,
            "metadata": metadata,
            "id": results['ids'][0][i],
            "score": 1.0 - (i / limit)  # Approximate score based on position
        })
    
    return formatted_results

# Define function declarations for these tools
database_tools = [
    Tool(
        function_declarations=[
            FunctionDeclaration(
                name="save_claim_data",
                description="Save claim data to the database",
                parameters={
                    "type": "object",
                    "properties": {
                        "claim_id": {"type": "string", "description": "The unique ID of the claim"},
                        "data_type": {"type": "string", "description": "Type of data (claimant, employer, medical, etc.)"},
                        "data": {"type": "object", "description": "The data to save"}
                    },
                    "required": ["claim_id", "data_type", "data"]
                }
            ),
            FunctionDeclaration(
                name="retrieve_claim_data",
                description="Retrieve claim data from the database",
                parameters={
                    "type": "object",
                    "properties": {
                        "claim_id": {"type": "string", "description": "The unique ID of the claim"},
                        "data_type": {"type": "string", "description": "Optional type of data to retrieve"}
                    },
                    "required": ["claim_id"]
                }
            ),
            FunctionDeclaration(
                name="save_to_vector_db",
                description="Save text to vector database for semantic search",
                parameters={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to be stored"},
                        "metadata": {"type": "object", "description": "Metadata for the text (claim_id, type, etc.)"}
                    },
                    "required": ["text", "metadata"]
                }
            ),
            FunctionDeclaration(
                name="search_vector_db",
                description="Search vector database for relevant documents",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "metadata_filter": {"type": "object", "description": "Filter by metadata"},
                        "limit": {"type": "integer", "description": "Maximum number of results"}
                    },
                    "required": ["query"]
                }
            )
        ]
    )
]
