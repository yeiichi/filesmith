.PHONY: help install build wheel test clean distclean

PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@printf "  \033[36m%-15s\033[0m %s\n" "help" "Show this help message"
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| grep -v '^help:' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in editable mode
	$(PIP) install -e .

build: ## Build the project
	$(PIP) install -U build
	$(PYTHON) -m build

wheel: ## Build only a wheel
	$(PIP) install -U build
	$(PYTHON) -m build --wheel

test: ## Run the test suite
	$(PYTEST)

clean: ## Remove common build/test artifacts
	rm -rf build dist .pytest_cache .mypy_cache .ruff_cache htmlcov
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +

distclean: clean ## Remove all generated artifacts
	rm -rf *.egg-info src/*.egg-info