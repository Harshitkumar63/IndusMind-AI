#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# IndusMind AI — Development Setup Script
# ──────────────────────────────────────────────────────────────

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[32m"
CYAN="\033[36m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║        IndusMind AI — Setup          ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${RESET}"

# ─── Frontend ──────────────────────────────────────────────
echo -e "${GREEN}[1/4]${RESET} Setting up frontend..."
if command -v node &> /dev/null; then
    cd frontend
    npm install
    cd ..
    echo "  ✅ Frontend dependencies installed"
else
    echo "  ⚠️  Node.js not found. Install Node.js 20+ from https://nodejs.org"
fi

# ─── Backend ───────────────────────────────────────────────
echo -e "${GREEN}[2/4]${RESET} Setting up backend..."
if command -v python3 &> /dev/null; then
    cd backend
    python3 -m venv .venv 2>/dev/null || true
    source .venv/bin/activate 2>/dev/null || true
    pip install -r requirements.txt -q
    pip install -e ".[dev]" -q 2>/dev/null || true
    cd ..
    echo "  ✅ Backend dependencies installed"
else
    echo "  ⚠️  Python not found. Install Python 3.11+ from https://python.org"
fi

# ─── Environment ───────────────────────────────────────────
echo -e "${GREEN}[3/4]${RESET} Setting up environment..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "  ✅ Created backend/.env from .env.example"
else
    echo "  ℹ️  backend/.env already exists (skipped)"
fi

# ─── Verification ──────────────────────────────────────────
echo -e "${GREEN}[4/4]${RESET} Verifying setup..."
echo ""
echo -e "${BOLD}  Ready! Start developing:${RESET}"
echo ""
echo "  Frontend:    cd frontend && npm run dev"
echo "  Backend:     cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo "  Full Stack:  cd docker && docker compose up -d"
echo "  Both:        make dev"
echo ""
echo -e "${CYAN}  Frontend → http://localhost:3000${RESET}"
echo -e "${CYAN}  Backend  → http://localhost:8000${RESET}"
echo -e "${CYAN}  API Docs → http://localhost:8000/docs${RESET}"
echo ""
