"""Test suite for cookiecutter.json manifest validation."""
import json
import os
import re
from pathlib import Path


class TestCookiecutterManifest:
    """Tests for cookiecutter.json manifest validity and completeness."""

    @classmethod
    def setup_class(cls):
        """Load the cookiecutter.json manifest."""
        manifest_path = Path(__file__).parent.parent / "cookiecutter.json"
        assert manifest_path.exists(), f"cookiecutter.json not found at {manifest_path}"
        with open(manifest_path, "r") as f:
            cls.manifest = json.load(f)

    def test_manifest_is_valid_json(self):
        """Test that cookiecutter.json is valid JSON."""
        manifest_path = Path(__file__).parent.parent / "cookiecutter.json"
        with open(manifest_path, "r") as f:
            # Should not raise an exception
            manifest = json.load(f)
            assert isinstance(manifest, dict), "Manifest must be a JSON object"

    def test_all_required_variables_present(self):
        """Test that all required variables are defined in the manifest."""
        required_vars = [
            "service_name",
            "service_slug",
            "description",
            "language",
            "package_name",
            "version",
            "author",
            "email",
            "license",
            "python_version",
            "go_version",
            "node_version",
            "create_github_repo",
            "repo_visibility",
        ]
        for var in required_vars:
            assert var in self.manifest, f"Missing required variable: {var}"

    def test_all_variables_have_defaults(self):
        """Test that all variables have non-None default values."""
        for key, value in self.manifest.items():
            assert value is not None, f"Variable '{key}' has None as default value"
            # repo_visibility is special - it's a list of options
            if key == "repo_visibility":
                assert isinstance(value, list), f"{key} should be a list"
                assert len(value) > 0, f"{key} list should not be empty"
            else:
                # All other values should be non-empty strings
                if isinstance(value, str):
                    assert len(value) > 0, f"Variable '{key}' has empty string as default"

    def test_service_slug_format(self):
        """Test that service_slug follows Python identifier rules."""
        slug = self.manifest["service_slug"]
        # Python identifiers: start with letter or underscore, contain alphanumerics and underscores
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
        assert re.match(
            pattern, slug
        ), f"service_slug '{slug}' does not match valid Python identifier format"

    def test_package_name_format(self):
        """Test that package_name follows Python identifier rules."""
        package = self.manifest["package_name"]
        pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
        assert re.match(
            pattern, package
        ), f"package_name '{package}' does not match valid Python identifier format"

    def test_language_is_valid(self):
        """Test that language is one of the supported languages."""
        language = self.manifest["language"]
        valid_languages = ["python", "go", "nodejs"]
        assert (
            language in valid_languages
        ), f"language '{language}' not in {valid_languages}"

    def test_version_format_is_semver(self):
        """Test that version follows semantic versioning (MAJOR.MINOR.PATCH)."""
        version = self.manifest["version"]
        pattern = r"^\d+\.\d+\.\d+$"
        assert re.match(
            pattern, version
        ), f"version '{version}' does not follow semantic versioning"

    def test_python_version_format(self):
        """Test that python_version is in valid format (e.g., 3.11.0)."""
        py_version = self.manifest["python_version"]
        pattern = r"^\d+\.\d+\.\d+$"
        assert re.match(
            pattern, py_version
        ), f"python_version '{py_version}' is not in X.Y.Z format"

    def test_go_version_format(self):
        """Test that go_version is in valid format (e.g., 1.21.0)."""
        go_version = self.manifest["go_version"]
        pattern = r"^\d+\.\d+\.\d+$"
        assert re.match(
            pattern, go_version
        ), f"go_version '{go_version}' is not in X.Y.Z format"

    def test_node_version_format(self):
        """Test that node_version is in valid format (e.g., 20.10.0)."""
        node_version = self.manifest["node_version"]
        pattern = r"^\d+\.\d+\.\d+$"
        assert re.match(
            pattern, node_version
        ), f"node_version '{node_version}' is not in X.Y.Z format"

    def test_email_format(self):
        """Test that email is in a basic valid format."""
        email = self.manifest["email"]
        # Simple email validation: something@something.something
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        assert re.match(
            pattern, email
        ), f"email '{email}' does not match valid email format"

    def test_repo_visibility_options(self):
        """Test that repo_visibility contains only valid options."""
        visibility_options = self.manifest["repo_visibility"]
        valid_options = {"private", "public"}
        actual_options = set(visibility_options)
        assert actual_options.issubset(
            valid_options
        ), f"repo_visibility contains invalid options: {actual_options - valid_options}"

    def test_create_github_repo_format(self):
        """Test that create_github_repo is yes/no."""
        value = self.manifest["create_github_repo"]
        valid_values = ["yes", "no"]
        assert (
            value in valid_values
        ), f"create_github_repo '{value}' must be 'yes' or 'no'"

    def test_template_directory_exists(self):
        """Test that the template directory {{ cookiecutter.service_slug }} exists."""
        template_dir = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}"
        assert (
            template_dir.exists()
        ), f"Template directory {template_dir} does not exist"
        assert (
            template_dir.is_dir()
        ), f"Template path {template_dir} is not a directory"

    def test_template_files_use_placeholders(self):
        """Test that template files contain at least one cookiecutter placeholder."""
        template_dir = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}"
        template_files = list(template_dir.rglob("*.md"))
        assert (
            len(template_files) > 0
        ), "No template files found in template directory"

        # Check at least one file has cookiecutter placeholders
        has_placeholders = False
        for template_file in template_files:
            content = template_file.read_text()
            if "{{ cookiecutter." in content:
                has_placeholders = True
                break

        assert (
            has_placeholders
        ), "No template files contain {{ cookiecutter.* }} placeholders"

    def test_placeholder_variables_are_defined(self):
        """Test that all {{ cookiecutter.* }} placeholders have matching manifest variables."""
        import re as regex

        template_dir = Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}"
        template_files = list(template_dir.rglob("*"))

        # Find all placeholders in template files
        placeholder_pattern = r"\{\{\s*cookiecutter\.\w+\s*\}\}"
        found_placeholders = set()

        for template_file in template_files:
            if template_file.is_file():
                try:
                    content = template_file.read_text()
                    matches = regex.findall(placeholder_pattern, content)
                    for match in matches:
                        # Extract variable name from {{ cookiecutter.variable_name }}
                        var_name = regex.search(r"cookiecutter\.(\w+)", match).group(1)
                        found_placeholders.add(var_name)
                except (UnicodeDecodeError, AttributeError):
                    # Skip binary files
                    pass

        # Check that all found placeholders are defined in manifest
        for placeholder_var in found_placeholders:
            assert (
                placeholder_var in self.manifest
            ), f"Placeholder variable '{{ cookiecutter.{placeholder_var} }}' is not defined in manifest"


class TestCookiecutterInputValidation:
    """Tests for input validation rules that would be used in pre_gen_project.py hook."""

    def test_service_slug_validation_logic(self):
        """Test validation logic for service_slug."""
        valid_slugs = ["my_service", "_private_service", "service123", "MyService"]
        invalid_slugs = ["123service", "-service", "my-service", ""]

        for slug in valid_slugs:
            pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
            assert re.match(pattern, slug), f"Valid slug '{slug}' failed validation"

        for slug in invalid_slugs:
            pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
            assert not re.match(
                pattern, slug
            ), f"Invalid slug '{slug}' passed validation"

    def test_language_validation_logic(self):
        """Test validation logic for language selection."""
        valid_languages = ["python", "go", "nodejs"]
        invalid_languages = ["java", "rust", "c++", ""]

        for lang in valid_languages:
            assert lang in ["python", "go", "nodejs"], f"Valid language '{lang}' failed"

        for lang in invalid_languages:
            assert (
                lang not in ["python", "go", "nodejs"]
            ), f"Invalid language '{lang}' passed"

    def test_version_validation_logic(self):
        """Test validation logic for semantic version format."""
        valid_versions = ["0.1.0", "1.0.0", "2.5.10", "10.20.30"]
        invalid_versions = ["1.0", "v1.0.0", "1.0.0-alpha", ""]

        pattern = r"^\d+\.\d+\.\d+$"
        for version in valid_versions:
            assert re.match(
                pattern, version
            ), f"Valid version '{version}' failed validation"

        for version in invalid_versions:
            assert not re.match(
                pattern, version
            ), f"Invalid version '{version}' passed validation"
