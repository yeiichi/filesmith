# Project Makefile for filesmith

PYTHON ?= python
PIP ?= $(PYTHON) -m pip
PYTEST ?= $(PYTHON) -m pytest

PACKAGE_NAME := filesmith

.PHONY: help test test-verbose install-dev clean build run-cli run-find-move run-knapsack

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@printf "  \033[36m%-15s\033[0m %s\n" "help" "Show this help message"
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) \
		| grep -v '^help:' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install-dev: ## Install project in editable mode
	$(PIP) install -e .

test: ## Run the test suite
	$(PYTEST)

test-verbose: ## Run the test suite with verbose output
	$(PYTEST) -v

build: ## Build source and wheel distributions
	$(PYTHON) -m build

clean: ## Remove Python cache files and build artifacts
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf build dist *.egg-info .pytest_cache

run-cli: ## Run the umbrella CLI
	$(PYTHON) -m filesmith.cli

run-find-move: ## Run the find-move CLI
	$(PYTHON) -m filesmith.cli_findmove

run-knapsack: ## Run the knapsack CLI
	$(PYTHON) -m filesmith.cli_knapsack
