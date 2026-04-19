# {{ cookiecutter.service_name }} - Setup Guide

Welcome to **{{ cookiecutter.service_name }}** setup documentation. This guide covers installation prerequisites, local development environment configuration, and common troubleshooting.

## Installation Prerequisites

Before setting up the development environment, ensure you have the following installed:

### Required Tools

- **Python 3.9+** (for cookiecutter template generation)
  ```bash
  python3 --version  # Should be 3.9 or higher
  ```

- **Docker** (for containerized development and testing)
  ```bash
  docker --version  # Should be Docker 20.10+
  ```

- **Docker Compose** (for local multi-container orchestration)
  ```bash
  docker-compose --version  # Should be Docker Compose 1.29+
  ```

- **Make** (for running development targets)
  ```bash
  make --version
  ```

### Optional Tools (for Kubernetes deployment)

- **Helm 3.x** (for Kubernetes package management)
  ```bash
  helm version  # Should show version 3.x
  ```

- **kubectl** (for Kubernetes CLI operations)
  ```bash
  kubectl version --client
  ```

### Language-Specific Requirements

Depending on the service language, install:

#### Python Services
- **Python 3.9+** (already listed above)
- Virtual environment tools: `venv` (built-in) or `pyenv`
- Package manager: `pip` or `poetry`

#### Go Services
- **Go 1.18+**
  ```bash
  go version
  ```

#### Node.js Services
- **Node.js 16+** and **npm 8+** (or yarn)
  ```bash
  node --version
  npm --version
  ```

#### Java Services
- **Java 11+** (JDK)
  ```bash
  java -version
  ```
- **Maven 3.8+** (or Gradle)
  ```bash
  mvn --version
  ```

## Quick Start: Cookiecutter Template Generation

### Step 1: Generate a New Service from Template

```bash
# Install cookiecutter if not already installed
pip install cookiecutter

# Generate a new service from this template
cookiecutter . \
  --no-input \
  --config-file cookiecutter.json
```

### Step 2: Configure Template Variables

When prompted, provide the following information:

```
service_name: My Microservice
service_slug: my-microservice
service_port: 8080
language: python  # or: go, nodejs, java
docker_registry: myregistry.azurecr.io
environment: development  # or: staging, production
```

### Step 3: Verify Generated Structure

```bash
cd my-microservice/
ls -la

# Expected files and directories:
# - Dockerfile
# - Makefile
# - docker-compose.yml
# - helm/
# - src/
# - tests/
# - .github/workflows/
```

## Local Development Setup

### Step 1: Install Dependencies

#### Python Services
```bash
# Using pip
pip install -r requirements.txt

# Or using poetry (if pyproject.toml exists)
poetry install
```

#### Go Services
```bash
go mod download
go mod verify
```

#### Node.js Services
```bash
npm install
# or
yarn install
```

#### Java Services
```bash
mvn install
```

### Step 2: Configure Environment Variables (Optional)

Create a `.env` file in the service directory:

```bash
# Example .env file
LOG_LEVEL=DEBUG
COMPRESSION=gzip
ENABLE_METRICS=true
ENABLE_TRACING=false
HEALTH_CHECK_INTERVAL=30
```

The `docker-compose.yml` will automatically load these values.

### Step 3: Start Docker Compose Services

```bash
# Start services in detached mode
make up

# Verify services are running
make ps

# View logs
make logs
```

Expected output:
```
CONTAINER ID   IMAGE                       STATUS      NAMES
abc123def456   my-microservice:latest      Up 2 mins   my-microservice-dev
```

### Step 4: Verify Service Health

Check the health endpoint:

```bash
# Using curl
curl -i http://localhost:8080/health

# Expected response
HTTP/1.1 200 OK
Content-Type: application/json

{"status": "healthy", "service": "{{ cookiecutter.service_slug }}"}
```

## Running Tests

### Unit Tests

Run all unit tests for the service:

```bash
# Using make (recommended)
make test

# Alternatively, use language-specific commands:
# Python
pytest tests/ -v

# Go
go test ./... -v

# Node.js
npm test

# Java
mvn test
```

### Test Coverage

Generate test coverage reports:

```bash
# Python with coverage
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

## Building Docker Image

### Build Locally

```bash
# Build using make
make build

# Or manually
docker build -t my-microservice:latest .

# Verify the image
docker images | grep my-microservice
```

### Tag and Push to Registry

```bash
# Tag with registry
docker tag my-microservice:latest myregistry.azurecr.io/my-microservice:latest

# Push to registry (requires authentication)
docker push myregistry.azurecr.io/my-microservice:latest
```

## Code Quality

### Linting

Check code for style issues:

```bash
make lint

# Language-specific:
# Python
ruff check .

# Go
golangci-lint run ./...

# Node.js
eslint .

# Java
mvn checkstyle:check
```

### Code Formatting

Auto-format code to meet style standards:

```bash
make format

# Language-specific:
# Python
black .

# Go
gofmt -s -w .

# Node.js
prettier --write .

# Java
mvn spotless:apply
```

### Check Formatting (without changes)

```bash
make format-check

# Useful in CI/CD pipelines to verify code style
```

## Available Make Targets

| Target | Description |
|--------|-------------|
| `make help` | Display all available targets and their descriptions |
| `make build` | Build Docker image for the service |
| `make test` | Run unit tests (language-aware) |
| `make lint` | Run code linter (language-aware) |
| `make format` | Format code (language-aware) |
| `make format-check` | Check code formatting without applying changes |
| `make up` | Start services with docker-compose in detached mode |
| `make down` | Stop and remove services |
| `make restart` | Restart all services |
| `make clean` | Remove build artifacts, cache, and temporary files |
| `make logs` | Stream logs from all docker-compose services |
| `make logs-service` | Stream logs from main service container |
| `make ps` | Show running containers |
| `make helm-lint` | Validate Helm chart syntax |
| `make helm-template` | Render Helm template for review |
| `make helm-values` | Display Helm chart default values |

## Helm Chart Management

### Validate Helm Chart

```bash
# Lint the chart for syntax errors
make helm-lint

# Expected output:
# ==> Linting helm/
# 1 chart(s) linted, 0 chart(s) failed
```

### Preview Helm Deployment

```bash
# Render the template to see what will be deployed
make helm-template

# This shows the actual Kubernetes manifests that will be created
```

### View Chart Values

```bash
# Display all available configuration values
make helm-values

# Example output:
# replicaCount: 1
# image:
#   repository: localhost/my-microservice
#   tag: latest
# service:
#   type: ClusterIP
#   port: 8080
```

## Troubleshooting

### Issue: "Docker daemon is not running"

**Error**: `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`

**Solution**:
```bash
# Start Docker (macOS with Docker Desktop)
open /Applications/Docker.app

# Or on Linux
sudo systemctl start docker

# Verify Docker is running
docker ps
```

### Issue: "Port already in use"

**Error**: `Error response from daemon: driver failed... port is already allocated`

**Solution**:
```bash
# Find which process is using the port (default 8080)
lsof -i :8080

# Stop the conflicting service
kill -9 <PID>

# Or use a different port
docker-compose down
PORT=9090 docker-compose up
```

### Issue: "Permission denied" running Docker

**Error**: `Got permission denied while trying to connect to the Docker daemon`

**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes without logout
newgrp docker

# Test Docker access
docker ps
```

### Issue: "Make target not found"

**Error**: `make: *** No rule to make target 'test'. Stop.`

**Solution**:
```bash
# View all available targets
make help

# Verify you're in the service directory
pwd

# Verify Makefile exists
ls -la Makefile
```

### Issue: "Tests are failing due to missing dependencies"

**Error**: `ModuleNotFoundError: No module named 'pytest'` (Python example)

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or with poetry
poetry install

# Then run tests again
make test
```

### Issue: "Docker Compose not found"

**Error**: `docker-compose: command not found`

**Solution**:
```bash
# Check if installed
docker compose version  # Note: newer versions use 'docker compose'

# If only 'docker compose' available, check docker-compose alias
which docker-compose

# Install docker-compose if needed
# macOS with Homebrew
brew install docker-compose

# Or use Docker's built-in (v2+)
docker compose up -d
```

### Issue: "Helm chart validation fails"

**Error**: `error converting YAML to JSON: yaml: line X: ...`

**Solution**:
```bash
# Check chart syntax
helm lint helm/

# Validate with strict mode
helm lint helm/ --strict

# Check for template errors
helm template my-service helm/ --debug

# Verify values.yaml syntax
helm show values helm/
```

### Issue: "Health check fails after services start"

**Error**: `Service unhealthy` or `Health check failed`

**Solution**:
```bash
# Check service logs
make logs-service

# Verify service is actually running
make ps

# Check if port is correctly exposed
curl -v http://localhost:8080/health

# Increase health check retries in docker-compose.yml
# Edit the 'healthcheck' section and adjust 'retries' value
```

## Environment-Specific Configuration

### Development Environment

Optimized for rapid iteration and debugging:

```bash
# In .env
LOG_LEVEL=DEBUG
COMPRESSION=gzip
ENABLE_METRICS=true
ENABLE_TRACING=false
```

Start services:
```bash
make up
make logs
```

### Staging Environment

Closer to production with monitoring:

```bash
# In .env
LOG_LEVEL=INFO
COMPRESSION=gzip
ENABLE_METRICS=true
ENABLE_TRACING=true
```

### Production Environment

Optimized for performance and minimal logging:

```bash
# In .env
LOG_LEVEL=WARN
COMPRESSION=gzip
ENABLE_METRICS=true
ENABLE_TRACING=true
HEALTH_CHECK_INTERVAL=60
```

## Next Steps

1. **Local Testing**: Run `make test` to verify the test suite
2. **Code Quality**: Run `make lint` and `make format` before commits
3. **Kubernetes Deployment**: Use `make helm-lint` and `make helm-template` to prepare for cluster deployment
4. **CI/CD Integration**: See `.github/workflows/` for GitHub Actions pipeline examples
5. **Architecture Documentation**: Review `ARCHITECTURE.md` for system design details

## Additional Resources

- **Makefile Reference**: See `Makefile` for complete list of development targets
- **Docker Compose**: See `docker-compose.yml` for service configuration
- **Helm Charts**: See `helm/Chart.yaml` and `helm/values.yaml` for Kubernetes deployment
- **Docker Build**: See `Dockerfile` for container image specification
- **Quick Start Guide**: See `QUICKSTART.md` for a 5-minute tutorial

## Getting Help

- Check the troubleshooting section above for common issues
- View logs with `make logs` to debug runtime problems
- Consult the Makefile for all available commands: `make help`
- Review the Helm chart validation with `make helm-lint`
