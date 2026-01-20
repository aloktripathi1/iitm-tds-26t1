# Q27: Local Ollama Endpoint Setup

## Task

Set up a local AI server using Ollama and expose it to the internet via ngrok with proper CORS configuration and custom headers for remote access and verification.

---

## Requirements

* Run Ollama locally on port 11434
* Enable CORS to allow cross-origin requests from any origin
* Expose the local server via ngrok tunnel with public HTTPS URL
* Inject custom `X-Email` header in all responses
* Configure proper CORS headers for browser compatibility
* Submit the public ngrok URL for grading

---

## Approach

### 1. Install Ollama
Download and install Ollama to run AI models locally on your machine.

### 2. Download AI Model
Pull a lightweight model suitable for running inference locally.

### 3. Configure CORS
Set environment variable to allow cross-origin requests before starting the server.

### 4. Start Ollama Server
Run Ollama with CORS enabled on localhost:11434.

### 5. Install and Configure ngrok
Set up ngrok to create a secure tunnel from internet to localhost.

### 6. Create Public Tunnel
Run ngrok with custom headers to expose Ollama publicly.

### 7. Verify Setup
Test the public URL to ensure proper connectivity and header injection.

---

## Installation

### Install Ollama

**Download:**
```
Visit: https://ollama.com/download
Download the installer for your operating system
```

**Verify Installation:**
```powershell
ollama --version
```

### Download AI Model

**Pull Model:**
```powershell
ollama pull llama3
```

**Verify Model:**
```powershell
ollama list
```

**Expected Output:**
```
NAME                ID              SIZE      MODIFIED
llama3:latest       a6990ed6be41    4.7 GB    2 minutes ago
```

### Install ngrok

**Download:**
```
Visit: https://ngrok.com/download
Extract ngrok executable to a folder (e.g., C:\ngrok\)
```

**Get Authtoken:**
```
Sign up at: https://ngrok.com
Get authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
```

**Configure ngrok:**
```powershell
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

---

## Execution

### Step 1: Start Ollama Server (Terminal Window 1)

**Set CORS Environment Variable:**
```powershell
$env:OLLAMA_ORIGINS="*"
```

**Start Server:**
```powershell
ollama serve
```

**Expected Output:**
```
Ollama is running on 127.0.0.1:11434
```

**Note:** Keep this terminal window open.

### Step 2: Start ngrok Tunnel (Terminal Window 2)

**Create Public Tunnel:**
```powershell
ngrok http 11434 --response-header-add "X-Email: 23f300XXXX@ds.study.iitm.ac.in" --response-header-add "Access-Control-Expose-Headers: *" --response-header-add "Access-Control-Allow-Headers: Ngrok-skip-browser-warning" --host-header=localhost
```

**Expected Output:**
```
Session Status                online
Account                       23f300XXXX@ds.study.iitm.ac.in (Plan: Free)
Forwarding                    https://random-string.ngrok-free.app -> http://localhost:11434
```

**Note:** Keep this terminal window open as well.

---

## Verification

### Test Local Connection

```powershell
curl http://localhost:11434/api/version
```

**Expected Response:**
```json
{"version":"0.5.8"}
```

### Test Public URL

```powershell
curl https://YOUR-NGROK-URL.ngrok-free.app/api/version
```

**Expected Response:**
```json
{"version":"0.5.8"}
```

---

## Common Issues

### Issue 1: Port Already in Use

**Problem:**
```
Error: listen tcp 127.0.0.1:11434: bind: address already in use
```

**Cause:** Ollama is already running as a background service.

**Solution:**
* Option 1: Use the existing instance (skip `ollama serve` and proceed to ngrok)
* Option 2: Stop the existing service and restart with CORS enabled

### Issue 2: CORS Not Configured

**Problem:** Assignment checker reports CORS errors.

**Cause:** `OLLAMA_ORIGINS` environment variable not set.

**Solution:**
Ensure `$env:OLLAMA_ORIGINS="*"` is set **before** running `ollama serve` in the same terminal session.

### Issue 3: ngrok Cannot Connect

**Problem:** Testing ngrok URL returns HTML error page instead of JSON.

**Cause:** Ollama server not running or not accessible.

**Solution:**
1. Verify Ollama is running: `curl http://localhost:11434/api/version`
2. Ensure ngrok command includes `--host-header=localhost` flag
3. Check both terminal windows are still open

---

## Configuration Details

### CORS Setup

```powershell
$env:OLLAMA_ORIGINS="*"
```
Allows requests from any origin, enabling browser-based access.

### ngrok Flags Explained

* `--response-header-add "X-Email: ..."` - Identifies submission for grading
* `--response-header-add "Access-Control-Expose-Headers: *"` - Allows JavaScript to read all response headers
* `--response-header-add "Access-Control-Allow-Headers: Ngrok-skip-browser-warning"` - Permits custom header to bypass ngrok browser warning
* `--host-header=localhost` - Ensures Ollama sees requests as from localhost (prevents 403 errors)

---

## Submission

**Your Public URL:**
```
https://random-string.ngrok-free.app
```

Copy the HTTPS forwarding URL from ngrok and submit it to the assignment platform.

**Important:** Keep both terminal windows (Ollama and ngrok) running until grading is complete.

---

## Architecture

**Request Flow:**
```
Internet → ngrok Tunnel → localhost:11434 → Ollama Server
```

**Response Flow:**
```
Ollama Server → ngrok (injects custom headers) → Internet
```

**Components:**
* **Ollama** - Local LLM server running AI models
* **ngrok** - Secure tunnel service exposing localhost to internet
* **CORS** - Enables cross-origin browser requests
* **Custom Headers** - Tracks and verifies submissions

---

## Summary

This setup demonstrates how to:
* Run AI models locally with Ollama
* Expose local services securely via ngrok
* Configure CORS for web API access
* Inject custom HTTP headers for tracking

**Result:** A publicly accessible AI API endpoint running entirely on your local machine with proper security and verification headers.

