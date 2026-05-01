<div align="center">

<img src="apps/frontend/public/logo.png" alt="Indom" width="140" />

<h1>INDOM.</h1>

<h3>Your CV. Their requirements. No mercy.</h3>

<p>
  <a href="https://instagram.com/getindom">📸 Instagram</a> ✦
  <a href="https://github.com/yugdabgar21/Indom/issues">🐛 Report Bug</a> ✦
  <a href="https://github.com/yugdabgar21/Indom/issues">✨ Request Feature</a> ✦
  <a href="CONTRIBUTING.md">🤝 Contribute</a>
</p>

<p>
  <img src="https://img.shields.io/badge/License-Apache_2.0-00ff87.svg" alt="License" />
  <img src="https://img.shields.io/badge/Python-3.10+-00ff87.svg" alt="Python" />
  <img src="https://img.shields.io/badge/Next.js-15-00ff87.svg" alt="Next.js" />
  <img src="https://img.shields.io/badge/PRs-Welcome-00ff87.svg" alt="PRs Welcome" />
  <img src="https://img.shields.io/badge/Cost-Zero-00ff87.svg" alt="Zero Cost" />
  <img src="https://img.shields.io/badge/Cloud-None-00ff87.svg" alt="No Cloud" />
</p>

---

> *The hiring game is rigged. ATS bots filter your CV before a human ever reads it.*
> *Job descriptions ask for 5 years experience in a tool that's 2 years old.*
> *Every tool that fixes this costs money.*
>
> **We're rewriting it. Free. Forever. Local.**

---

</div>

## 🎯 What is Indom?

**Indom** is a 100% free, open source, locally-run CV tailoring tool. It takes your master CV, cross-references it with any job description, and generates a brand new ATS-optimized LaTeX PDF — tailored, smart, and ready to get you in the room.

Unlike other tools, Indom tells you **exactly what it changed** and gives you a **5-day free learning roadmap** so you actually know what you claimed before the interview.

---

## ⚡ How It Works

```
📄 Your Master CV  +  📋 Job Description
              ↓
         🤖 AI Analysis
              ↓
     🎭 Smart Faking Engine
     (calibrated to job level)
              ↓
     📝 LaTeX CV Generated
              ↓
  ⚠️  Faking Warnings + Match Score
              ↓
  📚 5-Day Free Learning Roadmap
              ↓
        🚀 Get In The Room
```

> **Projects are NEVER modified.** Only skills, keywords, and objective are tailored.
> **Every faked item is flagged in red.** No surprises at the interview.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎭 Smart Faking | Adds only what the JD asks, calibrated to experience level |
| 📊 Match Score | Before vs after score so you see the real difference |
| ⚠️ Faking Warnings | Every added skill shown clearly — full transparency |
| 📝 LaTeX PDF | Cleanest, most ATS-compatible output format |
| 📚 Learning Roadmap | 5-day plan with free YouTube and course links via SearXNG |
| 🔒 Fully Local | CV never leaves your machine. Zero cloud. Zero tracking. |
| ⚙️ Settings UI | Configure API key and model from browser — no .env editing |
| 🔄 Multi-Model | OpenRouter, Ollama, OpenAI, Gemini — your choice |
| ⚡ Real-time | SSE streaming with live progress bar |
| 🛡️ ATS-Safe | LaTeX output scores higher than HTML/CSS PDFs |

---

## 🛠️ Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.10+ | Backend runtime |
| Node.js | 18+ | Frontend runtime |
| uv | Latest | [astral.sh/uv](https://astral.sh/uv) — Python package manager |
| MiKTeX or TeX Live | Latest | For `pdflatex` — PDF compilation |
| Docker | Latest | For SearXNG (optional but recommended) |

---

## 🚀 Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/yugdabgar21/Indom.git
cd Indom
cp .env.example .env
```

### 2. Start SearXNG — for real learning resource links (optional)

```bash
docker run -d -p 8080:8080 searxng/searxng
```

### 3. Run the Backend

```bash
cd apps/backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

### 4. Run the Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

### 5. Open and configure

Visit **http://localhost:3000**

Click the ⚙️ settings icon → enter your API key and model. Done.

---

## ⚙️ Configuration

Edit `config.yaml` at the root:

```yaml
model:
  provider: openrouter    # openrouter | ollama | openai | gemini
  name: your-model-name
  api_key: your-api-key   # or configure via UI settings panel

searxng:
  url: http://localhost:8080

template: classic          # classic | modern (coming soon)
```

---

## 📁 Project Structure

```
indom/
├── apps/
│   ├── frontend/           # Next.js 15 + React + TypeScript + Tailwind
│   │   └── src/
│   │       ├── app/        # Pages and routes
│   │       └── components/ # UI components
│   └── backend/            # FastAPI + Python + LiteLLM
│       └── app/
│           ├── routes/     # API endpoints
│           └── services/   # CV parser, AI engine, LaTeX builder, SearXNG
├── docs/                   # Full project documentation
├── searxng/                # SearXNG Docker config
├── config.yaml.example     # Config template
├── docker-compose.yml
└── .env.example
```

---

## 🆚 Why Indom?

| Feature | **Indom** | Resume Matcher | Resume.io | Kickresume |
|---------|-----------|---------------|-----------|------------|
| Free forever | ✅ | ✅ | ❌ | ❌ |
| Smart faking | ✅ | ❌ | ❌ | ❌ |
| Faking warnings | ✅ | ❌ | ❌ | ❌ |
| Learning roadmap | ✅ | ❌ | ❌ | ❌ |
| LaTeX output | ✅ | ❌ | ❌ | ❌ |
| Fully local | ✅ | ❌ | ❌ | ❌ |
| Projects untouched | ✅ | ❌ | ❌ | ❌ |
| No account needed | ✅ | ❌ | ❌ | ❌ |

---

## 🗺️ Roadmap

- [x] CV upload and parsing
- [x] AI tailoring with smart faking
- [x] LaTeX PDF generation and compilation
- [x] Real-time SSE progress streaming
- [x] Faking warning panel
- [x] Match score before and after
- [x] 5-day learning roadmap via SearXNG
- [x] Settings UI for API key and model config
- [ ] Cover letter generation
- [ ] OCR support for image-based CVs
- [ ] More LaTeX templates
- [ ] Setup wizard for non-developers
- [ ] Docker one-command setup

---

## 🤝 Contributing

Indom is built by freshers for freshers. Every contribution matters.

```bash
# Fork the repo, then:
git clone https://github.com/YOUR_USERNAME/Indom.git
cd Indom
git checkout -b feature/your-feature-name
# make your changes
git commit -m "feat: your feature"
git push origin feature/your-feature-name
# open a PR
```

**Good first issues are labeled** `good first issue` in the Issues tab.

We need help with:
- 🎨 New LaTeX CV templates
- 🤖 Better AI prompts
- 💅 UI/UX improvements
- 🔍 SearXNG search query improvements
- 📖 Documentation and translations

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## 📄 License

Apache License 2.0 — Open source only.

You can use, modify, and distribute freely.
You **cannot** take this and sell it as a paid product.

---

<div align="center">

**// the game is rigged. // we're rewriting it.**

**indom. © 2026**

[Instagram @getindom](https://instagram.com/getindom) · [Issues](https://github.com/yugdabgar21/Indom/issues) · [Apache 2.0](LICENSE)

</div>
