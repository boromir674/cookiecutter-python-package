"""Unit tests for gen_docs_common.py"""

from pathlib import Path
from unittest.mock import patch

import pytest

from cookiecutter_python.backend.gen_docs_common import get_docs_gen_internal_config


@pytest.fixture
def mock_correct_proj_template_dir(tmp_path: Path) -> Path:
    """Fixture to create a mock project template directory."""
    docs_mkdocs = tmp_path / "docs-mkdocs"
    docs_sphinx = tmp_path / "docs-sphinx"
    docs_newbuilder = tmp_path / "docs-newbuilder"
    docs_mkdocs.mkdir()
    docs_sphinx.mkdir()
    docs_newbuilder.mkdir()
    return tmp_path


@pytest.fixture
def mock_wrong_proj_template_dir(tmp_path: Path) -> Path:
    """Fixture to create a mock project template directory."""
    docs_mkdocs = tmp_path / "docs-mkdocs"
    docs_sphinx = tmp_path / "docs-sphinx"
    invalid_docs = tmp_path / "docs-invalid-folder"
    docs_mkdocs.mkdir()
    docs_sphinx.mkdir()
    invalid_docs.mkdir()
    return tmp_path


def test_get_docs_gen_internal_config_valid(mock_correct_proj_template_dir: Path):
    """Test that valid docs folders are correctly mapped."""
    with patch(
        "cookiecutter_python.backend.gen_docs_common.PROJ_TEMPLATE_DIR",
        mock_correct_proj_template_dir,
    ):
        result = get_docs_gen_internal_config()
        assert result == {
            "mkdocs": "docs-mkdocs",
            "sphinx": "docs-sphinx",
            "newbuilder": "docs-newbuilder",
        }


@pytest.mark.xfail(
    reason="This tests new requirements, but app code is not adjusted yet"
)
def test_get_docs_gen_internal_config_invalid_folder_name(
    mock_wrong_proj_template_dir: Path,
):
    """Test that invalid folder names raise a ValueError."""
    _invalid_folder = mock_wrong_proj_template_dir / "docs-invalid-folder"  # noqa: F841
    # invalid_folder.rename(mock_proj_template_dir / "docs_invalid")
    with patch(
        "cookiecutter_python.backend.gen_docs_common.PROJ_TEMPLATE_DIR",
        mock_wrong_proj_template_dir,
    ):
        with pytest.raises(
            ValueError, match="Docs Tempate Folder name, does not follow proper pattern"
        ):
            get_docs_gen_internal_config()


@pytest.mark.xfail(
    reason="This tests new requirements, but app code is not adjusted yet"
)
def test_get_docs_gen_internal_config_empty_directory(tmp_path: Path):
    """Test that an empty directory raises an assertion error."""
    from cookiecutter_python.backend.gen_docs_common import NoDocsTemplateFolderError  # type: ignore[attr-defined]

    with patch(
        "cookiecutter_python.backend.gen_docs_common.PROJ_TEMPLATE_DIR", tmp_path
    ):
        with pytest.raises(NoDocsTemplateFolderError, match="templated_proj_folder"):
            get_docs_gen_internal_config()
