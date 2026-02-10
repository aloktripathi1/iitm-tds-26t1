import pickle
import os
from openai import OpenAI
from config import Config
import numpy as np

# Initialize OpenAI client with aipipe.org base URL
client = OpenAI(
    api_key=Config.AIPIPE_TOKEN,
    base_url=Config.AIPIPE_BASE_URL
)

def get_embedding(text, model=Config.EMBEDDING_MODEL):
    """
    Get embedding for a single text using aipipe.org API.
    """
    text = text.replace("\n", " ")
    try:
        response = client.embeddings.create(
            input=[text],
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        raise

def get_embeddings_batch(texts, model=Config.EMBEDDING_MODEL):
    """
    Get embeddings for multiple texts in a batch (more efficient).
    """
    texts = [text.replace("\n", " ") for text in texts]
    try:
        response = client.embeddings.create(
            input=texts,
            model=model
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"Error getting batch embeddings: {e}")
        raise

def compute_document_embeddings(documents):
    """
    Compute embeddings for all documents.
    """
    print(f"Computing embeddings for {len(documents)} documents using aipipe.org...")
    
    # Batch process for efficiency
    batch_size = Config.EMBEDDING_BATCH_SIZE
    all_embeddings = []
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        texts = [doc['content'] for doc in batch]
        
        print(f"Processing batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        embeddings = get_embeddings_batch(texts)
        all_embeddings.extend(embeddings)
    
    print("✓ Embeddings computed successfully!")
    return all_embeddings

def save_embeddings(embeddings, filepath=Config.EMBEDDINGS_CACHE):
    """
    Save embeddings to disk for reuse.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        pickle.dump(embeddings, f)
    print(f"✓ Embeddings cached to {filepath}")

def load_embeddings(filepath=Config.EMBEDDINGS_CACHE):
    """
    Load cached embeddings from disk.
    """
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'rb') as f:
        embeddings = pickle.load(f)
    print(f"✓ Loaded {len(embeddings)} cached embeddings")
    return embeddings

def cosine_similarity(a, b):
    """
    Compute cosine similarity between two vectors.
    """
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))