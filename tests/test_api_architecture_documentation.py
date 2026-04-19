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
        # Check for markdown headers
        assert re.search(r'^#', content, re.MULTILINE), "No markdown headers found"
        # Check for some structure
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
        # Check for markdown headers
        assert re.search(r'^#', content, re.MULTILINE), "No markdown headers found"
        assert "#" in content, "Missing markdown headers"


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
        assert "Base URL" in content or "base url" in content.lower(), "Base URL not documented"
        assert "localhost" in content or "example.com" in content, "No URL example provided"

    def test_api_has_authentication_section(self):
        """API.md documents authentication methods."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "## Authentication" in content, "Authentication section not found"
        assert "API Key" in content or "Bearer" in content, "Auth methods not documented"

    def test_api_has_http_status_codes(self):
        """API.md documents HTTP status codes."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "200" in content, "200 status code not documented"
        assert "201" in content, "201 status code not documented"
        assert "400" in content, "400 status code not documented"
        assert "404" in content, "404 status code not documented"
        assert "500" in content, "500 status code not documented"

    def test_api_documents_error_handling(self):
        """API.md documents error handling."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Error" in content, "Error handling not documented"
        assert "error" in content.lower(), "No error documentation"

    def test_api_has_rate_limiting_documented(self):
        """API.md documents rate limiting."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Rate" in content or "rate" in content.lower(), "Rate limiting not documented"
        assert "limit" in content.lower(), "Limits not specified"

    def test_api_has_request_response_format(self):
        """API.md documents request/response format."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Request" in content or "request" in content.lower(), "Request format not documented"
        assert "Response" in content or "response" in content.lower(), "Response format not documented"
        assert "JSON" in content, "JSON format not mentioned"


class TestAPIEndpointsDocumentation:
    """Tests for API endpoint documentation."""

    def test_api_has_health_endpoint(self):
        """API.md documents health check endpoint."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "health" in content.lower(), "Health endpoint not documented"
        assert "GET" in content, "HTTP method not specified"

    def test_api_has_crud_endpoints(self):
        """API.md documents CRUD endpoints."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "GET" in content, "GET method not documented"
        assert "POST" in content, "POST method not documented"
        assert "PUT" in content or "PATCH" in content, "Update methods not documented"
        assert "DELETE" in content, "DELETE method not documented"

    def test_api_has_endpoint_descriptions(self):
        """API.md provides descriptions for endpoints."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Check for endpoint sections with descriptions
        assert re.search(r'###.*?[Gg]et|[Pp]ost|[Pp]ut|[Dd]elete', content), "No endpoint methods documented"

    def test_api_has_path_parameters_documented(self):
        """API.md documents path parameters."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Path Parameter" in content or "path parameter" in content.lower() or "{id}" in content, \
            "Path parameters not documented"

    def test_api_has_query_parameters_documented(self):
        """API.md documents query parameters."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Query" in content or "query" in content.lower() or "?" in content, \
            "Query parameters not documented"

    def test_api_has_pagination_documented(self):
        """API.md documents pagination."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "pagination" in content.lower() or "page" in content.lower(), \
            "Pagination not documented"


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
        assert re.search(r'curl.*-X\s+(GET|POST|PUT|DELETE|PATCH)', content), \
            "Curl examples missing HTTP method"

    def test_curl_examples_include_headers(self):
        """Curl examples include request headers."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Check for header indicators in curl examples
        assert re.search(r'-H\s*"', content) or "-H " in content, "Curl examples missing headers"

    def test_curl_examples_use_authentication(self):
        """Curl examples demonstrate authentication."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "API-Key" in content or "Bearer" in content or "Authorization" in content, \
            "Authentication not shown in curl examples"

    def test_curl_examples_show_request_body(self):
        """Curl examples show request body where applicable."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "-d" in content or "--data" in content, "Request body examples missing"


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

        for json_block in json_blocks[:3]:  # Test first 3 examples
            try:
                json.loads(json_block)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON example: {e}")

    def test_api_has_response_examples(self):
        """API.md contains response examples."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "Response" in content, "No response examples"
        assert "200" in content or "201" in content, "No success response examples"

    def test_api_has_error_response_examples(self):
        """API.md contains error response examples."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "error" in content.lower(), "No error response examples"
        assert "400" in content or "404" in content or "500" in content, \
            "No error status codes in examples"


class TestOpenAPIDocumentation:
    """Tests for OpenAPI/Swagger documentation."""

    def test_api_references_openapi(self):
        """API.md references OpenAPI specification."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "OpenAPI" in content or "Swagger" in content, \
            "OpenAPI/Swagger not mentioned"

    def test_api_has_openapi_endpoints(self):
        """API.md documents OpenAPI endpoints."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        assert "openapi.json" in content or "swagger" in content.lower() or "/docs" in content, \
            "OpenAPI endpoints not documented"


class TestArchitectureDocumentationContent:
    """Tests for ARCHITECTURE.md content validation."""

    def test_architecture_has_overview(self):
        """ARCHITECTURE.md contains system overview."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Overview" in content or "overview" in content.lower(), "Overview missing"

    def test_architecture_has_components_section(self):
        """ARCHITECTURE.md documents service components."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Component" in content or "component" in content.lower(), \
            "Components section not found"

    def test_architecture_documents_api_layer(self):
        """ARCHITECTURE.md documents API layer."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "API" in content, "API layer not documented"

    def test_architecture_documents_database_layer(self):
        """ARCHITECTURE.md documents data access layer."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Database" in content or "database" in content.lower() or "Data Access" in content, \
            "Database layer not documented"

    def test_architecture_documents_caching(self):
        """ARCHITECTURE.md documents caching strategy."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Cache" in content or "cache" in content.lower() or "Redis" in content, \
            "Caching not documented"

    def test_architecture_documents_messaging(self):
        """ARCHITECTURE.md documents message queue."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Message" in content or "message" in content.lower() or "Queue" in content or "RabbitMQ" in content, \
            "Messaging not documented"

    def test_architecture_has_data_flow_section(self):
        """ARCHITECTURE.md documents data flow."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Data Flow" in content or "data flow" in content.lower() or "Flow" in content, \
            "Data flow section missing"

    def test_architecture_documents_design_patterns(self):
        """ARCHITECTURE.md documents design patterns."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Pattern" in content or "pattern" in content.lower(), \
            "Design patterns not documented"


class TestArchitectureDiagrams:
    """Tests for architecture diagrams and visualizations."""

    def test_architecture_has_ascii_diagram(self):
        """ARCHITECTURE.md contains ASCII diagram."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        # Look for ASCII art indicators
        assert "├" in content or "├─" in content or "└" in content or "┌" in content or \
               "┐" in content or "│" in content, "No ASCII diagram found"

    def test_architecture_has_flow_diagrams(self):
        """ARCHITECTURE.md contains flow diagrams."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        # Look for flow indicators
        assert "→" in content or "->" in content or "↓" in content, \
            "No flow diagrams found"


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
        assert "Authentication" in content or "authentication" in content.lower(), \
            "Authentication not documented"

    def test_architecture_covers_authorization(self):
        """ARCHITECTURE.md covers authorization."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Authorization" in content or "authorization" in content.lower() or "RBAC" in content or "ABAC" in content, \
            "Authorization not documented"

    def test_architecture_covers_encryption(self):
        """ARCHITECTURE.md covers encryption."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Encryption" in content or "encryption" in content.lower() or "TLS" in content, \
            "Encryption not documented"

    def test_architecture_covers_input_validation(self):
        """ARCHITECTURE.md covers input validation."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Validation" in content or "validation" in content.lower() or "sanitization" in content.lower(), \
            "Input validation not documented"


class TestArchitectureScalability:
    """Tests for scalability documentation."""

    def test_architecture_documents_scalability(self):
        """ARCHITECTURE.md documents scalability."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Scalability" in content or "Scaling" in content or "scalable" in content.lower(), \
            "Scalability not documented"

    def test_architecture_covers_horizontal_scaling(self):
        """ARCHITECTURE.md covers horizontal scaling."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Horizontal" in content or "horizontal" in content.lower() or "stateless" in content.lower(), \
            "Horizontal scaling not documented"

    def test_architecture_covers_caching_strategy(self):
        """ARCHITECTURE.md covers caching for performance."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "cache" in content.lower() and ("performance" in content.lower() or "optimization" in content.lower()), \
            "Caching strategy not documented"


class TestArchitectureMonitoring:
    """Tests for monitoring and observability documentation."""

    def test_architecture_documents_monitoring(self):
        """ARCHITECTURE.md documents monitoring."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Monitor" in content or "monitor" in content.lower() or "Observ" in content, \
            "Monitoring not documented"

    def test_architecture_documents_logging(self):
        """ARCHITECTURE.md documents logging."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Log" in content or "log" in content.lower(), "Logging not documented"

    def test_architecture_documents_metrics(self):
        """ARCHITECTURE.md documents metrics collection."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Metrics" in content or "metrics" in content.lower() or "Prometheus" in content, \
            "Metrics not documented"

    def test_architecture_documents_tracing(self):
        """ARCHITECTURE.md documents distributed tracing."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        assert "Trace" in content or "trace" in content.lower() or "Jaeger" in content or "tracing" in content.lower(), \
            "Tracing not documented"


class TestDocumentationLinkReferences:
    """Tests for link validation and reference consistency."""

    def test_api_internal_references_valid(self):
        """API.md internal markdown links are formatted correctly."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Check for properly formatted markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        # All links should have text and href
        for text, href in links:
            assert len(text) > 0, "Link text is empty"
            assert len(href) > 0, "Link href is empty"

    def test_architecture_internal_references_valid(self):
        """ARCHITECTURE.md internal markdown links are formatted correctly."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        for text, href in links:
            assert len(text) > 0, "Link text is empty"
            assert len(href) > 0, "Link href is empty"


class TestDocumentationTableValidation:
    """Tests for markdown table validation."""

    def test_api_has_markdown_tables(self):
        """API.md contains markdown tables."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Look for table separator pattern
        assert re.search(r'\|.*\|.*\n.*\|.*-.*\|', content), "No markdown tables found"

    def test_api_tables_properly_formatted(self):
        """API.md tables are properly formatted."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Extract table lines
        tables = re.findall(r'(\|[^\n]+\n\|[-|\s]+\n(?:\|[^\n]+\n)+)', content)
        assert len(tables) > 0, "No valid markdown tables found"

        for table in tables[:3]:  # Validate first 3 tables
            lines = table.strip().split('\n')
            # First line is header
            header_cols = len(lines[0].split('|')) - 2
            # Validate each data row has same number of columns
            for line in lines[2:]:
                data_cols = len(line.split('|')) - 2
                assert data_cols == header_cols, f"Table has inconsistent columns: {header_cols} vs {data_cols}"

    def test_architecture_has_markdown_tables(self):
        """ARCHITECTURE.md contains markdown tables or code blocks."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        # Architecture doc may use ASCII diagrams instead of tables
        has_tables = re.search(r'\|.*\|.*\n.*\|.*-.*\|', content)
        has_code_blocks = "```" in content
        has_ascii_diagrams = "├" in content or "│" in content or "┌" in content
        assert has_tables or has_code_blocks or has_ascii_diagrams, \
            "No markdown tables, code blocks, or ASCII diagrams found"


class TestCodeExamples:
    """Tests for code examples in documentation."""

    def test_api_has_code_blocks(self):
        """API.md contains code blocks."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Look for markdown code blocks
        assert re.search(r'```[\w]*\n', content), "No code blocks found"

    def test_architecture_has_code_examples(self):
        """ARCHITECTURE.md contains code examples."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        # Look for code blocks (ASCII diagrams or actual code)
        assert "```" in content or "┌" in content, "No code examples found"

    def test_code_blocks_have_language_tags(self):
        """Code blocks should have language identifiers."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Count code blocks with language tags
        with_tags = len(re.findall(r'```[\w]+\n', content))
        total = len(re.findall(r'```\n', content)) + with_tags
        # Should have reasonable coverage of tagged blocks
        assert with_tags > 0, "No code blocks with language tags found"


class TestDocumentationCompleteness:
    """Tests for overall documentation completeness."""

    def test_both_documents_exist(self):
        """Both API.md and ARCHITECTURE.md exist."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        assert api_path.exists(), "API.md not found"
        assert arch_path.exists(), "ARCHITECTURE.md not found"

    def test_combined_documentation_size(self):
        """Combined documentation has sufficient content."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        api_content = api_path.read_text()
        arch_content = arch_path.read_text()
        combined_size = len(api_content) + len(arch_content)
        # Ensure substantial documentation (at least 5000 chars combined)
        assert combined_size > 5000, f"Documentation too small: {combined_size} chars"

    def test_api_mentions_service_name(self):
        """API.md references the service name."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Should mention service name using templating
        assert "{{ cookiecutter.service_" in content or "service" in content.lower(), \
            "Service name not referenced"

    def test_architecture_mentions_service_name(self):
        """ARCHITECTURE.md references the service name."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        # Should mention service name
        assert "{{ cookiecutter.service_" in content or "service" in content.lower(), \
            "Service name not referenced"


class TestDocumentationBestPractices:
    """Tests for documentation best practices."""

    def test_api_uses_consistent_formatting(self):
        """API.md uses consistent header formatting."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        content = api_path.read_text()
        # Check for consistent use of markdown headers
        h1_count = len(re.findall(r'^#[^#]', content, re.MULTILINE))
        h2_count = len(re.findall(r'^##[^#]', content, re.MULTILINE))
        h3_count = len(re.findall(r'^###[^#]', content, re.MULTILINE))

        # Should have hierarchical structure
        assert h1_count >= 1, "No top-level headers"
        assert h2_count > h1_count, "Missing subsections"

    def test_architecture_uses_consistent_formatting(self):
        """ARCHITECTURE.md uses consistent header formatting."""
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")
        content = arch_path.read_text()
        h1_count = len(re.findall(r'^#[^#]', content, re.MULTILINE))
        h2_count = len(re.findall(r'^##[^#]', content, re.MULTILINE))

        assert h1_count >= 1, "No top-level headers"
        assert h2_count > h1_count, "Missing subsections"

    def test_documentation_avoids_placeholder_content(self):
        """Documentation doesn't contain TODO or placeholder content."""
        api_path = Path("{{ cookiecutter.service_slug }}/API.md")
        arch_path = Path("{{ cookiecutter.service_slug }}/ARCHITECTURE.md")

        api_content = api_path.read_text()
        arch_content = arch_path.read_text()

        # Should not have generic TODOs (template variables are OK)
        assert "TODO: " not in api_content, "API.md contains TODO"
        assert "TODO: " not in arch_content, "ARCHITECTURE.md contains TODO"

        # Should not have placeholder text
        assert "[PLACEHOLDER]" not in api_content.upper(), "API.md contains placeholders"
        assert "[PLACEHOLDER]" not in arch_content.upper(), "ARCHITECTURE.md contains placeholders"


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
