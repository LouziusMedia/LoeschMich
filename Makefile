.PHONY: help install test lint clean run init

help:
	@echo "GDPR Deletion Tool - Makefile Commands"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make init       - Initialize the application"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make run        - Run the application"
	@echo ""

install:
	pip install --upgrade pip
	pip install -r requirements.txt

init:
	python main.py init

test:
	pytest --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src tests
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	python main.py

.DEFAULT_GOAL := help
