"""Tests for language-specific stubs (Python, Go, Node.js)."""

import json
import os
from pathlib import Path

import pytest


class TestPythonStubs:
    """Test Python language stub structure and files."""

    def test_python_package_directory_exists(self):
        """Verify {{ cookiecutter.package_name }} package directory exists."""
        base_dir = Path("{{ cookiecutter.service_slug }}")
        src_dir = base_dir / "src" / "{{ cookiecutter.package_name }}"
        assert src_dir.is_dir(), f"Python package directory {src_dir} does not exist"

    def test_python_init_file_exists(self):
        """Verify __init__.py exists in Python package."""
        init_file = Path("{{ cookiecutter.service_slug }}/src/{{ cookiecutter.package_name }}/__init__.py")
        assert init_file.is_file(), f"__init__.py not found at {init_file}"

    def test_python_init_file_contains_version(self):
        """Verify __init__.py contains version info."""
        init_file = Path("{{ cookiecutter.service_slug }}/src/{{ cookiecutter.package_name }}/__init__.py")
        content = init_file.read_text()
        assert "__version__" in content, "__version__ not found in __init__.py"
        assert "__author__" in content, "__author__ not found in __init__.py"

    def test_python_main_file_exists(self):
        """Verify main.py exists in Python package."""
        main_file = Path("{{ cookiecutter.service_slug }}/src/{{ cookiecutter.package_name }}/main.py")
        assert main_file.is_file(), f"main.py not found at {main_file}"

    def test_python_main_file_contains_main_function(self):
        """Verify main.py contains main function."""
        main_file = Path("{{ cookiecutter.service_slug }}/src/{{ cookiecutter.package_name }}/main.py")
        content = main_file.read_text()
        assert "def main():" in content, "main() function not found in main.py"
        assert "if __name__" in content, "__name__ guard not found in main.py"

    def test_pyproject_toml_exists(self):
        """Verify pyproject.toml exists."""
        pyproject = Path("{{ cookiecutter.service_slug }}/pyproject.toml")
        assert pyproject.is_file(), f"pyproject.toml not found at {pyproject}"

    def test_pyproject_toml_contains_build_system(self):
        """Verify pyproject.toml contains [build-system] section."""
        pyproject = Path("{{ cookiecutter.service_slug }}/pyproject.toml")
        content = pyproject.read_text()
        assert "[build-system]" in content, "[build-system] section not found"
        assert "setuptools" in content, "setuptools not configured"

    def test_pyproject_toml_contains_project_metadata(self):
        """Verify pyproject.toml contains [project] section with metadata."""
        pyproject = Path("{{ cookiecutter.service_slug }}/pyproject.toml")
        content = pyproject.read_text()
        assert "[project]" in content, "[project] section not found"
        assert "name =" in content, "project name not found"
        assert "version =" in content, "project version not found"

    def test_pyproject_toml_contains_pytest_config(self):
        """Verify pyproject.toml contains pytest configuration."""
        pyproject = Path("{{ cookiecutter.service_slug }}/pyproject.toml")
        content = pyproject.read_text()
        assert "[tool.pytest.ini_options]" in content, "pytest config not found"
        assert "testpaths" in content, "testpaths not configured"


class TestGoStubs:
    """Test Go language stub structure and files."""

    def test_go_main_file_exists(self):
        """Verify main.go exists."""
        main_go = Path("{{ cookiecutter.service_slug }}/main.go")
        assert main_go.is_file(), f"main.go not found at {main_go}"

    def test_go_main_file_contains_package_main(self):
        """Verify main.go contains package main declaration."""
        main_go = Path("{{ cookiecutter.service_slug }}/main.go")
        content = main_go.read_text()
        assert "package main" in content, "package main not found in main.go"

    def test_go_main_file_contains_main_function(self):
        """Verify main.go contains main function."""
        main_go = Path("{{ cookiecutter.service_slug }}/main.go")
        content = main_go.read_text()
        assert "func main()" in content, "func main() not found in main.go"

    def test_go_main_file_contains_imports(self):
        """Verify main.go contains required imports."""
        main_go = Path("{{ cookiecutter.service_slug }}/main.go")
        content = main_go.read_text()
        assert "import" in content, "import statement not found in main.go"

    def test_go_mod_file_exists(self):
        """Verify go.mod exists."""
        go_mod = Path("{{ cookiecutter.service_slug }}/go.mod")
        assert go_mod.is_file(), f"go.mod not found at {go_mod}"

    def test_go_mod_file_contains_module_declaration(self):
        """Verify go.mod contains module declaration."""
        go_mod = Path("{{ cookiecutter.service_slug }}/go.mod")
        content = go_mod.read_text()
        assert "module " in content, "module declaration not found in go.mod"

    def test_go_mod_file_contains_go_version(self):
        """Verify go.mod contains Go version."""
        go_mod = Path("{{ cookiecutter.service_slug }}/go.mod")
        content = go_mod.read_text()
        assert "go " in content, "go version not found in go.mod"


class TestNodeJsStubs:
    """Test Node.js language stub structure and files."""

    def test_nodejs_src_directory_exists(self):
        """Verify src directory exists for Node.js."""
        src_dir = Path("{{ cookiecutter.service_slug }}/src")
        assert src_dir.is_dir(), f"src directory not found at {src_dir}"

    def test_nodejs_index_file_exists(self):
        """Verify src/index.js exists."""
        index_js = Path("{{ cookiecutter.service_slug }}/src/index.js")
        assert index_js.is_file(), f"src/index.js not found at {index_js}"

    def test_nodejs_index_file_contains_main_function(self):
        """Verify src/index.js contains main function."""
        index_js = Path("{{ cookiecutter.service_slug }}/src/index.js")
        content = index_js.read_text()
        assert "async function main()" in content or "function main()" in content, \
            "main function not found in index.js"
        assert "module.exports" in content, "module.exports not found in index.js"

    def test_package_json_exists(self):
        """Verify package.json exists."""
        package_json = Path("{{ cookiecutter.service_slug }}/package.json")
        assert package_json.is_file(), f"package.json not found at {package_json}"

    def test_package_json_valid_json(self):
        """Verify package.json is valid JSON."""
        package_json = Path("{{ cookiecutter.service_slug }}/package.json")
        content = package_json.read_text()
        try:
            data = json.loads(content)
            assert isinstance(data, dict), "package.json is not a valid JSON object"
        except json.JSONDecodeError as e:
            pytest.fail(f"package.json contains invalid JSON: {e}")

    def test_package_json_contains_metadata(self):
        """Verify package.json contains required metadata."""
        package_json = Path("{{ cookiecutter.service_slug }}/package.json")
        data = json.loads(package_json.read_text())
        assert "name" in data, "name not found in package.json"
        assert "version" in data, "version not found in package.json"
        assert "description" in data, "description not found in package.json"
        assert "main" in data, "main not found in package.json"

    def test_package_json_contains_scripts(self):
        """Verify package.json contains scripts section."""
        package_json = Path("{{ cookiecutter.service_slug }}/package.json")
        data = json.loads(package_json.read_text())
        assert "scripts" in data, "scripts section not found in package.json"
        assert "start" in data["scripts"], "start script not found"
        assert "test" in data["scripts"], "test script not found"

    def test_package_json_contains_engines(self):
        """Verify package.json specifies Node.js version."""
        package_json = Path("{{ cookiecutter.service_slug }}/package.json")
        data = json.loads(package_json.read_text())
        assert "engines" in data, "engines section not found in package.json"
        assert "node" in data["engines"], "node version not specified in engines"
