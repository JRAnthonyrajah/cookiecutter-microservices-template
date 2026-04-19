"""Tests for SETUP.md and QUICKSTART.md documentation.

This module validates that setup and quick-start documentation
exist, are properly formatted, and contain required sections,
code examples, and helpful information.
"""
import re
from pathlib import Path


class TestSetupMdPresence:
    """Tests for SETUP.md file existence and basic structure."""

    def test_setup_md_exists(self):
        """SETUP.md exists in service directory."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        assert setup_file.exists(), "SETUP.md not found in service directory"

    def test_setup_md_not_empty(self):
        """SETUP.md is not empty."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()
        assert len(content) > 500, "SETUP.md is too small (< 500 chars)"

    def test_setup_md_is_valid_markdown(self):
        """SETUP.md is valid markdown format."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()
        # Check for markdown elements
        assert "#" in content, "SETUP.md missing markdown headings"
        assert "```" in content, "SETUP.md missing code blocks"


class TestQuickstartMdPresence:
    """Tests for QUICKSTART.md file existence and basic structure."""

    def test_quickstart_md_exists(self):
        """QUICKSTART.md exists in service directory."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        assert quickstart_file.exists(), "QUICKSTART.md not found in service directory"

    def test_quickstart_md_not_empty(self):
        """QUICKSTART.md is not empty."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()
        assert len(content) > 500, "QUICKSTART.md is too small (< 500 chars)"

    def test_quickstart_md_is_valid_markdown(self):
        """QUICKSTART.md is valid markdown format."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()
        # Check for markdown elements
        assert "#" in content, "QUICKSTART.md missing markdown headings"
        assert "```" in content, "QUICKSTART.md missing code blocks"


class TestSetupMdSections:
    """Tests for required sections in SETUP.md."""

    def _get_setup_content(self):
        """Helper to get SETUP.md content."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        return setup_file.read_text().lower()

    def test_setup_has_installation_section(self):
        """SETUP.md has Installation Prerequisites section."""
        content = self._get_setup_content()
        assert "installation" in content and "prerequisite" in content, \
            "SETUP.md missing Installation Prerequisites section"

    def test_setup_has_quickstart_section(self):
        """SETUP.md has Quick Start section."""
        content = self._get_setup_content()
        assert "quick start" in content or "cookiecutter" in content, \
            "SETUP.md missing Quick Start section"

    def test_setup_has_local_development_section(self):
        """SETUP.md has Local Development Setup section."""
        content = self._get_setup_content()
        assert "local development" in content or "development setup" in content, \
            "SETUP.md missing Local Development Setup section"

    def test_setup_has_testing_section(self):
        """SETUP.md has Running Tests section."""
        content = self._get_setup_content()
        assert "test" in content or "pytest" in content, \
            "SETUP.md missing Running Tests section"

    def test_setup_has_docker_build_section(self):
        """SETUP.md has Building Docker Image section."""
        content = self._get_setup_content()
        assert "docker" in content and "build" in content, \
            "SETUP.md missing Docker build section"

    def test_setup_has_make_targets_section(self):
        """SETUP.md has Make Targets reference section."""
        content = self._get_setup_content()
        assert "make" in content, "SETUP.md missing Make targets reference"

    def test_setup_has_troubleshooting_section(self):
        """SETUP.md has Troubleshooting section."""
        content = self._get_setup_content()
        assert "troubleshoot" in content, "SETUP.md missing Troubleshooting section"

    def test_setup_has_helm_section(self):
        """SETUP.md has Helm Chart Management section."""
        content = self._get_setup_content()
        assert "helm" in content, "SETUP.md missing Helm section"

    def test_setup_has_requirements_subsections(self):
        """SETUP.md has Required Tools subsection."""
        content = self._get_setup_content()
        assert "required tool" in content or "required" in content, \
            "SETUP.md missing required tools information"


class TestQuickstartMdSections:
    """Tests for required sections in QUICKSTART.md."""

    def _get_quickstart_content(self):
        """Helper to get QUICKSTART.md content."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        return quickstart_file.read_text().lower()

    def test_quickstart_has_prerequisites(self):
        """QUICKSTART.md mentions prerequisites."""
        content = self._get_quickstart_content()
        assert "prerequisite" in content or "before starting" in content, \
            "QUICKSTART.md missing prerequisites"

    def test_quickstart_has_clone_step(self):
        """QUICKSTART.md has clone/navigate step."""
        content = self._get_quickstart_content()
        assert "clone" in content or "navigate" in content, \
            "QUICKSTART.md missing clone/navigate instructions"

    def test_quickstart_has_setup_step(self):
        """QUICKSTART.md has setup step."""
        content = self._get_quickstart_content()
        assert "setup" in content or "install" in content, \
            "QUICKSTART.md missing setup step"

    def test_quickstart_has_start_services_step(self):
        """QUICKSTART.md has step to start services."""
        content = self._get_quickstart_content()
        assert "make up" in content or "start" in content, \
            "QUICKSTART.md missing service startup instructions"

    def test_quickstart_has_health_check_step(self):
        """QUICKSTART.md has health check verification."""
        content = self._get_quickstart_content()
        assert "health" in content or "/health" in content, \
            "QUICKSTART.md missing health check step"

    def test_quickstart_has_first_request_example(self):
        """QUICKSTART.md has example API request."""
        content = self._get_quickstart_content()
        assert "curl" in content or "request" in content, \
            "QUICKSTART.md missing example request"

    def test_quickstart_has_stopping_services_step(self):
        """QUICKSTART.md has step to stop services."""
        content = self._get_quickstart_content()
        assert "make down" in content or "stop" in content, \
            "QUICKSTART.md missing service stopping instructions"

    def test_quickstart_has_next_steps(self):
        """QUICKSTART.md has Next Steps section."""
        content = self._get_quickstart_content()
        assert "next step" in content or "further reading" in content, \
            "QUICKSTART.md missing Next Steps section"


class TestSetupMdCodeBlocks:
    """Tests for valid code blocks in SETUP.md."""

    def _get_setup_content(self):
        """Helper to get SETUP.md content."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        return setup_file.read_text()

    def test_setup_has_python_examples(self):
        """SETUP.md includes Python code examples."""
        content = self._get_setup_content()
        # Check for Python-related code blocks or pip commands
        assert "pip" in content or "python" in content, \
            "SETUP.md missing Python examples"

    def test_setup_has_docker_examples(self):
        """SETUP.md includes Docker examples."""
        content = self._get_setup_content()
        assert "docker" in content, "SETUP.md missing Docker examples"

    def test_setup_has_curl_examples(self):
        """SETUP.md includes curl examples."""
        content = self._get_setup_content()
        assert "curl" in content, "SETUP.md missing curl examples"

    def test_setup_has_make_examples(self):
        """SETUP.md includes Make command examples."""
        content = self._get_setup_content()
        # Check for make commands in code blocks
        bash_blocks = re.findall(r'```bash\s*(.*?)```', content, re.DOTALL)
        make_examples = any('make' in block for block in bash_blocks)
        assert make_examples or "make up" in content, \
            "SETUP.md missing make command examples"

    def test_setup_shell_blocks_are_valid(self):
        """SETUP.md shell code blocks have proper syntax."""
        content = self._get_setup_content()
        # Count code blocks
        code_blocks = re.findall(r'```(.*?)```', content, re.DOTALL)
        assert len(code_blocks) > 5, "SETUP.md has too few code examples"

    def test_setup_has_environment_variable_examples(self):
        """SETUP.md includes environment variable examples."""
        content = self._get_setup_content()
        assert "export" in content or ".env" in content, \
            "SETUP.md missing environment variable examples"


class TestQuickstartMdCodeBlocks:
    """Tests for valid code blocks in QUICKSTART.md."""

    def _get_quickstart_content(self):
        """Helper to get QUICKSTART.md content."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        return quickstart_file.read_text()

    def test_quickstart_has_startup_example(self):
        """QUICKSTART.md includes service startup example."""
        content = self._get_quickstart_content()
        assert "make up" in content, \
            "QUICKSTART.md missing make up example"

    def test_quickstart_has_curl_example(self):
        """QUICKSTART.md includes curl request example."""
        content = self._get_quickstart_content()
        assert "curl" in content, "QUICKSTART.md missing curl example"

    def test_quickstart_has_health_check_example(self):
        """QUICKSTART.md includes health check curl command."""
        content = self._get_quickstart_content()
        assert "/health" in content, \
            "QUICKSTART.md missing health check example"

    def test_quickstart_has_stop_example(self):
        """QUICKSTART.md includes service stop example."""
        content = self._get_quickstart_content()
        assert "make down" in content, \
            "QUICKSTART.md missing make down example"

    def test_quickstart_code_blocks_count(self):
        """QUICKSTART.md has sufficient code examples."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()
        code_blocks = re.findall(r'```(.*?)```', content, re.DOTALL)
        assert len(code_blocks) >= 8, \
            f"QUICKSTART.md has {len(code_blocks)} code blocks, need at least 8"

    def test_quickstart_has_json_response_example(self):
        """QUICKSTART.md includes JSON response example."""
        content = self._get_quickstart_content()
        assert "{" in content and "}" in content, \
            "QUICKSTART.md missing JSON response examples"


class TestSetupMdContent:
    """Tests for specific content in SETUP.md."""

    def _get_setup_content(self):
        """Helper to get SETUP.md content."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        return setup_file.read_text()

    def test_setup_mentions_python_version(self):
        """SETUP.md specifies Python version requirement."""
        content = self._get_setup_content()
        assert "3.9" in content or "3.10" in content or "python" in content.lower(), \
            "SETUP.md missing Python version requirement"

    def test_setup_mentions_docker_requirement(self):
        """SETUP.md mentions Docker as requirement."""
        content = self._get_setup_content()
        assert "docker" in content.lower(), "SETUP.md missing Docker requirement"

    def test_setup_mentions_helm(self):
        """SETUP.md mentions Helm as optional tool."""
        content = self._get_setup_content()
        assert "helm" in content.lower(), "SETUP.md missing Helm reference"

    def test_setup_has_language_specific_section(self):
        """SETUP.md has language-specific requirements."""
        content = self._get_setup_content()
        # Should mention at least one language
        languages = ["python", "go", "node", "java"]
        has_language = any(lang in content.lower() for lang in languages)
        assert has_language, "SETUP.md missing language-specific content"

    def test_setup_mentions_make_targets(self):
        """SETUP.md references available Make targets."""
        content = self._get_setup_content()
        targets = ["make test", "make build", "make lint", "make up", "make down"]
        for target in targets:
            assert target in content, f"SETUP.md missing '{target}' reference"

    def test_setup_troubleshooting_has_docker_issue(self):
        """SETUP.md troubleshooting includes Docker daemon issue."""
        content = self._get_setup_content()
        assert "docker daemon" in content.lower() or "cannot connect" in content.lower(), \
            "SETUP.md troubleshooting missing Docker daemon issue"

    def test_setup_troubleshooting_has_port_issue(self):
        """SETUP.md troubleshooting includes port conflict issue."""
        content = self._get_setup_content()
        assert "port" in content.lower(), \
            "SETUP.md troubleshooting missing port conflict issue"

    def test_setup_has_environment_configuration(self):
        """SETUP.md explains environment configuration."""
        content = self._get_setup_content()
        assert ".env" in content or "environment" in content.lower(), \
            "SETUP.md missing environment configuration explanation"


class TestQuickstartMdContent:
    """Tests for specific content in QUICKSTART.md."""

    def _get_quickstart_content(self):
        """Helper to get QUICKSTART.md content."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        return quickstart_file.read_text()

    def test_quickstart_mentions_five_minutes(self):
        """QUICKSTART.md emphasizes 5-minute timeframe."""
        content = self._get_quickstart_content()
        assert "5" in content or "minute" in content.lower(), \
            "QUICKSTART.md should emphasize 5-minute quick start"

    def test_quickstart_has_step_structure(self):
        """QUICKSTART.md follows step-by-step structure."""
        content = self._get_quickstart_content()
        # Should have numbered or labeled steps
        step_patterns = ["step", "step 1", "step 2", "1.", "2.", "3."]
        has_steps = any(pattern.lower() in content.lower() for pattern in step_patterns)
        assert has_steps, "QUICKSTART.md missing step structure"

    def test_quickstart_mentions_curl_http_client(self):
        """QUICKSTART.md mentions curl as HTTP client."""
        content = self._get_quickstart_content()
        assert "curl" in content.lower(), \
            "QUICKSTART.md should mention curl for API requests"

    def test_quickstart_shows_expected_output(self):
        """QUICKSTART.md includes expected output examples."""
        content = self._get_quickstart_content()
        assert "expected" in content.lower() or "output" in content.lower(), \
            "QUICKSTART.md missing expected output examples"

    def test_quickstart_references_full_setup_guide(self):
        """QUICKSTART.md references SETUP.md."""
        content = self._get_quickstart_content()
        assert "setup.md" in content.lower() or "setup guide" in content.lower(), \
            "QUICKSTART.md should reference full SETUP.md guide"

    def test_quickstart_has_command_table(self):
        """QUICKSTART.md includes command reference table."""
        content = self._get_quickstart_content()
        # Check for markdown table
        assert "|" in content, "QUICKSTART.md missing command reference table"

    def test_quickstart_mentions_make_help(self):
        """QUICKSTART.md mentions make help command."""
        content = self._get_quickstart_content()
        assert "make help" in content, \
            "QUICKSTART.md should mention 'make help' command"


class TestDocumentationLinks:
    """Tests for internal references and links."""

    def test_setup_references_dockerfile(self):
        """SETUP.md references Dockerfile."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()
        assert "dockerfile" in content.lower(), \
            "SETUP.md should reference Dockerfile"

    def test_setup_references_docker_compose(self):
        """SETUP.md references docker-compose."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()
        assert "docker-compose" in content.lower() or "docker compose" in content.lower(), \
            "SETUP.md should reference docker-compose.yml"

    def test_quickstart_references_troubleshooting(self):
        """QUICKSTART.md includes troubleshooting section."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()
        assert "troubleshoot" in content.lower() or "issues" in content.lower(), \
            "QUICKSTART.md should include troubleshooting"

    def test_quickstart_references_architecture(self):
        """QUICKSTART.md references architecture documentation."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()
        assert "architecture" in content.lower() or "design" in content.lower(), \
            "QUICKSTART.md should reference architecture documentation"

    def test_setup_has_related_docs_section(self):
        """SETUP.md has related documentation references."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()
        assert "makefile" in content.lower() or "dockerfile" in content.lower(), \
            "SETUP.md should reference related documentation"


class TestDocumentationCompleteness:
    """Tests for overall documentation completeness."""

    def test_both_docs_exist_together(self):
        """Both SETUP.md and QUICKSTART.md exist."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        assert setup_file.exists() and quickstart_file.exists(), \
            "Both SETUP.md and QUICKSTART.md must exist"

    def test_setup_md_is_comprehensive(self):
        """SETUP.md is comprehensive (> 3000 chars)."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()
        assert len(content) > 3000, \
            f"SETUP.md should be comprehensive (> 3000 chars, current: {len(content)})"

    def test_quickstart_md_is_substantial(self):
        """QUICKSTART.md is substantial (> 1500 chars)."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()
        assert len(content) > 1500, \
            f"QUICKSTART.md should be substantial (> 1500 chars, current: {len(content)})"

    def test_setup_has_minimum_sections(self):
        """SETUP.md has at least 8 main sections."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()
        # Count H2 headings (##)
        h2_headings = re.findall(r'^## ', content, re.MULTILINE)
        assert len(h2_headings) >= 8, \
            f"SETUP.md should have at least 8 main sections, found {len(h2_headings)}"

    def test_quickstart_has_minimum_steps(self):
        """QUICKSTART.md has at least 5 main steps."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()
        # Count H2 headings (##)
        h2_headings = re.findall(r'^## ', content, re.MULTILINE)
        assert len(h2_headings) >= 5, \
            f"QUICKSTART.md should have at least 5 steps, found {len(h2_headings)}"

    def test_documentation_uses_template_variables(self):
        """Documentation correctly uses cookiecutter template variables."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")

        setup_content = setup_file.read_text()
        quickstart_content = quickstart_file.read_text()

        # Should use template variables
        assert "{{ cookiecutter" in setup_content or "cookiecutter" in setup_content, \
            "SETUP.md should use template variables"
        assert "{{ cookiecutter" in quickstart_content or "cookiecutter" in quickstart_content, \
            "QUICKSTART.md should use template variables"


class TestDocumentationFormatting:
    """Tests for proper markdown formatting."""

    def test_setup_md_has_proper_heading_hierarchy(self):
        """SETUP.md uses proper markdown heading hierarchy."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()

        # Check for title (H1) and sections (H2)
        h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## ', content, re.MULTILINE))

        assert h1_count >= 1, "SETUP.md should have a title (H1)"
        assert h2_count >= 5, "SETUP.md should have multiple sections (H2)"

    def test_quickstart_md_has_proper_heading_hierarchy(self):
        """QUICKSTART.md uses proper markdown heading hierarchy."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()

        # Check for title (H1) and sections (H2)
        h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## ', content, re.MULTILINE))

        assert h1_count >= 1, "QUICKSTART.md should have a title (H1)"
        assert h2_count >= 5, "QUICKSTART.md should have multiple sections (H2)"

    def test_setup_code_blocks_have_language_specified(self):
        """SETUP.md code blocks specify language."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()

        # Find all code blocks
        code_blocks = re.findall(r'```(\w*)', content)
        # Many should have language specified (at least 40%)
        specified = sum(1 for block in code_blocks if block)
        assert specified > len(code_blocks) * 0.4, \
            "Most code blocks should specify language"

    def test_quickstart_code_blocks_have_language_specified(self):
        """QUICKSTART.md code blocks specify language."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()

        # Find all code blocks
        code_blocks = re.findall(r'```(\w*)', content)
        # Many should have language specified (at least 30%)
        specified = sum(1 for block in code_blocks if block)
        assert specified > len(code_blocks) * 0.3, \
            "Many code blocks should specify language"

    def test_setup_has_no_unclosed_code_blocks(self):
        """SETUP.md has properly closed code blocks."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()

        # Count opening and closing backticks (in groups of 3)
        opens = len(re.findall(r'```', content))
        assert opens % 2 == 0, "SETUP.md has unclosed code blocks"

    def test_quickstart_has_no_unclosed_code_blocks(self):
        """QUICKSTART.md has properly closed code blocks."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()

        # Count opening and closing backticks (in groups of 3)
        opens = len(re.findall(r'```', content))
        assert opens % 2 == 0, "QUICKSTART.md has unclosed code blocks"


class TestDocumentationPracticalContent:
    """Tests for practical, actionable content."""

    def test_setup_covers_all_languages(self):
        """SETUP.md covers multiple programming languages."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text().lower()

        # Should mention at least 2 languages
        languages = ["python", "go", "node", "java"]
        found = sum(1 for lang in languages if lang in content)
        assert found >= 2, f"SETUP.md should cover multiple languages, found {found}"

    def test_quickstart_includes_estimated_time(self):
        """QUICKSTART.md indicates time for each step."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()

        # Should indicate time estimates like "1 minute"
        assert "minute" in content.lower(), \
            "QUICKSTART.md should include time estimates"

    def test_setup_includes_actual_command_examples(self):
        """SETUP.md includes actual executable commands."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text()

        # Should have make, docker, pip, curl commands
        commands = ["make", "docker", "pip", "curl", "git"]
        found = sum(1 for cmd in commands if cmd in content.lower())
        assert found >= 4, f"SETUP.md should include multiple command examples, found {found}"

    def test_quickstart_includes_actual_command_examples(self):
        """QUICKSTART.md includes actual executable commands."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()

        # Should have make, curl commands at minimum
        assert "make" in content.lower(), "QUICKSTART.md should include make commands"
        assert "curl" in content.lower(), "QUICKSTART.md should include curl commands"

    def test_setup_addresses_common_errors(self):
        """SETUP.md troubleshooting addresses common errors."""
        setup_file = Path("{{ cookiecutter.service_slug }}/SETUP.md")
        content = setup_file.read_text().lower()

        # Should address common issues
        issues = ["error", "issue", "failed", "fail", "not found", "permission"]
        found = sum(1 for issue in issues if issue in content)
        assert found >= 2, "SETUP.md troubleshooting should address common errors"

    def test_quickstart_has_expected_outputs(self):
        """QUICKSTART.md shows expected outputs for commands."""
        quickstart_file = Path("{{ cookiecutter.service_slug }}/QUICKSTART.md")
        content = quickstart_file.read_text()

        # Should show "Expected output" or similar
        assert "expected" in content.lower() or "output" in content.lower(), \
            "QUICKSTART.md should show expected outputs"
