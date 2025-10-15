# Test Buddy (scaffold)

This repository contains a scaffold for the Test Buddy project: a Next.js frontend and a FastAPI backend.

Quick start (PowerShell):

1. Backend

```powershell
cd "c:\Users\91991\Desktop\Test Buddy\apps\server"
python -m venv venv; .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

2. Frontend

Install Node.js (16+), then:

```powershell
cd "c:\Users\91991\Desktop\Test Buddy\apps\web"
npm install
npm run dev
```

The frontend expects the backend base URL in `.env.local` as `NEXT_PUBLIC_API_BASE`.
