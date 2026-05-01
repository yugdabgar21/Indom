# Setup Indom

## Prerequisites
- Python 3.13+
- Node.js 22+
- `uv` (Latest — astral.sh/uv)
- Ollama (Latest — for running Qwen locally)
- pdflatex (TeX Live or MiKTeX — for compiling LaTeX)
- Qwen Model (qwen2.5:7b)
- Docker (for SearXNG)

## 1. Quick Setup Script (Windows)
We have provided a PowerShell script to automatically initialize the Next.js and FastAPI folders. 

Open your VS Code terminal and run:
```powershell
.\setup.ps1
```

## 2. Backend (Terminal 1)
```bash
cd apps/backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

## 3. Frontend (Terminal 2)
```bash
cd apps/frontend
npm install
npm run dev
```

## 4. SearXNG Local Search Engine
```bash
docker-compose up -d
```
