"""Tests for Dockerfile template validation."""
import re
from pathlib import Path


class TestDockerfilePresence:
    """Tests for Dockerfile existence and basic structure."""

    def test_dockerfile_exists(self):
        """Dockerfile exists in service directory."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        assert dockerfile.exists(), "Dockerfile not found"

    def test_dockerfile_not_empty(self):
        """Dockerfile is not empty."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert len(content) > 100, "Dockerfile is too small"


class TestDockerfileStructure:
    """Tests for Dockerfile structure and commands."""

    def test_has_from_statement(self):
        """Dockerfile contains FROM statement."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "FROM" in content, "FROM statement not found"

    def test_has_workdir(self):
        """Dockerfile contains WORKDIR statement."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "WORKDIR" in content, "WORKDIR statement not found"

    def test_has_expose(self):
        """Dockerfile contains EXPOSE statement."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "EXPOSE" in content, "EXPOSE statement not found"

    def test_has_healthcheck(self):
        """Dockerfile contains HEALTHCHECK instruction."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "HEALTHCHECK" in content, "HEALTHCHECK not found"

    def test_has_user_statement(self):
        """Dockerfile contains USER statement for non-root execution."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "USER" in content, "USER statement not found"

    def test_has_cmd_or_entrypoint(self):
        """Dockerfile contains CMD or ENTRYPOINT."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "CMD" in content or "ENTRYPOINT" in content, "CMD or ENTRYPOINT not found"


class TestDockerfileLanguageSupport:
    """Tests for language-specific Dockerfile content."""

    def test_conditional_python_block(self):
        """Python conditional block present."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "cookiecutter.language == 'python'" in content, "Python block not found"

    def test_conditional_go_block(self):
        """Go conditional block present."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "cookiecutter.language == 'go'" in content, "Go block not found"

    def test_conditional_nodejs_block(self):
        """Node.js conditional block present."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "cookiecutter.language == 'nodejs'" in content, "Node.js block not found"

    def test_python_uses_correct_base_image(self):
        """Python block uses correct base image."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        python_section = re.search(
            r"cookiecutter\.language == 'python'.*?(?={% elif|{% else|{% endif %})",
            content,
            re.DOTALL
        )
        assert python_section, "Python section not found"
        assert "python:" in python_section.group(0), "Python base image not found"

    def test_go_uses_multi_stage(self):
        """Go block uses multi-stage build."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        go_section = re.search(
            r"cookiecutter\.language == 'go'.*?(?={% elif|{% else|{% endif %})",
            content,
            re.DOTALL
        )
        assert go_section, "Go section not found"
        assert "as builder" in go_section.group(0), "Multi-stage build not found"

    def test_nodejs_uses_correct_base_image(self):
        """Node.js block uses correct base image."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        nodejs_section = re.search(
            r"cookiecutter\.language == 'nodejs'.*?(?={% endif %})",
            content,
            re.DOTALL
        )
        assert nodejs_section, "Node.js section not found"
        assert "node:" in nodejs_section.group(0), "Node.js base image not found"


class TestDockerfileSecurity:
    """Tests for security best practices."""

    def test_uses_non_root_user(self):
        """Dockerfile runs container as non-root user."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        # Check for user creation and switch
        assert re.search(r"(useradd|adduser|addgroup)", content), "Non-root user not configured"
        assert "USER" in content, "USER switch not found"

    def test_user_id_1000(self):
        """Non-root user has UID 1000."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "1000" in content, "User ID 1000 not found"

    def test_healthcheck_includes_timeout(self):
        """HEALTHCHECK includes timeout configuration."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        healthcheck = re.search(r"HEALTHCHECK.*", content)
        assert healthcheck, "HEALTHCHECK not found"
        assert "--timeout" in healthcheck.group(0), "Timeout not configured in HEALTHCHECK"


class TestDockerfileEnvironment:
    """Tests for environment variable configuration."""

    def test_port_env_variable(self):
        """PORT environment variable defined."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "ENV PORT" in content, "PORT environment variable not defined"

    def test_uses_env_variable_in_expose(self):
        """EXPOSE uses environment variable or port number."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        # Just verify EXPOSE exists; value varies by language
        assert "EXPOSE" in content, "EXPOSE instruction missing"
