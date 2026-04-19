"""Test suite for Helm Service template validation."""
from pathlib import Path


class TestHelmServiceTemplate:
    """Tests for Helm Service template."""

    @classmethod
    def setup_class(cls):
        """Load the service.yaml template."""
        service_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "service.yaml"
        assert service_path.exists(), f"service.yaml not found at {service_path}"
        with open(service_path, "r") as f:
            cls.template_content = f.read()

    def test_service_file_exists(self):
        """Test that service.yaml template file exists."""
        service_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "service.yaml"
        assert service_path.exists(), f"service.yaml not found at {service_path}"
        assert service_path.is_file(), f"service.yaml is not a file"

    def test_service_kind_is_service(self):
        """Test that the kind is set to Service."""
        assert "kind: Service" in self.template_content, "kind: Service not found in template"

    def test_service_apiversion_is_v1(self):
        """Test that apiVersion is set to v1."""
        assert "apiVersion: v1" in self.template_content, "apiVersion: v1 not found in template"

    def test_service_has_metadata_section(self):
        """Test that service has metadata section with name and labels."""
        assert "metadata:" in self.template_content, "metadata section not found"
        assert "name:" in self.template_content, "metadata.name not found"
        assert "labels:" in self.template_content, "metadata.labels not found"

    def test_service_has_spec_section(self):
        """Test that service has spec section with type and selector."""
        assert "spec:" in self.template_content, "spec section not found"
        assert "type:" in self.template_content, "spec.type not found"
        assert "selector:" in self.template_content, "spec.selector not found"

    def test_service_selector_labels_present(self):
        """Test that selector includes selectorLabels helper."""
        assert "selector:" in self.template_content, "selector section missing"
        assert "include \"service.selectorLabels\"" in self.template_content, "selectorLabels helper call missing"

    def test_service_has_port_configuration(self):
        """Test that service has port configuration."""
        assert "port:" in self.template_content, "port configuration missing"
        assert "targetPort:" in self.template_content, "targetPort configuration missing"
        assert "protocol:" in self.template_content, "protocol configuration missing"
        assert "name:" in self.template_content, "portName configuration missing"

    def test_service_supports_clusterip_type(self):
        """Test that service supports ClusterIP type from values."""
        assert ".Values.service.type" in self.template_content, "Values reference for service type missing"
        assert "default \"ClusterIP\"" in self.template_content, "ClusterIP default type missing"

    def test_service_supports_headless_mode(self):
        """Test that service supports headless mode with clusterIP: None."""
        assert "eq .Values.service.type \"Headless\"" in self.template_content, "Headless mode conditional missing"
        assert "clusterIP: None" in self.template_content, "clusterIP: None for headless mode missing"

    def test_service_port_configurable(self):
        """Test that service port is configurable from values."""
        assert ".Values.service.port" in self.template_content, "Values reference for port missing"
        assert "default 8080" in self.template_content, "Default port value missing"

    def test_service_target_port_configurable(self):
        """Test that service targetPort is configurable from values."""
        assert ".Values.service.targetPort" in self.template_content, "Values reference for targetPort missing"
        assert "default 8080" in self.template_content, "Default targetPort value missing"

    def test_service_protocol_configurable(self):
        """Test that service protocol is configurable from values."""
        assert ".Values.service.protocol" in self.template_content, "Values reference for protocol missing"
        assert "default \"TCP\"" in self.template_content, "Default protocol value missing"

    def test_service_session_affinity_optional(self):
        """Test that sessionAffinity is optional and conditional."""
        assert "sessionAffinity:" in self.template_content, "sessionAffinity configuration missing"
        assert "if .Values.service.sessionAffinity" in self.template_content, "sessionAffinity conditional missing"

    def test_service_uses_helpers_template(self):
        """Test that service template uses _helpers.tpl functions."""
        assert "include \"service.fullname\"" in self.template_content, "service.fullname helper missing"
        assert "include \"service.labels\"" in self.template_content, "service.labels helper missing"
        assert "include \"service.selectorLabels\"" in self.template_content, "service.selectorLabels helper missing"

    def test_helpers_template_exists(self):
        """Test that _helpers.tpl exists."""
        helpers_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "_helpers.tpl"
        assert helpers_path.exists(), f"_helpers.tpl not found at {helpers_path}"
        assert helpers_path.is_file(), f"_helpers.tpl is not a file"

    def test_helpers_has_service_name_define(self):
        """Test that _helpers.tpl defines chart.name."""
        helpers_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "_helpers.tpl"
        with open(helpers_path, "r") as f:
            helpers_content = f.read()
        assert 'define "chart.name"' in helpers_content, 'chart.name definition missing'

    def test_helpers_has_fullname_define(self):
        """Test that _helpers.tpl defines chart.fullname."""
        helpers_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "_helpers.tpl"
        with open(helpers_path, "r") as f:
            helpers_content = f.read()
        assert 'define "chart.fullname"' in helpers_content, 'chart.fullname definition missing'

    def test_helpers_has_selector_labels_define(self):
        """Test that _helpers.tpl defines chart.selectorLabels."""
        helpers_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "_helpers.tpl"
        with open(helpers_path, "r") as f:
            helpers_content = f.read()
        assert 'define "chart.selectorLabels"' in helpers_content, 'chart.selectorLabels definition missing'

    def test_helpers_has_labels_define(self):
        """Test that _helpers.tpl defines chart.labels."""
        helpers_path = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}" / "helm" / "templates" / "_helpers.tpl"
        with open(helpers_path, "r") as f:
            helpers_content = f.read()
        assert 'define "chart.labels"' in helpers_content, 'chart.labels definition missing'

    def test_service_port_uses_tcp_protocol(self):
        """Test that service port protocol defaults to TCP."""
        assert "TCP" in self.template_content, "TCP protocol reference missing"

    def test_service_metadata_uses_helpers(self):
        """Test that service metadata labels use labels helper."""
        assert "labels:" in self.template_content, "metadata.labels section missing"
        assert "| nindent 4" in self.template_content, "nindent formatting for labels missing"

    def test_clusterip_headless_mode_conditional(self):
        """Test conditional logic for headless vs ClusterIP mode."""
        assert "if eq" in self.template_content, "Conditional check for service type missing"
        assert "Headless" in self.template_content, "Headless service type reference missing"

    def test_service_ports_array_structure(self):
        """Test that service has proper ports array structure."""
        assert "ports:" in self.template_content, "ports array missing"
        assert "- port:" in self.template_content, "port array item missing"

    def test_service_helm_metadata_naming(self):
        """Test that service uses Helm naming conventions."""
        assert "include \"service.fullname\"" in self.template_content, "fullname helper for metadata.name missing"
