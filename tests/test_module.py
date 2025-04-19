import re
import sys


def test_simple_invocation(run_subprocess):
    result = run_subprocess(
        sys.executable,
        '-m',
        'cookiecutter_python',
        '--help',
    )
    assert result.exit_code == 0
    assert re.match(r'Usage: generate\-python \[OPTIONS\]', result.stdout.split('\n')[0])
    assert result.stderr == ''


def test_importing(get_object):
    main_in__main__namespace = get_object('main', 'cookiecutter_python.__main__')
    assert '__call__' in dir(main_in__main__namespace)
