# Go Development Guide

This guide covers Go-specific setup, development, testing, and best practices for the `{{ cookiecutter.service_name }}` microservice.

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Module Management](#module-management)
3. [Building and Running](#building-and-running)
4. [Testing](#testing)
5. [Code Quality](#code-quality)
6. [Development Workflow](#development-workflow)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Environment Setup

### Installing Go

#### macOS

```bash
# Using Homebrew
brew install go

# Verify installation
go version

# Set GOPATH (usually ~/.go or ~/go)
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

#### Linux (Ubuntu/Debian)

```bash
# Download and extract
wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz

# Add to PATH
export PATH=$PATH:/usr/local/go/bin
echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
source ~/.bashrc

# Verify
go version
```

#### Windows

```powershell
# Using Chocolatey
choco install golang

# Or download from https://go.dev/dl/ and run installer
# Verify
go version
```

### Workspace Setup

Go 1.18+ supports workspace mode for managing multiple modules:

```bash
# Create workspace file
go work init

# List Go version and environment
go version
go env

# Verify GOPATH is set
echo $GOPATH
```

## Module Management

### go.mod and go.sum

The project uses standard Go module management. Every Go project must have a `go.mod` file.

### Initialize Module

```bash
# Create new module
go mod init github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.service_slug }}

# Or use provided go.mod
cat go.mod
```

### Managing Dependencies

```bash
# Download/update dependencies
go mod download

# Update all dependencies to latest patch versions
go get -u ./...

# Update all dependencies including minor versions
go get -u=patch ./...

# Add specific dependency
go get github.com/gin-gonic/gin@v1.9.0

# Remove unused dependencies
go mod tidy

# Verify dependencies
go mod verify

# Display module graph
go mod graph

# Display module download URL
go mod download -json github.com/gin-gonic/gin
```

### Vendoring (Optional)

Store dependencies in version control:

```bash
# Create vendor directory
go mod vendor

# Use vendored dependencies
go build -mod=vendor

# Clean up vendor directory
go mod tidy -v
```

## Building and Running

### Simple Execution

```bash
# Run directly without compilation
go run main.go

# Run with build flags
go run -v main.go

# Run package
go run ./cmd/service
```

### Build Compilation

#### Basic Build

```bash
# Build binary
go build -o {{ cookiecutter.service_slug }} main.go

# Build and run
./{{ cookiecutter.service_slug }}

# Build for specific OS/Architecture
GOOS=linux GOARCH=amd64 go build -o {{ cookiecutter.service_slug }}-linux main.go
GOOS=darwin GOARCH=amd64 go build -o {{ cookiecutter.service_slug }}-mac main.go
```

#### Build with Flags

```bash
# Set version during build
go build \
  -ldflags "-X main.Version=1.0.0 -X main.GitCommit=$(git rev-parse HEAD)" \
  -o {{ cookiecutter.service_slug }} main.go

# Optimize binary size
go build -ldflags "-s -w" -o {{ cookiecutter.service_slug }} main.go

# Strip debug symbols (smaller binary)
go build -trimpath -o {{ cookiecutter.service_slug }} main.go
```

#### Build Configuration in Makefile

```makefile
VERSION ?= 0.1.0
GIT_COMMIT := $(shell git rev-parse --short HEAD)
BUILD_TIME := $(shell date -u '+%Y-%m-%d_%H:%M:%S')

.PHONY: build
build:
	go build \
		-ldflags "-X main.Version=$(VERSION) -X main.GitCommit=$(GIT_COMMIT) -X main.BuildTime=$(BUILD_TIME)" \
		-o {{ cookiecutter.service_slug }} main.go

.PHONY: build-linux
build-linux:
	GOOS=linux GOARCH=amd64 make build

.PHONY: build-all
build-all: build build-linux

.PHONY: run
run:
	go run main.go
```

### Development Server

```bash
# Run with live reload (requires air or similar)
go install github.com/cosmtrek/air@latest
air

# Or using CompileDaemon
go install github.com/githubnemo/CompileDaemon@latest
CompileDaemon -build="go build -o {{ cookiecutter.service_slug }} main.go" -command={{ cookiecutter.service_slug }}
```

## Testing

### Test Structure

Go tests follow naming convention: `*_test.go`

```
{{ cookiecutter.service_slug }}/
├── main.go
├── service.go
├── service_test.go        # Unit tests
├── integration_test.go    # Integration tests (with build tag)
└── ...
```

### Running Tests

```bash
# Run all tests
go test ./...

# Run tests with verbose output
go test -v ./...

# Run specific test package
go test ./cmd/service

# Run specific test function
go test -run TestHealthCheck ./cmd/service

# Run tests matching pattern
go test -run "^Test.*Handler$" ./...

# Stop on first failure
go test -failfast ./...

# Run tests sequentially (default is parallel)
go test -p 1 ./...

# Run with timeout
go test -timeout 30s ./...
```

### Coverage Analysis

```bash
# Generate coverage report
go test -cover ./...

# Generate coverage to file
go test -coverprofile=coverage.out ./...

# View coverage in terminal
go tool cover -func=coverage.out

# Generate HTML coverage report
go tool cover -html=coverage.out -o coverage.html

# Set coverage threshold
go test -coverprofile=coverage.out ./... && \
  echo "Coverage: $(go tool cover -func=coverage.out | tail -1)"

# Exclude specific files from coverage
go test -cover -coverprofile=coverage.out \
  -coverpkg=./cmd/service,./internal/... ./...
```

### Test Types

#### Unit Tests

```go
package service

import "testing"

func TestHealthCheck(t *testing.T) {
    result := HealthCheck()
    if !result {
        t.Errorf("expected true, got %v", result)
    }
}

func TestValidateInput(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    bool
        wantErr bool
    }{
        {"valid", "test", true, false},
        {"empty", "", false, true},
        {"long", strings.Repeat("a", 1000), false, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ValidateInput(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateInput() error = %v, wantErr %v", err, tt.wantErr)
            }
            if got != tt.want {
                t.Errorf("ValidateInput() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

#### Table-Driven Tests

```go
func TestProcessData(t *testing.T) {
    tests := []struct {
        name      string
        data      string
        expected  string
        shouldErr bool
    }{
        {
            name:      "valid JSON",
            data:      `{"key": "value"}`,
            expected:  "value",
            shouldErr: false,
        },
        {
            name:      "invalid JSON",
            data:      `{invalid}`,
            expected:  "",
            shouldErr: true,
        },
    }

    for _, test := range tests {
        t.Run(test.name, func(t *testing.T) {
            result, err := ProcessData(test.data)
            if (err != nil) != test.shouldErr {
                t.Fatalf("expected error: %v, got: %v", test.shouldErr, err)
            }
            if result != test.expected {
                t.Errorf("expected %q, got %q", test.expected, result)
            }
        })
    }
}
```

#### Integration Tests (Build Tag)

```go
//go:build integration
// +build integration

package service

import "testing"

func TestIntegrationWithDatabase(t *testing.T) {
    // Integration test that requires database
    db := setupTestDB()
    defer db.Close()

    result, err := FetchUserFromDB(db, "123")
    if err != nil {
        t.Fatalf("failed to fetch user: %v", err)
    }
    if result.ID != "123" {
        t.Errorf("expected ID 123, got %v", result.ID)
    }
}
```

Run integration tests:

```bash
# Run only integration tests
go test -tags=integration ./...

# Run all tests including integration
go test -tags=integration -v ./...
```

### Mock and Testing Utilities

```go
package service

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

type MockDatabase struct {
    mock.Mock
}

func (m *MockDatabase) GetUser(id string) (User, error) {
    args := m.Called(id)
    return args.Get(0).(User), args.Error(1)
}

func TestGetUserWithMock(t *testing.T) {
    mockDB := new(MockDatabase)
    mockDB.On("GetUser", "123").Return(User{ID: "123"}, nil)

    result, err := GetUser(mockDB, "123")

    assert.NoError(t, err)
    assert.Equal(t, "123", result.ID)
    mockDB.AssertExpectations(t)
}
```

## Code Quality

### golangci-lint

golangci-lint is a fast Go linter with many checks enabled.

#### Installation

```bash
# Using Homebrew
brew install golangci-lint

# Using go install
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Docker
docker run --rm -v $(pwd):/app golangci/golangci-lint:latest golangci-lint run
```

#### Configuration (.golangci.yml)

```yaml
run:
  timeout: 5m
  modules-download-mode: readonly

linters:
  enable:
    - errcheck
    - govet
    - ineffassign
    - linters
    - staticcheck
    - typecheck
    - unused
    - misspell
    - goimports
    - revive
    - gosimple
    - gocritic
    - goerr113
    - contextcheck

linters-settings:
  govet:
    enable-all: true
  revive:
    rules:
      - name: exported
        disabled: false

issues:
  exclude-rules:
    - path: _test\.go
      linters:
        - govet
```

#### Running golangci-lint

```bash
# Run linter
golangci-lint run ./...

# Run with specific linters
golangci-lint run --no-config --disable-all -E errcheck -E govet ./...

# Fix issues automatically (where possible)
golangci-lint run --fix ./...

# Output in JSON format
golangci-lint run --out-format json ./...

# Report only new issues
golangci-lint run --new ./...
```

### Code Formatting

```bash
# Format code with gofmt
gofmt -s -w .

# Format using goimports (adds/removes imports)
goimports -w .

# Check if code is formatted
gofmt -l .

# Auto-format in editor (most editors support gofmt on save)
```

### Code Generation

```bash
# Generate mocks for testing
go generate ./...

# Or use mockgen specifically
mockgen -source=service.go -destination=mocks/mock_service.go

# Use go:generate directives in code
# Add to source file: //go:generate mockgen -source=$GOFILE -destination=mocks/mock_$GOFILE
```

## Development Workflow

### Using Makefile

```makefile
.PHONY: help
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d: -f1 | sort

.PHONY: install-tools
install-tools:
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install gotest.tools/gotestsum@latest

.PHONY: lint
lint:
	golangci-lint run ./...

.PHONY: test
test:
	go test -v -race -coverprofile=coverage.out ./...

.PHONY: test-coverage
test-coverage: test
	go tool cover -html=coverage.out -o coverage.html

.PHONY: build
build:
	go build -o {{ cookiecutter.service_slug }} main.go

.PHONY: run
run:
	go run main.go

.PHONY: clean
clean:
	go clean
	rm -f {{ cookiecutter.service_slug }}
	rm -f coverage.out coverage.html

.PHONY: all
all: lint test build
```

### Git Hooks

```bash
# Install pre-commit framework
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/golangci/golangci-lint
    rev: v1.54.0
    hooks:
      - id: golangci-lint

  - repo: https://github.com/pre-commit/mirrors-goimports
    rev: v0.1.0
    hooks:
      - id: goimports

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
EOF

# Install hooks
pre-commit install

# Run hooks
pre-commit run --all-files
```

## Best Practices

### 1. Project Structure

```
{{ cookiecutter.service_slug }}/
├── cmd/
│   └── service/
│       └── main.go        # Application entry point
├── internal/
│   ├── config/
│   │   └── config.go      # Configuration
│   ├── service/
│   │   └── service.go     # Business logic
│   ├── handler/
│   │   └── handler.go     # HTTP handlers
│   └── repository/
│       └── repository.go  # Data access
├── pkg/
│   └── models/            # Public domain models
├── go.mod
├── go.sum
├── main.go
├── Dockerfile
├── Makefile
└── README.md
```

### 2. Error Handling

```go
package service

import (
    "fmt"
    "errors"
)

var (
    ErrNotFound = errors.New("resource not found")
    ErrInvalid  = errors.New("invalid input")
)

func GetUser(id string) (User, error) {
    if id == "" {
        return User{}, fmt.Errorf("user ID cannot be empty: %w", ErrInvalid)
    }
    
    user, err := fetchFromDB(id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return User{}, fmt.Errorf("user %s not found: %w", id, ErrNotFound)
        }
        return User{}, fmt.Errorf("failed to fetch user: %w", err)
    }
    
    return user, nil
}

// Usage
user, err := GetUser("")
if errors.Is(err, ErrInvalid) {
    // Handle validation error
}
```

### 3. Context Usage

```go
package handler

import (
    "context"
    "net/http"
)

func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    
    // Add timeout
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    
    user, err := h.service.GetUser(ctx, userID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    
    json.NewEncoder(w).Encode(user)
}
```

### 4. Logging

```go
package main

import (
    "log/slog"
    "os"
)

func setupLogging() {
    opts := &slog.HandlerOptions{
        Level: slog.LevelInfo,
    }
    handler := slog.NewJSONHandler(os.Stdout, opts)
    logger := slog.New(handler)
    slog.SetDefault(logger)
}

func main() {
    setupLogging()
    slog.Info("Service started", "version", "1.0.0")
    
    if err := runServer(); err != nil {
        slog.Error("Server error", "err", err)
    }
}
```

### 5. Configuration Management

```go
package config

import (
    "os"
    "strconv"
)

type Config struct {
    ServiceName string
    Host        string
    Port        int
    LogLevel    string
    Debug       bool
}

func FromEnv() *Config {
    port, _ := strconv.Atoi(os.Getenv("PORT"))
    if port == 0 {
        port = 8000
    }
    
    return &Config{
        ServiceName: getEnv("SERVICE_NAME", "{{ cookiecutter.service_slug }}"),
        Host:        getEnv("HOST", "0.0.0.0"),
        Port:        port,
        LogLevel:    getEnv("LOG_LEVEL", "INFO"),
        Debug:       getEnv("DEBUG", "false") == "true",
    }
}

func getEnv(key, defaultValue string) string {
    if val := os.Getenv(key); val != "" {
        return val
    }
    return defaultValue
}
```

### 6. Interface Design

```go
package service

// Define interfaces for dependency injection
type UserRepository interface {
    GetUser(ctx context.Context, id string) (User, error)
    SaveUser(ctx context.Context, user User) error
}

type UserService struct {
    repo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

func (s *UserService) GetUser(ctx context.Context, id string) (User, error) {
    return s.repo.GetUser(ctx, id)
}
```

## Troubleshooting

### Module Issues

**Problem**: `go: github.com/foo/bar@vX.Y.Z: unknown revision`

```bash
# Solution: Update module index
go get -u github.com/foo/bar@latest
go mod tidy
```

**Problem**: `cannot find module providing package`

```bash
# Solution: Ensure module is in go.mod
go get github.com/missing/package
go mod tidy
go mod verify
```

### Build Errors

**Problem**: `undefined: someFunction`

```bash
# Solution: Check import paths and build tags
go build -x -v .  # Verbose output
```

**Problem**: Cross-compilation fails

```bash
# Solution: Check supported OS/ARCH combinations
go tool dist list  # List all supported combinations

# Use correct flags
GOOS=linux GOARCH=amd64 go build -o app main.go
```

### Test Failures

**Problem**: Race condition detected

```bash
# Solution: Use race detector (slower but finds races)
go test -race ./...

# Profile the race
go test -race -cpuprofile=cpu.prof ./...
```

**Problem**: Tests timeout

```bash
# Solution: Increase timeout or identify slow tests
go test -timeout 60s ./...
go test -timeout 10s -run TestSlowFunction -v
```

### Performance Profiling

```bash
# CPU profiling
go test -cpuprofile=cpu.prof -benchmem -bench=. ./...
go tool pprof cpu.prof

# Memory profiling
go test -memprofile=mem.prof -benchmem -bench=. ./...
go tool pprof mem.prof

# View profiles
go tool pprof -http=:8080 cpu.prof
```

## Resources

- [Go Official Documentation](https://go.dev/doc/)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [golangci-lint](https://golangci-lint.run/)
- [Go Testing Best Practices](https://golang.org/doc/effective_go#tests)
- [Standard Library Package Docs](https://pkg.go.dev/)

## See Also

- [PYTHON.md](./PYTHON.md) - Python-specific development guide
- [NODEJS.md](./NODEJS.md) - Node.js-specific development guide
- [Makefile](./Makefile) - Build automation
- [go.mod](./go.mod) - Module definition
