#!/usr/bin/env python3
"""Pre-generation hook for cookiecutter template validation.

Validates all cookiecutter inputs before project generation:
- service_slug matches [a-z0-9_]+
- package_name is valid Python identifier
- version matches semver X.Y.Z
- language is in [python, go, nodejs]
"""
import re
import sys
from pathlib import Path


def validate_slug(slug: str) -> bool:
    """Validate service_slug matches [a-z0-9_]+."""
    return bool(re.match(r'^[a-z0-9_]+$', slug))


def validate_package_name(name: str) -> bool:
    """Validate package_name is a valid Python identifier."""
    if not name.isidentifier():
        return False
    if name[0].isdigit():
        return False
    return True


def validate_version(version: str) -> bool:
    """Validate version matches semver X.Y.Z."""
    return bool(re.match(r'^\d+\.\d+\.\d+$', version))


def validate_language(language: str) -> bool:
    """Validate language is in [python, go, nodejs]."""
    return language in ['python', 'go', 'nodejs']


def main():
    """Run all validations on cookiecutter context."""
    errors = []

    # Get values from environment (set by cookiecutter)
    service_slug = '{{ cookiecutter.service_slug }}'
    package_name = '{{ cookiecutter.package_name }}'
    version = '{{ cookiecutter.version }}'
    language = '{{ cookiecutter.language }}'

    # Validate each field
    if not validate_slug(service_slug):
        errors.append(
            f"Invalid service_slug '{service_slug}': "
            f"must contain only lowercase letters, digits, and underscores"
        )

    if not validate_package_name(package_name):
        errors.append(
            f"Invalid package_name '{package_name}': "
            f"must be a valid Python identifier (alphanumeric + underscore, "
            f"cannot start with digit)"
        )

    if not validate_version(version):
        errors.append(
            f"Invalid version '{version}': "
            f"must follow semantic versioning (X.Y.Z format)"
        )

    if not validate_language(language):
        errors.append(
            f"Invalid language '{language}': "
            f"must be one of [python, go, nodejs]"
        )

    # Report results
    if errors:
        print("Template generation failed validation:", file=sys.stderr)
        for error in errors:
            print(f"  ✗ {error}", file=sys.stderr)
        sys.exit(1)

    print("✓ All validations passed")
    sys.exit(0)


if __name__ == '__main__':
    main()
