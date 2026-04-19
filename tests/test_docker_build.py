"""Tests for Docker image build validation across all languages."""
import re
from pathlib import Path


class TestDockerfilePython:
    """Test Python-specific Dockerfile configuration."""

    def test_dockerfile_has_python_conditional(self):
        """Dockerfile includes Python conditional block."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "cookiecutter.language == 'python'" in content

    def test_python_uses_official_base_image(self):
        """Python uses official Python base image."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        python_match = re.search(
            r"cookiecutter\.language == 'python'.*?FROM python:",
            content,
            re.DOTALL
        )
        assert python_match, "Python block doesn't use FROM python"

    def test_python_has_healthcheck(self):
        """Python Dockerfile includes HEALTHCHECK."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        python_section = re.search(
            r"cookiecutter\.language == 'python'.*?(?={% elif|{% else|{% endif %})",
            content,
            re.DOTALL
        )
        assert python_section and "HEALTHCHECK" in python_section.group(0)

    def test_python_has_non_root_user(self):
        """Python Dockerfile configures non-root user."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        python_section = re.search(
            r"cookiecutter\.language == 'python'.*?(?={% elif|{% else|{% endif %})",
            content,
            re.DOTALL
        )
        assert python_section and "useradd" in python_section.group(0)


class TestDockerfileGo:
    """Test Go-specific Dockerfile configuration."""

    def test_dockerfile_has_go_conditional(self):
        """Dockerfile includes Go conditional block."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "cookiecutter.language == 'go'" in content

    def test_go_uses_official_base_image(self):
        """Go uses official Go base image."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        go_match = re.search(
            r"cookiecutter\.language == 'go'.*?FROM golang:",
            content,
            re.DOTALL
        )
        assert go_match, "Go block doesn't use FROM golang"

    def test_go_uses_multistage_build(self):
        """Go Dockerfile uses multi-stage build."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        go_section = re.search(
            r"cookiecutter\.language == 'go'.*?(?={% elif|{% else|{% endif %})",
            content,
            re.DOTALL
        )
        assert go_section and "as builder" in go_section.group(0)

    def test_go_final_stage_minimal(self):
        """Go final stage uses minimal runtime (alpine or scratch)."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        go_section = re.search(
            r"cookiecutter\.language == 'go'.*?(?={% elif|{% else|{% endif %})",
            content,
            re.DOTALL
        )
        assert go_section and ("alpine" in go_section.group(0) or "scratch" in go_section.group(0))

    def test_go_has_healthcheck(self):
        """Go Dockerfile includes HEALTHCHECK."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        go_section = re.search(
            r"cookiecutter\.language == 'go'.*?(?={% elif|{% else|{% endif %})",
            content,
            re.DOTALL
        )
        assert go_section and "HEALTHCHECK" in go_section.group(0)


class TestDockerfileNodeJS:
    """Test Node.js-specific Dockerfile configuration."""

    def test_dockerfile_has_nodejs_conditional(self):
        """Dockerfile includes Node.js conditional block."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "cookiecutter.language == 'nodejs'" in content

    def test_nodejs_uses_official_base_image(self):
        """Node.js uses official Node.js base image."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        nodejs_match = re.search(
            r"cookiecutter\.language == 'nodejs'.*?FROM node:",
            content,
            re.DOTALL
        )
        assert nodejs_match, "Node.js block doesn't use FROM node"

    def test_nodejs_has_healthcheck(self):
        """Node.js Dockerfile includes HEALTHCHECK."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        nodejs_section = re.search(
            r"cookiecutter\.language == 'nodejs'.*?(?={% endif %})",
            content,
            re.DOTALL
        )
        assert nodejs_section and "HEALTHCHECK" in nodejs_section.group(0)

    def test_nodejs_has_non_root_user(self):
        """Node.js Dockerfile configures non-root user."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        nodejs_section = re.search(
            r"cookiecutter\.language == 'nodejs'.*?(?={% endif %})",
            content,
            re.DOTALL
        )
        assert nodejs_section and "adduser" in nodejs_section.group(0)


class TestDockerfileSecurityCommon:
    """Test common security hardening across all languages."""

    def test_all_use_uid_1000(self):
        """All languages use UID 1000 for non-root user."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "1000" in content, "UID 1000 not found"

    def test_all_have_expose(self):
        """All languages have EXPOSE instruction."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "EXPOSE" in content, "EXPOSE instruction not found"

    def test_all_have_cmd(self):
        """All languages have CMD instruction."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "CMD" in content, "CMD instruction not found"

    def test_all_set_port_env(self):
        """All languages set PORT environment variable."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "ENV PORT" in content, "PORT environment variable not set"


class TestDockerBuildValidation:
    """Test Docker build simulation and configuration."""

    def test_dockerfile_syntax_valid(self):
        """Dockerfile has valid syntax (basic checks)."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        # Check for balanced Jinja2 blocks
        assert content.count("{{") == content.count("}}"), "Unbalanced Jinja2 delimiters"
        assert content.count("{%") == content.count("%}"), "Unbalanced Jinja2 block tags"

    def test_all_languages_covered(self):
        """Dockerfile covers all three required languages."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        assert "python" in content.lower(), "Python language not covered"
        assert "go" in content.lower(), "Go language not covered"
        assert "node" in content.lower(), "Node.js language not covered"

    def test_healthcheck_timeout_configured(self):
        """All HEALTHCHECK instructions have timeout."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        healthchecks = re.findall(r"HEALTHCHECK.*", content)
        assert healthchecks, "No HEALTHCHECK found"
        for hc in healthchecks:
            assert "--timeout" in hc, "HEALTHCHECK missing timeout"

    def test_workdir_set_before_copy(self):
        """WORKDIR is set before COPY commands."""
        dockerfile = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        content = dockerfile.read_text()
        # Split by language blocks and check each
        blocks = re.split(r"{%\s*elif|{%\s*else|{%\s*endif", content)
        for block in blocks:
            if "COPY" in block:
                # Find indices
                workdir_idx = block.find("WORKDIR")
                copy_idx = block.find("COPY")
                if copy_idx != -1 and workdir_idx != -1:
                    assert workdir_idx < copy_idx, "COPY before WORKDIR"
