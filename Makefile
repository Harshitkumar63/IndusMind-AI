.PHONY: help dev frontend backend docker-up docker-down lint test clean setup

# ─── Default ────────────────────────────────────────────────
help: ## Show this help message
	@echo ""
	@echo "  IndusMind AI — Development Commands"
	@echo "  ────────────────────────────────────"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ─── Development ────────────────────────────────────────────
dev: ## Start both frontend and backend in development mode
	@echo "Starting IndusMind AI..."
	@make -j2 frontend backend

frontend: ## Start frontend development server
	cd frontend && npm run dev

backend: ## Start backend development server
	cd backend && uvicorn app.main:app --reload --port 8000

# ─── Docker ─────────────────────────────────────────────────
docker-up: ## Start all services with Docker Compose
	cd docker && docker compose up -d

docker-down: ## Stop all Docker services
	cd docker && docker compose down

docker-logs: ## View Docker logs (follow)
	cd docker && docker compose logs -f

docker-build: ## Rebuild Docker images
	cd docker && docker compose build --no-cache

docker-reset: ## Stop services and remove volumes
	cd docker && docker compose down -v

# ─── Quality ────────────────────────────────────────────────
lint: ## Run linters (frontend + backend)
	cd frontend && npm run lint
	cd backend && ruff check .

format: ## Format code (frontend + backend)
	cd frontend && npx prettier --write "src/**/*.{ts,tsx}"
	cd backend && ruff format .

test: ## Run all tests
	cd backend && python -m pytest tests/ -v

test-coverage: ## Run tests with coverage report
	cd backend && python -m pytest tests/ --cov=app --cov-report=html

typecheck: ## Run type checks
	cd frontend && npx tsc --noEmit
	cd backend && mypy app/

# ─── Setup ──────────────────────────────────────────────────
setup: ## Initial project setup
	cd frontend && npm install
	cd backend && pip install -r requirements.txt && pip install -e ".[dev]"
	@echo "Setup complete! Run 'make dev' to start."

clean: ## Clean build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf frontend/.next
	rm -rf backend/htmlcov
	@echo "Cleaned!"
