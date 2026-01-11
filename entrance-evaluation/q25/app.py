# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
# ]
# ///

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import csv
from pathlib import Path

app = FastAPI()

# Enable CORS to allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["GET"],  # Allow GET requests
    allow_headers=["*"],  # Allow all headers
)

# Load students data from CSV file
students_data: List[Dict[str, str | int]] = []

def load_data():
    """Load student data from CSV file"""
    csv_path = Path(__file__).parent / "q-fastapi.csv"
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            students_data.append({
                "studentId": int(row[0]),
                "class": row[1]
            })

# Load data on startup
load_data()

@app.get("/api")
async def get_students(class_filter: List[str] = Query(None, alias="class")) -> Dict[str, List[Dict[str, str | int]]]:
    """
    Get all students or filter by class
    
    Query parameters:
    - class: Filter by one or more classes (e.g., ?class=1A&class=1B)
    """
    if class_filter:
        # Filter students by the specified classes
        filtered_students = [
            student for student in students_data 
            if student["class"] in class_filter
        ]
        return {"students": filtered_students}
    else:
        # Return all students
        return {"students": students_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
