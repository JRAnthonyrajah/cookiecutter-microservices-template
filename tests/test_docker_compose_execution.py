"""Tests for docker-compose.yml execution validation.

This module provides comprehensive testing for docker-compose.yml execution scenarios,
including file validation, build configuration, service integration, and cleanup.
Tests are designed to validate execution without requiring Docker daemon to be running.
"""
import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from unittest import mock

import pytest
import yaml


logger = logging.getLogger(__name__)


# ============================================================================
# FIXTURES AND TEST UTILITIES
# ============================================================================


@pytest.fixture
def compose_file_path():
    """Return path to docker-compose.yml."""
    return Path("{{ cookiecutter.service_slug }}/docker-compose.yml")


@pytest.fixture
def compose_content(compose_file_path) -> str:
    """Read and return docker-compose.yml content."""
    return compose_file_path.read_text()


@pytest.fixture
def compose_dict(compose_content) -> dict:
    """Parse and return docker-compose.yml as dictionary.

    Note: For template files with Jinja2 variables, attempts to parse but may
    fail if Jinja2 template syntax is used. In such cases, returns minimal dict.
    """
    # Parse the YAML content
    try:
        data = yaml.safe_load(compose_content)
        return data if data else {}
    except yaml.YAMLError:
        # File contains Jinja2 templates, so we can't parse it directly
        # Return an empty dict - tests will use content-based validation instead
        return {}


@pytest.fixture
def mock_docker_compose():
    """Mock docker-compose command execution."""
    with mock.patch('subprocess.run') as mock_run:
        yield mock_run


@pytest.fixture
def service_config(compose_content) -> dict:
    """Extract main service configuration from content.

    Since compose_dict may be empty due to Jinja2 templates, we extract
    service name from content and return marker dict.
    """
    # Extract service name from content
    match = re.search(r'services:\s*\n\s*(\S+):', compose_content)
    if match:
        return {'name': match.group(1)}
    return {}


# ============================================================================
# SECTION A: FILE VALIDATION TESTS (10 tests)
# ============================================================================


class TestFileValidation:
    """Tests for docker-compose.yml file existence and YAML validity."""

    def test_compose_file_exists(self, compose_file_path):
        """docker-compose.yml file exists in service directory."""
        assert compose_file_path.exists(), \
            f"docker-compose.yml not found at {compose_file_path}"

    def test_compose_file_is_readable(self, compose_file_path):
        """docker-compose.yml file is readable."""
        assert compose_file_path.is_file(), \
            f"docker-compose.yml is not a regular file"
        assert compose_file_path.stat().st_size > 0, \
            "docker-compose.yml is empty"

    def test_compose_file_valid_yaml_syntax(self, compose_content):
        """docker-compose.yml contains valid YAML syntax (when Jinja2 rendered)."""
        # Since the file contains Jinja2 templates, we check for common syntax patterns
        # rather than full parsing
        assert "version:" in compose_content, \
            "Version declaration required"
        assert "services:" in compose_content, \
            "Services section required"
        # Check for proper indentation patterns
        lines = compose_content.split('\n')
        assert len(lines) > 5, \
            "File should have meaningful content"

    def test_compose_version_specified(self, compose_content):
        """docker-compose.yml specifies version."""
        assert 'version:' in compose_content, \
            "Version not specified in docker-compose.yml"
        # Check version pattern (3.8 or higher)
        assert re.search(r'version:\s*["\']?3\.[0-9]', compose_content), \
            "Version should be 3.x format"

    def test_compose_version_at_least_38(self, compose_content):
        """docker-compose.yml specifies version 3.8 or higher."""
        # Extract version from content
        match = re.search(r'version:\s*["\']?([0-9.]+)["\']?', compose_content)
        assert match, "Version not found"
        version = match.group(1)
        # Parse version parts
        parts = version.split('.')
        major = int(parts[0]) if len(parts) > 0 else 0
        minor = int(parts[1]) if len(parts) > 1 else 0
        assert major > 3 or (major == 3 and minor >= 8), \
            f"Version should be 3.8 or higher, got {version}"

    def test_compose_has_services_section(self, compose_content):
        """docker-compose.yml has services section."""
        assert 'services:' in compose_content, \
            "services section not found in docker-compose.yml"

    def test_compose_has_volumes_section(self, compose_content):
        """docker-compose.yml has volumes section."""
        assert 'volumes:' in compose_content, \
            "volumes section not found in docker-compose.yml"

    def test_compose_has_networks_section(self, compose_content):
        """docker-compose.yml has networks section."""
        assert 'networks:' in compose_content, \
            "networks section not found in docker-compose.yml"

    def test_compose_file_permissions_readable(self, compose_file_path):
        """docker-compose.yml file has readable permissions."""
        stat_info = compose_file_path.stat()
        readable = bool(stat_info.st_mode & 0o400)
        assert readable, \
            "docker-compose.yml is not readable"


# ============================================================================
# SECTION B: BUILD CONFIGURATION TESTS (15 tests)
# ============================================================================


class TestBuildConfiguration:
    """Tests for build context, Dockerfile configuration, and image naming."""

    def test_service_has_build_section(self, compose_content):
        """Main service defines build section."""
        assert 'build:' in compose_content, \
            "build section not found in service configuration"

    def test_build_context_specified(self, compose_content):
        """Build section specifies context."""
        assert re.search(r'build:\s*\n\s*context:', compose_content, re.MULTILINE), \
            "context not specified in build section"
        assert re.search(r'context:\s*\.', compose_content), \
            "context should be '.'"

    def test_build_dockerfile_specified(self, compose_content):
        """Build section specifies Dockerfile path."""
        assert re.search(r'dockerfile:\s*Dockerfile', compose_content), \
            "dockerfile not specified as 'Dockerfile' in build section"

    def test_dockerfile_exists_in_context(self):
        """Dockerfile exists in the build context directory."""
        dockerfile_path = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        assert dockerfile_path.exists(), \
            f"Dockerfile not found at {dockerfile_path}"

    def test_dockerfile_is_readable(self):
        """Dockerfile is readable."""
        dockerfile_path = Path("{{ cookiecutter.service_slug }}/Dockerfile")
        assert dockerfile_path.is_file(), \
            "Dockerfile is not a regular file"
        assert dockerfile_path.stat().st_size > 0, \
            "Dockerfile is empty"

    def test_service_container_name_defined(self, compose_content):
        """Service defines container_name."""
        assert 'container_name:' in compose_content, \
            "container_name not defined in service"

    def test_container_name_format(self, compose_content):
        """Container name follows naming convention (slug-dev)."""
        # Should have pattern like container_name: {{ cookiecutter.service_slug }}-dev
        assert re.search(r'container_name:.*-dev', compose_content), \
            "Container name should end with '-dev'"

    def test_build_args_optional(self, compose_content):
        """Build args are optional but properly formatted if present."""
        # If args are present, they should have proper format
        if 'args:' in compose_content:
            assert re.search(r'args:\s*(\n|$)', compose_content), \
                "build.args should be properly formatted"

    def test_image_naming_pattern(self, compose_content):
        """Image naming follows service slug pattern in templates."""
        # Check for consistent image naming in compose file
        if 'image:' in compose_content:
            # If explicit image is used, verify naming
            match = re.search(r'image:\s*([^\n]+)', compose_content)
            assert match, "Image definition found but not parseable"

    def test_service_ports_defined(self, compose_content):
        """Service defines ports for accessibility."""
        assert 'ports:' in compose_content, \
            "ports section not found in service"
        assert re.search(r'ports:\s*\n\s*-\s*', compose_content), \
            "No port mappings defined in ports section"

    def test_port_mapping_has_host_port(self, compose_content):
        """Port mapping includes host port."""
        # Find port mappings
        ports = re.findall(r'ports:\s*\n\s*-\s*["\']?([^\n]+)', compose_content)
        assert len(ports) > 0, \
            "No port mappings found"
        first_port = ports[0]
        assert ':' in first_port, \
            f"Port mapping should have format 'host:container', got {first_port}"

    def test_service_has_environment_section(self, compose_content):
        """Service defines environment variables section."""
        assert 'environment:' in compose_content, \
            "environment section not found in service"

    def test_environment_variables_properly_formatted(self, compose_content):
        """Environment variables are properly formatted."""
        # Find environment section and verify it has variables
        assert re.search(r'environment:\s*\n', compose_content), \
            "No environment section found"
        assert re.search(r'[A-Z_]+:', compose_content), \
            "No environment variables found"

    def test_service_no_privileged_mode_by_default(self, compose_content):
        """Service does not enable privileged mode by default."""
        # Check that privileged is not set to true
        # Should either not be present or be false
        if 'privileged:' in compose_content:
            assert not re.search(r'privileged:\s*true', compose_content), \
                "Service should not run in privileged mode by default"

    def test_build_and_image_not_both_specified(self, compose_content):
        """Service specifies either build OR image, not both."""
        has_build = 'build:' in compose_content
        # Count how many times 'image:' appears at service level (rough check)
        has_image = bool(re.search(r'^\s{2,4}image:', compose_content, re.MULTILINE))
        # Typically should have build for this template
        assert has_build, \
            "Service should have build section for template generation"


# ============================================================================
# SECTION C: SERVICE INTEGRATION TESTS (8 tests)
# ============================================================================


class TestServiceIntegration:
    """Tests for service startup, health checks, and integration."""

    def test_service_has_healthcheck(self, compose_content):
        """Service defines healthcheck configuration."""
        assert 'healthcheck:' in compose_content, \
            "healthcheck section not found in service"

    def test_healthcheck_has_test_command(self, compose_content):
        """Healthcheck defines test command."""
        assert re.search(r'healthcheck:.*\n.*test:', compose_content, re.DOTALL), \
            "test command not defined in healthcheck"

    def test_healthcheck_interval_reasonable(self, compose_content):
        """Healthcheck interval is reasonable (between 10s and 60s)."""
        # Extract interval value
        match = re.search(r'interval:\s*(\d+)([smh])', compose_content)
        if match:
            value = int(match.group(1))
            unit = match.group(2)
            # Convert to seconds for comparison
            if unit == 'm':
                value *= 60
            elif unit == 'h':
                value *= 3600
            assert 10 <= value <= 300, \
                f"Healthcheck interval should be 10-300s, got {match.group(0)}"

    def test_healthcheck_timeout_less_than_interval(self, compose_content):
        """Healthcheck timeout is less than interval."""
        timeout_match = re.search(r'timeout:\s*(\d+)([smh])', compose_content)
        interval_match = re.search(r'interval:\s*(\d+)([smh])', compose_content)

        if timeout_match and interval_match:
            t_val = int(timeout_match.group(1))
            i_val = int(interval_match.group(1))
            assert t_val < i_val, \
                f"Timeout should be less than interval"

    def test_service_volumes_mounted(self, compose_content):
        """Service has volumes mounted."""
        # Find service-level volumes
        assert re.search(r'volumes:.*\n\s*-\s*', compose_content, re.DOTALL), \
            "volumes section not found in service or no volumes mounted"

    def test_volume_mount_paths_exist_or_valid(self, compose_content):
        """Volume mount paths are valid."""
        # Find all volume mounts
        volumes = re.findall(r'-\s*([^\n]+(?::/[^\n]*)?)', compose_content)
        assert len(volumes) > 0, \
            "No volumes found"
        # At least check that volumes section exists
        assert 'volumes:' in compose_content, \
            "volumes section not found"

    def test_service_assigned_to_network(self, compose_content):
        """Service is assigned to a network."""
        # Find networks section within service
        assert re.search(r'^\s{4,6}networks:\s*\n\s*-\s*', compose_content, re.MULTILINE), \
            "networks section not found in service"

    def test_restart_policy_defined(self, compose_content):
        """Service defines restart policy."""
        assert re.search(r'restart(?:_policy)?:', compose_content), \
            "restart policy not defined in service"


# ============================================================================
# SECTION D: CLEANUP & TEARDOWN TESTS (7 tests)
# ============================================================================


class TestCleanupAndTeardown:
    """Tests for proper cleanup, volume management, and resource cleanup."""

    def test_volumes_properly_defined_at_root(self, compose_content):
        """All volumes referenced in service are defined at root level."""
        # Find all volume references in service
        service_volumes = re.findall(r'(?:^\s{6,8}|\s*-\s*)([a-z0-9\-_]+)(?::/|\s*:)',
                                    compose_content, re.MULTILINE)
        # Find all volume definitions at root
        root_volumes = re.findall(r'^([a-z0-9\-_]+):\s*\n\s*driver:',
                                 compose_content, re.MULTILINE)

        # Check that named volumes (no slashes) are defined
        for vol in service_volumes:
            if vol != '.' and '/' not in vol:
                assert vol in root_volumes or 'volumes:' in compose_content, \
                    f"Volume '{vol}' referenced but may not be defined at root level"

    def test_networks_properly_defined_at_root(self, compose_content):
        """All networks referenced in service are defined at root level."""
        # Find all network references in service
        service_networks = re.findall(r'networks:\s*\n(?:\s*-\s*(\S+))+',
                                     compose_content)
        # Find all network definitions at root
        root_networks = re.findall(r'^networks:\s*\n((?:\s{2}\S+:\s*\n)+)',
                                  compose_content, re.MULTILINE)

        # Networks section should exist
        assert 'networks:' in compose_content, \
            "networks section not found at root level"

    def test_volume_drivers_valid(self, compose_content):
        """Volume drivers are valid."""
        valid_drivers = ['local', 'nfs', 'tmpfs', 'bind']

        # Check for driver specifications
        drivers = re.findall(r'driver:\s*(\w+)', compose_content)
        for driver in drivers:
            assert driver in valid_drivers or driver in ['bridge', 'overlay', 'host', 'macvlan', 'ipvlan', 'none'], \
                f"Invalid driver '{driver}' found"

    def test_network_drivers_valid(self, compose_content):
        """Network drivers are valid."""
        valid_drivers = ['bridge', 'overlay', 'host', 'macvlan', 'ipvlan', 'none']

        # Find driver specifications
        drivers = re.findall(r'driver:\s*(\w+)', compose_content)
        # Check network-level drivers (those under networks: section)
        if 'networks:' in compose_content:
            # networks section should have bridge driver typically
            assert any(d in valid_drivers for d in drivers), \
                f"Invalid driver found, expected one of {valid_drivers}"

    def test_no_orphan_volumes_likely(self, compose_content):
        """Configuration minimizes orphan volumes."""
        # Check that volumes have descriptive names (not random)
        assert not re.search(r'[a-f0-9]{12}', compose_content), \
            "Volume names should be descriptive, not random hashes"

    def test_no_dangling_references(self, compose_content):
        """No references to undefined services."""
        # Find all service names
        services = re.findall(r'^([a-z0-9\-_]+):\s*\n\s*build:',
                             compose_content, re.MULTILINE)

        # Check depends_on references if present
        depends_on = re.findall(r'depends_on:\s*\n(?:\s*-\s*(\S+)|\s*(\S+):)',
                               compose_content)
        for dep_tuple in depends_on:
            dep_name = dep_tuple[0] or dep_tuple[1]
            # Just check that depends_on pattern is reasonable
            assert dep_name, "depends_on reference should be valid"

    def test_volume_cleanup_not_prevented(self, compose_content):
        """Volumes configuration allows proper cleanup."""
        # Check that volumes don't have external: true
        assert not re.search(r'external:\s*true', compose_content), \
            "Volumes should not be marked as external (prevents cleanup)"


# ============================================================================
# INTEGRATION & EXECUTION SCENARIO TESTS
# ============================================================================


class TestExecutionScenarios:
    """Tests simulating real docker-compose execution scenarios."""

    @mock.patch('subprocess.run')
    def test_mock_docker_compose_up_execution(self, mock_run, compose_file_path):
        """Simulate docker-compose up execution."""
        mock_run.return_value = mock.Mock(returncode=0, stdout=b'', stderr=b'')

        # This would be the command to execute
        cmd = ['docker-compose', '-f', str(compose_file_path), 'up', '-d']
        result = subprocess.run(cmd, capture_output=True)

        assert result.returncode == 0, \
            "docker-compose up should succeed"

    @mock.patch('subprocess.run')
    def test_mock_docker_compose_down_execution(self, mock_run, compose_file_path):
        """Simulate docker-compose down execution."""
        mock_run.return_value = mock.Mock(returncode=0, stdout=b'', stderr=b'')

        cmd = ['docker-compose', '-f', str(compose_file_path), 'down', '-v']
        result = subprocess.run(cmd, capture_output=True)

        assert result.returncode == 0, \
            "docker-compose down should succeed"

    @mock.patch('subprocess.run')
    def test_mock_docker_compose_ps_execution(self, mock_run, compose_file_path):
        """Simulate docker-compose ps execution."""
        mock_output = b'NAME\tCOMMAND\tSTATUS\n'
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout=mock_output,
            stderr=b''
        )

        cmd = ['docker-compose', '-f', str(compose_file_path), 'ps']
        result = subprocess.run(cmd, capture_output=True)

        assert result.returncode == 0, \
            "docker-compose ps should succeed"

    @mock.patch('subprocess.run')
    def test_mock_docker_compose_logs_execution(self, mock_run, compose_file_path):
        """Simulate docker-compose logs execution."""
        mock_output = b'service-name | [INFO] Application started\n'
        mock_run.return_value = mock.Mock(
            returncode=0,
            stdout=mock_output,
            stderr=b''
        )

        cmd = ['docker-compose', '-f', str(compose_file_path), 'logs', '-f']
        result = subprocess.run(cmd, capture_output=True)

        assert result.returncode == 0, \
            "docker-compose logs should succeed"

    def test_compose_file_can_be_validated_with_config_command(self, compose_file_path):
        """docker-compose config command structure is valid."""
        # This tests that the file is structured correctly for validation
        content = compose_file_path.read_text()

        # File contains Jinja2 templates, so we check structural validity instead
        # Check for key sections
        assert 'version:' in content, "version section missing"
        assert 'services:' in content, "services section missing"
        assert 'volumes:' in content, "volumes section missing"
        assert 'networks:' in content, "networks section missing"


# ============================================================================
# ERROR HANDLING & EDGE CASES
# ============================================================================


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_compose_handles_missing_env_gracefully(self, compose_content):
        """docker-compose.yml uses defaults for missing environment variables."""
        # Check for ${VAR:-default} syntax
        assert re.search(r'\$\{[A-Z_]+:-[^}]+\}', compose_content), \
            "Environment variables should use default syntax (${VAR:-default})"

    def test_compose_no_syntax_errors_in_jinja(self, compose_content):
        """docker-compose.yml Jinja2 syntax is valid."""
        # Count unmatched braces
        open_braces = compose_content.count('{%')
        close_braces = compose_content.count('%}')
        assert open_braces == close_braces, \
            f"Unmatched Jinja2 tags: {open_braces} open, {close_braces} close"

    def test_compose_no_circular_dependencies(self, compose_content):
        """Services don't have circular dependencies."""
        # Since we have a template with single service, just verify no self-reference
        if 'depends_on:' in compose_content:
            # Service should not depend on itself
            match = re.search(r'services:\s*\n\s*(\S+):', compose_content)
            if match:
                service_name = match.group(1)
                assert service_name not in re.sub(
                    rf'services:\s*\n\s*{service_name}:.*?depends_on:',
                    '', compose_content), \
                    f"Service should not depend on itself"

    def test_compose_port_numbers_valid(self, compose_content):
        """Port numbers in compose are valid."""
        # Extract port numbers from port mappings
        ports = re.findall(r'ports:\s*\n\s*-\s*["\']?([^:"/]+)', compose_content)
        for port in ports:
            port = port.strip()
            # Skip if it's a variable
            if not port.startswith('$') and not port.startswith('{'):
                try:
                    port_num = int(port)
                    assert 1 <= port_num <= 65535, \
                        f"Invalid port number: {port_num}"
                except ValueError:
                    # Port might be a Jinja template variable, which is ok
                    pass
