<div align="center">
<<<<<<< HEAD

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
=======

<img src="apps/frontend/public/logo.png" width="120" alt="Indom Logo" />

# INDOM.

**Your CV. Their requirements. No mercy.**

AI-powered ATS CV tailor that analyzes job descriptions, injects missing skills, generates LaTeX PDFs, and builds a 5-day learning roadmap — all from one click.

[𝙹𝚘𝚒𝚗 𝙳𝚒𝚜𝚌𝚘𝚛𝚍](#) ✦ [𝚆𝚎𝚋𝚜𝚒𝚝𝚎](#) ✦ [𝙷𝚘𝚠 𝚝𝚘 𝙸𝚗𝚜𝚝𝚊𝚕𝚕](#quick-start) ✦ [𝙲𝚘𝚗𝚝𝚛𝚒𝚋𝚞𝚝𝚘𝚛𝚜](#contributors) ✦ [𝙻𝚒𝚗𝚔𝚎𝚍𝙸𝚗](#)

</div>

<br>

<div align="center">

![License Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge&color=1d4ed8&labelColor=F0F0E8)
![Version](https://img.shields.io/badge/Version-1.0.0--MVP-green?style=for-the-badge&color=1d4ed8&labelColor=F0F0E8)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=for-the-badge&color=1d4ed8&labelColor=F0F0E8)

</div>

---

> [!IMPORTANT]
> **Indom** is designed for high-stakes CV tailoring. It uses "Smart Faking" to align your profile with ATS requirements while providing a structured roadmap to learn the injected skills before your interview. Use with intent.

### How It Works
1. **Upload** your master CV (PDF)
2. **Paste** the target job description
3. **Analyze** gaps and auto-inject required skills and keywords
4. **Compile** a professional LaTeX-based PDF resume instantly
5. **Learn** with a 5-day custom roadmap to master any "faked" skills

---

## Key Features

### 🎯 Smart ATS Alignment
Analyzes job descriptions using advanced LLMs to identify missing keywords and skills, then seamlessly integrates them into your professional profile.

### 📄 Real-time LaTeX Compilation
Generates high-quality, ATS-friendly PDF resumes using MiKTeX. No more fighting with Word formatting.

### 🗺️ 5-Day Skill Roadmap
Every tailored CV comes with a 5-day learning plan, complete with verified YouTube resources to help you master new skills quickly.

---

<a id="quick-start"></a>
>>>>>>> 6e25c3fc (fix: backend connection + readme update)

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

Follow these steps **in order**. Don't skip anything.

---

### Step 1 — Install Node.js

Download and install from the official site:

👉 **https://nodejs.org** → Download the LTS version

After installing, verify:
```bash
node --version   # should show v18 or higher
npm --version    # should show a version number
```

---

### Step 2 — Install Scoop (Windows package manager)

Open **PowerShell as Administrator** and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

Verify:
```powershell
scoop --version
```

---

### Step 3 — Install uv via Scoop

```powershell
scoop install uv
```

Verify:
```bash
uv --version
```

> **What is uv?** It's a fast Python package manager. Think of it like npm but for Python.

---

### Step 4 — Install Python via uv

```bash
uv python install 3.13
```

Verify:
```bash
uv python list
```

---

### Step 5 — Install MiKTeX (LaTeX compiler for PDF generation)

Download and install from:

👉 **https://miktex.org/download** → Choose Windows installer

After installing:
1. Open **MiKTeX Console** from Windows Start menu
2. Click **"Check for updates"** and install all updates
3. Go to **Settings → General**
4. Enable **"Always install missing packages on-the-fly"** ✅
5. Restart MiKTeX Console

Verify in terminal:
```bash
pdflatex --version
```

> **Why MiKTeX?** Indom generates CVs as LaTeX code and compiles them to professional PDFs using pdflatex.

---

### Step 6 — Install Docker (for SearXNG — optional but recommended)

Download from:

👉 **https://www.docker.com/products/docker-desktop**

After installing, verify:
```bash
docker --version
```

> **Why Docker?** SearXNG runs in Docker and gives Indom real, verified YouTube and course links for your learning roadmap. Without it, links won't appear in the roadmap.

---

### Step 7 — Get an AI API Key

Indom needs an AI model to analyze your CV. Pick one:

| Provider | Free Tier | Link |
|----------|-----------|------|
| **OpenRouter** (recommended) | Yes — free models available | https://openrouter.ai |
| Ollama | 100% free — runs locally | https://ollama.ai |
| OpenAI | Paid | https://platform.openai.com |
| Google Gemini | Free tier available | https://aistudio.google.com |

> For beginners, **OpenRouter** is easiest — sign up, get a free API key, done.

---

## 🚀 Quick Start

Once all prerequisites are installed:

### 1. Clone the repo

<<<<<<< HEAD
=======
### Prerequisites
| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.13+ | Backend logic & AI engine |
| **Node.js** | 20+ | Frontend UI (Next.js) |
| **uv** | Latest | Fast Python package management |
| **MiKTeX** | Latest | PDF compilation (Ensure `pdflatex` is in PATH) |

### Installation

>>>>>>> 6e25c3fc (fix: backend connection + readme update)
```bash
# 1. Clone the repository
git clone https://github.com/yugdabgar21/Indom.git
cd Indom
<<<<<<< HEAD
```

### 2. Start SearXNG (optional but recommended)

```bash
docker run -d -p 8080:8080 searxng/searxng
```

### 3. Run the Backend

Open Terminal 1:

```bash
cd apps/backend
uv sync
uv run python -m uvicorn app.main:app --reload --port 8000
```

### 4. Run the Frontend

Open Terminal 2:

```bash
cd apps/frontend
=======

# 2. Setup Environment
cp .env.example .env

# 3. Backend Setup
cd apps/backend
uv sync
uv run python -m uvicorn app.main:app --reload --port 8000

# 4. Frontend Setup
cd ../frontend
>>>>>>> 6e25c3fc (fix: backend connection + readme update)
npm install
npm run dev
```

<<<<<<< HEAD
### 5. Open Indom

Visit **http://localhost:3000** in your browser

Click the ⚙️ **Settings** icon → enter your API key and model name → Save

You're ready. Upload your CV and start tailoring. 🔥

---

## ⚙️ Configuration

All config in `config.yaml` at the root:

```yaml
model:
  provider: openrouter    # openrouter | ollama | openai | gemini
  name: your-model-name   # e.g. openai/gpt-4o-mini for OpenRouter
  api_key: your-api-key   # or configure via UI settings panel

searxng:
  url: http://localhost:8080   # SearXNG Docker instance

template: classic              # classic | modern (coming soon)
```

> You can also configure everything from the **Settings UI** inside the app — no manual file editing needed.

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
└── .env.example            # Copy to .env and fill in values
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

**`article.cls not found` error**
→ Open MiKTeX Console → Check for updates → Enable auto-install packages on-the-fly

**`uv run uvicorn` fails on Windows**
→ Use `uv run python -m uvicorn app.main:app --reload --port 8000` instead

**SearXNG links not showing in roadmap**
→ Make sure Docker is running and SearXNG container is started

**OpenRouter 401 error**
→ Check your API key in Settings — make sure it starts with `sk-or-v1-`

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
=======
Open **[http://localhost:3000](http://localhost:3000)** and configure your API key in the Settings panel.

---

## Tech Stack
| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI, LiteLLM, Python 3.13+ |
| **Frontend** | Next.js 16, React 19, TypeScript |
| **AI Engine** | OpenRouter (Ollama, GPT-4, Claude 3.5 support) |
| **Database** | TinyDB (Local JSON storage) |
| **PDF** | MiKTeX (pdflatex) |
| **Styling** | Vanilla CSS, Brutalist Design |

---

## Supported AI Providers
| Provider | Local/Cloud | Status |
|----------|-------------|--------|
| **OpenRouter** | Cloud | ✅ Supported (Recommended) |
| **Ollama** | Local | ✅ Supported |
| **OpenAI** | Cloud | ✅ Supported |
| **Anthropic** | Cloud | ✅ Supported |
| **Google Gemini** | Cloud | ✅ Supported |

---

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

<a id="contributors"></a>

## Contributors
<a href="https://github.com/yugdabgar21/Indom/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yugdabgar21/Indom" />
</a>

---

## License
Distributed under the **Apache License 2.0**. See `LICENSE` for more information.
>>>>>>> 6e25c3fc (fix: backend connection + readme update)
