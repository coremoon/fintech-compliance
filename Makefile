.PHONY: help install setup test clean weaviate-up weaviate-down weaviate-init weaviate-logs

# Platform detection
UNAME_S := $(shell uname -s)
ifeq ($(OS),Windows_NT)
    PLATFORM := Windows
    ACTIVATE := .venv\Scripts\activate
else ifeq ($(UNAME_S),Darwin)
    PLATFORM := macOS
    ACTIVATE := source .venv/bin/activate
else
    PLATFORM := Linux
    ACTIVATE := source .venv/bin/activate
endif

help:
	@echo "fintech-compliance"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Setup venv"
	@echo "  make install        - Install deps (Poetry)"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean cache"
	@echo ""
	@echo "Weaviate (IN THIS ORDER):"
	@echo "  make weaviate-up    - Start Weaviate"
	@echo "  make weaviate-init  - Initialize schemas"
	@echo "  make weaviate-down  - Stop Weaviate"
	@echo "  make weaviate-logs  - View logs"
	@echo ""

setup:
	python3 -m venv .venv
ifeq ($(PLATFORM),Windows)
	@echo "Run: .venv\Scripts\activate"
else
	@echo "Run: source .venv/bin/activate"
endif

install:
	@command -v poetry >/dev/null 2>&1 || (echo "Poetry not found. Install: pip install poetry" && exit 1)
	poetry install

test:
	poetry run pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

weaviate-up:
	@echo "Starting Weaviate..."
	cd docker && docker-compose up -d
	@sleep 3
	@curl -s http://localhost:8080/v1/meta > /dev/null && echo "✅ Weaviate ready at http://localhost:8080" || echo "⚠️ Weaviate starting..."

weaviate-down:
	@echo "Stopping Weaviate..."
	cd docker && docker-compose down
	@echo "✅ Weaviate stopped"

weaviate-init:
	@echo "Initializing Weaviate schemas..."
	python -m src.data.weaviate

weaviate-logs:
	cd docker && docker-compose logs -f weaviate

.DEFAULT_GOAL := help
