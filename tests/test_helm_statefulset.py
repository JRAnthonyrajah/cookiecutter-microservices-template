"""Tests for Helm StatefulSet template."""
import re
from pathlib import Path
from typing import Any, Dict

import pytest
import yaml


class TestStatefulSetPresence:
    """Test that StatefulSet template exists and is valid YAML."""

    @pytest.fixture
    def statefulset_file_path(self) -> Path:
        """Get path to statefulset.yaml file."""
        repo_root = Path(__file__).parent.parent
        return repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"

    @pytest.fixture
    def statefulset_data(self, statefulset_file_path: Path) -> str:
        """Load statefulset.yaml content."""
        assert statefulset_file_path.exists(), f"statefulset.yaml not found at {statefulset_file_path}"
        with open(statefulset_file_path, 'r') as f:
            content = f.read()
        assert content, "statefulset.yaml is empty"
        return content

    def test_statefulset_file_exists(self, statefulset_file_path: Path) -> None:
        """Verify statefulset.yaml file exists."""
        assert statefulset_file_path.exists(), "statefulset.yaml file does not exist"

    def test_statefulset_file_has_content(self, statefulset_data: str) -> None:
        """Verify statefulset.yaml has content and valid structure."""
        assert len(statefulset_data) > 0, "statefulset.yaml should not be empty"
        assert "apiVersion:" in statefulset_data, "apiVersion must be specified"
        assert "kind:" in statefulset_data, "kind must be specified"
        assert "metadata:" in statefulset_data, "metadata must be specified"
        assert "spec:" in statefulset_data, "spec must be specified"


class TestStatefulSetKind:
    """Test that StatefulSet has correct kind and apiVersion."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_statefulset_kind_is_correct(self, statefulset_data: str) -> None:
        """Verify kind is StatefulSet."""
        assert "kind: StatefulSet" in statefulset_data, "kind must be StatefulSet"

    def test_statefulset_apiversion_is_correct(self, statefulset_data: str) -> None:
        """Verify apiVersion is apps/v1."""
        assert "apiVersion: apps/v1" in statefulset_data, "apiVersion must be apps/v1"

    def test_statefulset_has_metadata(self, statefulset_data: str) -> None:
        """Verify metadata section exists."""
        assert "metadata:" in statefulset_data, "metadata section must exist"

    def test_statefulset_has_labels(self, statefulset_data: str) -> None:
        """Verify labels are defined using _helpers.tpl."""
        assert "labels:" in statefulset_data, "labels section must exist"
        assert "include" in statefulset_data and ".labels" in statefulset_data, \
            "labels should use helper template functions"


class TestServiceName:
    """Test that StatefulSet references serviceName correctly."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_servicename_is_defined(self, statefulset_data: str) -> None:
        """Verify serviceName is defined in spec."""
        assert "serviceName:" in statefulset_data, "serviceName must be defined in StatefulSet spec"

    def test_servicename_uses_fullname(self, statefulset_data: str) -> None:
        """Verify serviceName uses fullname helper."""
        assert "serviceName: {{ include" in statefulset_data, \
            "serviceName should use fullname helper for ordered pod naming"

    def test_pod_management_policy_is_parallel(self, statefulset_data: str) -> None:
        """Verify podManagementPolicy is set to Parallel for faster scaling."""
        assert "podManagementPolicy: Parallel" in statefulset_data, \
            "podManagementPolicy should be Parallel for faster scaling"


class TestReplicaCount:
    """Test that replica count configuration is correct."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_replicas_references_values(self, statefulset_data: str) -> None:
        """Verify replicas uses values.replicaCount."""
        assert "replicas: {{ .Values.replicaCount }}" in statefulset_data, \
            "replicas should reference .Values.replicaCount"

    def test_selector_match_labels(self, statefulset_data: str) -> None:
        """Verify selector uses matchLabels."""
        assert "selector:" in statefulset_data, "selector section must exist"
        assert "matchLabels:" in statefulset_data, "matchLabels must be defined in selector"


class TestPodTemplate:
    """Test pod template configuration."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_template_has_labels(self, statefulset_data: str) -> None:
        """Verify template has selector labels."""
        assert "template:" in statefulset_data, "template section must exist"
        assert "labels:" in statefulset_data, "template metadata must have labels"

    def test_container_specification(self, statefulset_data: str) -> None:
        """Verify container specification exists."""
        assert "containers:" in statefulset_data, "containers section must exist"
        assert "image:" in statefulset_data, "image must be specified"
        assert "ports:" in statefulset_data, "ports must be specified"


class TestProbes:
    """Test liveness and readiness probe configuration."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_liveness_probe_exists(self, statefulset_data: str) -> None:
        """Verify liveness probe is configured."""
        assert "livenessProbe:" in statefulset_data, "livenessProbe must be configured"

    def test_liveness_probe_uses_tcp_socket(self, statefulset_data: str) -> None:
        """Verify liveness probe uses TCP socket."""
        assert "tcpSocket:" in statefulset_data, "liveness probe should use tcpSocket"

    def test_liveness_probe_initial_delay(self, statefulset_data: str) -> None:
        """Verify liveness probe has initialDelaySeconds from values."""
        assert "initialDelaySeconds:" in statefulset_data, \
            "liveness probe must have initialDelaySeconds"
        assert ".Values.healthChecks.liveness.initialDelaySeconds" in statefulset_data, \
            "should reference healthChecks.liveness.initialDelaySeconds"

    def test_liveness_probe_period(self, statefulset_data: str) -> None:
        """Verify liveness probe has periodSeconds."""
        assert "periodSeconds:" in statefulset_data, "liveness probe must have periodSeconds"
        assert ".Values.healthChecks.liveness.periodSeconds" in statefulset_data, \
            "should reference healthChecks.liveness.periodSeconds"

    def test_readiness_probe_exists(self, statefulset_data: str) -> None:
        """Verify readiness probe is configured."""
        assert "readinessProbe:" in statefulset_data, "readinessProbe must be configured"

    def test_readiness_probe_uses_exec(self, statefulset_data: str) -> None:
        """Verify readiness probe uses exec command."""
        assert "exec:" in statefulset_data, "readiness probe should use exec"
        assert "command:" in statefulset_data, "readiness probe exec must have command"

    def test_readiness_probe_initial_delay(self, statefulset_data: str) -> None:
        """Verify readiness probe has initialDelaySeconds."""
        lines = statefulset_data.split('\n')
        found_readiness = False
        for i, line in enumerate(lines):
            if 'readinessProbe:' in line:
                found_readiness = True
                # Check next lines contain initialDelaySeconds
                probe_content = '\n'.join(lines[i:i+10])
                assert 'initialDelaySeconds:' in probe_content, \
                    "readiness probe must have initialDelaySeconds"
                break
        assert found_readiness, "readiness probe must exist"

    def test_readiness_probe_references_values(self, statefulset_data: str) -> None:
        """Verify readiness probe references health check values."""
        assert ".Values.healthChecks.readiness" in statefulset_data, \
            "readiness probe should reference healthChecks.readiness values"


class TestAffinity:
    """Test pod anti-affinity configuration."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_affinity_section_exists(self, statefulset_data: str) -> None:
        """Verify affinity section exists."""
        assert "affinity:" in statefulset_data, "affinity section must exist for pod distribution"

    def test_pod_anti_affinity_configured(self, statefulset_data: str) -> None:
        """Verify pod anti-affinity is configured."""
        assert "podAntiAffinity:" in statefulset_data, "podAntiAffinity must be configured"

    def test_anti_affinity_is_preferred(self, statefulset_data: str) -> None:
        """Verify anti-affinity uses preferredDuringScheduling (not required)."""
        assert "preferredDuringSchedulingIgnoredDuringExecution:" in statefulset_data, \
            "anti-affinity should be preferred (not required) for flexibility"

    def test_affinity_topology_key(self, statefulset_data: str) -> None:
        """Verify affinity uses hostname topology key for node distribution."""
        assert "topologyKey: kubernetes.io/hostname" in statefulset_data, \
            "topologyKey should be kubernetes.io/hostname for node-level distribution"


class TestEnvironmentVariables:
    """Test environment variable configuration."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_env_section_exists(self, statefulset_data: str) -> None:
        """Verify env section exists in container spec."""
        assert "env:" in statefulset_data, "env section must exist"

    def test_env_from_values(self, statefulset_data: str) -> None:
        """Verify env variables reference values."""
        assert ".Values.env" in statefulset_data, "env should reference .Values.env"

    def test_jvm_heap_env_vars(self, statefulset_data: str) -> None:
        """Verify JVM heap environment variables are configured."""
        assert "JVM_HEAP_MIN" in statefulset_data, "JVM_HEAP_MIN env var should be set"
        assert "JVM_HEAP_MAX" in statefulset_data, "JVM_HEAP_MAX env var should be set"
        assert ".Values.jvm.heapMin" in statefulset_data, \
            "JVM_HEAP_MIN should reference .Values.jvm.heapMin"
        assert ".Values.jvm.heapMax" in statefulset_data, \
            "JVM_HEAP_MAX should reference .Values.jvm.heapMax"

    def test_jvm_opts_env_var(self, statefulset_data: str) -> None:
        """Verify JVM options environment variable."""
        assert "JVM_OPTS" in statefulset_data, "JVM_OPTS env var should be set"
        assert ".Values.jvm.jvmOpts" in statefulset_data, \
            "JVM_OPTS should reference .Values.jvm.jvmOpts"

    def test_configmap_envfrom(self, statefulset_data: str) -> None:
        """Verify ConfigMap is referenced via envFrom when enabled."""
        assert "envFrom:" in statefulset_data, "envFrom should be used for ConfigMap"
        assert "configMapRef:" in statefulset_data, "configMapRef should reference ConfigMap"


class TestResources:
    """Test resource requests and limits."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_resources_section_exists(self, statefulset_data: str) -> None:
        """Verify resources section exists."""
        assert "resources:" in statefulset_data, "resources section must exist"

    def test_resources_references_values(self, statefulset_data: str) -> None:
        """Verify resources reference values.yaml."""
        assert ".Values.resources" in statefulset_data, \
            "resources should reference .Values.resources"


class TestVolumeConfiguration:
    """Test volume and storage configuration."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_volume_mounts_conditional(self, statefulset_data: str) -> None:
        """Verify volumeMounts are conditionally included."""
        assert "volumeMounts:" in statefulset_data, "volumeMounts should be defined"
        assert ".Values.storage.enabled" in statefulset_data, \
            "volume mounts should be conditional on storage.enabled"

    def test_volume_claim_templates(self, statefulset_data: str) -> None:
        """Verify volumeClaimTemplates are defined."""
        assert "volumeClaimTemplates:" in statefulset_data, \
            "volumeClaimTemplates must be defined for PVC generation"

    def test_storage_class_reference(self, statefulset_data: str) -> None:
        """Verify storage class references values."""
        assert ".Values.storage.storageClassName" in statefulset_data, \
            "storageClassName should reference .Values.storage.storageClassName"

    def test_storage_size_reference(self, statefulset_data: str) -> None:
        """Verify storage size references values."""
        assert ".Values.storage.size" in statefulset_data, \
            "storage size should reference .Values.storage.size"


class TestSecurityContext:
    """Test security context configuration."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    def test_security_context_exists(self, statefulset_data: str) -> None:
        """Verify securityContext is defined."""
        assert "securityContext:" in statefulset_data, "securityContext must be defined"

    def test_security_context_references_values(self, statefulset_data: str) -> None:
        """Verify securityContext references values."""
        assert ".Values.securityContext" in statefulset_data, \
            "securityContext should reference .Values.securityContext"


class TestHelperFunctions:
    """Test that helper functions from _helpers.tpl are used correctly."""

    @pytest.fixture
    def statefulset_data(self) -> str:
        """Load statefulset.yaml content."""
        repo_root = Path(__file__).parent.parent
        statefulset_file = repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "statefulset.yaml"
        with open(statefulset_file, 'r') as f:
            return f.read()

    @pytest.fixture
    def helpers_file(self) -> Path:
        """Get path to _helpers.tpl file."""
        repo_root = Path(__file__).parent.parent
        return repo_root / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "_helpers.tpl"

    def test_helpers_file_exists(self, helpers_file: Path) -> None:
        """Verify _helpers.tpl file exists."""
        assert helpers_file.exists(), "_helpers.tpl must exist for template functions"

    def test_uses_fullname_helper(self, statefulset_data: str) -> None:
        """Verify fullname helper is used."""
        assert 'include "chart.fullname"' in statefulset_data, \
            "fullname helper should be used for consistent naming"

    def test_uses_name_helper(self, statefulset_data: str) -> None:
        """Verify name helper is used."""
        assert 'include "chart.name"' in statefulset_data, \
            "name helper should be used"

    def test_uses_labels_helper(self, statefulset_data: str) -> None:
        """Verify labels helper is used."""
        assert 'include "chart.labels"' in statefulset_data, \
            "labels helper should be used for consistent labeling"

    def test_uses_selector_labels_helper(self, statefulset_data: str) -> None:
        """Verify selectorLabels helper is used."""
        assert 'include "chart.selectorLabels"' in statefulset_data, \
            "selectorLabels helper should be used in selectors and matchLabels"
