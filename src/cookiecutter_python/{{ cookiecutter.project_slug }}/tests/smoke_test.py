def test_import_module():
    import {{ cookiecutter.pkg_name }}

    assert {{ cookiecutter.pkg_name }} is not None
