import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_similarity():
    """Test the similarity endpoint"""
    
    # Sample documents
    docs = [
        "Python is a high-level programming language known for its simplicity and readability.",
        "JavaScript is primarily used for web development and runs in browsers.",
        "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
        "The quick brown fox jumps over the lazy dog.",
        "Authentication is the process of verifying a user's identity before granting access to a system."
    ]
    
    # Test query
    query = "How do I verify user identity?"
    
    print("="*60)
    print("Testing Vector Similarity API")
    print("="*60)
    print(f"\nQuery: '{query}'")
    print(f"\nDocuments to search: {len(docs)}")
    print("\n" + "-"*60)
    
    # Make request
    payload = {
        "docs": docs,
        "query": query
    }
    
    response = requests.post(
        f"{BASE_URL}/similarity",
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\nTop 3 Matches:")
        print("-"*60)
        for i, match in enumerate(result['matches'], 1):
            print(f"\n{i}. {match}")
        print("\n" + "="*60)
        print("✓ Test passed!")
    else:
        print(f"\n✗ Error: {response.status_code}")
        print(response.text)

def test_health():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print("\nHealth Check:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_health()
    test_similarity()