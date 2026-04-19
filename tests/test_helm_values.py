"""Tests for Helm values.yaml configuration."""
import re
from pathlib import Path
from typing import Any, Dict

import pytest
import yaml


class TestHelmValuesPresence:
    """Test that values.yaml file exists and is valid YAML."""

    @pytest.fixture
    def values_file_path(self) -> Path:
        """Get path to values.yaml file."""
        repo_root = Path(__file__).parent.parent
        return repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "values.yaml"

    @pytest.fixture
    def values_data(self, values_file_path: Path) -> Dict[str, Any]:
        """Load and parse values.yaml."""
        assert values_file_path.exists(), f"values.yaml not found at {values_file_path}"
        with open(values_file_path, 'r') as f:
            data = yaml.safe_load(f)
        assert data is not None, "values.yaml is empty or invalid"
        return data

    def test_values_file_exists(self, values_file_path: Path) -> None:
        """Verify values.yaml file exists."""
        assert values_file_path.exists(), "values.yaml file does not exist"

    def test_values_file_is_valid_yaml(self, values_file_path: Path) -> None:
        """Verify values.yaml is valid YAML."""
        with open(values_file_path, 'r') as f:
            data = yaml.safe_load(f)
        assert data is not None, "values.yaml is empty or invalid YAML"
        assert isinstance(data, dict), "values.yaml root must be a dictionary"


class TestRequiredSections:
    """Test that required sections exist in values.yaml."""

    @pytest.fixture
    def values_data(self) -> Dict[str, Any]:
        """Load and parse values.yaml."""
        repo_root = Path(__file__).parent.parent
        values_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "values.yaml"
        with open(values_file, 'r') as f:
            return yaml.safe_load(f)

    def test_replica_count_section_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify replicaCount section exists."""
        assert "replicaCount" in values_data, "replicaCount not found in values.yaml"

    def test_image_section_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify image section exists."""
        assert "image" in values_data, "image section not found in values.yaml"

    def test_resources_section_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify resources section exists."""
        assert "resources" in values_data, "resources section not found in values.yaml"

    def test_storage_section_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify storage section exists."""
        assert "storage" in values_data, "storage section not found in values.yaml"

    def test_jvm_section_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify JVM configuration section exists."""
        assert "jvm" in values_data, "jvm section not found in values.yaml"

    def test_health_checks_section_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify healthChecks section exists."""
        assert "healthChecks" in values_data, "healthChecks section not found in values.yaml"

    def test_env_section_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify env section exists."""
        assert "env" in values_data, "env section not found in values.yaml"


class TestDevDefaults:
    """Test that dev environment defaults are correctly set."""

    @pytest.fixture
    def values_data(self) -> Dict[str, Any]:
        """Load and parse values.yaml."""
        repo_root = Path(__file__).parent.parent
        values_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "values.yaml"
        with open(values_file, 'r') as f:
            return yaml.safe_load(f)

    def test_replica_count_is_three(self, values_data: Dict[str, Any]) -> None:
        """Verify replicaCount is set to 3."""
        assert values_data["replicaCount"] == 3, "replicaCount should be 3 for dev"

    def test_storage_size_is_10gi(self, values_data: Dict[str, Any]) -> None:
        """Verify storage size is set to 10Gi."""
        assert values_data["storage"]["size"] == "10Gi", "storage.size should be 10Gi"

    def test_heap_min_is_512m(self, values_data: Dict[str, Any]) -> None:
        """Verify JVM heap minimum is 512m."""
        assert values_data["jvm"]["heapMin"] == "512m", "jvm.heapMin should be 512m"

    def test_heap_max_is_1g(self, values_data: Dict[str, Any]) -> None:
        """Verify JVM heap maximum is 1g."""
        assert values_data["jvm"]["heapMax"] == "1g", "jvm.heapMax should be 1g"

    def test_image_pull_policy_is_ifnotpresent(self, values_data: Dict[str, Any]) -> None:
        """Verify image pullPolicy is IfNotPresent."""
        assert (
            values_data["image"]["pullPolicy"] == "IfNotPresent"
        ), "image.pullPolicy should be IfNotPresent"

    def test_compression_is_snappy(self, values_data: Dict[str, Any]) -> None:
        """Verify COMPRESSION environment variable is set to snappy."""
        env_vars = values_data["env"]
        compression_var = next(
            (var for var in env_vars if var.get("name") == "COMPRESSION"), None
        )
        assert compression_var is not None, "COMPRESSION env var not found"
        assert compression_var["value"] == "snappy", "COMPRESSION should be snappy"


class TestResourceUnits:
    """Test that resource units are valid."""

    @pytest.fixture
    def values_data(self) -> Dict[str, Any]:
        """Load and parse values.yaml."""
        repo_root = Path(__file__).parent.parent
        values_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "values.yaml"
        with open(values_file, 'r') as f:
            return yaml.safe_load(f)

    def _is_valid_memory_unit(self, value: str) -> bool:
        """Check if memory value has valid unit."""
        pattern = r'^[0-9]+([KMG]i|Ki)?$'
        return bool(re.match(pattern, value))

    def _is_valid_cpu_unit(self, value: str) -> bool:
        """Check if CPU value has valid unit."""
        pattern = r'^([0-9]+m|[0-9]+(\.[0-9]+)?)$'
        return bool(re.match(pattern, value))

    def test_request_memory_unit_valid(self, values_data: Dict[str, Any]) -> None:
        """Verify resources.requests.memory has valid unit."""
        memory = values_data["resources"]["requests"]["memory"]
        assert self._is_valid_memory_unit(
            memory
        ), f"Invalid memory unit: {memory}"

    def test_request_cpu_unit_valid(self, values_data: Dict[str, Any]) -> None:
        """Verify resources.requests.cpu has valid unit."""
        cpu = values_data["resources"]["requests"]["cpu"]
        assert self._is_valid_cpu_unit(cpu), f"Invalid CPU unit: {cpu}"

    def test_limit_memory_unit_valid(self, values_data: Dict[str, Any]) -> None:
        """Verify resources.limits.memory has valid unit."""
        memory = values_data["resources"]["limits"]["memory"]
        assert self._is_valid_memory_unit(
            memory
        ), f"Invalid memory unit: {memory}"

    def test_limit_cpu_unit_valid(self, values_data: Dict[str, Any]) -> None:
        """Verify resources.limits.cpu has valid unit."""
        cpu = values_data["resources"]["limits"]["cpu"]
        assert self._is_valid_cpu_unit(cpu), f"Invalid CPU unit: {cpu}"

    def test_storage_size_unit_valid(self, values_data: Dict[str, Any]) -> None:
        """Verify storage.size has valid unit."""
        size = values_data["storage"]["size"]
        assert self._is_valid_memory_unit(
            size
        ), f"Invalid storage unit: {size}"


class TestImageConfiguration:
    """Test image configuration details."""

    @pytest.fixture
    def values_data(self) -> Dict[str, Any]:
        """Load and parse values.yaml."""
        repo_root = Path(__file__).parent.parent
        values_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "values.yaml"
        with open(values_file, 'r') as f:
            return yaml.safe_load(f)

    def test_image_has_repository(self, values_data: Dict[str, Any]) -> None:
        """Verify image.repository is defined."""
        assert "repository" in values_data["image"], "image.repository not found"
        assert values_data["image"]["repository"], "image.repository cannot be empty"

    def test_image_has_tag(self, values_data: Dict[str, Any]) -> None:
        """Verify image.tag is defined."""
        assert "tag" in values_data["image"], "image.tag not found"
        assert values_data["image"]["tag"], "image.tag cannot be empty"

    def test_image_has_pull_policy(self, values_data: Dict[str, Any]) -> None:
        """Verify image.pullPolicy is defined."""
        assert "pullPolicy" in values_data["image"], "image.pullPolicy not found"
        assert values_data["image"]["pullPolicy"], "image.pullPolicy cannot be empty"


class TestHealthCheckConfiguration:
    """Test health check configuration."""

    @pytest.fixture
    def values_data(self) -> Dict[str, Any]:
        """Load and parse values.yaml."""
        repo_root = Path(__file__).parent.parent
        values_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "values.yaml"
        with open(values_file, 'r') as f:
            return yaml.safe_load(f)

    def test_liveness_probe_configured(self, values_data: Dict[str, Any]) -> None:
        """Verify liveness probe is configured."""
        assert (
            "liveness" in values_data["healthChecks"]
        ), "liveness probe not found"
        assert (
            values_data["healthChecks"]["liveness"]["enabled"] is True
        ), "liveness probe should be enabled"

    def test_readiness_probe_configured(self, values_data: Dict[str, Any]) -> None:
        """Verify readiness probe is configured."""
        assert (
            "readiness" in values_data["healthChecks"]
        ), "readiness probe not found"
        assert (
            values_data["healthChecks"]["readiness"]["enabled"] is True
        ), "readiness probe should be enabled"

    def test_liveness_has_required_fields(self, values_data: Dict[str, Any]) -> None:
        """Verify liveness probe has required timing fields."""
        liveness = values_data["healthChecks"]["liveness"]
        required_fields = [
            "initialDelaySeconds",
            "periodSeconds",
            "timeoutSeconds",
            "failureThreshold",
        ]
        for field in required_fields:
            assert field in liveness, f"liveness probe missing {field}"


class TestEnvironmentVariables:
    """Test environment variable configuration."""

    @pytest.fixture
    def values_data(self) -> Dict[str, Any]:
        """Load and parse values.yaml."""
        repo_root = Path(__file__).parent.parent
        values_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "values.yaml"
        with open(values_file, 'r') as f:
            return yaml.safe_load(f)

    def test_env_is_list(self, values_data: Dict[str, Any]) -> None:
        """Verify env is a list."""
        assert isinstance(values_data["env"], list), "env should be a list"

    def test_env_variables_have_name_and_value(self, values_data: Dict[str, Any]) -> None:
        """Verify each env var has name and value."""
        for env_var in values_data["env"]:
            assert "name" in env_var, "env var missing 'name'"
            assert "value" in env_var, "env var missing 'value'"

    def test_service_name_env_var_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify SERVICE_NAME environment variable is set."""
        env_vars = values_data["env"]
        service_name_var = next(
            (var for var in env_vars if var.get("name") == "SERVICE_NAME"), None
        )
        assert service_name_var is not None, "SERVICE_NAME env var not found"

    def test_log_level_env_var_exists(self, values_data: Dict[str, Any]) -> None:
        """Verify LOG_LEVEL environment variable is set."""
        env_vars = values_data["env"]
        log_level_var = next(
            (var for var in env_vars if var.get("name") == "LOG_LEVEL"), None
        )
        assert log_level_var is not None, "LOG_LEVEL env var not found"
