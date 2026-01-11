# Q25: FastAPI Server to Serve Student Data

## Task
Write a FastAPI server that serves student data from `q-fastapi.csv` file. The CSV contains 2 columns:
- `studentId`: Unique identifier (e.g., 1, 2, 3, ...)
- `class`: Student's class including section (e.g., 1A, 1B, 12A, 12B, 12Z)

### Requirements
- `/api` endpoint returns all students data in JSON format: `{"students": [{"studentId": 1, "class": "1A"}, ...]}`
- Support filtering by class using query parameter: `/api?class=1A`
- Support multiple class filters: `/api?class=1A&class=1B`
- Return students in the same order as they appear in CSV file
- Enable CORS to allow GET requests from any origin

## Approach
1. **Load CSV Data**: Read `q-fastapi.csv` on server startup using Python's `csv` module
2. **Store in Memory**: Keep data in a list of dictionaries for fast access
3. **Create API Endpoint**: Define `/api` GET endpoint with optional query parameter filtering
4. **Enable CORS**: Use FastAPI's `CORSMiddleware` to allow all origins for GET requests
5. **Filter Logic**: When class filters provided, return only matching students in original order

## Commands

### Install Dependencies
```bash
pip install fastapi uvicorn
```

### Run Server
```bash
python3 app.py
```

Or with uv (if installed):
```bash
uv run app.py
```

### Test API

Get all students:
```bash
curl http://127.0.0.1:8000/api
```

Filter by single class:
```bash
curl http://127.0.0.1:8000/api?class=1A
```

Filter by multiple classes:
```bash
curl "http://127.0.0.1:8000/api?class=1A&class=1B"
```

## API Endpoint
- **Local**: `http://127.0.0.1:8000/api`
- **Codespaces**: Check PORTS tab for forwarded URL (e.g., `https://<codespace>-8000.app.github.dev/api`)

## Implementation Details
- **Framework**: FastAPI (modern Python web framework)
- **Server**: Uvicorn (ASGI server)
- **Data Loading**: CSV module with Path for file handling
- **Type Hints**: Full type annotations for request/response
- **CORS**: Configured to allow all origins (*) for GET requests
- **Query Parameters**: Uses FastAPI's Query with alias for `class` parameter
