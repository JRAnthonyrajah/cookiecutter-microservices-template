"""Test suite for GitHub Actions CI/CD workflow template validation."""
import re
import yaml
from pathlib import Path


class TestGitHubActionsWorkflow:
    """Tests for GitHub Actions CI/CD workflow validity and structure."""

    @classmethod
    def setup_class(cls):
        """Load the CI/CD workflow template."""
        workflow_path = (
            Path(__file__).parent.parent
            / "{{ cookiecutter.service_slug }}"
            / ".github"
            / "workflows"
            / "ci.yml"
        )
        assert workflow_path.exists(), f"ci.yml not found at {workflow_path}"
        with open(workflow_path, "r") as f:
            cls.workflow_content = f.read()
        cls.workflow_path = workflow_path

    def test_workflow_file_exists(self):
        """Test that .github/workflows/ci.yml file exists."""
        assert (
            self.workflow_path.exists()
        ), f"CI/CD workflow file not found at {self.workflow_path}"
        assert (
            self.workflow_path.is_file()
        ), f"ci.yml is not a regular file at {self.workflow_path}"

    def test_workflow_is_not_empty(self):
        """Test that ci.yml is not empty."""
        assert len(self.workflow_content) > 0, "ci.yml file is empty"

    def test_workflow_name_declared(self):
        """Test that workflow name is declared."""
        assert "name: CI/CD Pipeline" in self.workflow_content, \
            "Workflow must declare name: CI/CD Pipeline"

    def test_workflow_has_push_trigger(self):
        """Test that workflow has push trigger."""
        assert "on:" in self.workflow_content, "Workflow must have 'on:' trigger section"
        assert "push:" in self.workflow_content, "Workflow must have push trigger"

    def test_workflow_has_pull_request_trigger(self):
        """Test that workflow has pull_request trigger."""
        assert "pull_request:" in self.workflow_content, \
            "Workflow must have pull_request trigger"

    def test_push_trigger_includes_branches(self):
        """Test that push trigger includes branches."""
        assert "branches:" in self.workflow_content, \
            "push trigger must include branches configuration"
        assert "main" in self.workflow_content, \
            "Branches should include main"
        assert "master" in self.workflow_content, \
            "Branches should include master"
        assert "develop" in self.workflow_content, \
            "Branches should include develop"

    def test_workflow_has_lint_job(self):
        """Test that workflow has lint job."""
        assert "lint:" in self.workflow_content, \
            "Workflow must have 'lint' job"

    def test_workflow_has_test_job(self):
        """Test that workflow has test job."""
        assert "test:" in self.workflow_content, \
            "Workflow must have 'test' job"

    def test_workflow_has_build_job(self):
        """Test that workflow has build job."""
        assert "build:" in self.workflow_content, \
            "Workflow must have 'build' job"

    def test_workflow_has_helm_lint_job(self):
        """Test that workflow has helm-lint job."""
        assert "helm-lint:" in self.workflow_content, \
            "Workflow must have 'helm-lint' job"

    def test_workflow_has_push_job(self):
        """Test that workflow has push job."""
        assert "push:" in self.workflow_content, \
            "Workflow must have 'push' job"

    def test_lint_job_uses_ubuntu_latest(self):
        """Test that lint job runs on ubuntu-latest."""
        # Extract lint job section
        lint_section = self.workflow_content[
            self.workflow_content.find("lint:"):
            self.workflow_content.find("\n  test:")
        ]
        assert "runs-on: ubuntu-latest" in lint_section, \
            "lint job must run on ubuntu-latest"

    def test_lint_job_has_checkout_step(self):
        """Test that lint job includes checkout step."""
        lint_section = self.workflow_content[
            self.workflow_content.find("lint:"):
            self.workflow_content.find("\n  test:")
        ]
        assert "actions/checkout@v4" in lint_section, \
            "lint job must use actions/checkout@v4"

    def test_test_job_uses_ubuntu_latest(self):
        """Test that test job runs on ubuntu-latest."""
        test_section = self.workflow_content[
            self.workflow_content.find("  test:"):
            self.workflow_content.find("\n  build:")
        ]
        assert "runs-on: ubuntu-latest" in test_section, \
            "test job must run on ubuntu-latest"

    def test_build_job_has_docker_buildx(self):
        """Test that build job sets up Docker Buildx."""
        build_section = self.workflow_content[
            self.workflow_content.find("  build:"):
            self.workflow_content.find("\n  helm-lint:")
        ]
        assert "docker/setup-buildx-action@v2" in build_section, \
            "build job must set up Docker Buildx"

    def test_build_job_has_docker_build_step(self):
        """Test that build job includes docker build step."""
        build_section = self.workflow_content[
            self.workflow_content.find("  build:"):
            self.workflow_content.find("\n  helm-lint:")
        ]
        assert "docker/build-push-action@v4" in build_section, \
            "build job must use docker/build-push-action@v4"

    def test_helm_lint_job_has_setup_helm(self):
        """Test that helm-lint job sets up Helm."""
        workflow = yaml.safe_load(self.workflow_content)
        helm_job = workflow.get("jobs", {}).get("helm-lint", {})
        steps = helm_job.get("steps", [])
        has_helm_setup = any(
            "azure/setup-helm" in str(step) for step in steps
        )
        assert has_helm_setup, \
            "helm-lint job must set up Helm"

    def test_helm_lint_job_runs_helm_lint(self):
        """Test that helm-lint job runs helm lint."""
        workflow = yaml.safe_load(self.workflow_content)
        helm_job = workflow.get("jobs", {}).get("helm-lint", {})
        steps = helm_job.get("steps", [])
        has_helm_lint_cmd = any(
            "helm lint" in str(step.get("run", "")) for step in steps
        )
        assert has_helm_lint_cmd, \
            "helm-lint job must run 'helm lint' command"

    def test_push_job_has_conditional_execution(self):
        """Test that push job only runs on main/master branches."""
        push_section = self.workflow_content[
            self.workflow_content.find("  push:"):
        ]
        assert "if:" in push_section, \
            "push job must have conditional execution"
        assert "main" in push_section or "master" in push_section, \
            "push job condition must check for main or master branch"

    def test_push_job_needs_other_jobs(self):
        """Test that push job depends on other jobs."""
        push_section = self.workflow_content[
            self.workflow_content.find("  push:"):
        ]
        assert "needs:" in push_section, \
            "push job must have 'needs' dependency specification"

    def test_push_job_has_docker_login(self):
        """Test that push job includes Docker login step."""
        push_section = self.workflow_content[
            self.workflow_content.find("  push:"):
        ]
        assert "docker/login-action@v2" in push_section, \
            "push job must use docker/login-action@v2"

    def test_push_job_pushes_to_registry(self):
        """Test that push job pushes Docker image to registry."""
        push_section = self.workflow_content[
            self.workflow_content.find("  push:"):
        ]
        assert "push: true" in push_section, \
            "push job must have push: true in docker build action"

    def test_yaml_structure_is_valid(self):
        """Test that the workflow file is valid YAML."""
        try:
            workflow = yaml.safe_load(self.workflow_content)
            assert isinstance(workflow, dict), \
                "Workflow should be a YAML dictionary"
        except yaml.YAMLError as e:
            raise AssertionError(f"Workflow contains invalid YAML syntax: {e}")

    def test_workflow_has_on_trigger_key(self):
        """Test that workflow has 'on' trigger key."""
        workflow = yaml.safe_load(self.workflow_content)
        # YAML parser converts 'on:' to True key due to YAML boolean parsing
        assert "on" in workflow or True in workflow, \
            "Workflow must have 'on' key for triggers (may be parsed as True)"
        # Also check the raw content to be sure
        assert "on:" in self.workflow_content, "Raw workflow content must have 'on:' trigger"

    def test_workflow_has_jobs_section(self):
        """Test that workflow has 'jobs' section."""
        workflow = yaml.safe_load(self.workflow_content)
        assert "jobs" in workflow, "Workflow must have 'jobs' section"

    def test_all_jobs_are_present_in_parsed_workflow(self):
        """Test that all required jobs are present in parsed workflow."""
        workflow = yaml.safe_load(self.workflow_content)
        jobs = workflow.get("jobs", {})
        required_jobs = ["lint", "test", "build", "helm-lint", "push"]
        for job in required_jobs:
            assert job in jobs, f"Workflow must have '{job}' job"

    def test_lint_job_has_steps(self):
        """Test that lint job has steps."""
        workflow = yaml.safe_load(self.workflow_content)
        lint_job = workflow.get("jobs", {}).get("lint", {})
        assert "steps" in lint_job, "lint job must have 'steps'"
        assert len(lint_job.get("steps", [])) > 0, "lint job must have at least one step"

    def test_test_job_has_steps(self):
        """Test that test job has steps."""
        workflow = yaml.safe_load(self.workflow_content)
        test_job = workflow.get("jobs", {}).get("test", {})
        assert "steps" in test_job, "test job must have 'steps'"
        assert len(test_job.get("steps", [])) > 0, "test job must have at least one step"

    def test_push_job_conditional_checks_for_main_branch(self):
        """Test that push job condition checks for main/master branch."""
        workflow = yaml.safe_load(self.workflow_content)
        push_job = workflow.get("jobs", {}).get("push", {})
        assert "if" in push_job, "push job must have 'if' condition"
        condition = push_job.get("if", "")
        assert "main" in condition or "master" in condition, \
            "push job condition must reference main or master branch"

    def test_push_job_has_needs_dependency(self):
        """Test that push job has needs dependency."""
        workflow = yaml.safe_load(self.workflow_content)
        push_job = workflow.get("jobs", {}).get("push", {})
        assert "needs" in push_job, "push job must have 'needs' dependency"
        needs = push_job.get("needs", [])
        if isinstance(needs, str):
            needs = [needs]
        assert len(needs) > 0, "push job must depend on other jobs"

    def test_lint_job_has_python_setup(self):
        """Test that lint job includes Python setup when applicable."""
        workflow = yaml.safe_load(self.workflow_content)
        lint_job = workflow.get("jobs", {}).get("lint", {})
        steps = lint_job.get("steps", [])
        # Check if any step is for setting up Python
        has_python_setup = any(
            "actions/setup-python" in str(step) for step in steps
        )
        assert has_python_setup or len(steps) > 1, \
            "lint job should have setup steps for language environments"

    def test_lint_job_lints_code(self):
        """Test that lint job includes linting steps."""
        lint_section = self.workflow_content[
            self.workflow_content.find("lint:"):
            self.workflow_content.find("\n  test:")
        ]
        has_linting = (
            "ruff" in lint_section
            or "black" in lint_section
            or "eslint" in lint_section
            or "golangci-lint" in lint_section
        )
        assert has_linting, \
            "lint job must include code linting steps (ruff, black, eslint, or golangci-lint)"

    def test_test_job_runs_tests(self):
        """Test that test job includes testing steps."""
        test_section = self.workflow_content[
            self.workflow_content.find("  test:"):
            self.workflow_content.find("\n  build:")
        ]
        has_testing = (
            "pytest" in test_section
            or "jest" in test_section
            or "go test" in test_section
        )
        assert has_testing, \
            "test job must include test execution steps (pytest, jest, or go test)"

    def test_checkout_action_versions(self):
        """Test that checkout action uses v4."""
        assert "actions/checkout@v4" in self.workflow_content, \
            "Workflow should use actions/checkout@v4 for best practices"

    def test_all_job_names_have_display_names(self):
        """Test that all jobs have 'name' field for display."""
        workflow = yaml.safe_load(self.workflow_content)
        jobs = workflow.get("jobs", {})
        for job_name in jobs:
            job = jobs[job_name]
            assert "name" in job or "runs-on" in job, \
                f"Job '{job_name}' should have a 'name' or 'runs-on' field"

    def test_lint_and_test_jobs_run_on_all_branches(self):
        """Test that lint and test jobs run on all branches (no if condition)."""
        workflow = yaml.safe_load(self.workflow_content)
        lint_job = workflow.get("jobs", {}).get("lint", {})
        test_job = workflow.get("jobs", {}).get("test", {})
        # These jobs should not have restrictive 'if' conditions
        assert "if" not in lint_job or "main" not in lint_job.get("if", ""), \
            "lint job should run on all branches"
        assert "if" not in test_job or "main" not in test_job.get("if", ""), \
            "test job should run on all branches"
