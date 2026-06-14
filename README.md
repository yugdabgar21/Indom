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
  <img src="https://img.shields.io/badge/Windows-0078D4?logo=windows" alt="Windows" />
  <img src="https://img.shields.io/badge/macOS-000000?logo=apple" alt="macOS" />
  <img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black" alt="Linux" />
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

## 🛠️ Installation — Step by Step

> Follow these steps **in order**. All three platforms covered — Windows, macOS, Linux.

---

### Step 1 — Install Node.js

Node.js is required to run the frontend.

**👉 All platforms:** Download LTS from **https://nodejs.org**

After installing, verify in terminal:
```bash
node --version   # should show v18 or higher
npm --version    # should show a version number
```

---

### Step 2 — Install uv (Python package manager)

uv manages all Python dependencies. No need to install Python separately — uv handles it.

**🪟 Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**🍎 macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**🐧 Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installing, **open a new terminal** then verify:
```bash
uv --version
```

> **Tip for Windows:** If `uv` still not found after install, restart your terminal or use PowerShell instead of CMD.

---

### Step 3 — Install Python via uv

```bash
uv python install 3.13
```

Verify:
```bash
uv python list
```

---

### Step 4 — Install MiKTeX or TeX Live (LaTeX compiler)

Indom compiles LaTeX to PDF using `pdflatex`. You need one of these installed.

**🪟 Windows — MiKTeX (recommended):**

Download from 👉 **https://miktex.org/download** → Windows installer

After installing:
1. Open **MiKTeX Console** from Start menu
2. Click **"Check for updates"** → install all
3. Go to **Settings → General**
4. Enable **"Always install missing packages on-the-fly"** ✅
5. Restart MiKTeX Console

**🍎 macOS — MacTeX:**
```bash
brew install --cask mactex
```
Or download from 👉 **https://www.tug.org/mactex/**

**🐧 Linux — TeX Live:**
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended

# Fedora/RHEL
sudo dnf install texlive-latex texlive-collection-latexextra

# Arch
sudo pacman -S texlive-most
```

Verify on all platforms:
```bash
pdflatex --version
```

---

### Step 5 — Install Docker (for SearXNG — optional but recommended)

SearXNG runs in Docker and provides real verified YouTube and course links for your learning roadmap.

**🪟 Windows & 🍎 macOS:**

Download Docker Desktop from 👉 **https://www.docker.com/products/docker-desktop**

**🐧 Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
# Log out and back in after this
```

Verify:
```bash
docker --version
```

> **Without Docker:** Indom still works fully — the learning roadmap just won't have verified links.

---

### Step 6 — Get an AI API Key

Indom uses an AI model to analyze your CV. Pick any provider:

| Provider | Free Tier | Best For | Link |
|----------|-----------|----------|------|
| **OpenRouter** ⭐ | Yes — free models available | Beginners, easiest setup | https://openrouter.ai |
| **Ollama** | 100% free — fully local | Maximum privacy | https://ollama.ai |
| OpenAI | Paid | GPT-4o quality | https://platform.openai.com |
| Google Gemini | Free tier | Fast responses | https://aistudio.google.com |

> **Recommended for beginners:** Sign up at OpenRouter → generate a free API key → use model `openai/gpt-4o-mini` for best results.

> **For maximum privacy:** Install Ollama locally and run `ollama pull qwen2.5:7b` — no API key needed, fully offline.

---

## 🚀 Quick Start

Once all prerequisites are installed:

### 1. Clone the repo

```bash
git clone https://github.com/yugdabgar21/Indom.git
cd Indom
```

### 2. Start SearXNG (optional)

```bash
docker run -d -p 8080:8080 searxng/searxng
```

### 3. Run the Backend

Open **Terminal 1:**

```bash
cd apps/backend
uv sync
uv run python -m uvicorn app.main:app --reload --port 8000
```

### 4. Run the Frontend

Open **Terminal 2:**

```bash
cd apps/frontend
npm install
npm run dev
```

### 5. Open Indom

Visit **http://localhost:3000** in your browser

Click the ⚙️ **Settings** icon → enter your API key and model name → Save

Upload your CV → Paste a job description → Hit **Commence Faking** 🔥

---

## ⚙️ Configuration

All config in `config.yaml` at root. Copy the example first:

```bash
cp config.yaml.example config.yaml
```

Then edit:

```yaml
model:
  provider: openrouter    # openrouter | ollama | openai | gemini
  name: your-model-name   # e.g. openai/gpt-4o-mini for OpenRouter
  api_key: your-api-key   # or configure via Settings UI in browser

searxng:
  url: http://localhost:8080   # SearXNG Docker instance

template: classic              # classic | modern (coming soon)
```

> **Tip:** You can also configure everything from the ⚙️ **Settings UI** inside the app — no manual file editing needed.

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
├── config.yaml.example     # Config template — copy to config.yaml
├── docker-compose.yml
└── .env.example            # Copy to .env
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
| No account needed | ✅ | ✅ | ❌ | ❌ |

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
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Indom.git
cd Indom
git checkout -b feature/your-feature-name
# make your changes
git commit -m "feat: your feature"
git push origin feature/your-feature-name
# open a Pull Request on GitHub
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

## ❓ Troubleshooting

| Problem | Fix |
|---------|-----|
| `article.cls not found` (Windows) | Open MiKTeX Console → Check for updates → Enable auto-install packages on-the-fly |
| `article.cls not found` (Linux) | Run `sudo apt-get install texlive-latex-extra` |
| `uv run uvicorn` fails on Windows | Use `uv run python -m uvicorn app.main:app --reload --port 8000` |
| SearXNG links not showing | Make sure Docker is running and SearXNG container is started |
| OpenRouter 401 error | Check API key in Settings — must start with `sk-or-v1-` |
| `uv: command not found` | Open a new terminal after installing uv |
| pdflatex not found on Mac | Run `sudo tlmgr update --self` after MacTeX install |

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
