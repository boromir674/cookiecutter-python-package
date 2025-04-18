from pathlib import Path


def test_git_sdk_init(tmp_path: Path):
    from git import Repo

    # GIVEN a temporary empty folder
    project_folder = tmp_path / "unit_test_git_sdk_init"
    project_folder.mkdir(parents=True, exist_ok=True)
    # sanity that no files exist
    assert not any(project_folder.iterdir())
    # WHEN we call the git_sdk_init function
    _ = Repo.init(project_folder)
    # THEN a .git folder should be created
    assert (project_folder / ".git").exists()


def test_git_sdk_is_dirty(tmp_path: Path):
    from git import Repo

    # GIVEN a temporary empty folder
    project_folder = tmp_path / "unit_test_git_sdk_is_dirty"
    project_folder.mkdir(parents=True, exist_ok=True)
    # sanity that no files exist
    assert not any(project_folder.iterdir())
    # WHEN we call the git_sdk_init function
    repo = Repo.init(project_folder)
    # THEN a .git folder should be created
    assert (project_folder / ".git").exists()
    print("\n" + str(project_folder))
    # WHEN we create a new file
    new_file = project_folder / "test_file.txt"
    new_file.write_text("Hello World!")

    # WHEN we check if the repo is dirty
    assert not repo.is_dirty()

    # cw = repo.config_writer()

    # # Access the global configuration writer
    # WARNING THIS destroys the format of .gitconfig and remove comments !!!!
    # with repo.config_writer(config_level='global') as cw:
    #     # Add the safe.directory entry
    #     cw.add_value('safe', 'directory', str(project_folder))

    # cr = repo.config_reader()  # use reader to assert writer effect
