"""Test suite for Helm Chart.yaml template validation."""
import re
import yaml
from pathlib import Path


class TestHelmChartYAML:
    """Tests for Helm Chart.yaml template validity and structure."""

    @classmethod
    def setup_class(cls):
        """Load the Chart.yaml template."""
        chart_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "Chart.yaml"
        assert chart_path.exists(), f"Chart.yaml not found at {chart_path}"
        with open(chart_path, "r") as f:
            cls.chart_content = f.read()

    def test_chart_yaml_file_exists(self):
        """Test that Chart.yaml file exists."""
        chart_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "Chart.yaml"
        assert chart_path.exists(), f"Chart.yaml file not found at {chart_path}"
        assert chart_path.is_file(), f"Chart.yaml is not a regular file at {chart_path}"

    def test_chart_yaml_is_not_empty(self):
        """Test that Chart.yaml is not empty."""
        assert len(self.chart_content) > 0, "Chart.yaml file is empty"

    def test_api_version_v2_declared(self):
        """Test that apiVersion: v2 is declared."""
        assert "apiVersion: v2" in self.chart_content, "Chart.yaml must declare apiVersion: v2"

    def test_chart_type_is_application(self):
        """Test that chart type is 'application'."""
        assert "type: application" in self.chart_content, \
            "Chart.yaml must declare type: application"

    def test_name_uses_cookiecutter_placeholder(self):
        """Test that name field uses {{ cookiecutter.service_slug }} placeholder."""
        assert "name: {{ cookiecutter.service_slug }}" in self.chart_content, \
            "name field must use {{ cookiecutter.service_slug }} placeholder"

    def test_version_uses_cookiecutter_placeholder(self):
        """Test that version field uses {{ cookiecutter.version }} placeholder."""
        assert "version: {{ cookiecutter.version }}" in self.chart_content, \
            "version field must use {{ cookiecutter.version }} placeholder"

    def test_appversion_uses_cookiecutter_placeholder(self):
        """Test that appVersion field uses {{ cookiecutter.version }} placeholder."""
        assert "appVersion: {{ cookiecutter.version }}" in self.chart_content, \
            "appVersion field must use {{ cookiecutter.version }} placeholder"

    def test_description_uses_cookiecutter_placeholder(self):
        """Test that description field uses {{ cookiecutter.service_name }} placeholder."""
        assert "{{ cookiecutter.service_name }}" in self.chart_content, \
            "description field must use {{ cookiecutter.service_name }} placeholder"

    def test_maintainers_section_exists(self):
        """Test that maintainers section is present."""
        assert "maintainers:" in self.chart_content, "Chart must have a maintainers section"

    def test_maintainers_have_name_field(self):
        """Test that maintainers have name field."""
        assert "- name: {{ cookiecutter.author }}" in self.chart_content, \
            "maintainers must have name field with {{ cookiecutter.author }} placeholder"

    def test_maintainers_have_email_field(self):
        """Test that maintainers have email field."""
        assert "email: {{ cookiecutter.email }}" in self.chart_content, \
            "maintainers must have email field with {{ cookiecutter.email }} placeholder"

    def test_maintainers_use_cookiecutter_placeholders(self):
        """Test that maintainers use {{ cookiecutter.* }} placeholders."""
        assert "{{ cookiecutter.author }}" in self.chart_content, \
            "maintainers.name must use {{ cookiecutter.author }} placeholder"
        assert "{{ cookiecutter.email }}" in self.chart_content, \
            "maintainers.email must use {{ cookiecutter.email }} placeholder"

    def test_dependencies_section_exists(self):
        """Test that dependencies section is present."""
        assert "dependencies:" in self.chart_content, "Chart must have a dependencies section"

    def test_zookeeper_dependency_present(self):
        """Test that Bitnami Zookeeper dependency is configured."""
        assert "- name: zookeeper" in self.chart_content, \
            "Zookeeper dependency must be present in dependencies"

    def test_zookeeper_uses_bitnami_repository(self):
        """Test that Zookeeper uses Bitnami repository."""
        assert 'repository: "https://charts.bitnami.com/bitnami"' in self.chart_content, \
            "Zookeeper must use Bitnami repository URL"

    def test_zookeeper_dependency_has_version(self):
        """Test that Zookeeper dependency has a version specified."""
        assert 'version: "14.x.x"' in self.chart_content, \
            "Zookeeper dependency must have a version field"

    def test_zookeeper_dependency_has_condition(self):
        """Test that Zookeeper dependency has a condition for optional enablement."""
        assert "condition: zookeeper.enabled" in self.chart_content, \
            "Zookeeper dependency must have condition: zookeeper.enabled"

    def test_zookeeper_dependency_has_alias(self):
        """Test that Zookeeper dependency has an alias."""
        assert "alias: zk" in self.chart_content, \
            "Zookeeper dependency must have alias: zk"

    def test_keywords_section_exists(self):
        """Test that keywords section is present."""
        assert "keywords:" in self.chart_content, "Chart must have a keywords section"
        assert "- microservice" in self.chart_content, "keywords must include 'microservice'"
        assert "- kubernetes" in self.chart_content, "keywords must include 'kubernetes'"

    def test_chart_has_home_metadata(self):
        """Test that chart has home metadata."""
        assert "home:" in self.chart_content, "Chart must have a 'home' field"

    def test_chart_has_sources_metadata(self):
        """Test that chart has sources metadata."""
        assert "sources:" in self.chart_content, "Chart must have a 'sources' field"

    def test_all_placeholders_are_valid(self):
        """Test that all {{ cookiecutter.* }} placeholders are valid variable names."""
        placeholder_pattern = r"\{\{\s*cookiecutter\.(\w+)\s*\}\}"
        placeholders = re.findall(placeholder_pattern, self.chart_content)

        valid_vars = {"service_slug", "service_name", "version", "author", "email"}
        for placeholder_var in placeholders:
            assert placeholder_var in valid_vars, \
                f"Unknown placeholder variable: cookiecutter.{placeholder_var}"

    def test_helm_chart_directory_structure(self):
        """Test that helm directory has correct structure."""
        helm_dir = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm"
        assert helm_dir.exists(), f"helm directory not found at {helm_dir}"
        assert helm_dir.is_dir(), f"helm path is not a directory at {helm_dir}"
        assert (helm_dir / "Chart.yaml").exists(), "Chart.yaml must exist in helm directory"

    def test_yaml_structure_can_be_loaded_after_placeholder_resolution(self):
        """Test that Chart.yaml can be loaded as valid YAML after placeholder resolution."""
        # Create a test version with placeholders resolved
        test_content = self.chart_content.replace("{{ cookiecutter.service_slug }}", "my_service")
        test_content = test_content.replace("{{ cookiecutter.service_name }}", "My Service")
        test_content = test_content.replace("{{ cookiecutter.version }}", "0.1.0")
        test_content = test_content.replace("{{ cookiecutter.author }}", "Test Author")
        test_content = test_content.replace("{{ cookiecutter.email }}", "test@example.com")

        try:
            chart = yaml.safe_load(test_content)
            assert isinstance(chart, dict), "Resolved Chart.yaml should be a YAML dictionary"
            assert chart.get("apiVersion") == "v2", "apiVersion should be v2"
            assert chart.get("name") == "my_service", "name should resolve correctly"
            assert chart.get("type") == "application", "type should be application"
        except yaml.YAMLError as e:
            raise AssertionError(f"Resolved Chart.yaml contains invalid YAML syntax: {e}")
