import json
import time
from embeddings import (
    get_embedding, 
    compute_document_embeddings,
    save_embeddings,
    load_embeddings,
    cosine_similarity
)
from reranker import rerank_batch
from config import Config

class SemanticSearchEngine:
    def __init__(self):
        self.documents = []
        self.embeddings = []
        self.load_documents()
        self.load_or_compute_embeddings()
    
    def load_documents(self):
        """Load documents from JSON file."""
        print("Loading documents...")
        with open(Config.DATA_PATH, 'r') as f:
            self.documents = json.load(f)
        print(f"✓ Loaded {len(self.documents)} documents")
    
    def load_or_compute_embeddings(self):
        """Load cached embeddings or compute new ones."""
        self.embeddings = load_embeddings()
        
        if self.embeddings is None:
            print("No cached embeddings found. Computing...")
            self.embeddings = compute_document_embeddings(self.documents)
            save_embeddings(self.embeddings)
        
        print(f"✓ Ready with {len(self.embeddings)} document embeddings")
    
    def vector_search(self, query_embedding, k=5):
        """
        Perform vector similarity search.
        Returns top k documents with cosine similarity scores.
        """
        similarities = []
        
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = cosine_similarity(query_embedding, doc_embedding)
            similarities.append({
                'id': self.documents[i]['id'],
                'score': float(similarity),
                'content': self.documents[i]['content'],
                'title': self.documents[i].get('title', ''),
                'source': self.documents[i].get('source', '')
            })
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: (-x['score'], x['id']))
        
        return similarities[:k]
    
    def search(self, query, k=5, rerank=True, rerank_k=3):
        """
        Main search function with optional re-ranking.
        """
        start_time = time.time()
        
        # Handle empty query
        if not query or query.strip() == '':
            return {
                'results': [],
                'reranked': False,
                'metrics': {
                    'latency': 0,
                    'totalDocs': len(self.documents)
                }
            }
        
        # Step 1: Vector search (fast retrieval)
        print(f"\n🔍 Searching for: '{query}'")
        query_embedding = get_embedding(query)
        candidates = self.vector_search(query_embedding, k=k)
        
        print(f"✓ Found {len(candidates)} candidates")
        
        # Step 2: Re-ranking (optional)
        if rerank and len(candidates) > 0:
            results = rerank_batch(query, candidates, top_k=rerank_k)
        else:
            results = candidates[:rerank_k]
        
        # Calculate latency
        latency = int((time.time() - start_time) * 1000)  # ms
        
        # Format response
        response = {
            'results': [
                {
                    'id': r['id'],
                    'score': round(r['score'], 4),
                    'content': r['content'],
                    'metadata': {
                        'title': r.get('title', ''),
                        'source': r.get('source', '')
                    }
                }
                for r in results
            ],
            'reranked': rerank,
            'metrics': {
                'latency': latency,
                'totalDocs': len(self.documents)
            }
        }
        
        print(f"✓ Search completed in {latency}ms")
        return response