# Microservices Cookiecutter Template

**ID:** PRD-20260418-001
**Created:** None

## Description

A production-ready cookiecutter template for generating Kubernetes-deployed microservices with standardized Helm charts, Docker infrastructure, ArgoCD integration, and cross-service conventions.

## Requirements

### REQ-001: Cookiecutter Template Structure

Define cookiecutter.json with all variables needed to generate a microservice

### REQ-002: Helm Chart Templates

Generate production-ready Helm charts for Kubernetes deployment

### REQ-003: Dockerfile and Image Strategy

Minimal, language-agnostic Dockerfile using official base images

### REQ-004: Docker Compose for Local Development

docker-compose.yml for local development without Kubernetes

### REQ-005: ArgoCD Integration

ApplicationSet template for GitOps-based deployment

### REQ-006: Makefile / Taskfile Automation

Common development and deployment commands

### REQ-007: GitHub Actions CI/CD Workflow

Pre-configured CI/CD for generated services

### REQ-008: Documentation Structure

Standardized documentation for all generated services

### REQ-009: Cross-Repository Rules Integration

Import shared conventions from ../shared-claude-rules/

### REQ-010: Multi-Language Support

Support Python, Go, and Node.js services with language-specific defaults

### REQ-011: Health Checks and Observability Patterns

Baked-in patterns for health checks, logging, and metrics

### REQ-012: Template Validation and Testing

Automated validation of generated services

