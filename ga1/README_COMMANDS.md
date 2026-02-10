# Setup Commands FOR Q18,19,24,26,27,28,31

## Q18: Semantic Search
```bash
cd ga1/q18/semantic-search
python app.py
# Runs on http://localhost:5000
```

## Q19: Vector Similarity API
```bash
cd ga1/q19/vector-similarity-api
uvicorn app.main:app --reload --port 8000
# Runs on http://localhost:8000
```

## Q24: AI Pipeline
```bash
cd ga1/q24/ai-pipeline
python -m uvicorn main:app --reload --port 8001
# Runs on http://localhost:8001
```

## Q26: AI Caching
```bash
cd ga1/q26
python -m uvicorn main:app --reload --port 8005
# Runs on http://localhost:8005
```

## Q27: Security Validation
```bash
cd ga1/q27
python -m uvicorn main:app --reload --port 8003
# Runs on http://localhost:8003
```

## Q28: Streaming LLM
```bash
cd ga1/q28
python -m uvicorn main:app --reload --port 8004
# Runs on http://localhost:8004
```

## Cloudflare Tunnels (For Public URLs)
Run these in separate terminals to expose your local servers. Note: Free tunnels generate a new random URL each time you restart them.

```bash
# Q19 (Port 8000)
cloudflared tunnel --url http://localhost:8000

# Q24 (Port 8001)
cloudflared tunnel --url http://localhost:8001

# Q26 (Port 8005)
cloudflared tunnel --url http://localhost:8005

# Q27 (Port 8003)
cloudflared tunnel --url http://localhost:8003

# Q28 (Port 8004)
cloudflared tunnel --url http://localhost:8004
```
