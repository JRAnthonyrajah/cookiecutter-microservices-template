# Cookiecutter Microservices Template

A production-ready, language-agnostic microservices template built with cookiecutter. This template provides a comprehensive foundation for developing, containerizing, and deploying microservices to Kubernetes clusters.

## Overview

This template accelerates microservice development with:

- **Multi-language Support**: Python, Go, Node.js/TypeScript
- **Container-Native**: Docker and Docker Compose configurations
- **Kubernetes-Ready**: Helm charts with comprehensive templating
- **Cloud Agnostic**: Deploy to AWS EKS, Google Cloud GKE, Azure AKS, or on-premise clusters
- **Observability**: Built-in monitoring, logging, and tracing integration
- **CI/CD**: GitHub Actions workflows for testing and deployment
- **Production Patterns**: Health checks, graceful shutdown, resource management

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 1.29+
- Python 3.9+
- kubectl 1.19+
- Helm 3.0+

### Generate a New Service

```bash
# Install cookiecutter
pip install cookiecutter

# Generate a new microservice
cookiecutter https://github.com/yourusername/cookiecutter-microservices-template

# Follow the prompts to configure your service
# Answer questions about:
# - Service name and slug
# - Description
# - Primary programming language
# - Author information
```

### Run the Generated Service

```bash
cd my-service

# Build Docker image
docker build -t my-service:latest .

# Run with Docker Compose (includes dependencies)
docker-compose up

# Access the service
curl http://localhost:8080/health
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace my-service

# Deploy with Helm
helm install my-service ./helm \
  --namespace my-service \
  --values ./helm/values.yaml

# Verify deployment
kubectl get pods -n my-service
kubectl port-forward svc/my-service 8080:8080 -n my-service

# Test service
curl http://localhost:8080/health
```

## Documentation Map

The template includes comprehensive documentation:

### Getting Started
- **[SETUP.md](./{{ cookiecutter.service_slug }}/SETUP.md)** - Installation and environment setup
- **[QUICKSTART.md](./{{ cookiecutter.service_slug }}/QUICKSTART.md)** - Quick development start guide

### Development Guides
- **[PYTHON.md](./{{ cookiecutter.service_slug }}/PYTHON.md)** - Python-specific development guide
- **[GO.md](./{{ cookiecutter.service_slug }}/GO.md)** - Go-specific development guide
- **[NODEJS.md](./{{ cookiecutter.service_slug }}/NODEJS.md)** - Node.js/TypeScript development guide

### Architecture & API
- **[ARCHITECTURE.md](./{{ cookiecutter.service_slug }}/ARCHITECTURE.md)** - System architecture and design patterns
- **[API.md](./{{ cookiecutter.service_slug }}/API.md)** - API documentation and examples

### Operations & Deployment
- **[DEPLOYMENT.md](./{{ cookiecutter.service_slug }}/DEPLOYMENT.md)** - Kubernetes deployment guide
- **[TROUBLESHOOTING.md](./{{ cookiecutter.service_slug }}/TROUBLESHOOTING.md)** - Common issues and solutions

## Features

### Multi-Language Support

The template supports three primary programming languages:

#### Python
- Project structure with `src/` layout
- Poetry for dependency management
- Comprehensive type hints and linting
- pytest for testing
- Example: Flask or FastAPI application

#### Go
- Idiomatic Go project structure
- Go modules for dependency management
- Error handling best practices
- Testing with Go's built-in testing framework
- Example: Gin web framework

#### Node.js/TypeScript
- TypeScript for type safety
- Express.js framework
- npm/yarn package management
- Jest for testing
- Example: Modern Node.js server

### Containerization

```
Service Structure:
├── Dockerfile              # Multi-stage build for optimized images
├── docker-compose.yml      # Local development orchestration
├── .dockerignore           # Optimize build context
└── src/                    # Application source code
```

Features:
- Multi-stage Docker builds for small production images
- Docker Compose with services: app, database, cache, message queue
- Health checks in Docker
- Non-root user for security

### Kubernetes Deployment

```
Helm Chart Structure:
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default configuration
├── values-staging.yaml     # Staging overrides
├── values-production.yaml  # Production overrides
└── templates/
    ├── statefulset.yaml    # Application deployment
    ├── service.yaml        # Service exposure
    ├── configmap.yaml      # Configuration management
    ├── pvc.yaml           # Persistent storage
    └── _helpers.tpl        # Template helpers
```

Features:
- StatefulSet for stateful applications
- ConfigMap and Secret management
- Persistent volumes for data durability
- Health checks and probes
- Resource limits and requests
- HorizontalPodAutoscaler configuration

### Observability

#### Monitoring (Prometheus)
- Metrics endpoint at `/metrics`
- Pre-configured Prometheus integration
- Custom application metrics

#### Logging (ELK Stack)
- Structured JSON logging
- Log aggregation with Elasticsearch
- Kibana dashboards
- Log searching and analysis

#### Tracing (Jaeger)
- Distributed trace propagation
- Service-to-service tracking
- Performance analysis
- Request flow visualization

### CI/CD

GitHub Actions workflows included:

- **Test**: Unit and integration tests on every push
- **Build**: Docker image building and registry push
- **Deploy**: Automatic deployment to staging/production
- **Lint**: Code quality and security scanning

Located in `.github/workflows/`:

```bash
ls -la {{ cookiecutter.service_slug }}/.github/workflows/
```

### Development Tools

#### Makefile
Convenient development commands:

```bash
make help              # Show all available targets
make build            # Build Docker image
make run              # Run service locally
make test             # Run tests
make lint             # Run linters
make docker-push      # Push to registry
make k8s-deploy       # Deploy to Kubernetes
make k8s-logs         # View pod logs
```

#### Docker Compose
Complete local development environment:

```bash
docker-compose up              # Start all services
docker-compose down            # Stop all services
docker-compose logs -f app     # View application logs
```

## Template Variables

When using cookiecutter, the following variables are available:

| Variable | Description | Example |
|----------|-------------|---------|
| `service_name` | Full service name | "User Authentication Service" |
| `service_slug` | URL-safe service identifier | "user-auth-service" |
| `service_description` | Service description | "Handles user authentication" |
| `author_name` | Author name | "John Doe" |
| `author_email` | Author email | "john@example.com" |
| `language` | Primary language | "python" |
| `port` | Service port | "8080" |

## Project Structure

After generation, the service directory contains:

```
{{ cookiecutter.service_slug }}/
├── SETUP.md                    # Setup guide
├── QUICKSTART.md               # Quick start guide
├── ARCHITECTURE.md             # Architecture documentation
├── API.md                      # API documentation
├── PYTHON.md                   # Python guide
├── GO.md                       # Go guide
├── NODEJS.md                   # Node.js guide
├── DEPLOYMENT.md               # Deployment guide
├── TROUBLESHOOTING.md          # Troubleshooting guide
│
├── Dockerfile                  # Container image definition
├── docker-compose.yml          # Local orchestration
├── Makefile                    # Development commands
│
├── helm/                       # Kubernetes Helm charts
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-staging.yaml
│   ├── values-production.yaml
│   └── templates/
│       ├── statefulset.yaml
│       ├── service.yaml
│       ├── configmap.yaml
│       ├── pvc.yaml
│       └── _helpers.tpl
│
├── .github/workflows/          # CI/CD workflows
│   ├── test.yml
│   ├── build.yml
│   └── deploy.yml
│
└── src/                        # Application source code
    ├── main.py (or .go/.js)   # Entry point
    ├── app/ (or cmd/)         # Application modules
    └── tests/                 # Test files
```

## Language Support Matrix

| Feature | Python | Go | Node.js |
|---------|--------|----|----|
| Project Setup | ✓ | ✓ | ✓ |
| Dockerfile | ✓ | ✓ | ✓ |
| Docker Compose | ✓ | ✓ | ✓ |
| Helm Charts | ✓ | ✓ | ✓ |
| CI/CD Workflows | ✓ | ✓ | ✓ |
| Unit Tests | ✓ | ✓ | ✓ |
| Linting | ✓ | ✓ | ✓ |
| Health Checks | ✓ | ✓ | ✓ |
| Metrics Export | ✓ | ✓ | ✓ |

## Getting Started with Generated Service

After running `cookiecutter` and answering the prompts, you'll have a ready-to-use microservice:

### 1. Setup Environment

```bash
cd {{ cookiecutter.service_slug }}

# Follow setup guide for your language
cat SETUP.md

# Install dependencies
make install  # or language-specific command
```

### 2. Local Development

```bash
# Build Docker image
docker build -t {{ cookiecutter.service_slug }}:dev .

# Start services with Docker Compose
docker-compose up

# In another terminal, test the service
curl http://localhost:8080/health
```

### 3. Run Tests

```bash
# Run all tests
make test

# Run with coverage
make test-coverage
```

### 4. Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace {{ cookiecutter.service_slug }}

# Deploy with Helm
helm install {{ cookiecutter.service_slug }} ./helm \
  --namespace {{ cookiecutter.service_slug }}

# Check deployment
kubectl get pods -n {{ cookiecutter.service_slug }}
```

### 5. Monitor and Debug

```bash
# View logs
kubectl logs -f deployment/{{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}

# Access metrics
kubectl port-forward svc/{{ cookiecutter.service_slug }} 8080:8080 -n {{ cookiecutter.service_slug }}
curl http://localhost:8080/metrics

# Check Helm deployment status
helm status {{ cookiecutter.service_slug }} -n {{ cookiecutter.service_slug }}
```

## Common Tasks

### Update Service Configuration

```bash
# Edit Helm values
vim helm/values.yaml

# Apply changes
helm upgrade {{ cookiecutter.service_slug }} ./helm -n {{ cookiecutter.service_slug }}
```

### Scale Service

```bash
# Horizontal scaling (more replicas)
helm upgrade {{ cookiecutter.service_slug }} ./helm \
  --set replicaCount=5 \
  -n {{ cookiecutter.service_slug }}

# Or use kubectl directly
kubectl scale statefulset {{ cookiecutter.service_slug }} --replicas=5
```

### Update Application

```bash
# Build and push new image
docker build -t myregistry/{{ cookiecutter.service_slug }}:v2.0 .
docker push myregistry/{{ cookiecutter.service_slug }}:v2.0

# Deploy new version
helm upgrade {{ cookiecutter.service_slug }} ./helm \
  --set image.tag=v2.0 \
  -n {{ cookiecutter.service_slug }}
```

### View Logs

```bash
# Recent logs
kubectl logs -n {{ cookiecutter.service_slug }} \
  -l app={{ cookiecutter.service_slug }} \
  --tail=50

# Stream logs
kubectl logs -n {{ cookiecutter.service_slug }} \
  -l app={{ cookiecutter.service_slug }} \
  -f
```

## Configuration

### Environment Variables

Set via ConfigMap or Helm values:

```yaml
# helm/values.yaml
config:
  serviceName: "{{ cookiecutter.service_slug }}"
  logLevel: "INFO"
  enableMetrics: "true"
  httpPort: "8080"
```

### Secrets

Store sensitive data in Kubernetes Secrets:

```bash
# Create secret
kubectl create secret generic db-creds \
  --from-literal=username=admin \
  --from-literal=password=secret \
  -n {{ cookiecutter.service_slug }}

# Reference in Helm
helm upgrade {{ cookiecutter.service_slug }} ./helm \
  --set secrets.database=db-creds \
  -n {{ cookiecutter.service_slug }}
```

## Troubleshooting

For common issues and solutions, see:

- **Deployment Issues**: [DEPLOYMENT.md Troubleshooting](./{{ cookiecutter.service_slug }}/DEPLOYMENT.md#common-deployment-issues)
- **Runtime Issues**: [TROUBLESHOOTING.md](./{{ cookiecutter.service_slug }}/TROUBLESHOOTING.md)
- **Language-Specific**: 
  - [PYTHON.md](./{{ cookiecutter.service_slug }}/PYTHON.md)
  - [GO.md](./{{ cookiecutter.service_slug }}/GO.md)
  - [NODEJS.md](./{{ cookiecutter.service_slug }}/NODEJS.md)

## Features Overview

### Code Quality
- ✓ Linting (pylint, golangci-lint, eslint)
- ✓ Type checking (mypy, TypeScript)
- ✓ Formatting (black, gofmt, prettier)
- ✓ Security scanning (bandit, gosec, npm audit)

### Testing
- ✓ Unit tests (pytest, go test, jest)
- ✓ Integration tests
- ✓ Code coverage reporting
- ✓ GitHub Actions CI/CD

### Deployment
- ✓ Docker containerization
- ✓ Kubernetes support (StatefulSet, Service, ConfigMap, PVC)
- ✓ Helm charts for templating
- ✓ Health checks and probes
- ✓ Resource management and scaling

### Observability
- ✓ Prometheus metrics
- ✓ Structured logging (JSON)
- ✓ Distributed tracing (Jaeger)
- ✓ Log aggregation (ELK Stack)

### DevOps
- ✓ GitHub Actions workflows
- ✓ Makefile for common tasks
- ✓ Docker Compose for local development
- ✓ Helm for package management

## Contributing

When contributing improvements to this template:

1. Update relevant documentation
2. Test with all supported languages
3. Ensure Helm charts render correctly
4. Update this README if changing features
5. Submit pull request with clear description

## Best Practices

### Development
- Use the provided Makefile for consistency
- Follow language-specific guides in documentation
- Write tests for all features
- Keep images small (multi-stage builds)

### Deployment
- Use environment-specific Helm values files
- Never hardcode secrets in code or configs
- Enable health checks and probes
- Set appropriate resource limits
- Use namespaces for isolation

### Monitoring
- Enable metrics collection in production
- Configure log aggregation
- Setup distributed tracing
- Create alerts for critical metrics
- Document runbooks for common issues

## License

This template is provided as-is. Generated services inherit the license you choose during generation.

## Support

For issues or questions:

1. Check the comprehensive documentation in each generated service
2. Review the troubleshooting guides
3. Examine logs and metrics using provided tools
4. Consult Kubernetes and container documentation

## Resources

### Documentation
- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Docker Documentation](https://docs.docker.com/)

### Language References
- [Python Official Docs](https://docs.python.org/)
- [Go Official Docs](https://golang.org/doc/)
- [Node.js Official Docs](https://nodejs.org/docs/)

### Cloud Providers
- [AWS EKS](https://aws.amazon.com/eks/)
- [Google Cloud GKE](https://cloud.google.com/kubernetes-engine)
- [Azure AKS](https://azure.microsoft.com/en-us/services/kubernetes-service/)

---

Built with love for microservice development. Happy coding!
