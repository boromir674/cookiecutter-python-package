import sys


def test_simple_invocation(get_cli_invocation):
    result = get_cli_invocation(
        sys.executable,
        '-m',
        'cookiecutter_python',
        '--help',
    )
    assert result.exit_code == 0
    assert result.stdout.split('\n')[0] == 'Usage: generate-python [OPTIONS]'
    assert result.stderr == ''


def test_importing(get_object):
    main_in__main__namespace = get_object('main', 'cookiecutter_python.__main__')
    assert '__call__' in dir(main_in__main__namespace)
