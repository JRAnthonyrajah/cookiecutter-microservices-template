# Claude Setup - Plugin Ecosystem Repository

This repository contains **claude-setup**, a production-grade plugin ecosystem providing 6 integrated plugins, 24+ specialized agents, 50+ commands, 8+ skills, and 75+ hooks for comprehensive Claude Code configuration and automation.

## Marketplace & Plugin Configuration

- **Marketplace:** `.claude-plugin/marketplace.json` — Private marketplace "james-core-marketplace" (v1.0.0) containing all plugins
- **Installation:** `claude plugin install claude-setup` (installs entire ecosystem)

## Plugins in This Repository

**Local plugins** (source: `plugins/<name>/`):
- `kernel` — Core orchestration: agents, commands, skills, deterministic execution framework
- `kernel-hooks` — Event-driven automation: 75+ hooks, TTS notifications, token tracking, schema validation
- `drivers` — External integrations: speech-to-text, image generation, video analysis
- `supervisor` — Expert system for repository-scoped agent coordination
- `userland` — User-facing utilities: documentation management, component evolution, project tools

**External plugins** (hosted on GitHub):
- `scheduler` — Task scheduling and workflow orchestration
- `thinker` — Advanced brainstorming with 62+ creative techniques
- `turing-connector` — WebSocket dashboard integration
- `ralph` — Configurable Claude Code loops

## Project Ground Rules

### Imported Modular Rules

- Python development: @.claude/rules/python-dev.md
- Configuration management: @.claude/rules/config-management.md
- Agent development: @.claude/rules/agent-development.md
- Plugin development: @.claude/rules/plugin-development.md
- Documentation standards: @.claude/rules/documentation-standards.md
- Testing guidelines: @.claude/rules/testing-guidelines.md
