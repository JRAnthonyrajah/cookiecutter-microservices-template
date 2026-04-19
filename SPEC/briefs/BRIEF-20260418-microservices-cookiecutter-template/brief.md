# Microservices Cookiecutter Template — Brief

**Date**: 2026-04-18  
**Status**: Ready for PRD synthesis

---

## Initiative Type
Foundation infrastructure / Templating system

## Context

The tensor-kafka repository demonstrates a production-ready Kubernetes service template combining:
- Helm charts for K8s deployment
- Dockerfile for containerization
- Docker Compose for local development
- ArgoCD for GitOps synchronization
- Makefile for common operations
- Cross-repository shared rules and conventions

The cookiecutter-poetry-project provides a Python project generation framework with Commitizen-based versioning, pre-commit hooks, GitHub Actions CI, and Poetry dependency management.

## Problem Statement

**Gap**: No standardized, reusable template exists for generating new microservices that combine:
1. Kubernetes-ready deployment (Helm + ArgoCD)
2. Container infrastructure (Dockerfile + Docker Compose)
3. Service scaffolding with pre-configured observability, CI/CD, and local dev workflows
4. Consistent cross-service conventions and documentation structure
5. Language-agnostic service architecture (applicable to multiple runtimes)

**Current state**: Each new service requires manually replicating the tensor-kafka structure, risking inconsistency in deployment patterns, configuration management, and operational tooling.

## Goals

1. **Reusability**: Generate production-ready microservice scaffolds from a single cookiecutter template
2. **Consistency**: Enforce unified patterns for Helm charts, Docker setup, ArgoCD config, and documentation across all services
3. **Rapid onboarding**: Reduce time-to-deployment for new services from days to minutes
4. **Cross-language support**: Support Python, Go, Node.js, and other containerized workloads
5. **GitOps alignment**: All generated services integrate seamlessly with ArgoCD and shared deployment infrastructure
6. **Observability**: Baked-in health checks, logging, and metric patterns aligned with platform standards

## Non-Goals

- Automatic service mesh integration (Istio/Linkerd)
- Security scanning or SBOM generation (handled by CI/CD pipeline)
- Multi-region deployment automation (handled by infrastructure layer)
- Application-level business logic templates

## Scope

**In scope**:
- Cookiecutter variables and hooks for microservice generation
- Helm chart templates (StatefulSet, Service, ConfigMap, PVC patterns)
- Dockerfile and docker-compose.yml scaffolds
- ArgoCD ApplicationSet template
- Makefile with deploy, validate, logs, test targets
- Pre-configured CI/CD workflow (GitHub Actions)
- Documentation structure (DEPLOYMENT.md, DEVELOPMENT.md, OPERATIONS.md)
- Optional GitHub repo creation post-hook
- Support for 2-3 language runtimes (Python, Go, Node.js)

**Out of scope**:
- Database schema generation
- API specification generation
- Monitoring/alerting rules
- Network policies

## Constraints

1. **Compatibility**: Must work with Kubernetes 1.20+
2. **Helm version**: Target Helm 3.x, avoid deprecated v2 APIs
3. **Cross-repo sharing**: Must integrate with existing `../shared-claude-rules/` structure
4. **Conventional Commits**: Generated projects must enforce commitizen + semantic-release
5. **Git workflow**: Align with existing Git workflow rules (feature/, fix/, chore/ branches)

## Affected Areas

- **Deployment infrastructure**: ArgoCD sync patterns, Helm dependency management
- **Developer experience**: Local dev setup (docker-compose, Taskfile/Makefile alternatives)
- **CI/CD pipeline**: GitHub Actions workflow templates
- **Documentation**: Standardized runbooks and operational playbooks
- **Repository conventions**: shared-claude-rules integration, CLAUDE.md structure

## Risks and Unknowns

**Risks**:
1. **Drift**: Generated services may diverge from template over time if post-generation updates are manual
2. **Language coverage**: Python and Go are clear; Node.js ecosystem is fragmented (npm, yarn, pnpm)
3. **Complexity**: Too many variables in cookiecutter.json may overwhelm new users; too few reduce flexibility

**Unknowns**:
1. Are there service types beyond stateless/stateful (e.g., job/cronjob templates)?
2. Should generated services include optional observability (Prometheus exporter, tracing instrumentation)?
3. What is the target team size for this template—single service owner or platform team ownership?

## Standards Impact

**Inherits**:
- Conventional Commits format (cz commit)
- semantic-release for versioning
- Shared documentation standards (docs/, AI-DOCS/, SPEC/ structure)
- Git workflow rules (branching, PR discipline, releases)
- Kubernetes API v1 (no deprecated v1beta)

**Extends**:
- Helm chart best practices (StatefulSet patterns, healthchecks, affinity rules)
- ArgoCD ApplicationSet usage
- Docker/docker-compose conventions

**May override**:
- Language-specific dependency managers (e.g., uv for Python instead of Poetry if explicitly chosen)

## Proposed Next Artifact

**PRD (Product Requirements Document)** with:
- Detailed feature list (cookiecutter variables, hook behaviors, Helm template options)
- Template file manifest (what files are generated, which are customizable)
- Configuration matrix (language × features)
- Testing strategy (template validation, generated service smoke tests)
- Rollout plan (pilot services, feedback loop, adoption timeline)
