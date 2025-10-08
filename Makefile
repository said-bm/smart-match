.PHONY: help setup install run test clean dev start docs check-env poetry-check lock

help:
	@echo "Smart Match API - Available Commands:"
	@echo ""
	@echo "  make setup       - Full setup with Poetry (install + configure)"
	@echo "  make install     - Install dependencies with Poetry"
	@echo "  make lock        - Regenerate poetry.lock file"
	@echo "  make check-env   - Check if .env file exists and is configured"
	@echo "  make run         - Run the API server"
	@echo "  make dev         - Run the API in development mode (with reload)"
	@echo "  make test        - Run API tests"
	@echo "  make docs        - Open API documentation in browser"
	@echo "  make start       - Quick start (run with script)"
	@echo "  make clean       - Remove cache and generated files"
	@echo "  make clean-all   - Full cleanup (including venv)"
	@echo "  make shell       - Open Poetry shell"
	@echo "  make update      - Update dependencies"
	@echo "  make show        - Show installed packages"
	@echo ""

poetry-check:
	@command -v poetry >/dev/null 2>&1 || { \
		echo "❌ Poetry is not installed!"; \
		echo ""; \
		echo "Install Poetry with:"; \
		echo "  curl -sSL https://install.python-poetry.org | python3 -"; \
		echo ""; \
		echo "Or visit: https://python-poetry.org/docs/#installation"; \
		exit 1; \
	}
	@echo "✓ Poetry is installed"

setup: poetry-check
	@echo "Setting up Smart Match API with Poetry..."
	@echo ""
	@echo "1. Configuring Poetry to create virtual environment in project..."
	poetry config virtualenvs.in-project true
	@echo ""
	@echo "2. Regenerating lock file (if needed)..."
	@poetry lock --no-update 2>/dev/null || poetry lock
	@echo ""
	@echo "3. Installing dependencies..."
	poetry install
	@echo ""
	@echo "4. Setting up environment file..."
	@if [ ! -f .env ]; then \
		cp env.example .env 2>/dev/null || touch .env; \
		echo "✓ Created .env file"; \
		echo "⚠️  Please add your OPENAI_API_KEY to .env"; \
	else \
		echo "✓ .env file already exists"; \
	fi
	@echo ""
	@echo "✓ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Edit .env and add your OPENAI_API_KEY"
	@echo "  2. Run: make run"
	@echo "  3. Visit: http://localhost:8000/docs"

lock: poetry-check
	@echo "Regenerating poetry.lock file..."
	@poetry lock --no-update 2>/dev/null || poetry lock
	@echo "✓ Lock file regenerated!"

install: poetry-check
	@echo "Installing dependencies with Poetry..."
	@poetry lock --no-update 2>/dev/null || poetry lock
	poetry install --no-dev
	@echo "✓ Dependencies installed!"

check-env:
	@echo "Checking environment configuration..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found!"; \
		echo "Run: make setup"; \
		exit 1; \
	fi
	@if ! grep -q "sk-" .env 2>/dev/null; then \
		echo "⚠️  OPENAI_API_KEY not configured in .env"; \
		echo "Please edit .env and add your OpenAI API key"; \
		exit 1; \
	fi
	@echo "✓ Environment configured!"

run: check-env poetry-check
	@echo "Starting Smart Match API..."
	poetry run python api.py

dev: check-env poetry-check
	@echo "Starting Smart Match API in development mode..."
	poetry run uvicorn api:app --reload --host 0.0.0.0 --port 8000

start: check-env
	@echo "Starting API with startup script..."
	./start.sh

test: check-env poetry-check
	@echo "Running API tests..."
	poetry run python test_api.py

docs:
	@echo "Opening API documentation..."
	@echo ""
	@echo "Swagger UI: http://localhost:8000/docs"
	@echo "ReDoc: http://localhost:8000/redoc"
	@echo ""
	@command -v open >/dev/null 2>&1 && open http://localhost:8000/docs || \
	command -v xdg-open >/dev/null 2>&1 && xdg-open http://localhost:8000/docs || \
	echo "Please open http://localhost:8000/docs in your browser"

shell: poetry-check
	@echo "Opening Poetry shell..."
	poetry shell

update: poetry-check
	@echo "Updating dependencies..."
	poetry update
	@echo "✓ Dependencies updated!"

show: poetry-check
	@echo "Installed packages:"
	@echo ""
	poetry show

clean:
	@echo "Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned up cache files!"

clean-all: clean
	@echo "Removing virtual environment and Poetry lock..."
	rm -rf .venv
	rm -rf venv
	rm -f poetry.lock
	@echo "✓ Full cleanup complete!"
	@echo ""
	@echo "To set up again, run: make setup"

# Quick aliases
.PHONY: api server
api: run
server: run
