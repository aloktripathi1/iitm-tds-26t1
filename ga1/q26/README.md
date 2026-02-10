# AI Caching System

Intelligent caching for LLM responses with exact match, semantic similarity, LRU eviction, and TTL expiration.

## 🚀 Endpoint URLs

```
POST http://localhost:8001/
GET  http://localhost:8001/analytics
```

## 📋 Setup

```bash
cd q26
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

## 📡 API Usage

### Query Endpoint
```bash
curl -X POST http://localhost:8001/ \
  -H "Content-Type: application/json" \
  -d '{"query": "summarize document", "application": "document summarizer"}'
```

**Response:**
```json
{
  "answer": "Summary for: summarize document",
  "cached": true,
  "latency": 0,
  "cacheKey": "exact"
}
```

### Analytics Endpoint
```bash
curl http://localhost:8001/analytics
```

**Response:**
```json
{
  "hitRate": 0.12,
  "totalRequests": 3222,
  "cacheHits": 386,
  "cacheMisses": 2835,
  "cacheSize": 1500,
  "costSavings": 1.00,
  "savingsPercent": 12,
  "strategies": ["exact match", "semantic similarity", "LRU eviction", "TTL expiration"]
}
```

## 🎯 Caching Strategies

| Strategy | Description |
|----------|-------------|
| **Exact Match** | MD5 hash of normalized query |
| **Semantic** | Embedding cosine similarity > 0.95 |
| **LRU Eviction** | Removes least recently used when full |
| **TTL Expiration** | 24-hour cache lifetime |

## ⚙️ Configuration

Edit `config.py`:
- `CACHE_MAX_SIZE`: 1500 entries
- `CACHE_TTL_SECONDS`: 86400 (24 hours)
- `EMBEDDING_SIM_THRESHOLD`: 0.95
