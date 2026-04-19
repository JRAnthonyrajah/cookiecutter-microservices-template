"""
Comprehensive test suite for per-language implementation guides.

Tests validate:
- File existence and markdown validity
- Content coverage (setup, testing, quality tools)
- Code examples syntax and completeness
- Tool configuration references
- Best practices coverage
- Troubleshooting sections
- Cross-references and links
"""

import os
import re
from pathlib import Path

import pytest


class TestLanguageGuidesExistence:
    """Test that all language guide files exist."""

    @pytest.fixture
    def cookiecutter_dir(self):
        """Get cookiecutter template directory."""
        return Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}"

    def test_python_md_exists(self, cookiecutter_dir):
        """Python guide should exist."""
        python_guide = cookiecutter_dir / "PYTHON.md"
        assert python_guide.exists(), "PYTHON.md should exist"
        assert python_guide.is_file(), "PYTHON.md should be a file"

    def test_go_md_exists(self, cookiecutter_dir):
        """Go guide should exist."""
        go_guide = cookiecutter_dir / "GO.md"
        assert go_guide.exists(), "GO.md should exist"
        assert go_guide.is_file(), "GO.md should be a file"

    def test_nodejs_md_exists(self, cookiecutter_dir):
        """Node.js guide should exist."""
        nodejs_guide = cookiecutter_dir / "NODEJS.md"
        assert nodejs_guide.exists(), "NODEJS.md should exist"
        assert nodejs_guide.is_file(), "NODEJS.md should be a file"


class TestMarkdownValidity:
    """Test markdown structure and validity."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_title(self, python_content):
        """Python guide should have a title."""
        assert python_content.startswith("# Python Development Guide")

    def test_go_has_title(self, go_content):
        """Go guide should have a title."""
        assert go_content.startswith("# Go Development Guide")

    def test_nodejs_has_title(self, nodejs_content):
        """Node.js guide should have a title."""
        assert nodejs_content.startswith("# Node.js Development Guide")

    def test_python_has_table_of_contents(self, python_content):
        """Python guide should have table of contents."""
        assert "## Table of Contents" in python_content

    def test_go_has_table_of_contents(self, go_content):
        """Go guide should have table of contents."""
        assert "## Table of Contents" in go_content

    def test_nodejs_has_table_of_contents(self, nodejs_content):
        """Node.js guide should have table of contents."""
        assert "## Table of Contents" in nodejs_content


class TestEnvironmentSetup:
    """Test environment setup section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_environment_setup(self, python_content):
        """Python guide should have environment setup section."""
        assert "## Environment Setup" in python_content

    def test_python_covers_venv(self, python_content):
        """Python guide should cover venv."""
        assert "venv" in python_content.lower()

    def test_python_covers_pyenv(self, python_content):
        """Python guide should cover pyenv."""
        assert "pyenv" in python_content.lower()

    def test_go_has_environment_setup(self, go_content):
        """Go guide should have environment setup section."""
        assert "## Environment Setup" in go_content

    def test_go_covers_installation(self, go_content):
        """Go guide should cover installation methods."""
        assert "brew install go" in go_content or "Download" in go_content

    def test_nodejs_has_environment_setup(self, nodejs_content):
        """Node.js guide should have environment setup section."""
        assert "## Environment Setup" in nodejs_content

    def test_nodejs_covers_nvm(self, nodejs_content):
        """Node.js guide should cover nvm."""
        assert "nvm" in nodejs_content.lower()


class TestDependenciesManagement:
    """Test dependency management section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_dependencies_section(self, python_content):
        """Python guide should have dependencies section."""
        assert "## Dependencies Management" in python_content

    def test_python_covers_pyproject_toml(self, python_content):
        """Python guide should mention pyproject.toml."""
        assert "pyproject.toml" in python_content

    def test_python_covers_poetry(self, python_content):
        """Python guide should mention Poetry."""
        assert "poetry" in python_content.lower()

    def test_go_has_module_management(self, go_content):
        """Go guide should have module management section."""
        assert "## Module Management" in go_content

    def test_go_covers_go_mod(self, go_content):
        """Go guide should mention go.mod."""
        assert "go.mod" in go_content

    def test_nodejs_has_package_management(self, nodejs_content):
        """Node.js guide should have package management section."""
        assert "## Package Management" in nodejs_content

    def test_nodejs_covers_package_json(self, nodejs_content):
        """Node.js guide should mention package.json."""
        assert "package.json" in nodejs_content


class TestTestingFrameworks:
    """Test testing section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_tests_section(self, python_content):
        """Python guide should have testing section."""
        assert "## Running Tests" in python_content

    def test_python_mentions_pytest(self, python_content):
        """Python guide should mention pytest."""
        assert "pytest" in python_content.lower()

    def test_python_covers_coverage(self, python_content):
        """Python guide should cover coverage testing."""
        assert "coverage" in python_content.lower()

    def test_go_has_tests_section(self, go_content):
        """Go guide should have testing section."""
        assert "## Testing" in go_content

    def test_go_mentions_go_test(self, go_content):
        """Go guide should mention go test."""
        assert "go test" in go_content

    def test_go_covers_table_driven_tests(self, go_content):
        """Go guide should cover table-driven tests."""
        assert "Table-Driven Tests" in go_content

    def test_nodejs_has_tests_section(self, nodejs_content):
        """Node.js guide should have testing section."""
        assert "## Testing" in nodejs_content

    def test_nodejs_mentions_jest(self, nodejs_content):
        """Node.js guide should mention Jest."""
        assert "jest" in nodejs_content.lower()


class TestCodeQuality:
    """Test code quality section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_code_quality_section(self, python_content):
        """Python guide should have code quality section."""
        assert "## Code Quality" in python_content

    def test_python_mentions_ruff(self, python_content):
        """Python guide should mention Ruff."""
        assert "Ruff" in python_content

    def test_python_mentions_black(self, python_content):
        """Python guide should mention Black."""
        assert "Black" in python_content

    def test_go_has_code_quality_section(self, go_content):
        """Go guide should have code quality section."""
        assert "## Code Quality" in go_content

    def test_go_mentions_golangci_lint(self, go_content):
        """Go guide should mention golangci-lint."""
        assert "golangci-lint" in go_content

    def test_nodejs_has_code_quality_section(self, nodejs_content):
        """Node.js guide should have code quality section."""
        assert "## Code Quality" in nodejs_content

    def test_nodejs_mentions_eslint(self, nodejs_content):
        """Node.js guide should mention ESLint."""
        assert "ESLint" in nodejs_content

    def test_nodejs_mentions_prettier(self, nodejs_content):
        """Node.js guide should mention Prettier."""
        assert "Prettier" in nodejs_content


class TestTypeChecking:
    """Test type checking section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_type_checking_section(self, python_content):
        """Python guide should have type checking section."""
        assert "## Type Checking" in python_content

    def test_python_mentions_mypy(self, python_content):
        """Python guide should mention mypy."""
        assert "mypy" in python_content.lower()

    def test_python_has_type_hints_examples(self, python_content):
        """Python guide should have type hint examples."""
        assert "from typing import" in python_content


class TestCodeExamples:
    """Test code example validity and completeness."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_code_blocks(self, python_content):
        """Python guide should have code blocks."""
        assert "```python" in python_content or "```bash" in python_content

    def test_python_has_toml_examples(self, python_content):
        """Python guide should have TOML configuration examples."""
        assert "```toml" in python_content

    def test_go_has_code_blocks(self, go_content):
        """Go guide should have Go code blocks."""
        assert "```go" in go_content or "```bash" in go_content

    def test_go_has_yaml_examples(self, go_content):
        """Go guide should have YAML configuration examples."""
        assert "```yaml" in go_content

    def test_nodejs_has_code_blocks(self, nodejs_content):
        """Node.js guide should have JavaScript code blocks."""
        assert "```javascript" in nodejs_content or "```bash" in nodejs_content

    def test_nodejs_has_json_examples(self, nodejs_content):
        """Node.js guide should have JSON configuration examples."""
        assert "```json" in nodejs_content


class TestProjectStructure:
    """Test project structure section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_structure_section(self, python_content):
        """Python guide should show project structure."""
        assert "src/" in python_content
        assert "tests/" in python_content

    def test_go_has_structure_section(self, go_content):
        """Go guide should show project structure."""
        assert "cmd/" in go_content
        assert "internal/" in go_content

    def test_nodejs_has_structure_section(self, nodejs_content):
        """Node.js guide should show project structure."""
        assert "src/" in nodejs_content
        assert "tests/" in nodejs_content


class TestBestPractices:
    """Test best practices section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_best_practices(self, python_content):
        """Python guide should have best practices section."""
        assert "## Best Practices" in python_content

    def test_python_covers_error_handling(self, python_content):
        """Python guide should cover error handling."""
        assert "Error Handling" in python_content or "error" in python_content.lower()

    def test_python_covers_logging(self, python_content):
        """Python guide should cover logging."""
        assert "Logging" in python_content or "logger" in python_content.lower()

    def test_go_has_best_practices(self, go_content):
        """Go guide should have best practices section."""
        assert "## Best Practices" in go_content

    def test_go_covers_error_handling(self, go_content):
        """Go guide should cover error handling."""
        assert "Error Handling" in go_content

    def test_nodejs_has_best_practices(self, nodejs_content):
        """Node.js guide should have best practices section."""
        assert "## Best Practices" in nodejs_content

    def test_nodejs_covers_error_handling(self, nodejs_content):
        """Node.js guide should cover error handling."""
        assert "Error Handling" in nodejs_content or "Custom error" in nodejs_content


class TestTroubleshooting:
    """Test troubleshooting section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_troubleshooting(self, python_content):
        """Python guide should have troubleshooting section."""
        assert "## Troubleshooting" in python_content

    def test_python_troubleshooting_has_problems(self, python_content):
        """Python troubleshooting should have problem/solution pairs."""
        assert "Problem" in python_content or "problem" in python_content.lower()

    def test_go_has_troubleshooting(self, go_content):
        """Go guide should have troubleshooting section."""
        assert "## Troubleshooting" in go_content

    def test_nodejs_has_troubleshooting(self, nodejs_content):
        """Node.js guide should have troubleshooting section."""
        assert "## Troubleshooting" in nodejs_content


class TestResources:
    """Test resources section coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_resources(self, python_content):
        """Python guide should have resources section."""
        assert "## Resources" in python_content

    def test_python_has_external_links(self, python_content):
        """Python guide should have external documentation links."""
        assert "http" in python_content

    def test_go_has_resources(self, go_content):
        """Go guide should have resources section."""
        assert "## Resources" in go_content

    def test_nodejs_has_resources(self, nodejs_content):
        """Node.js guide should have resources section."""
        assert "## Resources" in nodejs_content


class TestCrossReferences:
    """Test cross-references between guides."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_references_other_guides(self, python_content):
        """Python guide should reference other language guides."""
        assert "GO.md" in python_content or "Go" in python_content
        assert "NODEJS.md" in python_content or "Node.js" in python_content

    def test_go_references_other_guides(self, go_content):
        """Go guide should reference other language guides."""
        assert "PYTHON.md" in go_content or "Python" in go_content
        assert "NODEJS.md" in go_content or "Node.js" in go_content

    def test_nodejs_references_other_guides(self, nodejs_content):
        """Node.js guide should reference other language guides."""
        assert "PYTHON.md" in nodejs_content or "Python" in nodejs_content
        assert "GO.md" in nodejs_content or "Go" in nodejs_content


class TestConfigurationFiles:
    """Test references to configuration files."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_references_pyproject_toml(self, python_content):
        """Python guide should reference pyproject.toml."""
        assert "pyproject.toml" in python_content

    def test_python_references_makefile(self, python_content):
        """Python guide should reference Makefile."""
        assert "Makefile" in python_content

    def test_go_references_go_mod(self, go_content):
        """Go guide should reference go.mod."""
        assert "go.mod" in go_content

    def test_nodejs_references_package_json(self, nodejs_content):
        """Node.js guide should reference package.json."""
        assert "package.json" in nodejs_content


class TestMakefileReferences:
    """Test references to Makefile targets."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_mentions_make_lint(self, python_content):
        """Python guide should mention make lint."""
        assert "make lint" in python_content.lower()

    def test_python_mentions_make_test(self, python_content):
        """Python guide should mention make test."""
        assert "make test" in python_content.lower()

    def test_go_mentions_makefile(self, go_content):
        """Go guide should mention Makefile usage."""
        assert "Makefile" in go_content or "make" in go_content.lower()

    def test_nodejs_mentions_make_targets(self, nodejs_content):
        """Node.js guide should mention make targets."""
        assert "make" in nodejs_content.lower()


class TestDocumentationCompleteness:
    """Test overall documentation completeness."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_minimum_length(self, python_content):
        """Python guide should be comprehensive."""
        assert len(python_content) > 5000, "Python guide should be detailed"

    def test_go_has_minimum_length(self, go_content):
        """Go guide should be comprehensive."""
        assert len(go_content) > 5000, "Go guide should be detailed"

    def test_nodejs_has_minimum_length(self, nodejs_content):
        """Node.js guide should be comprehensive."""
        assert len(nodejs_content) > 5000, "Node.js guide should be detailed"

    def test_python_has_multiple_sections(self, python_content):
        """Python guide should have multiple main sections."""
        section_count = python_content.count("## ")
        assert section_count >= 8, f"Python guide should have at least 8 sections, has {section_count}"

    def test_go_has_multiple_sections(self, go_content):
        """Go guide should have multiple main sections."""
        section_count = go_content.count("## ")
        assert section_count >= 8, f"Go guide should have at least 8 sections, has {section_count}"

    def test_nodejs_has_multiple_sections(self, nodejs_content):
        """Node.js guide should have multiple main sections."""
        section_count = nodejs_content.count("## ")
        assert section_count >= 8, f"Node.js guide should have at least 8 sections, has {section_count}"


class TestWorkflowCoverage:
    """Test workflow and development process coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_has_workflow_section(self, python_content):
        """Python guide should have development workflow section."""
        assert "Development Workflow" in python_content or "workflow" in python_content.lower()

    def test_go_has_workflow_section(self, go_content):
        """Go guide should have development workflow section."""
        assert "Development Workflow" in go_content or "workflow" in go_content.lower()

    def test_nodejs_has_workflow_section(self, nodejs_content):
        """Node.js guide should have development workflow section."""
        assert "Development Workflow" in nodejs_content or "workflow" in nodejs_content.lower()


class TestAsyncPatterns:
    """Test async/concurrent programming pattern coverage."""

    @pytest.fixture
    def python_content(self):
        """Get Python guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "PYTHON.md"
        return path.read_text()

    @pytest.fixture
    def go_content(self):
        """Get Go guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "GO.md"
        return path.read_text()

    @pytest.fixture
    def nodejs_content(self):
        """Get Node.js guide content."""
        path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "NODEJS.md"
        return path.read_text()

    def test_python_covers_async_await(self, python_content):
        """Python guide should cover async/await patterns."""
        assert "async" in python_content.lower() or "asyncio" in python_content.lower()

    def test_nodejs_covers_async_await(self, nodejs_content):
        """Node.js guide should cover async/await patterns."""
        assert "async" in nodejs_content.lower() or "promise" in nodejs_content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
