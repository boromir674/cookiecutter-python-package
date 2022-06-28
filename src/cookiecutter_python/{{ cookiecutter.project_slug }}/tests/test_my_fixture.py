def test_fixture(testdir):
    testdir.makepyfile(
        """
    import pytest

    def test_fixture(my_fixture):

        assert my_fixture == 'Implement Me!'
    """
    )
    result = testdir.runpytest("--verbose")
    result.stdout.fnmatch_lines("test_fixture.py::test_fixture PASSED*")
