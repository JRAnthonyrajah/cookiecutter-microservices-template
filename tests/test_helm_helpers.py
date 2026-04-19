"""Test suite for Helm helpers template validation."""
import re
from pathlib import Path


class TestHelmHelpersTemplate:
    """Tests for Helm _helpers.tpl template validity and helper function definitions."""

    @classmethod
    def setup_class(cls):
        """Load the _helpers.tpl template."""
        helpers_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "_helpers.tpl"
        )
        assert helpers_path.exists(), f"_helpers.tpl not found at {helpers_path}"
        with open(helpers_path, "r") as f:
            cls.helpers_content = f.read()

    def test_helpers_tpl_file_exists(self):
        """Test that _helpers.tpl file exists in templates directory."""
        helpers_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
            / "_helpers.tpl"
        )
        assert helpers_path.exists(), f"_helpers.tpl not found at {helpers_path}"
        assert helpers_path.is_file(), f"_helpers.tpl is not a regular file at {helpers_path}"

    def test_helpers_tpl_is_not_empty(self):
        """Test that _helpers.tpl is not empty."""
        assert len(self.helpers_content) > 0, "_helpers.tpl file is empty"

    def test_chart_name_helper_defined(self):
        """Test that chart.name helper function is defined."""
        assert 'define "chart.name"' in self.helpers_content, \
            'Helper function chart.name must be defined with {{- define "chart.name" -}}'

    def test_chart_fullname_helper_defined(self):
        """Test that chart.fullname helper function is defined."""
        assert 'define "chart.fullname"' in self.helpers_content, \
            'Helper function chart.fullname must be defined with {{- define "chart.fullname" -}}'

    def test_chart_chart_helper_defined(self):
        """Test that chart.chart helper function is defined."""
        assert 'define "chart.chart"' in self.helpers_content, \
            'Helper function chart.chart must be defined with {{- define "chart.chart" -}}'

    def test_chart_labels_helper_defined(self):
        """Test that chart.labels helper function is defined."""
        assert 'define "chart.labels"' in self.helpers_content, \
            'Helper function chart.labels must be defined with {{- define "chart.labels" -}}'

    def test_chart_selectorlabels_helper_defined(self):
        """Test that chart.selectorLabels helper function is defined."""
        assert 'define "chart.selectorLabels"' in self.helpers_content, \
            'Helper function chart.selectorLabels must be defined with {{- define "chart.selectorLabels" -}}'

    def test_chart_serviceaccountname_helper_defined(self):
        """Test that chart.serviceAccountName helper function is defined."""
        assert 'define "chart.serviceAccountName"' in self.helpers_content, \
            'Helper function chart.serviceAccountName must be defined'

    def test_labels_macro_includes_chart_label(self):
        """Test that labels macro includes helm.sh/chart label."""
        assert "helm.sh/chart:" in self.helpers_content, \
            "Labels macro must include helm.sh/chart label"

    def test_labels_macro_includes_app_kubernetes_label(self):
        """Test that labels macro includes app.kubernetes.io/version label."""
        assert "app.kubernetes.io/version:" in self.helpers_content, \
            "Labels macro must include app.kubernetes.io/version label"

    def test_labels_macro_includes_managed_by_label(self):
        """Test that labels macro includes app.kubernetes.io/managed-by label."""
        assert "app.kubernetes.io/managed-by:" in self.helpers_content, \
            "Labels macro must include app.kubernetes.io/managed-by label"

    def test_selectorlabels_includes_app_kubernetes_name(self):
        """Test that selectorLabels macro includes app.kubernetes.io/name label."""
        assert "app.kubernetes.io/name:" in self.helpers_content, \
            "selectorLabels macro must include app.kubernetes.io/name label"

    def test_selectorlabels_includes_app_kubernetes_instance(self):
        """Test that selectorLabels macro includes app.kubernetes.io/instance label."""
        assert "app.kubernetes.io/instance:" in self.helpers_content, \
            "selectorLabels macro must include app.kubernetes.io/instance label"

    def test_fullname_uses_release_name(self):
        """Test that fullname helper uses .Release.Name."""
        assert ".Release.Name" in self.helpers_content, \
            "fullname helper must use .Release.Name from Helm context"

    def test_fullname_uses_chart_name(self):
        """Test that fullname helper uses .Chart.Name."""
        assert ".Chart.Name" in self.helpers_content, \
            "fullname helper must use .Chart.Name from Helm context"

    def test_chart_helper_uses_chart_version(self):
        """Test that chart helper uses .Chart.Version."""
        assert ".Chart.Version" in self.helpers_content, \
            "chart helper must use .Chart.Version from Helm context"

    def test_helpers_have_end_statements(self):
        """Test that all define blocks have corresponding end statements."""
        define_count = self.helpers_content.count("{{- define")
        # Count both "{{- end }}" and "{{ end }}" since Helm accepts both
        end_count = self.helpers_content.count("{{- end }}") + self.helpers_content.count("{{ end }}")
        assert define_count <= end_count, \
            f"More define blocks than end statements: {define_count} defines vs {end_count} ends"

    def test_helpers_have_proper_helm_syntax(self):
        """Test that helpers use proper Helm template syntax."""
        # Check for proper whitespace control markers
        assert "{{-" in self.helpers_content, "Helpers should use {{- for whitespace control"
        assert "-}}" in self.helpers_content, "Helpers should use -}} for whitespace control"

    def test_helpers_include_comments(self):
        """Test that helpers include documentation comments."""
        assert "{{/*" in self.helpers_content, "Helpers should include comment blocks"
        assert "*/}}" in self.helpers_content, "Helpers should properly close comment blocks"

    def test_include_function_used_in_labels(self):
        """Test that labels helper includes selectorLabels using include function."""
        assert "include \"chart.selectorLabels\"" in self.helpers_content, \
            "labels helper must include selectorLabels using include function"

    def test_serviceaccountname_checks_create_flag(self):
        """Test that serviceAccountName helper checks serviceAccount.create flag."""
        assert ".Values.serviceAccount.create" in self.helpers_content, \
            "serviceAccountName helper must check serviceAccount.create flag"

    def test_templates_directory_exists(self):
        """Test that templates directory exists in helm chart."""
        templates_dir = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "helm"
            / "templates"
        )
        assert templates_dir.exists(), f"templates directory not found at {templates_dir}"
        assert templates_dir.is_dir(), f"templates path is not a directory at {templates_dir}"

    def test_no_hardcoded_values_in_helpers(self):
        """Test that helpers do not contain hardcoded values (use template vars)."""
        # Check that specific hardcoded values that should be dynamic are not present
        # (we allow some like label names, but not service names, versions, etc.)
        forbidden_patterns = [
            r"my[_-]service",  # Hardcoded service name
            r"v[\d.]+\"",      # Hardcoded version
        ]
        for pattern in forbidden_patterns:
            matches = re.findall(pattern, self.helpers_content, re.IGNORECASE)
            assert not matches, \
                f"Helpers should not contain hardcoded values matching pattern: {pattern}"

    def test_labels_consistency_between_labels_and_selectorlabels(self):
        """Test that selectorLabels is a subset of labels (semantic check)."""
        # Extract label definitions from both helpers
        labels_section = self.helpers_content[
            self.helpers_content.find('define "chart.labels"'):
            self.helpers_content.find('{{- end }}', self.helpers_content.find('define "chart.labels"'))
        ]
        selector_section = self.helpers_content[
            self.helpers_content.find('define "chart.selectorLabels"'):
            self.helpers_content.find('{{- end }}', self.helpers_content.find('define "chart.selectorLabels"'))
        ]

        # selectorLabels should directly reference app.kubernetes.io/name and instance
        assert "app.kubernetes.io/name:" in selector_section, \
            "chart.selectorLabels should include app.kubernetes.io/name"
        assert "app.kubernetes.io/instance:" in selector_section, \
            "chart.selectorLabels should include app.kubernetes.io/instance"

        # labels should include selectorLabels via include function (not direct duplication)
        assert "include \"chart.selectorLabels\"" in labels_section, \
            "chart.labels should include selectorLabels via include function"

    def test_fullname_truncation(self):
        """Test that fullname helper includes truncation logic."""
        assert "trunc 63" in self.helpers_content, \
            "fullname helper should truncate names to 63 characters for DNS compliance"

    def test_fullname_suffix_trimming(self):
        """Test that fullname helper trims trailing dashes."""
        assert "trimSuffix" in self.helpers_content, \
            "fullname helper should trim trailing dashes for valid DNS names"
