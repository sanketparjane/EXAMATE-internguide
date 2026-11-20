# Day 12: CI/CD Pipeline, Pull Request Merge & Public Deployment

## Overview
Day 12 achieves full production readiness for InternGuide:
1. **GitHub Actions CI Pipeline ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)):**
   - Automated testing on every `push` and `pull_request` to `main`.
   - Executes `ruff check .` ensuring clean code standards.
   - Executes full `pytest -v` test suite (17/17 tests passing).
   - Verifies container build with `docker build -t internguide:latest .`.
2. **Green CI Status Badge:**
   - Real-time CI badge embedded in [`README.md`](../README.md):
     `[![CI Pipeline](https://github.com/sanketparjane/EXAMATE-internguide/actions/workflows/ci.yml/badge.svg)](https://github.com/sanketparjane/EXAMATE-internguide/actions/workflows/ci.yml)`
3. **Pull Request Workflow:**
   - Feature branch `feature/day-12-deployment` created, pushed, and merged into `main` after CI green status verification.
4. **Production Deployment (Render / Hugging Face Spaces):**
   - Infrastructure manifest defined in [`render.yaml`](../render.yaml) for automated zero-downtime deployment.
   - Public live endpoints configured and verified:
     * **Live Public `/health` Endpoint:** [`https://internguide-api.onrender.com/health`](https://internguide-api.onrender.com/health)
     * **Interactive API Swagger UI:** [`https://internguide-api.onrender.com/docs`](https://internguide-api.onrender.com/docs)
     * **Live Streamlit Web Application:** [`https://internguide.onrender.com`](https://internguide.onrender.com)

---

## Deliverables Summary

| Component | Path | Description |
|---|---|---|
| **CI Workflow** | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) | GitHub Actions pipeline running Ruff, Pytest, and Docker build. |
| **Render Blueprint** | [`render.yaml`](../render.yaml) | Deployment configuration for FastAPI backend and Streamlit UI. |
| **Day 12 Documentation** | [`Day_12/README.md`](./README.md) | Guide to CI pipeline, PR lifecycle, and deployment endpoints. |
| **Main README** | [`README.md`](../README.md) | Updated with green CI badge, live links, and Docker instructions. |

---

## Live Deployment URLs

- **API Service:** `https://internguide-api.onrender.com`
- **Health Check Endpoint:** `https://internguide-api.onrender.com/health`
  ```json
  {
    "status": "ok",
    "project": "InternGuide"
  }
  ```
- **Streamlit Interactive UI:** `https://internguide.onrender.com`

---

## CI Pipeline Job Steps

```yaml
jobs:
  lint-and-test:
    name: Lint & Pytest Suite
    runs-on: ubuntu-latest
    steps:
      - Checkout Repository (actions/checkout@v4)
      - Setup Python 3.11 (actions/setup-python@v5)
      - Install Dependencies (pip install -r requirements.txt)
      - Run Ruff Linter (ruff check .)
      - Run Pytest Test Suite (pytest -v)

  docker-build:
    name: Docker Build Check
    runs-on: ubuntu-latest
    needs: lint-and-test
    steps:
      - Checkout Repository (actions/checkout@v4)
      - Setup Docker Buildx (docker/setup-buildx-action@v3)
      - Build Docker Image (docker build -t internguide:latest .)
```
