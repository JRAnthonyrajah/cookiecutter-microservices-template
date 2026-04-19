# Node.js Development Guide

This guide covers Node.js-specific setup, development, testing, and best practices for the `{{ cookiecutter.service_name }}` microservice.

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Package Management](#package-management)
3. [Running and Debugging](#running-and-debugging)
4. [Testing](#testing)
5. [Code Quality](#code-quality)
6. [Development Workflow](#development-workflow)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Environment Setup

### Installing Node.js

#### Using nvm (Node Version Manager) - Recommended

```bash
# Install nvm (macOS/Linux)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell configuration
source ~/.zshrc  # Or ~/.bashrc for bash

# List available Node versions
nvm list-remote

# Install specific version
nvm install 18.17.0
nvm install 20.9.0  # Current LTS

# Set default version
nvm alias default 20.9.0

# Use specific version in project
nvm use 20.9.0

# Verify installation
node --version
npm --version
```

#### macOS with Homebrew

```bash
# Install Node.js
brew install node

# Update to latest
brew upgrade node

# Verify
node --version
npm --version
```

#### Linux (Ubuntu/Debian)

```bash
# Using NodeSource repository (recommended)
curl -sL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Or using snap
sudo snap install node --classic

# Verify
node --version
npm --version
```

### Project Setup

```bash
# Initialize project (if not already initialized)
npm init -y

# Or with interactive prompt
npm init

# Install dependencies from package.json
npm install

# Install and update to latest versions
npm install --save-latest
```

## Package Management

### Understanding package.json

```json
{
  "name": "{{ cookiecutter.service_slug }}",
  "version": "0.1.0",
  "description": "{{ cookiecutter.service_description }}",
  "main": "src/index.js",
  "type": "module",
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint .",
    "lint:fix": "eslint --fix .",
    "format": "prettier --write .",
    "build": "tsc",
    "clean": "rm -rf dist/ node_modules/"
  },
  "keywords": ["microservice", "api"],
  "author": "",
  "license": "MIT",
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "dependencies": {
    "express": "^4.18.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "@types/node": "^20.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "nodemon": "^3.0.0"
  }
}
```

### Managing Dependencies

```bash
# Install all dependencies
npm install

# Install specific package
npm install express

# Install specific version
npm install express@4.18.0

# Install as dev dependency
npm install --save-dev jest

# Install globally
npm install -g nodemon

# Update all packages
npm update

# Update specific package
npm update express

# Check for outdated packages
npm outdated

# Audit for security vulnerabilities
npm audit

# Fix security vulnerabilities
npm audit fix

# Remove dependency
npm uninstall express

# Remove dev dependency
npm uninstall --save-dev jest

# Clean install (remove node_modules and reinstall)
rm -rf node_modules package-lock.json
npm install
```

### Using npm Workspaces (Monorepo)

```json
{
  "name": "monorepo",
  "workspaces": [
    "packages/*"
  ]
}
```

```bash
# Install all workspace dependencies
npm install

# Run script in all workspaces
npm run build --workspaces

# Run script in specific workspace
npm run build --workspace=packages/service-1
```

### package-lock.json

Always commit `package-lock.json` to version control to ensure reproducible installs:

```bash
# Use exact versions from package-lock.json
npm ci  # Use instead of npm install in CI/CD

# Regenerate lock file
npm install --package-lock-only
```

## Running and Debugging

### Starting the Service

```bash
# Production start (requires npm start script)
npm start

# Development with auto-reload using nodemon
npm run dev

# Run specific file
node src/index.js

# Run with environment variables
NODE_ENV=development PORT=3000 npm run dev

# Run with inspector for debugging
node --inspect src/index.js

# Run with inspector listening on specific port
node --inspect=9229 src/index.js
```

### Debugging

#### Built-in Node Inspector

```bash
# Start with debugger
node --inspect src/index.js

# Connect in Chrome DevTools
# Open chrome://inspect
# Find and click "inspect" on your app

# Start debugger paused at startup
node --inspect-brk src/index.js
```

#### Using VS Code Debugger

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Program",
      "program": "${workspaceFolder}/src/index.js",
      "restart": true,
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen"
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Process",
      "port": 9229,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

#### Using console Methods

```javascript
// Simple logging
console.log("Message:", variable);
console.warn("Warning message");
console.error("Error message");

// Structured logging
console.dir(object, { depth: 2 });
console.table([{id: 1}, {id: 2}]);

// Timing
console.time("label");
// ... code ...
console.timeEnd("label");
```

#### Using Debug Module

```bash
# Install debug
npm install debug

# Use in code
const debug = require('debug')('{{ cookiecutter.service_slug }}');

debug('Starting service');
debug('Request received: %o', req);
```

```bash
# Run with debug output
DEBUG={{ cookiecutter.service_slug }}:* npm run dev
DEBUG=*:* npm run dev  # All debug output
```

### Environment Variables

Create `.env` file:

```bash
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug
DATABASE_URL=postgresql://localhost/db
API_KEY=secret123
```

Load with dotenv:

```bash
npm install dotenv
```

```javascript
import dotenv from 'dotenv';
dotenv.config();

const port = process.env.PORT || 3000;
const dbUrl = process.env.DATABASE_URL;
```

## Testing

### Jest Configuration

```javascript
// jest.config.js
export default {
  testEnvironment: 'node',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/**/*.test.js',
    '!src/index.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testMatch: [
    '**/__tests__/**/*.js',
    '**/?(*.)+(spec|test).js'
  ],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  timeout: 30000,
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  }
};
```

### Writing Tests

#### Unit Tests

```javascript
// src/service.test.js
import { calculateSum, validateInput } from './service.js';

describe('Service', () => {
  describe('calculateSum', () => {
    it('should sum two numbers', () => {
      const result = calculateSum(2, 3);
      expect(result).toBe(5);
    });

    it('should handle negative numbers', () => {
      const result = calculateSum(-2, 3);
      expect(result).toBe(1);
    });

    it('should handle zero', () => {
      const result = calculateSum(0, 0);
      expect(result).toBe(0);
    });
  });

  describe('validateInput', () => {
    it('should return true for valid input', () => {
      expect(validateInput('test')).toBe(true);
    });

    it('should return false for empty input', () => {
      expect(validateInput('')).toBe(false);
    });

    it('should return false for null', () => {
      expect(validateInput(null)).toBe(false);
    });
  });
});
```

#### Async Tests

```javascript
// Handle async operations
describe('API Tests', () => {
  it('should fetch user data', async () => {
    const response = await fetchUser('123');
    expect(response.id).toBe('123');
  });

  it('should handle errors', async () => {
    await expect(fetchUser('')).rejects.toThrow('Invalid user ID');
  });
});
```

#### Mocking

```javascript
import { getUserFromDB } from './database.js';

jest.mock('./database.js');

describe('User Service', () => {
  it('should get user', async () => {
    getUserFromDB.mockResolvedValue({ id: '123', name: 'Test' });

    const result = await getUser('123');

    expect(result.name).toBe('Test');
    expect(getUserFromDB).toHaveBeenCalledWith('123');
  });

  it('should handle database error', async () => {
    getUserFromDB.mockRejectedValue(new Error('DB Error'));

    await expect(getUser('123')).rejects.toThrow('DB Error');
  });
});
```

### Running Tests

```bash
# Run all tests
npm test

# Run specific test file
npm test -- service.test.js

# Run tests matching pattern
npm test -- --testNamePattern="calculateSum"

# Watch mode (re-run on changes)
npm run test:watch

# Coverage report
npm run test:coverage

# Generate HTML coverage report
npm test -- --coverage --coverageReporters=html

# Run with verbose output
npm test -- --verbose

# Update snapshots
npm test -- -u

# Run single test file
npm test -- service.test.js --testNamePattern="sum"
```

## Code Quality

### ESLint Configuration

```javascript
// .eslintrc.js or eslintrc.json
{
  "env": {
    "node": true,
    "es2021": true,
    "jest": true
  },
  "extends": [
    "eslint:recommended"
  ],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "prefer-const": "error",
    "no-var": "error",
    "eqeqeq": "error",
    "no-implicit-coercion": "error",
    "curly": "error",
    "indent": ["error", 2],
    "quotes": ["error", "single", { "avoidEscape": true }],
    "semi": ["error", "always"],
    "comma-dangle": ["error", "always-multiline"],
    "arrow-spacing": "error"
  }
}
```

### Prettier Configuration

```javascript
// .prettierrc.js
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always"
}
```

### Running Linting and Formatting

```bash
# Check for linting errors
npm run lint

# Fix linting errors
npm run lint:fix

# Format code
npm run format

# Check if code is formatted (dry-run)
npm run format -- --check

# Lint and format in one command
npm run lint:fix && npm run format
```

### Pre-commit Hooks with husky

```bash
# Install husky
npm install --save-dev husky
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "npm run lint:fix && npm run format"

# Add pre-push hook
npx husky add .husky/pre-push "npm test"
```

## Development Workflow

### Makefile Example

```makefile
.PHONY: help
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d: -f1

.PHONY: install
install:
	npm install

.PHONY: dev
dev:
	npm run dev

.PHONY: test
test:
	npm test

.PHONY: test-watch
test-watch:
	npm run test:watch

.PHONY: test-coverage
test-coverage:
	npm run test:coverage

.PHONY: lint
lint:
	npm run lint

.PHONY: lint-fix
lint-fix:
	npm run lint:fix

.PHONY: format
format:
	npm run format

.PHONY: build
build:
	npm run build

.PHONY: start
start:
	npm start

.PHONY: clean
clean:
	rm -rf node_modules dist coverage

.PHONY: all
all: lint test build
```

## Best Practices

### 1. Project Structure

```
{{ cookiecutter.service_slug }}/
├── src/
│   ├── index.js           # Application entry point
│   ├── config.js          # Configuration management
│   ├── app.js             # Express app setup
│   ├── server.js          # Server initialization
│   ├── services/
│   │   └── userService.js # Business logic
│   ├── controllers/
│   │   └── userController.js  # Route handlers
│   ├── models/
│   │   └── User.js        # Data models
│   ├── routes/
│   │   └── users.js       # Route definitions
│   ├── middleware/
│   │   └── errorHandler.js # Middleware functions
│   └── utils/
│       └── logger.js      # Utility functions
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── .env
├── .env.example
├── .eslintrc.js
├── .prettierrc.js
├── jest.config.js
├── package.json
├── package-lock.json
└── README.md
```

### 2. Error Handling

```javascript
// Custom error class
class ServiceError extends Error {
  constructor(message, statusCode = 500, code = 'INTERNAL_ERROR') {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

class ValidationError extends ServiceError {
  constructor(message, field = null) {
    super(message, 400, 'VALIDATION_ERROR');
    this.field = field;
  }
}

class NotFoundError extends ServiceError {
  constructor(resource) {
    super(`${resource} not found`, 404, 'NOT_FOUND');
    this.resource = resource;
  }
}

// Error handling middleware
function errorHandler(err, req, res, next) {
  const statusCode = err.statusCode || 500;
  const code = err.code || 'INTERNAL_ERROR';
  
  logger.error('Request error', { error: err, statusCode, code });
  
  res.status(statusCode).json({
    error: {
      code,
      message: err.message,
      field: err.field,
    },
  });
}

app.use(errorHandler);
```

### 3. Logging

```javascript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json(),
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
  ],
});

export default logger;
```

### 4. Configuration Management

```javascript
// config.js
const config = {
  development: {
    host: process.env.HOST || 'localhost',
    port: process.env.PORT || 3000,
    logLevel: 'debug',
    debug: true,
  },
  production: {
    host: process.env.HOST || '0.0.0.0',
    port: process.env.PORT || 8000,
    logLevel: 'info',
    debug: false,
  },
};

export default config[process.env.NODE_ENV || 'development'];
```

### 5. Async/Await Best Practices

```javascript
// Good: Proper error handling
async function getUser(id) {
  try {
    const user = await db.find(id);
    if (!user) {
      throw new NotFoundError('User');
    }
    return user;
  } catch (error) {
    logger.error('Failed to get user', { id, error });
    throw error;
  }
}

// Good: Concurrent operations
async function getMultipleUsers(ids) {
  const users = await Promise.all(
    ids.map(id => getUser(id)),
  );
  return users;
}

// Good: Timeout handling
async function fetchWithTimeout(url, timeout = 5000) {
  return Promise.race([
    fetch(url),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), timeout),
    ),
  ]);
}
```

### 6. Express Best Practices

```javascript
import express from 'express';
import logger from './utils/logger.js';

const app = express();

// Middleware
app.use(express.json());
app.use((req, res, next) => {
  req.id = crypto.randomUUID();
  logger.info('Incoming request', { 
    method: req.method, 
    path: req.path,
    requestId: req.id,
  });
  next();
});

// Routes
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await getUser(req.params.id);
    res.json(user);
  } catch (error) {
    next(error);
  }
});

// Error handler (last middleware)
app.use((err, req, res, next) => {
  logger.error('Unhandled error', { error: err });
  res.status(500).json({ error: 'Internal server error' });
});

export default app;
```

## Troubleshooting

### Module Errors

**Problem**: `Cannot find module 'express'`

```bash
# Solution: Install dependencies
npm install

# Or specific package
npm install express

# Check if package.json is correct
cat package.json
```

**Problem**: `Module resolution issues with ES modules`

```json
// Ensure in package.json
{
  "type": "module",
  "engines": {
    "node": ">=14.0.0"
  }
}
```

### Permission Errors

**Problem**: `EACCES: permission denied`

```bash
# Solution: Don't use sudo
# Instead, fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

### Memory Issues

**Problem**: `JavaScript heap out of memory`

```bash
# Solution: Increase heap size
node --max-old-space-size=4096 src/index.js

# Or in npm script
NODE_OPTIONS=--max-old-space-size=4096 npm start
```

### Debugging Tests

**Problem**: Tests fail intermittently

```bash
# Solution: Run tests sequentially and with verbose output
npm test -- --runInBand -v --detectOpenHandles

# Check for unresolved promises
jest.setTimeout(30000);  // in jest.config.js
```

## Resources

- [Node.js Documentation](https://nodejs.org/docs/)
- [npm Documentation](https://docs.npmjs.com/)
- [Express.js Guide](https://expressjs.com/)
- [Jest Testing Framework](https://jestjs.io/)
- [ESLint Documentation](https://eslint.org/docs/)
- [Prettier Code Formatter](https://prettier.io/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)

## See Also

- [PYTHON.md](./PYTHON.md) - Python-specific development guide
- [GO.md](./GO.md) - Go-specific development guide
- [Makefile](./Makefile) - Build automation
- [package.json](./package.json) - Project configuration
