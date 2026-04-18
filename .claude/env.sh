#!/usr/bin/env bash
# Sourced before each Claude Bash command. Add exports here.

export PATH="$HOME/.local/bin:$PATH"
export CLAUDE_CODE_MAX_OUTPUT_TOKENS="8000"
export DISABLE_TELEMETRY="1"
export DISABLE_NON_ESSENTIAL_MODEL_CALLS="1"
export DISABLE_COST_WARNINGS="1"
export USE_BUILTIN_RIPGREP="1"
export CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR="1"
export CLAUDE_CODE_DISABLE_TERMINAL_TITLE="0"
export CLAUDE_AUDIO_DIR="~/.claude/audio"
export TTS_VOLUME="0.3"
export ENGINEER_NAME="James Anthonyrajah"
export CLAUDE_WORKFLOW_DIR="/Users/jamesanthonyrajah/Projects-Revamped/turing_workspace/cookiecutter-microservices-template/workflows"
export CLAUDE_AGENTS_DIR="/Users/jamesanthonyrajah/Projects-Revamped/turing_workspace/cookiecutter-microservices-template/.agents"
export CLAUDE_SESSIONS_DIR="/Users/jamesanthonyrajah/Projects-Revamped/turing_workspace/cookiecutter-microservices-template/.claude/data/sessions"
export CLAUDE_CHECKPOINTS_DIR="/Users/jamesanthonyrajah/Projects-Revamped/turing_workspace/cookiecutter-microservices-template/.claude/data/sessions/checkpoints"
export CLAUDE_PROJECT_DIR="/Users/jamesanthonyrajah/Projects-Revamped/turing_workspace/cookiecutter-microservices-template"
export CLAUDE_ENV_FILE="/Users/jamesanthonyrajah/Projects-Revamped/turing_workspace/cookiecutter-microservices-template/.claude/env.sh"

# API Keys are stored in .env file (gitignored)
# Source .env if it exists to load API keys
if [ -f "${CLAUDE_PROJECT_DIR}/.env" ]; then
  set -a
  source "${CLAUDE_PROJECT_DIR}/.env"
  set +a
fi
