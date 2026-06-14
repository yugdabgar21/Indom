# Contributing to Indom

First off, thank you for considering contributing to Indom! It's people like you that make Indom a better tool for everyone.

## Code of Conduct

By participating in this project, you agree to abide by the terms of the [Apache 2.0 License](LICENSE).

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check that you are using the latest version of the code and check the existing issues to see if the problem has already been reported.

### Submitting Pull Requests

1.  **Fork the repository** and create your branch from `main`.
2.  **Install dependencies** using `uv` for the backend and `npm` for the frontend.
3.  **Make your changes**. If you've added code that should be tested, add tests.
4.  **Ensure the code follows the existing style**.
5.  **Submit a pull request** with a clear description of the changes.

## Local Setup

### Backend

1.  Navigate to `apps/backend`.
2.  Install `uv` if you haven't already.
3.  Run `uv sync` to install dependencies.
4.  Copy `.env.example` to `.env` and fill in your API keys.
5.  Run `uv run uvicorn app.main:app --reload`.

### Frontend

1.  Navigate to `apps/frontend`.
2.  Run `npm install`.
3.  Copy `.env.example` (if present) or set `NEXT_PUBLIC_API_URL` to `http://localhost:8000`.
4.  Run `npm run dev`.

## Style Guidelines

*   **Python**: Follow PEP 8. Use clear, descriptive variable names.
*   **TypeScript/React**: Use functional components and hooks. Follow standard React best practices.

## Issue Templates

We don't have formal templates yet, but please include:
*   A clear and descriptive title.
*   Steps to reproduce the issue.
*   Expected vs. Actual behavior.
*   Your environment (OS, Python version, Node version).
