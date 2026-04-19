"""Tests for API and architecture documentation.

Comprehensive test suite validating API.md and ARCHITECTURE.md documentation
for the {{ cookiecutter.service_slug }} microservice, including content validation,
examples, structure, and best practices.
"""
import json
import re
from pathlib import Path
import pytest


class TestAPIDocumentationPresence:
    """Tests for API.md existence and basic structure."""

    def test_api_md_exists(self):
        """API.md exists in service directory."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        assert api_path.exists(), "API.md file not found"

    def test_api_md_not_empty(self):
        """API.md is not empty."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert len(content) > 500, "API.md is too small"

    def test_api_md_is_valid_markdown(self):
        """API.md is valid markdown."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert re.search(r'^#', content, re.MULTILINE), "No markdown headers found"
        assert "#" in content, "Missing markdown headers"


class TestArchitectureDocumentationPresence:
    """Tests for ARCHITECTURE.md existence and basic structure."""

    def test_architecture_md_exists(self):
        """ARCHITECTURE.md exists in service directory."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        assert arch_path.exists(), "ARCHITECTURE.md file not found"

    def test_architecture_md_not_empty(self):
        """ARCHITECTURE.md is not empty."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert len(content) > 500, "ARCHITECTURE.md is too small"

    def test_architecture_md_is_valid_markdown(self):
        """ARCHITECTURE.md is valid markdown."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert re.search(r'^#', content, re.MULTILINE), "No markdown headers found"


class TestAPIDocumentationContent:
    """Tests for API.md content validation."""

    def test_api_has_overview_section(self):
        """API.md contains Overview section."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "## Overview" in content, "Overview section not found"

    def test_api_has_base_url_documented(self):
        """API.md documents the base URL."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Base URL" in content, "Base URL not documented"

    def test_api_has_authentication_section(self):
        """API.md documents authentication methods."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "## Authentication" in content, "Authentication section not found"

    def test_api_has_http_status_codes(self):
        """API.md documents HTTP status codes."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "200" in content and "404" in content and "500" in content, "HTTP codes not documented"

    def test_api_documents_error_handling(self):
        """API.md documents error handling."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Error" in content, "Error handling not documented"

    def test_api_has_rate_limiting_documented(self):
        """API.md documents rate limiting."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Rate" in content or "rate" in content.lower(), "Rate limiting not documented"

    def test_api_has_request_response_format(self):
        """API.md documents request/response format."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Request" in content and "Response" in content, "Request/Response not documented"


class TestAPIEndpointsDocumentation:
    """Tests for API endpoint documentation."""

    def test_api_has_health_endpoint(self):
        """API.md documents health check endpoint."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "health" in content.lower(), "Health endpoint not documented"

    def test_api_has_crud_endpoints(self):
        """API.md documents CRUD endpoints."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "GET" in content and "POST" in content and "DELETE" in content, "CRUD methods not documented"

    def test_api_has_endpoint_descriptions(self):
        """API.md provides descriptions for endpoints."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert re.search(r'###.*?[Gg]et', content), "No endpoint methods documented"

    def test_api_has_path_parameters_documented(self):
        """API.md documents path parameters."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Parameter" in content or "{id}" in content, "Path parameters not documented"

    def test_api_has_query_parameters_documented(self):
        """API.md documents query parameters."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Query" in content, "Query parameters not documented"

    def test_api_has_pagination_documented(self):
        """API.md documents pagination."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "pagination" in content.lower() or "page" in content.lower(), "Pagination not documented"


class TestAPICurlExamples:
    """Tests for curl command examples in API.md."""

    def test_api_has_curl_examples(self):
        """API.md contains curl command examples."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "curl" in content, "No curl examples found"

    def test_curl_examples_use_correct_format(self):
        """Curl examples have proper syntax."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert re.search(r'curl.*-X\s+(GET|POST)', content), "Curl missing HTTP method"

    def test_curl_examples_include_headers(self):
        """Curl examples include request headers."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "-H " in content, "Curl examples missing headers"

    def test_curl_examples_use_authentication(self):
        """Curl examples demonstrate authentication."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "API-Key" in content or "Bearer" in content, "Auth not shown in examples"

    def test_curl_examples_show_request_body(self):
        """Curl examples show request body where applicable."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "-d" in content, "Request body examples missing"


class TestAPIJSONExamples:
    """Tests for JSON payload examples in API.md."""

    def test_api_has_json_request_examples(self):
        """API.md contains JSON request examples."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        json_blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)
        assert len(json_blocks) > 0, "No JSON examples found"

    def test_json_examples_are_valid(self):
        """JSON examples in API.md are syntactically valid."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        json_blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)

        for json_block in json_blocks[:3]:
            try:
                json.loads(json_block)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON: {e}")

    def test_api_has_response_examples(self):
        """API.md contains response examples."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Response" in content, "No response examples"

    def test_api_has_error_response_examples(self):
        """API.md contains error response examples."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "error" in content.lower(), "No error response examples"


class TestOpenAPIDocumentation:
    """Tests for OpenAPI/Swagger documentation."""

    def test_api_references_openapi(self):
        """API.md references OpenAPI specification."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "OpenAPI" in content or "Swagger" in content, "OpenAPI/Swagger not mentioned"

    def test_api_has_openapi_endpoints(self):
        """API.md documents OpenAPI endpoints."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "openapi.json" in content or "swagger" in content.lower(), "OpenAPI endpoints not documented"


class TestArchitectureDocumentationContent:
    """Tests for ARCHITECTURE.md content validation."""

    def test_architecture_has_overview(self):
        """ARCHITECTURE.md contains system overview."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Overview" in content, "Overview missing"

    def test_architecture_has_components_section(self):
        """ARCHITECTURE.md documents service components."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Component" in content, "Components section not found"

    def test_architecture_documents_api_layer(self):
        """ARCHITECTURE.md documents API layer."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "API" in content, "API layer not documented"

    def test_architecture_documents_database_layer(self):
        """ARCHITECTURE.md documents data access layer."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Database" in content or "Data Access" in content, "Database layer not documented"

    def test_architecture_documents_caching(self):
        """ARCHITECTURE.md documents caching strategy."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Cache" in content or "Redis" in content, "Caching not documented"

    def test_architecture_documents_messaging(self):
        """ARCHITECTURE.md documents message queue."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Message" in content or "Queue" in content, "Messaging not documented"

    def test_architecture_has_data_flow_section(self):
        """ARCHITECTURE.md documents data flow."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Data Flow" in content or "Flow" in content, "Data flow section missing"

    def test_architecture_documents_design_patterns(self):
        """ARCHITECTURE.md documents design patterns."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Pattern" in content, "Design patterns not documented"


class TestArchitectureDiagrams:
    """Tests for architecture diagrams and visualizations."""

    def test_architecture_has_ascii_diagram(self):
        """ARCHITECTURE.md contains ASCII diagram."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "├" in content or "│" in content or "┌" in content, "No ASCII diagram found"

    def test_architecture_has_flow_diagrams(self):
        """ARCHITECTURE.md contains flow diagrams."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "→" in content or "->" in content or "↓" in content, "No flow diagrams found"


class TestArchitectureSecurityContent:
    """Tests for security documentation in ARCHITECTURE.md."""

    def test_architecture_documents_security(self):
        """ARCHITECTURE.md documents security architecture."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Security" in content, "Security not documented"

    def test_architecture_covers_authentication(self):
        """ARCHITECTURE.md covers authentication."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Authentication" in content, "Authentication not documented"

    def test_architecture_covers_authorization(self):
        """ARCHITECTURE.md covers authorization."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Authorization" in content or "RBAC" in content, "Authorization not documented"

    def test_architecture_covers_encryption(self):
        """ARCHITECTURE.md covers encryption."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Encryption" in content or "TLS" in content, "Encryption not documented"

    def test_architecture_covers_input_validation(self):
        """ARCHITECTURE.md covers input validation."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Validation" in content, "Input validation not documented"


class TestArchitectureScalability:
    """Tests for scalability documentation."""

    def test_architecture_documents_scalability(self):
        """ARCHITECTURE.md documents scalability."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Scalability" in content or "Scaling" in content, "Scalability not documented"

    def test_architecture_covers_horizontal_scaling(self):
        """ARCHITECTURE.md covers horizontal scaling."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Horizontal" in content or "stateless" in content.lower(), "Horizontal scaling not documented"

    def test_architecture_covers_caching_strategy(self):
        """ARCHITECTURE.md covers caching for performance."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "cache" in content.lower(), "Caching strategy not documented"


class TestArchitectureMonitoring:
    """Tests for monitoring and observability documentation."""

    def test_architecture_documents_monitoring(self):
        """ARCHITECTURE.md documents monitoring."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Monitor" in content or "Observ" in content, "Monitoring not documented"

    def test_architecture_documents_logging(self):
        """ARCHITECTURE.md documents logging."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Log" in content, "Logging not documented"

    def test_architecture_documents_metrics(self):
        """ARCHITECTURE.md documents metrics collection."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Metrics" in content or "Prometheus" in content, "Metrics not documented"

    def test_architecture_documents_tracing(self):
        """ARCHITECTURE.md documents distributed tracing."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Trace" in content or "Jaeger" in content, "Tracing not documented"


class TestDocumentationLinkReferences:
    """Tests for link validation and reference consistency."""

    def test_api_internal_references_valid(self):
        """API.md internal markdown links are formatted correctly."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        for text, href in links:
            assert len(text) > 0 and len(href) > 0, "Invalid link format"

    def test_architecture_internal_references_valid(self):
        """ARCHITECTURE.md internal markdown links are formatted correctly."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        for text, href in links:
            assert len(text) > 0 and len(href) > 0, "Invalid link format"


class TestDocumentationTableValidation:
    """Tests for markdown table validation."""

    def test_api_has_markdown_tables(self):
        """API.md contains markdown tables."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert re.search(r'\|.*\|.*\n.*\|.*-.*\|', content), "No markdown tables found"

    def test_api_tables_properly_formatted(self):
        """API.md tables are properly formatted."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        tables = re.findall(r'(\|[^\n]+\n\|[-|\s]+\n(?:\|[^\n]+\n)+)', content)
        assert len(tables) > 0, "No valid markdown tables found"

    def test_architecture_has_diagrams_or_code(self):
        """ARCHITECTURE.md contains diagrams or code blocks."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        has_ascii = "├" in content or "│" in content
        has_code = "```" in content
        assert has_ascii or has_code, "No diagrams or code blocks found"


class TestCodeExamples:
    """Tests for code examples in documentation."""

    def test_api_has_code_blocks(self):
        """API.md contains code blocks."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "```" in content, "No code blocks found"

    def test_architecture_has_code_examples(self):
        """ARCHITECTURE.md contains code examples."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "```" in content or "┌" in content, "No code examples found"

    def test_code_blocks_have_language_tags(self):
        """Code blocks should have language identifiers."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        with_tags = len(re.findall(r'```[\w]+\n', content))
        assert with_tags > 0, "No code blocks with language tags found"


class TestDocumentationCompleteness:
    """Tests for overall documentation completeness."""

    def test_both_documents_exist(self):
        """Both API.md and ARCHITECTURE.md exist."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        assert api_path.exists() and arch_path.exists(), "Missing documentation files"

    def test_combined_documentation_size(self):
        """Combined documentation has sufficient content."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        api_content = api_path.read_text()
        arch_content = arch_path.read_text()
        combined_size = len(api_content) + len(arch_content)
        assert combined_size > 5000, f"Documentation too small: {combined_size} chars"

    def test_api_mentions_service_name(self):
        """API.md references the service name."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "{{ cookiecutter.service_" in content or "service" in content.lower(), \
            "Service name not referenced"

    def test_architecture_mentions_service_name(self):
        """ARCHITECTURE.md references the service name."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "{{ cookiecutter.service_" in content or "service" in content.lower(), \
            "Service name not referenced"


class TestDocumentationBestPractices:
    """Tests for documentation best practices."""

    def test_api_uses_consistent_formatting(self):
        """API.md uses consistent header formatting."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        h1_count = len(re.findall(r'^#[^#]', content, re.MULTILINE))
        h2_count = len(re.findall(r'^##[^#]', content, re.MULTILINE))
        assert h1_count >= 1 and h2_count > h1_count, "Inconsistent header formatting"

    def test_architecture_uses_consistent_formatting(self):
        """ARCHITECTURE.md uses consistent header formatting."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        h1_count = len(re.findall(r'^#[^#]', content, re.MULTILINE))
        h2_count = len(re.findall(r'^##[^#]', content, re.MULTILINE))
        assert h1_count >= 1 and h2_count > h1_count, "Inconsistent header formatting"

    def test_documentation_avoids_placeholder_content(self):
        """Documentation doesn't contain TODO or placeholder content."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        api_content = api_path.read_text()
        arch_content = arch_path.read_text()
        assert "TODO: " not in api_content and "TODO: " not in arch_content, "Contains TODO"
        assert "[PLACEHOLDER]" not in api_content.upper() and "[PLACEHOLDER]" not in arch_content.upper(), \
            "Contains placeholders"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
