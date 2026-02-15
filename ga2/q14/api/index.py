from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import statistics

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Load telemetry data
with open("telemetry.json", "r") as f:
    telemetry_data = json.load(f)

class AnalysisRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

class RegionMetrics(BaseModel):
    avg_latency: float
    p95_latency: float
    avg_uptime: float
    breaches: int

@app.post("/")
def analyze(payload: AnalysisRequest):
    results = {}
    
    for region in payload.regions:
        # Filter data for this region
        region_data = [record for record in telemetry_data if record["region"] == region]
        
        if not region_data:
            continue
        
        # Extract latencies and uptimes
        latencies = [record["latency_ms"] for record in region_data]
        uptimes = [record["uptime_pct"] for record in region_data]
        
        # Calculate metrics
        avg_latency = statistics.mean(latencies)
        
        # Calculate 95th percentile using linear interpolation
        sorted_latencies = sorted(latencies)
        n = len(sorted_latencies)
        index = 0.95 * (n - 1)
        lower = int(index)
        upper = lower + 1
        fraction = index - lower
        
        if upper < n:
            p95_latency = sorted_latencies[lower] + fraction * (sorted_latencies[upper] - sorted_latencies[lower])
        else:
            p95_latency = sorted_latencies[lower]
        
        avg_uptime = statistics.mean(uptimes)
        
        # Count breaches (records above threshold)
        breaches = sum(1 for lat in latencies if lat > payload.threshold_ms)
        
        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }
    
    return {"regions": results}

