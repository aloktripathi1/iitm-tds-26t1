# Quick Setup: Make Your API Publicly Accessible

## ✅ Ngrok is Installed!

I've installed ngrok for you. Now follow these steps to get your public URL:

## Step 1: Get Ngrok Auth Token (1 minute)
1. Go to https://dashboard.ngrok.com/signup
2. Sign up (free account)
3. Copy your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken

## Step 2: Configure Ngrok
Open a **NEW** PowerShell terminal and run:
```powershell
& "C:\Users\adity\AppData\Local\Microsoft\WinGet\Packages\Ngrok.Ngrok_Microsoft.Winget.Source_8wekyb3d8bbwe\ngrok.exe" config add-authtoken YOUR_TOKEN_HERE
```
(Replace `YOUR_TOKEN_HERE` with the token from step 1)

## Step 3: Start Ngrok Tunnel
In the same terminal, run:
```powershell
& "C:\Users\adity\AppData\Local\Microsoft\WinGet\Packages\Ngrok.Ngrok_Microsoft.Winget.Source_8wekyb3d8bbwe\ngrok.exe" http 8000
```

## Step 4: Get Your Public URL
You'll see output like:
```
Forwarding  https://abc123-xyz.ngrok-free.app -> http://localhost:8000
```

**Your endpoint is**: `https://abc123-xyz.ngrok-free.app/pipeline`

Copy this URL and paste it into the assignment submission form!

## Important Notes
- Keep BOTH terminals running (your server AND ngrok)
- The ngrok URL changes each time you restart ngrok (free plan)
- Your server is already running on port 8000 ✅
