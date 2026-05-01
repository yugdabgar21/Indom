<div align="center">

<img src="apps/frontend/public/logo.png" alt="Indom Logo" width="120" />

# INDOM.

### Your CV. Their requirements. No mercy.

**AI-powered local CV tailor built by freshers, for freshers.**  
Zero cost. Zero cloud. Zero BS. 100% open source.

[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-green.svg)](https://nextjs.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-green.svg)](CONTRIBUTING.md)

---

*The hiring game is rigged against freshers.*  
*ATS bots filter your CV before a human ever reads it.*  
*Every tool that fixes this costs money.*  

**We're rewriting it.**

---

</div>

## What is Indom?

Indom analyzes your CV against any job description, tailors it to match, generates a professional LaTeX PDF, and gives you a 5-day learning roadmap — all running locally on your machine.

No cloud. No subscriptions. No data leaving your laptop. Ever.

## How It Works

```
Your CV + Job Description
        ↓
   AI Analysis
        ↓
Smart Faking (just enough, fresher-level)
        ↓
LaTeX PDF Generated
        ↓
Faking Warnings + 5-Day Learning Roadmap
        ↓
You walk into that interview prepared
```

**Projects are NEVER modified.** Only skills, keywords, and objective are tailored.  
**Every faked item is flagged.** We tell you exactly what to learn before you apply.

## Features

- **Smart CV Tailoring** — AI maps your existing skills to job requirements
- **Calibrated Faking** — Fresher job = fresher level faking, never over-inflated
- **LaTeX PDF Output** — Cleanest, most ATS-compatible format possible
- **Real-time Progress** — SSE streaming with live progress bar
- **Faking Warning Panel** — Every added skill shown in red, no surprises
- **Match Score** — Before and after score so you see the difference
- **5-Day Learning Roadmap** — Free YouTube and course links via SearXNG
- **Zero Cloud** — Everything runs on your machine, CV data never leaves
- **Multi-Model Support** — OpenRouter, Ollama, OpenAI, Gemini — your choice
- **Settings UI** — Configure your API key and model from the browser, no .env editing

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.10+ | Backend |
| Node.js | 18+ | Frontend |
| uv | Latest | [astral.sh/uv](https://astral.sh/uv) |
| MiKTeX or TeX Live | Latest | For `pdflatex` PDF compilation |
| SearXNG | Latest | Optional — for real learning resource links |

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/yugdabgar21/Indom.git
cd Indom
cp .env.example .env
```

### 2. Start SearXNG (Optional but recommended)

```bash
docker run -d -p 8080:8080 searxng/searxng
```

### 3. Run Backend

```bash
cd apps/backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

### 4. Run Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

### 5. Open and configure

Visit **http://localhost:3000**

Click the ⚙️ settings icon and enter your API key and model details. No .env editing required.

## Configuration

All config lives in `config.yaml` at the root:

```yaml
model:
  provider: openrouter   # openrouter | ollama | openai | gemini
  name: your-model-name
  api_key: your-api-key  # or set via UI settings

searxng:
  url: http://localhost:8080

template: classic        # classic | modern | minimal
```

## Project Structure

```
indom/
├── apps/
│   ├── frontend/          # Next.js 15 + React + TypeScript + Tailwind
│   └── backend/           # FastAPI + Python + LiteLLM
├── docs/                  # Full project documentation
├── searxng/               # SearXNG configuration
├── config.yaml            # Your local config (gitignored)
├── config.yaml.example    # Template config
├── docker-compose.yml
└── .env.example
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python, LiteLLM |
| AI | OpenRouter / Ollama / Any LLM provider |
| PDF | pdflatex (MiKTeX / TeX Live) |
| Search | SearXNG (self-hosted) |
| Storage | TinyDB (local JSON) |

## Why Indom over other tools?

| Feature | Indom | Resume Matcher | Resume.io | Kickresume |
|---------|-------|---------------|-----------|------------|
| Free forever | ✅ | ✅ | ❌ | ❌ |
| Smart faking | ✅ | ❌ | ❌ | ❌ |
| Learning roadmap | ✅ | ❌ | ❌ | ❌ |
| LaTeX output | ✅ | ❌ | ❌ | ❌ |
| Fully local | ✅ | ❌ | ❌ | ❌ |
| Projects untouched | ✅ | ❌ | ❌ | ❌ |
| Faking warnings | ✅ | ❌ | ❌ | ❌ |

## Contributing

Indom is built by freshers for freshers. Every contribution matters.

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get started.

**Good first issues are labeled** `good first issue` in the Issues tab.

Areas we need help with:
- New LaTeX CV templates
- Better AI prompts
- UI improvements
- More SearXNG search queries
- Documentation and translations

## License

Apache 2.0 — Open source only. You can use, modify, and distribute this freely.  
You cannot take this code and sell it as a paid product.

---

<div align="center">

**// the game is rigged. // we're rewriting it.**

**indom. © 2026**

[Instagram](https://instagram.com/getindom) · [GitHub Issues](https://github.com/yugdabgar21/Indom/issues)

</div>
