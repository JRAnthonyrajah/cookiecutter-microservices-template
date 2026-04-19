"""Tests for pre_gen_project.py validation hook."""
import re
import sys
from pathlib import Path

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'hooks'))

from pre_gen_project import (
    validate_slug,
    validate_package_name,
    validate_version,
    validate_language,
)


class TestSlugValidation:
    """Tests for service_slug validation."""

    def test_valid_slug_lowercase_letters(self):
        """Valid slug with lowercase letters."""
        assert validate_slug('my_service') is True

    def test_valid_slug_with_numbers(self):
        """Valid slug with numbers."""
        assert validate_slug('service123') is True

    def test_valid_slug_with_underscores(self):
        """Valid slug with underscores."""
        assert validate_slug('my_service_name') is True

    def test_valid_slug_single_letter(self):
        """Valid slug with single letter."""
        assert validate_slug('a') is True

    def test_valid_slug_single_number(self):
        """Valid slug with single number."""
        assert validate_slug('1') is True

    def test_invalid_slug_uppercase(self):
        """Invalid slug with uppercase letters."""
        assert validate_slug('MyService') is False

    def test_invalid_slug_with_hyphens(self):
        """Invalid slug with hyphens."""
        assert validate_slug('my-service') is False

    def test_invalid_slug_with_spaces(self):
        """Invalid slug with spaces."""
        assert validate_slug('my service') is False

    def test_invalid_slug_with_special_chars(self):
        """Invalid slug with special characters."""
        assert validate_slug('my$service') is False


class TestPackageNameValidation:
    """Tests for package_name validation."""

    def test_valid_package_name_simple(self):
        """Valid package name."""
        assert validate_package_name('myservice') is True

    def test_valid_package_name_with_underscores(self):
        """Valid package name with underscores."""
        assert validate_package_name('my_service') is True

    def test_valid_package_name_mixed_case(self):
        """Valid package name with mixed case."""
        assert validate_package_name('MyService') is True

    def test_invalid_package_name_starting_with_digit(self):
        """Invalid package name starting with digit."""
        assert validate_package_name('1service') is False

    def test_invalid_package_name_with_hyphens(self):
        """Invalid package name with hyphens."""
        assert validate_package_name('my-service') is False

    def test_invalid_package_name_with_spaces(self):
        """Invalid package name with spaces."""
        assert validate_package_name('my service') is False

    def test_invalid_package_name_with_special_chars(self):
        """Invalid package name with special characters."""
        assert validate_package_name('my$service') is False


class TestVersionValidation:
    """Tests for version validation."""

    def test_valid_version_semver(self):
        """Valid semantic version."""
        assert validate_version('1.0.0') is True

    def test_valid_version_complex(self):
        """Valid complex semantic version."""
        assert validate_version('2.15.3') is True

    def test_valid_version_leading_zeros(self):
        """Valid version with leading zeros."""
        assert validate_version('01.02.03') is True

    def test_invalid_version_missing_patch(self):
        """Invalid version missing patch."""
        assert validate_version('1.0') is False

    def test_invalid_version_too_many_parts(self):
        """Invalid version with too many parts."""
        assert validate_version('1.0.0.0') is False

    def test_invalid_version_with_v_prefix(self):
        """Invalid version with v prefix."""
        assert validate_version('v1.0.0') is False

    def test_invalid_version_with_letters(self):
        """Invalid version with letters."""
        assert validate_version('1.0.0-beta') is False

    def test_invalid_version_empty(self):
        """Invalid empty version."""
        assert validate_version('') is False


class TestLanguageValidation:
    """Tests for language validation."""

    def test_valid_language_python(self):
        """Valid language: python."""
        assert validate_language('python') is True

    def test_valid_language_go(self):
        """Valid language: go."""
        assert validate_language('go') is True

    def test_valid_language_nodejs(self):
        """Valid language: nodejs."""
        assert validate_language('nodejs') is True

    def test_invalid_language_uppercase(self):
        """Invalid language: uppercase."""
        assert validate_language('Python') is False

    def test_invalid_language_java(self):
        """Invalid language: not supported."""
        assert validate_language('java') is False

    def test_invalid_language_rust(self):
        """Invalid language: not supported."""
        assert validate_language('rust') is False

    def test_invalid_language_empty(self):
        """Invalid language: empty."""
        assert validate_language('') is False


class TestIntegration:
    """Integration tests for multiple validations."""

    def test_all_valid_inputs(self):
        """All inputs valid."""
        assert validate_slug('my_service') is True
        assert validate_package_name('my_service') is True
        assert validate_version('1.0.0') is True
        assert validate_language('python') is True

    def test_multiple_invalid_inputs(self):
        """Multiple inputs invalid."""
        assert validate_slug('MyService') is False
        assert validate_package_name('1service') is False
        assert validate_version('1.0') is False
        assert validate_language('java') is False
