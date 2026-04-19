# How `cookiecutter-poetry-project` is Structured

## Anatomy of a Cookiecutter Template

Three core components:

### 1. `cookiecutter.json` — The prompt manifest
Defines all variables the user is asked for (project name, slug, package name, Python version, GitHub visibility, etc.) plus their defaults. Every `{{ cookiecutter.variable }}` reference in the template resolves from this file.

### 2. `{{ cookiecutter.project_slug }}/` — The template tree
The entire output skeleton lives under a Jinja2-named directory. Everything inside gets rendered on generation — filenames, file contents, directory names — with `{{ cookiecutter.* }}` placeholders substituted. The resulting structure is:
```
src/<package_name>/      # src layout with hello() stub
tests/                   # Pytest + sample test
.github/workflows/ci.yml # GitHub Actions CI
pyproject.toml           # Poetry + Commitizen config
Taskfile.yml             # pyenv/venv/poetry automation
.pre-commit-config.yaml  # Black + commitizen enforcement
```

### 3. `hooks/` — Lifecycle scripts
- `pre_gen_project.py` — Validates inputs (slug regex, valid Python identifier) before any files are written
- `post_gen_project.py` — Runs after generation: `git init`, initial commit, version tag, `task setup`, pre-commit install, optionally `gh repo create`

---

## Key Variables (cookiecutter.json)

| Variable | Default | Purpose |
|---|---|---|
| `project_name` | "My Project" | Human-readable name |
| `project_slug` | "my_project" | Directory/repo identifier |
| `package_name` | "my_project" | Python package name |
| `version` | "0.1.0" | Initial semantic version |
| `description` | — | One-line description |
| `author` | "K3rm1t" | Author name |
| `email` | janthonyrajah@gmail.com | Author email |
| `license` | "MIT" | Project license |
| `python_version` | "3.10.13" | pyenv Python version |
| `create_github_repo` | "yes" | Auto-create GitHub repo |
| `repo_visibility` | ["private", "public"] | GitHub visibility |

---

## Key Design Decisions

- **`src/` layout** — package code lives under `src/<package_name>/`, not at root
- **Commitizen + pre-commit** — enforces conventional commits and auto-bumps versions
- **`Taskfile.yml`** replaces Makefile for common dev tasks (`setup`, `clean`, `run`, `shell`)
- **Post-hook does heavy lifting** — the generated project is immediately runnable, not just scaffolded
- **Commitizen** manages semantic versioning with version files in both `pyproject.toml` and `__init__.py`
- **GitHub Actions CI** — runs pytest on push to main/master and on PRs

---

## What the Template Generates

A complete, production-ready Python project skeleton with:
- Structured `src/` layout per Python best practices
- Poetry for reproducible dependency management
- Automated pyenv + virtualenv setup via Task
- Pytest + pytest-asyncio with sample test
- Pre-commit hooks enforcing black formatting and conventional commits
- Commitizen automatic semantic versioning with changelog
- GitHub Actions CI workflow
- Auto-initialized git repo with initial commit and version tag
- Optional GitHub remote repo creation and push on generation
