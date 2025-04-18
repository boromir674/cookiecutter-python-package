from pathlib import Path

import pytest


def test_git_status_porcelain_subprocess_fails_with_check_equals_false(
    my_run_subprocess, tmp_path: Path
):
    """Test that git status --porcelain returns an error when not in a git directory."""
    # GIVEN a directory that is NOT a git repository
    non_git_folder = (tmp_path / 'non_git_dir').resolve().absolute()
    non_git_folder.mkdir()

    # WHEN running git status --porcelain
    result = my_run_subprocess(
        'git',
        *['status', '--porcelain'],
        cwd=str(non_git_folder),
        check=False,  # prevent raising exception
    )
    # THEN the command should return an error
    assert result.stdout == ''
    assert 'fatal: not a git repository' in result.stderr
    assert result.exit_code != 0


def test_git_status_porcelain_subprocess_fails_with_check_equals_true(
    my_run_subprocess, tmp_path: Path
):
    """Test that git status --porcelain raises an exception when not in a git directory."""
    # GIVEN a directory that is NOT a git repository
    non_git_folder = (tmp_path / 'non_git_dir').resolve().absolute()
    non_git_folder.mkdir()

    # WHEN running git status --porcelain
    from subprocess import CalledProcessError

    with pytest.raises(
        CalledProcessError,
        match=r"Command '\['git', 'status', '--porcelain'\]' returned non-zero exit status 128.",
    ):
        _ = my_run_subprocess(
            'git',
            *['status', '--porcelain'],
            cwd=str(non_git_folder),
            check=True,
        )


def test_git_porcelain_after_git_init(tmp_path: Path):
    # GIVEN a directory with one file inside
    git_folder = (tmp_path / 'non_git_dir').resolve().absolute()
    git_folder.mkdir()

    # place one a.txt file inside
    (git_folder / 'a.txt').touch()

    # GIVEN it is initialized as a git repository
    from git import Repo

    repo = Repo.init(f"{git_folder}")
    assert (git_folder / '.git').exists()
    assert (git_folder / '.git').is_dir()

    # WHEN running git status --porcelain
    result = repo.git.status(porcelain=True)

    # THEN the command should return an empty string
    assert result == '?? a.txt'
    assert repo.is_dirty() is False


def test_git_porcelain_after_git_init_with_subprocess(my_run_subprocess, tmp_path):
    # GIVEN a directory with one file inside
    git_folder: Path = (tmp_path / 'non_git_dir').resolve().absolute()
    git_folder.mkdir()

    # place one a.txt file inside
    (git_folder / 'a.txt').touch()

    # GIVEN it is initialized as a git repository
    result = my_run_subprocess(
        'git',
        *['init'],
        cwd=str(git_folder),
        check=True,  # prevent raising exception
    )
    assert (git_folder / '.git').exists()
    assert (git_folder / '.git').is_dir()

    result = my_run_subprocess(
        'git',
        *['status', '--porcelain'],
        cwd=str(git_folder),
        check=False,  # prevent raising exception
    )

    assert result.exit_code == 0
    assert result.stdout == '?? a.txt\n'
    assert result.stderr == ''


def test_git_porcelain_after_git_init_with_subprocess_v2(my_run_subprocess, tmp_path):
    # GIVEN a directory with one file inside
    git_folder: Path = (tmp_path / 'non_git_dir').resolve().absolute()
    git_folder.mkdir()

    # place one a.txt file inside
    (git_folder / 'a.txt').touch()

    # GIVEN it is initialized as a git repository
    from git import Repo

    _ = Repo.init(f"{git_folder}")
    assert (git_folder / '.git').exists()
    assert (git_folder / '.git').is_dir()

    result = my_run_subprocess(
        'git',
        *['status', '--porcelain'],
        cwd=str(git_folder),
        check=False,  # prevent raising exception
    )

    assert result.exit_code == 0
    assert result.stdout == '?? a.txt\n'
    assert result.stderr == ''
