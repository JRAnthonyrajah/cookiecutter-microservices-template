# Python Development Guide

This guide covers Python-specific setup, development, testing, and best practices for the `{{ cookiecutter.service_name }}` microservice.

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Dependencies Management](#dependencies-management)
3. [Running Tests](#running-tests)
4. [Code Quality](#code-quality)
5. [Type Checking](#type-checking)
6. [Development Workflow](#development-workflow)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Environment Setup

### Using Python venv (Standard Library)

Create and activate a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Verify activation
which python  # Should show path to venv/bin/python
```

### Using pyenv (Recommended for Multiple Python Versions)

Install pyenv if not already installed:

```bash
# macOS with Homebrew
brew install pyenv

# Linux (Ubuntu/Debian)
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
```

Set Python version for the project:

```bash
# Install a specific Python version
pyenv install 3.11.0

# Set local Python version
pyenv local 3.11.0

# Verify
python --version  # Should show 3.11.0
```

### Using pyenv-virtualenv

```bash
# Install pyenv-virtualenv plugin
brew install pyenv-virtualenv

# Create virtual environment with specific Python version
pyenv virtualenv 3.11.0 {{ cookiecutter.service_slug }}

# Activate
pyenv activate {{ cookiecutter.service_slug }}

# Auto-activate when entering directory (add to .python-version)
echo {{ cookiecutter.service_slug }} > .python-version
```

## Dependencies Management

### Project Structure

The project uses `pyproject.toml` for dependency management following PEP 517/518 standards:

```toml
[project]
name = "{{ cookiecutter.service_slug }}"
version = "0.1.0"
description = "{{ cookiecutter.service_description }}"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]
```

### Installing Dependencies

Using **Poetry** (recommended):

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install all dependencies
poetry install

# Install with only production dependencies
poetry install --no-dev

# Add new dependency
poetry add requests
poetry add --group dev pytest
```

Using **pip with requirements files**:

```bash
# Install from pyproject.toml (requires PEP 517 support)
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"

# Generate requirements.txt for deployment
pip freeze > requirements.txt
```

Using **uv** (fastest):

```bash
# Install dependencies
uv pip install -e .

# Install with extras
uv pip install -e ".[dev]"
```

## Running Tests

### Test Framework: pytest

Tests should be placed in the `tests/` directory and follow pytest conventions.

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_service.py

# Run specific test function
pytest tests/test_service.py::test_health_check

# Run with verbose output
pytest -v

# Run with print statements visible
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

### Coverage Analysis

```bash
# Run tests with coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Generate HTML coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser

# Set coverage threshold
pytest --cov=src --cov-fail-under=80

# Coverage for specific module
pytest --cov=src.service --cov-report=term-missing
```

### Test Configuration (pytest.ini or pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--strict-markers --cov=src --cov-report=term-missing"
markers = [
    "unit: unit tests",
    "integration: integration tests",
    "slow: slow running tests",
]
```

### Running Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

## Code Quality

### Ruff: Fast Python Linter

Ruff is a blazing-fast linter written in Rust.

#### Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

#### Running Ruff

```bash
# Check for linting issues
ruff check .

# Check specific file or directory
ruff check src/ tests/

# Fix issues automatically
ruff check --fix .

# View detailed output
ruff check --show-source .
```

### Black: Code Formatter

Black enforces a consistent code style.

#### Configuration (pyproject.toml)

```toml
[tool.black]
line-length = 100
target-version = ["py311"]
include = '\.pyi?$'
```

#### Running Black

```bash
# Format code
black src/ tests/

# Check without making changes
black --check src/

# Show diff
black --diff src/
```

### Integrate in Development Workflow

```bash
# Run linting and formatting checks
ruff check .
black --check .

# Auto-fix issues
ruff check --fix .
black .

# Run all quality checks (recommended setup)
make lint    # From Makefile
```

## Type Checking

### mypy Configuration

mypy performs static type analysis to catch type errors before runtime.

#### Configuration (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

#### Running mypy

```bash
# Type check all files
mypy src/

# Type check specific file
mypy src/service.py

# Type check with strict mode
mypy --strict src/

# Generate coverage report
mypy --html mypy-report src/

# Skip imports without types
mypy --ignore-missing-imports src/
```

#### Type Hints Best Practices

```python
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class ServiceConfig:
    """Configuration for the service."""
    host: str
    port: int
    debug: bool = False

def process_data(items: List[str]) -> Dict[str, Any]:
    """Process a list of items."""
    result: Dict[str, Any] = {}
    for item in items:
        result[item] = len(item)
    return result

async def health_check() -> Optional[Dict[str, bool]]:
    """Check service health."""
    return {"status": True}
```

## Development Workflow

### Using Makefile

The project includes a Makefile for common tasks:

```bash
# Install dependencies
make install

# Run linting
make lint

# Run tests with coverage
make test

# Run type checking
make type-check

# Format code
make format

# Run all checks
make check

# Clean up artifacts
make clean
```

### Git Workflow with Pre-commit

Use pre-commit hooks to ensure code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks from .pre-commit-config.yaml
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

#### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

## Best Practices

### 1. Structure for Microservices

```
{{ cookiecutter.service_slug }}/
├── src/
│   ├── __init__.py
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration management
│   ├── service.py        # Core business logic
│   ├── api/
│   │   ├── __init__.py
│   │   └── handlers.py   # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── domain.py     # Domain models
│   └── infra/
│       ├── __init__.py
│       └── repository.py # Data access layer
├── tests/
│   ├── __init__.py
│   ├── test_service.py
│   └── fixtures/
├── pyproject.toml
└── README.md
```

### 2. Configuration Management

```python
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class ServiceConfig:
    """Application configuration."""
    service_name: str = "{{ cookiecutter.service_slug }}"
    service_version: str = "0.1.0"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    @classmethod
    def from_env(cls) -> "ServiceConfig":
        """Create config from environment variables."""
        return cls()

config = ServiceConfig.from_env()
```

### 3. Error Handling

```python
from typing import Optional

class ServiceError(Exception):
    """Base exception for service errors."""
    pass

class ValidationError(ServiceError):
    """Raised when validation fails."""
    pass

class NotFoundError(ServiceError):
    """Raised when resource not found."""
    pass

async def get_user(user_id: str) -> Dict[str, Any]:
    """Get user by ID."""
    if not user_id:
        raise ValidationError("user_id cannot be empty")
    
    user = await db.fetch_user(user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found")
    
    return user
```

### 4. Logging

```python
import logging
from pythonjsonlogger import jsonlogger

def setup_logging(level: str = "INFO") -> None:
    """Configure JSON logging."""
    logger = logging.getLogger()
    logger.setLevel(level)
    
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger = logging.getLogger(__name__)

async def process_request(request_id: str) -> None:
    """Process incoming request."""
    logger.info("Processing request", extra={"request_id": request_id})
    try:
        result = await do_work()
        logger.info("Request completed", extra={"request_id": request_id, "result": result})
    except Exception as e:
        logger.error("Request failed", extra={"request_id": request_id, "error": str(e)})
        raise
```

### 5. Testing Patterns

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_db():
    """Mock database fixture."""
    return AsyncMock()

@pytest.mark.asyncio
async def test_get_user_success(mock_db):
    """Test successful user retrieval."""
    mock_db.fetch_user.return_value = {"id": "123", "name": "Test"}
    
    result = await get_user("123")
    
    assert result["id"] == "123"
    mock_db.fetch_user.assert_called_once_with("123")

@pytest.mark.asyncio
async def test_get_user_not_found(mock_db):
    """Test user not found."""
    mock_db.fetch_user.return_value = None
    
    with pytest.raises(NotFoundError):
        await get_user("999")
```

### 6. Async/Await Patterns

```python
import asyncio
from typing import List

async def fetch_data(url: str) -> Dict[str, Any]:
    """Fetch data from URL."""
    # Use aiohttp or httpx for async HTTP
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def fetch_multiple(urls: List[str]) -> List[Dict[str, Any]]:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)

async def main() -> None:
    """Main entry point."""
    data = await fetch_multiple(["http://api1.com", "http://api2.com"])
    print(data)

if __name__ == "__main__":
    asyncio.run(main())
```

## Troubleshooting

### Virtual Environment Issues

**Problem**: `python: command not found`

```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
which python  # Should show venv path
```

**Problem**: `ModuleNotFoundError: No module named 'requests'`

```bash
# Solution: Install dependencies
pip install -e .
# OR
poetry install
```

### Test Failures

**Problem**: Tests pass locally but fail in CI/CD

```bash
# Solution: Ensure tests use consistent environment
poetry install --no-cache
pytest --tb=short

# Check for environment-specific issues
pytest -v --tb=long
```

**Problem**: Slow tests

```bash
# Solution: Identify slow tests
pytest --durations=10

# Run only fast tests during development
pytest -m "not slow"
```

### Type Checking Issues

**Problem**: `error: Unsupported operand types for + ("str" and "int")`

```python
# Wrong:
result = "count: " + 5

# Correct:
result = f"count: {5}"
# OR
result = "count: " + str(5)
```

**Problem**: mypy complains about third-party library

```bash
# Solution: Install type stubs
pip install types-requests
# Or use mypy's --ignore-missing-imports for untyped packages
```

### Performance Optimization

**Profile code execution**:

```bash
# Using cProfile
python -m cProfile -s cumulative src/main.py

# Using py-spy for sampling
py-spy record -o profile.svg -- python src/main.py
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [mypy Type Checker](https://mypy.readthedocs.io/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [Poetry Package Manager](https://python-poetry.io/)
- [PEP 8 Style Guide](https://pep8.org/)

## See Also

- [GO.md](./GO.md) - Go-specific development guide
- [NODEJS.md](./NODEJS.md) - Node.js-specific development guide
- [Makefile](./Makefile) - Build automation
- [pyproject.toml](./pyproject.toml) - Project configuration
