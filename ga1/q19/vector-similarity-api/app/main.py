from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Vector Similarity API",
    description="API for semantic document similarity search",
    version="1.0.0"
)

# Enable CORS (allows requests from any origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Initialize OpenAI client with aipipe.org
client = OpenAI(
    api_key=os.getenv('AIPIPE_TOKEN'),
    base_url=os.getenv('AIPIPE_BASE_URL', 'https://aipipe.org/openai/v1')
)

# Define request/response models using Pydantic
class SimilarityRequest(BaseModel):
    docs: List[str]  # Array of document texts
    query: str       # Search query

class SimilarityResponse(BaseModel):
    matches: List[str]  # Top 3 matching documents

def get_embedding(text: str) -> List[float]:
    """
    Get embedding for a single text using OpenAI API.
    
    Args:
        text: The text to embed
    
    Returns:
        List of floats representing the embedding
    """
    text = text.replace("\n", " ")  # Clean newlines
    response = client.embeddings.create(
        input=[text],
        model=os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small')
    )
    return response.data[0].embedding

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Compute cosine similarity between two embeddings.
    
    Formula: cos(θ) = (A · B) / (|A| × |B|)
    
    Args:
        a: First embedding vector
        b: Second embedding vector
    
    Returns:
        Similarity score between -1 and 1 (higher = more similar)
    """
    a = np.array(a)
    b = np.array(b)
    
    # Compute dot product and norms
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    # Avoid division by zero
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Vector Similarity API is running",
        "endpoints": {
            "similarity": "POST /similarity",
            "docs": "GET /docs"
        }
    }

@app.post("/similarity", response_model=SimilarityResponse)
def calculate_similarity(request: SimilarityRequest):
    """
    Calculate similarity between query and documents.
    
    Process:
    1. Get embeddings for all documents
    2. Get embedding for query
    3. Calculate cosine similarity between query and each doc
    4. Return top 3 most similar documents
    
    Args:
        request: SimilarityRequest with docs and query
    
    Returns:
        SimilarityResponse with top 3 matching document contents
    """
    try:
        # Step 1: Get embeddings for all documents
        print(f"Processing {len(request.docs)} documents...")
        doc_embeddings = []
        for i, doc in enumerate(request.docs):
            embedding = get_embedding(doc)
            doc_embeddings.append(embedding)
            print(f"  Document {i+1}/{len(request.docs)} embedded")
        
        # Step 2: Get embedding for query
        print(f"Processing query: '{request.query[:50]}...'")
        query_embedding = get_embedding(request.query)
        
        # Step 3: Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(doc_embeddings):
            similarity = cosine_similarity(query_embedding, doc_embedding)
            similarities.append({
                'index': i,
                'content': request.docs[i],
                'similarity': similarity
            })
            print(f"  Document {i+1} similarity: {similarity:.4f}")
        
        # Step 4: Sort by similarity (highest first) and get top 3
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_3 = similarities[:3]
        
        # Extract just the document contents
        matches = [item['content'] for item in top_3]
        
        print(f"✓ Returning top 3 matches")
        
        return SimilarityResponse(matches=matches)
    
    except Exception as e:
        print(f"Error: {e}")
        # Return error but keep API functional
        return SimilarityResponse(matches=[])

@app.options("/similarity")
def options_similarity():
    """Handle OPTIONS request for CORS preflight"""
    return {"message": "OK"}