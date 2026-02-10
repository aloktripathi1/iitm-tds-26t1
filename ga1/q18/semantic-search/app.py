from flask import Flask, request, jsonify
from flask_cors import CORS
from search import SemanticSearchEngine
from config import Config

app = Flask(__name__)
CORS(app)

# Initialize search engine (loads documents and embeddings)
print("Initializing search engine...")
search_engine = SemanticSearchEngine()
print("✓ Search engine ready!\n")

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'documents': len(search_engine.documents)
    })

@app.route('/search', methods=['POST'])
def search():
    """
    Semantic search endpoint with optional re-ranking.
    
    Request body:
    {
        "query": "how to authenticate",
        "k": 5,
        "rerank": true,
        "rerankK": 3
    }
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400
        
        query = data['query']
        k = data.get('k', Config.DEFAULT_K)
        rerank = data.get('rerank', True)
        rerank_k = data.get('rerankK', Config.DEFAULT_RERANK_K)
        
        # Validate parameters
        if k < 1 or k > 20:
            return jsonify({'error': 'k must be between 1 and 20'}), 400
        
        if rerank_k < 1 or rerank_k > k:
            return jsonify({'error': f'rerankK must be between 1 and {k}'}), 400
        
        # Perform search
        results = search_engine.search(
            query=query,
            k=k,
            rerank=rerank,
            rerank_k=rerank_k
        )
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/documents', methods=['GET'])
def get_documents():
    """Get all documents (for debugging)."""
    return jsonify({
        'total': len(search_engine.documents),
        'documents': search_engine.documents[:10]  # First 10
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)