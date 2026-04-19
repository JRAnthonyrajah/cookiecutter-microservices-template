"""Tests for Makefile template validation and functionality."""
import re
import subprocess
from pathlib import Path
from typing import List


class TestMakefilePresence:
    """Tests for Makefile existence and basic structure."""

    def test_makefile_exists(self):
        """Makefile exists in service directory."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        assert makefile.exists(), "Makefile not found in service directory"

    def test_makefile_not_empty(self):
        """Makefile is not empty."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert len(content) > 500, "Makefile is too small"

    def test_makefile_is_readable(self):
        """Makefile content is valid."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert content.count(":") > 0, "No target definitions found"


class TestPhonyDeclarations:
    """Tests for .PHONY declarations."""

    def test_phony_declaration_exists(self):
        """.PHONY declaration is present."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert ".PHONY:" in content, ".PHONY declaration not found"

    def test_phony_contains_help(self):
        """help target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "help" in phony_line.group(0), "help not in .PHONY"

    def test_phony_contains_build(self):
        """build target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "build" in phony_line.group(0), "build not in .PHONY"

    def test_phony_contains_test(self):
        """test target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "test" in phony_line.group(0), "test not in .PHONY"

    def test_phony_contains_lint(self):
        """lint target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "lint" in phony_line.group(0), "lint not in .PHONY"

    def test_phony_contains_format(self):
        """format target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "format" in phony_line.group(0), "format not in .PHONY"

    def test_phony_contains_up(self):
        """up target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "up" in phony_line.group(0), "up not in .PHONY"

    def test_phony_contains_down(self):
        """down target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "down" in phony_line.group(0), "down not in .PHONY"

    def test_phony_contains_clean(self):
        """clean target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "clean" in phony_line.group(0), "clean not in .PHONY"

    def test_phony_contains_helm_lint(self):
        """helm-lint target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "helm-lint" in phony_line.group(0), "helm-lint not in .PHONY"

    def test_phony_contains_helm_template(self):
        """helm-template target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "helm-template" in phony_line.group(0), "helm-template not in .PHONY"

    def test_phony_contains_logs(self):
        """logs target is declared as .PHONY."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        phony_line = re.search(r"\.PHONY:.*", content)
        assert phony_line, ".PHONY line not found"
        assert "logs" in phony_line.group(0), "logs not in .PHONY"


class TestTargetDefinitions:
    """Tests for target definitions and implementation."""

    def test_build_target_exists(self):
        """build target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^build:", content, re.MULTILINE), "build target not defined"

    def test_build_target_has_docker_build(self):
        """build target contains docker build command."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        build_section = re.search(
            r"^build:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert build_section, "build section not found"
        assert "docker build" in build_section.group(0), "docker build not found in build target"

    def test_test_target_exists(self):
        """test target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^test:", content, re.MULTILINE), "test target not defined"

    def test_test_target_has_language_awareness(self):
        """test target includes language-specific test commands."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should have pytest, go test, npm test, or mvn test defined
        assert any(cmd in content for cmd in ["pytest", "go test", "npm test", "mvn test"]), \
            "No language-aware test command found"

    def test_lint_target_exists(self):
        """lint target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^lint:", content, re.MULTILINE), "lint target not defined"

    def test_lint_target_has_language_awareness(self):
        """lint target includes language-specific linters."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should have ruff, golangci-lint, eslint, or mvn checkstyle
        assert any(cmd in content for cmd in ["ruff", "golangci-lint", "eslint", "checkstyle"]), \
            "No language-aware linter found"

    def test_format_target_exists(self):
        """format target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^format:", content, re.MULTILINE), "format target not defined"

    def test_format_target_has_language_awareness(self):
        """format target includes language-specific formatters."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should have black, gofmt, prettier, or spotless
        assert any(cmd in content for cmd in ["black", "gofmt", "prettier", "spotless"]), \
            "No language-aware formatter found"

    def test_up_target_exists(self):
        """up target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^up:", content, re.MULTILINE), "up target not defined"

    def test_up_target_has_docker_compose(self):
        """up target contains docker-compose command."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        up_section = re.search(
            r"^up:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert up_section, "up section not found"
        assert "docker-compose up" in up_section.group(0), "docker-compose up not found"

    def test_down_target_exists(self):
        """down target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^down:", content, re.MULTILINE), "down target not defined"

    def test_down_target_has_docker_compose(self):
        """down target contains docker-compose command."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        down_section = re.search(
            r"^down:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert down_section, "down section not found"
        assert "docker-compose down" in down_section.group(0), "docker-compose down not found"

    def test_clean_target_exists(self):
        """clean target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^clean:", content, re.MULTILINE), "clean target not defined"

    def test_clean_target_has_cleanup_commands(self):
        """clean target includes cleanup commands."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        clean_section = re.search(
            r"^clean:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert clean_section, "clean section not found"
        clean_text = clean_section.group(0)
        # Should have language-specific cleanup
        assert any(cmd in clean_text for cmd in ["__pycache__", "node_modules", "*.pyc", "clean"]), \
            "No cleanup commands found"

    def test_helm_lint_target_exists(self):
        """helm-lint target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^helm-lint:", content, re.MULTILINE), "helm-lint target not defined"

    def test_helm_lint_target_has_helm_command(self):
        """helm-lint target contains helm lint command."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        helm_section = re.search(
            r"^helm-lint:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert helm_section, "helm-lint section not found"
        assert "helm lint" in helm_section.group(0), "helm lint command not found"

    def test_helm_template_target_exists(self):
        """helm-template target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^helm-template:", content, re.MULTILINE), "helm-template target not defined"

    def test_helm_template_target_has_helm_command(self):
        """helm-template target contains helm template command."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        helm_section = re.search(
            r"^helm-template:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert helm_section, "helm-template section not found"
        assert "helm template" in helm_section.group(0), "helm template command not found"

    def test_logs_target_exists(self):
        """logs target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^logs:", content, re.MULTILINE), "logs target not defined"

    def test_logs_target_has_docker_compose(self):
        """logs target contains docker-compose logs command."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        logs_section = re.search(
            r"^logs:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert logs_section, "logs section not found"
        assert "docker-compose logs" in logs_section.group(0), "docker-compose logs not found"

    def test_help_target_exists(self):
        """help target is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^help:", content, re.MULTILINE), "help target not defined"


class TestHelpTarget:
    """Tests for help target output formatting."""

    def test_help_target_output_format(self):
        """help target has proper formatting."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        help_section = re.search(
            r"^help:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert help_section, "help section not found"
        help_text = help_section.group(0)
        # Should have echo statements for nice formatting
        assert "echo" in help_text, "Help target lacks output"

    def test_help_target_displays_service_name(self):
        """help target displays service name."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        help_section = re.search(
            r"^help:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert help_section, "help section not found"
        # Service name should be in help output
        assert "SERVICE_NAME" in help_section.group(0) or "$(SERVICE_NAME)" in help_section.group(0), \
            "Service name not displayed in help"

    def test_help_target_lists_targets(self):
        """help target lists available targets."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        help_section = re.search(
            r"^help:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert help_section, "help section not found"
        help_text = help_section.group(0)
        # Should have awk or similar for parsing targets
        assert "awk" in help_text or "grep" in help_text or "##" in help_text, \
            "Help target doesn't parse target descriptions"


class TestVariables:
    """Tests for Makefile variables and configuration."""

    def test_has_service_name_variable(self):
        """SERVICE_NAME variable is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "SERVICE_NAME" in content, "SERVICE_NAME variable not defined"

    def test_has_docker_image_variable(self):
        """DOCKER_IMAGE variable is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "DOCKER_IMAGE" in content, "DOCKER_IMAGE variable not defined"

    def test_has_docker_tag_variable(self):
        """DOCKER_TAG variable is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "DOCKER_TAG" in content, "DOCKER_TAG variable not defined"

    def test_has_language_variable(self):
        """LANGUAGE variable is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "LANGUAGE" in content, "LANGUAGE variable not defined"

    def test_has_helm_chart_dir_variable(self):
        """HELM_CHART_DIR variable is defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "HELM_CHART_DIR" in content, "HELM_CHART_DIR variable not defined"

    def test_docker_image_uses_registry(self):
        """DOCKER_IMAGE uses DOCKER_REGISTRY variable."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "DOCKER_REGISTRY" in content, "DOCKER_REGISTRY variable not defined"
        assert "$(DOCKER_REGISTRY)" in content, "DOCKER_REGISTRY not used in DOCKER_IMAGE"


class TestLanguageSpecificCommands:
    """Tests for language-specific command configuration."""

    def test_python_commands_defined(self):
        """Python language commands are defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "python" in content.lower(), "Python language support not found"
        assert "ruff" in content or "black" in content, "Python tooling not configured"

    def test_go_commands_defined(self):
        """Go language commands are defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "go" in content.lower(), "Go language support not found"
        assert "golangci-lint" in content or "gofmt" in content, "Go tooling not configured"

    def test_nodejs_commands_defined(self):
        """Node.js language commands are defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "nodejs" in content.lower() or "node" in content.lower(), "Node.js language support not found"
        assert "eslint" in content or "prettier" in content, "Node.js tooling not configured"

    def test_java_commands_defined(self):
        """Java language commands are defined."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "java" in content.lower(), "Java language support not found"
        assert "mvn" in content, "Maven tooling not configured"

    def test_language_specific_test_commands(self):
        """Language-specific test commands are configured."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Each language should have a test command
        assert "pytest" in content or "go test" in content or "npm test" in content or "mvn test" in content, \
            "No language-specific test commands found"

    def test_language_specific_linters(self):
        """Language-specific linters are configured."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should have at least one linter
        assert any(lint in content for lint in ["ruff", "golangci-lint", "eslint", "checkstyle"]), \
            "No language-specific linters found"

    def test_language_specific_formatters(self):
        """Language-specific formatters are configured."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should have at least one formatter
        assert any(fmt in content for fmt in ["black", "gofmt", "prettier", "spotless"]), \
            "No language-specific formatters found"


class TestDockerIntegration:
    """Tests for Docker and Docker Compose integration."""

    def test_docker_build_uses_dockerfile(self):
        """docker build uses Dockerfile."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert "-f Dockerfile" in content or "Dockerfile" in content, "Dockerfile not referenced"

    def test_docker_build_tags_image(self):
        """docker build tags the image with DOCKER_IMAGE:DOCKER_TAG."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        build_section = re.search(
            r"^build:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert build_section, "build section not found"
        assert "-t" in build_section.group(0), "Docker image tagging not found"

    def test_docker_compose_up_detached(self):
        """docker-compose up uses -d flag for detached mode."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        up_section = re.search(
            r"^up:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert up_section, "up section not found"
        assert "-d" in up_section.group(0), "Detached mode not used in docker-compose up"

    def test_docker_compose_down_exists(self):
        """docker-compose down command is properly configured."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        down_section = re.search(
            r"^down:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert down_section, "down section not found"
        assert "docker-compose down" in down_section.group(0), "docker-compose down not configured"

    def test_logs_command_follows_container(self):
        """logs command uses -f flag to follow output."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        logs_section = re.search(
            r"^logs:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert logs_section, "logs section not found"
        assert "-f" in logs_section.group(0), "Follow flag not used in logs command"


class TestHelmIntegration:
    """Tests for Helm chart integration."""

    def test_helm_lint_checks_directory(self):
        """helm-lint checks HELM_CHART_DIR exists."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        helm_section = re.search(
            r"^helm-lint:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert helm_section, "helm-lint section not found"
        helm_text = helm_section.group(0)
        # Should check if directory exists
        assert "if" in helm_text and "HELM_CHART_DIR" in helm_text, \
            "Helm chart directory check not found"

    def test_helm_template_uses_service_name(self):
        """helm-template uses SERVICE_NAME."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        helm_section = re.search(
            r"^helm-template:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert helm_section, "helm-template section not found"
        assert "SERVICE_NAME" in helm_section.group(0), "SERVICE_NAME not used in helm template"

    def test_helm_template_outputs_to_stdout(self):
        """helm-template outputs rendered template."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        helm_section = re.search(
            r"^helm-template:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert helm_section, "helm-template section not found"
        assert "helm template" in helm_section.group(0), "helm template command not found"


class TestArtifactCleanup:
    """Tests for artifact cleanup validation."""

    def test_clean_removes_python_cache(self):
        """clean target removes Python cache."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should have Python cache cleanup
        assert "__pycache__" in content or ".pyc" in content or ".pytest_cache" in content, \
            "Python cache cleanup not found"

    def test_clean_removes_go_artifacts(self):
        """clean target removes Go build artifacts."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should have Go cleanup
        assert "go clean" in content or ".test" in content, \
            "Go artifact cleanup not found"

    def test_clean_removes_node_modules(self):
        """clean target removes node_modules."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should have Node.js cleanup
        assert "node_modules" in content, "node_modules cleanup not found"

    def test_clean_removes_ds_store(self):
        """clean target removes .DS_Store files."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Should remove .DS_Store
        assert ".DS_Store" in content, ".DS_Store cleanup not found"


class TestErrorHandling:
    """Tests for error handling and robustness."""

    def test_helm_lint_handles_missing_directory(self):
        """helm-lint handles missing chart directory gracefully."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        helm_section = re.search(
            r"^helm-lint:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert helm_section, "helm-lint section not found"
        helm_text = helm_section.group(0)
        # Should check if directory exists before running helm
        assert "if [ ! -d" in helm_text, "Directory existence check not found"

    def test_helm_template_handles_missing_directory(self):
        """helm-template handles missing chart directory gracefully."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        helm_section = re.search(
            r"^helm-template:.*?(?=^[a-zA-Z]|\Z)",
            content,
            re.MULTILINE | re.DOTALL
        )
        assert helm_section, "helm-template section not found"
        helm_text = helm_section.group(0)
        # Should check if directory exists before running helm
        assert "if [ ! -d" in helm_text, "Directory existence check not found"

    def test_default_goal_set(self):
        """DEFAULT_GOAL is set."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert ".DEFAULT_GOAL" in content, "DEFAULT_GOAL not set"
        assert "help" in content, "help should be the default goal"


class TestDocumentation:
    """Tests for Makefile documentation and comments."""

    def test_targets_have_help_comments(self):
        """Targets have help comments."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        # Count lines with ## (help comments)
        help_comments = len(re.findall(r"##", content))
        assert help_comments > 5, "Insufficient help comments for targets"

    def test_build_target_documented(self):
        """build target has documentation."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^build:.*##", content, re.MULTILINE), "build target not documented"

    def test_test_target_documented(self):
        """test target has documentation."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^test:.*##", content, re.MULTILINE), "test target not documented"

    def test_format_target_documented(self):
        """format target has documentation."""
        makefile = Path("{{ cookiecutter.service_slug }}/Makefile")
        content = makefile.read_text()
        assert re.search(r"^format:.*##", content, re.MULTILINE), "format target not documented"
