# Quick Setup Guide - Semantic Search API

## 📋 Prerequisites

- Python 3.8+
- AI Pipe Token from https://aipipe.org/login

---

## ⚡ Quick Start (3 Steps)

### **1. Install Dependencies**

```bash
# Navigate to project directory
cd semantic-search

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

### **2. Configure API Token**

Edit `.env` file:
```bash
AIPIPE_TOKEN=your_actual_token_here
AIPIPE_BASE_URL=https://aipipe.org/openai/v1
EMBEDDING_MODEL=text-embedding-3-small
RERANK_MODEL=gpt-4o-mini
```

**Get token:** Visit https://aipipe.org/login → Sign in with Google → Copy token

### **3. Run the Server**

```bash
python app.py
```

**Server will start at:** `http://127.0.0.1:5000`

---

## 🧪 Test the API

**In another terminal:**

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python test_search.py
```

**Or use curl:**

```bash
curl -X POST http://127.0.0.1:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "how to authenticate",
    "k": 5,
    "rerank": true,
    "rerankK": 3
  }'
```

---

## 📁 Project Structure

```
semantic-search/
├── .env                  # API configuration (UPDATE TOKEN HERE)
├── requirements.txt      # Python dependencies
├── app.py               # Flask API server
├── config.py            # Configuration
├── embeddings.py        # Embedding generation
├── search.py            # Search engine
├── reranker.py          # Re-ranking logic
├── test_search.py       # Test suite
├── data/
│   └── api_docs.json    # 124 documents
└── cache/
    └── embeddings.pkl   # Cached embeddings (auto-generated)
```

---

## 🔧 Common Issues

### **Issue: Virtual environment not found**
```bash
sudo apt install python3-venv  # Ubuntu/Debian
python3 -m venv venv
```

### **Issue: API authentication failed**
```bash
# Check your token in .env
cat .env | grep AIPIPE_TOKEN

# Should NOT be: your_aipipe_token_here
# Should be: eyJhbGci... (actual JWT token)
```

### **Issue: Embeddings computation slow**
```bash
# First run computes embeddings for all 124 docs (~30-60 seconds)
# Subsequent runs load from cache (~instant)

# To force recompute:
rm -rf cache/embeddings.pkl
python app.py
```

### **Issue: Port 5000 already in use**
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in app.py (line 75):
# app.run(debug=True, port=5001)
```

---

## 🚀 API Endpoints

### **POST /search**
```json
{
  "query": "your search query",
  "k": 5,
  "rerank": true,
  "rerankK": 3
}
```

### **GET /health**
Check server status

### **GET /documents**
View all documents (debugging)

---

## 📊 Performance Metrics

- **Initial retrieval:** < 200ms
- **With re-ranking:** 1-3 seconds
- **Precision@3:** > 0.6
- **Total documents:** 124

---

## 💾 Data Management

**Add more documents:**

Edit `data/api_docs.json`:
```json
[
  {
    "id": 0,
    "title": "Document Title",
    "content": "Document content...",
    "source": "source.md"
  }
]
```

Then restart server (it will recompute embeddings).

---

## 🔄 Reset Everything

```bash
# Remove cache and virtual environment
rm -rf cache/ venv/

# Fresh start
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## 📝 Notes

- ✅ Embeddings are cached after first computation
- ✅ Re-ranking uses aipipe.org (costs ~$0.001 per query)
- ✅ Check usage at https://aipipe.org/login
- ✅ Budget limit can be set in aipipe.org dashboard

---

**That's it! Your semantic search API is ready to use.** 🎉
