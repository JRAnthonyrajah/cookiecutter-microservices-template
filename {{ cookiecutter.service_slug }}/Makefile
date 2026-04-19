.PHONY: help build test lint format up down clean helm-lint helm-template logs

# Default target
.DEFAULT_GOAL := help

# Service configuration
SERVICE_NAME := {{ cookiecutter.service_slug }}
DOCKER_REGISTRY := {{ cookiecutter.docker_registry | default('localhost') }}
DOCKER_IMAGE := $(DOCKER_REGISTRY)/$(SERVICE_NAME)
DOCKER_TAG := latest
HELM_CHART_DIR := helm

# Language-specific variables
LANGUAGE := {{ cookiecutter.language }}

# Python-specific variables
ifeq ($(LANGUAGE),python)
	PYTHON_CMD := python3
	LINT_CMD := ruff check .
	FORMAT_CMD := black .
	FORMAT_CHECK_CMD := black --check .
	TEST_CMD := pytest tests/
endif

# Go-specific variables
ifeq ($(LANGUAGE),go)
	LINT_CMD := golangci-lint run ./...
	FORMAT_CMD := gofmt -s -w .
	FORMAT_CHECK_CMD := gofmt -s -l .
	TEST_CMD := go test ./...
endif

# Node.js-specific variables
ifeq ($(LANGUAGE),nodejs)
	LINT_CMD := eslint .
	FORMAT_CMD := prettier --write .
	FORMAT_CHECK_CMD := prettier --check .
	TEST_CMD := npm test
endif

# Java-specific variables
ifeq ($(LANGUAGE),java)
	LINT_CMD := mvn checkstyle:check
	FORMAT_CMD := mvn spotless:apply
	FORMAT_CHECK_CMD := mvn spotless:check
	TEST_CMD := mvn test
endif

##@ Build Targets

build: ## Build Docker image for the service
	@echo "Building Docker image: $(DOCKER_IMAGE):$(DOCKER_TAG)"
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) \
		--build-arg SERVICE_NAME=$(SERVICE_NAME) \
		-f Dockerfile .
	@echo "✓ Docker image built successfully"

##@ Testing Targets

test: ## Run unit tests (language-aware)
	@echo "Running tests for $(LANGUAGE)..."
ifeq ($(LANGUAGE),python)
	@$(TEST_CMD) -v --tb=short
else ifeq ($(LANGUAGE),go)
	@$(TEST_CMD) -v -cover ./...
else ifeq ($(LANGUAGE),nodejs)
	@npm test -- --verbose
else ifeq ($(LANGUAGE),java)
	@mvn test -X
else
	@echo "No test command configured for language: $(LANGUAGE)"
endif
	@echo "✓ Tests completed"

##@ Linting and Formatting Targets

lint: ## Run code linter (language-aware)
	@echo "Linting code for $(LANGUAGE)..."
ifeq ($(LANGUAGE),python)
	@$(LINT_CMD) --select=E,W,F
else ifeq ($(LANGUAGE),go)
	@$(LINT_CMD)
else ifeq ($(LANGUAGE),nodejs)
	@$(LINT_CMD)
else ifeq ($(LANGUAGE),java)
	@$(LINT_CMD)
else
	@echo "No linter configured for language: $(LANGUAGE)"
endif
	@echo "✓ Linting completed"

format: ## Format code (language-aware)
	@echo "Formatting code for $(LANGUAGE)..."
ifeq ($(LANGUAGE),python)
	@$(FORMAT_CMD)
else ifeq ($(LANGUAGE),go)
	@$(FORMAT_CMD)
else ifeq ($(LANGUAGE),nodejs)
	@$(FORMAT_CMD)
else ifeq ($(LANGUAGE),java)
	@$(FORMAT_CMD)
else
	@echo "No formatter configured for language: $(LANGUAGE)"
endif
	@echo "✓ Code formatted successfully"

format-check: ## Check code formatting without applying changes
	@echo "Checking code format for $(LANGUAGE)..."
ifeq ($(LANGUAGE),python)
	@$(FORMAT_CHECK_CMD)
else ifeq ($(LANGUAGE),go)
	@$(FORMAT_CHECK_CMD) > /dev/null || (echo "Code formatting issues detected"; exit 1)
else ifeq ($(LANGUAGE),nodejs)
	@$(FORMAT_CHECK_CMD)
else ifeq ($(LANGUAGE),java)
	@$(FORMAT_CHECK_CMD)
else
	@echo "No format checker configured for language: $(LANGUAGE)"
endif
	@echo "✓ Code format check completed"

##@ Docker Compose Targets

up: ## Start services with docker-compose (-d for detached mode)
	@echo "Starting services..."
	docker-compose up -d
	@echo "✓ Services started. Run 'make logs' to view output"

down: ## Stop and remove services
	@echo "Stopping services..."
	docker-compose down
	@echo "✓ Services stopped"

restart: down up ## Restart all services

##@ Cleanup Targets

clean: ## Remove build artifacts, cache, and temporary files
	@echo "Cleaning up artifacts..."
ifeq ($(LANGUAGE),python)
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
else ifeq ($(LANGUAGE),go)
	@go clean -cache -testcache
	@find . -type f -name "*.test" -delete
else ifeq ($(LANGUAGE),nodejs)
	@rm -rf node_modules/
	@rm -f package-lock.json
else ifeq ($(LANGUAGE),java)
	@mvn clean
endif
	@find . -type f -name ".DS_Store" -delete
	@echo "✓ Cleanup completed"

##@ Helm Targets

helm-lint: ## Validate Helm chart
	@echo "Linting Helm chart..."
	@if [ ! -d "$(HELM_CHART_DIR)" ]; then \
		echo "Helm chart directory not found at $(HELM_CHART_DIR)"; \
		exit 1; \
	fi
	helm lint $(HELM_CHART_DIR)
	@echo "✓ Helm chart validation passed"

helm-template: ## Render Helm template
	@echo "Rendering Helm template..."
	@if [ ! -d "$(HELM_CHART_DIR)" ]; then \
		echo "Helm chart directory not found at $(HELM_CHART_DIR)"; \
		exit 1; \
	fi
	helm template $(SERVICE_NAME) $(HELM_CHART_DIR)
	@echo "✓ Helm template rendering completed"

helm-values: ## Show Helm values
	@echo "Displaying Helm values..."
	@if [ ! -d "$(HELM_CHART_DIR)" ]; then \
		echo "Helm chart directory not found at $(HELM_CHART_DIR)"; \
		exit 1; \
	fi
	helm show values $(HELM_CHART_DIR)

##@ Logs and Debugging

logs: ## Stream logs from docker-compose services
	@docker-compose logs -f

logs-service: ## Stream logs from main service container
	@docker-compose logs -f $(SERVICE_NAME)

ps: ## Show running containers
	@docker-compose ps

##@ Help

help: ## Display all available targets
	@echo "$(SERVICE_NAME) - Development Makefile"
	@echo ""
	@echo "Language: $(LANGUAGE)"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\033[36m%-18s\033[0m %s\n", "TARGET", "DESCRIPTION"} /^[a-zA-Z_-]+:.*?##/ {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "Examples:"
	@echo "  make build         # Build Docker image"
	@echo "  make test          # Run tests"
	@echo "  make lint          # Run linter"
	@echo "  make format        # Format code"
	@echo "  make up            # Start services"
	@echo "  make down          # Stop services"
	@echo "  make clean         # Remove artifacts"
	@echo "  make helm-lint     # Validate Helm chart"
	@echo ""
