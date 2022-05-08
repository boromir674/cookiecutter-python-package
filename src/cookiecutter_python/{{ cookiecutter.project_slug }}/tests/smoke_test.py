def test_smoke_is_not_risingfrom_module():
    import {{ cookiecutter.pkg_name }}

    assert {{ cookiecutter.pkg_name }} is not None
