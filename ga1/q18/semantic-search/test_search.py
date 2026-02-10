import requests
import json

BASE_URL = 'http://localhost:5000'

def test_health():
    """Test health endpoint."""
    response = requests.get(f'{BASE_URL}/health')
    print("Health Check:", response.json())

def test_search(query, k=5, rerank=True, rerank_k=3):
    """Test search endpoint."""
    print(f"\n{'='*60}")
    print(f"Query: '{query}'")
    print(f"{'='*60}")
    
    payload = {
        'query': query,
        'k': k,
        'rerank': rerank,
        'rerankK': rerank_k
    }
    
    response = requests.post(f'{BASE_URL}/search', json=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"\nReranked: {data['reranked']}")
        print(f"Latency: {data['metrics']['latency']}ms")
        print(f"Total Docs: {data['metrics']['totalDocs']}")
        print(f"\nTop {len(data['results'])} Results:")
        print("-" * 60)
        
        for i, result in enumerate(data['results'], 1):
            print(f"\n{i}. Score: {result['score']:.4f}")
            print(f"   Title: {result['metadata']['title']}")
            print(f"   Content: {result['content'][:150]}...")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

def run_tests():
    """Run test suite."""
    print("\n🧪 Starting Search Tests\n")
    
    # Test 1: Authentication query
    test_search("how to authenticate API requests", rerank=True)
    
    # Test 2: Error handling query
    test_search("what error codes does the API return", rerank=True)
    
    # Test 3: Without re-ranking
    test_search("rate limiting", k=5, rerank=False)
    
    # Test 4: Empty query handling
    test_search("", rerank=True)

if __name__ == '__main__':
    test_health()
    run_tests()