<<<<<<< HEAD
<p align="center">
  <img src="apps/frontend/public/logo.png" width="120" alt="Indom Logo" />
</p>

<h1 align="center">INDOM.</h1>
<p align="center"><strong>Your CV. Their requirements. No mercy.</strong></p>

<p align="center">
  AI-powered ATS CV tailor that analyzes job descriptions, injects missing skills, generates LaTeX PDFs, and builds a 5-day learning roadmap — all from one click.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License Apache 2.0" />
</p>

---

## What It Does

Indom is a production-ready CV tailoring system designed to bypass ATS (Applicant Tracking Systems) by dynamically aligning your resume with specific job descriptions. 

1. **Analyze**: AI cross-references your CV with a Job Description to find gaps.
2. **Tailor**: It performs "Smart Faking" to inject required skills while preserving your real projects and education.
3. **Compile**: Generates a professional, ATS-optimized LaTeX PDF in real-time.
4. **Learn**: Builds a 5-day roadmap with verified YouTube resources so you can master the skills you "faked."

## Prerequisites

- **Python 3.10+** (Backend)
- **Node.js 18+** (Frontend)
- **MiKTeX** (For PDF compilation - ensure `pdflatex` is in your PATH)
- **SearXNG** (Optional, for roadmap resource fetching)

## Quick Start

### 1. Clone & Configure
```bash
git clone https://github.com/yugdabgar21/Indom.git
cd Indom
cp .env.example .env
```

### 2. Run Backend
```bash
cd apps/backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

### 3. Run Frontend
```bash
cd apps/frontend
npm install
npm run dev
```

Visit **http://localhost:3000**, click the ⚙️ gear icon, and enter your OpenRouter API key.

## Security & Production

- **No Hardcoded Secrets**: All keys are managed via `.env` or the UI Settings panel.
- **Local First**: Your CV data stays in a local `cv_database.json` file.
- **Multi-Model Fallback**: Built-in resilience against AI provider rate limits.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
=======
# Indom
Your CV. Their requirements. No mercy. AI-powered local CV tailor for freshers. Zero cost. Zero cloud. 100% open source.
>>>>>>> 5e238606ff292564487f20b4657651c3792ca052
