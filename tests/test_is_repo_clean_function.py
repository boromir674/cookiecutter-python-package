from pathlib import Path


def test_is_git_repo_clean_returns_true_for_new_repo(my_run_subprocess, tmp_path: Path):
    # GIVEN a directory with one file inside
    git_folder = (tmp_path / 'non_git_dir').resolve().absolute()
    git_folder.mkdir()
    (git_folder / 'a.txt').touch()

    # GIVEN it is initialized as a git repository
    from git import Repo

    repo = Repo.init(f"{git_folder}")
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

    # WHEN calling is_git_repo_clean function
    repo_is_clean = not repo.is_dirty()

    # THEN the command should return True
    assert repo_is_clean is True
