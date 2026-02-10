from openai import OpenAI
from config import Config
import re

# Initialize OpenAI client with aipipe.org base URL
client = OpenAI(
    api_key=Config.AIPIPE_TOKEN,
    base_url=Config.AIPIPE_BASE_URL
)

def rerank_with_llm(query, documents, top_k=3):
    """
    Re-rank documents using LLM-based relevance scoring via aipipe.org.
    Returns top_k documents sorted by relevance.
    """
    print(f"Re-ranking {len(documents)} documents using aipipe.org...")
    
    reranked = []
    
    for doc in documents:
        # Truncate content to save tokens
        content = doc['content'][:Config.MAX_CONTENT_LENGTH]
        
        # Create relevance scoring prompt
        prompt = f"""Query: "{query}"
Document: "{content}"

Rate how relevant this document is to answering the query on a scale of 0-10 where:
- 0 = completely irrelevant
- 5 = somewhat relevant
- 10 = perfectly answers the query

Respond with only the number (e.g., "7" or "8.5")."""

        try:
            response = client.chat.completions.create(
                model=Config.RERANK_MODEL,
                messages=[
                    {"role": "system", "content": "You are a relevance scoring expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=10
            )
            
            # Extract score from response
            score_text = response.choices[0].message.content.strip()
            score = float(re.findall(r'\d+\.?\d*', score_text)[0])
            
            # Normalize to 0-1 range
            normalized_score = min(score / 10.0, 1.0)
            
            reranked.append({
                'id': doc['id'],
                'score': normalized_score,
                'content': doc['content'],
                'title': doc.get('title', ''),
                'metadata': {'source': doc.get('source', 'unknown')}
            })
            
        except Exception as e:
            print(f"Error re-ranking doc {doc['id']}: {e}")
            # Fallback to original score
            reranked.append({
                'id': doc['id'],
                'score': doc.get('score', 0.5),
                'content': doc['content'],
                'title': doc.get('title', ''),
                'metadata': {'source': doc.get('source', 'unknown')}
            })
    
    # Sort by score (descending) and use ID as tiebreaker
    reranked.sort(key=lambda x: (-x['score'], x['id']))
    
    print(f"✓ Re-ranking complete!")
    return reranked[:top_k]

def rerank_batch(query, documents, top_k=3):
    """
    More efficient batch re-ranking (all documents in one LLM call).
    """
    if len(documents) == 0:
        return []
    
    # Build batch prompt
    doc_texts = []
    for i, doc in enumerate(documents, 1):
        content = doc['content'][:Config.MAX_CONTENT_LENGTH]
        doc_texts.append(f"Document {i}: {content}")
    
    prompt = f"""Query: "{query}"

{chr(10).join(doc_texts)}

Rate the relevance of each document to the query (0-10).
Respond ONLY in this format: "1: 8, 2: 6, 3: 9, 4: 7, 5: 5"
"""

    try:
        response = client.chat.completions.create(
            model=Config.RERANK_MODEL,
            messages=[
                {"role": "system", "content": "You are a relevance scoring expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=50
        )
        
        # Parse scores
        scores_text = response.choices[0].message.content.strip()
        scores = {}
        for match in re.finditer(r'(\d+):\s*(\d+\.?\d*)', scores_text):
            doc_num = int(match.group(1))
            score = float(match.group(2)) / 10.0
            scores[doc_num - 1] = score
        
        # Build reranked results
        reranked = []
        for i, doc in enumerate(documents):
            reranked.append({
                'id': doc['id'],
                'score': scores.get(i, 0.5),
                'content': doc['content'],
                'title': doc.get('title', ''),
                'metadata': {'source': doc.get('source', 'unknown')}
            })
        
        reranked.sort(key=lambda x: (-x['score'], x['id']))
        return reranked[:top_k]
        
    except Exception as e:
        print(f"Batch re-ranking failed: {e}, falling back to individual scoring")
        return rerank_with_llm(query, documents, top_k)