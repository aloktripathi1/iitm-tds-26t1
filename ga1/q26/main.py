import time
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

from cache import cache
from analytics import analytics
from config import AVG_TOKENS_PER_REQUEST
from embeddings import embed
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Clear cache on startup for fresh testing
    cache.store.clear()
    analytics.total_requests = 0
    analytics.cache_hits = 0
    analytics.cache_misses = 0
    analytics.cached_tokens = 0
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    application: str

@app.post("/")
def query_ai(req: QueryRequest):
    start = time.time()
    normalized = cache.normalize(req.query)

    # 1. Exact cache
    answer = cache.get_exact(normalized)
    if answer:
        latency = max(1, int((time.time() - start) * 1000))
        analytics.record_hit(latency, AVG_TOKENS_PER_REQUEST)
        return {
            "answer": answer,
            "cached": True,
            "latency": latency,
            "cacheKey": "exact"
        }

    # 2. Semantic cache
    emb = embed(normalized)
    answer = cache.get_semantic(emb)
    if answer:
        latency = max(1, int((time.time() - start) * 1000))
        analytics.record_hit(latency, AVG_TOKENS_PER_REQUEST)
        return {
            "answer": answer,
            "cached": True,
            "latency": latency,
            "cacheKey": "semantic"
        }

    # 3. LLM call (simulated with realistic latency)
    time.sleep(2)  # simulate realistic LLM API latency
    answer = f"Summary for: {req.query}"

    cache.set(normalized, answer)

    latency = int((time.time() - start) * 1000)
    analytics.record_miss(latency)

    return {
        "answer": answer,
        "cached": False,
        "latency": latency,
        "cacheKey": None
    }

@app.get("/analytics")
def get_analytics():
    report = analytics.report()
    report["cacheSize"] = len(cache.store)
    report["strategies"] = [
        "exact match",
        "semantic similarity",
        "LRU eviction",
        "TTL expiration"
    ]
    return report

@app.post("/reset")
def reset_cache():
    cache.store.clear()
    analytics.total_requests = 0
    analytics.cache_hits = 0
    analytics.cache_misses = 0
    analytics.cached_tokens = 0
    return {"status": "reset", "message": "Cache and analytics cleared"}
