# Plan: Implementation Plan: Microservices Cookiecutter Template

**ID:** PLAN-20260418-001
**PRD:** PRD-20260418-001
**Created:** None

## Description

Decomposed implementation plan for building a production-ready cookiecutter template that generates Kubernetes-deployed microservices with Helm charts, Docker infrastructure, ArgoCD integration, and cross-service conventions.

## Task Definitions

### TASK-001: Design cookiecutter.json manifest

**Description:** Define all variables (service name, language, package name, versions, GitHub options) and their defaults

### TASK-002: Implement pre_gen_project.py validation hook

**Dependencies:** TASK-001
**Description:** Validate inputs before template generation (slug regex, valid Python identifier, version format)

### TASK-003: Create Helm Chart.yaml template

**Description:** Generate Chart.yaml with correct apiVersion, dependencies, and metadata

### TASK-004: Create Helm values.yaml with dev defaults

**Description:** Define dev environment defaults (3 replicas, 10Gi storage, 512m-1g heap, etc.)

### TASK-005: Create Helm StatefulSet template

**Dependencies:** TASK-003, TASK-004
**Description:** Generate StatefulSet for stateful workloads with ordered scaling and probes

### TASK-006: Create Helm Service template

**Dependencies:** TASK-003
**Description:** Generate Service supporting ClusterIP and headless modes

### TASK-007: Create Helm ConfigMap and PVC templates

**Dependencies:** TASK-003
**Description:** Generate ConfigMap for env vars and PVC for persistent storage

### TASK-008: Create Helm helpers template

**Dependencies:** TASK-003
**Description:** Generate _helpers.tpl with consistent labels and naming functions

### TASK-009: Create root values.yaml for production overrides

**Dependencies:** TASK-004
**Description:** Create production environment overrides (50Gi, 1-2GB heap, etc.)

### TASK-010: Create Dockerfile template

**Description:** Generate language-specific Dockerfile with health checks and JVM tuning

### TASK-011: Create docker-compose.yml template

**Dependencies:** TASK-010
**Description:** Generate docker-compose for local dev mirroring Helm configuration

### TASK-012: Create ArgoCD ApplicationSet template

**Dependencies:** TASK-003
**Description:** Generate ApplicationSet for GitOps sync with auto-prune and retry logic

### TASK-013: Create GitHub Actions CI/CD workflow template

**Dependencies:** TASK-001
**Description:** Generate .github/workflows/ci.yml for lint, test, build, and push

### TASK-014: Create Makefile/Taskfile with common commands

**Dependencies:** TASK-003, TASK-011
**Description:** Generate automation file with deploy, validate, logs, test, clean targets

### TASK-015: Create documentation templates

**Dependencies:** TASK-014
**Description:** Generate DEPLOYMENT.md, DEVELOPMENT.md, OPERATIONS.md, README.md, and CLAUDE.md

### TASK-016: Configure cross-repo rules imports in CLAUDE.md

**Dependencies:** TASK-015
**Description:** Set up @shared-claude-rules imports for conventions (git, testing, secrets, docs)

### TASK-017: Implement post_gen_project.py hook

**Dependencies:** TASK-002, TASK-014
**Description:** Implement hook that runs git init, initial commit, GitHub repo creation, tooling setup

### TASK-018: Create language-specific stubs (Python, Go, Node.js)

**Dependencies:** TASK-001
**Description:** Generate {{ cookiecutter.service_slug }}/ subdirectories with language-specific scaffolds

### TASK-019: Implement pre-generation input validation and testing

**Dependencies:** TASK-002
**Description:** Test pre_gen_project hook with valid and invalid inputs

### TASK-020: Test Helm template rendering

**Dependencies:** TASK-005, TASK-006, TASK-007, TASK-008
**Description:** Render Helm templates with test values; validate YAML syntax

### TASK-021: Test Docker image builds for all languages

**Dependencies:** TASK-010
**Description:** Build Docker images for Python, Go, Node.js; verify health checks

### TASK-022: Test docker-compose up and service health

**Dependencies:** TASK-011
**Description:** Run docker-compose up locally; verify services are healthy and reachable

### TASK-023: End-to-end template validation

**Dependencies:** TASK-017, TASK-020, TASK-021, TASK-022
**Description:** Generate a service from template; validate all artifacts are created, git init works, deployment is possible

### TASK-024: Documentation and deployment instructions

**Dependencies:** TASK-015, TASK-023
**Description:** Write comprehensive guide on using the template, customizing generated services, and deploying to Kubernetes

