"""Test suite for ArgoCD ApplicationSet template validation."""
import re
import yaml
from pathlib import Path


class TestArgocdApplicationSetYAML:
    """Tests for ArgoCD ApplicationSet template validity and structure."""

    @classmethod
    def setup_class(cls):
        """Load the ApplicationSet YAML template."""
        appset_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "argocd"
            / "applicationset.yaml"
        )
        assert appset_path.exists(), f"applicationset.yaml not found at {appset_path}"
        with open(appset_path, "r") as f:
            cls.appset_content = f.read()

    def test_applicationset_yaml_file_exists(self):
        """Test that applicationset.yaml file exists."""
        appset_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "argocd"
            / "applicationset.yaml"
        )
        assert appset_path.exists(), f"applicationset.yaml file not found at {appset_path}"
        assert appset_path.is_file(), f"applicationset.yaml is not a regular file at {appset_path}"

    def test_argocd_directory_exists(self):
        """Test that argocd directory exists."""
        argocd_dir = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / "argocd"
        )
        assert argocd_dir.exists(), f"argocd directory not found at {argocd_dir}"
        assert argocd_dir.is_dir(), f"argocd path is not a directory at {argocd_dir}"

    def test_applicationset_yaml_is_not_empty(self):
        """Test that applicationset.yaml is not empty."""
        assert len(self.appset_content) > 0, "applicationset.yaml file is empty"

    def test_api_version_argoproj_v1alpha1_declared(self):
        """Test that apiVersion: argoproj.io/v1alpha1 is declared."""
        assert "apiVersion: argoproj.io/v1alpha1" in self.appset_content, \
            "ApplicationSet must declare apiVersion: argoproj.io/v1alpha1"

    def test_kind_applicationset_declared(self):
        """Test that kind: ApplicationSet is declared."""
        assert "kind: ApplicationSet" in self.appset_content, \
            "Kind must be ApplicationSet"

    def test_metadata_name_uses_cookiecutter_placeholder(self):
        """Test that metadata.name uses {{ cookiecutter.service_slug }} placeholder."""
        assert "name: {{ cookiecutter.service_slug }}" in self.appset_content, \
            "metadata.name must use {{ cookiecutter.service_slug }} placeholder"

    def test_metadata_namespace_is_argocd(self):
        """Test that metadata.namespace is 'argocd'."""
        assert "namespace: argocd" in self.appset_content, \
            "metadata.namespace must be set to argocd"

    def test_generators_section_exists(self):
        """Test that generators section is present."""
        assert "generators:" in self.appset_content, \
            "ApplicationSet must have a generators section"

    def test_generators_has_list_type(self):
        """Test that generators uses list generator type."""
        assert "- list:" in self.appset_content, \
            "generators must use list generator type"

    def test_generators_has_elements_section(self):
        """Test that generators.list has elements section."""
        assert "elements:" in self.appset_content, \
            "list generator must have elements section"

    def test_dev_environment_in_generators(self):
        """Test that dev environment is in generators elements."""
        assert "- name: dev" in self.appset_content, \
            "dev environment must be present in generators"
        assert "{{ cookiecutter.service_slug }}-dev" in self.appset_content, \
            "dev namespace must be based on service_slug"

    def test_staging_environment_in_generators(self):
        """Test that staging environment is in generators elements."""
        assert "- name: staging" in self.appset_content, \
            "staging environment must be present in generators"
        assert "{{ cookiecutter.service_slug }}-staging" in self.appset_content, \
            "staging namespace must be based on service_slug"

    def test_prod_environment_in_generators(self):
        """Test that prod environment is in generators elements."""
        assert "- name: prod" in self.appset_content, \
            "prod environment must be present in generators"
        assert "{{ cookiecutter.service_slug }}-prod" in self.appset_content, \
            "prod namespace must be based on service_slug"

    def test_template_section_exists(self):
        """Test that template section is present."""
        assert "template:" in self.appset_content, \
            "ApplicationSet must have a template section"

    def test_template_spec_section_exists(self):
        """Test that template.spec section exists."""
        assert "spec:" in self.appset_content, \
            "template must have a spec section"

    def test_project_is_default(self):
        """Test that project is set to 'default'."""
        assert "project: default" in self.appset_content, \
            "ApplicationSet must use default project"

    def test_source_section_exists(self):
        """Test that source section exists in spec."""
        assert "source:" in self.appset_content, \
            "spec must have a source section"

    def test_source_has_repourl(self):
        """Test that source has repoURL."""
        assert "repoURL:" in self.appset_content, \
            "source must have repoURL field"

    def test_source_has_path(self):
        """Test that source has path pointing to helm directory."""
        assert "path: \"helm\"" in self.appset_content, \
            "source.path must point to helm directory"

    def test_source_has_targetrevision(self):
        """Test that source has targetRevision."""
        assert "targetRevision: HEAD" in self.appset_content, \
            "source must have targetRevision set to HEAD"

    def test_destination_section_exists(self):
        """Test that destination section exists in spec."""
        assert "destination:" in self.appset_content, \
            "spec must have a destination section"

    def test_destination_server_is_configured(self):
        """Test that destination has server configuration."""
        assert "server:" in self.appset_content, \
            "destination must have server field"

    def test_destination_namespace_is_configurable(self):
        """Test that destination namespace is set from generator element."""
        assert "{{ '{{' }}element.namespace{{ '}}' }}" in self.appset_content, \
            "destination.namespace must be templated from element.namespace"

    def test_syncopolicy_section_exists(self):
        """Test that syncPolicy section exists."""
        assert "syncPolicy:" in self.appset_content, \
            "spec must have a syncPolicy section"

    def test_syncopolicy_automated_section_exists(self):
        """Test that automated sync policy is configured."""
        assert "automated:" in self.appset_content, \
            "syncPolicy must have automated section"

    def test_syncopolicy_automated_prune_enabled(self):
        """Test that auto-prune is enabled."""
        assert "prune: true" in self.appset_content, \
            "syncPolicy.automated.prune must be true"

    def test_syncopolicy_automated_selfheal_enabled(self):
        """Test that selfHeal is enabled."""
        assert "selfHeal: true" in self.appset_content, \
            "syncPolicy.automated.selfHeal must be true"

    def test_syncopolicy_retry_section_exists(self):
        """Test that retry section exists in syncPolicy."""
        assert "retry:" in self.appset_content, \
            "syncPolicy must have retry section"

    def test_retry_limit_is_five(self):
        """Test that retry limit is set to 5."""
        assert "limit: 5" in self.appset_content, \
            "retry.limit must be set to 5"

    def test_retry_backoff_section_exists(self):
        """Test that retry backoff configuration exists."""
        assert "backoff:" in self.appset_content, \
            "retry must have backoff section"

    def test_retry_backoff_initial_duration(self):
        """Test that backoff initial duration is 5s."""
        assert "duration: 5s" in self.appset_content, \
            "retry.backoff.duration must be 5s"

    def test_retry_backoff_max_duration_is_three_minutes(self):
        """Test that backoff max duration is 3m."""
        assert "maxDuration: 3m" in self.appset_content, \
            "retry.backoff.maxDuration must be 3m"

    def test_retry_backoff_has_exponential_factor(self):
        """Test that backoff has exponential factor."""
        assert "factor: 2" in self.appset_content, \
            "retry.backoff.factor must be 2 for exponential backoff"

    def test_ignoredifferences_section_exists(self):
        """Test that ignoreDifferences section exists."""
        assert "ignoreDifferences:" in self.appset_content, \
            "spec must have ignoreDifferences section"

    def test_ignoredifferences_has_pvc_entry(self):
        """Test that ignoreDifferences includes PersistentVolumeClaim."""
        assert "kind: PersistentVolumeClaim" in self.appset_content, \
            "ignoreDifferences must include PersistentVolumeClaim entries"
        assert "group: v1" in self.appset_content, \
            "PVC ignoreDifferences must specify group: v1"

    def test_ignoredifferences_has_statefulset_entry(self):
        """Test that ignoreDifferences includes StatefulSet."""
        assert "kind: StatefulSet" in self.appset_content, \
            "ignoreDifferences must include StatefulSet entries"
        assert "group: apps" in self.appset_content, \
            "StatefulSet ignoreDifferences must specify group: apps"

    def test_ignoredifferences_uses_jsonpointers(self):
        """Test that ignoreDifferences uses jsonPointers for ignoring fields."""
        assert "jsonPointers:" in self.appset_content, \
            "ignoreDifferences must use jsonPointers field"

    def test_syncoptions_section_exists(self):
        """Test that syncOptions section exists."""
        assert "syncOptions:" in self.appset_content, \
            "syncPolicy must have syncOptions section"

    def test_syncoptions_has_createnamespace(self):
        """Test that syncOptions includes CreateNamespace."""
        assert "CreateNamespace=true" in self.appset_content, \
            "syncOptions must include CreateNamespace=true"

    def test_template_metadata_section_exists(self):
        """Test that template.metadata section exists."""
        assert "metadata:" in self.appset_content, \
            "template must have metadata section"

    def test_all_placeholders_are_valid(self):
        """Test that all {{ cookiecutter.* }} placeholders are valid variable names."""
        placeholder_pattern = r"\{\{\s*cookiecutter\.(\w+)\s*\}\}"
        placeholders = re.findall(placeholder_pattern, self.appset_content)

        valid_vars = {"service_slug", "repo_url"}
        for placeholder_var in placeholders:
            assert placeholder_var in valid_vars, \
                f"Unknown placeholder variable: cookiecutter.{placeholder_var}"

    def test_yaml_structure_is_valid_after_placeholder_resolution(self):
        """Test that ApplicationSet YAML is valid after placeholder resolution."""
        test_content = self.appset_content.replace("{{ cookiecutter.service_slug }}", "my_service")
        test_content = test_content.replace("{{ cookiecutter.repo_url | default('https://github.com') }}", "https://github.com/example/my_service")

        try:
            appset = yaml.safe_load(test_content)
            assert isinstance(appset, dict), "Resolved ApplicationSet should be a YAML dictionary"
            assert appset.get("apiVersion") == "argoproj.io/v1alpha1", "apiVersion should be correct"
            assert appset.get("kind") == "ApplicationSet", "kind should be ApplicationSet"
            assert appset.get("metadata", {}).get("name") == "my_service", "name should resolve correctly"
        except yaml.YAMLError as e:
            raise AssertionError(f"Resolved ApplicationSet contains invalid YAML syntax: {e}")

    def test_generators_list_has_three_environments(self):
        """Test that generators list has exactly three environments."""
        test_content = self.appset_content.replace("{{ cookiecutter.service_slug }}", "my_service")
        test_content = test_content.replace("{{ cookiecutter.repo_url | default('https://github.com') }}", "https://github.com/example/my_service")

        try:
            appset = yaml.safe_load(test_content)
            generators = appset.get("spec", {}).get("generators", [])
            assert len(generators) > 0, "generators section must not be empty"
            list_gen = generators[0].get("list", {})
            elements = list_gen.get("elements", [])
            assert len(elements) == 3, "Must have exactly 3 environments (dev, staging, prod)"
            env_names = {el.get("name") for el in elements}
            assert env_names == {"dev", "staging", "prod"}, "Environments must be dev, staging, prod"
        except (yaml.YAMLError, KeyError, IndexError) as e:
            raise AssertionError(f"Failed to validate generators structure: {e}")

    def test_template_metadata_has_templating(self):
        """Test that template metadata uses dynamic naming."""
        assert "{{ '{{' }}element.name{{ '}}' }}" in self.appset_content, \
            "template.metadata.name must use dynamic templating from element"

    def test_helm_releasename_is_dynamic(self):
        """Test that Helm releaseName is dynamically generated."""
        assert "releaseName:" in self.appset_content, \
            "helm section must have releaseName"
        assert "{{ '{{' }}element.name{{ '}}' }}" in self.appset_content, \
            "releaseName must use element.name for dynamic naming"
