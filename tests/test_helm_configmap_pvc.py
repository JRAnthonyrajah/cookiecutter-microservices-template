"""Test suite for Helm ConfigMap and PersistentVolumeClaim templates."""
import re
import yaml
from pathlib import Path


class TestHelmConfigMapTemplate:
    """Tests for ConfigMap Helm template."""

    @classmethod
    def setup_class(cls):
        """Load the ConfigMap template."""
        template_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "configmap.yaml"
        )
        assert template_path.exists(), f"ConfigMap template not found at {template_path}"
        with open(template_path, "r") as f:
            cls.configmap_content = f.read()

    def test_configmap_file_exists(self):
        """Test that configmap.yaml file exists."""
        template_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "configmap.yaml"
        )
        assert template_path.exists(), "configmap.yaml template not found"

    def test_configmap_contains_api_version(self):
        """Test that ConfigMap has correct API version."""
        assert "apiVersion: v1" in self.configmap_content, "ConfigMap missing apiVersion"

    def test_configmap_contains_kind(self):
        """Test that ConfigMap specifies kind as ConfigMap."""
        assert "kind: ConfigMap" in self.configmap_content, "ConfigMap missing kind"

    def test_configmap_has_metadata_section(self):
        """Test that ConfigMap has metadata section with name and labels."""
        assert "metadata:" in self.configmap_content, "ConfigMap missing metadata section"
        assert "name:" in self.configmap_content, "ConfigMap metadata missing name"
        assert "labels:" in self.configmap_content, "ConfigMap metadata missing labels"

    def test_configmap_uses_include_for_name(self):
        """Test that ConfigMap uses include helper for name."""
        assert (
            '{{ include "{{ cookiecutter.service_slug }}.fullname"' in self.configmap_content
        ), "ConfigMap name should use fullname include"

    def test_configmap_uses_include_for_labels(self):
        """Test that ConfigMap uses include helper for labels."""
        assert (
            'include "{{ cookiecutter.service_slug }}.labels"' in self.configmap_content
        ), "ConfigMap labels should use labels include"

    def test_configmap_has_data_section(self):
        """Test that ConfigMap has data section."""
        assert "data:" in self.configmap_content, "ConfigMap missing data section"

    def test_configmap_contains_service_name(self):
        """Test that ConfigMap includes SERVICE_NAME environment variable."""
        assert (
            "SERVICE_NAME:" in self.configmap_content
        ), "ConfigMap data missing SERVICE_NAME"
        assert (
            ".Values.config.serviceName" in self.configmap_content
        ), "SERVICE_NAME should reference values.config.serviceName"

    def test_configmap_contains_log_level(self):
        """Test that ConfigMap includes LOG_LEVEL environment variable."""
        assert "LOG_LEVEL:" in self.configmap_content, "ConfigMap data missing LOG_LEVEL"
        assert (
            ".Values.config.logLevel" in self.configmap_content
        ), "LOG_LEVEL should reference values.config.logLevel"

    def test_configmap_contains_compression(self):
        """Test that ConfigMap includes COMPRESSION environment variable."""
        assert (
            "COMPRESSION:" in self.configmap_content
        ), "ConfigMap data missing COMPRESSION"
        assert (
            ".Values.config.compression" in self.configmap_content
        ), "COMPRESSION should reference values.config.compression"

    def test_configmap_contains_enable_metrics(self):
        """Test that ConfigMap includes ENABLE_METRICS environment variable."""
        assert (
            "ENABLE_METRICS:" in self.configmap_content
        ), "ConfigMap data missing ENABLE_METRICS"
        assert (
            ".Values.config.enableMetrics" in self.configmap_content
        ), "ENABLE_METRICS should reference values.config.enableMetrics"

    def test_configmap_contains_enable_tracing(self):
        """Test that ConfigMap includes ENABLE_TRACING environment variable."""
        assert (
            "ENABLE_TRACING:" in self.configmap_content
        ), "ConfigMap data missing ENABLE_TRACING"
        assert (
            ".Values.config.enableTracing" in self.configmap_content
        ), "ENABLE_TRACING should reference values.config.enableTracing"

    def test_configmap_contains_http_port(self):
        """Test that ConfigMap includes HTTP_PORT environment variable."""
        assert (
            "HTTP_PORT:" in self.configmap_content
        ), "ConfigMap data missing HTTP_PORT"
        assert (
            ".Values.config.httpPort" in self.configmap_content
        ), "HTTP_PORT should reference values.config.httpPort"

    def test_configmap_contains_health_check_interval(self):
        """Test that ConfigMap includes HEALTH_CHECK_INTERVAL environment variable."""
        assert (
            "HEALTH_CHECK_INTERVAL:" in self.configmap_content
        ), "ConfigMap data missing HEALTH_CHECK_INTERVAL"
        assert (
            ".Values.config.healthCheckInterval" in self.configmap_content
        ), "HEALTH_CHECK_INTERVAL should reference values.config.healthCheckInterval"

    def test_configmap_supports_custom_env_vars(self):
        """Test that ConfigMap supports custom environment variables."""
        assert (
            "customEnvVars" in self.configmap_content
        ), "ConfigMap should support custom environment variables"
        assert (
            "with .Values.config.customEnvVars" in self.configmap_content
        ), "ConfigMap should use 'with' to check for custom vars"

    def test_configmap_uses_namespace_from_release(self):
        """Test that ConfigMap uses Release.Namespace."""
        assert (
            ".Release.Namespace" in self.configmap_content
        ), "ConfigMap should use Release.Namespace"

    def test_configmap_quotes_values(self):
        """Test that ConfigMap quotes string values properly."""
        assert (
            "| quote" in self.configmap_content
        ), "ConfigMap should quote values using | quote filter"


class TestHelmPVCTemplate:
    """Tests for PersistentVolumeClaim Helm template."""

    @classmethod
    def setup_class(cls):
        """Load the PVC template."""
        template_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "pvc.yaml"
        )
        assert template_path.exists(), f"PVC template not found at {template_path}"
        with open(template_path, "r") as f:
            cls.pvc_content = f.read()

    def test_pvc_file_exists(self):
        """Test that pvc.yaml file exists."""
        template_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "pvc.yaml"
        )
        assert template_path.exists(), "pvc.yaml template not found"

    def test_pvc_contains_api_version(self):
        """Test that PVC has correct API version."""
        assert "apiVersion: v1" in self.pvc_content, "PVC missing apiVersion"

    def test_pvc_contains_kind(self):
        """Test that PVC specifies kind as PersistentVolumeClaim."""
        assert (
            "kind: PersistentVolumeClaim" in self.pvc_content
        ), "PVC missing correct kind"

    def test_pvc_has_metadata_section(self):
        """Test that PVC has metadata section."""
        assert "metadata:" in self.pvc_content, "PVC missing metadata section"
        assert "name:" in self.pvc_content, "PVC metadata missing name"
        assert "labels:" in self.pvc_content, "PVC metadata missing labels"

    def test_pvc_uses_include_for_name(self):
        """Test that PVC uses include helper for name."""
        assert (
            '{{ include "{{ cookiecutter.service_slug }}.fullname"' in self.pvc_content
        ), "PVC name should use fullname include"
        assert "-data" in self.pvc_content, "PVC name should include -data suffix"

    def test_pvc_uses_include_for_labels(self):
        """Test that PVC uses include helper for labels."""
        assert (
            'include "{{ cookiecutter.service_slug }}.labels"' in self.pvc_content
        ), "PVC labels should use labels include"

    def test_pvc_has_spec_section(self):
        """Test that PVC has spec section."""
        assert "spec:" in self.pvc_content, "PVC missing spec section"

    def test_pvc_has_access_modes(self):
        """Test that PVC specifies accessModes."""
        assert "accessModes:" in self.pvc_content, "PVC missing accessModes"
        assert (
            "ReadWriteOnce" in self.pvc_content
        ), "PVC should have ReadWriteOnce access mode"

    def test_pvc_has_storage_class_name(self):
        """Test that PVC specifies storageClassName."""
        assert (
            "storageClassName:" in self.pvc_content
        ), "PVC missing storageClassName"
        assert (
            ".Values.persistence.storageClassName" in self.pvc_content
        ), "PVC should reference values.persistence.storageClassName"

    def test_pvc_has_storage_resources(self):
        """Test that PVC specifies storage resources."""
        assert "resources:" in self.pvc_content, "PVC missing resources section"
        assert "requests:" in self.pvc_content, "PVC missing requests section"
        assert "storage:" in self.pvc_content, "PVC missing storage request"

    def test_pvc_storage_size_configurable(self):
        """Test that PVC storage size is configurable via values."""
        assert (
            ".Values.persistence.size" in self.pvc_content
        ), "PVC storage size should reference values.persistence.size"

    def test_pvc_uses_release_namespace(self):
        """Test that PVC uses Release.Namespace."""
        assert (
            ".Release.Namespace" in self.pvc_content
        ), "PVC should use Release.Namespace"

    def test_pvc_quotes_string_values(self):
        """Test that PVC quotes string values properly."""
        assert (
            "| quote" in self.pvc_content
        ), "PVC should quote values using | quote filter"


class TestHelmTemplatesIntegration:
    """Integration tests for ConfigMap and PVC templates."""

    def test_both_templates_exist(self):
        """Test that both ConfigMap and PVC templates exist."""
        configmap_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "configmap.yaml"
        )
        pvc_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "pvc.yaml"
        )
        assert configmap_path.exists(), "ConfigMap template not found"
        assert pvc_path.exists(), "PVC template not found"

    def test_both_templates_use_consistent_naming(self):
        """Test that both templates use consistent naming patterns."""
        configmap_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "configmap.yaml"
        )
        pvc_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "pvc.yaml"
        )
        with open(configmap_path, "r") as f:
            configmap = f.read()
        with open(pvc_path, "r") as f:
            pvc = f.read()

        # Both should use the same fullname helper
        assert (
            '{{ include "{{ cookiecutter.service_slug }}.fullname"' in configmap
        ), "ConfigMap should use fullname helper"
        assert (
            '{{ include "{{ cookiecutter.service_slug }}.fullname"' in pvc
        ), "PVC should use fullname helper"

        # Both should use the same labels helper
        assert (
            'include "{{ cookiecutter.service_slug }}.labels"' in configmap
        ), "ConfigMap should use labels helper"
        assert (
            'include "{{ cookiecutter.service_slug }}.labels"' in pvc
        ), "PVC should use labels helper"

    def test_templates_directory_structure(self):
        """Test that templates directory has proper structure."""
        templates_dir = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
        )
        assert templates_dir.exists(), "templates directory not found"
        assert templates_dir.is_dir(), "templates should be a directory"

        # Verify both templates are present
        files = list(templates_dir.glob("*.yaml"))
        file_names = {f.name for f in files}
        assert "configmap.yaml" in file_names, "configmap.yaml not found in templates"
        assert "pvc.yaml" in file_names, "pvc.yaml not found in templates"
