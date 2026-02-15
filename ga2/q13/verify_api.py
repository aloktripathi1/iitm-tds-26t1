
import requests
import sys

try:
    print("Testing API...")
    
    # Test 1: All students
    r = requests.get("http://127.0.0.1:8000/api")
    if r.status_code != 200:
        print(f"FAIL: Status code {r.status_code}")
        sys.exit(1)
    data = r.json()
    if 'students' not in data:
        print("FAIL: 'students' key missing")
        sys.exit(1)
    print(f"Total students: {len(data['students'])}")

    # Test 2: Filter class=1A
    r = requests.get("http://127.0.0.1:8000/api?class=1A")
    data = r.json()
    classes = set(s['class'] for s in data['students'])
    if classes and classes != {'1A'}:
        print(f"FAIL: Expected only class 1A, got {classes}")
        sys.exit(1)
    print(f"Class 1A count: {len(data['students'])}")

    # Test 3: Multiple classes
    r = requests.get("http://127.0.0.1:8000/api?class=1A&class=1B")
    data = r.json()
    classes = set(s['class'] for s in data['students'])
    if classes and not classes.issubset({'1A', '1B'}):
        print(f"FAIL: Expected 1A/1B, got {classes}")
        sys.exit(1)
    print(f"Class 1A+1B count: {len(data['students'])}")

    # Test 4: CORS
    if r.headers.get('access-control-allow-origin') != '*':
        print(f"WARNING: CORS header might be missing: {r.headers.get('access-control-allow-origin')}")
    else:
        print("CORS verified.")

    print("ALL TESTS PASSED")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
