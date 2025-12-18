.PHONY: help install dev-install test lint format clean run run-api docs

help: ## Show this help message
	@echo "Personal AI - Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies
	pip3 install -r requirements.txt

dev-install: ## Install development dependencies
	pip3 install -r requirements.txt
	pip3 install pytest pytest-cov black flake8 mypy isort pre-commit
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src --cov-report=html --cov-report=term-missing

lint: ## Run linting checks
	black --check src tests
	flake8 src tests
	mypy src

format: ## Format code
	black src tests
	isort src tests

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

run: ## Run the AI in interactive mode
	python3 src/main.py --mode interactive

run-api: ## Run the API server
	python3 src/main.py --mode api

run-verbose: ## Run with verbose logging
	python3 src/main.py --mode interactive --verbose

docs: ## Generate documentation (placeholder)
	@echo "Documentation generation not yet implemented"

setup-dev: dev-install ## Complete development setup
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the personal AI"

check: lint test ## Run all checks (lint and test)