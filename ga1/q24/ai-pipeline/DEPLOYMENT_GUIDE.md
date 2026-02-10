# Making Your API Publicly Accessible

## Problem
Your server runs on `http://localhost:8000/pipeline` but the grading system cannot reach it because localhost is only accessible from your computer.

## Solution: Expose Your Local Server

### Option 1: ngrok (Recommended - Fastest)

**Steps:**
1. Download ngrok from https://ngrok.com/download
2. Extract the zip file
3. Open a NEW terminal (keep your server running in the current one)
4. Navigate to where you extracted ngrok
5. Run:
   ```bash
   ngrok http 8000
   ```
6. Copy the public URL from the output (looks like `https://xxxx.ngrok-free.app`)
7. Your endpoint will be: `https://xxxx.ngrok-free.app/pipeline`

**Example ngrok output:**
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
```
Your endpoint: `https://abc123.ngrok-free.app/pipeline`

### Option 2: Railway (Free, Permanent Deployment)

**Steps:**
1. Go to https://railway.app and create account
2. Click "New Project" → "Deploy from GitHub" or "Empty Project"
3. Upload your `ga1/q24/ai-pipeline` folder
4. Add environment variables from `.env` file
5. Railway will provide a public URL
6. Your endpoint: `https://your-app.railway.app/pipeline`

### Option 3: Render (Free, Permanent Deployment)

**Steps:**
1. Go to https://render.com and create account
2. Click "New" → "Web Service"
3. Connect GitHub or upload files
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python main.py`
6. Add environment variables
7. Your endpoint: `https://your-app.onrender.com/pipeline`

## Current Status
✅ Server running locally on port 8000
✅ All 4 pipeline stages working
❌ Not publicly accessible (localhost only)

## Next Steps
Choose one option above and follow the steps to get a public URL.
