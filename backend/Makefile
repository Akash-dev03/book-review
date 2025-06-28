.PHONY: help install dev migrate upgrade test lint format docker-up docker-down clean

include .env
export

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

dev: ## Run dev server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate: ## Create new migration (pass like: make migrate msg="add books")
	alembic revision --autogenerate -m "$(msg)"

upgrade: ## Apply latest DB migration
	alembic upgrade head

test: ## Run all tests
	pytest -v

lint: ## Lint code
	flake8 app/ tests/

format: ## Auto format code
	black app/ tests/
	isort app/ tests/

docker-up: ## Start Docker containers
	docker-compose up --build

docker-down: ## Stop Docker containers
	docker-compose down

clean: ## Clean cache/pyc/__pycache__ files
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
