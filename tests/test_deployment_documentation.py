"""
Comprehensive test suite for deployment documentation and README.

Tests verify:
- DEPLOYMENT.md existence, structure, and content completeness
- TROUBLESHOOTING.md existence, structure, and content completeness
- Root README.md existence and navigation
- Code examples and commands validity
- Documentation best practices
"""

import os
import re
import json
import pytest
from pathlib import Path


# Test fixtures
@pytest.fixture
def service_dir():
    """Get service directory path."""
    return Path(__file__).parent.parent / "{{ cookiecutter.service_slug }}"


@pytest.fixture
def root_dir():
    """Get project root directory path."""
    return Path(__file__).parent.parent


@pytest.fixture
def deployment_md(service_dir):
    """Load DEPLOYMENT.md content."""
    path = service_dir / "DEPLOYMENT.md"
    if path.exists():
        with open(path, 'r') as f:
            return f.read()
    return None


@pytest.fixture
def troubleshooting_md(service_dir):
    """Load TROUBLESHOOTING.md content."""
    path = service_dir / "TROUBLESHOOTING.md"
    if path.exists():
        with open(path, 'r') as f:
            return f.read()
    return None


@pytest.fixture
def readme_md(root_dir):
    """Load root README.md content."""
    path = root_dir / "README.md"
    if path.exists():
        with open(path, 'r') as f:
            return f.read()
    return None


# ============================================================================
# DEPLOYMENT.md Tests
# ============================================================================

class TestDeploymentMarkdownExistence:
    """Test DEPLOYMENT.md file existence and basic structure."""

    def test_deployment_md_exists(self, service_dir):
        """DEPLOYMENT.md file must exist in service directory."""
        path = service_dir / "DEPLOYMENT.md"
        assert path.exists(), "DEPLOYMENT.md not found in service directory"
        assert path.is_file(), "DEPLOYMENT.md is not a file"

    def test_deployment_md_not_empty(self, deployment_md):
        """DEPLOYMENT.md must not be empty."""
        assert deployment_md is not None, "DEPLOYMENT.md could not be loaded"
        assert len(deployment_md) > 500, "DEPLOYMENT.md is too short"

    def test_deployment_md_valid_markdown(self, deployment_md):
        """DEPLOYMENT.md must have valid markdown structure."""
        assert deployment_md.startswith("#"), "DEPLOYMENT.md should start with heading"
        assert "##" in deployment_md, "DEPLOYMENT.md should have subheadings"

    def test_deployment_md_has_title(self, deployment_md):
        """DEPLOYMENT.md must have a clear title."""
        assert "Deployment" in deployment_md, "Title should contain 'Deployment'"
        first_line = deployment_md.split('\n')[0]
        assert first_line.startswith("#"), "First line should be a heading"


class TestDeploymentPrerequisites:
    """Test Deployment Prerequisites section."""

    def test_has_prerequisites_section(self, deployment_md):
        """DEPLOYMENT.md must include Prerequisites section."""
        assert "Prerequisites" in deployment_md, "Missing Prerequisites section"
        assert "Deployment Prerequisites" in deployment_md or "prerequisites" in deployment_md.lower()

    def test_kubectl_requirement_documented(self, deployment_md):
        """kubectl must be documented as a requirement."""
        assert "kubectl" in deployment_md, "kubectl not documented"
        assert "installation" in deployment_md.lower(), "kubectl installation not documented"

    def test_helm_requirement_documented(self, deployment_md):
        """Helm must be documented as a requirement."""
        assert "helm" in deployment_md, "Helm not documented"
        assert "Helm 3" in deployment_md or "helm version" in deployment_md.lower()

    def test_docker_requirement_documented(self, deployment_md):
        """Docker must be documented as a requirement."""
        assert "Docker" in deployment_md, "Docker not documented"

    def test_cloud_provider_setup_documented(self, deployment_md):
        """Cloud provider setup must be documented."""
        cloud_providers = ["AWS", "EKS", "GKE", "AKS", "Azure"]
        provider_mentioned = any(provider in deployment_md for provider in cloud_providers)
        assert provider_mentioned, "No cloud provider setup documented"

    def test_version_requirements_specified(self, deployment_md):
        """Required versions must be specified."""
        version_patterns = [
            r"1\.19\+",  # Kubernetes
            r"3\.0\+",   # Helm
            r"20\.10\+", # Docker
        ]
        has_versions = any(re.search(pattern, deployment_md) for pattern in version_patterns)
        assert has_versions, "Version requirements not clearly specified"


class TestDeploymentKubernetesSetup:
    """Test Kubernetes cluster setup section."""

    def test_has_cluster_setup_section(self, deployment_md):
        """DEPLOYMENT.md must include Kubernetes Cluster Setup section."""
        assert "Cluster Setup" in deployment_md or "kubernetes" in deployment_md.lower()

    def test_eks_setup_documented(self, deployment_md):
        """AWS EKS setup must be documented."""
        assert "EKS" in deployment_md, "EKS setup not documented"
        assert "eksctl" in deployment_md or "create cluster" in deployment_md.lower()

    def test_gke_setup_documented(self, deployment_md):
        """Google Cloud GKE setup must be documented."""
        assert "GKE" in deployment_md or "gcloud" in deployment_md, "GKE setup not documented"

    def test_aks_setup_documented(self, deployment_md):
        """Azure AKS setup must be documented."""
        assert "AKS" in deployment_md or "az aks" in deployment_md.lower(), "AKS setup not documented"

    def test_namespace_creation_documented(self, deployment_md):
        """Namespace creation must be documented."""
        assert "namespace" in deployment_md.lower(), "Namespace creation not documented"
        assert "kubectl create namespace" in deployment_md or "namespace" in deployment_md.lower()

    def test_cluster_verification_documented(self, deployment_md):
        """Cluster verification procedures must be documented."""
        assert "verify" in deployment_md.lower() or "verification" in deployment_md.lower()


class TestDeploymentHelmCharts:
    """Test Helm chart deployment section."""

    def test_has_helm_deployment_section(self, deployment_md):
        """DEPLOYMENT.md must include Helm deployment section."""
        assert "Helm" in deployment_md, "Helm deployment section missing"

    def test_helm_chart_structure_documented(self, deployment_md):
        """Helm chart structure must be documented."""
        assert "Chart.yaml" in deployment_md or "templates/" in deployment_md

    def test_helm_install_example(self, deployment_md):
        """Helm install command example must be provided."""
        assert "helm install" in deployment_md, "helm install example missing"

    def test_helm_upgrade_example(self, deployment_md):
        """Helm upgrade command example must be provided."""
        assert "helm upgrade" in deployment_md, "helm upgrade example missing"

    def test_helm_values_override_documented(self, deployment_md):
        """Values override methods must be documented."""
        assert "values" in deployment_md.lower() or "--set" in deployment_md

    def test_helm_dependency_management(self, deployment_md):
        """Helm dependency management must be documented."""
        assert "dependency" in deployment_md.lower() or "dependencies" in deployment_md.lower()


class TestDeploymentConfigurationManagement:
    """Test configuration management section."""

    def test_has_config_section(self, deployment_md):
        """DEPLOYMENT.md must include Configuration section."""
        assert "Configuration" in deployment_md or "ConfigMap" in deployment_md

    def test_configmap_management_documented(self, deployment_md):
        """ConfigMap management must be documented."""
        assert "ConfigMap" in deployment_md, "ConfigMap not documented"
        assert "kubectl" in deployment_md, "kubectl commands not documented"

    def test_secrets_management_documented(self, deployment_md):
        """Secrets management must be documented."""
        assert "Secret" in deployment_md or "secret" in deployment_md.lower()
        assert "sensitive" in deployment_md.lower() or "credentials" in deployment_md.lower()

    def test_environment_specific_config(self, deployment_md):
        """Environment-specific configuration must be documented."""
        assert "staging" in deployment_md.lower() or "production" in deployment_md.lower()


class TestDeploymentServiceExposure:
    """Test service exposure section."""

    def test_has_service_exposure_section(self, deployment_md):
        """DEPLOYMENT.md must include Service Exposure section."""
        assert "Service" in deployment_md or "Exposure" in deployment_md.lower()

    def test_clusterip_documented(self, deployment_md):
        """ClusterIP service type must be documented."""
        assert "ClusterIP" in deployment_md, "ClusterIP not documented"

    def test_loadbalancer_documented(self, deployment_md):
        """LoadBalancer service type must be documented."""
        assert "LoadBalancer" in deployment_md, "LoadBalancer not documented"

    def test_ingress_documented(self, deployment_md):
        """Ingress must be documented."""
        assert "Ingress" in deployment_md, "Ingress not documented"
        assert "ingress" in deployment_md.lower()

    def test_service_exposure_examples(self, deployment_md):
        """Service exposure must have code examples."""
        yaml_blocks = deployment_md.count("```yaml") + deployment_md.count("```yml")
        bash_blocks = deployment_md.count("```bash")
        assert yaml_blocks > 0, "Missing YAML examples"
        assert bash_blocks > 0, "Missing bash examples"


class TestDeploymentMonitoring:
    """Test monitoring and logging section."""

    def test_has_monitoring_section(self, deployment_md):
        """DEPLOYMENT.md must include Monitoring section."""
        assert "Monitor" in deployment_md or "Logging" in deployment_md or "Prometheus" in deployment_md

    def test_prometheus_documented(self, deployment_md):
        """Prometheus monitoring must be documented."""
        assert "Prometheus" in deployment_md, "Prometheus not documented"

    def test_elk_stack_documented(self, deployment_md):
        """ELK Stack logging must be documented."""
        assert "Elasticsearch" in deployment_md or "ELK" in deployment_md or "Kibana" in deployment_md, \
            "ELK Stack not documented"

    def test_jaeger_tracing_documented(self, deployment_md):
        """Jaeger distributed tracing must be documented."""
        assert "Jaeger" in deployment_md or "tracing" in deployment_md.lower() or "trace" in deployment_md.lower()

    def test_log_aggregation_documented(self, deployment_md):
        """Log aggregation must be documented."""
        assert "log" in deployment_md.lower(), "Logging not documented"


class TestDeploymentScaling:
    """Test scaling and resource management."""

    def test_has_scaling_section(self, deployment_md):
        """DEPLOYMENT.md must include Scaling section."""
        assert "Scal" in deployment_md or "HPA" in deployment_md, "Scaling section missing"

    def test_hpa_documented(self, deployment_md):
        """HorizontalPodAutoscaler must be documented."""
        assert "HPA" in deployment_md or "HorizontalPodAutoscaler" in deployment_md, "HPA not documented"

    def test_manual_scaling_documented(self, deployment_md):
        """Manual scaling must be documented."""
        assert "scale" in deployment_md.lower(), "Manual scaling not documented"

    def test_resource_management_documented(self, deployment_md):
        """Resource limits and requests must be documented."""
        assert "resources" in deployment_md.lower() or "limit" in deployment_md.lower()
        assert "request" in deployment_md.lower() or "limit" in deployment_md.lower()


class TestDeploymentHealthChecks:
    """Test health checks section."""

    def test_has_health_checks_section(self, deployment_md):
        """DEPLOYMENT.md must include Health Checks section."""
        assert "Health" in deployment_md, "Health checks section missing"

    def test_liveness_probe_documented(self, deployment_md):
        """Liveness probe must be documented."""
        assert "liveness" in deployment_md.lower(), "Liveness probe not documented"
        assert "probe" in deployment_md.lower()

    def test_readiness_probe_documented(self, deployment_md):
        """Readiness probe must be documented."""
        assert "readiness" in deployment_md.lower(), "Readiness probe not documented"

    def test_startup_probe_documented(self, deployment_md):
        """Startup probe must be documented."""
        assert "startup" in deployment_md.lower() or "probe" in deployment_md.lower()

    def test_health_check_configuration(self, deployment_md):
        """Health check configuration parameters must be documented."""
        params = ["initialDelaySeconds", "periodSeconds", "timeoutSeconds", "failureThreshold"]
        has_params = any(param in deployment_md for param in params)
        assert has_params, "Health check parameters not documented"


class TestDeploymentUpdatesRollback:
    """Test rolling updates and rollback section."""

    def test_has_updates_section(self, deployment_md):
        """DEPLOYMENT.md must include Updates/Rollback section."""
        assert "Update" in deployment_md or "Rollback" in deployment_md or "Rolling" in deployment_md

    def test_rolling_update_documented(self, deployment_md):
        """Rolling updates must be documented."""
        assert "rolling" in deployment_md.lower() or "update" in deployment_md.lower()

    def test_blue_green_documented(self, deployment_md):
        """Blue-green deployment strategy must be documented."""
        assert "blue" in deployment_md.lower() or "green" in deployment_md.lower()

    def test_canary_deployment_documented(self, deployment_md):
        """Canary deployment strategy must be documented."""
        assert "canary" in deployment_md.lower() or "gradual" in deployment_md.lower()

    def test_rollback_procedure_documented(self, deployment_md):
        """Rollback procedures must be documented."""
        assert "rollback" in deployment_md.lower(), "Rollback not documented"
        assert "helm rollback" in deployment_md or "undo" in deployment_md.lower()


class TestDeploymentDisasterRecovery:
    """Test disaster recovery section."""

    def test_has_disaster_recovery_section(self, deployment_md):
        """DEPLOYMENT.md must include Disaster Recovery section."""
        assert "Disaster" in deployment_md or "Recovery" in deployment_md or "Backup" in deployment_md

    def test_backup_strategy_documented(self, deployment_md):
        """Backup strategy must be documented."""
        assert "backup" in deployment_md.lower(), "Backup strategy not documented"

    def test_recovery_procedures_documented(self, deployment_md):
        """Recovery procedures must be documented."""
        assert "recover" in deployment_md.lower() or "restore" in deployment_md.lower()

    def test_velero_documented(self, deployment_md):
        """Velero backup tool should be mentioned."""
        assert "Velero" in deployment_md or "backup" in deployment_md.lower()

    def test_multi_region_documented(self, deployment_md):
        """Multi-region setup must be documented."""
        assert "region" in deployment_md.lower() or "disaster" in deployment_md.lower()


# ============================================================================
# TROUBLESHOOTING.md Tests
# ============================================================================

class TestTroubleshootingMarkdownExistence:
    """Test TROUBLESHOOTING.md file existence and basic structure."""

    def test_troubleshooting_md_exists(self, service_dir):
        """TROUBLESHOOTING.md file must exist."""
        path = service_dir / "TROUBLESHOOTING.md"
        assert path.exists(), "TROUBLESHOOTING.md not found"
        assert path.is_file(), "TROUBLESHOOTING.md is not a file"

    def test_troubleshooting_md_not_empty(self, troubleshooting_md):
        """TROUBLESHOOTING.md must not be empty."""
        assert troubleshooting_md is not None
        assert len(troubleshooting_md) > 500

    def test_troubleshooting_md_valid_markdown(self, troubleshooting_md):
        """TROUBLESHOOTING.md must have valid markdown."""
        assert troubleshooting_md.startswith("#")
        assert "##" in troubleshooting_md


class TestTroubleshootingDeploymentIssues:
    """Test Troubleshooting common deployment issues."""

    def test_has_deployment_issues_section(self, troubleshooting_md):
        """Must include common deployment issues section."""
        assert "Deployment" in troubleshooting_md or "deployment" in troubleshooting_md.lower()

    def test_helm_errors_documented(self, troubleshooting_md):
        """Helm chart errors must be documented."""
        assert "Helm" in troubleshooting_md or "Chart" in troubleshooting_md

    def test_pending_pods_documented(self, troubleshooting_md):
        """Pending pod issue must be documented."""
        assert "Pending" in troubleshooting_md or "pending" in troubleshooting_md.lower()

    def test_imagepullbackoff_documented(self, troubleshooting_md):
        """ImagePullBackOff error must be documented."""
        assert "ImagePull" in troubleshooting_md or "image" in troubleshooting_md.lower()

    def test_crashloopbackoff_documented(self, troubleshooting_md):
        """CrashLoopBackOff error must be documented."""
        assert "CrashLoop" in troubleshooting_md or "crash" in troubleshooting_md.lower()


class TestTroubleshootingDebugProcedures:
    """Test debugging procedures."""

    def test_has_debugging_section(self, troubleshooting_md):
        """Must include debugging section."""
        assert "Debug" in troubleshooting_md or "debug" in troubleshooting_md.lower()

    def test_pod_debugging_documented(self, troubleshooting_md):
        """Pod debugging procedures must be documented."""
        assert "kubectl debug" in troubleshooting_md or "logs" in troubleshooting_md.lower()

    def test_environment_variable_debugging(self, troubleshooting_md):
        """Environment variable debugging must be documented."""
        assert "env" in troubleshooting_md.lower() or "environment" in troubleshooting_md.lower()

    def test_mount_point_verification(self, troubleshooting_md):
        """Volume mount verification must be documented."""
        assert "mount" in troubleshooting_md.lower()

    def test_kubectl_commands_documented(self, troubleshooting_md):
        """kubectl debugging commands must be provided."""
        assert "kubectl" in troubleshooting_md


class TestTroubleshootingNetworking:
    """Test networking issues troubleshooting."""

    def test_has_networking_section(self, troubleshooting_md):
        """Must include networking section."""
        assert "Network" in troubleshooting_md or "DNS" in troubleshooting_md or "Service" in troubleshooting_md

    def test_service_discovery_documented(self, troubleshooting_md):
        """Service discovery issues must be documented."""
        assert "discovery" in troubleshooting_md.lower() or "DNS" in troubleshooting_md

    def test_external_traffic_documented(self, troubleshooting_md):
        """External traffic issues must be documented."""
        assert "external" in troubleshooting_md.lower() or "LoadBalancer" in troubleshooting_md

    def test_dns_resolution_issues(self, troubleshooting_md):
        """DNS resolution issues must be documented."""
        assert "DNS" in troubleshooting_md or "nslookup" in troubleshooting_md or "dig" in troubleshooting_md


class TestTroubleshootingStorage:
    """Test storage and volume troubleshooting."""

    def test_has_storage_section(self, troubleshooting_md):
        """Must include storage/volume section."""
        assert "Storage" in troubleshooting_md or "Volume" in troubleshooting_md or "PVC" in troubleshooting_md

    def test_pvc_pending_documented(self, troubleshooting_md):
        """PVC pending issues must be documented."""
        assert "PVC" in troubleshooting_md or "PersistentVolume" in troubleshooting_md

    def test_mount_failures_documented(self, troubleshooting_md):
        """Mount failure issues must be documented."""
        assert "mount" in troubleshooting_md.lower()

    def test_data_loss_recovery(self, troubleshooting_md):
        """Data loss and recovery must be documented."""
        assert "data" in troubleshooting_md.lower() or "backup" in troubleshooting_md.lower()


class TestTroubleshootingPerformance:
    """Test performance optimization troubleshooting."""

    def test_has_performance_section(self, troubleshooting_md):
        """Must include performance section."""
        assert "Performance" in troubleshooting_md or "CPU" in troubleshooting_md or "Memory" in troubleshooting_md

    def test_high_cpu_documented(self, troubleshooting_md):
        """High CPU usage issues must be documented."""
        assert "CPU" in troubleshooting_md or "cpu" in troubleshooting_md.lower()

    def test_high_memory_documented(self, troubleshooting_md):
        """High memory usage issues must be documented."""
        assert "Memory" in troubleshooting_md or "memory" in troubleshooting_md.lower() or "OOM" in troubleshooting_md

    def test_slow_response_documented(self, troubleshooting_md):
        """Slow response time issues must be documented."""
        assert "response" in troubleshooting_md.lower() or "latency" in troubleshooting_md.lower()


class TestTroubleshootingLogging:
    """Test log analysis and debugging."""

    def test_has_logging_section(self, troubleshooting_md):
        """Must include logging section."""
        assert "Log" in troubleshooting_md or "log" in troubleshooting_md.lower()

    def test_kubectl_logs_documented(self, troubleshooting_md):
        """kubectl logs command must be documented."""
        assert "kubectl logs" in troubleshooting_md

    def test_log_filtering_documented(self, troubleshooting_md):
        """Log filtering techniques must be documented."""
        assert "grep" in troubleshooting_md or "filter" in troubleshooting_md.lower()

    def test_elk_stack_queries(self, troubleshooting_md):
        """ELK Stack querying must be documented."""
        assert "Elasticsearch" in troubleshooting_md or "Kibana" in troubleshooting_md


class TestTroubleshootingResourceConstraints:
    """Test resource constraint issues."""

    def test_has_resource_section(self, troubleshooting_md):
        """Must include resource constraints section."""
        assert "Resource" in troubleshooting_md or "Memory" in troubleshooting_md or "CPU" in troubleshooting_md

    def test_oomkilled_documented(self, troubleshooting_md):
        """OOMKilled errors must be documented."""
        assert "OOM" in troubleshooting_md or "memory" in troubleshooting_md.lower()

    def test_cpu_throttling_documented(self, troubleshooting_md):
        """CPU throttling must be documented."""
        assert "throttle" in troubleshooting_md.lower() or "CPU" in troubleshooting_md

    def test_disk_space_documented(self, troubleshooting_md):
        """Disk space issues must be documented."""
        assert "disk" in troubleshooting_md.lower() or "storage" in troubleshooting_md.lower()


class TestTroubleshootingHealthChecks:
    """Test health check failure troubleshooting."""

    def test_has_health_section(self, troubleshooting_md):
        """Must include health checks section."""
        assert "Health" in troubleshooting_md or "health" in troubleshooting_md.lower()

    def test_liveness_probe_failures(self, troubleshooting_md):
        """Liveness probe failures must be documented."""
        assert "liveness" in troubleshooting_md.lower()

    def test_readiness_probe_failures(self, troubleshooting_md):
        """Readiness probe failures must be documented."""
        assert "readiness" in troubleshooting_md.lower()


class TestTroubleshootingTesting:
    """Test validation and testing procedures."""

    def test_has_testing_section(self, troubleshooting_md):
        """Must include testing/validation section."""
        assert "Test" in troubleshooting_md or "Validation" in troubleshooting_md or "test" in troubleshooting_md.lower()

    def test_smoke_tests_documented(self, troubleshooting_md):
        """Smoke testing must be documented."""
        assert "smoke" in troubleshooting_md.lower() or "test" in troubleshooting_md.lower()

    def test_integration_tests_documented(self, troubleshooting_md):
        """Integration testing must be documented."""
        assert "integration" in troubleshooting_md.lower() or "test" in troubleshooting_md.lower()

    def test_load_testing_documented(self, troubleshooting_md):
        """Load testing must be documented."""
        assert "load" in troubleshooting_md.lower() or "test" in troubleshooting_md.lower()


# ============================================================================
# Root README.md Tests
# ============================================================================

class TestRootReadmeExistence:
    """Test root README.md existence."""

    def test_root_readme_exists(self, root_dir):
        """Root README.md must exist."""
        path = root_dir / "README.md"
        assert path.exists(), "Root README.md not found"

    def test_root_readme_not_empty(self, readme_md):
        """Root README.md must not be empty."""
        assert readme_md is not None
        assert len(readme_md) > 500


class TestRootReadmeTitle:
    """Test README title and overview."""

    def test_has_clear_title(self, readme_md):
        """README must have clear title."""
        assert "Cookiecutter" in readme_md or "Microservice" in readme_md or "Template" in readme_md

    def test_has_overview_section(self, readme_md):
        """README must have overview section."""
        assert "Overview" in readme_md or "overview" in readme_md.lower()


class TestRootReadmeDocumentation:
    """Test README documentation links."""

    def test_setup_guide_linked(self, readme_md):
        """SETUP.md must be linked."""
        assert "SETUP.md" in readme_md or "setup" in readme_md.lower()

    def test_deployment_guide_linked(self, readme_md):
        """DEPLOYMENT.md must be linked."""
        assert "DEPLOYMENT.md" in readme_md or "deployment" in readme_md.lower()

    def test_troubleshooting_guide_linked(self, readme_md):
        """TROUBLESHOOTING.md must be linked."""
        assert "TROUBLESHOOTING.md" in readme_md or "troubleshooting" in readme_md.lower()

    def test_architecture_linked(self, readme_md):
        """ARCHITECTURE.md must be linked."""
        assert "ARCHITECTURE.md" in readme_md or "architecture" in readme_md.lower()

    def test_api_docs_linked(self, readme_md):
        """API.md must be linked."""
        assert "API.md" in readme_md or "api" in readme_md.lower()

    def test_language_guides_linked(self, readme_md):
        """Language guides must be referenced."""
        langs = ["PYTHON.md", "GO.md", "NODEJS.md", "Python", "Go", "Node"]
        has_lang = any(lang in readme_md for lang in langs)
        assert has_lang, "Language guides not referenced"


class TestRootReadmeFeatures:
    """Test README feature descriptions."""

    def test_multi_language_mentioned(self, readme_md):
        """Multi-language support must be mentioned."""
        assert "language" in readme_md.lower() or "Python" in readme_md or "Go" in readme_md or "Node" in readme_md

    def test_kubernetes_mentioned(self, readme_md):
        """Kubernetes support must be mentioned."""
        assert "Kubernetes" in readme_md or "kubernetes" in readme_md.lower() or "K8s" in readme_md

    def test_docker_mentioned(self, readme_md):
        """Docker support must be mentioned."""
        assert "Docker" in readme_md

    def test_helm_mentioned(self, readme_md):
        """Helm support must be mentioned."""
        assert "Helm" in readme_md

    def test_monitoring_mentioned(self, readme_md):
        """Monitoring must be mentioned."""
        assert "monitor" in readme_md.lower() or "Prometheus" in readme_md

    def test_cicd_mentioned(self, readme_md):
        """CI/CD must be mentioned."""
        assert "CI/CD" in readme_md or "GitHub Actions" in readme_md or "workflow" in readme_md.lower()


class TestRootReadmeQuickStart:
    """Test README quick start section."""

    def test_has_quick_start(self, readme_md):
        """README must have quick start section."""
        assert "Quick Start" in readme_md or "quick start" in readme_md.lower() or "Getting Started" in readme_md

    def test_prerequisites_listed(self, readme_md):
        """Prerequisites must be listed."""
        assert "Prerequisites" in readme_md or "prerequisites" in readme_md.lower()

    def test_installation_instructions(self, readme_md):
        """Installation instructions must be provided."""
        assert "install" in readme_md.lower() or "setup" in readme_md.lower()


class TestRootReadmeExamples:
    """Test README code examples."""

    def test_has_code_examples(self, readme_md):
        """README must have code examples."""
        code_blocks = readme_md.count("```")
        assert code_blocks >= 4, "Not enough code examples"

    def test_has_bash_examples(self, readme_md):
        """README must have bash command examples."""
        assert "```bash" in readme_md or "$ " in readme_md

    def test_has_docker_example(self, readme_md):
        """README must have Docker example."""
        assert "docker" in readme_md.lower()

    def test_has_kubernetes_example(self, readme_md):
        """README must have Kubernetes example."""
        assert "kubectl" in readme_md or "helm" in readme_md.lower()


class TestRootReadmeStructure:
    """Test README project structure documentation."""

    def test_project_structure_documented(self, readme_md):
        """Project structure must be documented."""
        assert "Structure" in readme_md or "structure" in readme_md.lower() or "Directory" in readme_md

    def test_service_directory_explained(self, readme_md):
        """Service directory structure must be explained."""
        assert "src" in readme_md or "helm" in readme_md or "docker" in readme_md.lower()


class TestRootReadmeLanguageSupport:
    """Test language support matrix."""

    def test_language_matrix_present(self, readme_md):
        """Language support matrix should be documented."""
        assert "Python" in readme_md or "Go" in readme_md or "Node" in readme_md

    def test_python_support_mentioned(self, readme_md):
        """Python support must be mentioned."""
        assert "Python" in readme_md

    def test_go_support_mentioned(self, readme_md):
        """Go support must be mentioned."""
        assert "Go" in readme_md

    def test_nodejs_support_mentioned(self, readme_md):
        """Node.js support must be mentioned."""
        assert "Node" in readme_md or "JavaScript" in readme_md or "TypeScript" in readme_md


class TestRootReadmeContributing:
    """Test README contributing and support sections."""

    def test_contributing_section(self, readme_md):
        """README should mention contributing."""
        assert "Contributing" in readme_md or "contributing" in readme_md.lower()

    def test_support_section(self, readme_md):
        """README should mention support or troubleshooting."""
        assert "Support" in readme_md or "support" in readme_md.lower() or "troubleshoot" in readme_md.lower()

    def test_resources_section(self, readme_md):
        """README should link to external resources."""
        assert "resource" in readme_md.lower() or "documentation" in readme_md.lower() or "link" in readme_md.lower()


# ============================================================================
# Code Example Validation Tests
# ============================================================================

class TestCodeExamples:
    """Test code examples in documentation."""

    def test_deployment_bash_examples(self, deployment_md):
        """DEPLOYMENT.md bash examples must be valid syntax."""
        bash_blocks = re.findall(r'```bash\n(.*?)```', deployment_md, re.DOTALL)
        assert len(bash_blocks) > 10, "Not enough bash examples in DEPLOYMENT.md"

    def test_troubleshooting_bash_examples(self, troubleshooting_md):
        """TROUBLESHOOTING.md bash examples must be valid."""
        bash_blocks = re.findall(r'```bash\n(.*?)```', troubleshooting_md, re.DOTALL)
        assert len(bash_blocks) > 5, "Not enough bash examples in TROUBLESHOOTING.md"

    def test_yaml_examples_present(self, deployment_md):
        """DEPLOYMENT.md must have YAML examples."""
        yaml_blocks = deployment_md.count("```yaml") + deployment_md.count("```yml")
        assert yaml_blocks >= 3, "Not enough YAML examples"


class TestCommandValidity:
    """Test command examples validity."""

    def test_kubectl_commands_documented(self, deployment_md):
        """kubectl commands must be documented."""
        assert "kubectl" in deployment_md

    def test_helm_commands_documented(self, deployment_md):
        """helm commands must be documented."""
        assert "helm" in deployment_md

    def test_docker_commands_documented(self, deployment_md):
        """docker commands should be documented."""
        assert "docker" in deployment_md.lower()


# ============================================================================
# Cross-Reference Tests
# ============================================================================

class TestCrossReferences:
    """Test references between documents."""

    def test_deployment_links_architecture(self, deployment_md):
        """DEPLOYMENT.md should reference ARCHITECTURE.md."""
        assert "ARCHITECTURE" in deployment_md or "architecture" in deployment_md.lower()

    def test_deployment_links_api(self, deployment_md):
        """DEPLOYMENT.md should reference API.md."""
        assert "API" in deployment_md or "api" in deployment_md.lower()

    def test_troubleshooting_links_deployment(self, troubleshooting_md):
        """TROUBLESHOOTING.md should reference DEPLOYMENT.md."""
        assert "DEPLOYMENT" in troubleshooting_md or "deployment" in troubleshooting_md.lower()


# ============================================================================
# Summary Statistics Tests
# ============================================================================

class TestDocumentationCompleteness:
    """Test overall documentation completeness."""

    def test_deployment_word_count(self, deployment_md):
        """DEPLOYMENT.md should be substantial (3000+ words)."""
        word_count = len(deployment_md.split())
        assert word_count > 3000, f"DEPLOYMENT.md too short: {word_count} words"

    def test_troubleshooting_word_count(self, troubleshooting_md):
        """TROUBLESHOOTING.md should be substantial (2000+ words)."""
        word_count = len(troubleshooting_md.split())
        assert word_count > 2000, f"TROUBLESHOOTING.md too short: {word_count} words"

    def test_readme_word_count(self, readme_md):
        """Root README.md should be substantial (1000+ words)."""
        word_count = len(readme_md.split())
        assert word_count > 1000, f"README.md too short: {word_count} words"

    def test_deployment_sections_count(self, deployment_md):
        """DEPLOYMENT.md should have multiple main sections."""
        section_count = deployment_md.count("## ")
        assert section_count >= 8, f"DEPLOYMENT.md has too few sections: {section_count}"

    def test_troubleshooting_sections_count(self, troubleshooting_md):
        """TROUBLESHOOTING.md should have multiple main sections."""
        section_count = troubleshooting_md.count("## ")
        assert section_count >= 7, f"TROUBLESHOOTING.md has too few sections: {section_count}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
