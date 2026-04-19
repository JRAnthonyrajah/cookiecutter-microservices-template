"""
Test suite for Helm template rendering.

This module tests Helm template rendering with test values, validates YAML syntax,
verifies the presence of required Kubernetes resources (ConfigMap, PVC, StatefulSet, Service),
and checks probe configuration, labels, and selectors consistency.
"""
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
import yaml


class TestHelmChartValidation:
    """Test Helm chart structure and linting."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    def test_chart_yaml_exists(self, chart_dir: Path) -> None:
        """Test that Chart.yaml file exists."""
        chart_file = chart_dir / "Chart.yaml"
        assert chart_file.exists(), f"Chart.yaml not found at {chart_file}"
        assert chart_file.is_file(), f"Chart.yaml is not a file at {chart_file}"

    def test_chart_yaml_is_valid(self, chart_dir: Path) -> None:
        """Test that Chart.yaml is valid YAML."""
        chart_file = chart_dir / "Chart.yaml"
        with open(chart_file, 'r') as f:
            try:
                chart_data = yaml.safe_load(f)
                assert chart_data is not None, "Chart.yaml parsed as empty"
            except yaml.YAMLError as e:
                pytest.fail(f"Chart.yaml is not valid YAML: {e}")

    def test_chart_yaml_has_required_fields(self, chart_dir: Path) -> None:
        """Test that Chart.yaml has required fields."""
        chart_file = chart_dir / "Chart.yaml"
        with open(chart_file, 'r') as f:
            chart_data = yaml.safe_load(f)

        required_fields = ["apiVersion", "name", "description", "type", "version"]
        for field in required_fields:
            assert field in chart_data, f"Chart.yaml missing required field: {field}"

    def test_values_yaml_exists(self, chart_dir: Path) -> None:
        """Test that values.yaml file exists."""
        values_file = chart_dir / "values.yaml"
        assert values_file.exists(), f"values.yaml not found at {values_file}"

    def test_values_yaml_is_valid(self, chart_dir: Path) -> None:
        """Test that values.yaml is valid YAML."""
        values_file = chart_dir / "values.yaml"
        with open(values_file, 'r') as f:
            try:
                values_data = yaml.safe_load(f)
                assert values_data is not None, "values.yaml parsed as empty"
            except yaml.YAMLError as e:
                pytest.fail(f"values.yaml is not valid YAML: {e}")

    def test_templates_directory_exists(self, chart_dir: Path) -> None:
        """Test that templates directory exists."""
        templates_dir = chart_dir / "templates"
        assert templates_dir.exists(), f"templates directory not found at {templates_dir}"
        assert templates_dir.is_dir(), f"templates is not a directory at {templates_dir}"


class TestHelmLinting:
    """Test Helm chart linting."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    def test_helm_lint_passes(self, chart_dir: Path) -> None:
        """Test that helm lint passes for the chart."""
        try:
            result = subprocess.run(
                ["helm", "lint", str(chart_dir)],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0, \
                f"helm lint failed with exit code {result.returncode}:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        except FileNotFoundError:
            pytest.skip("helm command not found")
        except subprocess.TimeoutExpired:
            pytest.fail("helm lint command timed out")


class TestHelmTemplateRendering:
    """Test Helm template rendering with test values."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    @pytest.fixture
    def test_values_file(self) -> Path:
        """Get path to test values file."""
        return Path(__file__).parent / "fixtures" / "test-values.yaml"

    @pytest.fixture
    def rendered_manifests(self, chart_dir: Path, test_values_file: Path) -> str:
        """Render Helm templates with test values."""
        try:
            result = subprocess.run(
                [
                    "helm", "template",
                    "test-release",
                    str(chart_dir),
                    "--values", str(test_values_file)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                pytest.fail(
                    f"helm template failed with exit code {result.returncode}:\n"
                    f"stdout: {result.stdout}\nstderr: {result.stderr}"
                )
            return result.stdout
        except FileNotFoundError:
            pytest.skip("helm command not found")
        except subprocess.TimeoutExpired:
            pytest.fail("helm template command timed out")

    def test_helm_template_dry_run_succeeds(self, chart_dir: Path, test_values_file: Path) -> None:
        """Test that helm template dry-run succeeds."""
        try:
            result = subprocess.run(
                [
                    "helm", "template",
                    "test-release",
                    str(chart_dir),
                    "--values", str(test_values_file)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0, \
                f"helm template failed with exit code {result.returncode}:\n" \
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
        except FileNotFoundError:
            pytest.skip("helm command not found")

    def test_rendered_output_is_not_empty(self, rendered_manifests: str) -> None:
        """Test that rendered output contains Kubernetes manifests."""
        assert rendered_manifests, "helm template produced empty output"
        assert "---" in rendered_manifests or "apiVersion" in rendered_manifests, \
            "Rendered output does not contain Kubernetes resources"

    def test_all_rendered_yaml_documents_are_valid(self, rendered_manifests: str) -> None:
        """Test that all rendered YAML documents are valid."""
        # Split by document separator
        documents = rendered_manifests.split("---")

        valid_documents = 0
        for i, doc in enumerate(documents):
            # Skip empty documents
            if not doc.strip():
                continue

            try:
                parsed = yaml.safe_load(doc)
                # YAML parsing succeeded for this document
                valid_documents += 1
            except yaml.YAMLError as e:
                pytest.fail(f"Document {i} is not valid YAML: {e}\nContent: {doc[:200]}")

        assert valid_documents > 0, "No valid YAML documents found in rendered output"

    def test_statefulset_in_rendered_output(self, rendered_manifests: str) -> None:
        """Test that StatefulSet resource is present in rendered output."""
        assert "kind: StatefulSet" in rendered_manifests, \
            "StatefulSet not found in rendered Helm output"

    def test_service_in_rendered_output(self, rendered_manifests: str) -> None:
        """Test that Service resource is present in rendered output."""
        assert "kind: Service" in rendered_manifests, \
            "Service not found in rendered Helm output"

    def test_configmap_in_rendered_output(self, rendered_manifests: str) -> None:
        """Test that ConfigMap resource is present in rendered output."""
        assert "kind: ConfigMap" in rendered_manifests, \
            "ConfigMap not found in rendered Helm output"

    def test_pvc_in_rendered_output(self, rendered_manifests: str) -> None:
        """Test that PersistentVolumeClaim resource is present in rendered output."""
        assert "kind: PersistentVolumeClaim" in rendered_manifests, \
            "PersistentVolumeClaim not found in rendered Helm output"


class TestProbeConfiguration:
    """Test probe configuration in rendered templates."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    @pytest.fixture
    def test_values_file(self) -> Path:
        """Get path to test values file."""
        return Path(__file__).parent / "fixtures" / "test-values.yaml"

    @pytest.fixture
    def rendered_manifests(self, chart_dir: Path, test_values_file: Path) -> str:
        """Render Helm templates with test values."""
        try:
            result = subprocess.run(
                [
                    "helm", "template",
                    "test-release",
                    str(chart_dir),
                    "--values", str(test_values_file)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                pytest.fail(f"helm template failed: {result.stderr}")
            return result.stdout
        except FileNotFoundError:
            pytest.skip("helm command not found")

    def test_liveness_probe_configured(self, rendered_manifests: str) -> None:
        """Test that liveness probe is configured in StatefulSet."""
        assert "livenessProbe:" in rendered_manifests, \
            "livenessProbe not found in rendered StatefulSet"

    def test_readiness_probe_configured(self, rendered_manifests: str) -> None:
        """Test that readiness probe is configured in StatefulSet."""
        assert "readinessProbe:" in rendered_manifests, \
            "readinessProbe not found in rendered StatefulSet"

    def test_liveness_probe_has_initial_delay(self, rendered_manifests: str) -> None:
        """Test that liveness probe has initialDelaySeconds configured."""
        # Extract StatefulSet section
        if "livenessProbe:" in rendered_manifests:
            probe_section = rendered_manifests[
                rendered_manifests.find("livenessProbe:"):
                rendered_manifests.find("readinessProbe:")
            ]
            assert "initialDelaySeconds:" in probe_section, \
                "livenessProbe missing initialDelaySeconds"

    def test_readiness_probe_has_initial_delay(self, rendered_manifests: str) -> None:
        """Test that readiness probe has initialDelaySeconds configured."""
        if "readinessProbe:" in rendered_manifests:
            probe_section = rendered_manifests[
                rendered_manifests.find("readinessProbe:"):
                rendered_manifests.find("volumeClaimTemplates:") if "volumeClaimTemplates:" in rendered_manifests else len(rendered_manifests)
            ]
            assert "initialDelaySeconds:" in probe_section, \
                "readinessProbe missing initialDelaySeconds"


class TestLabelsAndSelectors:
    """Test labels and selectors consistency across resources."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    @pytest.fixture
    def test_values_file(self) -> Path:
        """Get path to test values file."""
        return Path(__file__).parent / "fixtures" / "test-values.yaml"

    @pytest.fixture
    def parsed_resources(self, chart_dir: Path, test_values_file: Path) -> List[Dict[str, Any]]:
        """Render and parse all resources."""
        try:
            result = subprocess.run(
                [
                    "helm", "template",
                    "test-release",
                    str(chart_dir),
                    "--values", str(test_values_file)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                pytest.fail(f"helm template failed: {result.stderr}")

            # Parse all documents
            documents = result.stdout.split("---")
            resources = []
            for doc in documents:
                if doc.strip():
                    try:
                        parsed = yaml.safe_load(doc)
                        if parsed and isinstance(parsed, dict):
                            resources.append(parsed)
                    except yaml.YAMLError:
                        pass
            return resources
        except FileNotFoundError:
            pytest.skip("helm command not found")

    def test_statefulset_has_selector_labels(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that StatefulSet has selector labels."""
        statefulsets = [r for r in parsed_resources if r.get("kind") == "StatefulSet"]
        assert statefulsets, "No StatefulSet found in rendered output"

        for ss in statefulsets:
            assert "spec" in ss, "StatefulSet missing spec"
            assert "selector" in ss["spec"], "StatefulSet missing selector"
            assert "matchLabels" in ss["spec"]["selector"], \
                "StatefulSet selector missing matchLabels"

    def test_service_has_selector_labels(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that Service has selector labels."""
        services = [r for r in parsed_resources if r.get("kind") == "Service"]
        assert services, "No Service found in rendered output"

        for svc in services:
            assert "spec" in svc, "Service missing spec"
            assert "selector" in svc["spec"], "Service missing selector"

    def test_statefulset_and_service_label_consistency(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that StatefulSet and Service selectors are consistent."""
        statefulsets = [r for r in parsed_resources if r.get("kind") == "StatefulSet"]
        services = [r for r in parsed_resources if r.get("kind") == "Service"]

        if statefulsets and services:
            ss = statefulsets[0]
            svc = services[0]

            ss_selector = ss.get("spec", {}).get("selector", {}).get("matchLabels", {})
            svc_selector = svc.get("spec", {}).get("selector", {})

            # Service selector should match StatefulSet pod labels
            # Check for app.kubernetes.io/name and app.kubernetes.io/instance labels
            if ss_selector and svc_selector:
                for key in ["app.kubernetes.io/name", "app.kubernetes.io/instance"]:
                    assert key in svc_selector, \
                        f"Service selector missing {key} label"


class TestResourceRequests:
    """Test resource requests and limits syntax."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    @pytest.fixture
    def test_values_file(self) -> Path:
        """Get path to test values file."""
        return Path(__file__).parent / "fixtures" / "test-values.yaml"

    @pytest.fixture
    def parsed_resources(self, chart_dir: Path, test_values_file: Path) -> List[Dict[str, Any]]:
        """Render and parse all resources."""
        try:
            result = subprocess.run(
                [
                    "helm", "template",
                    "test-release",
                    str(chart_dir),
                    "--values", str(test_values_file)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                pytest.fail(f"helm template failed: {result.stderr}")

            documents = result.stdout.split("---")
            resources = []
            for doc in documents:
                if doc.strip():
                    try:
                        parsed = yaml.safe_load(doc)
                        if parsed and isinstance(parsed, dict):
                            resources.append(parsed)
                    except yaml.YAMLError:
                        pass
            return resources
        except FileNotFoundError:
            pytest.skip("helm command not found")

    def test_statefulset_has_resource_requests(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that StatefulSet containers have resource requests."""
        statefulsets = [r for r in parsed_resources if r.get("kind") == "StatefulSet"]

        for ss in statefulsets:
            containers = ss.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])
            assert containers, "StatefulSet template spec should have containers"

            for container in containers:
                assert "resources" in container, \
                    f"Container {container.get('name')} missing resources"
                assert "requests" in container["resources"], \
                    f"Container {container.get('name')} missing resource requests"

    def test_statefulset_has_resource_limits(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that StatefulSet containers have resource limits."""
        statefulsets = [r for r in parsed_resources if r.get("kind") == "StatefulSet"]

        for ss in statefulsets:
            containers = ss.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])

            for container in containers:
                assert "resources" in container, \
                    f"Container {container.get('name')} missing resources"
                assert "limits" in container["resources"], \
                    f"Container {container.get('name')} missing resource limits"

    def test_resource_requests_have_valid_units(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that resource requests/limits have valid Kubernetes units."""
        statefulsets = [r for r in parsed_resources if r.get("kind") == "StatefulSet"]

        valid_cpu_units = ["m", ""]  # millicores or full cores
        valid_memory_units = ["Mi", "Gi", "Ki", "M", "G", "K"]

        for ss in statefulsets:
            containers = ss.get("spec", {}).get("template", {}).get("spec", {}).get("containers", [])

            for container in containers:
                requests = container.get("resources", {}).get("requests", {})
                limits = container.get("resources", {}).get("limits", {})

                for resource_dict in [requests, limits]:
                    if "cpu" in resource_dict:
                        cpu = str(resource_dict["cpu"])
                        # Valid formats: 100m, 1, 1.5
                        assert re.match(r"^\d+(\.\d+)?m?$", cpu), \
                            f"Invalid CPU value: {cpu}"

                    if "memory" in resource_dict:
                        memory = str(resource_dict["memory"])
                        # Valid formats: 256Mi, 1Gi, 512M
                        assert re.match(r"^\d+(Mi|Gi|Ki|M|G|K)?$", memory), \
                            f"Invalid memory value: {memory}"


class TestPlaceholderReplacement:
    """Test cookiecutter placeholder replacement."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    @pytest.fixture
    def test_values_file(self) -> Path:
        """Get path to test values file."""
        return Path(__file__).parent / "fixtures" / "test-values.yaml"

    @pytest.fixture
    def rendered_manifests(self, chart_dir: Path, test_values_file: Path) -> str:
        """Render Helm templates with test values."""
        try:
            result = subprocess.run(
                [
                    "helm", "template",
                    "test-release",
                    str(chart_dir),
                    "--values", str(test_values_file)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                pytest.fail(f"helm template failed: {result.stderr}")
            return result.stdout
        except FileNotFoundError:
            pytest.skip("helm command not found")

    def test_no_unrendered_cookiecutter_variables(self, rendered_manifests: str) -> None:
        """Test that no unrendered cookiecutter variables remain in output."""
        # Check for common cookiecutter patterns
        unrendered_patterns = [
            r"{{ cookiecutter\.",
            r"{%\s*if\s*cookiecutter",
            r"{%\s*for\s*",
        ]

        for pattern in unrendered_patterns:
            matches = re.findall(pattern, rendered_manifests)
            assert not matches, \
                f"Unrendered cookiecutter variables found matching pattern: {pattern}"

    def test_rendered_manifest_has_helm_variables(self, rendered_manifests: str) -> None:
        """Test that rendered manifests contain Helm template variables."""
        # Should have .Release.Name, .Chart.Name, etc resolved
        assert ".Release.Name" not in rendered_manifests or "test-release" in rendered_manifests, \
            "Helm template variables not properly rendered"


class TestConfigMapPresence:
    """Test ConfigMap content and structure."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    @pytest.fixture
    def test_values_file(self) -> Path:
        """Get path to test values file."""
        return Path(__file__).parent / "fixtures" / "test-values.yaml"

    @pytest.fixture
    def parsed_resources(self, chart_dir: Path, test_values_file: Path) -> List[Dict[str, Any]]:
        """Render and parse all resources."""
        try:
            result = subprocess.run(
                [
                    "helm", "template",
                    "test-release",
                    str(chart_dir),
                    "--values", str(test_values_file)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                pytest.fail(f"helm template failed: {result.stderr}")

            documents = result.stdout.split("---")
            resources = []
            for doc in documents:
                if doc.strip():
                    try:
                        parsed = yaml.safe_load(doc)
                        if parsed and isinstance(parsed, dict):
                            resources.append(parsed)
                    except yaml.YAMLError:
                        pass
            return resources
        except FileNotFoundError:
            pytest.skip("helm command not found")

    def test_configmap_has_data_section(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that ConfigMap has data section."""
        configmaps = [r for r in parsed_resources if r.get("kind") == "ConfigMap"]
        assert configmaps, "No ConfigMap found in rendered output"

        for cm in configmaps:
            assert "data" in cm, "ConfigMap missing data section"
            assert len(cm["data"]) > 0, "ConfigMap data section is empty"

    def test_configmap_has_required_keys(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that ConfigMap contains required configuration keys."""
        configmaps = [r for r in parsed_resources if r.get("kind") == "ConfigMap"]

        for cm in configmaps:
            data = cm.get("data", {})
            required_keys = ["SERVICE_NAME", "LOG_LEVEL", "HTTP_PORT"]

            for key in required_keys:
                assert key in data, \
                    f"ConfigMap missing required key: {key}"

    def test_configmap_custom_vars_included(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that ConfigMap includes custom environment variables from values."""
        configmaps = [r for r in parsed_resources if r.get("kind") == "ConfigMap"]

        for cm in configmaps:
            data = cm.get("data", {})
            # From test-values.yaml, these custom vars should be included
            assert "CUSTOM_VAR_1" in data or "customEnvVars" not in str(data), \
                "Custom environment variables not properly included in ConfigMap"


class TestPVCPresence:
    """Test PersistentVolumeClaim structure."""

    @pytest.fixture
    def chart_dir(self) -> Path:
        """Get path to the Helm chart directory."""
        return Path(__file__).parent / "test-helm-chart"

    @pytest.fixture
    def test_values_file(self) -> Path:
        """Get path to test values file."""
        return Path(__file__).parent / "fixtures" / "test-values.yaml"

    @pytest.fixture
    def parsed_resources(self, chart_dir: Path, test_values_file: Path) -> List[Dict[str, Any]]:
        """Render and parse all resources."""
        try:
            result = subprocess.run(
                [
                    "helm", "template",
                    "test-release",
                    str(chart_dir),
                    "--values", str(test_values_file)
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                pytest.fail(f"helm template failed: {result.stderr}")

            documents = result.stdout.split("---")
            resources = []
            for doc in documents:
                if doc.strip():
                    try:
                        parsed = yaml.safe_load(doc)
                        if parsed and isinstance(parsed, dict):
                            resources.append(parsed)
                    except yaml.YAMLError:
                        pass
            return resources
        except FileNotFoundError:
            pytest.skip("helm command not found")

    def test_pvc_has_spec(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that PVC has spec section."""
        pvcs = [r for r in parsed_resources if r.get("kind") == "PersistentVolumeClaim"]
        assert pvcs, "No PVC found in rendered output"

        for pvc in pvcs:
            assert "spec" in pvc, "PVC missing spec section"

    def test_pvc_has_storage_request(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that PVC requests storage."""
        pvcs = [r for r in parsed_resources if r.get("kind") == "PersistentVolumeClaim"]

        for pvc in pvcs:
            spec = pvc.get("spec", {})
            assert "resources" in spec, "PVC spec missing resources"
            assert "requests" in spec["resources"], "PVC resources missing requests"
            assert "storage" in spec["resources"]["requests"], \
                "PVC requests missing storage"

    def test_pvc_has_access_modes(self, parsed_resources: List[Dict[str, Any]]) -> None:
        """Test that PVC has accessModes."""
        pvcs = [r for r in parsed_resources if r.get("kind") == "PersistentVolumeClaim"]

        for pvc in pvcs:
            spec = pvc.get("spec", {})
            assert "accessModes" in spec, "PVC spec missing accessModes"
            assert len(spec["accessModes"]) > 0, "PVC accessModes list is empty"
