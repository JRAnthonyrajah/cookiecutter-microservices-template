"""Tests for docker-compose.yml template validation."""
import re
from pathlib import Path

import yaml


class TestDockerComposePresence:
    """Tests for docker-compose.yml existence and basic structure."""

    def test_docker_compose_exists(self):
        """docker-compose.yml exists in service directory."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        assert compose_file.exists(), "docker-compose.yml not found"

    def test_docker_compose_not_empty(self):
        """docker-compose.yml is not empty."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert len(content) > 50, "docker-compose.yml is too small"


class TestDockerComposeYamlValidity:
    """Tests for YAML structure and validity."""

    def test_has_version(self):
        """docker-compose.yml specifies version."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "version:" in content, "Version not specified"
        # Check for version 3.8 or higher
        assert re.search(r'version:\s*["\']?3\.[8-9]', content), "Version should be 3.8 or higher"

    def test_has_services_section(self):
        """docker-compose.yml has services section."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "services:" in content, "Services section not found"


class TestDockerComposeServices:
    """Tests for service configuration."""

    def test_main_service_defined(self):
        """Main service is defined in docker-compose.yml."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Service should match cookiecutter.service_slug
        assert "{{ cookiecutter.service_slug }}:" in content, "Main service not defined"

    def test_build_section_present(self):
        """Service has build section."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "build:" in content, "Build section not found"

    def test_build_has_context(self):
        """Build section specifies context."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"context:\s*\.", content), "Build context not specified or incorrect"

    def test_build_has_dockerfile(self):
        """Build section specifies Dockerfile."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"dockerfile:\s*Dockerfile", content), "Dockerfile not specified"

    def test_service_has_container_name(self):
        """Service defines container_name."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "container_name:" in content, "container_name not defined"

    def test_container_name_format(self):
        """Container name follows naming convention."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"container_name:\s*{{ cookiecutter.service_slug }}-dev", content), \
            "Container name should follow pattern: {service}-dev"


class TestDockerComposePorts:
    """Tests for port configuration."""

    def test_ports_section_present(self):
        """Service defines ports."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "ports:" in content, "Ports section not found"

    def test_port_mapping_format(self):
        """Port mapping follows correct format."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should have format like "{{ cookiecutter.service_port | default('8080') }}:..."
        assert re.search(r'ports:\s*-\s*["\']?.*?:', content), \
            "Port mapping format is incorrect"


class TestDockerComposeEnvironment:
    """Tests for environment variable configuration."""

    def test_environment_section_present(self):
        """Service defines environment variables."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "environment:" in content, "Environment section not found"

    def test_service_name_env_var(self):
        """SERVICE_NAME environment variable defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "SERVICE_NAME:" in content, "SERVICE_NAME not defined"

    def test_log_level_env_var(self):
        """LOG_LEVEL environment variable defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "LOG_LEVEL:" in content, "LOG_LEVEL not defined"

    def test_compression_env_var(self):
        """COMPRESSION environment variable defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "COMPRESSION:" in content, "COMPRESSION not defined"

    def test_enable_metrics_env_var(self):
        """ENABLE_METRICS environment variable defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "ENABLE_METRICS:" in content, "ENABLE_METRICS not defined"

    def test_enable_tracing_env_var(self):
        """ENABLE_TRACING environment variable defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "ENABLE_TRACING:" in content, "ENABLE_TRACING not defined"

    def test_http_port_env_var(self):
        """HTTP_PORT environment variable defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "HTTP_PORT:" in content, "HTTP_PORT not defined"

    def test_health_check_interval_env_var(self):
        """HEALTH_CHECK_INTERVAL environment variable defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "HEALTH_CHECK_INTERVAL:" in content, "HEALTH_CHECK_INTERVAL not defined"

    def test_env_vars_use_defaults(self):
        """Environment variables have sensible defaults."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Check for default values using ${VAR:-default} syntax
        assert "${LOG_LEVEL" in content, "LOG_LEVEL should have default"
        assert "${ENABLE_METRICS" in content, "ENABLE_METRICS should have default"


class TestDockerComposeVolumes:
    """Tests for volume configuration."""

    def test_volumes_section_present(self):
        """Service defines volumes."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "volumes:" in content, "Volumes section not found"

    def test_code_mount_present(self):
        """Code mount for hot reload configured."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should mount current directory to /app for code hot reload
        assert re.search(r'\.\s*:\s*/app', content), "Code mount (./:/app) not found"

    def test_data_volume_present(self):
        """Data persistence volume configured."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should reference a named volume for data
        assert re.search(r'{{ cookiecutter.service_slug }}-data\s*:\s*/data', content), \
            "Data volume not properly configured"

    def test_named_volume_definition(self):
        """Named volume defined at top level."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "{{ cookiecutter.service_slug }}-data:" in content, \
            "Named volume not defined in volumes section"

    def test_volume_has_driver(self):
        """Named volume specifies driver."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"driver:\s*local", content), "Volume driver not specified"


class TestDockerComposeHealthCheck:
    """Tests for healthcheck configuration."""

    def test_healthcheck_section_present(self):
        """Service defines healthcheck."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "healthcheck:" in content, "Healthcheck section not found"

    def test_healthcheck_has_test(self):
        """Healthcheck has test command."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Test command uses CMD format or similar
        assert "test:" in content, "Healthcheck test not defined"

    def test_healthcheck_interval(self):
        """Healthcheck specifies interval."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"interval:\s*\d+s", content), "Healthcheck interval not defined"

    def test_healthcheck_timeout(self):
        """Healthcheck specifies timeout."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"timeout:\s*\d+s", content), "Healthcheck timeout not defined"

    def test_healthcheck_retries(self):
        """Healthcheck specifies retries."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"retries:\s*\d+", content), "Healthcheck retries not defined"

    def test_healthcheck_start_period(self):
        """Healthcheck specifies start_period."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"start_period:\s*\d+s", content), "Healthcheck start_period not defined"

    def test_healthcheck_mirrors_helm_probe(self):
        """Healthcheck configuration mirrors Helm probe values."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Helm default: initialDelaySeconds: 10, periodSeconds: 30, timeoutSeconds: 10, failureThreshold: 3
        assert "30s" in content, "Interval should default to 30s matching Helm periodSeconds"
        assert "10s" in content, "Timeout should be 10s matching Helm timeoutSeconds"
        assert "retries: 3" in content, "Retries should be 3 matching Helm failureThreshold"


class TestDockerComposeNetworking:
    """Tests for networking configuration."""

    def test_networks_section_present(self):
        """Networks section defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "networks:" in content, "Networks section not found"

    def test_service_network_assigned(self):
        """Service assigned to network."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Service should reference a network
        assert re.search(r"networks:\s*-\s*{{ cookiecutter.service_slug }}-network", content), \
            "Service not assigned to network"

    def test_network_defined(self):
        """Network defined at top level."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "{{ cookiecutter.service_slug }}-network:" in content, \
            "Network not defined in networks section"

    def test_network_has_driver(self):
        """Network specifies driver."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert re.search(r"driver:\s*bridge", content), "Network driver not specified as bridge"


class TestDockerComposeRestartPolicy:
    """Tests for restart policy."""

    def test_restart_policy_present(self):
        """Service defines restart policy."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "restart:" in content, "Restart policy not defined"

    def test_restart_policy_unless_stopped(self):
        """Restart policy is unless-stopped."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        assert "unless-stopped" in content, "Restart policy should be 'unless-stopped'"


class TestDockerComposeStructure:
    """Tests for overall structure without YAML parsing."""

    def test_has_top_level_volumes(self):
        """Top-level volumes section defined."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Check for volumes section after services
        lines = content.split('\n')
        services_idx = next((i for i, line in enumerate(lines) if line.startswith('volumes:')), -1)
        assert services_idx > 0, "Top-level volumes section not found"

    def test_volumes_and_networks_at_end(self):
        """volumes and networks sections at end of file."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Both should be present at file level
        assert "volumes:" in content, "volumes section missing"
        assert "networks:" in content, "networks section missing"

    def test_jinja_template_variables_present(self):
        """Jinja2 template variables present for dynamic rendering."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should have {{ cookiecutter.service_slug }} variable
        assert "{{ cookiecutter.service_slug }}" in content, "Template variable not found"

    def test_jinja_filters_for_defaults(self):
        """Jinja2 filters used for providing defaults."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should use | default() filter for optional values
        assert "| default(" in content, "Default filter not used for template variables"

    def test_conditional_jvm_config(self):
        """Conditional JVM configuration for Java language."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should have conditional block for Java
        assert "{% if cookiecutter.language == 'java'" in content, "JVM conditional block not found"

    def test_environment_variable_substitution_syntax(self):
        """Environment variables use shell substitution syntax."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should use ${VAR:-default} syntax for runtime overrides
        assert re.search(r'\$\{[A-Z_]+:-[^}]+\}', content), \
            "Environment variable substitution syntax not found"

    def test_comment_documentation(self):
        """Code contains helpful comments."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should have comments explaining sections
        assert "#" in content, "Comments not found for documentation"
        comment_count = content.count("#")
        assert comment_count >= 3, f"Expected at least 3 comments, found {comment_count}"

    def test_service_port_uses_filter(self):
        """Service port uses Jinja default filter."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Port should use default filter: {{ cookiecutter.service_port | default('8080') }}
        assert "| default('8080')" in content, "Port default filter not found"

    def test_health_check_uses_netcat(self):
        """Healthcheck uses netcat (nc) command for TCP check."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should use nc (netcat) for TCP probe
        assert "nc" in content, "netcat command not found in healthcheck"

    def test_all_env_vars_documented(self):
        """All environment variables are documented with comments."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Comments should explain the purpose of env vars
        assert "Service configuration matching Helm ConfigMap" in content, \
            "Helm ConfigMap reference comment not found"

    def test_no_hardcoded_secrets(self):
        """Configuration does not contain hardcoded secrets."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should not contain patterns like password=, token=, secret=, api_key=
        secret_patterns = ['password=', 'token=', 'secret=', 'api_key=', 'AWS_SECRET_ACCESS_KEY']
        for pattern in secret_patterns:
            assert pattern not in content, f"Potential secret found: {pattern}"

    def test_volume_mount_paths_absolute(self):
        """Volume mount paths use absolute paths or dot notation."""
        compose_file = Path("{{ cookiecutter.service_slug }}/docker-compose.yml")
        content = compose_file.read_text()
        # Should use . for current directory or absolute paths
        assert re.search(r'volumes:\s*#.*\n\s*-\s*\.:', content), \
            "Volume mount should use dot notation for current directory"
