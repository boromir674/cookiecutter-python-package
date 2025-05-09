"""Test building our Source Distribution results in expected File System"""

import typing as t
from pathlib import Path

import pytest


# EXPECTATIONS as fixture
@pytest.fixture(scope="session")
def sdist_expected_correct_file_structure():
    METADATA_SHIPPED_IN_TEMPLATE_PROJECT = (
        'pyproject.toml',
        'README.rst',
        'CHANGELOG.rst',
        'LICENSE',
        'CONTRIBUTING.md',
    )
    SRC = tuple(
        [
            'src/cookiecutter_python/{{ cookiecutter.project_slug }}/' + x
            for x in METADATA_SHIPPED_IN_TEMPLATE_PROJECT
        ]
    ) + (
        # COOKIECUTTER TEMPLATE
        'src/cookiecutter_python/cookiecutter.json',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/src/{{ cookiecutter.pkg_name }}/__init__.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/src/{{ cookiecutter.pkg_name }}/__main__.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/src/{{ cookiecutter.pkg_name }}/cli.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/src/{{ cookiecutter.pkg_name }}/_logging.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/src/{{ cookiecutter.pkg_name }}/fixtures.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/src/{{ cookiecutter.pkg_name }}/py.typed',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/tests/conftest.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/tests/smoke_test.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/tests/test_cli.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/tests/test_invoking_cli.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/tests/test_my_fixture.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.coveragerc',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.github/labeler.yml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.github/workflows/cicd.yml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.github/workflows/codecov-upload.yml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.github/workflows/labeler.yaml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.github/workflows/policy_lint.yml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.github/workflows/signal-deploy.yml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.github/workflows/test.yaml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.gitignore',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.prospector.yml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.pylintrc',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/.readthedocs.yml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/Dockerfile',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/MANIFEST.in',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/assets/docker_off.png',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/build-process_DAG.md',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/cicd.md',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/cicd_mermaid.md',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/dev_guides/docker.md',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/dev_guides/index.md',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/dockerfile_mermaid.md',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/index.md',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "mkdocs" %}docs{% else %}PyGen_TO_DELETE{% endif %}/tags.md',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/Makefile',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/conf.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/contents/10_introduction.rst',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/contents/20_why_this_package.rst',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/contents/30_usage.rst',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/contents/40_modules.rst',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/contents/{{ cookiecutter.pkg_name }}.rst',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/index.rst',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/make.bat',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/{% if cookiecutter.docs_builder == "sphinx" %}docs{% else %}PyGen_TO_DELETE{% endif %}/spelling_wordlist.txt',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/mkdocs.yml',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/scripts/gen_api_refs_pages.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/scripts/parse_version.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/scripts/visualize-dockerfile.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/scripts/visualize-ga-workflow.py',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/setup.cfg',
        'src/cookiecutter_python/{{ cookiecutter.project_slug }}/tox.ini',
        'src/cookiecutter_python/_find_lib.py',
        'src/cookiecutter_python/__init__.py',
        'src/cookiecutter_python/__main__.py',
        'src/cookiecutter_python/cli.py',
        'src/cookiecutter_python/exceptions.py',
        'src/cookiecutter_python/utils.py',
        'src/cookiecutter_python/backend/check_server_result.py',
        'src/cookiecutter_python/backend/error_handling/handler_builder.py',
        'src/cookiecutter_python/backend/error_handling/__init__.py',
        'src/cookiecutter_python/backend/generator/generator.py',
        'src/cookiecutter_python/backend/generator/__init__.py',
        'src/cookiecutter_python/backend/helpers.py',
        'src/cookiecutter_python/backend/hosting_services/check_engine.py',
        'src/cookiecutter_python/backend/hosting_services/checker.py',
        'src/cookiecutter_python/backend/hosting_services/checkers.py',
        'src/cookiecutter_python/backend/hosting_services/check_service.py',
        'src/cookiecutter_python/backend/hosting_services/check_web_hosting_service.py',
        'src/cookiecutter_python/backend/hosting_services/exceptions.py',
        'src/cookiecutter_python/backend/hosting_services/extract_name.py',
        'src/cookiecutter_python/backend/hosting_services/handle_hosting_service_check.py',
        'src/cookiecutter_python/backend/hosting_services/handler.py',
        'src/cookiecutter_python/backend/hosting_services/__init__.py',
        'src/cookiecutter_python/backend/hosting_services/value_extractor.py',
        'src/cookiecutter_python/backend/hosting_services/web_hosting_service.py',
        'src/cookiecutter_python/backend/__init__.py',
        'src/cookiecutter_python/backend/load_config.py',
        'src/cookiecutter_python/backend/main.py',
        'src/cookiecutter_python/backend/post_main.py',
        'src/cookiecutter_python/backend/pre_main.py',
        'src/cookiecutter_python/backend/proxy.py',
        'src/cookiecutter_python/backend/request.py',
        'src/cookiecutter_python/backend/sanitization/__init__.py',
        'src/cookiecutter_python/backend/sanitization/input_sanitization.py',
        'src/cookiecutter_python/backend/sanitization/interpreters_support.py',
        'src/cookiecutter_python/backend/sanitization/string_sanitizers/base_sanitizer.py',
        'src/cookiecutter_python/backend/sanitization/string_sanitizers/__init__.py',
        'src/cookiecutter_python/backend/sanitization/string_sanitizers/sanitize_reg_input.py',
        'src/cookiecutter_python/backend/sanitization/string_sanitizers/sanitize_reg_module_name.py',
        'src/cookiecutter_python/backend/sanitization/string_sanitizers/sanitize_reg_version.py',
        'src/cookiecutter_python/backend/user_config_proxy.py',
        'src/cookiecutter_python/cli_handlers.py',
        'src/cookiecutter_python/exceptions.py',
        'src/cookiecutter_python/handle/dialogs/dialog.py',
        'src/cookiecutter_python/handle/dialogs/__init__.py',
        'src/cookiecutter_python/handle/dialogs/lib/__init__.py',
        'src/cookiecutter_python/handle/dialogs/lib/project_name.py',
        'src/cookiecutter_python/handle/__init__.py',
        'src/cookiecutter_python/handle/interactive_cli_pipeline.py',
        'src/cookiecutter_python/handle/node_base.py',
        'src/cookiecutter_python/handle/node_factory.py',
        'src/cookiecutter_python/handle/node_interface.py',
        'src/cookiecutter_python/hooks/__init__.py',
        'src/cookiecutter_python/hooks/post_gen_project.py',
        'src/cookiecutter_python/hooks/pre_gen_project.py',
        'src/cookiecutter_python/__init__.py',
        'src/cookiecutter_python/_logging_config.py',
        'src/cookiecutter_python/_logging.py',
        'src/cookiecutter_python/__main__.py',
        'src/cookiecutter_python/py.typed',
        'src/cookiecutter_python/utils.py',
        # 'src/stubs/cookiecutter/config.pyi',
        # 'src/stubs/cookiecutter/exceptions.pyi',
        # 'src/stubs/cookiecutter/generate.pyi',
        # 'src/stubs/cookiecutter/__init__.pyi',
        # 'src/stubs/cookiecutter/main.pyi',
        # 'src/stubs/git/exc.pyi',
        # 'src/stubs/git/__init__.pyi',
        # 'src/stubs/requests_futures/__init__.pyi',
        # 'src/stubs/requests_futures/sessions.pyi',
    )
    TESTS = (
        'tests/test_git_sdk.py',
        'tests/test_git_porcelain.py',
        'tests/test_is_repo_clean_function.py',
        'tests/biskotaki_ci/conftest.py',
        'tests/test_load_util.py',
        'tests/biskotaki_ci/snapshot/biskotaki_ci_no_input/test_build_creates_artifacts.py',
        'tests/biskotaki_ci/snapshot/biskotaki_ci_no_input/test_lint_passes.py',
        'tests/biskotaki_ci/snapshot/test_matches_biskotaki_runtime_gen.py',
        'tests/biskotaki_ci/snapshot/test_valid_ci_config.py',
        'tests/biskotaki_ci/test_logging.py',
        'tests/biskotaki_ci/test_regression_biskotaki.py',
        'tests/conftest.py',
        'tests/data/biskotaki-with-no-docs-specs.yaml',
        'tests/data/biskotaki-without-interpreters.yaml',
        'tests/data/correct_python_package_names.txt',
        'tests/data/gold-standard.yml',
        'tests/data/pytest-fixture.yaml',
        'tests/data/rendering/only_list_template/cookiecutter.json',
        'tests/data/rendering/only_list_template/{{ cookiecutter.project_dir_name }}/a.txt',
        'tests/data/rendering/only_list_template/hooks/pre_gen_project.py',
        'tests/data/rendering/user_config.yml',
        'tests/data/snapshots/biskotaki-gold-standard/CHANGELOG.rst',
        'tests/data/snapshots/biskotaki-gold-standard/CONTRIBUTING.md',
        'tests/data/snapshots/biskotaki-gold-standard/Dockerfile',
        'tests/data/snapshots/biskotaki-gold-standard/docs/assets/docker_off.png',
        'tests/data/snapshots/biskotaki-gold-standard/docs/build-process_DAG.md',
        'tests/data/snapshots/biskotaki-gold-standard/docs/cicd.md',
        'tests/data/snapshots/biskotaki-gold-standard/docs/cicd_mermaid.md',
        'tests/data/snapshots/biskotaki-gold-standard/docs/dev_guides/docker.md',
        'tests/data/snapshots/biskotaki-gold-standard/docs/dev_guides/index.md',
        'tests/data/snapshots/biskotaki-gold-standard/docs/dockerfile_mermaid.md',
        'tests/data/snapshots/biskotaki-gold-standard/docs/index.md',
        'tests/data/snapshots/biskotaki-gold-standard/docs/tags.md',
        'tests/data/snapshots/biskotaki-gold-standard/LICENSE',
        'tests/data/snapshots/biskotaki-gold-standard/mkdocs.yml',
        # 'tests/data/snapshots/biskotaki-gold-standard/poetry.lock',
        'tests/data/snapshots/biskotaki-gold-standard/pyproject.toml',
        'tests/data/snapshots/biskotaki-gold-standard/README.rst',
        'tests/data/snapshots/biskotaki-gold-standard/scripts/gen_api_refs_pages.py',
        'tests/data/snapshots/biskotaki-gold-standard/scripts/parse_version.py',
        'tests/data/snapshots/biskotaki-gold-standard/scripts/visualize-dockerfile.py',
        'tests/data/snapshots/biskotaki-gold-standard/scripts/visualize-ga-workflow.py',
        'tests/data/snapshots/biskotaki-gold-standard/src/biskotakigold/cli.py',
        'tests/data/snapshots/biskotaki-gold-standard/src/biskotakigold/__init__.py',
        'tests/data/snapshots/biskotaki-gold-standard/src/biskotakigold/_logging.py',
        'tests/data/snapshots/biskotaki-gold-standard/src/biskotakigold/__main__.py',
        'tests/data/snapshots/biskotaki-gold-standard/src/biskotakigold/py.typed',
        'tests/data/snapshots/biskotaki-gold-standard/tests/smoke_test.py',
        'tests/data/snapshots/biskotaki-gold-standard/tests/test_cli.py',
        'tests/data/snapshots/biskotaki-gold-standard/tests/test_invoking_cli.py',
        'tests/data/snapshots/biskotaki-gold-standard/tox.ini',
        'tests/data/snapshots/biskotaki-interactive/CHANGELOG.rst',
        'tests/data/snapshots/biskotaki-interactive/CONTRIBUTING.md',
        'tests/data/snapshots/biskotaki-interactive/Dockerfile',
        'tests/data/snapshots/biskotaki-interactive/docs/conf.py',
        'tests/data/snapshots/biskotaki-interactive/docs/contents/10_introduction.rst',
        'tests/data/snapshots/biskotaki-interactive/docs/contents/20_why_this_package.rst',
        'tests/data/snapshots/biskotaki-interactive/docs/contents/30_usage.rst',
        'tests/data/snapshots/biskotaki-interactive/docs/contents/40_modules.rst',
        'tests/data/snapshots/biskotaki-interactive/docs/contents/biskotaki.rst',
        'tests/data/snapshots/biskotaki-interactive/docs/index.rst',
        'tests/data/snapshots/biskotaki-interactive/docs/make.bat',
        'tests/data/snapshots/biskotaki-interactive/docs/Makefile',
        'tests/data/snapshots/biskotaki-interactive/docs/spelling_wordlist.txt',
        'tests/data/snapshots/biskotaki-interactive/LICENSE',
        'tests/data/snapshots/biskotaki-interactive/pyproject.toml',
        'tests/data/snapshots/biskotaki-interactive/README.rst',
        'tests/data/snapshots/biskotaki-interactive/scripts/parse_version.py',
        'tests/data/snapshots/biskotaki-interactive/scripts/visualize-dockerfile.py',
        'tests/data/snapshots/biskotaki-interactive/scripts/visualize-ga-workflow.py',
        'tests/data/snapshots/biskotaki-interactive/src/biskotaki/__init__.py',
        'tests/data/snapshots/biskotaki-interactive/src/biskotaki/_logging.py',
        'tests/data/snapshots/biskotaki-interactive/src/biskotaki/py.typed',
        'tests/data/snapshots/biskotaki-interactive/tests/smoke_test.py',
        'tests/data/snapshots/biskotaki-interactive/tox.ini',
        'tests/data/snapshots/biskotaki-no-input/CHANGELOG.rst',
        'tests/data/snapshots/biskotaki-no-input/CONTRIBUTING.md',
        'tests/data/snapshots/biskotaki-no-input/Dockerfile',
        'tests/data/snapshots/biskotaki-no-input/docs/conf.py',
        'tests/data/snapshots/biskotaki-no-input/docs/contents/10_introduction.rst',
        'tests/data/snapshots/biskotaki-no-input/docs/contents/20_why_this_package.rst',
        'tests/data/snapshots/biskotaki-no-input/docs/contents/30_usage.rst',
        'tests/data/snapshots/biskotaki-no-input/docs/contents/40_modules.rst',
        'tests/data/snapshots/biskotaki-no-input/docs/contents/biskotaki.rst',
        'tests/data/snapshots/biskotaki-no-input/docs/index.rst',
        'tests/data/snapshots/biskotaki-no-input/docs/make.bat',
        'tests/data/snapshots/biskotaki-no-input/docs/Makefile',
        'tests/data/snapshots/biskotaki-no-input/docs/spelling_wordlist.txt',
        'tests/data/snapshots/biskotaki-no-input/LICENSE',
        # probably this was added accidentally, but when there is ci for maintaining modern locks
        # we shall uncomment
        # 'tests/data/snapshots/biskotaki-no-input/poetry.lock',
        'tests/data/snapshots/biskotaki-no-input/pyproject.toml',
        'tests/data/snapshots/biskotaki-no-input/README.rst',
        'tests/data/snapshots/biskotaki-no-input/scripts/parse_version.py',
        'tests/data/snapshots/biskotaki-no-input/scripts/visualize-dockerfile.py',
        'tests/data/snapshots/biskotaki-no-input/scripts/visualize-ga-workflow.py',
        'tests/data/snapshots/biskotaki-no-input/src/biskotaki/__init__.py',
        'tests/data/snapshots/biskotaki-no-input/src/biskotaki/_logging.py',
        'tests/data/snapshots/biskotaki-no-input/src/biskotaki/py.typed',
        'tests/data/snapshots/biskotaki-no-input/tests/smoke_test.py',
        'tests/data/snapshots/biskotaki-no-input/tox.ini',
        'tests/data/snapshots/README.md',
        'tests/data/test_cookiecutter.json',
        'tests/data/snapshots/biskotaki-gold-standard/.coveragerc',
        'tests/data/snapshots/biskotaki-gold-standard/.github/labeler.yml',
        'tests/data/snapshots/biskotaki-gold-standard/.github/workflows/cicd.yml',
        'tests/data/snapshots/biskotaki-gold-standard/.github/workflows/codecov-upload.yml',
        'tests/data/snapshots/biskotaki-gold-standard/.github/workflows/labeler.yaml',
        'tests/data/snapshots/biskotaki-gold-standard/.github/workflows/policy_lint.yml',
        'tests/data/snapshots/biskotaki-gold-standard/.github/workflows/signal-deploy.yml',
        'tests/data/snapshots/biskotaki-gold-standard/.gitignore',
        'tests/data/snapshots/biskotaki-gold-standard/.prospector.yml',
        'tests/data/snapshots/biskotaki-gold-standard/.pylintrc',
        'tests/data/snapshots/biskotaki-gold-standard/.readthedocs.yml',
        'tests/data/snapshots/biskotaki-interactive/.coveragerc',
        'tests/data/snapshots/biskotaki-interactive/.github/labeler.yml',
        'tests/data/snapshots/biskotaki-interactive/.github/workflows/cicd.yml',
        'tests/data/snapshots/biskotaki-interactive/.github/workflows/codecov-upload.yml',
        'tests/data/snapshots/biskotaki-interactive/.github/workflows/labeler.yaml',
        'tests/data/snapshots/biskotaki-interactive/.github/workflows/policy_lint.yml',
        'tests/data/snapshots/biskotaki-interactive/.github/workflows/signal-deploy.yml',
        'tests/data/snapshots/biskotaki-interactive/.gitignore',
        'tests/data/snapshots/biskotaki-interactive/.prospector.yml',
        'tests/data/snapshots/biskotaki-interactive/.pylintrc',
        'tests/data/snapshots/biskotaki-interactive/.readthedocs.yml',
        'tests/data/snapshots/biskotaki-no-input/.coveragerc',
        'tests/data/snapshots/biskotaki-no-input/.github/labeler.yml',
        'tests/data/snapshots/biskotaki-no-input/.github/workflows/cicd.yml',
        'tests/data/snapshots/biskotaki-no-input/.github/workflows/codecov-upload.yml',
        'tests/data/snapshots/biskotaki-no-input/.github/workflows/labeler.yaml',
        'tests/data/snapshots/biskotaki-no-input/.github/workflows/policy_lint.yml',
        'tests/data/snapshots/biskotaki-no-input/.github/workflows/signal-deploy.yml',
        'tests/data/snapshots/biskotaki-no-input/.gitignore',
        'tests/data/snapshots/biskotaki-no-input/.prospector.yml',
        'tests/data/snapshots/biskotaki-no-input/.pylintrc',
        'tests/data/snapshots/biskotaki-no-input/.readthedocs.yml',
        'tests/generator_defaults_shift/test_docs_settings.py',
        'tests/test_build_backend_sdist.py',
        'tests/test_ci_pipeline_generation.py',
        'tests/test_cli.py',
        'tests/test_cookiecutter_choice_var.py',
        'tests/test_cookiecutter_context.py',
        'tests/test_dialog_system.py',
        'tests/test_docs_gen_feat_compatibillity.py',
        'tests/test_error_classifier.py',
        'tests/test_generate.py',
        'tests/test_gold_standard.py',
        'tests/test_module.py',
        'tests/test_post_hook.py',
        'tests/test_prehook.py',
        'tests/test_running_test_suite.py',
        'tests/test_sanitization_component.py',
        'tests/test_sanity.py',
        'tests/test_snapshot_workflow_yaml.py',
    )
    # METADATA of this PROJECT
    METADATA = (
        'pyproject.toml',
        'README.md',
        'LICENSE',
        'CHANGELOG.rst',
        'CONTRIBUTING.md',
    )
    # Injected by Build Backend (Process)
    ADDED_METADATA = ('PKG-INFO',)
    return SRC + TESTS + METADATA + ADDED_METADATA


@pytest.fixture
def verify_file_size_within_acceptable_limits():
    class SizeAcceptanceCriteria(t.TypedDict):
        expected_size: t.Union[int, float]
        allowed_margin: t.Optional[t.Union[int, float]]

    def _verify_file_size_within_acceptable_limits(
        file: Path, size_acceptance_criteria: SizeAcceptanceCriteria
    ) -> t.Tuple[bool, t.Optional[str]]:
        expected_size = size_acceptance_criteria["expected_size"]
        allowed_margin = (
            size_acceptance_criteria.get("allowed_margin") or 500
        )  # default 500 Bytes

        lower_accepted = expected_size - allowed_margin
        upper_accepted = expected_size + allowed_margin

        runtime_tar_gz_size = file.stat().st_size

        accepted_size: bool = lower_accepted < runtime_tar_gz_size < upper_accepted
        return accepted_size, (
            f"Expected Distro to be {expected_size} +- {allowed_margin} Bytes: {lower_accepted} < x < {upper_accepted}. Got {runtime_tar_gz_size} {'>' if runtime_tar_gz_size > upper_accepted else '<'} {'UPPER' if runtime_tar_gz_size > upper_accepted else 'LOWER'}"
            if not accepted_size
            else None
        )

    return _verify_file_size_within_acceptable_limits


@pytest.fixture
def is_path_traversal_safe():
    """
    Canonicalizes both paths and ensures `target` is strictly inside `base`.
    """

    def _is_path_traversal_safe(base: Path, target: Path) -> bool:
        """
        Canonicalizes both paths and ensures `target` is strictly inside `base`.
        """
        try:
            base_resolved = base.resolve(strict=False)
            target_resolved = target.resolve(strict=False)
        except FileNotFoundError:
            return False

        return str(target_resolved).startswith(str(base_resolved))

    return _is_path_traversal_safe


@pytest.fixture
def create_safe_extract():
    """
    Safely extract tarfile members to the specified path.
    Ensures no file escapes the target directory.
    """
    import re
    import tarfile

    class TarMembersValidator:
        def __init__(self, is_path_traversal_safe: t.Callable[[Path, Path], bool]):
            self.is_path_traversal_safe = is_path_traversal_safe

        def validate_tar_members(
            self, tar: tarfile.TarFile, base_path: Path
        ) -> t.Iterator[tarfile.TarInfo]:
            # Location to extract to
            base_path = base_path.resolve(strict=False)

            for member in tar.getmembers():
                # File Path after extraction
                member_path = base_path / member.name

                # Normalize and reject absolute paths and traversal
                if not self.is_path_traversal_safe(base_path, member_path):
                    raise ValueError(f"Unsafe path detected in tar file: {member.name}")

                # Optional: block symlinks inside tar to ensure secure extraction
                if member.issym() or member.islnk():
                    raise ValueError(f"Symlink not allowed: {member.name}")

                # Optional: sanitize explicitly (fails fast on traversal hints)
                if (
                    # 1. Detect invalid characters or sequences commonly used in traversal attacks.
                    member.name is None
                    or any([x in member.name for x in {"..", "\\"}])
                    or
                    # 2. Enforce strict whitelist pattern. Adjust pattern as necessary.
                    any(
                        [
                            re.fullmatch(r"[a-zA-Z0-9_.\- {}%=\"]+", x) is None
                            for x in member.name.split("/")
                        ]
                    )
                ):
                    # Extra: Use only allowed filenames if applicable
                    raise ValueError(f"Invalid file name '{member.name}'")

                yield member

        def __call__(self, tar: tarfile.TarFile, path: Path):
            """
            Safely extract tar file into the given path using validated members.
            """
            path = path.resolve(strict=False)
            tar.extractall(path=path, members=self.validate_tar_members(tar, path))

    return lambda is_path_traversal_safe: TarMembersValidator(is_path_traversal_safe)


@pytest.fixture
def assert_sdist_exact_file_structure(
    create_safe_extract, is_path_traversal_safe, tmp_path: Path
):
    def _verify_sdist_file_structure(
        sdist_built_at_runtime: Path, expected_file_structure: t.Tuple[str]
    ):
        # Extract the tar.gz file to a temporary directory
        extracted_from_tar_gz = tmp_path / "extracted_from_tar_gz"
        import tarfile

        my_safe_extract = create_safe_extract(is_path_traversal_safe)

        with tarfile.open(sdist_built_at_runtime, "r:gz") as tar:
            my_safe_extract(tar, extracted_from_tar_gz)

        from cookiecutter_python import __version__

        # if verion includes metadata (ie 1.2.5-dev) then we must match 1.2.5.dev0 !
        if '-' in __version__:
            DISTRO_NAME_AS_IN_SITE_PACKAGES = (
                f'cookiecutter_python-{__version__.split("-")[0]}.{__version__.split("-")[1]}0'
            )
        else:
            DISTRO_NAME_AS_IN_SITE_PACKAGES = f'cookiecutter_python-{__version__}'

        # Relative Paths extracted from tar.gz
        runtime_files = [
            file.relative_to(extracted_from_tar_gz / DISTRO_NAME_AS_IN_SITE_PACKAGES)
            for file in extracted_from_tar_gz.rglob("*")
            if file.is_file()
        ]

        # Verify all expected files are present
        missing_files = set(map(Path, expected_file_structure)) - set(runtime_files)
        assert missing_files == set(), (
            "Expected no missing files compared to expected Source Distribution file structure, "
            "got [" + '\n'.join(map(str, missing_files)) + "]"
        )

        # Verify no extra files are present
        extra_runtime_files = set(runtime_files) - set(map(Path, expected_file_structure))
        assert extra_runtime_files == set(), (
            "Expected no extra runtime files compared to expectations, "
            "got [" + '\n'.join(map(str, sorted(extra_runtime_files))) + "]"
        )

        # NOW we have asserted that expected and runtime File structure are identical

    return _verify_sdist_file_structure


######## uv + poetry as build backend ########
@pytest.fixture(scope="module")
def sdist_built_at_runtime_with_uv(my_run_subprocess) -> Path:
    """Build project (at runtime) with 'uv', and return SDist tar.gz file."""
    # Create a temporary directory
    import tempfile
    import typing as t

    tmp_path = Path(tempfile.mkdtemp())
    OUT_DIR = tmp_path / "dist-unit-test-sdist_built_at_runtime"
    # Get distro_path: ie '/site-packages/cookiecutter_python'
    # import cookiecutter_python
    # distro_path = Path(cookiecutter_python.__file__).parent.absolute()
    project_path = Path(__file__).parent.parent
    import sys

    # result = run_subprocess('uv', 'python', 'pin', sys.executable, check=False)
    # assert result.exit_code == 0, f"Expected exit code 0, got {result.exit_code}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\n"
    # invoke uv as build frontend to whatever [build-system] is in pyproject.toml
    COMMAND_LINE_ARGS: t.List[str] = [
        # 'uv', 'python', 'pin', sys.executable, '&&',
        "uv",
        "build",
        "--python",
        sys.executable,
        "--sdist",
        "--out-dir",
        str(OUT_DIR),
        str(project_path),
    ]
    result = my_run_subprocess(*COMMAND_LINE_ARGS, check=False)

    import re

    print()
    print("==========")
    print(result.stdout)
    print("==========")
    print(result.stderr)
    print("==========")
    assert (
        result.exit_code == 0
    ), f"Expected exit code 0, got {result.exit_code}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\n"

    # THIS IS ONLY FOR UV BUILD CMD
    assert re.search(r"Building source distribution\.\.\.", result.stderr)
    pattern = r"Successfully built .+cookiecutter_python-.+\.tar\.gz"
    assert re.search(pattern, result.stderr)

    # After build, retrieve the tar.gz file
    tar_gz_file = list(OUT_DIR.glob("*.tar.gz"))
    assert len(tar_gz_file) == 1, f"Expected 1 tar.gz file, got {len(tar_gz_file)}"
    assert tar_gz_file[0].is_file(), f"Expected {tar_gz_file[0]} to be a file"
    return tar_gz_file[0]


## Test SDist Tar GZ file Size is within Acceptable Limits
@pytest.mark.requires_uv
def test_sdist_tar_gz_file_size_is_within_acceptable_lower_and_upper_limits_when_produced_via_uv_frontend(
    # GIVEN we invoke our current build backend to create a source distribution
    sdist_built_at_runtime_with_uv: Path,
    verify_file_size_within_acceptable_limits: t.Callable[
        [Path, t.Dict[str, t.Union[int, float]]], t.Tuple[bool, t.Optional[str]]
    ],
):
    # Observed: [380KB, 442KB]
    observations = (
        380,
        442,
    )
    AVG = sum(observations) / len(observations)
    (
        tar_gz_file_size_within_acceptable_limits,
        assertion_error_message,
    ) = verify_file_size_within_acceptable_limits(
        sdist_built_at_runtime_with_uv,
        {
            # Observed: [380KB, 442KB]
            "expected_size": AVG * 1024,  # average of observed sizes
            "allowed_margin": 100 * 1024,  # 10KB
        },
    )
    assert tar_gz_file_size_within_acceptable_limits, assertion_error_message


## VERIFY SDIST FILE STRUCTURE TO BE EXACTLY AS EXPECTED ##
@pytest.mark.requires_uv
def test_sdist_includes_dirs_and_files_exactly_as_expected_when_produced_via_uv_frontend(
    sdist_built_at_runtime_with_uv: Path,
    sdist_expected_correct_file_structure: t.Tuple[str],
    assert_sdist_exact_file_structure,
):
    assert_sdist_exact_file_structure(
        sdist_built_at_runtime_with_uv, sdist_expected_correct_file_structure
    )


######## Build + poetry as build backend ########
@pytest.fixture(scope="module")
def sdist_built_at_runtime_with_build(my_run_subprocess) -> Path:
    """Build project (at runtime) with 'build module', and return SDist tar.gz file."""
    # Create a temporary directory
    import tempfile
    import typing as t

    temp_dir: str = tempfile.mkdtemp()

    OUT_DIR = Path(temp_dir) / "unit-test-sdist_built_at_runtime_with_build"
    # Get distro_path: ie '/site-packages/cookiecutter_python'
    # import cookiecutter_python
    # distro_path = Path(cookiecutter_python.__file__).parent.absolute()
    project_path = Path(__file__).parent.parent

    # invoke build module as frontend to whatever [build-system] is in pyproject.toml
    import sys

    PYTHON = sys.executable  # python from virtualenv
    COMMAND_LINE_ARGS: t.List[str] = [
        PYTHON,
        "-m",
        "build",
        "--sdist",
        "--outdir",
        str(OUT_DIR),
        str(project_path),
    ]
    result = my_run_subprocess(*COMMAND_LINE_ARGS, check=False)

    print()
    print("==========")
    print(result.stdout)
    print("==========")
    print(result.stderr)
    print("==========")
    assert result.exit_code == 0, f"Expected exit code 0, got {result.exit_code}"

    import re

    assert re.search(r"Building sdist\.\.\.", result.stdout)
    pattern = "Successfully built .*cookiecutter_python-.+\.tar\.gz"
    assert re.search(pattern, result.stdout)

    # After build, retrieve the tar.gz file
    tar_gz_file = list(OUT_DIR.glob("*.tar.gz"))
    assert len(tar_gz_file) == 1, f"Expected 1 tar.gz file, got {len(tar_gz_file)}"
    assert tar_gz_file[0].is_file(), f"Expected {tar_gz_file[0]} to be a file"
    return tar_gz_file[0]


## Test SDist Tar GZ file Size is within Acceptable Limits
@pytest.mark.slow
def test_sdist_tar_gz_file_size_is_within_acceptable_lower_and_upper_limits_when_produced_via_build_module_frontend(
    # GIVEN we invoke our current build backend to create a source distribution
    sdist_built_at_runtime_with_build: Path,
    verify_file_size_within_acceptable_limits: t.Callable[
        [Path, t.Dict[str, t.Union[int, float]]], t.Tuple[bool, t.Optional[str]]
    ],
):
    # Observed: [379KB, 442KB, 388]
    observations = (
        379,
        442,
        388,
    )
    AVG = sum(observations) / len(observations)

    (
        tar_gz_file_size_within_acceptable_limits,
        assertion_error_message,
    ) = verify_file_size_within_acceptable_limits(
        sdist_built_at_runtime_with_build,
        {
            "expected_size": AVG * 1024,  # Bytes
            "allowed_margin": 100 * 1024,  # 100KB
        },
    )
    assert tar_gz_file_size_within_acceptable_limits, assertion_error_message


## VERIFY SDIST FILE STRUCTURE TO BE AS EXPECTED ##
@pytest.mark.slow
def test_sdist_includes_dirs_and_files_exactly_as_expected_when_produced_via_build_module_frontend(
    sdist_built_at_runtime_with_build: Path,
    sdist_expected_correct_file_structure: t.Tuple[str],
    assert_sdist_exact_file_structure,
):
    assert_sdist_exact_file_structure(
        sdist_built_at_runtime_with_build, sdist_expected_correct_file_structure
    )
