# Q14: Vercel FastAPI Latency

## Overview
This is a FastAPI application that provides latency analysis for different regions based on telemetry data. It is designed to be deployed on Vercel.

## Project Structure
-   `api/index.py`: The main FastAPI application.
-   `telemetry.json`: Sample data containing latency and uptime records.
-   `vercel.json`: Configuration for Vercel deployment.
-   `requirements.txt`: Python dependencies (`fastapi`, `uvicorn`).

## API Usage

### Endpoint
`POST /`

### Request Body
```json
{
  "regions": ["us-east-1", "eu-west-1"],
  "threshold_ms": 200
}
```

### Response
```json
{
  "regions": {
    "us-east-1": {
      "avg_latency": 150.5,
      "p95_latency": 210.2,
      "avg_uptime": 99.9,
      "breaches": 5
    }
  }
}
```

## Local Development

1.  **Install Dependencies**:
    ```bash
    pip install fastapi uvicorn
    ```

2.  **Run Locally**:
    ```bash
    uvicorn api.index:app --reload
    ```

3.  **Test**:
    ```bash
    curl -X POST "http://127.0.0.1:8000/" \
         -H "Content-Type: application/json" \
         -d '{"regions": ["us-east-1"], "threshold_ms": 200}'
    ```

## Deployment to Vercel

1.  **Install Vercel CLI**: `npm i -g vercel`
2.  **Login**: `vercel login`
3.  **Deploy**: Run `vercel` in this directory.
    -   Link to existing project: No
    -   Link to existing settings: No
    -   Link to existing codebase: No
4.  **Production Deployment**: `vercel --prod`

## Note on File Paths
The application loads `telemetry.json` from the root directory. On Vercel, ensure the file is included in the build output. The current `vercel.json` and file structure are set up for standard Vercel python builds.