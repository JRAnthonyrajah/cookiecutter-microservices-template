# {{ cookiecutter.service_name }} - 5-Minute Quick Start

Get **{{ cookiecutter.service_name }}** running locally in 5 minutes with this quick start guide.

## Prerequisites

Before starting, ensure you have:
- Docker installed and running
- Docker Compose installed
- Make installed
- Basic curl or HTTP client knowledge

## Step 1: Clone and Navigate (1 minute)

```bash
# Navigate to the service directory
cd {{ cookiecutter.service_slug }}/

# Verify key files exist
ls -la Makefile docker-compose.yml Dockerfile
```

Expected output:
```
-rw-r--r--  1 user  staff  6118 Apr 19 Makefile
-rw-r--r--  1 user  staff  1550 Apr 19 docker-compose.yml
-rw-r--r--  1 user  staff  2239 Apr 19 Dockerfile
```

## Step 2: Setup Environment (1 minute)

```bash
# Install dependencies (language-specific)
# For Python:
pip install -r requirements.txt

# For Go:
go mod download

# For Node.js:
npm install

# For Java:
mvn install
```

## Step 3: Start Services (1 minute)

```bash
# Start all services in background
make up

# Watch the startup (Ctrl+C to stop watching logs)
make logs
```

You should see output like:
```
{{ cookiecutter.service_slug }}-dev | Starting service...
{{ cookiecutter.service_slug }}-dev | [INFO] Service initialized
{{ cookiecutter.service_slug }}-dev | [INFO] Server listening on :8080
```

Wait for the "Server listening" message or similar health indication.

## Step 4: Verify Service is Running (1 minute)

```bash
# Check running containers
make ps
```

Expected output:
```
CONTAINER ID   IMAGE                      STATUS      NAMES
a1b2c3d4e5f6   {{ cookiecutter.service_slug }}:latest   Up 30s   {{ cookiecutter.service_slug }}-dev
```

### Health Check

```bash
# Check service health endpoint
curl -i http://localhost:{{ cookiecutter.service_port | default('8080') }}/health
```

Expected response:
```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 45

{"status":"healthy","service":"{{ cookiecutter.service_slug }}"}
```

## Step 5: Make Your First Request (1 minute)

### Example: Greeting Endpoint

```bash
# Make a request to the service
curl -X GET http://localhost:{{ cookiecutter.service_port | default('8080') }}/api/greeting \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "message": "Hello from {{ cookiecutter.service_name }}",
  "timestamp": "2025-04-19T10:30:45Z",
  "service": "{{ cookiecutter.service_slug }}"
}
```

### Example: JSON POST Request

```bash
# Send JSON data to the service
curl -X POST http://localhost:{{ cookiecutter.service_port | default('8080') }}/api/echo \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello from local dev"}'
```

Expected response:
```json
{
  "received": "Hello from local dev",
  "timestamp": "2025-04-19T10:31:12Z",
  "echo": true
}
```

## Running Tests

```bash
# Run the test suite
make test

# You should see output like:
# Running tests for python...
# tests/test_service.py::test_health_check PASSED
# tests/test_service.py::test_greeting PASSED
# ✓ Tests completed
```

## Building Docker Image

```bash
# Build the Docker image
make build

# Verify the image was created
docker images | grep {{ cookiecutter.service_slug }}
```

Expected output:
```
{{ cookiecutter.service_slug }}   latest   abc123def456   30 seconds ago   150MB
```

## Stopping Services

When you're done with development:

```bash
# Stop and remove all services
make down

# Verify services are stopped
make ps
```

Expected output:
```
CONTAINER ID   IMAGE   STATUS   NAMES
(no containers running)
```

## Next Steps

### 1. Read the Full Setup Guide
For detailed configuration, troubleshooting, and advanced options:
```bash
cat SETUP.md
```

### 2. Explore Available Commands
View all development targets:
```bash
make help
```

### 3. Check Code Quality
Run linter and formatter:
```bash
make lint
make format
```

### 4. View Application Logs
```bash
make logs-service
```

### 5. Explore the Codebase
```bash
# Navigate to source code
cd src/

# Language-specific structure:
# Python:   src/main.py, src/app.py
# Go:       main.go
# Node.js:  src/index.js
# Java:     src/main/java/
```

## Common Commands at a Glance

| Task | Command |
|------|---------|
| Start services | `make up` |
| Stop services | `make down` |
| View logs | `make logs` |
| Run tests | `make test` |
| Check code style | `make lint` |
| Fix code style | `make format` |
| Build Docker image | `make build` |
| View all commands | `make help` |

## Troubleshooting

### Service won't start
```bash
# Check logs for errors
make logs

# Check if port is already in use
lsof -i :{{ cookiecutter.service_port | default('8080') }}
```

### Health check fails
```bash
# Wait longer for service to initialize
sleep 5

# Then try health check again
curl -i http://localhost:{{ cookiecutter.service_port | default('8080') }}/health
```

### Docker Compose not found
```bash
# Try using docker compose (v2+)
docker compose up -d

# Or install docker-compose
brew install docker-compose  # macOS
apt-get install docker-compose  # Linux
```

### Permission denied
```bash
# Add yourself to docker group
sudo usermod -aG docker $USER
newgrp docker
```

## That's It!

You now have:
- ✓ Service running locally
- ✓ Made your first API request
- ✓ Run the test suite
- ✓ Built a Docker image
- ✓ Stopped the services

For more information, see:
- `SETUP.md` - Complete setup and configuration guide
- `ARCHITECTURE.md` - System design and architecture
- `Makefile` - All available development commands
- `docker-compose.yml` - Service configuration
- `Dockerfile` - Container image specification
